import json
import os

import mysql.connector
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from mysql.connector import Error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==========================================
# CONFIGURACIÓN MQTT
# ==========================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "guau-rdian/equipo3/nivel-alimento"

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS MYSQL
# ==========================================
DB_HOST = "localhost"
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "guaurdian_db")

# ==========================================
# FUNCIONES DE CONEXIÓN A BASE DE DATOS
# ==========================================
def obtener_conexion_db():
    """Crea y retorna una conexión a la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return conexion
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None


def insertar_lectura(nivel_alimento, distancia_cm, estado_compuerta, hora_dispositivo):
    """Inserta una lectura recibida desde el ESP32 en la tabla Lecturas."""
    conexion = obtener_conexion_db()
    if conexion is None or not conexion.is_connected():
        print("⚠️ No hay conexión a la base de datos. Registro omitido.")
        return

    cursor = None
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO Lecturas (nivel_alimento, distancia_cm, estado_compuerta, hora_dispositivo, fecha_registro)
            VALUES (%s, %s, %s, %s, NOW())
        """
        valores = (nivel_alimento, distancia_cm, estado_compuerta, hora_dispositivo)
        cursor.execute(query, valores)
        conexion.commit()
        print(
            f"💾 [MySQL] Dato guardado -> Nivel: {nivel_alimento}% | "
            f"Distancia: {distancia_cm}cm | Compuerta: {estado_compuerta}"
        )
    except Error as e:
        print(f"❌ Error al insertar datos en MySQL: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conexion.is_connected():
            conexion.close()


# ==========================================
# CALLBACKS DE PAHO MQTT
# ==========================================
def on_connect(client, userdata, flags, rc, properties=None):
    """Se ejecuta cuando el cliente se conecta al broker MQTT."""
    if rc == 0:
        print("\n--------------------------------------------------")
        print(" ¡Conexión exitosa al Broker MQTT!")
        print(f" Suscribiéndose al tópico: {MQTT_TOPIC}")
        print("--------------------------------------------------\n")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Error al conectar al Broker MQTT. Código: {rc}")


def on_message(client, userdata, msg):
    """Procesa cada mensaje JSON recibido desde el ESP32."""
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"📩 Mensaje recibido en [{msg.topic}]: {payload_str}")

        datos = json.loads(payload_str)
        nivel_alimento = datos.get("nivel_alimento")
        distancia_cm = datos.get("distancia_cm")
        estado_compuerta = datos.get("estado_compuerta")
        hora_dispositivo = datos.get("hora")

        insertar_lectura(nivel_alimento, distancia_cm, estado_compuerta, hora_dispositivo)
    except json.JSONDecodeError:
        print("⚠️ Error: El mensaje recibido no tiene formato JSON válido.")
    except Exception as e:
        print(f"⚠️ Error al procesar el mensaje: {e}")


# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print("        INICIANDO SERVIDOR REMOTO GUAU-RDIAN        ")
    print("==================================================")

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"Conectando a {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido manualmente.")
    except Exception as e:
        print(f"❌ Error general en el servidor: {e}")
