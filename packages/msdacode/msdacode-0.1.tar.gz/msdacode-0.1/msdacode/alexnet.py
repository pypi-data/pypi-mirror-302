def alexnet():
    code = '''
    import tensorflow as tf
    from tensorflow.keras import layers, models
    # Initialize the AlexNet model
    model = models.Sequential()

    # 1st Convolutional Layer
    model.add(layers.Conv2D(96, (11, 11), strides=(4, 4), input_shape=(227, 227, 3), padding='valid', activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    # 2nd Convolutional Layer
    model.add(layers.Conv2D(256, (5, 5), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    # 3rd Convolutional Layer
    model.add(layers.Conv2D(384, (3, 3), padding='same', activation='relu'))

    # 4th Convolutional Layer
    model.add(layers.Conv2D(384, (3, 3), padding='same', activation='relu'))

    # 5th Convolutional Layer
    model.add(layers.Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    # Flatten the output for the fully connected layers
    model.add(layers.Flatten())

    # 1st Fully Connected Layer
    model.add(layers.Dense(9216, activation='relu'))
    model.add(layers.Dropout(0.5))  # Dropout layer to avoid overfitting

    # 2nd Fully Connected Layer
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))

    # 3ed Fully Connected Layer
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(0.5))

    # Output Layer (1000 classes)
    model.add(layers.Dense(1000, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Model summary
    model.summary()

    '''
    print(code)