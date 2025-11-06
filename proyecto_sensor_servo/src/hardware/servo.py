# src/hardware/servo.py

import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ServoMotor:
    """
    Librería para controlar un servomotor utilizando la librería RPi.GPIO (BCM).
    Encapsula la configuración de GPIO y la lógica de PWM.
    """

    def __init__(self, pin, frequency=50, min_angle=-90, max_angle=90):
        """
        Inicializa el servomotor.
        
        :param pin: Número de pin GPIO (BCM) conectado al cable de señal del servo.
        :param frequency: Frecuencia del PWM (típicamente 50 Hz).
        :param min_angle: Ángulo mínimo de seguridad (grados).
        :param max_angle: Ángulo máximo de seguridad (grados).
        """
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        # Configuración de GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Inicializar PWM
        self.pwm = GPIO.PWM(self.pin, frequency)
        self.pwm.start(0)
        logging.info(f"Servo en pin {self.pin} inicializado.")

    def _angle_to_duty_cycle(self, angle):
        """
        Convierte un ángulo en grados a un ciclo de trabajo (duty cycle) de PWM.
        """
        # Aplicar límites de movimiento de seguridad (Tarea 4)
        safe_angle = max(self.min_angle, min(self.max_angle, angle))
        
        # Fórmula de conversión (asumiendo 180 grados de movimiento total)
        duty = 2.5 + (safe_angle + 90) / 180 * 10
        
        return duty

    def set_angle(self, angle):
        """
        Mueve el servomotor al ángulo especificado.
        
        :param angle: El ángulo deseado en grados (será limitado por min/max_angle).
        """
        duty = self._angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        
        # Agregar logging del movimiento del servo (Tarea 4)
        logging.debug(f"Servo movido a {angle}°. Duty: {duty:.2f}%")
        
        # Pequeña pausa para que el servo se mueva.
        time.sleep(0.05) 
        
        # Dejar de enviar pulsos (duty cycle 0)
        self.pwm.ChangeDutyCycle(0)

    def stop(self):
        """Detiene el PWM y limpia el GPIO."""
        self.pwm.stop()
        # Nota: La limpieza final de GPIO debe hacerse solo una vez en main.py.