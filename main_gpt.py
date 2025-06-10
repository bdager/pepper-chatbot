#!usr/bin/python
'''
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
import speech_recognition as sr
import paramiko
import scp
import random
import argparse
import threading
from gpt_class import GPTDescriptor
import time
 

def call_python_script(action, args_dict=None):
    '''
    Function used to run a script in another python version. We need this to use Naoqi and work with
    Pepper robot, which only works in Python 2.7 (https://developer.softbankrobotics.com/pepper-naoqi-25/naoqi-developer-guide/getting-started/downloading-installing-softbank-robotics)
    '''
    command = ["python2.7", "pepper_interact.py", "--action", action]
    if args_dict:
        for key, value in args_dict.items():
            command.append(f"--{key}")
            command.append(str(value))
    subprocess.call(command)
    

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password, look_for_keys=False, allow_agent=False)
    return client


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"⏳ Time left: {i:2d} seconds", end="\r")
        time.sleep(1)
    print("\n⏹️ Time's up!")


def main(gpt_model, args):
    recognizer = sr.Recognizer()
    os.system('clear')
    
    use_pepper = args.usePepper
    IP = args.IP  
    recording_time = args.recording_time # in seconds
    num_of_words = args.num_of_words  

    sentence = "Toca mi cabeza para hacerme una pregunta"
    text_robot = sentence
    print(sentence)     
    language = 'Spanish' #Spanish, 'en': English
    call_python_script("speak", {"sentence": text_robot, "language": language})
    
    waiting_messages = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
    
    try:
        while True:
            # Wait for pepper to sense touch
            call_python_script("wait_touch", {"language": language})
            # Open microphone and wait for the question            
            if use_pepper:
                print('Pepper is listening to you!')        
                call_python_script("listen", {"listen_time": recording_time})
                print("Pepper has stopped listening.")
                print('Copying audio file...')
                call_python_script("speak", {"sentence": random.choice(waiting_messages)[0], "language": language})
                ssh = createSSHClient(IP, 22, 'nao', 'nao')
                scpClient = scp.SCPClient(ssh.get_transport())
                scpClient.get('/home/nao/test.wav', os.getcwd() + '/recording.wav')
                print('File copied!')
                recording = sr.AudioFile('recording.wav')   
                with recording as source:
                    audio = recognizer.listen(source)
            else:
                with sr.Microphone() as source:
                    print(f"🎙️ Listening... You have {recording_time} seconds to speak")
                    
                    # Start countdown in background
                    countdown_thread = threading.Thread(target=countdown, args=(recording_time,))
                    countdown_thread.start()
                    
                    start_time = time.time()
                    # Start listening (in background) and show countdown simultaneously
                    audio = recognizer.listen(source, phrase_time_limit=recording_time)    
                    elapsed_time = time.time() - start_time                             
                    print("⏹️ Stop listening. Recording time was: {:.2f} seconds".format(elapsed_time))
                call_python_script("speak", {"sentence": random.choice(waiting_messages)[0], "language": language})        

            try:
                print('Translating...')
                print("I think you asked: ")
                langue_voulue = 'es'
                translation = recognizer.recognize_google(audio, language=langue_voulue)
                print(translation)
            except sr.UnknownValueError:
                print("Sorry, I didn't understand you")
                message_error = "No pude entenderte, lo siento"
                call_python_script("speak", {"sentence": message_error, "language": language})
                continue 
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

            prompt = "Por favor, responde a la siguiente pregunta con una sola opción utilizando menos de " + str(num_of_words) + " palabras: "
            text_question = prompt + " '" + translation + "?' "
            print(text_question)

            response = gpt_model.generate_answer(text_question)
            print("GPT response: ", response)
            
            resp = response.get('respuesta', '')         
            resp = resp.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'ny')
            result = resp.strip()

            if result == '':
                print("Respuesta vacía")
                result = "Puedes repetir la pregunta"

            print([result])
            call_python_script("speak", {"sentence": result, "language": language})

    except KeyboardInterrupt:
        call_python_script("switch_awareness", {"sentence": "Disable"})

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_pepper_mic", dest="usePepper", type=bool, default=False, required=False)
    parser.add_argument("--IP", type=str, default="192.168.1.82")
    parser.add_argument("--port", type=int, default=9559, required=False)
    parser.add_argument("--recording_time", type=int, default=6, required=False,
                        help="Time in seconds to record the question")
    parser.add_argument("--num_of_words", type=int, default=30, required=False)
    args = parser.parse_args()
    gpt_model = GPTDescriptor()    
    main(gpt_model, args)