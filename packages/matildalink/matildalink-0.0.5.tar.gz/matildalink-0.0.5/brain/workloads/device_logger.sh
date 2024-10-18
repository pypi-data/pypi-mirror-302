#!/bin/bash

# python main.py -p configs/te/te_resnet_inference.yaml --device-log > ./device_logs/te_resnet_inference.log
# python main.py -p configs/te/te_resnet_train.yaml --device-log > ./device_logs/te_resnet_train.log
# python main.py -p configs/te/te_retinanet_inference.yaml --device-log > ./device_logs/te_retinanet_inference.log
# python main.py -p configs/te/te_retinanet_train.yaml --device-log > ./device_logs/te_retinanet_train.log
# python main.py -p configs/te/te_maskrcnn_inference.yaml --device-log > ./device_logs/te_maskrcnn_inference.log
# python main.py -p configs/te/te_maskrcnn_train.yaml --device-log > ./device_logs/te_maskrcnn_train.log
# python main.py -p configs/te/te_bert_inference.yaml --device-log > ./device_logs/te_bert_inference.log
# python main.py -p configs/te/te_bert_train.yaml --device-log > ./device_logs/te_bert_train.log

python parse_log.py -p ./device_logs/te_resnet_inference.log
python parse_log.py -p ./device_logs/te_resnet_train.log
python parse_log.py -p ./device_logs/te_retinanet_inference.log
python parse_log.py -p ./device_logs/te_retinanet_train.log
python parse_log.py -p ./device_logs/te_maskrcnn_inference.log
python parse_log.py -p ./device_logs/te_maskrcnn_train.log
python parse_log.py -p ./device_logs/te_bert_inference.log
python parse_log.py -p ./device_logs/te_bert_train.log
