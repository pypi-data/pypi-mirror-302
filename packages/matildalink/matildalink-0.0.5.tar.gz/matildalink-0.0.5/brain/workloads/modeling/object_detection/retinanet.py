import tensorflow as tf, tf_keras
from typing import Optional, Mapping, Union, Sequence, Tuple, Any
import collections

from official.vision.modeling import backbones
from official.vision.modeling import retinanet_model
from official.vision.modeling.decoders.fpn import FPN
from official.vision.modeling.heads import dense_prediction_heads
from official.vision.modeling.layers import detection_generator as detect_gen
from official.vision.ops import anchor
from official.vision.losses import focal_loss, loss_utils


class MLBRetinaNet(tf_keras.Model):

    def __init__(
        self,
        input_specs: tf_keras.layers.InputSpec,
        model_config,
        backbone: Optional[tf_keras.Model] = None,
        l2_regularizer: Optional[tf_keras.regularizers.Regularizer] = None,
        anchor_boxes: Mapping[str, tf.Tensor] | None = None,
        **kwargs
    ):

        super(MLBRetinaNet, self).__init__(**kwargs)

        norm_activation_config = model_config.norm_activation
        if not backbone:
            backbone = backbones.ResNet(18, input_specs=input_specs)
        backbone_features = backbone(tf_keras.Input(input_specs.shape[1:]))

        decoder = FPN(input_specs=backbone.output_specs)

        head_config = model_config.head
        generator_config = model_config.detection_generator
        num_anchors_per_location = len(model_config.anchor.aspect_ratios) * model_config.anchor.num_scales

        head = dense_prediction_heads.RetinaNetHead(
            min_level=model_config.min_level,
            max_level=model_config.max_level,
            num_classes=model_config.num_classes,
            num_anchors_per_location=num_anchors_per_location,
            num_convs=head_config.num_convs,
            num_filters=head_config.num_filters,
            attribute_heads=[
                cfg.as_dict() for cfg in (head_config.attribute_heads or [])
            ],
            share_classification_heads=head_config.share_classification_heads,
            use_separable_conv=head_config.use_separable_conv,
            activation=norm_activation_config.activation,
            use_sync_bn=norm_activation_config.use_sync_bn,
            norm_momentum=norm_activation_config.norm_momentum,
            norm_epsilon=norm_activation_config.norm_epsilon,
            kernel_regularizer=l2_regularizer,
            share_level_convs=head_config.share_level_convs,
        )

        # Builds decoder and head so that their trainable weights are initialized
        if decoder:
            decoder_features = decoder(backbone_features)
            _ = head(decoder_features)

        # Add `input_image_size` into `tflite_post_processing_config`.
        tflite_post_processing_config = (
            generator_config.tflite_post_processing.as_dict()
        )
        tflite_post_processing_config['input_image_size'] = (
            input_specs.shape[1],
            input_specs.shape[2],
        )
        detection_generator_obj = detect_gen.MultilevelDetectionGenerator(
            apply_nms=generator_config.apply_nms,
            pre_nms_top_k=generator_config.pre_nms_top_k,
            pre_nms_score_threshold=generator_config.pre_nms_score_threshold,
            nms_iou_threshold=generator_config.nms_iou_threshold,
            max_num_detections=generator_config.max_num_detections,
            nms_version=generator_config.nms_version,
            use_cpu_nms=generator_config.use_cpu_nms,
            soft_nms_sigma=generator_config.soft_nms_sigma,
            tflite_post_processing_config=tflite_post_processing_config,
            return_decoded=generator_config.return_decoded,
            use_class_agnostic_nms=generator_config.use_class_agnostic_nms,
            box_coder_weights=generator_config.box_coder_weights,
        )

        num_scales = None
        aspect_ratios = None
        anchor_size = None
        if anchor_boxes is None:
            num_scales = model_config.anchor.num_scales
            aspect_ratios = model_config.anchor.aspect_ratios
            anchor_size = model_config.anchor.anchor_size
        self._config_dict = {
            'backbone': backbone,
            'decoder': decoder,
            'head': head,
            'detection_generator': detection_generator_obj,
            'min_level': model_config.min_level,
            'max_level': model_config.max_level,
            'num_scales': num_scales,
            'aspect_ratios': aspect_ratios,
            'anchor_size': anchor_size
        }

        self._backbone = backbone
        self._decoder = decoder
        self._head = head
        self._detection_generator = detection_generator_obj
        self._anchor_boxes = anchor_boxes
        self._num_classes = model_config.num_classes
        

    @tf.function
    def call(
        self,
        images: Union[tf.Tensor, Sequence[tf.Tensor]],
        image_shape: Optional[tf.Tensor] = None,
        anchor_boxes: Mapping[str, tf.Tensor] | None = None,
        output_intermediate_features: bool = False,
        training: bool = None) -> Mapping[str, tf.Tensor]:

        outputs = {}
        # Feature extraction.
        features = self._backbone(images)
        if output_intermediate_features:
            outputs.update(
                {'backbone_{}'.format(k): v for k, v in features.items()})
        if self._decoder:
            features = self._decoder(features)
        if output_intermediate_features:
            outputs.update(
                {'decoder_{}'.format(k): v for k, v in features.items()})

        # Dense prediction. `raw_attributes` can be empty.
        raw_scores, raw_boxes, raw_attributes = self._head(features)
        outputs.update({
            'cls_outputs': raw_scores,
            'box_outputs': raw_boxes,
        })

        if training:
            if raw_attributes:
                outputs.update({'attribute_outputs': raw_attributes})
            return outputs
        else:
            if self._anchor_boxes is not None:
                batch_size = tf.shape(raw_boxes[str(self._config_dict['min_level'])])[0]
                anchor_boxes = collections.OrderedDict()
                for level, boxes in self._anchor_boxes.items():
                    anchor_boxes[level] = tf.tile(boxes[None, ...], [batch_size, 1, 1, 1])
            elif anchor_boxes is None:
            # Generate anchor boxes for this batch if not provided.
                if isinstance(images, Sequence):
                    primary_images = images[0]
                elif isinstance(images, tf.Tensor):
                    primary_images = images
                else:
                    raise ValueError(
                        'Input should be a tf.Tensor or a sequence of tf.Tensor, not {}.'
                        .format(type(images)))

            _, image_height, image_width, _ = primary_images.get_shape().as_list()
            anchor_boxes = anchor.Anchor(
                min_level=self._config_dict['min_level'],
                max_level=self._config_dict['max_level'],
                num_scales=self._config_dict['num_scales'],
                aspect_ratios=self._config_dict['aspect_ratios'],
                anchor_size=self._config_dict['anchor_size'],
                image_size=(image_height, image_width)).multilevel_boxes
            for l in anchor_boxes:
                anchor_boxes[l] = tf.tile(
                    tf.expand_dims(anchor_boxes[l], axis=0),
                    [tf.shape(primary_images)[0], 1, 1, 1])

        # Post-processing.
        final_results = self._detection_generator(raw_boxes, raw_scores,
                                                anchor_boxes, image_shape,
                                               raw_attributes)
        def _update_decoded_results():
            outputs.update({
            'decoded_boxes': final_results['decoded_boxes'],
            'decoded_box_scores': final_results['decoded_box_scores'],
            })
            if final_results.get('decoded_box_attributes') is not None:
                outputs['decoded_box_attributes'] = final_results[
                    'decoded_box_attributes'
                ]

        if self._detection_generator.get_config()['apply_nms']:
            outputs.update({
            'detection_boxes': final_results['detection_boxes'],
            'detection_scores': final_results['detection_scores'],
            'detection_classes': final_results['detection_classes'],
            'num_detections': final_results['num_detections'],
            })

        # Users can choose to include the decoded results (boxes before NMS) in
        # the output tensor dict even if `apply_nms` is set to `True`.
            if self._detection_generator.get_config()['return_decoded']:
                _update_decoded_results()
        else:
            _update_decoded_results()

        if raw_attributes:
            outputs.update({
            'attribute_outputs': raw_attributes,
            'detection_attributes': final_results['detection_attributes'],
            })

        return outputs

    def train_step(
        self,
        inputs: Tuple[Any, Any],
    ):

        features, labels = inputs

        with tf.GradientTape() as tape:

            outputs = self(features)
            trainable_var = self.trainable_variables

            cls_loss_fn = focal_loss.FocalLoss(alpha=0.25, gamma=1.5, reduction=tf_keras.losses.Reduction.SUM)
            box_loss_fn = tf_keras.losses.Huber(0.1, reduction=tf_keras.losses.Reduction.SUM)

            cls_sample_weight = labels['cls_weights']
            box_sample_weight = labels['box_weights']

            num_positives = tf.reduce_sum(box_sample_weight) + 1.0

            cls_sample_weight = cls_sample_weight / num_positives
            box_sample_weight = box_sample_weight / num_positives

            y_true_cls = loss_utils.multi_level_flatten(
                labels['cls_targets'], last_dim=None)
            y_true_cls = tf.one_hot(y_true_cls, self._num_classes)
            y_pred_cls = loss_utils.multi_level_flatten(
                outputs['cls_outputs'], last_dim=self._num_classes)
            y_true_box = loss_utils.multi_level_flatten(
                labels['box_targets'], last_dim=4)
            y_pred_box = loss_utils.multi_level_flatten(
                outputs['box_outputs'], last_dim=4)

            cls_loss = cls_loss_fn(
                y_true=y_true_cls, y_pred=y_pred_cls, sample_weight=cls_sample_weight)
            box_loss = box_loss_fn(
                y_true=y_true_box, y_pred=y_pred_box, sample_weight=box_sample_weight)

            loss = cls_loss + 50 * box_loss # box_loss_weight = 50

            grads = tape.gradient(loss, trainable_var)

        return grads
