import tensorflow as tf, tf_keras

from typing import List, Tuple, Optional, Callable

from official.modeling import tf_utils
from official.vision.modeling.layers import nn_blocks, nn_layers

CUSTOM_RESNET_SPECS = [[('residual', 2**filter_exp, repeat) for filter_exp in range(6, 10)] for repeat in range(1, 21)]

class BackboneResNet(tf_keras.Model):

    def __init__(
        self, 
        input_specs: tf_keras.layers.InputSpec = tf_keras.layers.InputSpec(
            shape=[None, None, None, 3]),
        spec_idx: int = 0,
        num_classes: int = 10,
        depth_multiplier: float = 1.0,
        resnetd_shortcut: bool = False,
        se_ratio: Optional[float] = None,
        init_stochastic_depth_rate: float = 0.0,
        scale_stem: bool = True,
        activation: str = 'relu',
        use_sync_bn: bool = False,
        norm_momentum: float = 0.99,
        norm_epsilon: float = 0.001,
        kernel_initializer: str = 'VarianceScaling',
        kernel_regularizer: Optional[tf_keras.regularizers.Regularizer] = None,
        bias_regularizer: Optional[tf_keras.regularizers.Regularizer] = None,
        bn_trainable: bool = True,
        skip_logits_layer: bool = False,
        dropout_rate: float = 0.0,
        **kwargs):


        self._block_specs = CUSTOM_RESNET_SPECS[spec_idx]
        self._input_specs = input_specs
        self._num_classes = num_classes
        self._depth_multiplier = depth_multiplier
        self._resnetd_shortcut = resnetd_shortcut
        self._se_ratio = se_ratio
        self._init_stochastic_depth_rate = init_stochastic_depth_rate
        self._scale_stem = scale_stem
        self._use_sync_bn = use_sync_bn
        self._activation = activation
        self._norm_momentum = norm_momentum
        self._norm_epsilon = norm_epsilon
        self._norm = tf_keras.layers.BatchNormalization
        self._kernel_initializer = kernel_initializer
        self._kernel_regularizer = kernel_regularizer
        self._bias_regularizer = bias_regularizer
        self._bn_trainable = bn_trainable

        if tf_keras.backend.image_data_format() == 'channels_last':
            self._bn_axis = -1
        else:
            self._bn_axis = 1

        # Build ResNet.
        inputs = tf_keras.Input(shape=input_specs.shape[1:])
        stem_depth_multiplier = self._depth_multiplier if self._scale_stem else 1.0
        x = tf_keras.layers.Conv2D(
            filters=int(64 * stem_depth_multiplier),
            kernel_size=7,
            strides=2,
            use_bias=False,
            padding='same',
            kernel_initializer=self._kernel_initializer,
            kernel_regularizer=self._kernel_regularizer,
            bias_regularizer=self._bias_regularizer,
        )(inputs)
        x = tf_keras.layers.BatchNormalization(
            axis=self._bn_axis,
            momentum=self._norm_momentum,
            epsilon=self._norm_epsilon,
            trainable=self._bn_trainable,
            synchronized=self._use_sync_bn,
        )(x)
        x = tf_keras.layers.Activation('relu')(x)
        x = tf_keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same')(x)

        endpoints = {}
        for i, spec in enumerate(self._block_specs):
            if spec[0] == 'residual':
                block_fn = nn_blocks.ResidualBlock
            elif spec[0] == 'bottleneck':
                block_fn = nn_blocks.BottleneckBlock
            else:
                raise ValueError('Block fn `{}` is not supported.'.format(spec[0]))

            x = self._block_group(
                inputs=x,
                filters=int(spec[1] * self._depth_multiplier),
                strides=(1 if i == 0 else 2),
                block_fn=block_fn,
                block_repeats=spec[2],
                stochastic_depth_drop_rate=nn_layers.get_stochastic_depth_rate(
                    self._init_stochastic_depth_rate, i + 2, 5),
                name='block_group_l{}'.format(i + 2))
            endpoints[str(i + 2)] = x

        self.output_specs = {l: endpoints[l].get_shape() for l in endpoints}

        super(BackboneResNet, self).__init__(inputs=inputs, outputs=endpoints, **kwargs)

    def _block_group(self,
                    inputs: tf.Tensor,
                    filters: int,
                    strides: int,
                    block_fn: Callable[..., tf_keras.layers.Layer],
                    block_repeats: int = 1,
                    stochastic_depth_drop_rate: float = 0.0,
                    name: str = 'block_group'):
        """Creates one group of blocks for the ResNet model.

        Args:
            inputs: A `tf.Tensor` of size `[batch, channels, height, width]`.
            filters: An `int` number of filters for the first convolution of the
            layer.
            strides: An `int` stride to use for the first convolution of the layer.
            If greater than 1, this layer will downsample the input.
            block_fn: The type of block group. Either `nn_blocks.ResidualBlock` or
            `nn_blocks.BottleneckBlock`.
            block_repeats: An `int` number of blocks contained in the layer.
            stochastic_depth_drop_rate: A `float` of drop rate of the current block
            group.
            name: A `str` name for the block.

        Returns:
            The output `tf.Tensor` of the block layer.
        """
        x = block_fn(
            filters=filters,
            strides=strides,
            use_projection=True,
            stochastic_depth_drop_rate=stochastic_depth_drop_rate,
            se_ratio=self._se_ratio,
            resnetd_shortcut=self._resnetd_shortcut,
            kernel_initializer=self._kernel_initializer,
            kernel_regularizer=self._kernel_regularizer,
            bias_regularizer=self._bias_regularizer,
            activation=self._activation,
            use_sync_bn=self._use_sync_bn,
            norm_momentum=self._norm_momentum,
            norm_epsilon=self._norm_epsilon,
            bn_trainable=self._bn_trainable)(
                inputs)

        for _ in range(1, block_repeats):
            x = block_fn(
                filters=filters,
                strides=1,
                use_projection=False,
                stochastic_depth_drop_rate=stochastic_depth_drop_rate,
                se_ratio=self._se_ratio,
                resnetd_shortcut=self._resnetd_shortcut,
                kernel_initializer=self._kernel_initializer,
                kernel_regularizer=self._kernel_regularizer,
                bias_regularizer=self._bias_regularizer,
                activation=self._activation,
                use_sync_bn=self._use_sync_bn,
                norm_momentum=self._norm_momentum,
                norm_epsilon=self._norm_epsilon,
                bn_trainable=self._bn_trainable)(x)

        return tf_keras.layers.Activation('linear', name=name)(x)
