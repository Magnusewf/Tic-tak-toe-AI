#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
tf.random.set_seed(0)
data_1 = np.loadtxt('Data set\\data_tic_tak_toe_v1.csv', delimiter=',')
data_2 = np.loadtxt('Data set\\data_tic_tak_toe_v1_2.csv', delimiter=',')
model = load_model(r'Modeler\forste_model_tic_tak_toe_p2.h5')
data = np.concatenate((data_1, data_2), axis=0)
posisjoner_pa_brett = data[:, 0:18]
vinner = (data[:, 18] == 2)*1

print("data loded")

model = Sequential([
    layers.Dense(16, activation='relu', input_shape=(18,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(posisjoner_pa_brett, vinner, epochs=10, batch_size=32, verbose=1)
model.save('Modeler\\andre_model_tic_tak_toe_p2_v2.h5') 

