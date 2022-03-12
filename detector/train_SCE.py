'''
This code was inspired by:
https://www.tensorflow.org/datasets/keras_example
'''

import tensorflow as tf
import tensorflow_datasets as tfds
import cv2
import datetime
import os
from utils.files import read_json, write_json
import utils.models as models

# hyper params
EPOCHS = 40
BATCH_SIZE = 128
LR = 0.001

(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label

ds_train = ds_train.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)

ds_train = ds_train.cache()
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
ds_train = ds_train.batch(BATCH_SIZE)
ds_train = ds_train.prefetch(tf.data.AUTOTUNE)

ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = ds_test.batch(BATCH_SIZE)
ds_test = ds_test.cache()
ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

ARCH_DIR = './models/arch40'
model = models.build_arch40(learning_rate= LR)

stopped = False
try:
    model.fit(
        ds_train,
        epochs=EPOCHS,
        validation_data=ds_test,
    )
except KeyboardInterrupt:
    stopped = True

test_loss, test_acc = model.evaluate(ds_test)
print("Test Loss:", test_loss)
print("Test accuracy:", test_acc)


# SAVING MODEL

curr_dt = datetime.datetime.now()
curr_time = curr_dt.strftime("%Y%m%d_%H%M")

model_path = os.path.join(ARCH_DIR, curr_time)
results_path = os.path.join(ARCH_DIR, 'results.json')

data = read_json(results_path)

model_data = {
    'time_completed': curr_time,
    'test_loss': test_loss,
    'test_acc': test_acc,
    'model_path': model_path,
    'epochs': EPOCHS,
    'batch_size': BATCH_SIZE,
    'learning_rate': LR,
    'method' : "Adam",
    'loss': "SparseCategoricalCrossentropy",
    'Accuracy': 'SparseCategoricalAccuracy'
}
if stopped:
    model_data['stopped'] = True

data['models'].append(model_data)

write_json(results_path, data)

model.save(model_path)