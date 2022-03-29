import tensorflow as tf
import cv2
import numpy as np
import os


def classify(img_path, model):
    img = cv2.imread(img_path, 0)

    # print(np.amax(img))
    # print(np.amin(img))
    max_val = np.amax(img)


    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_LINEAR)
    img_tensor = tf.convert_to_tensor(img, dtype=tf.int8)
    img_tensor = tf.cast(img, tf.float32) / max_val
    img_tensor = tf.reshape(img_tensor, (1, 28, 28))

    # print(img.shape)

    result_tensor = model.predict(img_tensor)
    # print(result_tensor)
    result = tf.math.argmax(result_tensor[0])
    print("Answer:", int(result))
    print("Confidence:", result_tensor[0][int(result)])


if __name__ == '__main__':

    MODEL_PATH = 'detector/models/arch8/20220312_2200'
    IMG_PATH = 'detector/datasets/mine/9.png'

    model = tf.keras.models.load_model(MODEL_PATH)
    model.summary()
    classify(IMG_PATH, model)
