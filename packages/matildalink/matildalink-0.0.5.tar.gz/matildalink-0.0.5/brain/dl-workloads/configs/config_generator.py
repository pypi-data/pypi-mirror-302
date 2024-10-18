from .mlb_config import MLBConfig

from .image_classification import resnet
from .object_detection import retinanet, maskrcnn
from .nlp import bert

def generate_resnet_block_specs(block_type='residual'):
    return [
        [
            (block_type, 2**num_filter_exponent, block_repeats) for num_filter_exponent in range(6, 10)
        ] for block_repeats in range(1,11)
    ]

def generate_resnet_mlb_configs(is_train=False):
    tfm_config = resnet.base_te_config()
    resnet_block_specs_list = generate_resnet_block_specs(block_type='residual')
    mlb_configs = [
        MLBConfig(
            tfm_config=tfm_config, 
            experiment_dir='resnet_variation_experiment', 
            experiment_name=f'block_repeat_{resnet_block_specs[0][2]}',
            model_arch='resnet', 
            backbone_type='resnet',
            is_train=is_train,
            resnet_block_specs=resnet_block_specs) 
            for resnet_block_specs in resnet_block_specs_list]
    return mlb_configs

def generate_retinanet_mlb_configs(is_train=False):
    tfm_config = retinanet.base_te_config()
    resnet_block_specs_list = generate_resnet_block_specs(block_type='residual')
    mlb_configs = [
        MLBConfig(
            tfm_config=tfm_config, 
            experiment_dir='retinanet_backbone_variation_experiment', 
            experiment_name=f'block_repeat_{resnet_block_specs[0][2]}',
            model_arch='retinanet',
            backbone_type='resnet', 
            is_train=is_train,
            resnet_block_specs=resnet_block_specs) 
            for resnet_block_specs in resnet_block_specs_list]
    return mlb_configs

def generate_maskrcnn_mlb_configs(is_train=False):
    tfm_config = maskrcnn.base_te_config()
    resnet_block_specs_list = generate_resnet_block_specs(block_type='residual')
    mlb_configs = [
        MLBConfig(
            tfm_config=tfm_config,
            experiment_dir='maskrcnn_backbone_variation_experiment',
            experiment_name=f'block_repeat_{resnet_block_specs[0][2]}',
            model_arch='maskrcnn',
            backbone_type='resnet',
            is_train=is_train,
            resnet_block_specs=resnet_block_specs)
            for resnet_block_specs in resnet_block_specs_list]
    return mlb_configs

def generate_bert_mlb_configs(is_train=False):
    mlb_configs = []
    bert_encoder_cfgs = bert.generate_bert_encoder_configs()
    for bert_encoder_cfg in bert_encoder_cfgs:
        base_tfm_cfg = bert.base_te_config()
        base_tfm_cfg.override({'task':{'model':{'encoder':{'bert': bert_encoder_cfg}}}}),
        mlb_config = MLBConfig(
            tfm_config=base_tfm_cfg,
            experiment_dir='bert_layers_hidden_size_exp',
            experiment_name=f'l_{bert_encoder_cfg.num_layers}_hs_{bert_encoder_cfg.hidden_size}',
            model_arch='bert',
            is_train=is_train)
        mlb_configs.append(mlb_config)
    return mlb_configs

def generate_configs(type='resnet'): # TODO: refactor later to take in csv file for config generation
    if type == 'resnet':
        return generate_resnet_mlb_configs(True)
    elif type == 'retinanet':
        return generate_retinanet_mlb_configs(True)
    elif type == 'maskrcnn':
        return generate_maskrcnn_mlb_configs(True)
    elif type == 'bert':
        return generate_bert_mlb_configs(True)
    else: # provide resnet configs as default
        return generate_retinanet_mlb_configs()
