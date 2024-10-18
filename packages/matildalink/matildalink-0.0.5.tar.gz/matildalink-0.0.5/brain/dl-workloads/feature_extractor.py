# imports
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-a', '--model-arch')
args = parser.parse_args()
model_arch = args.model_arch

import time
import multiprocessing as mp

import tensorflow as tf, tf_keras
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

from official.vision.modeling import factory
from official.vision.losses import maskrcnn_losses
from official.nlp.modeling import models as nlp_models
from official.nlp.modeling import networks, layers
from official.core import task_factory

from configs.image_classification import resnet18_cifar10
from configs.object_detection import retinanet_resnetfpn_coco, maskrcnn_resnetfpn_coco
from configs.nlp import bert_wiki



# profile #flops
def get_flops(graph_def):
    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
            flops_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)
            return flops_profiler.total_float_ops

# profile activation memory
def get_activation_memory(graph_def):
    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            # Estimate activation memory movement
            return calculate_graph_ops_memory(sess.graph)

# profile parameter memory
def get_parameter_memory_with_graph(graph_def):
    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            # Memory profiler options
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.trainable_variables_parameter()
            mem_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)
            # Total parameters in bytes (assuming 4 bytes per parameter)
            total_params = mem_profiler.total_parameters
            param_memory = total_params * 4  # 4 bytes per parameter (float32)
            return param_memory

def get_parameter_memory_from_keras(experiment):
    if 'resnet' in experiment:
        config = resnet18_cifar10.train_config()
        model = load_resnet_model()
    elif 'retinanet' in experiment:
        config = retinanet_resnetfpn_coco.train_config()
        model = load_retinanet_model()
    elif 'maskrcnn' in experiment:
        config = maskrcnn_resnetfpn_coco.train_config()
        model = load_maskrcnn_model()
    elif 'bert' in experiment:
        config = bert_wiki.train_config()
        model = load_bert_model()
    else:
        print('Invalid experiment name')
        return 0

    # build model through feeding temp input
    task = task_factory.get_task(config.task)
    if 'bert' in experiment:
        temp_input = next(iter(task.build_inputs(config.task.train_data)))
        _ = model(temp_input)
    elif 'maskrcnn' in experiment:
        temp_feat, temp_label = next(iter(task.build_inputs(config.task.train_data)))
        image_shape = temp_label['image_info'][:,1,:]
        _ = model(temp_feat, image_shape=image_shape)
    else:
        temp_feat, _ = next(iter(task.build_inputs(config.task.train_data)))
        _ = model(temp_feat)

    return model.count_params() * 4

# get inference graphs
def resnet_inference_graph():

    config = resnet18_cifar10.train_config() # TODO: fix config retriever to be more concise
    model = load_resnet_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

    @tf.function
    def infer_step(inputs):
        features, _ = inputs
        return model(features)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def retinanet_inference_graph():

    config = retinanet_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    model = load_retinanet_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

    @tf.function
    def infer_step(inputs):
        features, _ = inputs
        return model(features)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def maskrcnn_inference_graph():

    config = maskrcnn_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    model = load_maskrcnn_model()


    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

    @tf.function
    def infer_step(inputs):
        features, labels = inputs
        model_kwargs = {
            'image_shape': labels['image_info'][:, 1, :],
            'anchor_boxes': labels['anchor_boxes'],
            'gt_boxes': labels['gt_boxes'],
            'gt_classes': labels['gt_classes']
        }
        if config.task.model.include_mask:
            model_kwargs['gt_masks'] = labels['gt_masks']
            if config.task.model.outer_boxes_scale > 1.0:
                model_kwargs['gt_outer_boxes'] = labels['gt_outer_boxes']
        return model(features, **model_kwargs)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def bert_inference_graph():

    config = bert_wiki.train_config() # TODO: fix config retriever to be more concise
    model = load_bert_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

    @tf.function
    def infer_step(inputs):
        return model(inputs)

    concrete_func = infer_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

# get train graph
def resnet_train_graph():
    config = resnet18_cifar10.train_config() # TODO: fix config retriever to be more concise
    model = load_resnet_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

    @tf.function
    def train_step(inputs):
        features, labels = inputs
        labels = tf.one_hot(labels, config.task.model.num_classes)
        with tf.GradientTape() as tape:
            outputs = model(features) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            loss = task.build_losses(outputs, labels, aux_losses=model.losses)
            grads = tape.gradient(loss, trainable_var)
        return grads

    concrete_func = train_step.get_concrete_function(temp_data)
    frozen_func = convert_variables_to_constants_v2(concrete_func)

    return frozen_func.graph.as_graph_def()

def retinanet_train_graph():

    config = retinanet_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    model = load_retinanet_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

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

