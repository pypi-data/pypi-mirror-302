from official.core import exp_factory

import pprint
pp = pprint.PrettyPrinter(indent=4)

def train_config(batch_size, steps, steps_per_loop):

    config = exp_factory.get_exp_config('retinanet_resnetfpn_coco')

    tfds_name = 'coco/2017'

    config.task.annotation_file=''

    config.task.train_data.input_path=''
    config.task.train_data.tfds_name=tfds_name
    config.task.train_data.tfds_split='train'
    config.task.train_data.drop_remainder=True
    config.task.train_data.dtype='bfloat16'
    config.task.train_data.shuffle_buffer_size=1000
    config.task.train_data.global_batch_size=batch_size

    config.task.validation_data = None

    train_steps = steps

    config.trainer.steps_per_loop = steps_per_loop
    config.trainer.summary_interval = 100
    config.trainer.checkpoint_interval = train_steps
    config.trainer.train_steps = train_steps

    return config
    
def inference_config(batch_size, steps):

    config = exp_factory.get_exp_config('retinanet_resnetfpn_coco')

    tfds_name = 'coco/2017'

    config.task.annotation_file=''

    config.task.train_data = None

    config.task.validation_data.input_path = ''
    config.task.validation_data.tfds_name=tfds_name
    config.task.validation_data.tfds_split='test'
    config.task.validation_data.drop_remainder=True
    config.task.validation_data.dtype='bfloat16'
    config.task.validation_data.shuffle_buffer_size=1000
    config.task.validation_data.global_batch_size=batch_size

    config.trainer.steps_per_loop = 10
    config.trainer.validation_steps = steps

    return config
