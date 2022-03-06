from __future__ import print_function
import tensorflow as tf
import os 
import datetime

def write_file(file_path, words, clear=False):
    mode = 'a'
    if clear:
        mode = 'w'
    with open(file_path, mode) as f:
        f.write(words)

def model_sum_print(summ):
    with open(SUMMARY_FILE, 'w+') as f:
        print(summ, file=f)

def model_details(model, summary_file):

    with open(summary_file, 'w') as f:
        model.summary(print_fn=lambda x: f.write(x + '\n'))

    
    layers = model.layers
    count = 0
    for layer in layers:
        if isinstance(layer, tf.keras.layers.Dense):
            params = layer.get_weights()
            weights = "Weights: {}\n\n".format(params[0])
            biases = "Biases: {}\n".format(params[1])
            write_file(summary_file, f"## Layer {count}\n\n")
            write_file(summary_file, weights + biases)
            print(weights + biases)
            count += 1


if __name__ == '__main__':
    MODEL_PATH = './models/arch8/20220307_0024'
    file_name = f'{os.path.basename(os.path.dirname(MODEL_PATH))}_{os.path.basename(MODEL_PATH)}.md'
    SUMMARY_FILE = f'./summaries/{file_name}'
    os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True) # creates the directory if it doesnt already exist


    model = tf.keras.models.load_model(MODEL_PATH)
    model_details(model, SUMMARY_FILE)