#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
tf.random.set_seed(0)
data = np.loadtxt('data_tic_tak_toe_v0.csv', delimiter=',')

posisjoner_pa_brett = data[0:1000000, 0:18]
vinner = (data[0:1000000, 18] == 2)*1

print("data loded")
# Define the model
model = Sequential([
    layers.Dense(16, activation='relu', input_shape=(18,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model with the callback
model.fit(posisjoner_pa_brett, vinner, epochs=3, batch_size=32, verbose=1)
model.save('forste_model_tic_tak_toe_p2.h5') 

# Evaluate the model
loss, accuracy = model.evaluate(posisjoner_pa_brett, vinner, verbose=1)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')