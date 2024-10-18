## Running workloads
```
pip install -r requirements.txt
python prepare_directories.py -m remove #cleans up any previous experiment data
python prepare_directories.py -m build -p [path/to/experiment/config/file] #builds directories for storing experiment data
python main.py -p [path/to/experiment/config/file] -i [name_of_the_instance]
python collect_data.py -cp [path/to/experiment/config/file] -i [name_of_the_instance] -p [on-demand_price_for_this_instance]
```

## Run GPU profiling using Nsight Compute CLI (ncu)
```bash
$ <bootstrap_script> <path_config_file> <instance_type>

# example case
(nsight_cuda12.2) $ ./bootstrap_explicit2.sh ./config_csv/prof_3xs/bert_train.csv g5.xlarge
```

## Arithmetic Intensity (AI) calculation from Nsight Profile
```bash
$ extract_ncu_profile.py
Usage: extract_ncu_profile.py <path_ncu_csv_report>

# example case
$ extract_ncu_profile.py prof-01a1-3xs-bert-train.csv
{
    'arithmetic_intensity': 0.5612804375525522,
    'dram__sectors_read.sum': 261302800,
    'dram__sectors_write.sum': 171819368,
    'dram_read_transactions': 261302800,
    'dram_write_transactions': 171819368,
    'flop_count_sp': 7779295999,
    'report_filename': 'prof-01a1-3xs-bert-train.csv',
    'smsp__sass_thread_inst_executed_op_fadd_pred_on.sum': 1062024300,
    'smsp__sass_thread_inst_executed_op_ffma_pred_on.sum': 2682645099,
    'smsp__sass_thread_inst_executed_op_fmul_pred_on.sum': 1351981501
}
```