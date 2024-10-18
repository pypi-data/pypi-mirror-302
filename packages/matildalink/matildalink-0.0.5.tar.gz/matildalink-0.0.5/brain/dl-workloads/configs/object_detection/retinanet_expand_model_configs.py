import pprint
from official import vision
from official.vision.modeling.backbones.resnet import RESNET_SPECS
from official.core import exp_factory

def generate_resnet_backbone_configs(base_config, min_level=0, max_level=10):
    configs = []
    resnet_id_list = RESNET_SPECS.keys()
    for resnet_id in list(resnet_id_list)[min_level:max_level+1]:
        kwargs = {'task': {'model': {'backbone': {'resnet': {'model_id': resnet_id}}}}}
        configs.append(base_config.replace(**kwargs))
    return configs

def base_te_config():

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

    config.task.validation_data = None

    train_steps = 600

    config.trainer.steps_per_loop = 10
    config.trainer.summary_interval = 100
    config.trainer.checkpoint_interval = train_steps
    config.trainer.train_steps = train_steps

    return config

if __name__ == '__main__':

    base_config = base_te_config()
    generated_configs = generate_resnet_backbone_configs(base_config, 0, 1)
    for config in generated_configs:
        pprint.PrettyPrinter(indent=4).pprint(config.as_dict())
