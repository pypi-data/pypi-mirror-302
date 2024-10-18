import tensorflow as tf, tf_keras
from official.vision.modeling import factory
from official.core import task_factory
from configs.image_classification import resnet

import argparse
parser= argparse.ArgumentParser()
parser.add_argument('-w', '--workload')

args = parser.parse_args()

if __name__ == '__main__':

    workload = args.workload

    NUM_STEPS = 3 # TODO: step fixed to 2 steps; add 3 steps version and consider automation

    config = resnet.base_te_config()
    task = task_factory.get_task(config.task)

    dataset = task.build_inputs(config.task.train_data)

    if workload == 'te_resnet_infer':

        model = factory.build_classification_model(
            input_specs=tf_keras.layers.InputSpec(shape=[None]+list(config.task.model.input_size)),
            model_config=config.task.model
        )

        @tf.function
        def infer(inputs):
            features, _ = inputs
            return model(features)

        @tf.function
        def main_loop(num_steps):
            data_iter = iter(dataset)
            for _ in range(num_steps):
                data = next(data_iter)
                output = infer(data)
            return output

    else: # TODO: placeholder
        def main_loop():
            pass
        
    main_loop(NUM_STEPS)

