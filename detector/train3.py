import tensorflow as tf
import tensorflow_datasets as tfds
import cv2

(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., tf.one_hot(label, 10)

gen = ds_train.__iter__()
curr = gen.next()
print(curr[0].shape)
print(curr[0].numpy())
print(curr[1].shape)

input()

ds_train = ds_train.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)

ds_train = ds_train.cache()
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
ds_train = ds_train.batch(128)
ds_train = ds_train.prefetch(tf.data.AUTOTUNE)

ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = ds_test.batch(128)
ds_test = ds_test.cache()
ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='sigmoid'),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(
    optimizer=tf.keras.optimizers.SGD(0.05),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics=[tf.keras.metrics.Accuracy()],
)

model.fit(
    ds_train,
    epochs=100,
    validation_data=ds_test,
)
test_loss, test_acc = model.evaluate(ds_test)