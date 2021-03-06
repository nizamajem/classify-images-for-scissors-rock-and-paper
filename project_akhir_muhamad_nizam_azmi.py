# -*- coding: utf-8 -*-
"""Project Akhir_Muhamad Nizam Azmi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1avRv1Fva-A1QQgH3nDVNH5Og8GoscUlC
"""

!wget https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \
-O /tmp/rockpaperscissors.zip

!pip install split-folders

# melakukan extrasi pada file zip 
import splitfolders
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import zipfile,os
local_zip ='/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

os.listdir('/tmp/rockpaperscissors/rps-cv-images')

# menghapus folder rps-cv-images secara recursive
os.remove('/tmp/rockpaperscissors/rps-cv-images/README_rpc-cv-images.txt')

os.listdir('/tmp/rockpaperscissors/rps-cv-images')

train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'nearest',
                    validation_split=0.4)

train_dataset = train_datagen.flow_from_directory(batch_size=32,
                                                 directory='/tmp/rockpaperscissors/rps-cv-images',
                                                 shuffle=True,
                                                 target_size=(150, 150), 
                                                 subset="training",
                                                 class_mode='categorical')

validation_dataset = train_datagen.flow_from_directory(batch_size=32,
                                                 directory='/tmp/rockpaperscissors/rps-cv-images',
                                                 shuffle=True,
                                                 target_size=(150, 150), 
                                                 subset="validation",
                                                 class_mode='categorical')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(256, (3, 3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation = 'relu'),
    tf.keras.layers.Dense(3, activation = 'softmax')
])

# compile model dengan 'adam' optimizer loss function 'binary_crossentropy' 
model.compile(loss='binary_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

# melakukan model fit dengen 5 validation step dan mendeteksi 25 batch per epoch
model.fit(
    train_dataset,
    steps_per_epoch=25,
    epochs=5,
    validation_data=validation_dataset,
    validation_steps=5,
    verbose=2)

model.evaluate(train_dataset)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)

  print(fn)
  print(classes)


  scissors = "[1. 0. 0.]"
  rock = "[0. 1. 0.]"
  paper = "[0. 0. 1.]"
  
  if str(classes[0]) == paper:
   print('this is Paper')
  elif str(classes[0]) == rock:
   print('this is Rock')
  else:
   print('this is Scissors')

