from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, Flatten, Activation
import numpy as np

from .config import SAMPLING_RATE

class Ensamble_CNN(object):
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dropout(0.25, input_shape=(8, SAMPLING_RATE)))
        self.model.add(Conv1D(8, 1, input_shape=(8, SAMPLING_RATE)))
        self.model.add(Activation('relu'))
        self.model.add(Flatten())
        self.model.add(Dense(21))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.25))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

    def fit(self, X, y, *args, **kwargs):
        self.model.fit(X, y, batch_size=16, nb_epoch=10, verbose=1)

    def predict(self, X,):
        return np.round(self.model.predict(X.reshape(1, 8, SAMPLING_RATE)))

    def predict_proba(self, X):
        return self.model.predict_proba(X.reshape(1, 8, SAMPLING_RATE))[0][0]

    def __str__(self):
        return 'Ensamble_CNN'
