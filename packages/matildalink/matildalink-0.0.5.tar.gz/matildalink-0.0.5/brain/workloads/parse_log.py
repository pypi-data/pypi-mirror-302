from collections import defaultdict

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--log_path')
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

with open(args.log_path, 'r') as f:
    logs = f.readlines()

device_op_map = {'GPU:0':[], 'CPU:0':[]}

for log in logs:

    op_name = log.split(':')[0]
    device = ':'.join(log[:-1].split(':')[-2:])

    if device in device_op_map.keys():
        device_op_map[device].append(op_name)

for device_name, op_list in device_op_map.items():
    print(f'{device_name}: {len(op_list)} ops placed ({len(set(op_list))} unique)')
    if args.verbose:
        print(op_list)
    print('=========================================')
