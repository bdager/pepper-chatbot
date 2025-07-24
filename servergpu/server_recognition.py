import speech_recognition as sr
from providers import get_provider
from personality_manager import PersonalityManager

'''
Programa que procesa un archivo de audio, lo convierte a texto y llama a un modelo de IA para generar una respuesta.
'''


def procesar_archivo(archivo, provider, personalidad):
    """
    Procesa un archivo de audio y genera una respuesta usando el provider y personalidad especificados.
    
    Args:
        archivo (str): Ruta del archivo de audio
        provider (str): Nombre del provider ('gemini', 'openai', etc.)
        personalidad (str): ID de la personalidad a usar
        
    Returns:
        str: Respuesta generada por el modelo de IA
    """
    language_code = 'es-ES'  # Language code for Spanish
    
    # Validar los inputs
    if not provider:
        return "Error: Provider no especificado"
    
    if not personalidad:
        personalidad = "4"  # Default personality
    
    # Transcribir audio a texto
    transcription = transcribir_audio(archivo, language_code)
    if transcription.startswith("Error:") or transcription.startswith("No pude"):
        return transcription
    
    # Generar la respuesta de la IA
    return generar_respuesta_ai(transcription, provider, personalidad)

def transcribir_audio(archivo, language_code='es-ES'):
    """
    Transcribe un archivo de audio a texto usando Google Speech Recognition.
    
    Args:
        archivo (str): Ruta del archivo de audio
        language_code (str): Código de idioma para la transcripción
        
    Returns:
        str: Transcripción del audio o mensaje de error
    """
    print('Transcribiendo audio...')
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(archivo) as source:
            audio = recognizer.record(source)
        
        print("Procesando transcripción...")
        transcription = recognizer.recognize_google(audio, language=language_code)
        print(f"Transcripción: {transcription}")
        return transcription
        
    except sr.UnknownValueError:
        print("Error: No se pudo entender el audio.")
        return "No pude entenderte, lo siento"
    except sr.RequestError as e:
        print(f"Error al conectar con el servicio de reconocimiento: {e}")
        return "Error al procesar la solicitud de reconocimiento de voz"
    except Exception as e:
        print(f"Error inesperado durante la transcripción: {e}")
        return "Error inesperado durante el procesamiento de audio"

def generar_respuesta_ai(pregunta, provider_name, personalidad_id):
    """
    Genera una respuesta usando el provider y personalidad especificados.
    
    Args:
        pregunta (str): Pregunta transcrita del audio
        provider_name (str): Nombre del provider a usar
        personalidad_id (str): ID de la personalidad
        
    Returns:
        str: Respuesta generada por la IA
    """
    try:
        # Obtener el provider
        provider = get_provider(provider_name)
        print(f"Usando provider: {provider.name}")

        # Inicializar el manager de personalidades
        personality_manager = PersonalityManager()
        
        # Obtener la personalidad
        personality = personality_manager.get_personality(personalidad_id)
        if not personality:
            return "Error: Personalidad no encontrada"
        
        system_prompt = personality.get('system_prompt', '')
        personality_name = personality.get('name', '')
        print(f"Usando personalidad: {personality_name}")
        
        # Preparar el prompt
        prompt_prefix = "Por favor, responde a la siguiente pregunta usando menos de 40 palabras: "
        full_prompt = f"{prompt_prefix}'{pregunta}'"
        print(f"Prompt: {full_prompt}")
        
        # Generar la respuesta usando el provider
        response = provider.generate_response(
            prompt=full_prompt,
            system_prompt=system_prompt,
        )
        
        print(f"Respuesta de {provider_name}: {response}")
        return response
        
    except ValueError as e:
        print(f"Error de configuración: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        print(f"Error al generar respuesta: {e}")
        return "Error al procesar la solicitud de IA"

if __name__ == "__main__":
    print(procesar_archivo("test.wav", "gemini", "4"))