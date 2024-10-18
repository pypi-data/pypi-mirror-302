from .image_classification import resnet18
from .nlp import bert
from .object_detection import retinanet, maskrcnn

def load(model, is_train, batch_size, steps, steps_per_loop):

    if model == 'resnet18':
        config = resnet18.train_config(batch_size, steps, steps_per_loop) if is_train else resnet18.inference_config(batch_size, steps)
    elif model == 'bert_base':
        config = bert.train_config(batch_size, steps, steps_per_loop) if is_train else bert.inference_config(batch_size, steps)
    elif model == 'retinanet':
        config = retinanet.train_config(batch_size, steps, steps_per_loop) if is_train else retinanet.inference_config(batch_size, steps)
    elif model == 'maskrcnn':
        config = maskrcnn.train_config(batch_size, steps, steps_per_loop) if is_train else maskrcnn.inference_config(batch_size, steps)
    else:
        print(f'no experiment with model type: {model}')
        config = None

    return config
