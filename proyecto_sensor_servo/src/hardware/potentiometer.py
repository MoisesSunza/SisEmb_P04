# src/hardware/potentiometer.py

import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Potentiometer:
    """
    Librería para leer un potenciómetro conectado en un circuito RC (Resistor-Capacitor).
    """

    def __init__(self, pin, max_ohms=10000):
        """
        Inicializa el objeto Potentiometer.
        
        :param pin: Número de pin GPIO (BCM) conectado.
        :param max_ohms: Resistencia nominal máxima del potenciómetro.
        """
        self.pin = pin
        self.min_value = 0
        self.max_value = 0
        self.max_ohms = max_ohms
        GPIO.setmode(GPIO.BCM)

    def read_raw_value(self):
        """
        Mide el tiempo de carga del capacitor (valor crudo).
        
        :return: Valor crudo (conteo) del potenciómetro.
        """
        count = 0
        
        # 1. Descargar capacitor
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        time.sleep(0.005)  
        
        # 2. Medir tiempo de carga
        GPIO.setup(self.pin, GPIO.IN)
        
        while GPIO.input(self.pin) == GPIO.LOW:
            count += 1
            if count > 60000:
                break
                
        return count

    def calibrate(self):
        """
        Realiza la calibración de los valores mínimo y máximo.
        """
        logging.info("Potenciómetro: Realizando calibración. Por favor, gire a min/max.")
        time.sleep(1)
        
        self.min_value = self.read_raw_value()
        self.max_value = self.read_raw_value() + 1
        
        logging.info(f"Potenciómetro: Valores de referencia establecidos: Min={self.min_value}, Max={self.max_value}")

    def get_data(self):
        """
        Lee el potenciómetro y normaliza el valor.
        
        :return: Tupla (valor_crudo, porcentaje, resistencia_aprox_ohms)
        """
        value = self.read_raw_value()
        
        normalized = 0.0
        range_val = self.max_value - self.min_value
        
        if range_val > 0:
            normalized = (value - self.min_value) / range_val * 100.0
            normalized = max(0, min(100, normalized))
        
        resistance_approx = (normalized / 100) * self.max_ohms
        
        return (value, normalized, resistance_approx)