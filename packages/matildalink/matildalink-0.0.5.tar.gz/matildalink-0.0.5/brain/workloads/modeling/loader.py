import tf_keras

from official.core.config_definitions import ExperimentConfig

from .image_classification.resnet import MLBResNet
from .backbone.resnet import BackboneResNet
from .object_detection.retinanet import MLBRetinaNet
from .object_detection.maskrcnn import MLBMaskRCNN
from .nlp.bert import MLBBert

def load(tfm_config: ExperimentConfig):

    # TODO: ensure tfm config has config.task.name attribute set as [image_classification, object_detection, natural_language_processing]
    task = tfm_config.task.name 
    model = None
    if task == 'image_classification':
        input_size = tfm_config.task.model.input_size
        input_specs = tf_keras.layers.InputSpec(shape=[None]+list(input_size))
        spec_idx = tfm_config.task.model.backbone.resnet.spec_idx
        model = MLBResNet(input_specs=input_specs, spec_idx=spec_idx)
    elif task == 'object_detection_retinanet':
        input_size = tfm_config.task.model.input_size
        input_specs = tf_keras.layers.InputSpec(shape=[None]+list(input_size))
        spec_idx = tfm_config.task.model.backbone.resnet.spec_idx
        backbone = BackboneResNet(input_specs=input_specs, spec_idx=spec_idx)
        model = MLBRetinaNet(input_specs=input_specs, backbone=backbone, model_config=tfm_config.task.model)
    elif task == 'object_detection_maskrcnn':
        input_size = tfm_config.task.model.input_size
        input_specs = tf_keras.layers.InputSpec(shape=[None]+list(input_size))
        spec_idx = tfm_config.task.model.backbone.resnet.spec_idx
        backbone = BackboneResNet(input_specs=input_specs, spec_idx=spec_idx)
        model = MLBMaskRCNN(input_specs=input_specs, backbone=backbone, model_config=tfm_config.task.model)
    elif task == 'natural_language_processing':
        model = MLBBert(model_config=tfm_config.task.model)
    else:
        pass

    return model
