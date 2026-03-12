#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import print_function
'''

Este script sería para ejecutarlo en el robot Pepper y manda las ordendes de IA a un servidor remoto.

Main script to perform the whole conversation pipeline. This consists of:

1) Speech recognition system: 
    - Input: Human voice recording
    - Output: Text recognixed from the audio

2) Question answering bot:
    - Input: Text recognized from the audio
    - Output: Answer for the question in a given context

3) Text-to-speech generation:
    - Input Answer for the question
    - Output: Audio for the answer
'''
import subprocess
import os 
import random 
import argparse 
import time
import sys
import requests
from choice_script import ask_pepper_question

 

def call_python_script(action, args_dict=None):
    '''
    Function used to run a script in another python version. We need this to use Naoqi and work with
    Pepper robot, which only works in Python 2.7 (https://developer.softbankrobotics.com/pepper-naoqi-25/naoqi-developer-guide/getting-started/downloading-installing-softbank-robotics)
    '''
    command = ["python", "pepper_interact.py", "--action", action]
    if args_dict:
        for key, value in args_dict.items():
            command.append("--%s" % key)
            command.append(str(value))
    subprocess.call(command)

def call_AI_model(provider, ip, port, personalidad=4, word_limit=40):

    # El endpoint al que queremos llamar
    url = "http://" + ip + ":" + port + "/procesar_recibir_respuesta"

    print("Llamando al modelo AI en:", url)

    try:
        # Preparamos los parámetros de la petición
        payload = {
            "provider": provider,  # Puede ser 'gemini', 'openai'...
            "personalidad": personalidad,  # Puedes ajustar esto según tus necesidades
            "word_limit": word_limit
        }

        # Hacemos la petición GET
        response = requests.get(url, params=payload)

        # Verificamos si la petición fue exitosa (código de estado 200)
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)

        # Convertimos la respuesta a formato JSON
        data = response.text
        if isinstance(data, unicode):
            data = data.encode('utf-8')

    
        # Imprimimos los datos obtenidos
        print("Petición exitosa!")
        print("Datos recibidos:")
        print(data)

        return data

    except requests.exceptions.HTTPError as errh:
        print("Error HTTP: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        print("Error de Conexión: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        print("Error de Timeout: {}".format(errt))
    except requests.exceptions.RequestException as err:
        print("Algo salió mal: {}".format(err))



def mandarArchivo(archivo, ip):

    print("Mandando archivo al servidor remoto...")
    user = 'pepper'
    
    # Comando SCP
    cmd = [
        'scp', '-P', '8080',
        '-o', 'StrictHostKeyChecking=no',  # Evitar verificación de host
        '-o', 'BatchMode=yes',              # No pedir contraseña interactiva
        archivo,
        '{}@{}:/home/pepper/pepper-chatbot/servergpu/'.format(user, ip)
    ]
    print("Ejecutando comando: {}".format(' '.join(cmd)))
    
    try:
        # Ejecutar comando SCP capturando stdout y stderr
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        result = proc.returncode
        if result == 0:
            print("Archivo transferido exitosamente")
            if stdout:
                print("Output: {}".format(stdout.strip()))
        else:
            print("Error en la transferencia (código {}):".format(result))
            if stderr:
                print("Detalle del error: {}".format(stderr.strip()))
            if stdout:
                print("Output: {}".format(stdout.strip()))
    except Exception as e:
        print("Error: {}".format(e))


def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write("⏳ Time left: %2d seconds\r" % i)
        sys.stdout.flush()
        time.sleep(1)
    print("\n⏹️ Time's up!")

def preguntar_personalidad():
    
    pregunta = "¿Qué personalidad quieres que tenga? Puedo ser: cuidador de mayores, cuidador de niños, profesor o pepper"
    respuestas = {
        "mayores": {"text": "Has elegido ser cuidador de mayores", "value": 1},
        "niños": {"text": "Has elegido ser cuidador de niños", "value": 2},
        "profesor": {"text": "Has elegido ser profesor", "value": 3},
        "pepper": {"text": "Has elegido ser pepper", "value": 4}
    }
    return ask_pepper_question(pregunta, respuestas)


def main(server_ip, server_port, recording_time, provider, word_limit):
    os.system('clear')
    
    asking = True
    language = 'Spanish'

    if provider == 'none':
        pregunta = "¿Qué proveedor de IA quieres usar? Di 'uno' para Gemini y 'dos' para OpenAI"
        respuestas = {
            "uno": {"text": "Gemini", "value": "gemini"},
            "dos": {"text": "OpenAI", "value": "openai"},
        }
        _, provider_value = ask_pepper_question(pregunta, respuestas)
        if provider_value == None:  
            print("No se ha seleccionado ningún proveedor de IA")
            return
        else:
            provider = provider_value

    personalidad, valor_personalidad = preguntar_personalidad()

    call_python_script("speak", {"sentence": personalidad, "language": language})

    
    waiting_messages = [["Estoy pensando"], ["Un momento"],["Espere un momento"]]
    
    try:
        while asking:
            sentence = "Toca mi cabeza para hacerme una pregunta"
            print(sentence)     
            call_python_script("speak", {"sentence": sentence, "language": language})
            # Wait for pepper to sense touch
            call_python_script("wait_touch", {"language": language})
            # Open microphone and wait for the question            
            print('Pepper is listening to you!')        
            call_python_script("listen", {"listen_time": recording_time})
            print("Pepper has stopped listening.")
            call_python_script("speak", {"sentence": random.choice(waiting_messages)[0], "language": language})
            createdFile = '/home/nao/test.wav'

            call_python_script("speak", {"sentence": "ya he terminado de escuchar", "language": language})


            print('Mandamos archivo al servidor remoto.')
            mandarArchivo(createdFile, server_ip)
            print('Llamamos al modelo AI.')
            response = call_AI_model(provider, server_ip, server_port, personalidad=valor_personalidad, word_limit=word_limit)
            print("Respuesta del modelo AI: ", response)

            if response == '':
                print("Respuesta vacía")
                response = "Puedes repetir la pregunta"

            call_python_script("speak", {"sentence": response, "language": language})

            pregunta = "¿Tienes alguna otra pregunta?"
            respuestas = {
                "si": {"text": "¡Vamos!", "value": 1},
                "no": {"text": "Entiendo. Ha sido un placer. No dudes en volver a consultarme.", "value": 0}
            }

            value = None
            while value is None:
                answer, value = ask_pepper_question(pregunta, respuestas)
                time.sleep(0.5)
            asking = value 

        call_python_script("speak", {"sentence": answer, "language": language})
    except KeyboardInterrupt:
        call_python_script("switch_awareness", {"sentence": "Disable"})

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script de control para la interacción con Pepper AI")

    parser.add_argument("--recording_time", type=int, default=6, required=False, help="Tiempo en segundos para grabar la pregunta (por defecto: 6)")
    parser.add_argument("--num_of_words", type=int, default=40, required=False, help="Número máximo de palabras a procesar (por defecto: 40)")
    parser.add_argument("--provider", type=str, default="none", required=False, help="Proveedor a utilizar para el bot de preguntas y respuestas (por defecto: gemini)")
    parser.add_argument("--serverIP", type=str, required=True, help="Dirección IP del servidor donde está alojado el modelo de IA")
    parser.add_argument("--serverPort", type=str, default="5000", required=True, help="Puerto del servidor donde está alojado el modelo de IA (por defecto: 5000)")
    
    args = parser.parse_args()

    main(args.serverIP, args.serverPort, args.recording_time, args.provider, args.num_of_words)