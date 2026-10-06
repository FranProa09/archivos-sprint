# Python Guardian

Proyecto para recibir lecturas de nivel de alimento desde un ESP32 por MQTT y almacenarlas en MySQL.

## Requisitos

- Python 3
- MySQL Server
- Broker MQTT público como HiveMQ o Mosquitto

## Instalación de dependencias

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

1. Crea la base de datos y la tabla ejecutando el script SQL ubicado en `config/database.sql`.
2. Verifica que MySQL esté corriendo en `localhost`.

## Ejecución del servidor

```bash
python3 src/main.py
```

El script escucha el tópico MQTT `guau-rdian/equipo3/nivel-alimento` y guarda cada lectura en la tabla `Lecturas`.
