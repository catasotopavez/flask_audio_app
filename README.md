# 🧠 Analizador de Audios con Flask + OpenAI + MySQL

Esta es una aplicación web desarrollada con Flask que permite subir audios en formato `.mp3`, transcribirlos automáticamente con **Whisper (OpenAI)** y evaluarlos con **GPT-4**. Los resultados se almacenan en una base de datos **MySQL** y pueden visualizarse en un historial web.

---

## 🚀 Características

- Subida de archivos `.mp3`
- Transcripción automática del audio con `whisper-1`
- Análisis del texto con un prompt personalizado usando GPT-4
- Almacenamiento en MySQL de:
  - Nombre del archivo
  - Transcripción
  - Puntaje de recomendación
  - Nivel de satisfacción
  - Problemas mencionados
  - Clasificación de la experiencia (positiva, neutra o negativa)
  - Timestamp
- Visualización de historial de análisis

---

## 🧰 Requisitos

- Python 3.8 o superior
- MySQL instalado y funcionando
- Clave API de OpenAI

---

## ⚙️ Instalación y configuración

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/flask_audio_app.git
cd flask_audio_app
```

### 2. Crea y activa un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura tus variables de entorno

Copia el archivo de ejemplo y edítalo:

```bash
cp .env.example .env
```

Modifica `.env` con tus credenciales:

```env
API_KEY=sk-tu_clave_de_openai
DB_HOST=localhost
DB_USER=root
DB_PASS=tu_contraseña
DB_NAME=flask_audio
```

---

## 🗃️ Configuración de base de datos

### 1. Abre MySQL con el usuario root

```bash
mysql -u root -p
```

### 2. Ejecuta el script de inicialización

```sql
SOURCE /ruta/completa/al/proyecto/mysql_init.sql;
```

Ejemplo en Mac:

```sql
SOURCE /Users/tu_usuario/Desktop/flask_audio_app/mysql_init.sql;
```

---

## 🏃 Ejecutar la aplicación

Con el entorno virtual activo:

```bash
python app.py
```

Abre tu navegador y accede a:

- **Página principal:** [http://localhost:5001](http://localhost:5001)
- **Historial de análisis:** [http://localhost:5001/historial](http://localhost:5001/historial)

---

## 📝 Estructura del proyecto

```
flask_audio_app/
│
├── app.py
├── .env.example
├── requirements.txt
├── mysql_init.sql
├── templates/
│   ├── index.html
│   └── historial.html
├── uploads/
└── README.md
```

---

## ✅ Próximas mejoras (opcional)

- Exportar historial como `.csv`
- Añadir paginación o filtros en el historial
- Agregar autenticación básica
- Integrar dashboard con gráficas

---

## 📄 Licencia

Este proyecto es de uso libre para fines educativos.