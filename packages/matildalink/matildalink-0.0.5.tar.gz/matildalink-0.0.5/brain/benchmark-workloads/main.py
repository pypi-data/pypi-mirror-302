import image_classification as ic
import object_detection as od
import nlp

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--experiment', action='store')
parser.add_argument('-m', '--model_dir', action='store')

args = parser.parse_args()

experiment = args.experiment
model_dir = args.model_dir

if experiment == 'image_classification':

    ic.resnet18_cifar10_scratch.prepare_dataset.download_dataset()
    ic.resnet18_cifar10_scratch.train.train_model(model_dir)

elif experiment == 'object_detection_light':

    od.retinanet_resnetfpn_coco_scratch.prepare_dataset.download_dataset()
    od.retinanet_resnetfpn_coco_scratch.train.train_model(model_dir)

elif experiment == 'object_detection_heavy':

    od.maskrcnn_resnetfpn_coco_scratch.prepare_dataset.download_dataset()
    od.maskrcnn_resnetfpn_coco_scratch.train.train_model(model_dir)

elif experiment == 'nlp':

    nlp.bert_wiki20201201_pretrain.prepare_dataset.download_and_prepare()
    nlp.bert_wiki20201201_pretrain.train.train_model(model_dir)

else:
    print('Invalid experiment')

