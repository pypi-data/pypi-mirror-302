import argparse

import os
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode')
parser.add_argument('-p', '--config_path')
args = parser.parse_args()

def build_dirs():
    with open(args.config_path, 'r') as f:

        for exp_line in f.readlines()[1:]:

            model, training, batch_size, steps, steps_per_loop = exp_line.strip().split(',') 

            exp_dir_path = f'./exp_{model}_{"train" if training == "True" else "inference"}_{batch_size}_{steps}_{steps_per_loop}/'
            if not os.path.exists(exp_dir_path):
                os.makedirs(exp_dir_path)
                os.makedirs(exp_dir_path+'model/')
                os.makedirs(exp_dir_path+'metrics/')

def remove_dirs():
    exp_dirs = glob.glob('./exp_*')
    for exp_dir in exp_dirs:
        if os.path.isdir(exp_dir):
            shutil.rmtree(exp_dir)

if __name__ == '__main__':
    mode = args.mode
    if mode == 'build':
        build_dirs()
    elif mode == 'remove':
        remove_dirs()
    else:
        pass

