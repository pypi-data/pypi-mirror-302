#!/bin/bash

PATH_WORKROOT=/home/frodohong

PATH_CONDAENV=${PATH_WORKROOT}/miniconda3/envs/nsight_cuda12.2

PATH_NCU=${PATH_CONDAENV}/nsight-compute/2023.2.0/target/linux-desktop-glibc_2_11_3-x64
#PATH_NCU=${PATH_WORKROOT}/miniconda3/envs/nsight_cuda12.5/nsight-compute-2024.1.1/target/linux-desktop-glibc_2_11_3-x64

PATH_NCU_REPORT=${PATH_WORKROOT}/Nsight_verbose

BIN_NCU=${PATH_NCU}/ncu
BIN_PYTHON=${PATH_CONDAENV}/bin/python

EXEC_TARGET="${BIN_PYTHON} main.py -p ${1} -i ${2}"

export DT_NOW=$(date +"%Y%m%d-%H%M%S")

stdout_log="${PATH_NCU_REPORT}/stdout_${DT_NOW}.log"
stderr_log="${PATH_NCU_REPORT}/stderr_${DT_NOW}.log"

#NCU_TGT_PROCS="--target-processes application-only"
NCU_TGT_PROCS="--target-processes all"

# plain metrics
# reference1: https://docs.nvidia.com/nsight-compute/pdf/NsightComputeCli.pdf
# reference2: https://docs.nersc.gov/tools/performance/roofline/#arithmetic-intensity
NCU_METRICS="--metrics "
# flop_count_dp:nvprof -> PerfWorks
NCU_METRICS+="smsp__sass_thread_inst_executed_op_dadd_pred_on.sum,smsp__sass_thread_inst_executed_op_dmul_pred_on.sum,smsp__sass_thread_inst_executed_op_dfma_pred_on.sum,"
# flop_count_hp:nvprof -> PerfWorks
NCU_METRICS+="smsp__sass_thread_inst_executed_op_hadd_pred_on.sum,smsp__sass_thread_inst_executed_op_hmul_pred_on.sum,smsp__sass_thread_inst_executed_op_hfma_pred_on.sum,"
# flop_count_sp:nvprof -> PerfWorks
NCU_METRICS+="smsp__sass_thread_inst_executed_op_fadd_pred_on.sum,smsp__sass_thread_inst_executed_op_fmul_pred_on.sum,smsp__sass_thread_inst_executed_op_ffma_pred_on.sum,"
# dram_read_transactions,dram_write_transactions:nvprof -> PerfWorks
NCU_METRICS+="dram__sectors_read.sum,dram__sectors_write.sum,"
# gld_throughput,gld_transactions:nvprof -> PerfWorks
NCU_METRICS+="l1tex__t_bytes_pipe_lsu_mem_global_op_ld.sum.per_second,l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum,"
# gst_throughput,gst_transactions:nvprof -> PerfWorks
NCU_METRICS+="l1tex__t_bytes_pipe_lsu_mem_global_op_st.sum.per_second,l1tex__t_sectors_pipe_lsu_mem_global_op_st.sum,"
# achieved_occupancy:nvprof -> PerfWorks
NCU_METRICS+="sm__warps_active.avg.pct_of_peak_sustained_active,"
# inst_executed,ipc:nvprof -> PerfWorks
NCU_METRICS+="smsp__inst_executed.sum,smsp__inst_executed.avg.per_cycle_active,"
# *_fu_utilization:nvprof -> PerfWorks
NCU_METRICS+="smsp__inst_executed_pipe_fp64.avg.pct_of_peak_sustained_active,smsp__inst_executed_pipe_fp16.avg.pct_of_peak_sustained_active,smsp__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_active,smsp__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active,smsp__inst_executed_pipe_xu.avg.pct_of_peak_sustained_active,sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active,sm__pipe_tensor_op_imma_cycles_active.avg.pct_of_peak_sustained_active,smsp__inst_executed_pipe_tex.avg.pct_of_peak_sustained_active,"
# sysmem_read_*,sysmem_write_*:nvprof -> PerfWorks
NCU_METRICS+="lts__t_sectors_aperture_sysmem_op_read,lts__t_sectors_aperture_sysmem_op_read.sum.per_second,lts__t_sectors_aperture_sysmem_op_read.sum,lts__t_sectors_aperture_sysmem_op_write,lts__t_sectors_aperture_sysmem_op_write.sum.per_second,lts__t_sectors_aperture_sysmem_op_write.sum,"
# gpu time-aware metrics
NCU_METRICS+="gpu__cycles_active.sum,gpu__cycles_elapsed.sum,gpu__time_active.sum,gpu__time_duration_measured_user.sum,gpu__time_duration_measured_wallclock.sum"

