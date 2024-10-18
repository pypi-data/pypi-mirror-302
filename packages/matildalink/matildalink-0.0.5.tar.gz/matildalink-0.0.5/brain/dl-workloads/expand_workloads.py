from multiprocessing import Process, Value
import os

import argparse

import tensorflow as tf, tf_keras
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

from official.core import task_factory
from official.vision.modeling import factory
from official.vision.losses import maskrcnn_losses
from official.nlp.modeling import models as nlp_models, networks, layers

from configs import config_generator
from configs.mlb_config import MLBConfig

from modeling.backbone import CustomResNet

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--base_model_type')
args = parser.parse_args()

def load_mlb_configs(base_model_type):
    return config_generator.generate_configs(type=base_model_type)

def load_backbone(mlb_config):

    input_shape = mlb_config.tfm_config.task.model.input_size
    input_specs = tf.keras.layers.InputSpec(shape=[None]+list(input_shape))

    if mlb_config.backbone_type == 'resnet':
        return CustomResNet(block_specs=mlb_config.resnet_block_specs, input_specs=input_specs)
    elif mlb_config.backbone_type == 'mobilenet': # TODO
        return None
    else:
        return None

def load_resnet_model(mlb_config):
    input_shape = mlb_config.tfm_config.task.model.input_size
    input_specs = tf.keras.layers.InputSpec(shape=[None]+list(input_shape))
    backbone = load_backbone(mlb_config)
    return factory.build_classification_model(
        input_specs=input_specs,
        backbone=backbone,
        model_config=mlb_config.tfm_config.task.model,
        l2_regularizer=None)


def load_retinanet_model(mlb_config):
    input_shape = mlb_config.tfm_config.task.model.input_size
    input_specs=tf.keras.layers.InputSpec(shape=[None]+list(input_shape))
    backbone = load_backbone(mlb_config)
    return factory.build_retinanet(
        input_specs=input_specs,
        backbone=backbone,
        model_config=mlb_config.tfm_config.task.model,
        l2_regularizer=None)

def load_maskrcnn_model(mlb_config):
    input_shape = mlb_config.tfm_config.task.model.input_size
    input_specs=tf.keras.layers.InputSpec(shape=[None]+list(input_shape))
    backbone = load_backbone(mlb_config)
    return factory.build_maskrcnn(
        input_specs=input_specs,
        backbone=backbone,
        model_config=mlb_config.tfm_config.task.model,
        l2_regularizer=tf_keras.regularizers.l2(5e-5))

def load_bert_model(mlb_config: MLBConfig):
    tfm_config = mlb_config.tfm_config
    cls_head_cfgs = tfm_config.task.model.cls_heads
    encoder_cfg = tfm_config.task.model.encoder.bert
    cls_heads = [layers.cls_head.ClassificationHead(**cls_head_cfg.as_dict()) for cls_head_cfg in cls_head_cfgs] # build BERT classification heads
    bert_encoder = networks.BertEncoderV2( # build BERT encoder
        vocab_size=encoder_cfg.vocab_size,
            num_layers=encoder_cfg.num_layers,
        hidden_size=encoder_cfg.hidden_size,
        max_sequence_length=encoder_cfg.max_position_embeddings)
    return nlp_models.BertPretrainerV2( # build BERT pretrainer model
        encoder_network=bert_encoder,
        classification_heads=cls_heads,
        mlm_activation='gelu')

