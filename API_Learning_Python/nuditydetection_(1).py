# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf



path='../input/my-nsfw-dataset/train/train/'

Nude=os.listdir(path+'NSFW/')
Decent=os.listdir(path+'SFW/')
test_path='../input/my-nsfw-dataset/test/test/'
test=os.listdir(test_path)


vgg16 = tf.keras.applications.VGG16(include_top=False)
preprocess_input = tf.keras.applications.vgg16.preprocess_input
image = tf.keras.preprocessing.image

batch_size=20


def extract_features(img_paths, batch_size=batch_size):

    global vgg16
    n = len(img_paths)
    img_array = np.zeros((n, 299, 299, 3))

    for i, path in enumerate(img_paths):
        img = image.load_img(path, target_size=(299, 299))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        x = preprocess_input(img)
        img_array[i] = x

    X = vgg16.predict(img_array, batch_size=batch_size, verbose=1)
    X = X.reshape(n, 512, -1)
    return X

X = extract_features(
    list(map(lambda x: path + 'NSFW/' + x, Nude)) + list(map(lambda x: path + 'SFW/' + x, Decent))
)
y = np.array([1] * len(Nude) + [0] * len(Decent))

X_test = extract_features(
    list(map(lambda x: test_path + x, test))
)
y_test = np.array([1] * len(Nude) + [0] * len(Decent))



def train():
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(1724, activation=tf.nn.relu),


      tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)

    ])
    return model

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state=42)

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Dense
np.random.seed(42)

epochs = 10

model = train()
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
                    validation_data=(X_test,y_test),
                    batch_size=batch_size,
                    epochs=epochs)



plt.plot(range(1,epochs+1), history.history['accuracy'], label='train')
plt.plot(range(1,epochs+1), history.history['val_accuracy'], label='test')
plt.legend()

plt.plot(range(1,epochs+1), history.history['loss'], label='train loss')
plt.plot(range(1,epochs+1), history.history['val_loss'], label='test loss')
plt.legend()


import cv2


X_test = extract_features(
    list(map(lambda x: '../input/my-nsfw-dataset/test/test/NSFW (2).jpg' , test))
)

y_pred = model.predict(X_test)
if(y_pred>0.5).all():
    print("This image is not safe to use and it depicts Nudity")
elif(y_pred<0.5).all():
    print("Safe to use")
else:
    print("Invalid Image")


plt.imshow(cv2.imread('../input/safeee/s1.jpg'))

plt.imshow(cv2.imread('../input/safeee/s2.jpg'))

X_test = extract_features(
    list(map(lambda x: '../input/safeee/s1.jpg' , test))
)

y_pred = model.predict(X_test)
if(y_pred>0.5).all():
    print("This image is not safe to use and it depicts Nudity")
elif(y_pred<0.5).all():
    print("Safe to use")
else:
    print("Invalid Image")

X_test = extract_features(
    list(map(lambda x: '../input/safeee/s2.jpg' , test))
)

y_pred = model.predict(X_test)
if(y_pred>0.5).all():
    print("This image is not safe to use and it depicts Nudity")
elif(y_pred<0.5).all():
    print("Safe to use")
else:
    print("Invalid Image")
