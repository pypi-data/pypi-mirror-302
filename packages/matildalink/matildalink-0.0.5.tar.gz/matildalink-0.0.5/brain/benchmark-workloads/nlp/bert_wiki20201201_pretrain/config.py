import tensorflow_models as tfm
import official.nlp.configs.pretraining_experiments as exp_config
import pprint
pp = pprint.PrettyPrinter(indent=4)

def bert_wiki_pretrain():
    # config = tfm.core.exp_factory.get_exp_config('bert/pretraining')
    config = exp_config.bert_text_wiki_pretraining()
    config.task.train_data.global_batch_size = 8
    config.task.train_data.seq_length = 8
    config.task.train_data.max_predictions_per_seq = 19
    config.task.train_data.vocab_file_path = './vocab.txt'
    config.task.validation_data.global_batch_size = 8
    config.task.validation_data.seq_length = 8
    config.task.validation_data.max_predictions_per_seq = 19
    config.task.validation_data.vocab_file_path = './vocab.txt'
    config.trainer.optimizer_config.warmup.polynomial.warmup_steps = 10000
    config.trainer.optimizer_config.learning_rate.polynomial.decay_steps = 1000000
    pp.pprint(config.as_dict())
    return config
