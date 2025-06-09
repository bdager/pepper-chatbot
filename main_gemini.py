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
import json
import subprocess
import os
import speech_recognition as sr

import execnet
from unidecode import unidecode
import paramiko
import scp
import random
#from googletrans import Translator

# import requests
from gemini import Gemini
# import ipdb
import argparse
from langcodes import Language
from langcodes.tag_parser import LanguageTagError

def call_python_version(Version, Module, Function, ArgumentList):
    '''
    Function used to run a script in another python version. We need this to use Naoqi and work with
    Pepper robot, which only works in Python 2.7 (https://developer.softbankrobotics.com/pepper-naoqi-25/naoqi-developer-guide/getting-started/downloading-installing-softbank-robotics)

    Code borrowed from https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3
    '''
    gw      = execnet.makegateway("popen//python=python%s" % Version)
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


def main(gemini, args):
    # ---------------- INITIALIZATION -------------------- #
    # Identify current path
    path = os.path.dirname(os.path.abspath(__file__))
    # Create Speech-to-text recognizer object
    recognizer = sr.Recognizer()
    # Create Question-Answering bot
     
    # Stop awareness module from the robot
    #call_python_version("2.7", "pepper_interact", "switch_awareness", ["Disable"])
    # Clear terminal output for clearness
    os.system('clear')

    # Initiate conversation loop
    converse_enabled = False
    #print('Touch me to ask a question!')
    
    sentence= "Toca mi cabeza para hacerme una pregunta"
    # ipdb.set_trace()
    text_robot = sentence
    #print(text_robot.text)
    print(sentence)     
    language = 'Spanish'
    langue_voulue = 'es' #Spanish, 'en': English     
    
    
    call_python_version("2.7", "pepper_interact", "speak", [text_robot,language])
    try:
        while True:
            # Wait for pepper to sense touch
            call_python_version("2.7", "pepper_interact", "wait_touch", [language])
            
            # ---------------- SPEECH TO TEXT -------------------- #
            # use_pepper = args.usePepper
            use_pepper = False
            
            # Open microphone and wait for the question            
            if use_pepper:
                # Start audio recording with pepper
                print('Pepper is listening to you!')        
                call_python_version("2.7", "pepper_interact", "listen", ["8"])
                print("Pepper has stopped listening.")
                # Get audio file from pepper
                #Create ssh client and scp
                print('Copying audio file...')
                # Feedback message
                messages = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
                #messages = [translator.translate(msg[0], dest=language).text for msg in messages2]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages),language])
                
                ssh = createSSHClient("192.168.10.116", 22, 'nao', 'nao')
                scpClient = scp.SCPClient(ssh.get_transport())
                    
                #Get file
                scpClient.get('/home/nao/test.wav', os.getcwd() + '/recording.wav')
                print('File copied!')

                # Load recorded audio file from pepper
                recording = sr.AudioFile('recording.wav')   
                with recording as source:
                    audio = recognizer.listen(source)
            else:
                # Use pc microphone    
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source, phrase_time_limit=8)
                    
                    print("Stop listening")
                    
                # Feedback message
                messages = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
                #messages = [translator.translate(msg[0], dest=language).text for msg in messages2]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages),language])                

        # Use Google Speech Recognition module to perform speech-to-text
            try:
                print('Translating...')
                print("I think you asked: ")
                langue_voulue = 'es'
                translation = recognizer.recognize_google(audio, language=langue_voulue)
                print(translation)
            except sr.UnknownValueError:
                print("Sorry, I didn't understand you")
               
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))     
                
            # Force the question to be in less than a determined number of words
            num_of_words = 30
            prompt = "Por favor, responde a la siguiente pregunta con una sola opción utilizando menos de " + str(num_of_words) + " palabras: "
            #prompt = translator.translate(text_force_prompt, dest= language_voice)                     
            text_question = prompt + " '" + translation + "?' "
            
            print(text_question)
                       
            #get the answer using Gemini
            client = Gemini(cookies=cookies)
            response_text, response_status = client.send_request(text_question)
            #print(response_text)
            response = response_text
    
            resp = response.replace('\n', '')
            resp = resp.replace('\\\\n', '')
            resp = resp.replace('\r', '')
            #resp = resp.replace('?', '')
            resp = resp.replace('null,', '')
            
            # Delete tildes
            resp = resp.replace('á', 'a')
            resp = resp.replace('é', 'e')
            resp = resp.replace('í', 'i')
            resp = resp.replace('ó', 'o')
            resp = resp.replace('ú', 'u')
            resp = resp.replace('ñ', 'ny')
            text = resp[150:500]
    
            substring = "rc_"
            result = ''
    
            parts = text.split(substring, 1)
            if len(parts) > 1:
                result = parts[1]
            #print(result)  # Output: the part you need]
            else:
                print("Substring not found")
            
            substring2 = ",["
            result2 =''
    
            parts = result.split(substring2, 1)
            if len(parts) > 1:
                result2 = parts[1][2:]
            #print(result2)  # Output: the part you need]
            else:
                print("Substring not found")
          
            parts = result2.split("]", 1)  
            result3 = parts[0][:-2]
                        
            result3 = ".".join(result3.split('.')[:-1])
            print(result3)  # Output: the part you need]
            
            if result3 == '':
                print("Respuesta vacía")
                result3="Puedes repetir la pregunta"

            # ----------------- TEXT TO SPEECH -------------------#
            # Make Pepper reply with the answer found by the bot
            args = []
            args.append(result3)
            print(args)
            call_python_version("2.7", "pepper_interact", "speak", [args,language])

    except KeyboardInterrupt:
       call_python_version("2.7", "pepper_interact", "switch_awareness", ["Disable"])
            #print("")

