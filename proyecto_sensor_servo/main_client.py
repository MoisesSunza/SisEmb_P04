# main_client.py
# Se ejecuta en la Raspberry Pi conectada al SERVOMOTOR.
# Su función es consumir la API del servidor y controlar el actuador.

import logging
import time
import RPi.GPIO as GPIO # Necesario para la limpieza final

# Importar los módulos modulares
from src.client.api_client import SensorAPIClient
from src.hardware.servo import ServoMotor 

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DEL SISTEMA ---
SERVO_PIN = 18                 # Pin GPIO BCM para el servomotor
# IMPORTANTE: DEBES REEMPLAZAR ESTA IP con la IP REAL de tu Raspberry Pi Servidora
API_URL = "http://192.168.1.XXX:5000" 

def servo_control_loop(servo_motor: ServoMotor, api_client: SensorAPIClient):
    """
    Función principal de control. Consume la API y mueve el servo.
    """
    logging.info("Controlador: Bucle de control iniciado. Buscando datos del servidor...")
    while True:
        try:
            # 1. Consumir la API (Tarea 3)
            sensor_data = api_client.get_sensor_data()
            
            if sensor_data and 'Porcentaje' in sensor_data:
                # 2. Obtener el valor normalizado del potenciómetro
                percentage = sensor_data['Porcentaje']
                
                # 3. Mapear el porcentaje (0% a 100%) al ángulo del servo (-90° a 90°)
                angle = (percentage * 180 / 100) - 90 
                
                # 4. Mover el servo (Tarea 4)
                servo_motor.set_angle(angle)
                
                logging.info(f"Controlador: Pot: {percentage:.1f}% -> Moviendo Servo a {angle:.1f}°")
                
            else:
                logging.warning("Controlador: Sin datos de la API. Reintentando...")
            
            time.sleep(0.5) 
            
        except Exception as e:
            logging.error(f"Controlador: Error fatal en el bucle: {e}")
            time.sleep(5)


if __name__ == '__main__':
    try:
        logging.info("--- Pi CLIENTE INICIADA (CONTROLADOR DE ACTUADOR) ---")
        
        # 1. Inicializar Hardware Servomotor (Tarea 1, Tarea 4)
        servo = ServoMotor(SERVO_PIN, min_angle=-60, max_angle=60) 
        
        # 2. Inicializar Cliente API (Tarea 3)
        api_client = SensorAPIClient(API_URL)
        
        # 3. Ejecutar el Bucle de Control en el hilo principal
        servo_control_loop(servo, api_client)
        
    except KeyboardInterrupt:
        logging.info("\nPi Cliente: Programa detenido por el usuario.")
    
    finally:
        # 4. Limpieza final de recursos
        servo.stop() 
        GPIO.cleanup() 
        logging.info("Pi Cliente: Sistema apagado y GPIO limpiado.")