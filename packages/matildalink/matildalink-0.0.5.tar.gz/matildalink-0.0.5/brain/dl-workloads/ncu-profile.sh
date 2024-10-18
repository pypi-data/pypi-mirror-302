#!/bin/bash

BIN_NCU=/usr/local/cuda-12.3/bin/ncu
BIN_PYTHON=/opt/tensorflow/bin/python3.10

PATH_NCU_REPORT=./ncu-reports

EXEC_TARGET="${BIN_PYTHON} unit_workload.py -w ${1}"

export DT_NOW=$(date +"%Y%m%d-%H%M%S")

NCU_REPLAY_CFGS="--replay-mode application --app-replay-match grid --app-replay-mode relaxed"

NCU_OUTPUT_CFGS="--page raw --csv"

${BIN_NCU} --export ${PATH_NCU_REPORT}/${1}_${DT_NOW} ${NCU_OUTPUT_CFGS} --section SpeedOfLight_RooflineChart ${NCU_REPLAY_CFGS} ${EXEC_TARGET} | grep -v '^==' > ${PATH_NCU_REPORT}/${1}_${DT_NOW}.csv

