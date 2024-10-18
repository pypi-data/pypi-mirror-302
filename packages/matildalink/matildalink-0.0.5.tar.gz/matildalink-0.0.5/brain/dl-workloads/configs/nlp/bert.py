import tensorflow_models as tfm
from official.nlp.configs.encoders import BertEncoderConfig
import official.nlp.configs.pretraining_experiments as exp_config

# bert-related constants
MIN_HIDDEN_UNITS = 12*30
UNIT_INCREMENT = 10

def generate_bert_encoder_configs(num_att_heads=12, num_cfgs=10):
    hidden_units_specs = range(MIN_HIDDEN_UNITS, MIN_HIDDEN_UNITS + num_att_heads * UNIT_INCREMENT * num_cfgs + 1,  num_att_heads * UNIT_INCREMENT)
    num_layers_list = [12, 13]
    return [
        BertEncoderConfig(hidden_size=hidden_size, num_layers=num_layers) 
            for hidden_size in hidden_units_specs 
            for num_layers in num_layers_list
    ]


def base_te_config():
    return train_config(batch_size=8, steps=600, steps_per_loop=100)

def train_config(batch_size, steps, steps_per_loop):

    config = exp_config.bert_text_wiki_pretraining()

    config.task.train_data.global_batch_size = batch_size
    config.task.train_data.seq_length = 8
    config.task.train_data.max_predictions_per_seq = 19
    config.task.train_data.vocab_file_path = './data/vocab.txt'
    config.task.validation_data = None

    config.trainer.optimizer_config.warmup.polynomial.warmup_steps = 10000
    config.trainer.optimizer_config.learning_rate.polynomial.decay_steps = 1000000
    config.trainer.train_steps = steps
    config.trainer.steps_per_loop = steps_per_loop

    return config

def inference_config(batch_size, steps):

    config = exp_config.bert_text_wiki_pretraining()

    config.task.validation_data.global_batch_size = batch_size
    config.task.validation_data.seq_length = 8
    config.task.validation_data.max_predictions_per_seq = 19
    config.task.validation_data.vocab_file_path = './data/vocab.txt'

    config.trainer.optimizer_config.warmup.polynomial.warmup_steps = 10000
    config.trainer.optimizer_config.learning_rate.polynomial.decay_steps = 1000000
    config.trainer.validation_steps = steps
    config.trainer.steps_per_loop = 1000

    return config
