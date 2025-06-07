CREATE DATABASE IF NOT EXISTS flask_audio;
USE flask_audio;

CREATE TABLE IF NOT EXISTS analisis (
  id INT AUTO_INCREMENT PRIMARY KEY,
  archivo_mp3 VARCHAR(255),
  transcripcion TEXT,
  puntaje_recomendacion TINYINT,
  nivel_satisfaccion TINYINT,
  problemas_mencionados JSON,
  clasificacion_experiencia ENUM('Positiva', 'Neutra', 'Negativa'),
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);