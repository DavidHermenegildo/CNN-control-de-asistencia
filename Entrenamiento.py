#------------------------------------------------------------------------------
#                         Librerías para imagenes
#------------------------------------------------------------------------------
from skimage.io import imread_collection , concatenate_images #
import numpy as np
import matplotlib.pyplot as plt
#import copy  as cp
#import copy
import os
#import cv2
import re                                                      # importar imagenes
#import tensorflow as tf
from keras_preprocessing import image                          # Crea Etiquetas
from sklearn.model_selection import train_test_split           # Sets de entrenamiento
from tensorflow.keras.utils import to_categorical              # Encoding
#------------------------------------------------------------------------------
#                         Librerías para el modelo CNN
#------------------------------------------------------------------------------
import keras
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from tensorflow import keras
#from tensorflow.keras import layers

def Entrenamiento():

    #------------------------------------------------------------------------------
    #                         Cargar set de imagenes
    #------------------------------------------------------------------------------
    dirname = os.path.join(os.getcwd(), 'D:/14_CNN_Proyecto/Data')
    imgpath = dirname + os.sep 

    images = []
    directories = []
    dircount = []
    prevRoot=''
    cant=0

    print("leyendo imagenes de ",imgpath)

    for root, dirnames, filenames in os.walk(imgpath):
        for filename in filenames:
            if re.search("\.(jpg|jpeg|png|bmp|tiff)$", filename):
                cant=cant+1
                filepath = os.path.join(root, filename)
                image = plt.imread(filepath)
                images.append(image)
                b = "Leyendo..." + str(cant)
                #print (b, end="\r")
                if prevRoot !=root:
                    #print(root, cant)
                    prevRoot=root
                    directories.append(root)
                    dircount.append(cant)
                    cant=0
    dircount.append(cant)

    dircount = dircount[1:]
    dircount[0]=dircount[0]+1

    #print('Directorios leidos:',len(directories))
    #print("Imagenes en cada directorio", dircount)
    print('suma Total de imagenes en subdirs:',sum(dircount))

    #------------------------------------------------------------------------------
    #                         Creando Etiqetas
    #------------------------------------------------------------------------------
    labels=[]
    indice=0
    for cantidad in dircount:
        for i in range(cantidad):
            labels.append(indice)
        indice=indice+1
    print("Cantidad etiquetas creadas: ",len(labels))

    rostros=[]
    indice=0
    for directorio in directories:
        name = directorio.split(os.sep)
        print(indice , name[len(name)-1])
        rostros.append(name[len(name)-1])
        indice=indice+1

    y = np.array(labels)
    X = np.array(images, dtype=np.uint8) #convierto de lista a numpy

    classes = np.unique(y)
    nClasses = len(classes)
    #print('Total number of outputs : ', nClasses)
    print('Output classes : ', classes)

    #------------------------------------------------------------------------------
    #                         sets de Entrenamiento
    #------------------------------------------------------------------------------

    train_X,test_X,train_Y,test_Y = train_test_split(X,y,test_size=0.2)
    print('datos de entrenamiento : ', train_X.shape, train_Y.shape)
    print('Testing datos : ', test_X.shape, test_Y.shape)

    #------------------------------------------------------------------------------
    #                         Procesamiento de imagenes
    #------------------------------------------------------------------------------
    train_X = train_X.astype('float32')
    test_X = test_X.astype('float32')
    train_X = train_X / 255.
    test_X = test_X / 255.

    #------------------------------------------------------------------------------
    #                         Hacemos el One-hot Encoding para la red
    #------------------------------------------------------------------------------
    train_Y_one_hot = to_categorical(train_Y)
    test_Y_one_hot = to_categorical(test_Y)

    print('Original label:', train_Y[0])
    print('After conversion to one-hot:', train_Y_one_hot[0])

    #------------------------------------------------------------------------------
    #                         Set de Entrenamiento y Validación
    #------------------------------------------------------------------------------

    train_X,valid_X,train_label,valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)
    print(train_X.shape,valid_X.shape,train_label.shape,valid_label.shape)

    #------------------------------------------------------------------------------
    #                         Creamos el modelo de CNN
    #------------------------------------------------------------------------------
  
    INIT_LR = 1e-3 
    epochs = 8 
    batch_size = 64 

    model = Sequential()
    model.add(Conv2D(40, kernel_size=(3, 3),activation='linear',padding='same',input_shape=( 150, 150,3)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D((2, 2),padding='same'))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(40, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.5))
    model.add(Dense(nClasses, activation='softmax'))

    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adagrad(lr=INIT_LR, decay=INIT_LR / 100),metrics=['accuracy'])

    #------------------------------------------------------------------------------
    #                Entrenamos el modelo: Aprende a clasificar imágenes
    #------------------------------------------------------------------------------
    train = model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))
    model.save("D:/14_CNN_Proyecto/CNN/Model2_Biometrico.h5py")

    #Evaluamos la red
    test_eval = model.evaluate(test_X, test_Y_one_hot, verbose=1)

if __name__ == "__main__":
    Entrenamiento()