import pandas as pd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--profile-name')
args = parser.parse_args()

profile_name = args.profile_name

raw_df = pd.read_csv(f'./ncu-reports/{profile_name}.csv', index_col='ID')

metrics_map = {
    'duration': 'gpu__time_duration.sum',
    'fadd_per_cycle': 'smsp__sass_thread_inst_executed_op_fadd_pred_on.sum.per_cycle_elapsed',
    'fmul_per_cycle': 'smsp__sass_thread_inst_executed_op_fmul_pred_on.sum.per_cycle_elapsed',
    'ffma_per_cycle_x2': 'derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2',
    'dadd_per_cycle': 'smsp__sass_thread_inst_executed_op_dadd_pred_on.sum.per_cycle_elapsed',
    'dmul_per_cycle': 'smsp__sass_thread_inst_executed_op_dmul_pred_on.sum.per_cycle_elapsed',
    'dfma_per_cycle_x2': 'derived__smsp__sass_thread_inst_executed_op_dfma_pred_on_x2',
    'sm_frequency': 'smsp__cycles_elapsed.avg.per_second',
    'dram_bandwidth': 'dram__bytes.sum.per_second',
}

metric_units_map = {metric: unit for (metric, unit) in zip(raw_df.columns, raw_df.iloc[0])}

def convert_unit_to_float(unit_name):
    if unit_name == 'nsecond':
        return 1e-9
    else:
        return 1

def get_metric(row, metric):
    return float(row[metric]) * convert_unit_to_float(metric_units_map[metric])

def process_data(raw_report, output_path):

    float_operation_list = []
    double_operation_list = []
    memory_access_list = []
    ai_float_list = []
    ai_double_list = []

    for _, raw_row in list(raw_report.iterrows())[1:]:

        duration = get_metric(raw_row, metrics_map['duration'])
        fadd_per_cycle = get_metric(raw_row, metrics_map['fadd_per_cycle'])
        fmul_per_cycle = get_metric(raw_row, metrics_map['fmul_per_cycle'])
        ffma_per_cycle_x2 = get_metric(raw_row, metrics_map['ffma_per_cycle_x2'])
        dadd_per_cycle = get_metric(raw_row, metrics_map['dadd_per_cycle'])
        dmul_per_cycle = get_metric(raw_row, metrics_map['dmul_per_cycle'])
        dfma_per_cycle_x2 = get_metric(raw_row, metrics_map['dfma_per_cycle_x2'])
        sm_frequency = get_metric(raw_row, metrics_map['sm_frequency'])
        dram_bandwidth = get_metric(raw_row, metrics_map['dram_bandwidth'])

        float_operations = (fadd_per_cycle + fmul_per_cycle + ffma_per_cycle_x2) * sm_frequency * duration
        double_operations = (dadd_per_cycle + dmul_per_cycle + dfma_per_cycle_x2) * sm_frequency * duration
        memory_access = dram_bandwidth * duration 
        if memory_access:
            ai_float = float_operations / memory_access
            ai_double = double_operations / memory_access

        float_operation_list.append(float_operations)
        double_operation_list.append(double_operations)
        memory_access_list.append(memory_access)
        ai_float_list.append(ai_float)
        ai_double_list.append(ai_double)
    
    print(f'total fp32 ops count: {sum(float_operation_list)}')
    print(f'total fp64 ops count: {sum(double_operation_list)}')
    print(f'total memory access: {sum(memory_access_list)} Byte')
    print(f'total fp32 arithmetic intensity: {sum(float_operation_list)/sum(memory_access_list)}')
    print(f'total fp64 arithmetic intensity: {sum(double_operation_list)/sum(memory_access_list)}')
    
    pd.DataFrame(data={
        'fp32_ops_count': float_operation_list,
        'fp64_ops_count': double_operation_list,
        'memory_access': memory_access_list,
        'ai_fp32': ai_float_list,
        'ai_fp64': ai_double_list
    }).to_csv(output_path, index=False)

process_data(raw_df, f'./ncu-reports/{profile_name}-processed.csv')