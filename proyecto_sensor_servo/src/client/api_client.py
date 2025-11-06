# src/client/api_client.py

import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SensorAPIClient:
    """
    Librería cliente para consumir datos de la API (Consumo de API - Tarea 3).
    Implementa manejo de errores y reintentos para conexiones fallidas (Tarea 3).
    """

    def __init__(self, base_url, max_retries=5, retry_delay=2):
        """
        :param base_url: La URL base de la API.
        :param max_retries: Número máximo de veces a reintentar la conexión.
        :param retry_delay: Tiempo de espera entre reintentos (segundos).
        """
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def get_sensor_data(self):
        """
        Obtiene los datos del sensor desde el endpoint /api/sensor.
        """
        endpoint = f"{self.base_url}/api/sensor"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(endpoint, timeout=5) 
                response.raise_for_status() 
                
                return response.json()
                
            except requests.exceptions.ConnectionError:
                logging.warning(f"Cliente API: Error de Conexión. Reintentando... (Intento {attempt + 1}/{self.max_retries})")
                
            except requests.exceptions.Timeout:
                logging.warning(f"Cliente API: Error de Timeout. Reintentando... (Intento {attempt + 1}/{self.max_retries})")
            
            except requests.exceptions.HTTPError as e:
                logging.error(f"Cliente API: Error HTTP {response.status_code}: {e}")
                break 
                
            except requests.exceptions.RequestException as e:
                logging.error(f"Cliente API: Error general: {e}")
                break 
                
            time.sleep(self.retry_delay)

        logging.error(f"Cliente API: Fallo al conectar después de {self.max_retries} intentos. (Manejo de Errores - Tarea 3)")
        return None