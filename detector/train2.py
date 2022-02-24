from cgi import test
import json
import datetime
import os

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from matplotlib import pyplot as plt

from utils.files import read_json, write_json
import utils.models as models


# HYPER PARAMS
LR = 0.01
EPOCHS = 100
BATCH_SIZE = 128

(train_ds, test_ds), ds_info = tfds.load(
    'mnist', 
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)


def normalise_img(image, label):
    return tf.cast(image, tf.float32) / 255., label

train_ds = train_ds.map(
    normalise_img, num_parallel_calls=tf.data.AUTOTUNE)

train_ds = train_ds.cache()
train_ds = train_ds.shuffle(ds_info.splits['train'].num_examples)
train_ds = train_ds.batch(BATCH_SIZE)
train_ds = train_ds.prefetch(tf.data.AUTOTUNE)

test_ds = test_ds.map(
    normalise_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = test_ds.batch(BATCH_SIZE)
test_ds = test_ds.cache()
test_ds = test_ds.prefetch(tf.data.AUTOTUNE)


def train():
    ARCH_DIR = './models/arch5'
    model = models.build_arch5(learning_rate = LR)
    stopped = False # if the training was stopped aburptly for wtv reason
    try:
        model.fit(train_ds,
            epochs=EPOCHS,
            validation_data = test_ds)
    except KeyboardInterrupt:
        print("Stopped by user")
        stopped = True

    test_loss, test_acc = model.evaluate(test_ds)
    print('test_acc:', test_acc)

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
        'learning_rate': LR
    }
    if stopped:
        model_data['stopped'] = True

    data['models'].append(model_data)

    write_json(results_path, data)

    model.save(model_path)

if __name__ == '__main__':
    model = train()