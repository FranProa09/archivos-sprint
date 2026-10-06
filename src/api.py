import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_HOST = "localhost"
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "guaurdian_db")


# ==========================================
# CREAR API
# ==========================================

app = FastAPI(
    title="GUAU-RDIAN API",
    description="API REST para consultar los datos del dispensador.",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# CONEXIÓN A MYSQL
# ==========================================

def obtener_conexion_db():
    """Crea y retorna una conexión a MySQL."""
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


# ==========================================
# ENDPOINT PRINCIPAL
# ==========================================

@app.get("/")
def inicio():
    return {
        "mensaje": "API GUAU-RDIAN funcionando correctamente"
    }


# ==========================================
# ENDPOINT 1: TODAS LAS LECTURAS
# ==========================================

@app.get("/api/lecturas")
def obtener_lecturas():

    conexion = obtener_conexion_db()

    if conexion is None or not conexion.is_connected():
        return {
            "error": "No se pudo conectar a la base de datos"
        }

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        query = """
            SELECT
                id,
                nivel_alimento,
                distancia_cm,
                estado_compuerta,
                hora_dispositivo,
                fecha_registro
            FROM Lecturas
            ORDER BY fecha_registro DESC
        """

        cursor.execute(query)

        lecturas = cursor.fetchall()

        return lecturas

    except Error as e:

        return {
            "error": f"Error al consultar MySQL: {str(e)}"
        }

    finally:

        if cursor is not None:
            cursor.close()

        if conexion.is_connected():
            conexion.close()


# ==========================================
# ENDPOINT 2: ÚLTIMA LECTURA
# ==========================================

@app.get("/api/lecturas/ultima")
def obtener_ultima_lectura():

    conexion = obtener_conexion_db()

    if conexion is None or not conexion.is_connected():
        return {
            "error": "No se pudo conectar a la base de datos"
        }

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        query = """
            SELECT
                id,
                nivel_alimento,
                distancia_cm,
                estado_compuerta,
                hora_dispositivo,
                fecha_registro
            FROM Lecturas
            ORDER BY fecha_registro DESC
            LIMIT 1
        """

        cursor.execute(query)

        lectura = cursor.fetchone()

        if lectura is None:
            return {
                "mensaje": "No hay lecturas registradas"
            }

        return lectura

    except Error as e:

        return {
            "error": f"Error al consultar MySQL: {str(e)}"
        }

    finally:

        if cursor is not None:
            cursor.close()

        if conexion.is_connected():
            conexion.close()