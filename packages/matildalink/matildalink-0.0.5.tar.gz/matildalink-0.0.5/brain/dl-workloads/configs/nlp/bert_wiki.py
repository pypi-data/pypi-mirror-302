import tensorflow_models as tfm
import official.nlp.configs.pretraining_experiments as exp_config
import pprint
pp = pprint.PrettyPrinter(indent=4)

def train_config():

    config = exp_config.bert_text_wiki_pretraining()

    config.task.train_data.global_batch_size = 8
    config.task.train_data.seq_length = 8
    config.task.train_data.max_predictions_per_seq = 19
    config.task.train_data.vocab_file_path = './data/vocab.txt'
    config.task.validation_data = None

    config.trainer.optimizer_config.warmup.polynomial.warmup_steps = 10000
    config.trainer.optimizer_config.learning_rate.polynomial.decay_steps = 1000000
    config.trainer.train_steps = 5000
    config.trainer.steps_per_loop = 1000

    return config

def inference_config():

    config = exp_config.bert_text_wiki_pretraining()

    config.task.validation_data.global_batch_size = 8
    config.task.validation_data.seq_length = 8
    config.task.validation_data.max_predictions_per_seq = 19
    config.task.validation_data.vocab_file_path = './data/vocab.txt'

    config.trainer.optimizer_config.warmup.polynomial.warmup_steps = 10000
    config.trainer.optimizer_config.learning_rate.polynomial.decay_steps = 1000000
    config.trainer.validation_steps = 5000
    config.trainer.steps_per_loop = 1000

    return config
