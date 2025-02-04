# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:46:01 2024

@author: Robert Alvarez
"""
#Plantilla de clasificación.

#Importamos las librerías necesarias
import sqlite3
import pandas as pd
import numpy as n
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Conectar a la base de datos
conn = sqlite3.connect('exported_data.db')
cursor = conn.cursor()

query = "SELECT * FROM exported_table"
dataset = pd.read_sql_query(query, conn)


X = dataset.iloc[:, 1:3].values
y = dataset.iloc[:, -1].values

# Training the Linear Regression model on the whole dataset
#from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size = 0.25)

#Escalado de Variables

#from sklearn.preprocessing import StandardScaler
#Se usa igual que el LabelEncoder
# Se usa para hacer un fit_trasnform y luego para hacer el cambio propiamente.
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train) #De esta forma se escala automáticamente
X_test = sc_X.transform(X_test)

#Ajustar el clasificador en el Conjunto de entrenamiento
#Crear el modelo de clasificación Aquí
#from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 45, metric ="minkowski", p = 1)
classifier.fit(X_train, y_train)

#Predicción de los resultados con el conjunto de testing
y_pred = classifier.predict(X_test)

#Elaborar una matriz de confusión.
#from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
#accuracy = accuracy_score(y_test, y_pred)
#Los parámetros que consta es que debemos enviarle los valor de y verdaderos
# Y os valores de la predicción

#Metricas para saber el reporte de presición, exhaustividad y exactitud
from sklearn.metrics import classification_report

# Supongamos que y_test son las etiquetas reales y y_pred son las etiquetas predichas
print(classification_report(y_test, y_pred, target_names=['0', '1', '2', '3']))

