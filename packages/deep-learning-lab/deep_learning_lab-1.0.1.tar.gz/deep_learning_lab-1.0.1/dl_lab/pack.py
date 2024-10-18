def code():
    # Ex No 2 - Create a simple Neural network to perform classification

    import pandas as pd
    import tensorflow as tf
    from sklearn.model_selection import train_test_split
    df = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/insurance_data.csv')
    X = df[['age ', 'affordibility']]
    y = df['bought_insurance']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=25)
    X_train_scaled = X_train.copy()
    X_train_scaled['age '] /= 100
    X_test_scaled = X_test.copy()
    X_test_scaled['age '] /= 100
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, input_shape=(2,), activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train_scaled, y_train, epochs=500, verbose=0)
    model.evaluate(X_test_scaled, y_test)
    predictions = model.predict(X_test_scaled)
    coef, intercept = model.get_weights()
    coef, intercept



    #Ex No 3 - Test the performance of multi-layer neural network with different activation functions

    import pandas as pd
    import tensorflow as tf
    from sklearn.model_selection import train_test_split
    df = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/insurance_data.csv')
    X = df[['age ', 'affordibility']]
    y = df['bought_insurance']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=25)
    X_train_scaled = X_train.copy()
    X_train_scaled['age '] /= 100
    X_test_scaled = X_test.copy()
    X_test_scaled['age '] /= 100
    def build_and_train_model(activation, optimizer, loss, epochs=5, batch_size=None):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(1, input_shape=(2,), activation=activation, kernel_initializer='ones', bias_initializer='zeros')
        ])
        model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
        model.fit(X_train_scaled, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
        return model
    configurations = [
        ('sigmoid', 'adam', 'binary_crossentropy'),
        ('relu', 'adam', 'binary_crossentropy'),
        ('tanh', 'adam', 'binary_crossentropy'),
        ('tanh', 'sgd', 'binary_crossentropy'),
        ('relu', 'sgd', 'binary_crossentropy'),
        ('relu', 'sgd', 'mean_squared_error'),
        ('relu', 'sgd', 'mean_absolute_error')
    ]
    for activation, optimizer, loss in configurations:
        model = build_and_train_model(activation, optimizer, loss, epochs=10, batch_size=10)
        print(f"Config: {activation}, {optimizer}, {loss}")
        print("Evaluation:", model.evaluate(X_test_scaled, y_test, verbose=0))
        print("Weights:", model.get_weights())
    model.predict(X_test_scaled)
    model.evaluate(X_test_scaled, y_test)



    # Ex No 4 - Improve the performance of the neural network with hyper parameter tuning

    import pandas as pd
    import tensorflow as tf
    from tensorflow import keras
    from sklearn.model_selection import train_test_split
    df = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/insurance_data.csv')
    X = df[['age ', 'affordibility']]
    y = df['bought_insurance']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=25)
    X_train_scaled = X_train.copy()
    X_train_scaled['age '] /= 100
    X_test_scaled = X_test.copy()
    X_test_scaled['age '] /= 100
    model = keras.Sequential([
        keras.layers.Dense(16, input_shape=(2,), activation='relu', kernel_initializer='random_normal', bias_initializer='zeros'),
        keras.layers.Dense(8, activation='relu', kernel_initializer='random_normal', bias_initializer='zeros'),
        keras.layers.Dense(1, activation='sigmoid', kernel_initializer='random_normal', bias_initializer='zeros')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train_scaled, y_train, epochs=50)
    model.evaluate(X_test_scaled, y_test)
    predictions = model.predict(X_test_scaled)
    predictions[:5], y_test[:5] 



    # Ex No 5 - Implement a Convolutional Neural Network model for image classification

    import random
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    X_train = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/input.csv').values.reshape(-1, 100, 100, 3) / 255.0
    Y_train = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/labels.csv').values
    X_test = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/input_test.csv').values.reshape(-1, 100, 100, 3) / 255.0
    Y_test = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/labels_test.csv').values
    print(f"Shape of X_train: {X_train.shape}, Y_train: {Y_train.shape}")
    print(f"Shape of X_test: {X_test.shape}, Y_test: {Y_test.shape}")
    plt.imshow(X_train[random.randint(0, len(X_train))])
    plt.show()
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=5, batch_size=64)
    model.evaluate(X_test, Y_test)



    # Ex No 6 - Improve performance of Convolutional Neural Network by tuning hyper parameters

    import random
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
    from tensorflow.keras.optimizers import Adam
    X_train = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/input.csv').values.reshape(-1, 100, 100, 3) / 255.0
    Y_train = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/labels.csv').values
    X_test = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/input_test.csv').values.reshape(-1, 100, 100, 3) / 255.0
    Y_test = pd.read_csv(r'/content/gdrive/My Drive/Deep Learning/labels_test.csv').values
    print(f"Shape of X_train: {X_train.shape}, Y_train: {Y_train.shape}")
    print(f"Shape of X_test: {X_test.shape}, Y_test: {Y_test.shape}")
    plt.imshow(X_train[random.randint(0, len(X_train))])
    plt.show()
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=5, batch_size=64)
    model.evaluate(X_test, Y_test)



    # Ex No 7 - Implement an Auto encoder for dimensionality reduction

    import numpy as np
    import matplotlib.pyplot as plt
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
    (x_train, _), (x_test, _) = mnist.load_data()
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = np.reshape(x_train, (-1, 28, 28, 1))
    x_test = np.reshape(x_test, (-1, 28, 28, 1))
    noise_factor = 0.5
    x_train_noisy = np.clip(x_train + noise_factor * np.random.normal(size=x_train.shape), 0., 1.)
    x_test_noisy = np.clip(x_test + noise_factor * np.random.normal(size=x_test.shape), 0., 1.)
    plt.figure(figsize=(20, 2))
    for i in range(10):
        ax = plt.subplot(1, 10, i+1)
        plt.imshow(x_test_noisy[i].reshape(28, 28), cmap="binary")
    plt.show()
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2), padding='same'),
        Conv2D(8, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2), padding='same'),
        Conv2D(8, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2), padding='same'),
        Conv2D(8, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(8, (3, 3), activation='relu', padding='same'),
        UpSampling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        UpSampling2D((2, 2)),
        Conv2D(1, (3, 3), activation='sigmoid', padding='same')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train_noisy, x_train, epochs=10, batch_size=256, shuffle=True, validation_data=(x_test_noisy, x_test))
    model.evaluate(x_test_noisy, x_test)
    model.save('denoising_autoencoder.model')
    no_noise_img = model.predict(x_test_noisy)
    plt.figure(figsize=(20, 4))
    for i in range(10):
        ax = plt.subplot(2, 10, i + 1)
        plt.imshow(x_test_noisy[i].reshape(28, 28), cmap="binary")
        ax = plt.subplot(2, 10, i + 11)
        plt.imshow(no_noise_img[i].reshape(28, 28), cmap="binary")
    plt.show()



    # cnn object detection

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from PIL import Image
    import os
    from sklearn.model_selection import train_test_split
    from keras.utils import to_categorical
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

    # Set working directory
    os.chdir('E:/Education/Sem VII/DL Lab/archive')

    # Loading images and labels
    data = []
    labels = []
    classes = 43
    cur_path = os.getcwd()

    for i in range(classes):
        path = os.path.join(cur_path, 'train', str(i))
        images = os.listdir(path)
        for a in images:
            try:
                image = Image.open(path + '\\' + a)
                image = image.resize((30, 30))
                image = np.array(image)
                data.append(image)
                labels.append(i)
            except:
                print("Error loading image")

    # Convert lists to numpy arrays
    data = np.array(data)
    labels = np.array(labels)

    # Split data into training and testing sets
    X_t1, X_t2, y_t1, y_t2 = train_test_split(data, labels, test_size=0.2, random_state=42)

    # One-hot encoding
    y_t1 = to_categorical(y_t1, 43)
    y_t2 = to_categorical(y_t2, 43)

    # Build CNN model
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=X_t1.shape[1:]))
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(43, activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    eps = 15
    history = model.fit(X_t1, y_t1, batch_size=32, epochs=eps, validation_data=(X_t2, y_t2))

    # Save the model
    model.save("my_model.h5")

    # Plot accuracy
    plt.figure(0)
    plt.plot(history.history['accuracy'], label='training accuracy')
    plt.plot(history.history['val_accuracy'], label='val accuracy')
    plt.title('Accuracy')
    plt.xlabel('epochs')
    plt.ylabel('accuracy')
    plt.legend()
    plt.show()

    # Plot loss
    plt.figure(1)
    plt.plot(history.history['loss'], label='training loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.title('Loss')
    plt.xlabel('epochs')
    plt.ylabel('loss')
    plt.legend()
    plt.show()

    # Test the model on the test dataset
    y_test = pd.read_csv('Test.csv')
    labels = y_test["ClassId"].values
    imgs = y_test["Path"].values
    data = []
    for img in imgs:
        image = Image.open(img)
        image = image.resize((30, 30))
        data.append(np.array(image))

    X_test = np.array(data)
    Y_pred = np.argmax(model.predict(X_test), axis=-1)

    # Calculate accuracy
    from sklearn.metrics import accuracy_score
    print(accuracy_score(labels, Y_pred))

    # Save the final model
    model.save("traffic_classifier.h5")



    ## LSTM

    import numpy as np
    import pandas as pd
    from keras.models import Sequential
    from keras.layers import Dense, LSTM, Embedding
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.utils import to_categorical
    import emoji

    # Load data
    data = pd.read_csv('emoji_data.csv', header=None)
    X = data[0].values
    Y = data[1].values

    # Emoji dictionary
    emoji_dict = {
        0: ":red_heart:",
        1: ":baseball:",
        2: ":grinning_face_with_big_eyes:",
        3: ":disappointed_face:",
        4: ":fork_and_knife_with_plate:"
    }

    def label_to_emoji(label):
        return emoji.emojize(emoji_dict[label])

    # Load GloVe embeddings
    file = open('glove.6B.100d.txt', 'r', encoding='utf8')
    content = file.readlines()
    file.close()

    # Create embeddings dictionary
    embeddings = {}
    for line in content:
        line = line.split()
        embeddings[line[0]] = np.array(line[1:], dtype=float)

    # Tokenization
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    word2index = tokenizer.word_index
    Xtokens = tokenizer.texts_to_sequences(X)

    # Get maxlen for padding
    def get_maxlen(data):
        maxlen = 0
        for sent in data:
            maxlen = max(maxlen, len(sent))
        return maxlen

    maxlen = get_maxlen(Xtokens)

    # Padding sequences
    Xtrain = pad_sequences(Xtokens, maxlen=maxlen, padding='post', truncating='post')

    # Convert 'Y' and one-hot encoding
    Y = [int("".join(filter(str.isdigit, str(y)))) for y in Y]
    Ytrain = to_categorical(Y)

    # Create embedding matrix
    embed_size = 100
    embedding_matrix = np.zeros((len(word2index) + 1, embed_size))
    default_embedding = np.zeros(embed_size)

    for word, i in word2index.items():
        if word in embeddings:
            embedding_matrix[i] = embeddings[word]
        else:
            embedding_matrix[i] = default_embedding

    # Build model
    model = Sequential([
        Embedding(input_dim=len(word2index) + 1, output_dim=embed_size, input_length=maxlen, weights=[embedding_matrix], trainable=False),
        LSTM(units=16, return_sequences=True),
        LSTM(units=4),
        Dense(5, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train model
    model.fit(Xtrain, Ytrain, epochs=100)

    # Test model
    test = ["I feel good", "I feel very bad", "lets eat dinner"]
    test_seq = tokenizer.texts_to_sequences(test)
    Xtest = pad_sequences(test_seq, maxlen=maxlen, padding='post', truncating='post')

    # Predict
    y_pred = model.predict(Xtest)
    y_pred = np.argmax(y_pred, axis=1)

    # Display results
    for i in range(len(test)):
        print(test[i], label_to_emoji(y_pred[i]))


    ######LSTM USING HYPER PARAMETER


    import numpy as np
    import pandas as pd
    import emoji
    from keras.models import Sequential
    from keras.layers import Dense, LSTM, Embedding
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.utils import to_categorical

    # Load data
    data = pd.read_csv('emoji_data.csv', header=None)
    X = data[0].values
    Y = data[1].values

    # Emoji dictionary
    emoji_dict = {
        0: ":red_heart:",
        1: ":baseball:",
        2: ":grinning_face_with_big_eyes:",
        3: ":disappointed_face:",
        4: ":fork_and_knife_with_plate:"
    }

    def label_to_emoji(label):
        return emoji.emojize(emoji_dict[label])

    # Load GloVe embeddings
    file = open('glove.6B.100d.txt', 'r', encoding='utf8')
    content = file.readlines()
    file.close()

    # Create embeddings dictionary
    embeddings = {}
    for line in content:
        line = line.split()
        embeddings[line[0]] = np.array(line[1:], dtype=float)

    # Tokenization
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    word2index = tokenizer.word_index
    Xtokens = tokenizer.texts_to_sequences(X)

    # Get maxlen for padding
    def get_maxlen(data):
        maxlen = 0
        for sent in data:
            maxlen = max(maxlen, len(sent))
        return maxlen

    maxlen = get_maxlen(Xtokens)

    # Padding sequences
    Xtrain = pad_sequences(Xtokens, maxlen=maxlen, padding='post', truncating='post')

    # Convert 'Y' and one-hot encoding
    Y = [int("".join(filter(str.isdigit, str(y)))) for y in Y]
    Ytrain = to_categorical(Y)

    # Create embedding matrix
    embed_size = 100
    embedding_matrix = np.zeros((len(word2index) + 1, embed_size))
    default_embedding = np.zeros(embed_size)

    for word, i in word2index.items():
        if word in embeddings:
            embedding_matrix[i] = embeddings[word]
        else:
            embedding_matrix[i] = default_embedding

    # Build model
    model = Sequential([
        Embedding(input_dim=len(word2index) + 1, output_dim=embed_size, input_length=maxlen, weights=[embedding_matrix], trainable=False),
        LSTM(units=16, return_sequences=True),
        LSTM(units=4),
        Dense(5, activation='softmax')
    ])

    # Try different optimizers
    optimizers = ['adam', 'adagrad', 'sgd']

    for optimizer in optimizers:
        print(f"Training with optimizer: {optimizer}")
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(Xtrain, Ytrain, epochs=100)

    # Test model
    test = ["I feel good", "I feel very bad", "lets eat dinner"]
    test_seq = tokenizer.texts_to_sequences(test)
    Xtest = pad_sequences(test_seq, maxlen=maxlen, padding='post', truncating='post')

    # Predict
    y_pred = model.predict(Xtest)
    y_pred = np.argmax(y_pred, axis=1)

    # Display results
    for i in range(len(test)):
        print(test[i], label_to_emoji(y_pred[i]))