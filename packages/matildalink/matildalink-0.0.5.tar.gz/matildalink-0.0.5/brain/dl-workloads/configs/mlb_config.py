from typing import List
from official.modeling.hyperparams import Config

class MLBConfig():

    def __init__(
        self, 
        tfm_config: Config,
        experiment_dir: str,
        experiment_name: str,
        model_arch: str,
        backbone_type: str = 'resnet',
        is_train: bool = False,
        resnet_block_specs: List[tuple] = [],
        ):

        self.tfm_config = tfm_config

        self.experiment_dir = experiment_dir
        self.experiment_name = experiment_name

        self.model_arch = model_arch
        self.backbone_type = backbone_type

        self.is_train = is_train

        self.resnet_block_specs = resnet_block_specs


