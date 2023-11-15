import numpy as np
from tensorflow import keras
from Data_PreProcess import Data_PreProcess
import nltk
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
stemmer = LancasterStemmer()

_, _, _, training, output = Data_PreProcess()

training = np.array(training)
output = np.array(output)

model = keras.Sequential([
    keras.layers.Input(shape=(len(training[0]),)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(training, output, epochs=1500, batch_size=16, verbose=1)

model.save("Chat_Bot.h5")