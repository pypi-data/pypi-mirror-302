import tensorflow as tf

from feature_extractor import load_resnet_model, resnet_train_graph

def inspect_graph_ops(graph):

    ops = graph.get_operations()
    num_total_ops = len(ops)

    print(f'total #operations: {num_total_ops}')

    for op in ops:

        print('==============================================')
        print(f'operation type: {op.type}')
        print(f'operation name: {op.name}')

        outputs = op.outputs
        print(f'number of outputs {len(outputs)}')
        for output in outputs:
            print(f'output name: {output.name}')
            print(f'output shape: {output.shape}')



if __name__ == '__main__':

    graph_def = resnet_train_graph()

    with tf.Graph().as_default():
        tf.compat.v1.import_graph_def(graph_def)
        with tf.compat.v1.Session() as sess:
            inspect_graph_ops(sess.graph)
