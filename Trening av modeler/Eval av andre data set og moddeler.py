import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

tf.random.set_seed(0)
data_1 = np.loadtxt(r'Data set\data_tic_tak_toe_v1_eval.csv', delimiter=',')

model_1 = load_model(r'Modeler\andre_model_tic_tak_toe_p2.h5')
model_2 = load_model(r'Modeler\andre_model_tic_tak_toe_p2_v2.h5')
posisjoner_pa_brett = data_1[:, 0:18]
vinner = (data_1[:, 18] == 2)*1

loss, accuracy = model_1.evaluate(posisjoner_pa_brett, vinner, verbose=1)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')
loss, accuracy = model_2.evaluate(posisjoner_pa_brett, vinner, verbose=1)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')