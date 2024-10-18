import os
from pprint import pprint

import numpy as np
import tensorflow as tf
from tensorflow.python.summary.summary_iterator import summary_iterator

import tensorflow_models as tfm
from official.core.train_utils import create_trainer, try_count_params, try_count_flops

import datetime
import argparse
import glob
from pprint import PrettyPrinter

from configs import load_config

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--instance')
parser.add_argument('-p', '--config_path')
args = parser.parse_args()
instance = args.instance
config_path = args.config_path

pp = PrettyPrinter(indent=4)

def generate_exp_configs(config_path):
    exp_configs = []

    dt_now_fmt_candid = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dt_now_fmt = os.getenv("DT_NOW", dt_now_fmt_candid)

    with open(config_path, 'r') as f:
        for exp_list in [line.strip().split(',') for line in f.readlines()[1:]]:
            exp_config = {}
            exp_config['model'] = model = exp_list[0]
            exp_config['is_train'] = is_train = exp_list[1] == 'True'
            exp_config['batch_size'] = batch_size = int(exp_list[2])
            exp_config['steps'] = steps = int(exp_list[3])
            exp_config['steps_per_loop'] = steps_per_loop = int(exp_list[4])
            exp_config['config'] = load_config.load(model, is_train, batch_size, steps, steps_per_loop)

            folder_root = f'./exp_{model}_{"train" if is_train else "inference"}_{batch_size}_{steps}_{steps_per_loop}_{dt_now_fmt}'
            #folder_root = f'./exp_{model}_{"train" if is_train else "inference"}_{batch_size}_{steps}_{steps_per_loop}'
            exp_config['model_dir'] = os.path.join(folder_root, 'model')
            exp_config['metrics_dir'] = os.path.join(folder_root, 'metrics')

            policy_exist_ok: bool = True
            os.makedirs(folder_root, exist_ok=policy_exist_ok)
            os.makedirs(exp_config['model_dir'], exist_ok=policy_exist_ok)
            os.makedirs(exp_config['metrics_dir'], exist_ok=policy_exist_ok)

            #exp_config['model_dir'] = f'./exp_{model}_{"train" if is_train else "inference"}_{batch_size}_{steps}_{steps_per_loop}_{dt_now_fmt}/model/'
            #exp_config['metrics_dir'] = f'./exp_{model}_{"train" if is_train else "inference"}_{batch_size}_{steps}_{steps_per_loop}/metrics/'
            exp_configs.append(exp_config)
    return exp_configs

def get_mean_sps(exp_config):
    #target_path = exp_config['model_dir'] + ('train/*' if exp_config['is_train'] else 'validation/*')
    target_path_tfevents = os.path.join(exp_config['model_dir'], 'train/*' if exp_config['is_train'] else 'validation/*')
    tfevents_files = glob.glob(target_path_tfevents)
    sps_list = []
    for tfevents_file in tfevents_files:
        for event in summary_iterator(tfevents_file):
            for value in event.summary.value:
                if value.tag == 'steps_per_second':
                    sps_list.append(tf.make_ndarray(value.tensor))
    return sum(sps_list)/len(sps_list)

def record_metrics(mean_sps, metrics_dir):
    #target_path_metrics = os.path.join(metrics_dir, 'sps')

    dt_now_fmt_candid = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    target_path_metrics = os.path.join(metrics_dir, f"sps_{dt_now_fmt_candid}.log")
    #with open(metrics_dir+'sps', 'w') as f:
    with open(target_path_metrics, 'w') as f:
        f.write(f'{mean_sps}')

def get_model_explanation(model):

    # Calculate trainable and non-trainable parameters
    trainable_params = 0
    non_trainable_params = 0

    # Iterate over all variables in the model
    for var in model.variables:
        var_params = np.prod(var.shape.as_list())  # Total parameters in the variable
        var_name = var.name
        var_shape = var.shape.as_list()
        if var.trainable:
            trainable_params += var_params
            print(f"Trainable Variable: {var_name}, Shape: {var_shape}, Params: {var_params}")
        else:
            non_trainable_params += var_params
            print(f"Non-Trainable Variable: {var_name}, Shape: {var_shape}, Params: {var_params}")

    # Display total params
    total_params = trainable_params + non_trainable_params
    print("\nTotal Trainable Parameters: ", trainable_params)
    print("Total Non-Trainable Parameters: ", non_trainable_params)
    print("Total Parameters: ", total_params) 

    print('-' * 20)

    # fin
    return


def run_exp(exp_config):

    config = exp_config['config']
    is_train = exp_config['is_train']
    model_dir = exp_config['model_dir']

    # print("exp_config:")
    # pprint(exp_config, indent=1)

    logical_device_names = [logical_device.name for logical_device in tf.config.list_logical_devices()]
    if 'GPU' in ''.join(logical_device_names):
        distribution_strategy = tf.distribute.MirroredStrategy()
    else:
        distribution_strategy = tf.distribute.OneDeviceStrategy(logical_device_names[0])

    with distribution_strategy.scope():
        task = tfm.core.task_factory.get_task(config.task, logging_dir=model_dir)
        trainer = create_trainer(params=config, task=task, train=is_train, evaluate=(not is_train))

    # forcefully match 'steps_per_loop' and 'summary_interval' policies each other
    config.trainer.summary_interval = config.trainer.steps_per_loop
    model, _ = tfm.core.train_lib.run_experiment(
        distribution_strategy=distribution_strategy,
        task=task,
        mode='train' if is_train else 'eval',
        params=config,
        trainer=trainer,
        model_dir=model_dir)

    # check model params #1
    #model.summary()

    #print('-' * 20)

    # check model params #2
    #get_model_explanation(model)

    return model

if __name__ == '__main__':

    exp_configs = generate_exp_configs(config_path)

    for exp_config in exp_configs:

        model = run_exp(exp_config)

        # remove candid ckpt files with glob
        path_candid_ckpt1 = os.path.join(exp_config['model_dir'], "checkpoint")
        for f_candid in glob.glob(path_candid_ckpt1):
            os.remove(f_candid)

        path_candid_ckpt2 = os.path.join(exp_config['model_dir'], "ckpt*")
        for f_candid in glob.glob(path_candid_ckpt2):
            os.remove(f_candid)

        params = try_count_params(model)
        flops = try_count_flops(model)
        sps = get_mean_sps(exp_config)
        record_metrics(sps, exp_config['metrics_dir'])