def maskrcnn_train_graph():

    config = maskrcnn_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    model = load_maskrcnn_model()


    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

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
            if config.task.model.include_mask:
                model_kwargs['gt_masks'] = labels['gt_masks']
                if config.task.model.outer_boxes_scale > 1.0:
                    model_kwargs['gt_outer_boxes'] = labels['gt_outer_boxes']
            outputs = model(features, **model_kwargs) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = model.trainable_variables
            task_config = config.task
            loss_params = config.task.losses
            rpn_score_loss, rpn_box_loss = task._build_rpn_losses(outputs, labels)
            frcnn_cls_loss_fn =  maskrcnn_losses.FastrcnnClassLoss(
                use_binary_cross_entropy=task_config.losses.frcnn_class_use_binary_cross_entropy,
                top_k_percent=task_config.losses.frcnn_class_loss_top_k_percent
            )
            frcnn_box_loss_fn = maskrcnn_losses.FastrcnnBoxLoss(
                task_config.losses.frcnn_huber_loss_delta,
                task_config.model.detection_head.class_agnostic_bbox_pred
            )
            class_output_shape = tf.shape(outputs['class_outputs'])
            batch_size, num_boxes = class_output_shape[0], class_output_shape[1]
            class_targets_temp = tf.zeros([batch_size, num_boxes], dtype=tf.float32)
            box_targets_temp = tf.zeros([batch_size, num_boxes, 4], dtype=tf.float32)
            frcnn_cls_loss = frcnn_cls_loss_fn(outputs['class_outputs'], class_targets_temp, task_config.losses.class_weights)
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

def bert_train_graph():

    config = bert_wiki.train_config() # TODO: fix config retriever to be more concise
    model = load_bert_model()

    task = task_factory.get_task(config.task)
    temp_data = next(iter(task.build_inputs(config.task.train_data)))

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

# load models
def load_resnet_model():
    config = resnet18_cifar10.train_config() # TODO: fix config retriever to be more concise
    input_shape = config.task.model.input_size
    return factory.build_classification_model(
        input_specs=tf.keras.layers.InputSpec(shape=[None]+list(input_shape)),
        model_config=config.task.model,
        l2_regularizer=None)

def load_retinanet_model():
    config = retinanet_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    input_shape = config.task.model.input_size
    return factory.build_retinanet(
        input_specs=tf.keras.layers.InputSpec(shape=[None]+list(input_shape)),
        model_config=config.task.model,
        l2_regularizer=None)

def load_maskrcnn_model():
    config = maskrcnn_resnetfpn_coco.train_config() # TODO: fix config retriever to be more concise
    input_shape = config.task.model.input_size
    return factory.build_maskrcnn(
        input_specs=tf.keras.layers.InputSpec(shape=[None]+list(input_shape)),
        model_config=config.task.model,
        l2_regularizer=tf_keras.regularizers.l2(5e-5))

def load_bert_model():
    config = bert_wiki.train_config()
    cls_head_cfgs = config.task.model.cls_heads
    encoder_cfg = config.task.model.encoder.bert
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

# other functions
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

def extract_all_feat(model_arch: str): # TODO: profiling maskrcnn flops & memory at the same time breaks the instance

    if model_arch == 'resnet_inference':
        graph_def = resnet_inference_graph()
    elif model_arch == 'resnet_train':
        graph_def = resnet_train_graph()
    elif model_arch == 'retinanet_inference':
        graph_def = retinanet_inference_graph()
    elif model_arch == 'retinanet_train':
        graph_def = retinanet_train_graph()
    elif model_arch == 'maskrcnn_inference':
        graph_def = maskrcnn_inference_graph()
    elif model_arch == 'maskrcnn_train':
        graph_def = maskrcnn_train_graph()
    elif model_arch == 'bert_inference':
        graph_def = bert_inference_graph()
    elif model_arch == 'bert_train':
        graph_def = bert_train_graph()
    else:
        print(f'Unrecognized exp_name: {model_arch}')

    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
            flops_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)

            # Memory profiler options
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.trainable_variables_parameter()
            mem_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)

    if 'resnet' in model_arch:
        config = resnet18_cifar10.train_config()
        model = load_resnet_model()
    elif 'retinanet' in model_arch:
        config = retinanet_resnetfpn_coco.train_config()
        model = load_retinanet_model()
    elif 'maskrcnn' in model_arch:
        config = maskrcnn_resnetfpn_coco.train_config()
        model = load_maskrcnn_model()
    elif 'bert' in model_arch:
        config = bert_wiki.train_config()
        model = load_bert_model()
    else:
        print('Invalid experiment name')
        return 0

    # build model through feeding temp input
    task = task_factory.get_task(config.task)
    if 'bert' in model_arch:
        temp_input = next(iter(task.build_inputs(config.task.train_data)))
        _ = model(temp_input)
    elif 'maskrcnn' in model_arch:
        temp_feat, temp_label = next(iter(task.build_inputs(config.task.train_data)))
        image_shape = temp_label['image_info'][:,1,:]
        _ = model(temp_feat, image_shape=image_shape)
    else:
        temp_feat, _ = next(iter(task.build_inputs(config.task.train_data)))
        _ = model(temp_feat)

if __name__ == '__main__':

    t = time.time()
    extract_all_feat(model_arch)
    print(f'total time: {time.time()-t}')


