# Documentación Extendida del Sistema Embebido Sensor-Servo

Este documento detalla la arquitectura modular del proyecto de Sistemas Embebidos, cubriendo la API REST (Servidor Flask), el Módulo de Hardware y la Librería Cliente, con el objetivo de lograr una **Documentación Clara y Completa (Criterio 20%)**.

## 1. Módulos de Hardware (src/hardware)

### A. Clase Potentiometer (src/hardware/potentiometer.py)

Esta clase gestiona la lectura del potenciómetro mediante el circuito RC y el método de conteo de tiempo de carga.

| Método | Propósito | Parámetros | Retorno |
| :--- | :--- | :--- | :--- |
| **`__init__(pin, max_ohms)`** | Inicializa la clase. Configura el modo BCM en GPIO y establece el pin. | `pin`: Número de pin GPIO BCM. `max_ohms`: (opc) Resistencia nominal del potenciómetro (ej: 10000). | `None` |
| **`read_raw_value()`** | **Lectura fundamental.** Mide el tiempo de carga del capacitor en ciclos de conteo (valor crudo). | Ninguno. | `int`: El valor crudo de conteo. |
| **`calibrate()`** | Establece los valores de referencia (`min_value`, `max_value`) necesarios para normalizar la lectura a porcentaje. | Ninguno. | `None` |
| **`get_data()`** | **Lectura principal.** Normaliza el valor crudo entre 0.0 y 100.0 (Porcentaje) y calcula la resistencia aproximada. | Ninguno. | `tuple`: `(valor_crudo, porcentaje, resistencia_ohms)` |

***

### B. Clase ServoMotor (src/hardware/servo.py)

Esta clase gestiona el control del servomotor mediante PWM y aplica los mecanismos de seguridad solicitados (Tarea 4).

| Método | Propósito | Parámetros | Retorno |
| :--- | :--- | :--- | :--- |
| **`__init__(pin, freq, min_angle, max_angle)`** | Inicializa la clase. Configura el pin GPIO, el objeto PWM y establece los límites de seguridad. | `pin`: Número de pin GPIO BCM. `freq`: Frecuencia PWM (50 Hz por defecto). `min_angle`: Límite inferior seguro (ej: -60°). `max_angle`: Límite superior seguro (ej: 60°). | `None` |
| **`_angle_to_duty_cycle(angle)`** | **Función interna.** Convierte un ángulo en grados a un ciclo de trabajo (duty cycle) de PWM. Aplica los límites de seguridad (`min_angle/max_angle`). | `angle`: Ángulo deseado en grados. | `float`: Ciclo de trabajo (duty cycle) de PWM. |
| **`set_angle(angle)`** | **Control principal.** Mueve el servomotor al ángulo especificado, registrando la acción (*logging*) antes de moverse. | `angle`: Ángulo de destino en grados. | `None` |
| **`stop()`** | Detiene la señal PWM del servo. (La limpieza final de GPIO es responsabilidad de `main.py`). | Ninguno. | `None` |

---

## 2. Módulo Cliente (src/client)

### Clase SensorAPIClient (src/client/api_client.py)

Esta clase es la responsable de la **Adquisición de Datos** a través de la red y el **Manejo de Errores (Tarea 3)**.

| Método | Propósito | Parámetros | Retorno |
| :--- | :--- | :--- | :--- |
| **`__init__(base_url, max_retries, retry_delay)`** | Inicializa la clase. Configura la URL de destino y los parámetros de reintento. | `base_url`: URL del servidor API (ej: `http://192.168.1.XXX:5000`). `max_retries`: Máximo de intentos para la conexión (def: 5). `retry_delay`: Pausa entre reintentos (def: 2s). | `None` |
| **`get_sensor_data()`** | **Función clave de Consumo.** Realiza la petición GET al endpoint `/api/sensor`. Gestiona `ConnectionError`, `Timeout` y `HTTPError` (4xx/5xx). | Ninguno. | `dict`: Los datos JSON del sensor (en caso de éxito), o `None` (si fallan todos los reintentos). |

**Manejo de Errores (Tarea 3):**
El método `get_sensor_data` implementa la lógica de reintentos:
1.  Si ocurre un **`requests.exceptions.ConnectionError`** (servidor caído o no accesible), reintenta la conexión hasta `max_retries`.
2.  Si ocurre un **`requests.exceptions.HTTPError`** (error 4xx o 5xx), registra el error y **detiene el proceso de reintento**, asumiendo que el error es en el servidor y es persistente.

---

## 3. API Endpoints (src/api)

La API (Servidor Flask) expone los datos del sensor y el estado del servidor.

### A. Endpoint: `GET /api/sensor`

| Propósito | Retorna la lectura más reciente del potenciómetro. |
| :--- | :--- |
| **Uso Principal** | Utilizado por `main_client.py` para obtener el porcentaje de posición para el servomotor. |

**Esquema de Respuesta JSON (200 OK):**
```json
{
  "Valor_crudo": 1500,
  "Porcentaje": 45.5,
  "Resistencia_Ohms": 4550.0,
  "ultima_actualizacion": "2025-11-05T01:30:00.123456"
}