from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__, template_folder='templates')

# Configuración de conexión a la base de datos remota
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="if0_37824823_historial_emocional"
    )
    print("Conexión exitosa a la base de datos.")
except mysql.connector.Error as err:
    print(f"Error al conectar: {err}")

# Comprobar conexión a la base de datos
try:
    db.ping(reconnect=True)
    print("Conexión exitosa a la base de datos.")
except mysql.connector.Error as err:
    print(f"Error conectando a la base de datos: {err}")
    exit()

cursor = db.cursor()

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Registrar emociones
@app.route("/registrar_emocion", methods=["POST"])
def registrar_emocion():
    nombre = request.form.get("nombre", "").strip()
    emocion = request.form.get("emocion", "").strip()
    comentario = request.form.get("comentario", "").strip()

    # Validar datos
    emociones_validas = ["Estrés", "Ansiedad", "Tristeza", "Alegría"]
    if not nombre or emocion not in emociones_validas or not comentario:
        return "Datos inválidos o incompletos", 400

    try:
        query = "INSERT INTO emociones (fecha, emocion, comentario, nombre) VALUES (NOW(), %s, %s, %s)"
        cursor.execute(query, (emocion, comentario, nombre))
        db.commit()
        return redirect(url_for("ver_historial"))
    except mysql.connector.Error as err:
        print(f"Error al registrar emoción: {err}")
        return "Error al registrar emoción", 500

# Ver historial emocional
@app.route("/historial")
def ver_historial():
    query = "SELECT fecha, emocion, comentario, nombre FROM emociones"
    cursor.execute(query)
    historial = cursor.fetchall()
    return render_template("historial_emocional.html", historial=historial)

# Ruta para chatbot
@app.route("/procesar_mensaje", methods=["POST"])
def procesar_mensaje():
    mensaje = request.json.get("mensaje", "").lower()

    # Respuestas predefinidas del chatbot
    if "hola" in mensaje:
        respuesta = "¡Hola! ¿En qué puedo ayudarte?"
    elif "adiós" in mensaje:
        respuesta = "¡Hasta luego! Que tengas un buen día."
    else:
        respuesta = "Lo siento, no entiendo tu mensaje. ¿Puedes intentar de otra forma?"

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)
