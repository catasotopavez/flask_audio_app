import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import mysql.connector
import json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

client = openai.OpenAI(api_key=os.getenv("API_KEY"))

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "db"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

prompt = """Eres una herramienta especializada en el análisis de conversaciones con clientes. Trabajas para un supermercado cuya misión es comprender mejor los sentimientos y necesidades de sus clientes, con el fin de ofrecer un servicio de mayor calidad.

Tu tarea es recibir un audio de una conversación entre un cliente y un representante del supermercado, transcribirlo, y luego evaluarlo según los siguientes tres criterios:

Evaluación 1: Recomendación  
Asigna un puntaje entre 0 y 10 que indique qué tan probable es que el cliente recomiende el supermercado a un amigo o colega, basado únicamente en lo expresado durante la conversación.  
- 0 significa que no lo recomendaría en absoluto.  
- 10 significa que lo recomendaría con total seguridad.

Evaluación 2: Satisfacción  
Asigna un puntaje entre 0 y 10 que represente el nivel de satisfacción general del cliente con la atención recibida, según lo que se menciona en la conversación.  
- 0 representa una experiencia completamente insatisfactoria.  
- 10 representa una experiencia totalmente satisfactoria.

Evaluación 3: Problemas Mencionados  
Identifica cuáles de los siguientes problemas menciona el cliente durante la conversación. Puedes seleccionar múltiples categorías si corresponde:
- "Reposición"
- "Atención al cliente"
- "Producto no encontrado"
- "Mala calidad producto"
- "Precios"

Si el cliente menciona un problema que no corresponde a ninguna de las categorías anteriores, agrégalo bajo la categoría "Otros problemas".  
Si el cliente no menciona ningún problema, responde con "Cliente no menciona problemas".

Clasificación de la experiencia  
Clasifica la experiencia del cliente como "Positiva", "Neutra" o "Negativa" según el tono general de la conversación y los comentarios hechos por el cliente.

Tu respuesta debe estar estructurada en el siguiente formato JSON:

{
  "Evaluacion_1": "3",
  "Evaluacion_2": "2",
  "Evaluacion_3": ["Atención al cliente", "Producto no encontrado"],
  "Clasificacion": "Neutra"
}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    transcript, analysis_json = None, None

    if request.method == "POST":
        file = request.files.get("audio")
        if file and file.filename.endswith(".mp3"):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            with open(path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                ).text

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": transcript}
                ]
            )
            try:
                analysis_json = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                analysis_json = {
                    "Evaluacion_1": None,
                    "Evaluacion_2": None,
                    "Evaluacion_3": [],
                    "Clasificacion": "Neutra"
                }

            cursor.execute(
                """
                INSERT INTO analisis (
                    archivo_mp3,
                    transcripcion,
                    puntaje_recomendacion,
                    nivel_satisfaccion,
                    problemas_mencionados,
                    clasificacion_experiencia
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    file.filename,
                    transcript,
                    int(analysis_json.get("Evaluacion_1", 0)),
                    int(analysis_json.get("Evaluacion_2", 0)),
                    json.dumps(analysis_json.get("Evaluacion_3", [])),
                    analysis_json.get("Clasificacion", "Neutra")
                )
            )
            db.commit()

    return render_template("index.html", transcript=transcript, analysis=analysis_json)


@app.route("/historial")
def historial():
    cursor.execute("""
        SELECT archivo_mp3, puntaje_recomendacion, nivel_satisfaccion,
               clasificacion_experiencia, problemas_mencionados, fecha
        FROM analisis ORDER BY fecha DESC
    """)
    rows = cursor.fetchall()
    return render_template("historial.html", registros=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)