import tensorflow as tf
import tensorflow_datasets as tfds

from keras.applications.resnet50 import ResNet50, preprocess_input

from keras.optimizers import SGD
from keras.optimizers.schedules import PiecewiseConstantDecay

import datetime
import pickle

from utils import TimingCallback

BATCH_SIZE = 32

#=================== processor preparation ===================#
gpus = tf.config.list_physical_devices('GPU')
print(f'Number of GPUs available: {len(gpus)}')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

#=================== data preparation ===================#
ds_name = 'imagenet_v2'
train_percentage = 80
split = [f'test[:{train_percentage}%]', f'test[{train_percentage}%:]']

ds_train, ds_test = tfds.load(ds_name, split=split)

def preprocess(example):
    img = example['image']
    img = tf.image.resize(img, [224,224])
    label = example['label']
    return preprocess_input(img), label

def create_pipeline(ds):
    ds = ds.map(preprocess)
    ds = ds.cache()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds

ds_train = create_pipeline(ds_train)
ds_test = create_pipeline(ds_test)

#=================== model preparation ===================#

boundaries = [30*8000/32, 60*8000/32, 80*8000/32]
values = [0.1 * 32/256, 0.01 * 32/256, 0.001 * 32/256, 0.0001 *32/256]

learning_rate_schedule = PiecewiseConstantDecay(boundaries, values)
optimizer = SGD(momentum=0.9, learning_rate=learning_rate_schedule)

model = ResNet50(weights=None)
model.summary()
model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#=================== training preparation ===================#

# training hyperparameters
epochs = 100

# tensorboard setup
log_dir = f'./logs/{ds_name}/' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tbc = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
# earlystopping setup
esc = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=10)
# model checkpoint setup
checkpoint_path = f'./checkpoints/{ds_name}' + '/{epoch:02d}-{accuracy:.2f}.keras'
cc = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, monitor='accuracy', mode='max', save_best_only=True)
# timer callback setup
tc = TimingCallback()

callbacks = [tbc, esc, cc, tc]

history = model.fit(ds_train, validation_data=ds_test, epochs=epochs, callbacks=callbacks)

with open("./history/resnet50_history.pkl", "wb") as f:
    pickle.dump(history, f)

with open("./history/resnet50_timing.pkl", "wb") as f:
    pickle.dump(tc.logs, f)