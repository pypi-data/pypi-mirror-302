import tensorflow as tf

from configs import loader as configloader
from data import loader as dataloader
from modeling import loader as modelloader

import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--config-path')
parser.add_argument('--device-log', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if __name__ == '__main__':

    # enable logging
    tf.debugging.set_log_device_placement(args.device_log)

    # set TensorFlow memory growth
    gpus = tf.config.list_physical_devices('GPU')
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except:
        print('Error: invalid device / cannot modify virtual devices once initialized.')
        exit()

    # set global mixed_precision policy to float32
    tf.keras.mixed_precision.set_global_policy('float32')

    # load config
    mlb_config = configloader.load(config_path=args.config_path)
    tfm_config, is_train, num_steps = mlb_config.tfm_config, mlb_config.is_train, mlb_config.num_steps

    needs_additional_kwargs = tfm_config.task.name == 'object_detection_maskrcnn'
    is_self_supervised = tfm_config.task.name == 'natural_language_processing'

    # load data
    dataset = dataloader.load(tfm_config=tfm_config)

    # load model
    model = modelloader.load(tfm_config=tfm_config)

    # define tensorflow graph
    loop_fn = None
    if is_train:
        @tf.function
        def loop_fn(dataset: tf.data.Dataset, num_steps: int=2):
            for data in dataset.take(num_steps):
                _ = model.train_step(data)
    else:
        if needs_additional_kwargs:
            @tf.function
            def loop_fn(dataset: tf.data.Dataset, num_steps: int=2):
                for data in dataset.take(num_steps):
                    features, labels = data
                    model_kwargs = {
                        'image_shape': labels['image_info'][:,1,:],
                        'anchor_boxes': labels['anchor_boxes'],
                        'gt_boxes': labels['gt_boxes'],
                        'gt_classes': labels['gt_classes']
                    }
                    _ = model(features, **model_kwargs)
        elif is_self_supervised:
            @tf.function
            def loop_fn(dataset: tf.data.Dataset, num_steps: int=2):
                for data in dataset.take(num_steps):
                    _ = model(data)
        else:
            @tf.function
            def loop_fn(dataset: tf.data.Dataset, num_steps: int=2):
                for data in dataset.take(num_steps):
                    features, labels = data
                    _ = model(features)

    # run
    start_time = time.time()
    loop_fn(dataset, num_steps)
    end_time = time.time()
    print(f'total elapsed time: {end_time-start_time} seconds')
    print(f'average time per step: {(end_time-start_time)/num_steps} seconds')
