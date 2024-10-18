import official.vision # need this line for registering experiment config factory

from official.core import exp_factory
from official.nlp.configs import pretraining_experiments as exp_config

from official.modeling.hyperparams.params_dict import save_params_dict_to_yaml

def save_resnet_config(num_steps=2):

    config = exp_factory.get_exp_config('resnet_imagenet')

    # configure model
    config.task.model.num_classes = 10
    config.task.model.input_size = [32,32,3]
    config.task.model.backbone.resnet.model_id = 18
    config.task.model.backbone.resnet.spec_idx = 0
    
    # configure training and testing data
    config.task.train_data.input_path = ''
    config.task.train_data.tfds_name = 'cifar10'
    config.task.train_data.tfds_split = 'train'
    config.task.train_data.global_batch_size = 128

    config.task.validation_data = None
    
    # trainer configruation
    config.trainer.optimizer_config.learning_rate.type = 'cosine'
    config.trainer.optimizer_config.learning_rate.cosine.decay_steps = 1000
    config.trainer.optimizer_config.learning_rate.cosine.initial_learning_rate = 0.1
    config.trainer.optimizer_config.warmup.linear.warmup_steps = 100

    # additional information for MLBConfig
    for config_filepath in ['te_resnet_train.yaml', 'te_resnet_inference.yaml']:

        config.is_train = ('train' in config_filepath)
        config.num_steps = num_steps
        config.task.name = 'image_classification'

        output_path = f'configs/te/step{num_steps}/{config_filepath}'
        save_params_dict_to_yaml(config, output_path)

def save_retinanet_config(num_steps=2):

    config = exp_factory.get_exp_config('retinanet_resnetfpn_coco')

    config.task.model.backbone.resnet.spec_idx = 0

    config.task.annotation_file=''

    config.task.train_data.input_path=''
    config.task.train_data.tfds_name='coco/2017'
    config.task.train_data.tfds_split='train'

    config.task.train_data.drop_remainder=True
    config.task.train_data.shuffle_buffer_size=80
    config.task.train_data.global_batch_size=8

    config.task.train_data.parser.aug_type = None

    config.task.validation_data = None

    # additional information for MLBConfig
    for config_filepath in ['te_retinanet_train.yaml', 'te_retinanet_inference.yaml']:

        config.is_train = ('train' in config_filepath)
        config.num_steps = num_steps
        config.task.name = 'object_detection_retinanet'

        output_path = f'configs/te/step{num_steps}/{config_filepath}'
        save_params_dict_to_yaml(config, output_path)

def save_maskrcnn_config(num_steps=2):

    config = exp_factory.get_exp_config('maskrcnn_resnetfpn_coco')

    config.task.annotation_file=''
    config.task.init_checkpoint = None
    config.task.init_checkpoint_modules = 'backbone'

    config.task.model.backbone.resnet.spec_idx = 0
    config.task.model.num_classes = 91
    config.task.model.input_size = [640,640,3]
    config.task.model.anchor.anchor_size = 3
    config.task.model.norm_activation.norm_epsilon = 0.001
    config.task.model.norm_activation.norm_momentum = 0.99
    config.task.model.norm_activation.use_sync_bn = True
    config.task.model.detection_generator.pre_nms_top_k = 1000
    config.task.model.min_level = 3
    config.task.model.max_level = 7
    config.task.model.include_mask = False

    config.task.train_data.input_path=''
    config.task.train_data.is_training = True
    config.task.train_data.global_batch_size = 8
    config.task.train_data.tfds_name = 'coco/2017'
    config.task.train_data.tfds_split = 'train'
    config.task.train_data.drop_remainder = True
    config.task.train_data.shuffle_buffer_size = 80
    config.task.train_data.parser.aug_rand_hflip = False
    config.task.train_data.parser.aug_scale_min = 0.5
    config.task.train_data.parser.aug_scale_max = 2.0
    config.task.train_data.parser.aug_type = None

    config.task.validation_data = None

    # additional information for MLBConfig
    for config_filepath in ['te_maskrcnn_train.yaml', 'te_maskrcnn_inference.yaml']:

        config.is_train = ('train' in config_filepath)
        config.num_steps = num_steps
        config.task.name = 'object_detection_maskrcnn'

        output_path = f'configs/te/step{num_steps}/{config_filepath}'
        save_params_dict_to_yaml(config, output_path)

def save_bert_config(num_steps=2):

    config = exp_config.bert_text_wiki_pretraining()

    config.task.train_data.global_batch_size = 8
    config.task.train_data.seq_length = 8
    config.task.train_data.max_predictions_per_seq = 19
    config.task.train_data.vocab_file_path = './data/vocab.txt'
    config.task.validation_data = None

    # additional information for MLBConfig
    for config_filepath in ['te_bert_train.yaml', 'te_bert_inference.yaml']:

        config.is_train = ('train' in config_filepath)
        config.num_steps = num_steps
        config.task.name = 'natural_language_processing'

        output_path = f'configs/te/step{num_steps}/{config_filepath}'
        save_params_dict_to_yaml(config, output_path)


if __name__ == '__main__':

    num_steps = 3

    save_resnet_config(num_steps)
    save_retinanet_config(num_steps)
    save_maskrcnn_config(num_steps)
    save_bert_config(num_steps)

