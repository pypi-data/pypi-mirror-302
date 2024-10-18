import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

from configs import loader as configloader
from data import loader as dataloader
from modeling import loader as modelloader

from multiprocessing import Process, Value
import glob

def write_results(output_path, config_path, flops, imem, pmem):
    with open(output_path, 'a') as f:
        f.write(f'{config_path},{flops},{imem},{pmem}\n')

def calculate_graph_ops_memory(graph): # estimates activation memory

    total_activation_memory = 0
    ops = graph.get_operations()
    num_total_ops = len(ops)
    num_skipped_ops = 0

    for op in ops:
        # Skip irrelevant ops
        if op.type in ['Const', 'Assign', 'NoOp', 'Placeholder']:
            num_skipped_ops += 1
            continue

        for output in op.outputs:
            shape = output.get_shape()
            # Skip tensors with undefined shape
            if not shape.is_fully_defined():
                num_skipped_ops += 1
                continue  # Skip tensors with undefined shape

            num_elements = 1
            for dim in shape:
                num_elements *= dim
            tensor_memory = num_elements * 4 # assume float32 (4 bytes per element)
            total_activation_memory += tensor_memory

    return total_activation_memory

def extract_features(mlb_config, flops, imem, pmem):

    gpus = tf.config.list_physical_devices('GPU')
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except:
        print('Error: invalid device / cannot modify virtual devices once initialized.')
        exit()

    tfm_config, is_train, num_steps = mlb_config.tfm_config, mlb_config.is_train, mlb_config.num_steps

    needs_additional_kwargs = tfm_config.task.name == 'object_detection_maskrcnn'
    is_self_supervised = tfm_config.task.name == 'natural_language_processing'

    # load data
    dataset = dataloader.load(tfm_config=tfm_config)
    example_data = next(iter(dataset))

    # load model
    model = modelloader.load(tfm_config=tfm_config)

    # build model
    if needs_additional_kwargs:
        features, labels = example_data
        model_kwargs = {
            'image_shape': labels['image_info'][:,1,:],
            'anchor_boxes': labels['anchor_boxes'],
            'gt_boxes': labels['gt_boxes'],
            'gt_classes': labels['gt_classes']
        }
        _ = model(features, **model_kwargs)
    elif is_self_supervised:
        _ = model(example_data)
    else:
        features, labels = example_data
        _ = model(features)

    # define tensorflow graph
    target_fn = None
    if is_train:
        @tf.function
        def target_fn(data):
            return model.train_step(data)
    else:
        if needs_additional_kwargs:
            @tf.function
            def target_fn(data):
                features, labels = data
                model_kwargs = {
                        'image_shape': labels['image_info'][:,1,:],
                        'anchor_boxes': labels['anchor_boxes'],
                        'gt_boxes': labels['gt_boxes'],
                        'gt_classes': labels['gt_classes']
                }
                return model(features, **model_kwargs)
        elif is_self_supervised:
            @tf.function
            def target_fn(data):
                return model(data)
        else:
            @tf.function
            def target_fn(data):
                features, labels = data
                return model(features)

    concrete_func = target_fn.get_concrete_function(example_data)
    graph_def = convert_variables_to_constants_v2(concrete_func).graph.as_graph_def()

    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def, name='')
        with tf.compat.v1.Session() as sess:
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
            flops_profiler = tf.compat.v1.profiler.profile(
                graph=sess.graph,
                run_meta=tf.compat.v1.RunMetadata(),
                cmd='scope',
                options=opts)

            flops.value = flops_profiler.total_float_ops
            imem.value = calculate_graph_ops_memory(sess.graph)
            pmem.value = model.count_params() * 4
    

if __name__ == '__main__':

    # te + tr
    '''
    te = glob.glob('./configs/te/*.yaml')
    tr = glob.glob('./configs/tr/*.yaml')
    config_paths = te+tr
    '''

    # re-calculate bert_train workloads
    # config_paths = glob.glob('./configs/tr/tr_bert_train_*.yaml') + ['./configs/te/te_bert_train.yaml']

    config_paths = ['./configs/te/step2/te_resnet_train.yaml']

    # target output path
    output_path = './features/feature_data_v1.1.csv'

    for config_path in config_paths:

        mlb_config = configloader.load(config_path=config_path)
        tfm_config, is_train, num_steps = mlb_config.tfm_config, mlb_config.is_train, mlb_config.num_steps

        flops = Value('d', 0.0) # total number of floating operations (fp32)
        imem = Value('d', 0.0) # intermediate memory
        pmem = Value('d', 0.0) # parameter memory

        profile_process = Process(target=extract_features, args=(mlb_config, flops, imem, pmem))
        profile_process.start()
        profile_process.join()

        # write_results(output_path, config_path, flops.value, imem.value, pmem.value)
