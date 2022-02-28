import tensorflow as tf

def build_arch1(learning_rate, summary=True):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (28, 28)))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(100, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(56, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(56, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    if summary:
        model.summary()

    model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
                loss = tf.keras.losses.MeanSquaredError(),
                metrics = ['accuracy'])
    
    return model

def build_arch2(learning_rate, summary=True):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (28, 28)))
    model.add(tf.keras.layers.Dense(56, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    if summary:
        model.summary()

    model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
                loss = tf.keras.losses.MeanSquaredError(),
                metrics = ['accuracy'])
    
    return model

def build_arch3(learning_rate, summary=True):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (28, 28)))
    model.add(tf.keras.layers.Dense(20, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    if summary:
        model.summary()

    model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
                loss = tf.keras.losses.MeanSquaredError(),
                metrics = ['accuracy'])
    
    return model

def build_arch4(learning_rate, summary=True):
    '''
    Downsample the mnist dataset to 
    '''
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (14, 14)))
    model.add(tf.keras.layers.Dense(20, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
                loss = tf.keras.losses.MeanSquaredError(),
                metrics = ['accuracy'])
    
    return model

def build_arch5(learning_rate, summary=True):
    '''
    Downsample the mnist dataset to 
    '''
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (28, 28)))
    model.add(tf.keras.layers.Dense(20, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    model.compile(
        optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
        loss = tf.keras.losses.MeanSquaredError(),
        metrics = [tf.keras.metrics.Accuracy()]
    )
    
    return model

def build_arch10(learning_rate, summary=True):
    '''
    The goal of the 10 series is
    to reduce the number of calculations
    Referenced from arch4'''
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Resizing(14, 14, interpolation='bilinear'))
    model.add(tf.keras.layers.Flatten(input_shape = (14, 14)))
    model.add(tf.keras.layers.Dense(20, activation=tf.nn.sigmoid))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    # if summary:
    #     model.summary()

    model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate = learning_rate), 
                loss = tf.keras.losses.MeanSquaredError(),
                metrics = ['accuracy'])
    
    return model