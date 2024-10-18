import tensorflow as tf

from configs import loader as configloader
from data import loader as dataloader
from modeling import loader as modelloader

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--config-path')
args = parser.parse_args()

def check_model_dtype(model):
    for submodule in model.submodules:
        if hasattr(submodule, 'dtype'):
            if submodule.dtype != 'float32':
                print(f'{submodule.name} dtype: {submodule._compute_dtype}')
        if hasattr(submodule, 'submodules'):
            check_model_dtype(submodule)

if __name__ == '__main__':

    # set TensorFlow memory growth
    gpus = tf.config.list_physical_devices('GPU')
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except:
        print('Error: invalid device / cannot modify virtual devices once initialized.')
        exit()

    # load config
    mlb_config = configloader.load(config_path=args.config_path)
    tfm_config, is_train, num_steps = mlb_config.tfm_config, mlb_config.is_train, mlb_config.num_steps

    needs_additional_kwargs = tfm_config.task.name == 'object_detection_maskrcnn'
    is_self_supervised = tfm_config.task.name == 'natural_language_processing'

    # load data
    dataset = dataloader.load(tfm_config=tfm_config)
    if is_self_supervised:
        features = next(iter(dataset))
    else:
        features, labels = next(iter(dataset))

    # load & build model
    model = modelloader.load(tfm_config=tfm_config)
    if needs_additional_kwargs:
        kwargs = {
            'image_shape':labels['image_info'][:,1,:],
            'anchor_boxes':labels['anchor_boxes'],
            'gt_boxes':labels['gt_boxes'],
            'gt_classes':labels['gt_classes']
        }
        _ = model(features, **kwargs)
    else:
        _ = model(features)

    check_model_dtype(model)

