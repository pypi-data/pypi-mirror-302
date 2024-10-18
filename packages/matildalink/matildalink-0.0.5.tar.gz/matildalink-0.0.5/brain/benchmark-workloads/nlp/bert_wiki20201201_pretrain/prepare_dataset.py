import tensorflow_datasets as tfds
from tensorflow_text.tools.wordpiece_vocab import bert_vocab_from_dataset as bert_vocab

def download_and_prepare():
    ds, ds_info = download_dataset()
    dataset = ds['train'].map(lambda doc: doc['text'])
    generate_vocabulary(dataset)

def download_dataset():
    ds, ds_info = tfds.load('wikipedia/20201201.en', with_info=True)
    return ds, ds_info

def write_vocab_file(filepath, vocab):
  with open(filepath, 'w') as f:
    for token in vocab:
      print(token, file=f)

def generate_vocabulary(dataset):

    bert_tokenizer_params=dict(lower_case=True)
    reserved_tokens=["[PAD]", "[UNK]", "[START]", "[END]"]

    bert_vocab_args = dict(
        # The target vocabulary size
        vocab_size = 8000,
        # Reserved tokens that must be included in the vocabulary
        reserved_tokens=reserved_tokens,
        # Arguments for `text.BertTokenizer`
        bert_tokenizer_params=bert_tokenizer_params,
        # Arguments for `wordpiece_vocab.wordpiece_tokenizer_learner_lib.learn`
        learn_params={},
    )

    wiki_vocab = bert_vocab.bert_vocab_from_dataset(
        dataset.batch(50).prefetch(2),
        **bert_vocab_args
    )

    write_vocab_file('./vocab.txt', wiki_vocab)

if __name__ == '__main__':
    download_and_prepare()
