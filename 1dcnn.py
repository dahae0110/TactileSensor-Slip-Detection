# -*- coding: utf-8 -*-
"""1DCNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JgWxhyRg6OoZJUYTtPtD2_o0XuJmCRPK
"""

from google.colab import drive
drive.mount('/content/drive')

!gdown --id 1Lx4s240DQDVIF2Zz7P4_DpuBKu8ELUrY

!ls /content/TestData.zip -al

import zipfile
from google.colab import drive

drive.mount('/content/drive')

!unzip "/content/TestData.zip" -d "/content/TestData"

# coding:utf-8
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import re
import os
from PIL import Image
import glob
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, LSTM
from tensorflow.keras.preprocessing.image import ImageDataGenerator

csvdata_dir = "/content/TestData/"

# raw data from the sensor
folder = ["DiffForceLeft", "GrippingLeft",  "GrippingOnly", "GrippingWithDiffForce"]

max_dataarraysize = 19170

#max_dataarraysize = 2397

#df maximum value
#last_line = len(folder[0].iloc[:,-1:])

data_collect = []
label = []

n = 0
k = 10

for index, name in enumerate(folder):
    name = name + "/csvs"
    #print(name)
    dir = csvdata_dir + name
    files = glob.glob(dir + "/*.csv")

    for i, file in enumerate(files):
        csv = pd.read_csv(file, sep = ',', encoding = "UTF-8", error_bad_lines = False, header = None)
        data = np.array(csv, dtype = np.float32)
        if csv.empty:
            print('DataFrame is empty!')        # (198959, 3)
        print(data.shape)

        # (19896, 3)
        for i in range(int(max_dataarraysize)):
          
          preStack = np.hstack((data[n:k, 0], data[n:k, 1]))
          data_stack= np.hstack((preStack, data[n:k, 2]))
          
          #print(data_stack.shape)
          #data = data[n:k, :]  
          '''
          For data_collect shape to be (27600,30)
          preStack = np.hstack((data[n:k, 0], data[n:k, 1]))
          data_stack= np.hstack((preStack, data[n:k, 2]))
          '''
          '''
          For data_collect shape to be (14000, 3, 10)
          preStack = np.vstack((data[n:k, 0], data[n:k, 1]))
          data_stack= np.vstack((preStack, data[n:k, 2]))
          '''
          data_collect.append(data_stack)
          #print(data_collect)
          label.append([index])
          '''
          for w in data_stack:
            
            data_collect.append(data_stack)
            label.append([index])

            #print(data_collect)
            #print(label)
          '''
          n = n+10
          k = k+10
          #print(n,k)

        n = 0
        k = 10

        #data_collect.append(data_collect)

#data_collect = np.asarray(data_stack)

data_collect = np.asarray(data_collect)
label = np.asarray(label)
label =  tf.keras.utils.to_categorical(label, 4)

print(data_collect.shape)
print(label.shape)
# (14000, 30)

X_train, X_test, y_train, y_test = train_test_split(data_collect, label, test_size=0.3, random_state=111)

# (828, 2300, 3)
print(data_collect.shape)
# (2300, 3)
print(data_collect[1])
print(data_collect[2])
print(data_collect[3])

print(type(data_collect))

print(type(X_test), type(X_train), type(y_train), type(y_test))

print((X_test.shape))

print((y_test.shape))

X_test = np.array([np.array(val) for val in X_test])
X_train = np.array([np.array(val) for val in X_train])
y_test = np.array([np.array(val) for val in y_test])
y_train = np.array([np.array(val) for val in y_train])

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.layers import Dense, Conv1D, MaxPool1D, BatchNormalization, Flatten
from tensorflow.keras.models import Sequential

#best for (30,1)

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(30,1)))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))

model.add(Dropout(0.5))
model.add(MaxPool1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(4, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

'''
#best for (240,1)
model = Sequential()
model.add(Conv1D(32, 7, strides= 3,activation='relu', input_shape = (240, 1)))
model.add(MaxPool1D(3))
model.add(Conv1D(32, 5, strides= 3,activation='relu'))
model.add(MaxPool1D(1))
model.add(Conv1D(32, 5, strides= 3,activation='relu'))
model.add(Flatten())
model.add(BatchNormalization())
model.add(Dense(4, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()
'''

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Fit the model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
epochs=10)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

y_pred=model.predict(X_test) 
y_pred=np.argmax(y_pred, axis=1)
y_test=np.argmax(y_test, axis=1)
cm = confusion_matrix(y_test, y_pred)
print(cm)

#cm = confusion_matrix(y_test, y_pred)
labels = ["DiffForceLeft", "GrippingLeft", "GrippingOnly","GrippingWIthDiffForce"]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

disp.plot(cmap=plt.cm.Blues)
plt.show()
