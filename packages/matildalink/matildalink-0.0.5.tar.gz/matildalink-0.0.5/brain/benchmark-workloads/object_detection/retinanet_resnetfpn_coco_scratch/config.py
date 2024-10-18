from official.core import exp_factory

def retinanet_resnetfpn_coco_scratch():

    config = exp_factory.get_exp_config('retinanet_resnetfpn_coco')

    tfds_name = 'coco/2017'
    batch_size = 8

    config.task.annotation_file=''

    config.task.train_data.input_path=''
    config.task.train_data.tfds_name=tfds_name
    config.task.train_data.tfds_split='train'
    config.task.train_data.drop_remainder=True
    config.task.train_data.dtype='bfloat16'
    config.task.train_data.shuffle_buffer_size=1000
    config.task.train_data.global_batch_size=batch_size
    
    config.task.validation_data.input_path=''
    config.task.validation_data.tfds_name=tfds_name
    config.task.validation_data.tfds_split='validation'
    config.task.validation_data.drop_remainder=True
    config.task.validation_data.dtype='bfloat16'

    return config
    

