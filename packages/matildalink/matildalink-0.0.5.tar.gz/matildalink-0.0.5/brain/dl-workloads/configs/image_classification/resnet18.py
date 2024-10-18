import tensorflow_models as tfm

import pprint
pp = pprint.PrettyPrinter(indent=4)

def train_config(batch_size, steps, steps_per_loop):

    config = tfm.core.exp_factory.get_exp_config('resnet_imagenet')
    input_shape = [32, 32, 3] # ds_info.features['image'].shape

    # configure model
    config.task.model.num_classes = 10
    config.task.model.input_size = input_shape
    config.task.model.backbone.resnet.model_id = 18
    
    # configure training and testing data
    ds_name = 'cifar10'
    
    config.task.train_data.input_path = ''
    config.task.train_data.tfds_name = ds_name
    config.task.train_data.tfds_split = 'train'
    config.task.train_data.global_batch_size = batch_size

    config.task.validation_data = None
    
    # trainer configruation

    config.trainer.steps_per_loop = steps_per_loop
    config.trainer.summary_interval = 500
    config.trainer.checkpoint_interval = steps
    config.trainer.train_steps = steps
    config.trainer.validation_steps=None
    config.trainer.validation_interval=None
    config.trainer.optimizer_config.learning_rate.type = 'cosine'
    config.trainer.optimizer_config.learning_rate.cosine.decay_steps = steps
    config.trainer.optimizer_config.learning_rate.cosine.initial_learning_rate = 0.1
    config.trainer.optimizer_config.warmup.linear.warmup_steps = 100
    
    return config

def inference_config(batch_size, steps):

    config = tfm.core.exp_factory.get_exp_config('resnet_imagenet')
    input_shape = [32, 32, 3] # ds_info.features['image'].shape

    # configure model
    config.task.model.num_classes = 10
    config.task.model.input_size = input_shape
    config.task.model.backbone.resnet.model_id = 18
    
    # configure training and testing data
    ds_name = 'cifar10'

    config.task.validation_data.input_path = ''
    config.task.validation_data.tfds_name = ds_name
    config.task.validation_data.tfds_split = 'test'
    config.task.validation_data.batch_size = batch_size

    
    # trainer configruation
    config.trainer.validation_steps=steps

    return config