def load_resnet_inference_graph(model, temp_data):

    @tf.function
    def infer_step(inputs):
        features, labels = inputs
        return model(features)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_retinanet_inference_graph(model, temp_data):

    @tf.function
    def infer_step(inputs):
        features, labels = inputs
        return model(features)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_maskrcnn_inference_graph(model, temp_data):

    @tf.function
    def infer_step(inputs):
        features, labels = inputs
        model_kwargs = {
            'image_shape': labels['image_info'][:, 1, :],
            'anchor_boxes': labels['anchor_boxes'],
            'gt_boxes': labels['gt_boxes'],
            'gt_classes': labels['gt_classes']
        }
        return model(features, **model_kwargs)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_bert_inference_graph(model, temp_data):

    @tf.function
    def infer_step(inputs):
        return model(inputs)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_resnet_train_graph(model, temp_data, task):

    config = task._task_config

    @tf.function
    def train_step(inputs):
        features, labels = inputs
        labels = tf.one_hot(labels, config.model.num_classes)
        with tf.GradientTape() as tape:
            outputs = model(features) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            loss = task.build_losses(outputs, labels, aux_losses=model.losses)
            grads = tape.gradient(loss, trainable_var)
        return grads

    concrete_func = train_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_retinanet_train_graph(model, temp_data, task):

    @tf.function
    def train_step(inputs):
        features, labels = inputs
        with tf.GradientTape() as tape:
            outputs = model(features) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            loss = task.build_losses(outputs, labels, aux_losses=model.losses)
            grads = tape.gradient(loss, trainable_var)
        return grads

    concrete_func = train_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_maskrcnn_train_graph(model, temp_data, task):

    config = task._task_config

    @tf.function
    def train_step(inputs):
        features, labels = inputs
        with tf.GradientTape() as tape:
            model_kwargs = {
                'image_shape': labels['image_info'][:, 1, :],
                'anchor_boxes': labels['anchor_boxes'],
                'gt_boxes': labels['gt_boxes'],
                'gt_classes': labels['gt_classes']
            }
            if config.model.include_mask:
                model_kwargs['gt_masks'] = labels['gt_masks']
                if config.model.outer_boxes_scale > 1.0:
                    model_kwargs['gt_outer_boxes'] = labels['gt_outer_boxes']
            outputs = model(features, **model_kwargs) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            loss_params = config.losses
            rpn_score_loss, rpn_box_loss = task._build_rpn_losses(outputs, labels)
            frcnn_cls_loss_fn =  maskrcnn_losses.FastrcnnClassLoss(
                use_binary_cross_entropy=loss_params.frcnn_class_use_binary_cross_entropy,
                top_k_percent=loss_params.frcnn_class_loss_top_k_percent
            )
            frcnn_box_loss_fn = maskrcnn_losses.FastrcnnBoxLoss(
                loss_params.frcnn_huber_loss_delta,
                config.model.detection_head.class_agnostic_bbox_pred
            )
            class_output_shape = tf.shape(outputs['class_outputs'])
            batch_size, num_boxes = class_output_shape[0], class_output_shape[1]
            class_targets_temp = tf.zeros([batch_size, num_boxes], dtype=tf.float32)
            box_targets_temp = tf.zeros([batch_size, num_boxes, 4], dtype=tf.float32)
            frcnn_cls_loss = frcnn_cls_loss_fn(outputs['class_outputs'], class_targets_temp, loss_params.class_weights)
            frcnn_box_loss = frcnn_box_loss_fn(outputs['box_outputs'], class_targets_temp, box_targets_temp)
            total_loss = (
                loss_params.rpn_score_weight * rpn_score_loss
                + loss_params.rpn_box_weight * rpn_box_loss
                + loss_params.frcnn_class_weight * frcnn_cls_loss
                + loss_params.frcnn_box_weight * frcnn_box_loss
            )
            loss = loss_params.loss_weight * total_loss
            grads = tape.gradient(loss, trainable_var)
        return grads

    concrete_func = train_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def load_bert_train_graph(model, temp_data):

    @tf.function
    def train_step(inputs):
        with tf.GradientTape() as tape:
            labels = inputs
            outputs = model(inputs) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            with tf.name_scope('MaaskedLMTask/losses'):
                lm_prediction_losses = tf_keras.losses.sparse_categorical_crossentropy(
                    labels['masked_lm_ids'],
                    tf.cast(outputs['mlm_logits'], tf.float32),
                    from_logits=True)
                lm_label_weights = labels['masked_lm_weights']
                lm_numerator_loss = tf.reduce_sum(lm_prediction_losses * lm_label_weights)
                lm_denominator_loss = tf.reduce_sum(lm_label_weights)
                mlm_loss = tf.math.divide_no_nan(lm_numerator_loss, lm_denominator_loss)
                if 'next_sentence_labels' in labels:
                    sentence_labels = labels['next_sentence_labels']
                    sentence_outputs = tf.cast(outputs['next_sentence'], dtype=tf.float32)
                    sentence_loss = tf.reduce_mean(tf_keras.losses.sparse_categorical_crossentropy(sentence_labels, sentence_outputs, from_logits=True))
                    loss = mlm_loss + sentence_loss
            grads = tape.gradient(loss, trainable_var)
        return grads

    concrete_func = train_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()


