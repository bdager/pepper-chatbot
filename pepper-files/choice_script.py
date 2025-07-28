#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script para que Pepper reaccione a respuestas personalizables
Requiere Python 2.7 y NAOqi SDK
"""

from __future__ import print_function
from naoqi import ALProxy
import time

# Clave de ALMemory para marcar vocab inicializado
VOCAB_FLAG = "MyApp/VocabInitialized"
DISTINCT_VOCABS = []

class PepperInteractionHandler:
    def __init__(self, robot_ip="localhost", robot_port=9559):
        """
        Inicializa el manejador de interacciones de Pepper
        """
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.tts = None
        self.asr = None
        self.memory = None
        self._initialize_robot()

    def _initialize_robot(self):
        """
        Inicializa los proxies del robot
        """
        try:
            self.tts = ALProxy("ALTextToSpeech", self.robot_ip, self.robot_port)
            self.asr = ALProxy("ALSpeechRecognition", self.robot_ip, self.robot_port)
            self.memory = ALProxy("ALMemory", self.robot_ip, self.robot_port)
            
            # Configurar idioma
            self.asr.setLanguage("Spanish")
            print("Robot inicializado correctamente")
            
        except Exception as e:
            print("Error conectando al robot: {}".format(e))
            print("Asegúrate de que:")
            print("1. El robot esté encendido")
            print("2. La IP sea correcta")
            print("3. Estés en la misma red")
            raise

    def ask_question(self, question, response_actions, timeout=15, confidence_threshold=0.5):
        """
        Hace una pregunta al usuario y procesa la respuesta
        
        Args:
            question (str): La pregunta que hará el robot
            response_actions (dict): Diccionario que mapea cada respuesta a la acción del robot
                                   Formato: {"respuesta": {"text": "texto_respuesta", "value": numero}}
            timeout (int): Tiempo límite para esperar respuesta en segundos
            confidence_threshold (float): Umbral de confianza para aceptar la respuesta
            
        Returns:
            tuple: (texto_respuesta, valor_numerico) o (None, None) si no se reconoció
        """
        if not self.tts or not self.asr or not self.memory:
            print("Error: Robot no inicializado correctamente")
            return (None, None)

        try:
            # Extraer respuestas posibles del diccionario
            possible_responses = list(response_actions.keys())
            
            # Configurar vocabulario dinámicamente
            self._setup_vocabulary(possible_responses)
            
            # Hacer la pregunta
            self.tts.say(question)
            
            # Iniciar reconocimiento de voz
            self.asr.subscribe("Dynamic_ASR")
            
            print("Robot esperando respuesta...")
            print("Respuestas posibles: {}".format(", ".join(possible_responses)))
            
            # Limpiar datos anteriores de memoria
            self.memory.insertData("WordRecognized", [])
            
            # Esperar respuesta del usuario
            recognized_response = self._wait_for_response(timeout, confidence_threshold)
            
            if recognized_response:
                # Procesar la respuesta y devolver tupla
                return self._process_response(recognized_response, response_actions)
            else:
                self.tts.say("No pude escuchar tu respuesta. Intenta hablar más claro.")
                return (None, None)
                
        except Exception as e:
            print("Error durante la interacción: {}".format(e))
            print(e)
            return (None, None)
        finally:
            # Asegurar que se detenga el reconocimiento
            try:
                self.asr.unsubscribe("Dynamic_ASR")
            except:
                pass

    def _setup_vocabulary(self, possible_responses):
        """
        Configura el vocabulario dinámicamente basado en las respuestas posibles
        """
        try:
            # Pausar ASR para cambiar vocabulario
            self.asr.pause(True)
            
            self.asr.setLanguage("English")
            self.asr.setLanguage("Spanish")
            # Crear vocabulario expandido (incluir variaciones)
            vocabulary = []
            for response in possible_responses:
                vocabulary.append(response.lower())
                vocabulary.append(response.upper())
                vocabulary.append(response.capitalize())
            
            # Eliminar duplicados
            vocabulary = list(set(vocabulary))
            
            self.asr.setVocabulary(vocabulary, False)
            
            # Reanudar ASR
            self.asr.pause(False)
            
            print("Vocabulario configurado: {}".format(vocabulary))
            
        except Exception as e:
            print("Error configurando vocabulario")
            print(e)
            raise e

    def _wait_for_response(self, timeout, confidence_threshold):
        """
        Espera y procesa la respuesta del usuario
        """
        recognized = False
        start_time = time.time()
        time.sleep(1.0)  # Esperar antes de empezar a escuchar
        
        while not recognized and (time.time() - start_time) < timeout:
            # Verificar si hay una palabra reconocida
            word_recognized = self.memory.getData("WordRecognized")
            if word_recognized and len(word_recognized) > 1:
                recognized_word = word_recognized[0]
                confidence = word_recognized[1]
                
                print("Palabra detectada: '{}' con confianza: {:.2f}".format(recognized_word, confidence))
                
                if confidence > confidence_threshold:
                    print("Palabra reconocida con suficiente confianza: {}".format(recognized_word))
                    # Limpiar memoria después del reconocimiento
                    self.memory.insertData("WordRecognized", [])
                    return recognized_word
                else:
                    print("Confianza insuficiente ({:.2f}), continuando...".format(confidence))
                    # Limpiar para evitar re-procesamiento
                    self.memory.insertData("WordRecognized", [])
            
            time.sleep(0.1)
        
        return None

    def _process_response(self, recognized_word, response_actions):
        """
        Procesa la respuesta reconocida y devuelve la tupla correspondiente
        
        Returns:
            tuple: (texto_respuesta, valor_numerico) o (None, None) si no se encuentra
        """
        word_lower = recognized_word.lower()
        
        # Buscar la acción correspondiente
        for response_key, action_data in response_actions.items():
            if word_lower == response_key.lower():
                text = action_data.get("text", "")
                value = action_data.get("value", 0)
                
                print("Usuario respondió '{}' - Devolviendo: ('{}', {})".format(
                    recognized_word, text, value))
                return (text, value)
        
        # Si no se encuentra una acción específica
        print("Respuesta no reconocida en acciones: '{}'".format(recognized_word))
        return (None, None)


# Función de conveniencia para usar sin clase
def ask_pepper_question(question, response_actions, robot_ip="localhost", robot_port=9559, timeout=15):
    """
    Función de conveniencia para hacer una pregunta sin instanciar la clase
    
    Args:
        question (str): La pregunta que hará el robot
        response_actions (dict): Diccionario que mapea respuestas a acciones del robot
                               Formato: {"respuesta": {"text": "texto", "value": numero}}
        robot_ip (str): IP del robot
        robot_port (int): Puerto del robot
        timeout (int): Tiempo límite para respuesta
        
    Returns:
        tuple: (texto_respuesta, valor_numerico) o (None, None) si no se reconoció
    """
    handler = PepperInteractionHandler(robot_ip, robot_port)
    return handler.ask_question(question, response_actions, timeout)


# Ejemplo de uso
if __name__ == "__main__":

    print("\n=== Ejemplo 2: Múltiples opciones ===")
    # Ejemplo 2: Pregunta de múltiples opciones con diferentes valores
    question2 = "¿Qué te gustaría hacer? Puedes decir: bailar, cantar o hablar."
    actions2 = {
        "bailar": {"text": "¡Perfecto! Vamos a bailar juntos.", "value": 1},
        "cantar": {"text": "¡Qué divertido! Me encanta cantar.", "value": 2},
        "hablar": {"text": "Excelente, podemos tener una buena conversación.", "value": 3}
    }
    
    print("\n=== Ejemplo 2: Múltiples opciones ===")
    text, value = ask_pepper_question(question2, actions2)
    print("Resultado: ('{}', {})".format(text, value))
    
    # Ejemplo de uso del valor numérico para lógica de control
    if value == 1:
        print("Activando modo baile...")
    elif value == 2:
        print("Activando modo canto...")
    elif value == 3:
        print("Activando modo conversación...")
    else:
        print("No se reconoció la respuesta")

    print("\n=== Ejemplo 1: Múltiples opciones ===")
    # Ejemplo 1: Pregunta Sí/No con valores numéricos
    question1 = "¿Tienes alguna otra pregunta?"
    actions1 = {
        "si": {"text": "¡Vamos!", "value": 1},
        "no": {"text": "Entiendo. Ha sido un placer. No dudes en volver a consultarme.", "value": 0}
    }
    
    print("=== Ejemplo 1: Pregunta Sí/No ===")
    text, value = ask_pepper_question(question1, actions1)
    print("Resultado: ('{}', {})".format(text, value))
    
    # Si quieres que el robot diga el texto, lo puedes hacer después:
    if text:
        handler = PepperInteractionHandler()
        handler.tts.say(text)
    