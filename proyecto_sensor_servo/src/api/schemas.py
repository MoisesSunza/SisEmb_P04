# src/api/schemas.py

"""
Define los esquemas JSON para los endpoints de la API.
Esto sirve como documentación formal para la estructura de datos.
"""

# Esquema para el endpoint /api/sensor
SENSOR_DATA_SCHEMA = {
    "title": "Esquema de Datos del Potenciómetro",
    "type": "object",
    "properties": {
        "Valor_crudo": {
            "type": "integer",
            "description": "Valor de conteo directo del sensor RC (sin normalizar)."
        },
        "Porcentaje": {
            "type": "number",
            "format": "float",
            "description": "Valor normalizado del potenciómetro, de 0.0 a 100.0."
        },
        "Resistencia_Ohms": {
            "type": "number",
            "format": "float",
            "description": "Resistencia eléctrica aproximada en Ohmios (Ω)."
        },
        "ultima_actualizacion": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp de la última lectura del sensor en formato ISO 8601."
        }
    },
    "required": ["Valor_crudo", "Porcentaje", "Resistencia_Ohms", "ultima_actualizacion"]
}

# Esquema para el endpoint /api/estado
STATUS_SCHEMA = {
    "title": "Esquema de Estado del Sistema",
    "type": "object",
    "properties": {
        "estado": {
            "type": "string",
            "description": "Estado operativo del servidor (e.g., 'sistema funcionando')."
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp de la solicitud de estado en formato ISO 8601."
        }
    },
    "required": ["estado", "timestamp"]
}

# Estructura principal para la documentación
API_SCHEMAS = {
    "/api/sensor": {
        "GET": {
            "description": "Retorna los datos actuales del potenciómetro.",
            "response": SENSOR_DATA_SCHEMA,
            "example": {
                "Valor_crudo": 1500,
                "Porcentaje": 45.5,
                "Resistencia_Ohms": 4550.0,
                "ultima_actualizacion": "2025-11-05T01:30:00.123456"
            }
        }
    },
    "/api/estado": {
        "GET": {
            "description": "Retorna el estado de salud del servidor.",
            "response": STATUS_SCHEMA,
            "example": {
                "estado": "sistema funcionando",
                "timestamp": "2025-11-05T01:30:00.123456"
            }
        }
    }
}