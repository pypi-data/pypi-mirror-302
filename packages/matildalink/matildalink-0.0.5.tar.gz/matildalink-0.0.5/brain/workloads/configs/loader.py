from dataclasses import dataclass
import yaml

import tensorflow as tf

from official.modeling.hyperparams import Config
from official.core.config_definitions import ExperimentConfig
from official.core import exp_factory

@dataclass
class MLBConfig():
    tfm_config: Config
    is_train: bool = False
    num_steps: int = 2

def load(config_path: str) -> MLBConfig:

    with tf.io.gfile.GFile(config_path, 'r') as f:
        loaded = yaml.load(f, Loader=yaml.FullLoader)
    tfm_config = ExperimentConfig(task=loaded['task'], trainer=loaded['trainer'], runtime=loaded['runtime'])
    is_train = loaded['is_train']
    num_steps = loaded['num_steps']
    
    mlb_config = MLBConfig(tfm_config=tfm_config, is_train=is_train, num_steps=num_steps)
    return mlb_config


if __name__ == '__main__':

    test_config_path = './debug/resnet_debug.yaml'
    load(test_config_path)
    