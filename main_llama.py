#!usr/bin/python
'''
Main script to perform the whole conversation pipeline. This consists of:

1) Speech recognition system
2) Question answering bot (now using LLaMA)
3) Text-to-speech generation
'''
import subprocess
import os
import speech_recognition as sr
import execnet
from unidecode import unidecode
import paramiko
import scp
import random
import argparse
from langcodes import Language
from langcodes.tag_parser import LanguageTagError

import transformers
import torch

class Llama:
    
    def __init__(self, model_id="meta-llama/Meta-Llama-3-8B", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[INFO] Cargando modelo '{model_id}' en {self.device}...")

        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            tokenizer=model_id,
            torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
            device_map="auto",
            use_auth_token=True
        )

    def query(self, prompt, max_new_tokens=150):
        result = self.pipeline(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7, top_p=0.9)
        return result[0]["generated_text"]



def call_python_version(Version, Module, Function, ArgumentList):
    gw = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password, look_for_keys=False, allow_agent=False)
    return client

def main(llama, args):
    path = os.path.dirname(os.path.abspath(__file__))
    recognizer = sr.Recognizer()
    os.system('clear')

    sentence = "Toca mi cabeza para hacerme una pregunta"
    print(sentence)
    language = 'Spanish'
    langue_voulue = 'es'
    
    call_python_version("2.7", "pepper_interact", "speak", [sentence, language])
    
    try:
        while True:
            call_python_version("2.7", "pepper_interact", "wait_touch", [language])
            use_pepper = False

            if use_pepper:
                print('Pepper is listening to you!')
                call_python_version("2.7", "pepper_interact", "listen", ["8"])
                print("Pepper has stopped listening.")
                print('Copying audio file...')
                messages = [["Estoy pensando"], ["Un momento"], ["espere un momento"]]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages), language])

                ssh = createSSHClient("192.168.1.82", 22, 'nao', 'nao')
                scpClient = scp.SCPClient(ssh.get_transport())
                scpClient.get('/home/nao/test.wav', os.getcwd() + '/recording.wav')
                print('File copied!')

                recording = sr.AudioFile('recording.wav')
                with recording as source:
                    audio = recognizer.listen(source)
            else:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source, phrase_time_limit=8)
                    print("Stop listening")

                messages = [["Estoy pensando"], ["Un momento"], ["espere un momento"]]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages), language])

            try:
                print('Translating...')
                translation = recognizer.recognize_google(audio, language=langue_voulue)
                print(f"I think you asked: {translation}")
            except sr.UnknownValueError:
                print("Sorry, I didn't understand you")
                continue
            except sr.RequestError as e:
                print("Speech recognition error:", e)
                continue

            prompt = f"Por favor, responde a la siguiente pregunta con una sola opción utilizando menos de 30 palabras: '{translation}?'"
            print(prompt)

            response = llama.query(prompt)

            resp = response.replace('\n', '').replace('\\\\n', '').replace('\r', '').replace('null,', '')
            resp = resp.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'ny')
            text = resp[150:500]

            substring = "rc_"
            result = ''
            parts = text.split(substring, 1)
            if len(parts) > 1:
                result = parts[1]
            else:
                print("Substring not found")

            substring2 = ",["
            result2 = ''
            parts = result.split(substring2, 1)
            if len(parts) > 1:
                result2 = parts[1][2:]
            else:
                print("Substring not found")

            parts = result2.split("]", 1)
            result3 = parts[0][:-2]
            result3 = ".".join(result3.split('.')[:-1])
            print(result3)

            if result3 == '':
                print("Respuesta vacía")
                result3 = "Puedes repetir la pregunta"

            call_python_version("2.7", "pepper_interact", "speak", [[result3], language])

    except KeyboardInterrupt:
        call_python_version("2.7", "pepper_interact", "switch_awareness", ["Disable"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_pepper_mic", dest="usePepper", type=bool, default=False,
                        required=False, help="Select if you're using Pepper or PC mic")
    args = parser.parse_args()

    llama = Llama(model_id="meta-llama/Meta-Llama-3-8B")  # CORREGIDO: model_path → model_id
    main(llama, args)

