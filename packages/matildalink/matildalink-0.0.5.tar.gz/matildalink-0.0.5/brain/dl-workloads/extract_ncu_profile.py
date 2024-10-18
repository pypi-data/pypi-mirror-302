import argparse
import csv
import os


def main(parser: argparse.ArgumentParser):

    args = parser.parse_args()
    path_ncu_csv_report: str = args.path_report
    signature: str = args.signature
    workload: str = args.workload
    task: str = args.task
    mode: str = args.mode

    # target metrics
    # references:
    # - https://docs.nvidia.com/nsight-compute/pdf/NsightComputeCli.pdf
    # - https://docs.nersc.gov/tools/performance/roofline/#arithmetic-intensity

    target_metrics = (
        "gpu__time_duration.sum",
        "smsp__sass_thread_inst_executed_op_fadd_pred_on.sum.per_cycle_elapsed",
        "smsp__sass_thread_inst_executed_op_fmul_pred_on.sum.per_cycle_elapsed",
        "derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2",
        "smsp__sass_thread_inst_executed_op_dadd_pred_on.sum.per_cycle_elapsed",
        "smsp__sass_thread_inst_executed_op_dmul_pred_on.sum.per_cycle_elapsed",
        "derived__smsp__sass_thread_inst_executed_op_dfma_pred_on_x2",
        "smsp__cycles_elapsed.avg.per_second",
        "dram__bytes.sum.per_second"
    )

    path_file = path_ncu_csv_report

    fh_profile = open(path_file, 'r', encoding="utf-8-sig" if mode == "direct" else "utf-8")
    csv_reader = csv.DictReader(fh_profile)

    # header = next(csv_reader)
    # print(header)

    dict_aggregate = {key_tgt: 0 for key_tgt in target_metrics}
    num_kernel_ops = 0

    list_all = []

    list_header = []
    dict_unit = {}

    for elem in csv_reader:

        if (mode == "direct" and len(list_header) != 0) or (mode == "piped" and len(dict_unit) != 0):
            num_kernel_ops += 1
            pass
        else:
            for key_query in target_metrics:
                for key_candid in elem.keys():
                    if key_candid.startswith(key_query):
                        list_header.append(key_candid)
                    else:
                        continue

        if mode == "piped" and len(dict_unit) == 0:
            for key_header in list_header:
                dict_unit.update({key_header: elem[key_header]})
            continue
        else:
            pass

        # exact match doesn't work:
        # ex) 'smsp__sass_thread_inst_executed_op_fadd_pred_on.sum'
        # <-- 'smsp__sass_thread_inst_executed_op_fadd_pred_on.sum [inst]""(1.06202e+09)'

        list_sub_key, list_sub_val = [], []

        for key_query in target_metrics:
            # print("[D] working on {}...".format(key_query))
            for key_candid in elem.keys():
                if key_candid.startswith(key_query):
                    # print("[D] {} --> {} : {}/{}".format(
                    #     key_candid, key_query, elem[key_candid], ast.literal_eval(elem[key_candid].replace(',', ''))
                    # ))
                    list_sub_key.append(key_query)

                    #measure_tgt = int(elem[key_candid].replace(',', ''))
                    measure_tgt = float(elem[key_candid].replace(',', ''))
                    list_sub_val.append(measure_tgt)
                else:
                    continue

        dict_elem_rslv = {_key: _val for _key, _val in zip(list_sub_key, list_sub_val)}

        for key_tgt, val_tgt in dict_elem_rslv.items():
            dict_aggregate[key_tgt] += val_tgt

    # flop_count_sp:
    #  smsp__sass_thread_inst_executed_op_fadd_pred_on.sum + \
    #  smsp__sass_thread_inst_executed_op_fmul_pred_on.sum + \
    #  smsp__sass_thread_inst_executed_op_ffma_pred_on.sum * 2
    # dram_read_transactions: dram__sectors_read.sum
    # dram_write_transactions: dram__sectors_write.sum

    #eval_flop_count_sp = \
    #    dict_aggregate["smsp__sass_thread_inst_executed_op_fadd_pred_on.sum"] + \
    #    dict_aggregate["smsp__sass_thread_inst_executed_op_fmul_pred_on.sum"] + \
    #    dict_aggregate["smsp__sass_thread_inst_executed_op_ffma_pred_on.sum"] * 2
    #eval_dram_read_transactions = dict_aggregate["dram__sectors_read.sum"]
    #eval_dram_write_transactions = dict_aggregate["dram__sectors_write.sum"]

    #eval_arithmetic_intensity = \
    #    eval_flop_count_sp / ((eval_dram_read_transactions + eval_dram_write_transactions) * 32)


    #dict_aggregate.update({
    #    "report_filename":  os.path.basename(path_ncu_csv_report),
    #    "flop_count_sp": eval_flop_count_sp,
    #    "dram_read_transactions": eval_dram_read_transactions,
    #    "dram_write_transactions": eval_dram_write_transactions,
    #    "arithmetic_intensity": eval_arithmetic_intensity
    #})
    dict_aggregate.update({
        "signature": signature,
        "report_basename":  os.path.splitext(os.path.basename(path_ncu_csv_report))[0],
        "workload": workload,
        "task": task,
        "num_kernel_ops": num_kernel_ops
    })

    # final headers:
    headers = ["signature", "report_basename", "workload", "task", "num_kernel_ops"] + list(target_metrics)

    filename_result_csv = f"result__{dict_aggregate['report_basename']}.csv"

    with open(filename_result_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow(dict_aggregate)

    # pprint(dict_aggregate, indent=4)

    # fin
    return


if __name__ == "__main__":

    _parser = argparse.ArgumentParser()
    _parser.add_argument("--path_report", help="path to raw ncu report", required=True)
    _parser.add_argument("--signature", help="workload group signature", required=False, default="")
    _parser.add_argument("--workload", help="workload name", required=False, default="")
    _parser.add_argument("--task", help="task name", required=False, default="")
    _parser.add_argument("--mode", help="piped or direct", required=True)

    main(parser=_parser)
