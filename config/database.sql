CREATE DATABASE IF NOT EXISTS guaurdian_db;
USE guaurdian_db;

CREATE TABLE IF NOT EXISTS Lecturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel_alimento INT,
    distancia_cm INT,
    estado_compuerta VARCHAR(20),
    hora_dispositivo VARCHAR(10),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
