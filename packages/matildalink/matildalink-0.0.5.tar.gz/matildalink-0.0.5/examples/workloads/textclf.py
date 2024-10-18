"""
[소스 출처] https://www.tensorflow.org/tutorials/keras/text_classification?_gl=1*17xamlf*_up*MQ..*_ga*MzgwNDM3OTgxLjE3MjgwMzQzMDE.*_ga_W0YLR4190T*MTcyODAzNDMwMS4xLjAuMTcyODAzNDMxNy4wLjAuMA..

[실행 환경] 사무실 GPU 서버에서 쓰던 Conda 개발환경에서 특별히 문제 없이 실행되어,
아래에 Python 버전과 이미 설치되어 있던 Tensorflow 관련 패키지들 참고로 기록해둠.

[Python 버전] 3.10.14

[이미 설치되어 있던 패키지들]
tensorflow                2.17.0                   pypi_0    pypi
tensorflow-datasets       4.9.6                    pypi_0    pypi
tensorflow-hub            0.16.1                   pypi_0    pypi
tensorflow-io-gcs-filesystem 0.37.1                   pypi_0    pypi
tensorflow-metadata       1.16.0                   pypi_0    pypi
tensorflow-model-optimization 0.8.0                    pypi_0    pypi
tensorflow-text           2.17.0                   pypi_0    pypi
termcolor                 2.4.0                    pypi_0    pypi
text-unidecode            1.3                      pypi_0    pypi
textual                   0.78.0                   pypi_0    pypi
tf-keras                  2.17.0                   pypi_0    pypi
tf-models-official        2.17.0                   pypi_0    pypi
tf-slim                   1.1.0                    pypi_0    pypi

[Workload 및 출력 설명]
- Sentiment analysis (영화 리뷰 긍정 vs. 부정 분류) - 학습 workload
- 총 10 epochs
- 데이터 로딩/전처리부 제외하고 "순수 학습부"만 elapsed time 계산
- Elapsed time 출력

"""

import os
import re
import shutil
import string
import tensorflow as tf
from time import time

from tensorflow.keras import layers
from tensorflow.keras import losses

# ===
# Download and explore the IMDB dataset
# ===
url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"

dataset = tf.keras.utils.get_file("aclImdb_v1", url,
                                    untar=True, cache_dir='.',
                                    cache_subdir='')

#dataset_dir = os.path.join(os.path.dirname(dataset), 'aclImdb')
dataset_dir = 'aclImdb_v1/aclImdb'
os.listdir(dataset_dir) #
train_dir = os.path.join(dataset_dir, 'train')
os.listdir(train_dir) #

sample_file = os.path.join(train_dir, 'pos/1181_9.txt')
with open(sample_file) as f:
  print(f.read())

# ===
# Load the dataset
# ===
remove_dir = os.path.join(train_dir, 'unsup')
shutil.rmtree(remove_dir)

batch_size = 32
seed = 42

raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    'aclImdb_v1/aclImdb/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    'aclImdb_v1/aclImdb/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)

raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    'aclImdb_v1/aclImdb/test',
    batch_size=batch_size)

# ===
# Prepare the dataset for training
# ===
def custom_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
  return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation),
                                  '')
max_features = 10000
sequence_length = 250

vectorize_layer = layers.TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Make a text-only dataset (without labels), then call adapt
train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

# ===
# Configure the dataset for performance
# ===
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

# ===
# Create the model
# ===
embedding_dim = 16

model = tf.keras.Sequential([
  layers.Embedding(max_features, embedding_dim),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(1, activation='sigmoid')])

#model.summary()

# ===
# Loss function and optimizer
# ===
model.compile(loss=losses.BinaryCrossentropy(),
              optimizer='adam',
              metrics=[tf.metrics.BinaryAccuracy(threshold=0.5)])

# ===
# Train the model
# ===

time_start = time()

epochs = 10
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

time_end = time()
elapsed_time = time_end - time_start # NOTE
print("Elapsed time: ", elapsed_time)

# ===
# Evaluate the model
# ===
print("Now, evaluate the trained model..")
loss, accuracy = model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

