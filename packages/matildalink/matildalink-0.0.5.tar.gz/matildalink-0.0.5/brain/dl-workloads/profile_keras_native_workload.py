import tensorflow as tf, tf_keras

from official.core import task_factory, train_utils
from official.vision.modeling import factory as vision_factory

from configs.image_classification import resnet as resnet_config
from configs.object_detection import retinanet as retinanet_config, maskrcnn as maskrcnn_config
from configs.nlp import bert as bert_config

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--architecture_type')
parser.add_argument('-s', '--train', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

def load_config(architecture):
    if architecture == 'resnet':
        return resnet_config.base_te_config()
    elif architecture == 'retinanet':
        return retinanet_config.base_te_config()
    elif architecture == 'maskrcnn':
        return bert_config.base_te_config()
    else:
        return None

def load_tf_dataset(architecture, config):
    task = task_factory.get_task(config.task)
    if architecture == 'resnet':
        dataset = task.build_inputs(config.task.train_data)
        return dataset.map(lambda feature, labels: tf.reshape(tf.one_hot(labels, config.task.model.num_classes), [labels.shape[0], -1]))
    elif architecture == 'retinanet':
        config.task.train_data.global_batch_size = 32
        return task.build_inputs(config.task.train_data)
    else:
        return task.build_inputs(config.task.train_data)

def load_model(architecture, config):

    input_shape = config.task.model.input_size
    input_specs = tf.keras.layers.InputSpec(shape=[None]+list(input_shape))

    if architecture == 'resnet':
        return vision_factory.build_classification_model(input_specs=input_specs, model_config=config.task.model, l2_regularizer=None)
    elif architecture == 'retinanet':
        return vision_factory.build_retinanet(input_specs=input_specs, model_config=config.task.model, l2_regularizer=None)
    elif architecture == 'maskrcnn':
        return vision_factory.build_maskrcnn(input_specs=input_specs, model_config=config.task.model, l2_regularizer=tf_keras.regularizers.l2(5e-5))
    elif architecture == 'bert':
        return None
    else:
        return None

if __name__ == '__main__':

    # profiling parameters
    NUM_STEPS = 20
    policy = tf_keras.mixed_precision.Policy('mixed_float16')
    tf_keras.mixed_precision.set_global_policy(policy)

    # cli arguments
    architecture = args.architecture_type
    is_train = args.train

        # prepare profile log directory
    profile_log_path = f'./profile_logs/{architecture}_{"train" if is_train else "inference"}/'
    if not os.path.exists(profile_log_path):
        os.makedirs(profile_log_path)


    # load config
    config = load_config(architecture)

    # load tf dataset
    dataset = load_tf_dataset(architecture, config)

    # load model
    model = load_model(architecture, config)

    # run training/inference
    if is_train:

        # compile model
        task = task_factory.get_task(config.task)
        optimizer = train_utils.create_optimizer(task, config)

        if architecture == 'resnet':
            loss_fn = tf_keras.losses.CategoricalCrossentropy(from_logits=True)
            metrics =  [
                tf_keras.metrics.CategoricalAccuracy(name='accuracy'),
                tf_keras.metrics.TopKCategoricalAccuracy(k=5, name=f'top_5_accuracy')
            ]
            model.compile(optimizer=optimizer, loss=loss_fn, metrics=metrics)
            tb_callback = tf_keras.callbacks.TensorBoard(log_dir=profile_log_path, profile_batch=(10, 20))
            model.fit(x=dataset, steps_per_epoch=NUM_STEPS, epochs=5, callbacks=[tb_callback])

        elif architecture == 'retinanet':

            data_iter = iter(dataset)

            @tf.function(jit_compile=False) # False: disable XLA, True: enable XLA
            def train_step(inputs):
                features, labels = inputs
                with tf.GradientTape() as tape:
                    outputs = model(features, training=True)
                    outputs = tf.nest.map_structure(lambda x: tf.cast(x, tf.float32), outputs)
                    loss, cls_loss, box_loss, model_loss = task.build_losses(outputs=outputs, labels=labels, aux_losses=model.losses)
                trainable_var = model.trainable_variables
                grads = tape.gradient(loss, trainable_var)
                optimizer.apply_gradients(list(zip(grads, trainable_var)))
                return loss
            
            with tf.profiler.experimental.Profile(logdir=profile_log_path):
                for step in range(NUM_STEPS):
                    with tf.profiler.experimental.Trace('train', step_num=step, _r=1):
                        data = next(data_iter)
                        train_step(data)
        
        elif architecture == 'bert':
            pass

        else:
            pass

    else:
        pass