if __name__ == "__main__":  
    
    cookies_path = "/home/bessie/Downloads/cookies.txt"
    # Leer el archivo y convertirlo a diccionario
    with open(cookies_path, 'r') as file:
        cookies_data = file.read()
        
    cookies_data = cookies_data.replace("cookies = ", '')
    
    # Convertir el contenido JSON a diccionario
    cookies_dict = json.loads(cookies_data)

    # cookies = {
    #      "__Secure-1PSIDCC" : "AKEyXzVQrCbhUBmKzx1PVrw6-8BsiqP_EEsMvWkB0Pv2C82TxT6eQ1TwD4vKijzlNn7WHlVpf8I",
    #      "__Secure-1PSID" : "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076",
    #      "__Secure-1PSIDTS" : "sidts-CjIB3EgAEmoOLKl09YPoL5PzAW7axCGNg67roqPH-YKqbVh18HYUv_nUXlQwavjJfqKwHBAA",
    #      "NID" : "514=S-q95aCpyuQzMhB1QsxIy-cOoqAtpkZvXkRN5EiZltylMB65hemqTAoQxq9HWcDgLvtsGe4FNVVh9JJ436GYKLtcZgKuVRoI8W8HfaJHDuJjM708oMv-EP1r0OcDWBqdblBlNJRS-C6vI9UWiZLVEamAy9oR9Q6611hsHDnpmvVLjYo36dzBIgxAsVYzyhOeG2wUO5TBOI86AuD49FwmC3UeXqFTBvPkRw2f45JncjmHB4udN-ixdm6XfI-IIPj43Iy7qnAvuHs5y-G46lbJO_ATDQ5hhILNTuwlqBLdwWvXoxx3m5YJXvqK3Jd3JojXKAiiv6Nd0Ci-JQe43zjmOd-cb1HUGnpqVIpFy6f-NQif5SJ00zud1reBCmfW7mDqVg",
    #      # Cookies may vary by account or region. Consider sending the entire cookie file.
    #    }
    
    cookies = {
         "__Secure-1PSIDCC" : cookies_dict["__Secure-1PSIDCC"],
         "__Secure-1PSID" : cookies_dict["__Secure-1PSID"],
         "__Secure-1PSIDTS" : cookies_dict["__Secure-1PSIDTS"],
         "NID" : cookies_dict["NID"],
       }

    gemini = Gemini(cookies=cookies)    

    # Calls the Bard object's "get_answer" method to specify not to use images in its response.
    # bard_output = bard.get_answer("Please keep your answers to a maximum of 100 words without using images.")['content']

    # Select if you're going to use the pepper or the PC microphone
    # True => pepper microphone; False => PC microphone
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_pepper_mic", dest="usePepper", type=bool, default=False, 
                        required=False, help="Select if you're using Pepper or PC mic")
    args = parser.parse_args()

    main(gemini,args)
