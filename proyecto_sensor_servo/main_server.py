import threading
import logging
import time
import RPi.GPIO as GPIO 

from src.api.sensor_api import run_api_server
from src.hardware.servo import ServoMotor # Se importa para la limpieza de GPIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DEL SISTEMA ---
SERVO_PIN_DUMMY = 18 
POTENTIOMETER_OHMS = 100000 # Definir valor del potenciometro

if __name__ == '__main__':
    try:
        logging.info("--- Pi SERVER INICIADA (PUBLICADOR DE DATOS) ---")
        logging.info(f"--- RESISTENCIA DEL POTENCIÓMETRO CONFIGURADA EN: {POTENTIOMETER_OHMS} Ohms ---")
        
        dummy_servo = ServoMotor(SERVO_PIN_DUMMY, min_angle=0, max_angle=0)
        
        # 2. Iniciar el Servidor API, pasándole el valor de la resistencia
        run_api_server(POTENTIOMETER_OHMS)
        
    except KeyboardInterrupt:
        logging.info("\nPi Server: Programa detenido por el usuario.")
    
    finally:
        # 3. Limpieza final de recursos
        GPIO.cleanup() 

        logging.info("Pi Server: Sistema apagado y GPIO limpiado.")
