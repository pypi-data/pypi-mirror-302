import pprint

from official import vision
from official.vision.modeling.backbones.resnet import RESNET_SPECS
from official.core import exp_factory

from ..mlb_config import MLBConfig

RESNET_CUSTOM_SPECS = [[('residual', 2**filter_exp, block_repeats) for filter_exp in range(6, 10)] for block_repeats in range(10)]

def generate_resnet_backbone_configs(base_config, min_level=0, max_level=10):
    configs = []
    resnet_id_list = RESNET_CUSTOM_SPECS.keys()
    for resnet_id in list(resnet_id_list)[min_level:max_level+1]:
        kwargs = {'task': {'model': {'backbone': {'resnet': {'model_id': resnet_id}}}}}
        configs.append(base_config.replace(**kwargs))
    return configs

def generate_resnet_block_specs(block_type='residual'):
    specs_list = [
        [
            (block_type, 2**num_filter_exponent, block_repeats) for num_filter_exponent in range(6, 10)
        ] for block_repeats in range(10)
    ]
    return specs_list

def base_te_config():

    config = exp_factory.get_exp_config('resnet_imagenet')
    input_shape = [32, 32, 3] # ds_info.features['image'].shape

    # configure model
    config.task.model.num_classes = 10
    config.task.model.input_size = input_shape
    config.task.model.backbone.resnet.model_id = 18
    
    # configure training and testing data
    ds_name = 'cifar10'
    batch_size = 128
    
    config.task.train_data.input_path = ''
    config.task.train_data.tfds_name = ds_name
    config.task.train_data.tfds_split = 'train'
    config.task.train_data.global_batch_size = batch_size

    config.task.validation_data = None
    
    # trainer configruation
    train_steps = 5000

    config.trainer.steps_per_loop = 100
    config.trainer.summary_interval = 500
    config.trainer.checkpoint_interval = train_steps
    config.trainer.train_steps = train_steps
    config.trainer.validation_steps=None
    config.trainer.validation_interval=None
    config.trainer.optimizer_config.learning_rate.type = 'cosine'
    config.trainer.optimizer_config.learning_rate.cosine.decay_steps = train_steps
    config.trainer.optimizer_config.learning_rate.cosine.initial_learning_rate = 0.1
    config.trainer.optimizer_config.warmup.linear.warmup_steps = 100

    return config

if __name__ == '__main__':

    base_config = base_te_config()
    generated_configs = generate_resnet_backbone_configs(base_config)
    for config in generated_configs:
        pprint.PrettyPrinter(indent=4).pprint(config.as_dict())
