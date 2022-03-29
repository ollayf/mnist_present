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
LR = 0.001
EPOCHS = 200
BATCH_SIZE = 64

objects = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = objects.load_data()
print('train_images shape:', train_images.shape)
print('test_images shape:', test_images.shape)
print('train_labels shape:', train_labels.shape)

# # for i in range(9):
# #     plt.subplot(330 + 1 + i)
# #     plt.imshow(train_images[i])
# #     print(train_labels[i])
# # plt.show()

train_images = train_images / 255
test_images = test_images / 255

train_labels = tf.keras.utils.to_categorical(train_labels)
test_labels = tf.keras.utils.to_categorical(test_labels)

validation_data = (test_images[:100], test_labels[:100])

print(train_labels.shape)

def train():
    ARCH_DIR = './models/arch40'
    model = models.build_arch40(learning_rate = LR)
    stopped = False # if the training was stopped aburptly for wtv reason
    try:
        # Update weights using MNIST train dataset
        model.fit(train_images, train_labels, 
        epochs = EPOCHS, batch_size = BATCH_SIZE,
        validation_data = validation_data,
        shuffle=True)
    except KeyboardInterrupt:
        print("Stopped by user")
        stopped = True

    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('test_acc:', test_acc)

    # SAVING MODEL

    curr_dt = datetime.datetime.now()
    curr_time = curr_dt.strftime("%Y%m%d_%H%M")

    model_path = os.path.join(ARCH_DIR, curr_time)
    results_path = os.path.join(ARCH_DIR, 'results.json')

    data = read_json(results_path)
    print(data)

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