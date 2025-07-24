'''
Servidor Flask para procesar archivos de audio y recibir respuestas del modelo AI.
Alojado en el servidor externo de Pepper.

REQUISITOS:
- Tener flask
- Tener el archivo server_recognition.py en la misma carpeta que este script
- Tener los providers configurados (gemini.py, etc.)
- Tener las API keys configuradas en el entorno
- Tener el archivo de audio test.wav en la misma carpeta que este script
'''

from flask import Flask, request, jsonify
from server_recognition import procesar_archivo
from providers import get_available_providers
from personality_manager import PersonalityManager

app = Flask(__name__)

@app.route("/procesar_recibir_respuesta", methods=["GET"])
def llamada():
    """
    Endpoint principal para procesar audio y generar respuesta.
    
    Parámetros:
        provider (str): Nombre del provider ('gemini', 'openai', etc.)
        personalidad (str): ID de la personalidad (1, 2, 3, etc.)
        archivo (str, opcional): Nombre del archivo de audio (default: test.wav)
    
    Returns:
        str: Respuesta generada por la IA
    """
    # Get parameters
    provider = request.args.get("provider")
    personalidad = request.args.get("personalidad")
    archivo = request.args.get("archivo", "test.wav")  # Default to test.wav
    
    # Validate required parameters
    if not provider:
        return "Error: Parámetro 'provider' es requerido. Providers disponibles: " + ", ".join(get_available_providers()), 400
    
    if not personalidad:
        personalidad = "4"  # Default personality
    
    try:
        respuesta = procesar_archivo(archivo, provider, personalidad)
        return respuesta
    except Exception as e:
        return f"Error interno del servidor: {str(e)}", 500

@app.route("/", methods=["GET"])
def get_info():
    """
    Endpoint informativo que muestra todos los providers y personalidades disponibles.
    
    Returns:
        json: Información completa del sistema
    """
    try:
        providers = get_available_providers()
        personality_manager = PersonalityManager()
        personalidades_data = personality_manager.get_available_personalities()
        
        # Format personalities with line breaks for better display
        personalidades_formateadas = ""
        for key, value in personalidades_data.items():
            personalidades_formateadas += f"{key}: {value['name']}\n"
        
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Información del Sistema</title>
        </head>
        <body>
            <h1>INFORMACIÓN DEL SISTEMA</h1>
            
            <h2>PROVIDERS DISPONIBLES</h2>
            <pre>{}</pre>
            
            <h2>PERSONALIDADES DISPONIBLES</h2>
            <pre>{}</pre>
            
            <h2>PARÁMETROS</h2>
            <ul>
                <li><strong>provider</strong> (requerido): Nombre del provider (<code>gemini</code>, <code>openai</code>)</li>
                <li><strong>personalidad</strong> (opcional): ID de personalidad (1-4, default: 4)</li>
                <li><strong>archivo</strong> (opcional): Archivo de audio (default: test.wav)</li>
            </ul>
            
            <h2>ENDPOINTS DISPONIBLES</h2>
            <ul>
                <li><strong>/</strong> - Información completa del sistema</li>
                <li><strong>/procesar_recibir_respuesta</strong> - Procesar audio y generar respuesta</li>
            </ul>
            
            <h2>EJEMPLO DE USO</h2>
            <p>/procesar_recibir_respuesta?provider=gemini&personalidad=1</p>
        </body>
        </html>
        """.format(providers, personalidades_formateadas)
        
        return html_content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)