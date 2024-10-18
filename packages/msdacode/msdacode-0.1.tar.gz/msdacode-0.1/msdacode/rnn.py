def rnn():
    code = '''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb

# Load the IMDB dataset
max_words = 5000  # Only consider the top 5,000 words
max_len = 200  # Only consider the first 200 words of each review

# Load data
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

# Pad sequences to ensure uniform input size
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# Build the RNN model
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=128, input_length=max_len))  # Embedding Layer
model.add(SimpleRNN(128, return_sequences=False))  # Simple RNN Layer
model.add(Dropout(0.2))  # Regularization
model.add(Dense(1, activation='sigmoid'))  # Output Layer

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)
print('Test Accuracy:', accuracy)

    '''
    print(code)



def lstm():
    code = '''
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words = 5000)
x_train = sequence.pad_sequences(x_train, maxlen=80)
x_test = sequence.pad_sequences(x_test, maxlen=80)

model = Sequential()
model.add(Embedding(5000, 128))
model.add(LSTM(128,activation="tanh",recurrent_activation="sigmoid"))
model.add(Dense(1, activation = 'sigmoid'))


model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
lstm=model.fit(x_train, y_train, batch_size =32, epochs = 3, validation_data = (x_test, y_test),shuffle=True,verbose=1)
model.summary()

op=model.predict(x_test)
op

## For Prediction
from random import randint
arr_ind=randint(0,24999)
index=imdb.get_word_index()
reverse_index = dict([(value, key) for (key, value) in index.items()])
decoded = " ".join([reverse_index.get(i - 3, "#") for i in x_test[arr_ind]])
arr=[]

for i in op:
  if(i<0.5):
    arr.append("Negative")
  else:
    arr.append("Positive")

print("Sentence:",decoded)
print("Review:",arr[arr_ind])
print("Predicted Value:",op[arr_ind][0])
print("Expected Value:",y_test[arr_ind])
    '''
    print(code)