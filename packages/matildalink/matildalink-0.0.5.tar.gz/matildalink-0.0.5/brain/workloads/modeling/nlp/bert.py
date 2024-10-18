import tensorflow as tf, tf_keras
from official.core.config_definitions import ExperimentConfig
from official.nlp.modeling import models as nlp_models, networks, layers

class MLBBert(tf_keras.Model):

    def __init__(self, model_config, **kwargs):

        super(MLBBert, self).__init__(**kwargs)

        cls_head_cfgs = model_config.cls_heads
        encoder_cfg = model_config.encoder.bert

        cls_heads = [
            layers.cls_head.ClassificationHead(**cls_head_cfg.as_dict()) for cls_head_cfg in cls_head_cfgs
        ] # build BERT classification heads

        encoder_model = networks.BertEncoderV2( # build BERT encoder
            vocab_size=encoder_cfg.vocab_size,
                num_layers=encoder_cfg.num_layers,
            hidden_size=encoder_cfg.hidden_size,
            max_sequence_length=encoder_cfg.max_position_embeddings)

        self._pretrainer_model = nlp_models.BertPretrainerV2( # build BERT pretrainer model
            encoder_network=encoder_model,
            classification_heads=cls_heads,
            mlm_activation='gelu')

    @tf.function
    def call(self, inputs):
        return self._pretrainer_model(inputs)

    @tf.function
    def train_step(self, inputs):
        with tf.GradientTape() as tape:
            labels = inputs
            outputs = self._pretrainer_model(inputs) # set training=False for BatchNormalization layer, which causes variable update leading to profiling error; this adds inaccuracy in FLOPs calculation
            trainable_var = self._pretrainer_model.trainable_variables
            with tf.name_scope('MaaskedLMTask/losses'):
                lm_prediction_losses = tf_keras.losses.sparse_categorical_crossentropy(
                    labels['masked_lm_ids'],
                    tf.cast(outputs['mlm_logits'], tf.float32),
                    from_logits=True)
                lm_label_weights = labels['masked_lm_weights']
                lm_numerator_loss = tf.reduce_sum(lm_prediction_losses * lm_label_weights)
                lm_denominator_loss = tf.reduce_sum(lm_label_weights)
                mlm_loss = tf.math.divide_no_nan(lm_numerator_loss, lm_denominator_loss)
                if 'next_sentence_labels' in labels:
                    sentence_labels = labels['next_sentence_labels']
                    sentence_outputs = tf.cast(outputs['next_sentence'], dtype=tf.float32)
                    sentence_loss = tf.reduce_mean(tf_keras.losses.sparse_categorical_crossentropy(sentence_labels, sentence_outputs, from_logits=True))
                    loss = mlm_loss + sentence_loss
            grads = tape.gradient(loss, trainable_var)
        return grads