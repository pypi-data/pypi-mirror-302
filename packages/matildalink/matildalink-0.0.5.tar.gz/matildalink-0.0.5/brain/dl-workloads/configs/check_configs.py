from pprint import PrettyPrinter as pp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--experiment', action='store')
parser.add_argument('-t', '--type', action='store')

args = parser.parse_args()

experiment = args.experiment
workload_type = args.type

from nlp import bert_wiki
from object_detection import retinanet_resnetfpn_coco, maskrcnn_resnetfpn_coco
from image_classification import resnet18_cifar10

if __name__ == '__main__':

    if experiment == 'ic':
        if workload_type == 'train':
            configs = resnet18_cifar10.train_config()
        else:
            configs = resnet18_cifar10.inference_config()
    elif experiment == 'odl':
        if workload_type == 'train':
            configs = retinanet_resnetfpn_coco.train_config()
        else:
            configs = retinanet_resnetfpn_coco.inference_config()
        pass
    elif experiment == 'odh':
        if workload_type == 'train':
            configs = maskrcnn_resnetfpn_coco.train_config()
        else:
            configs = maskrcnn_resnetfpn_coco.inference_config()
    elif experiment == 'nlp':
        if workload_type == 'train':
            configs = bert_wiki.train_config()
        else:
            configs = bert_wiki.inference_config()
    else:
        configs = {}

    pp(indent=4).pprint(configs.as_dict())
