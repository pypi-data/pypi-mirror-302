import os
import shutil
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--instance')
parser.add_argument('-p', '--price', type=float)
parser.add_argument('-cp', '--config_path')
args = parser.parse_args()

instance = args.instance
price = args.price
config_path = args.config_path

exp_config_df = pd.read_csv(config_path, header=0)

sps_list = []
for i, conf in exp_config_df.iterrows():
    exp_name = f'exp_{conf["model"]}_{"train" if conf["is_train"] else "inference"}_{conf["batch_size"]}_{conf["steps"]}_{conf["steps_per_loop"]}'
    metric_path = exp_name + '/metrics/sps'
    with open(metric_path, 'r') as f:
        sps_list.append(float(f.readline()))

instance_list = [instance]*len(sps_list)
cost_per_hour_list = [price]*len(sps_list)

results_df = exp_config_df.assign(
    instance=instance_list,
    cost_per_hour=cost_per_hour_list,
    steps_per_second=sps_list,
    total_time=lambda x: x.steps/x.steps_per_second,
    total_cost=lambda x: (x.cost_per_hour/3600)*x.total_time
)

exp_dir_name = config_path.split('/')[-1].split('.')[0]
results_path = f'./results/{exp_dir_name}'
if os.path.exists(results_path):
    shutil.rmtree(results_path)
    os.makedirs(f'./results/{exp_dir_name}')
else:
    os.makedirs(f'./results/{exp_dir_name}')
results_df.to_csv(f'./results/{exp_dir_name}/{instance}_{exp_name}.csv', index=False)

