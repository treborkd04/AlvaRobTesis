
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 23:41:35 2025

@author: Robert Alvarez
"""

import serial
import time
import schedule
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging

# Configuración del puerto serie para la ESP32
esp32 = serial.Serial('/dev/ttyUSB0', 115200)

# Variables para almacenar los valores de los sensores
temperatura_valores = []
humedad_valores = []
temperatura_valoresBMP = []
presion_valoresBMP = []
rainValues = []

# URL de Firebase
firebase_url = 'https://minstationmeteo-default-rtdb.firebaseio.com/datos.json'

cred = credentials.Certificate("minstationmeteo-firebase-adminsdk-93gzs-fd2a7ac1fa.json")
firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})

# Obtiene una referencia a la base de datos
ref = db.reference('/datos')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("El programa ha arrancado correctamente")

def enviar_datos1():
    global temperatura, humedad, rainSensor, presionBMP, fechaTiempoReal

    logger.info("Subiendo datos a Firebase")

    data_datasheet1 = {
        'timestamp': fechaTiempoReal,
        'Temperatura C': temperatura,
        'Humedad (0-100)% RH': humedad,
        'Presion Atmosferica Pa': presionBMP,
        'Rain': rainSensor
    }

    try:
        ref.update(data_datasheet1)
        logger.info(f"Actualización exitosa en Firebase: {data_datasheet1}")
    except Exception as e:
        logger.error(f"Error al actualizar datos en Firebase: {e}")

def grabar_datosFIREBASE():
    global temperatura, humedad, fechaTiempoReal, presionBMP, rainSensor
    try:
        line = esp32.readline().decode('utf-8')
        if line:
            fechaTiempoReal = time.time()
            valores = line.split(',')
            if len(valores) > 1:
                valores = [float(dato) for dato in valores]
                temperatura = float(valores[1])
                humedad = float(valores[0])
                presionBMP = float(valores[2])
                rainSensor = int(valores[3])
                logger.info(f"Datos del serial recogidos exitosamente: {temperatura}, {humedad}, {presionBMP}, {rainSensor}")
                time.sleep(0.5)
                enviar_datos1()
            else:
                logger.warning("Error al enviar datos serial")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Error en grabar_datosFIREBASE: {e}")

schedule.every(1).seconds.do(grabar_datosFIREBASE)

try:
    while True:
        schedule.run_pending()
        time.sleep(0.5)
except Exception as e:
    logger.error(f"Error en el bucle principal: {e}")
finally:
    esp32.close()

