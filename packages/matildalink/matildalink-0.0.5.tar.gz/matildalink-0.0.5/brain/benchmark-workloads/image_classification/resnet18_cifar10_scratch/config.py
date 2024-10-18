import tensorflow_models as tfm

import pprint
pp = pprint.PrettyPrinter(indent=4)

def resnet18_cifar_scratch():

    config = tfm.core.exp_factory.get_exp_config('resnet_imagenet')
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
    
    config.task.validation_data.input_path = ''
    config.task.validation_data.tfds_name = ds_name
    config.task.validation_data.tfds_split = 'test'
    config.task.validation_data.global_batch_size = batch_size
    
    # trainer configruation
    train_steps = 5000
    num_test_ex = 10000 # ds_info.splits['test'].num_examples

    config.trainer.steps_per_loop = 100
    config.trainer.summary_interval = 100
    config.trainer.checkpoint_interval = train_steps
    config.trainer.validation_interval = 1000
    config.trainer.validation_steps = num_test_ex // batch_size
    config.trainer.train_steps = train_steps
    config.trainer.optimizer_config.learning_rate.type = 'cosine'
    config.trainer.optimizer_config.learning_rate.cosine.decay_steps = train_steps
    config.trainer.optimizer_config.learning_rate.cosine.initial_learning_rate = 0.1
    config.trainer.optimizer_config.warmup.linear.warmup_steps = 100
    
    print('experiment info')
    pp.pprint(config.as_dict())

    return config
