# src/api/sensor_api.py

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
potentiometer = Potentiometer(POT_PIN)

datos_sensor = {
    "Valor_crudo": 0,
    "Porcentaje": 0.0,
    "Resistencia_Ohms": 0.0,
    "ultima_actualizacion": None
}
datos_sensor_lock = threading.Lock()

# --- ENDPOINTS DE LA API ---

@app.route('/')
def home():
    """Punto de entrada de la API."""
    return jsonify({
        "mensaje": "API del Sensor de Potenciómetro", 
        "endpoints": ["/api/sensor", "/api/estado"]
    })

@app.route('/api/sensor')
def get_sensor_data():
    """Endpoint para obtener los datos más recientes del potenciómetro."""
    with datos_sensor_lock:
        return jsonify(datos_sensor.copy())

@app.route('/api/estado')
def get_status():
    """Endpoint para verificar el estado del servidor."""
    return jsonify({"estado": "sistema funcionando", "timestamp": datetime.now().isoformat()})

# --- HILO DE LECTURA DEL SENSOR (LOOP) ---

def sensor_loop():
    """
    Función que se ejecuta en un hilo separado para leer y actualizar los datos del sensor.
    """
    # La calibración se realiza una vez al inicio del hilo
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

# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---

def run_api_server():
    """
    Inicia el hilo del sensor y el servidor Flask.
    """
    logging.info("API: Iniciando hilo de actualización del sensor...")
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()

    logging.info("API: Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)