# main_server.py
# Se ejecuta en la Raspberry Pi conectada al POTENCIÓMETRO.
# Su función es leer el sensor y publicarlo en la red (Servidor Flask).

import threading
import logging
import time
import RPi.GPIO as GPIO # Necesario para la limpieza final

# Importar el módulo del Servidor y el Potenciómetro
from src.api.sensor_api import run_api_server
from src.hardware.servo import ServoMotor # Importado solo para cleanup

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DEL SISTEMA ---
# El pin del servo se define aquí solo para inicializarlo, pero NO se usa.
# Esto asegura que la clase ServoMotor pueda ser importada si es necesario.
SERVO_PIN_DUMMY = 18 

if __name__ == '__main__':
    try:
        logging.info("--- Pi SERVER INICIADA (PUBLICADOR DE DATOS) ---")
        
        # 1. Crear una instancia del ServoMotor para tener el objeto si es necesario.
        # En esta Pi, el servo NO se usa, pero es bueno tener la instancia para el cleanup.
        # Usamos límites muy ajustados para el dummy servo.
        dummy_servo = ServoMotor(SERVO_PIN_DUMMY, min_angle=0, max_angle=0)
        
        # 2. Iniciar el Servidor API. 
        # run_api_server() lanza el hilo de lectura del potenciómetro y luego inicia Flask.
        run_api_server()
        
    except KeyboardInterrupt:
        logging.info("\nPi Server: Programa detenido por el usuario.")
    
    finally:
        # 3. Limpieza final de recursos
        # Asegurarse de que GPIO se limpie correctamente.
        GPIO.cleanup() 
        logging.info("Pi Server: Sistema apagado y GPIO limpiado.")