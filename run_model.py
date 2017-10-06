import os
from random import randint

import numpy as np
from keras.callbacks import Callback
from keras.layers import Dense
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.optimizers import Adam

from next_batch import LSTM_WINDOW_SIZE, INPUT_SIZE
from next_batch import get_trainable_data

DATA_FILE = 'data.npz'
if not os.path.exists(DATA_FILE):
    (x_train, y_train), (x_test, y_test) = get_trainable_data()
    np.savez_compressed('data.npz', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)
else:
    d = np.load(DATA_FILE)
    x_train = d['x_train']
    y_train = d['y_train']
    x_test = d['x_test']
    y_test = d['y_test']

print('x_train.shape =', x_train.shape)
print('y_train.shape =', y_train.shape)

print('x_test.shape =', x_test.shape)
print('y_test.shape =', y_test.shape)


def print_np_arr(x):
    return np.array_repr(x).replace('\n', '')


class Monitor(Callback):
    def on_epoch_end(self, epoch, logs=None):

        print(logs)

        np.set_printoptions(precision=6, suppress=True)
        num_values_to_predict = 10
        r_idx = randint(a=0, b=len(x_test) - num_values_to_predict)
        print('\n\n')
        print('pred  =', print_np_arr(self.model.predict(x_test[r_idx:r_idx + num_values_to_predict]).flatten()))
        print('truth =', print_np_arr(y_test[r_idx:r_idx + num_values_to_predict].flatten()))
        print('\n')


m = Sequential()
m.add(LSTM(32, input_shape=(LSTM_WINDOW_SIZE, INPUT_SIZE)))
# m.add(Dense(32, activation='relu'))
m.add(Dense(1, activation='relu'))

adam = Adam(lr=0.001 * 0.1)  # 0.1x the usual LR.
m.compile(optimizer=adam, loss='mape')

monitor = Monitor()

m.fit(x_train, y_train,
      validation_data=(x_test, y_test),
      shuffle=True,
      batch_size=32,
      epochs=10000,
      verbose=0)
