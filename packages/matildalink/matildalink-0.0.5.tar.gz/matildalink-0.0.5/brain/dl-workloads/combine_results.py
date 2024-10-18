import glob
from itertools import groupby
from collections import defaultdict
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num_experiments')
parser.add_argument('-e', '--exp_dir_name')
args = parser.parse_args()
num_exp = int(args.num_experiments)
exp_dir_name = args.exp_dir_name

results_fps = glob.glob(f'./results/{exp_dir_name}/*.csv')
results_d = {}
for results_fp in results_fps:
    instance_name = results_fp.split('/')[3][:9]
    results_d[instance_name] = pd.read_csv(results_fp)

instance_names = list(results_d.keys())

def get_exp_name(ser):
    return f'exp_{ser["model"]}_{"train" if ser["is_train"] else "inference"}_{ser["batch_size"]}_{ser["steps"]}_{ser["steps_per_loop"]}'

def all_eq(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

aggregate_data = defaultdict(list)
for i in range(num_exp):
    assert all_eq([get_exp_name(results_d[instance_name].iloc[i]) for instance_name in instance_names]) # assert experiments to be equal in name and order
    aggregate_data['exp_name'].append(get_exp_name(results_d[instance_names[0]].iloc[i]))
    for instance_name in instance_names:
        data_row = results_d[instance_name].iloc[i]
        sps = data_row['steps_per_second']
        tt = data_row['total_time']
        tc = data_row['total_cost']
        aggregate_data[f'steps_per_second_{instance_name}'].append(sps)
        aggregate_data[f'total_time_{instance_name}'].append(tt)
        aggregate_data[f'total_cost_{instance_name}'].append(tc)

aggregate_df = pd.DataFrame(aggregate_data)
aggregate_df = aggregate_df.reindex(sorted(aggregate_df.columns), axis=1)

aggregate_df.to_csv(f'./results/{exp_dir_name}/combined_exp_results.csv', index=False)