def calculate_graph_ops_memory(graph): # estimates activation memory

    total_activation_memory = 0
    ops = graph.get_operations()
    num_total_ops = len(ops)
    num_skipped_ops = 0

    for op in ops:
        # Skip irrelevant ops
        if op.type in ['Const', 'Assign', 'NoOp', 'Placeholder']:
            num_skipped_ops += 1
            continue

        for output in op.outputs:
            shape = output.get_shape()
            # Skip tensors with undefined shape
            if not shape.is_fully_defined():
                num_skipped_ops += 1
                continue  # Skip tensors with undefined shape

            num_elements = 1
            for dim in shape:
                num_elements *= dim
            tensor_memory = num_elements * 4 # assume float32 (4 bytes per element)
            total_activation_memory += tensor_memory

    return total_activation_memory, num_total_ops, num_skipped_ops

def calculate_ai_estimate(mlb_config: MLBConfig, flops, imem, pmem):

    # load model
    if mlb_config.model_arch == 'resnet':
        model = load_resnet_model(mlb_config)
    elif mlb_config.model_arch == 'retinanet':
        model = load_retinanet_model(mlb_config)
    elif mlb_config.model_arch == 'maskrcnn':
        model = load_maskrcnn_model(mlb_config)
    elif mlb_config.model_arch == 'bert':
        model = load_bert_model(mlb_config)
    else:
        model = None
        print(f'invalid model architecture: {mlb_config.model_arch}')
        return

    # load concrete data for building model
    task = task_factory.get_task(mlb_config.tfm_config.task)
    temp_data = next(iter(task.build_inputs(mlb_config.tfm_config.task.train_data)))

    # build Keras model with concrete input
    # features = temp_data[0] # TODO: delete if not needed
    # _ = model(features) # TODO: delete if not needed

    if mlb_config.model_arch == 'resnet':
        if mlb_config.is_train:
            graph_def = load_resnet_train_graph(model, temp_data, task)
        else:
            graph_def = load_resnet_inference_graph(model, temp_data)
    elif mlb_config.model_arch == 'retinanet':
        if mlb_config.is_train:
            graph_def = load_retinanet_train_graph(model, temp_data, task)
        else:
            graph_def = load_retinanet_inference_graph(model, temp_data)
    elif mlb_config.model_arch == 'maskrcnn':
        if mlb_config.is_train:
            graph_def = load_maskrcnn_train_graph(model, temp_data, task)
        else:
            graph_def = load_maskrcnn_inference_graph(model, temp_data)
    elif mlb_config.model_arch == 'bert':
        if mlb_config.is_train:
            graph_def = load_bert_train_graph(model, temp_data)
        else:
            graph_def = load_bert_inference_graph(model, temp_data)
    else:
        print(f'invalid model architecture: {mlb_config.model_arch}')
        return

    # calculate flops & required memory
    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
            flops_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)

            flops.value = flops_profiler.total_float_ops
            imem.value, num_total_ops, num_skipped_ops = calculate_graph_ops_memory(sess.graph)
            pmem.value = model.count_params() * 4 # num_params * 4 Bytes


if __name__ == '__main__':

    base_model_type = args.base_model_type
    mlb_configs = load_mlb_configs(base_model_type)

    for mlb_config in mlb_configs:

        # check & prepare experiment directory
        exp_dir_path = f'./intensity-experiments/{mlb_config.experiment_dir}/'
        if not os.path.exists(exp_dir_path):
            os.makedirs(exp_dir_path)

        flops = Value('d', 0.0) # total number of floating operations (fp32)
        imem = Value('d', 0.0) # intermediate memory
        pmem = Value('d', 0.0) # parameter memory

        profile_process = Process(target=calculate_ai_estimate, args=(mlb_config, flops, imem, pmem))
        profile_process.start()
        profile_process.join()

        ai_estimate = flops.value/(imem.value+pmem.value)
        print(f'estimated arithmetic intensity: {ai_estimate}')

        with open(f'{exp_dir_path}{mlb_config.experiment_name}.csv', 'w') as f:
            f.write('flops,imem,pmem,ai_estimate\n')
            f.write(f'{flops.value},{imem.value},{pmem.value},{ai_estimate}')
    
