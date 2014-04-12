__author__ = 'Akmal'

import numpy as np
import pandas as pd
from random import shuffle
from math import sqrt, exp
from matplotlib import pylab, pyplot
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold, StratifiedKFold, ShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors, DistanceMetric
from sklearn.grid_search import GridSearchCV
from PIL import Image, ImageFilter
from sklearn.neighbors.base import _get_weights

def create_rotated_images(x_train, y_train, angles):
    '''
    Поворот цифр выборки на +-angle
    '''
    for i in range(0, x_train.shape[0]):
        for angle in angles:
            image = Image.fromarray(np.uint8(x_train[i]).reshape(28, 28))
            image1 = image.rotate(angle)
            rotated_image = np.asarray(image1).reshape(28 * 28)
            x_train = np.r_[x_train, np.array([rotated_image])]
            y_train = np.r_[y_train, y_train[i]]
            image2 = image.rotate(-angle)
            rotated_image = np.asarray(image2).reshape(28 * 28)
            x_train = np.r_[x_train, np.array([rotated_image])]
            y_train = np.r_[y_train, y_train[i]]
    return x_train, y_train

def create_smooth_images(x_train):
    '''
    Наложение на выборку SMOOTH фильтра
    '''
    for i in range(0, x_train.shape[0]):
        image = Image.fromarray(np.uint8(x_train[i]).reshape(28, 28))
        image = image.filter(ImageFilter.SMOOTH)
        smooth_image = np.asarray(image).reshape(28 * 28)
        x_train[i] = smooth_image
    return x_train

def cosin_metric(a, b):
    '''
    Косинусная метрика
    '''
    return 1 - abs(np.dot(a, b))/sqrt(np.dot(a, a) * np.dot(b, b))

def calc_weights(distances):
    '''
    Функция веса
    '''
    weights = distances
    for i in range (0, len(distances)):
        weights[i] = 1.0 / (distances[i]**2 + 0.00001)
    return weights

def make_submission(prediction, filename_or_buffer, id_col='Id',
                    prediction_col='Solution'):
    '''
    Результат работы алгоритма в формате .csv
    '''
    df = pd.DataFrame({id_col : range(1, len(prediction) + 1),
                       prediction_col : prediction})
    df.to_csv(filename_or_buffer, cols=[id_col, prediction_col], index=False)

#Считывание данных
train = pd.read_csv('kaggle\digits\mnist_small_train.csv')
data = pd.read_csv('kaggle\digits\mnist_test_no_label.csv')
x_data = np.asarray(data)

#Создание np-arrays с выборкой
indices = range(train.shape[0])
shuffle(indices)
x_full_train = np.asarray(train[range(1, train.shape[1])])
y_full_train = np.asarray(train[[0]]).ravel()

#Создание классификатора с наилучшими параметрами
estimator = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=6,
                                 metric=cosin_metric, weights=calc_weights)

#Обработка обучающей выборки
x_full_train = create_smooth_images(x_full_train)
angles = [12]
x_new_train, y_new_train = create_rotated_images(x_full_train,
                                                 y_full_train, angles)

#Обучение классификатора и предсказание тестовой выборки
estimator = estimator.fit(x_new_train, y_new_train)
prediction = estimator.predict(x_data)

#Сохранение результата
submission = list(prediction)
make_submission(submission, 'finalVersion.csv',
                id_col='Id', prediction_col='Prediction')