NCU_METRICS="--metrics sm__sass_thread_inst_executed.sum,sm__sass_thread_inst_executed_op_bit_pred_on.sum,sm__sass_thread_inst_executed_op_control_pred_on.sum,sm__sass_thread_inst_executed_op_conversion_pred_on.sum,sm__sass_thread_inst_executed_op_dadd_pred_on.sum,sm__sass_thread_inst_executed_op_dfma_pred_on.sum,sm__sass_thread_inst_executed_op_dmul_pred_on.sum,sm__sass_thread_inst_executed_op_fadd_pred_on.sum,sm__sass_thread_inst_executed_op_ffma_pred_on.sum,sm__sass_thread_inst_executed_op_fmul_pred_on.sum,sm__sass_thread_inst_executed_op_fp16_pred_on.sum,sm__sass_thread_inst_executed_op_fp32_pred_on.sum,sm__sass_thread_inst_executed_op_fp64_pred_on.sum,sm__sass_thread_inst_executed_op_hadd_pred_on.sum,sm__sass_thread_inst_executed_op_hfma_pred_on.sum,sm__sass_thread_inst_executed_op_hmul_pred_on.sum,sm__sass_thread_inst_executed_op_integer_pred_on.sum,sm__sass_thread_inst_executed_op_inter_thread_communication_pred_on.sum,sm__sass_thread_inst_executed_op_memory_pred_on.sum,sm__sass_thread_inst_executed_op_misc_pred_on.sum,sm__sass_thread_inst_executed_op_uniform_pred_on.sum,sm__sass_thread_inst_executed_ops_dadd_dmul_dfma_pred_on.sum,sm__sass_thread_inst_executed_ops_fadd_fmul_ffma_pred_on.sum,sm__sass_thread_inst_executed_ops_hadd_hmul_hfma_pred_on.sum,sm__sass_thread_inst_executed_pred_on.sum,sm__inst_executed.sum,sm__sass_inst_executed.sum,smsp__inst_executed.sum,smsp__sass_inst_executed.sum,smsp__sass_thread_inst_executed.sum,smsp__sass_thread_inst_executed_pred_on.sum,smsp__thread_inst_executed.sum,smsp__thread_inst_executed_pred_on.sum,sm__inst_executed_pipe_tensor.sum,smsp__inst_executed_pipe_tensor.sum,sm__throughput.avg.pct_of_peak_sustained_elapsed,dram__sectors_read.sum,dram__sectors_write.sum"
NCU_METRICS+=" --section ComputeWorkloadAnalysis --section InstructionStats --section MemoryWorkloadAnalysis --section Occupancy --section SpeedOfLight --section SpeedOfLight_HierarchicalDoubleRooflineChart --section SpeedOfLight_HierarchicalHalfRooflineChart --section SpeedOfLight_HierarchicalSingleRooflineChart --section SpeedOfLight_HierarchicalTensorRooflineChart --section SpeedOfLight_RooflineChart --section section0"

NCU_METRICS="--section SpeedOfLight_RooflineChart"

#NCU_REPLAY_CFGS="--replay-mode application --app-replay-match grid --app-replay-buffer file --app-replay-mode strict"
#NCU_REPLAY_CFGS="--replay-mode application --app-replay-match grid --app-replay-buffer file --app-replay-mode relaxed"
NCU_REPLAY_CFGS="--replay-mode application --app-replay-match all --app-replay-buffer file --app-replay-mode relaxed"

# Sampling Options:
#  --sampling-interval arg (=auto)       Set the sampling period in the range of [0..31]. Actual frequency is 2 ^ (5 + 
#                                        value) cycles. If set to 'auto', the profiler tries to automatically determine 
#                                        a high sampling frequency without skipping samples or overflowing the output 
#                                        buffer.
#  --sampling-max-passes arg (=5)        Set maximum number of passes used for sampling.
#  --sampling-buffer-size arg (=33554432)
#                                        Set the size of the device-sided allocation for samples in bytes.
NCU_SMP_STRATEGY="--sampling-interval 0 --sampling-max-passes 20 --sampling-buffer-size 268435456"
NCU_SMP_STRATEGY+=" --call-stack --nvtx --disable-profiler-start-stop"

# TF related
# export TF_DISABLE_AUTOTUNE=1
export CUDA_VISIBLE_DEVICES=0

# use $5 as mode switch
if [ -z "${3}" ]; then
    echo "No argument passed."
    exit 128
else
    if [ "${3}" == "direct" ]; then
        ${BIN_NCU} --config-file off --export ${PATH_NCU_REPORT}/${DT_NOW}.nsys-rep ${NCU_TGT_PROCS} ${NCU_METRICS} ${NCU_REPLAY_CFGS} ${NCU_SMP_STRATEGY} --clock-control base \
            ${EXEC_TARGET} > >(ts '[%Y-%m-%d %H:%M:%S]' > "$stdout_log") 2> >(ts '[%Y-%m-%d %H:%M:%S]' > "$stderr_log")
    elif [ "${3}" == "bypass" ]; then
        export LD_LIBRARY_PATH=/opt/amazon/efa/lib:/opt/amazon/openmpi/lib:/opt/aws-ofi-nccl/lib:/usr/local/cuda/lib:/usr/local/cuda:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/cuda/targets/x86_64-linux/lib:/usr/local/lib:/usr/lib
        ${EXEC_TARGET} > >(ts '[%Y-%m-%d %H:%M:%S]' > "$stdout_log") 2> >(ts '[%Y-%m-%d %H:%M:%S]' > "$stderr_log")
    else
        echo "Unknown argument: ${3}"
	exit 128
    fi
fi
