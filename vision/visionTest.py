from importPip import visionImport

visionImport()

import time
import psutil

import os
import pickle

from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

chemin_base = "vision/"
os.chdir(chemin_base)

# prepare data
input_dir = 'clf-data'
categories = ['empty', 'not_empty']

c = 0

data = []
labels = []
for category_idx, category in enumerate(categories):
    for file in os.listdir(os.path.join(input_dir, category)):
        img_path = os.path.join(input_dir, category, file)
        img = imread(img_path)
        img = resize(img, (15, 15))
        data.append(img.flatten())
        labels.append(category_idx)
        c += 1
        # #print(c)
        

data = np.asarray(data)
labels = np.asarray(labels)

# #print("\n1")

# train / test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# #print("2")

# train classifier
classifier = SVC()

# #print("3")

parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

# #print("4")

grid_search = GridSearchCV(classifier, parameters)

# #print("5")

# Mesurer le temps d'exécution
# start_time = time.time()

grid_search.fit(x_train, y_train)

# end_time = time.time()

# cpu_percent = psutil.cpu_percent(interval=1)  # Mesure pendant 1 seconde
# memory_usage = psutil.virtual_memory().percent
# temperatures = psutil.sensors_temperatures()

# #print("6")

# test performance
best_estimator = grid_search.best_estimator_

# #print("7")

y_prediction = best_estimator.predict(x_test)

# #print("8")

score = accuracy_score(y_prediction, y_test)

#print('{}% of samples were correctly classified'.format(str(score * 100)))

pickle.dump(best_estimator, open(chemin_base+'model.p', 'wb'))

# execution_time = end_time - start_time

#print(f"Temps d'exécution : {execution_time} secondes")

# Parcourir chaque capteur de température
# for sensor_name, entries in temperatures.items():
    #print("Capteur:", sensor_name)
    # for entry in entries:
        #print("Température actuelle:", entry.current)

# Mesurer l'utilisation CPU
#print(f"Utilisation CPU : {cpu_percent} %")
#print(f"Mémoire utilisée : {memory_usage} %")
