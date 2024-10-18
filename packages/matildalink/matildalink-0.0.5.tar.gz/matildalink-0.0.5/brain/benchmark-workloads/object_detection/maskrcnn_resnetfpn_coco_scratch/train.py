import tensorflow as tf
import tensorflow_models as tfm

import tempfile

from .config import mrcnn_resnetfpn_coco_scratch 

def train_model(model_dir):

    config = mrcnn_resnetfpn_coco_scratch()
    
    logical_device_names = [logical_device.name for logical_device in tf.config.list_logical_devices()]
    
    if 'GPU' in ''.join(logical_device_names):
        distribution_strategy = tf.distribute.MirroredStrategy()
    else:
        distribution_strategy = tf.distribute.OneDeviceStrategy(logical_device_names[0])
    
    if model_dir:
        with distribution_strategy.scope():
            task = tfm.core.task_factory.get_task(config.task, logging_dir=model_dir)
        
        model, eval_logs = tfm.core.train_lib.run_experiment(
            distribution_strategy=distribution_strategy,
            task=task,
            mode='train_and_eval',
            params=config,
            model_dir=model_dir,
            run_post_eval=True)
    else:
        with tempfile.TemporaryDirectory() as tempdir:
            with distribution_strategy.scope():
                task = tfm.core.task_factory.get_task(config.task, logging_dir=tempdir)
            
            model, eval_logs = tfm.core.train_lib.run_experiment(
                distribution_strategy=distribution_strategy,
                task=task,
                mode='train_and_eval',
                params=config,
                model_dir=tempdir,
                run_post_eval=True)
    
    return model, eval_logs

if __name__ == '__main__':
    train_model()

