import tensorflow as tf, tf_keras

from typing import Optional, Mapping, Tuple, Any

from official.vision.configs import maskrcnn as maskrcnn_cfg
from official.vision.ops import box_ops, anchor
from official.vision.losses import maskrcnn_losses
from official.vision.modeling import backbones, decoders
from official.vision.modeling import maskrcnn_model
from official.vision.modeling.heads import dense_prediction_heads
from official.vision.modeling.heads import dense_prediction_heads
from official.vision.modeling.heads import instance_heads
from official.vision.modeling.heads import segmentation_heads
from official.vision.modeling.layers import detection_generator
from official.vision.modeling.layers import mask_sampler
from official.vision.modeling.layers import roi_aligner
from official.vision.modeling.layers import roi_generator
from official.vision.modeling.layers import roi_sampler

class MLBMaskRCNN(tf_keras.Model):

    def __init__(
        self,
        input_specs: tf_keras.layers.InputSpec,
        model_config: maskrcnn_cfg.MaskRCNN,
        l2_regularizer: Optional[tf_keras.regularizers.Regularizer] = None,
        backbone: Optional[tf_keras.Model] = None,
        decoder: Optional[tf_keras.Model] = None,
        **kwargs
    ):

        super(MLBMaskRCNN, self).__init__(**kwargs)

        norm_activation_config = model_config.norm_activation

        if not backbone:
            backbone = backbones.ResNet(18, input_specs=input_specs)

        backbone_features = backbone(tf_keras.Input(input_specs.shape[1:]))

        decoder = decoders.FPN(input_specs=backbone.output_specs)

        rpn_head_config = model_config.rpn_head
        roi_generator_config = model_config.roi_generator
        roi_sampler_config = model_config.roi_sampler
        roi_aligner_config = model_config.roi_aligner
        detection_head_config = model_config.detection_head
        generator_config = model_config.detection_generator
        num_anchors_per_location = len(model_config.anchor.aspect_ratios) * model_config.anchor.num_scales

        rpn_head = dense_prediction_heads.RPNHead(
            min_level=model_config.min_level,
            max_level=model_config.max_level,
            num_anchors_per_location=num_anchors_per_location,
            num_convs=rpn_head_config.num_convs,
            num_filters=rpn_head_config.num_filters,
            use_separable_conv=rpn_head_config.use_separable_conv,
            activation=norm_activation_config.activation,
            use_sync_bn=norm_activation_config.use_sync_bn,
            norm_momentum=norm_activation_config.norm_momentum,
            norm_epsilon=norm_activation_config.norm_epsilon,
            kernel_regularizer=l2_regularizer)

        detection_head = instance_heads.DetectionHead(
            num_classes=model_config.num_classes,
            num_convs=detection_head_config.num_convs,
            num_filters=detection_head_config.num_filters,
            use_separable_conv=detection_head_config.use_separable_conv,
            num_fcs=detection_head_config.num_fcs,
            fc_dims=detection_head_config.fc_dims,
            class_agnostic_bbox_pred=detection_head_config.class_agnostic_bbox_pred,
            activation=norm_activation_config.activation,
            use_sync_bn=norm_activation_config.use_sync_bn,
            norm_momentum=norm_activation_config.norm_momentum,
            norm_epsilon=norm_activation_config.norm_epsilon,
            kernel_regularizer=l2_regularizer,
            name='detection_head')

        if decoder:
            decoder_features = decoder(backbone_features)
            rpn_head(decoder_features)

        if roi_sampler_config.cascade_iou_thresholds:
            detection_head_cascade = [detection_head]
            for cascade_num in range(len(roi_sampler_config.cascade_iou_thresholds)):
                detection_head = instance_heads.DetectionHead(
                    num_classes=model_config.num_classes,
                    num_convs=detection_head_config.num_convs,
                    num_filters=detection_head_config.num_filters,
                    use_separable_conv=detection_head_config.use_separable_conv,
                    num_fcs=detection_head_config.num_fcs,
                    fc_dims=detection_head_config.fc_dims,
                    class_agnostic_bbox_pred=detection_head_config
                    .class_agnostic_bbox_pred,
                    activation=norm_activation_config.activation,
                    use_sync_bn=norm_activation_config.use_sync_bn,
                    norm_momentum=norm_activation_config.norm_momentum,
                    norm_epsilon=norm_activation_config.norm_epsilon,
                    kernel_regularizer=l2_regularizer,
                    name='detection_head_{}'.format(cascade_num + 1))
                detection_head_cascade.append(detection_head)
            detection_head = detection_head_cascade

        roi_generator_obj = roi_generator.MultilevelROIGenerator(
            pre_nms_top_k=roi_generator_config.pre_nms_top_k,
            pre_nms_score_threshold=roi_generator_config.pre_nms_score_threshold,
            pre_nms_min_size_threshold=(
                roi_generator_config.pre_nms_min_size_threshold),
            nms_iou_threshold=roi_generator_config.nms_iou_threshold,
            num_proposals=roi_generator_config.num_proposals,
            test_pre_nms_top_k=roi_generator_config.test_pre_nms_top_k,
            test_pre_nms_score_threshold=(
                roi_generator_config.test_pre_nms_score_threshold),
            test_pre_nms_min_size_threshold=(
                roi_generator_config.test_pre_nms_min_size_threshold),
            test_nms_iou_threshold=roi_generator_config.test_nms_iou_threshold,
            test_num_proposals=roi_generator_config.test_num_proposals,
            use_batched_nms=roi_generator_config.use_batched_nms)

        roi_sampler_cascade = []
        roi_sampler_obj = roi_sampler.ROISampler(
            mix_gt_boxes=roi_sampler_config.mix_gt_boxes,
            num_sampled_rois=roi_sampler_config.num_sampled_rois,
            foreground_fraction=roi_sampler_config.foreground_fraction,
            foreground_iou_threshold=roi_sampler_config.foreground_iou_threshold,
            background_iou_high_threshold=(
                roi_sampler_config.background_iou_high_threshold),
            background_iou_low_threshold=(
                roi_sampler_config.background_iou_low_threshold))
        roi_sampler_cascade.append(roi_sampler_obj)
        # Initialize additional roi simplers for cascade heads.
        if roi_sampler_config.cascade_iou_thresholds:
            for iou in roi_sampler_config.cascade_iou_thresholds:
                roi_sampler_obj = roi_sampler.ROISampler(
                    mix_gt_boxes=False,
                    num_sampled_rois=roi_sampler_config.num_sampled_rois,
                    foreground_iou_threshold=iou,
                    background_iou_high_threshold=iou,
                    background_iou_low_threshold=0.0,
                    skip_subsampling=True)
                roi_sampler_cascade.append(roi_sampler_obj)

        roi_aligner_obj = roi_aligner.MultilevelROIAligner(
            crop_size=roi_aligner_config.crop_size,
            sample_offset=roi_aligner_config.sample_offset)

        detection_generator_obj = detection_generator.DetectionGenerator(
            apply_nms=generator_config.apply_nms,
            pre_nms_top_k=generator_config.pre_nms_top_k,
            pre_nms_score_threshold=generator_config.pre_nms_score_threshold,
            nms_iou_threshold=generator_config.nms_iou_threshold,
            max_num_detections=generator_config.max_num_detections,
            nms_version=generator_config.nms_version,
            use_cpu_nms=generator_config.use_cpu_nms,
            soft_nms_sigma=generator_config.soft_nms_sigma,
            use_sigmoid_probability=generator_config.use_sigmoid_probability)

        if model_config.include_mask:
            mask_head = instance_heads.MaskHead(
                num_classes=model_config.num_classes,
                upsample_factor=model_config.mask_head.upsample_factor,
                num_convs=model_config.mask_head.num_convs,
                num_filters=model_config.mask_head.num_filters,
                use_separable_conv=model_config.mask_head.use_separable_conv,
                activation=model_config.norm_activation.activation,
                norm_momentum=model_config.norm_activation.norm_momentum,
                norm_epsilon=model_config.norm_activation.norm_epsilon,
                kernel_regularizer=l2_regularizer,
                class_agnostic=model_config.mask_head.class_agnostic)

            mask_sampler_obj = mask_sampler.MaskSampler(
                mask_target_size=(
                    model_config.mask_roi_aligner.crop_size *
                    model_config.mask_head.upsample_factor),
                num_sampled_masks=model_config.mask_sampler.num_sampled_masks)

            mask_roi_aligner_obj = roi_aligner.MultilevelROIAligner(
                crop_size=model_config.mask_roi_aligner.crop_size,
                sample_offset=model_config.mask_roi_aligner.sample_offset)
        else:
            mask_head = None
            mask_sampler_obj = None
            mask_roi_aligner_obj = None

        model = maskrcnn_model.MaskRCNNModel(
            backbone=backbone,
            decoder=decoder,
            rpn_head=rpn_head,
            detection_head=detection_head,
            roi_generator=roi_generator_obj,
            roi_sampler=roi_sampler_cascade,
            roi_aligner=roi_aligner_obj,
            detection_generator=detection_generator_obj,
            mask_head=mask_head,
            mask_sampler=mask_sampler_obj,
            mask_roi_aligner=mask_roi_aligner_obj,
            class_agnostic_bbox_pred=detection_head_config.class_agnostic_bbox_pred,
            cascade_class_ensemble=detection_head_config.cascade_class_ensemble,
            min_level=model_config.min_level,
            max_level=model_config.max_level,
            num_scales=model_config.anchor.num_scales,
            aspect_ratios=model_config.anchor.aspect_ratios,
            anchor_size=model_config.anchor.anchor_size,
            outer_boxes_scale=model_config.outer_boxes_scale)

        self._config_dict = {
            'backbone': backbone,
            'decoder': decoder,
            'rpn_head': rpn_head,
            'detection_head': detection_head,
            'roi_generator': roi_generator_obj,
            'roi_sampler': roi_sampler_cascade,
            'roi_aligner': roi_aligner_obj,
            'detection_generator': detection_generator_obj,
            'outer_boxes_scale': model_config.outer_boxes_scale,
            'mask_head': mask_head,
            'mask_sampler': mask_sampler_obj,
            'mask_roi_aligner': mask_roi_aligner_obj,
            'class_agnostic_bbox_pred': detection_head_config.class_agnostic_bbox_pred,
            'cascade_class_ensemble': detection_head_config.cascade_class_ensemble,
            'min_level': model_config.min_level,
            'max_level': model_config.max_level,
            'num_scales': model_config.anchor.num_scales,
            'aspect_ratios': model_config.anchor.aspect_ratios,
            'anchor_size': model_config.anchor.anchor_size}

        self.backbone = backbone
        self.decoder = decoder
        self.rpn_head = rpn_head
        if not isinstance(detection_head, (list, tuple)):
            self.detection_head = [detection_head]
        else:
            self.detection_head = detection_head
        self.roi_generator = roi_generator_obj
        if not isinstance(roi_sampler_obj, (list, tuple)):
            self.roi_sampler = [roi_sampler_obj]
        else:
            self.roi_sampler = roi_sampler_obj
        if len(self.roi_sampler) > 1 and not detection_head_config.class_agnostic_bbox_pred:
            raise ValueError('`class_agnostic_bbox_pred` needs to be True if multiple detection heads are specified.')

        self.roi_aligner = roi_aligner_obj
        self.detection_generator = detection_generator_obj
        self._include_mask = mask_head is not None
        if model_config.outer_boxes_scale < 1.0:
            raise ValueError('`outer_boxes_scale` should be a value >= 1.0.')
        self.outer_boxes_scale = model_config.outer_boxes_scale
        self.mask_head = mask_head
        if self._include_mask and mask_sampler_obj is None:
            raise ValueError('`mask_sampler` is not provided in Mask R-CNN.')
        self.mask_sampler = mask_sampler_obj
        if self._include_mask and mask_roi_aligner_obj is None:
            raise ValueError('`mask_roi_aligner` is not provided in Mask R-CNN.')
        self.mask_roi_aligner = mask_roi_aligner_obj

        # Weights for the regression losses for each FRCNN layer.
        # TODO(jiageng): Make the weights configurable.
        self._cascade_layer_to_weights = [
            [10.0, 10.0, 5.0, 5.0],
            [20.0, 20.0, 10.0, 10.0],
            [30.0, 30.0, 15.0, 15.0],
        ]

    def call(
        self,
        images: tf.Tensor,
        image_shape: tf.Tensor,
        anchor_boxes: Optional[Mapping[str, tf.Tensor]] = None,
        gt_boxes: Optional[tf.Tensor] = None,
        gt_classes: Optional[tf.Tensor] = None,
        gt_masks: Optional[tf.Tensor] = None,
        gt_outer_boxes: Optional[tf.Tensor] = None,
        training: Optional[bool] = None) -> Mapping[str, Optional[tf.Tensor]]:

        call_box_outputs_kwargs = {
            'images': images,
            'image_shape': image_shape,
            'anchor_boxes': anchor_boxes,
            'gt_boxes': gt_boxes,
            'gt_classes': gt_classes,
            'training': training,
        }

        if self.outer_boxes_scale > 1.0:
            call_box_outputs_kwargs['gt_outer_boxes'] = gt_outer_boxes
        model_outputs, intermediate_outputs = self._call_box_outputs(
            **call_box_outputs_kwargs)

        return model_outputs


    def train_step(self, inputs):
        features, labels = inputs
        with tf.GradientTape() as tape:
            model_kwargs = {
                'image_shape': labels['image_info'][:, 1, :],
                'anchor_boxes': labels['anchor_boxes'],
                'gt_boxes': labels['gt_boxes'],
                'gt_classes': labels['gt_classes']
            }

            loss_params = {
                'class_weights': None,
                'frcnn_box_weight': 1.0,
                'frcnn_class_loss_top_k_percent': 1.0,
                'frcnn_class_use_binary_cross_entropy': False,
                'frcnn_class_weight': 1.0,
                'frcnn_huber_loss_delta': 1.0,
                'l2_weight_decay': 8e-05,
                'loss_weight': 1.0,
                'mask_weight': 1.0,
                'rpn_box_weight': 1.0,
                'rpn_huber_loss_delta': 0.1111111111111111,
                'rpn_score_weight': 1.0}

            outputs = self(features, **model_kwargs)
            trainable_var = self.trainable_variables

            rpn_score_loss, rpn_box_loss = self._build_rpn_losses(outputs, labels)
            frcnn_cls_loss_fn =  maskrcnn_losses.FastrcnnClassLoss(
                use_binary_cross_entropy=loss_params['frcnn_class_use_binary_cross_entropy'],
                top_k_percent=loss_params['frcnn_class_loss_top_k_percent']
            )
            frcnn_box_loss_fn = maskrcnn_losses.FastrcnnBoxLoss(
                loss_params['frcnn_huber_loss_delta'],
                self._config_dict['class_agnostic_bbox_pred']
            )
            class_output_shape = tf.shape(outputs['class_outputs'])
            batch_size, num_boxes = class_output_shape[0], class_output_shape[1]
            class_targets_temp = tf.zeros([batch_size, num_boxes], dtype=tf.float32)
            box_targets_temp = tf.zeros([batch_size, num_boxes, 4], dtype=tf.float32)
            frcnn_cls_loss = frcnn_cls_loss_fn(outputs['class_outputs'], class_targets_temp, loss_params['class_weights'])
            frcnn_box_loss = frcnn_box_loss_fn(outputs['box_outputs'], class_targets_temp, box_targets_temp)
            total_loss = (
                loss_params['rpn_score_weight'] * rpn_score_loss
                + loss_params['rpn_box_weight'] * rpn_box_loss
                + loss_params['frcnn_class_weight'] * frcnn_cls_loss
                + loss_params['frcnn_box_weight'] * frcnn_box_loss
            )
            loss = loss_params['loss_weight'] * total_loss
            grads = tape.gradient(loss, trainable_var)

        return grads

    def _build_rpn_losses(
        self, outputs: Mapping[str, Any],
        labels: Mapping[str, Any]) -> Tuple[tf.Tensor, tf.Tensor]:
        """Builds losses for Region Proposal Network (RPN)."""
        rpn_score_loss_fn = maskrcnn_losses.RpnScoreLoss(
            tf.shape(outputs['box_outputs'])[1])
        rpn_box_loss_fn = maskrcnn_losses.RpnBoxLoss(0.11111111111111111)
        rpn_score_loss = tf.reduce_mean(
            rpn_score_loss_fn(outputs['rpn_scores'], labels['rpn_score_targets']))
        rpn_box_loss = tf.reduce_mean(
            rpn_box_loss_fn(outputs['rpn_boxes'], labels['rpn_box_targets']))
        return rpn_score_loss, rpn_box_loss

    def _get_backbone_and_decoder_features(self, images):
        backbone_features = self.backbone(images)
        if self.decoder:
            features = self.decoder(backbone_features)
        else:
            features = backbone_features
        return backbone_features, features


    def _call_box_outputs(
        self,
        images: tf.Tensor,
        image_shape: tf.Tensor,
        anchor_boxes: Optional[Mapping[str, tf.Tensor]] = None,
        gt_boxes: Optional[tf.Tensor] = None,
        gt_classes: Optional[tf.Tensor] = None,
        training: Optional[bool] = None,
        gt_outer_boxes: Optional[tf.Tensor] = None,
    ) -> Tuple[Mapping[str, Any], Mapping[str, Any]]:

        """Implementation of the Faster-RCNN logic for boxes."""
        model_outputs = {}

        # Feature extraction.
        (backbone_features,
        decoder_features) = self._get_backbone_and_decoder_features(images)

        # Region proposal network.
        rpn_scores, rpn_boxes = self.rpn_head(decoder_features)

        model_outputs.update({
            'backbone_features': backbone_features,
            'decoder_features': decoder_features,
            'rpn_boxes': rpn_boxes,
            'rpn_scores': rpn_scores
        })

        # Generate anchor boxes for this batch if not provided.
        if anchor_boxes is None:
            _, image_height, image_width, _ = images.get_shape().as_list()
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
                    [tf.shape(images)[0], 1, 1, 1])

        # Generate RoIs.
        current_rois, _ = self.roi_generator(rpn_boxes, rpn_scores, anchor_boxes,
                                            image_shape, training)

        next_rois = current_rois
        all_class_outputs = []
        for cascade_num in range(len(self.roi_sampler)):
        # In cascade RCNN we want the higher layers to have different regression
        # weights as the predicted deltas become smaller and smaller.
            regression_weights = self._cascade_layer_to_weights[cascade_num]
            current_rois = next_rois

            if self.outer_boxes_scale == 1.0:
                (class_outputs, box_outputs, model_outputs, matched_gt_boxes,
                matched_gt_classes, matched_gt_indices,
                current_rois) = self._run_frcnn_head(
                    features=decoder_features,
                    rois=current_rois,
                    gt_boxes=gt_boxes,
                    gt_classes=gt_classes,
                    training=training,
                    model_outputs=model_outputs,
                    cascade_num=cascade_num,
                    regression_weights=regression_weights)
            else:
                (class_outputs, box_outputs, model_outputs,
                (matched_gt_boxes, matched_gt_outer_boxes), matched_gt_classes,
                matched_gt_indices, current_rois) = self._run_frcnn_head(
                    features=decoder_features,
                    rois=current_rois,
                    gt_boxes=gt_boxes,
                    gt_outer_boxes=gt_outer_boxes,
                    gt_classes=gt_classes,
                    training=training,
                    model_outputs=model_outputs,
                    cascade_num=cascade_num,
                    regression_weights=regression_weights)
            all_class_outputs.append(class_outputs)

            # Generate ROIs for the next cascade head if there is any.
            if cascade_num < len(self.roi_sampler) - 1:
                next_rois = box_ops.decode_boxes(
                    tf.cast(box_outputs, tf.float32),
                    current_rois,
                    weights=regression_weights)
                next_rois = box_ops.clip_boxes(next_rois,
                                            tf.expand_dims(image_shape, axis=1))

        if not training:
            if self._config_dict['cascade_class_ensemble']:
                class_outputs = tf.add_n(all_class_outputs) / len(all_class_outputs)

            detections = self.detection_generator(
                box_outputs,
                class_outputs,
                current_rois,
                image_shape,
                regression_weights,
                bbox_per_class=(not self._config_dict['class_agnostic_bbox_pred']))
            model_outputs.update({
                'cls_outputs': class_outputs,
                'box_outputs': box_outputs,
            })
            if self.detection_generator.get_config()['apply_nms']:
                model_outputs.update({
                    'detection_boxes': detections['detection_boxes'],
                    'detection_scores': detections['detection_scores'],
                    'detection_classes': detections['detection_classes'],
                    'num_detections': detections['num_detections']
                })
                if self.outer_boxes_scale > 1.0:
                    detection_outer_boxes = box_ops.compute_outer_boxes(
                        detections['detection_boxes'],
                        tf.expand_dims(image_shape, axis=1), self.outer_boxes_scale)
                    model_outputs['detection_outer_boxes'] = detection_outer_boxes
            else:
                model_outputs.update({
                    'decoded_boxes': detections['decoded_boxes'],
                    'decoded_box_scores': detections['decoded_box_scores']
                })

        intermediate_outputs = {
            'matched_gt_boxes': matched_gt_boxes,
            'matched_gt_indices': matched_gt_indices,
            'matched_gt_classes': matched_gt_classes,
            'current_rois': current_rois,
        }

        if self.outer_boxes_scale > 1.0:
            intermediate_outputs['matched_gt_outer_boxes'] = matched_gt_outer_boxes

        return (model_outputs, intermediate_outputs)

    def _run_frcnn_head(self,
                        features,
                        rois,
                        gt_boxes,
                        gt_classes,
                        training,
                        model_outputs,
                        cascade_num,
                        regression_weights,
                        gt_outer_boxes=None):
        """Runs the frcnn head that does both class and box prediction.

        Args:
        features: `list` of features from the feature extractor.
        rois: `list` of current rois that will be used to predict bbox refinement
            and classes from.
        gt_boxes: a tensor with a shape of [batch_size, MAX_NUM_INSTANCES, 4].
            This tensor might have paddings with a negative value.
        gt_classes: [batch_size, MAX_INSTANCES] representing the groundtruth box
            classes. It is padded with -1s to indicate the invalid classes.
        training: `bool`, if model is training or being evaluated.
        model_outputs: `dict`, used for storing outputs used for eval and losses.
        cascade_num: `int`, the current frcnn layer in the cascade.
        regression_weights: `list`, weights used for l1 loss in bounding box
            regression.
        gt_outer_boxes: a tensor with a shape of [batch_size, MAX_NUM_INSTANCES,
            4]. This tensor might have paddings with a negative value. Default to
            None.

        Returns:
        class_outputs: Class predictions for rois.
        box_outputs: Box predictions for rois. These are formatted for the
            regression loss and need to be converted before being used as rois
            in the next stage.
        model_outputs: Updated dict with predictions used for losses and eval.
        matched_gt_boxes: If `is_training` is true, then these give the gt box
            location of its positive match.
        matched_gt_classes: If `is_training` is true, then these give the gt class
            of the predicted box.
        matched_gt_boxes: If `is_training` is true, then these give the box
            location of its positive match.
        matched_gt_outer_boxes: If `is_training` is true, then these give the
            outer box location of its positive match. Only exist if
            outer_boxes_scale is greater than 1.0.
        matched_gt_indices: If `is_training` is true, then gives the index of
            the positive box match. Used for mask prediction.
        rois: The sampled rois used for this layer.
        """
        # Only used during training.
        matched_gt_boxes, matched_gt_classes, matched_gt_indices = None, None, None
        if self.outer_boxes_scale > 1.0:
            matched_gt_outer_boxes = None

        if training and gt_boxes is not None:
            rois = tf.stop_gradient(rois)

        current_roi_sampler = self.roi_sampler[cascade_num]
        if self.outer_boxes_scale == 1.0:
            rois, matched_gt_boxes, matched_gt_classes, matched_gt_indices = (
                current_roi_sampler(rois, gt_boxes, gt_classes))
        else:
            (rois, matched_gt_boxes, matched_gt_outer_boxes, matched_gt_classes,
            matched_gt_indices) = current_roi_sampler(rois, gt_boxes, gt_classes,
                                                    gt_outer_boxes)
        # Create bounding box training targets.
        box_targets = box_ops.encode_boxes(
            matched_gt_boxes, rois, weights=regression_weights)
        # If the target is background, the box target is set to all 0s.
        box_targets = tf.where(
            tf.tile(
                tf.expand_dims(tf.equal(matched_gt_classes, 0), axis=-1),
                [1, 1, 4]), tf.zeros_like(box_targets), box_targets)
        model_outputs.update({
            'class_targets_{}'.format(cascade_num)
            if cascade_num else 'class_targets':
                matched_gt_classes,
            'box_targets_{}'.format(cascade_num)
            if cascade_num else 'box_targets':
                box_targets,
        })

        # Get roi features.
        roi_features = self.roi_aligner(features, rois)

        # Run frcnn head to get class and bbox predictions.
        current_detection_head = self.detection_head[cascade_num]
        class_outputs, box_outputs = current_detection_head(roi_features)

        model_outputs.update({
            'class_outputs_{}'.format(cascade_num)
            if cascade_num else 'class_outputs':
                class_outputs,
            'box_outputs_{}'.format(cascade_num) if cascade_num else 'box_outputs':
                box_outputs,
        })
        if self.outer_boxes_scale == 1.0:
            return (class_outputs, box_outputs, model_outputs, matched_gt_boxes,
                matched_gt_classes, matched_gt_indices, rois)
        else:
            return (class_outputs, box_outputs, model_outputs,
                (matched_gt_boxes, matched_gt_outer_boxes), matched_gt_classes,
                matched_gt_indices, rois)