# src/api/sensor_api.py (Actualizado para aceptar RESISTANCE_OHMS)

from flask import Flask, jsonify
from datetime import datetime
import threading
import time
import logging
from src.hardware.potentiometer import Potentiometer 
import RPi.GPIO as GPIO 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN Y VARIABLES GLOBALES ---
app = Flask(__name__)
POT_PIN = 4 
SENSOR_DELAY = 0.3 

# Variables globales que serán inicializadas en run_api_server
potentiometer = None 
datos_sensor = {
    "Valor_crudo": 0,
    "Porcentaje": 0.0,
    "Resistencia_Ohms": 0.0,
    "ultima_actualizacion": None
}
datos_sensor_lock = threading.Lock()

# ... [Endpoints get_sensor_data y get_status NO CAMBIAN] ...
@app.route('/api/sensor')
def get_sensor_data():
    with datos_sensor_lock:
        return jsonify(datos_sensor.copy())
# ...

def sensor_loop():
    """
    Función que se ejecuta en un hilo separado para leer y actualizar los datos del sensor.
    """
    global potentiometer # Necesitamos acceder a la instancia global
    
    if potentiometer is None:
        logging.error("ERROR: Potenciómetro no inicializado. Deteniendo loop.")
        return

    potentiometer.calibrate()
    
    while True:
        try:
            value, normalized, resistance_approx = potentiometer.get_data()
            
            with datos_sensor_lock:
                datos_sensor["Valor_crudo"] = value
                datos_sensor["Porcentaje"] = normalized
                datos_sensor["Resistencia_Ohms"] = resistance_approx
                datos_sensor["ultima_actualizacion"] = datetime.now().isoformat()
                
            time.sleep(SENSOR_DELAY)
            
        except Exception as e:
            logging.error(f"Error en el hilo del sensor: {e}")
            time.sleep(5) 

# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN (MODIFICADA) ---

def run_api_server(resistance_ohms):
    """
    Inicia el hilo del sensor y el servidor Flask, usando la resistencia especificada.
    
    :param resistance_ohms: Resistencia máxima del potenciómetro (ej: 10000).
    """
    global potentiometer
    
    # 1. Inicializar el potenciómetro con el valor de Ohms pasado
    potentiometer = Potentiometer(POT_PIN, resistance_ohms)

    logging.info("API: Iniciando hilo de actualización del sensor...")
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()

    logging.info("API: Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)