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

import execnet
from unidecode import unidecode
import paramiko
import scp
import random
from googletrans import Translator

import requests
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
from langcodes import Language
from langcodes.tag_parser import LanguageTagError
from langdetect import detect_langs
# import ipdb
import argparse

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


def main(bard, args):
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
    
    while True : 
        try:
            
            langue_voulue = input("Please enter the desired language code (example 'es' for Spanish,'en' for english) : ")

            #Get the language name corresponding to the standardized language code
            language_code = Language.get(langue_voulue)
            language_voice = str(language_code.language_name())
            #the robot only speak english and spanish(we can install others languages)
            if language_voice=="English" or language_voice=="Spanish":
                language=language_voice
                print("language selected:", language)
            else : 
                language="English"
                print("you can ask questions in "+language_voice+" but the robot will respond to you in", language)
                call_python_version("2.7", "pepper_interact", "speak", ["you can ask question in "+language_voice+" but the robot will respond to you in English",language])
            
            break 
        except  LanguageTagError :
            print("invalid code, try it again")


    # Initiate conversation loop
    converse_enabled = False
    #print('Touch me to ask a question!')
    
    translator = Translator()
    sentence= "Toca mi cabeza para preguntarme una pregunta"
    # ipdb.set_trace()
    text_robot = translator.translate(sentence, dest= language) 
    #print(text_robot.text)
    print(sentence)            
    
    
    call_python_version("2.7", "pepper_interact", "speak", [text_robot.text,language])
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
                messages2 = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
                messages = [translator.translate(msg[0], dest=language).text for msg in messages2]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages),language])
                
                ssh = createSSHClient("192.168.10.117", 22, 'nao', 'nao')
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
                messages2 = [["Estoy pensando"], ["Un momento"],["espere un momento"]]
                messages = [translator.translate(msg[0], dest=language).text for msg in messages2]
                call_python_version("2.7", "pepper_interact", "speak", [random.choice(messages),language])                
            
            # Use Google Speech Recognition module to perform speech-to-text
            try:
                print('Translating...')
                print("I think you asked: ")
                translation = recognizer.recognize_google(audio, language=langue_voulue)
                print(translation)
            except sr.UnknownValueError:
                print("Sorry, I didn't understand you")
               
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))     
            
            translator = Translator()          

            # Force the question to be in less than a determined number of words
            num_of_words = 30
            text_force_prompt = "please answer the following question using just text, a single option. Use less than " + str(num_of_words) + " words. Do not use images. The question is: "
            prompt = translator.translate(text_force_prompt, dest= language_voice)                     
            text_question=prompt.text + " '" + translation + "?' "
            
            print(text_question)
                       
            #get the answer using Bard
            bard_output = bard.get_answer(text_question)['content']
            
            #loop to get the answer whitout the sentence "here is the reponse in less than (num_of_words) words"
            n=len(bard_output)
            c=-1
            if len(bard_output)>num_of_words:
                for j in range (20,num_of_words):
                    if bard_output[j]==":":
                        c=j
                        break            
            real_output=""
            for i in range (c+1,n):
                real_output+=bard_output[i]
            
            #Translation of the answer in the desired language   
            text = translator.translate(real_output, dest=language)
            text_translate=text.text
            
            #avoiding the pronunciation of special characters 
            text_translate=unidecode(text_translate)
            
            #avoiding the pronunciation of 'return to line'  
            text_translate = text_translate.replace('\n', '')
            text_translate = text_translate.replace('\r', '')
            text_translate = text_translate.replace('?', '')
            
            # num = 10
            for i in range(10,79):               
                text_translate = text_translate.replace('(' + str(i) + ' palabras)', '')
            # text_translate = text_translate.replace('?', '')
            
            print('\n')
            print(text_translate)

            # ----------------- TEXT TO SPEECH -------------------#
            # Make Pepper reply with the answer found by the bot
            args = []
            args.append(text_translate)
            print(args)
            call_python_version("2.7", "pepper_interact", "speak", [args,language])

    except KeyboardInterrupt:
       call_python_version("2.7", "pepper_interact", "switch_awareness", ["Disable"])
            #print("")

if __name__ == "__main__":  

    # Assigns the authentication token to the variable 'token'
    token= "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076."
    # Creates a new session object
    session = requests.Session()
    # Sets the headers of the session object
    session.headers = SESSION_HEADERS
    # Sets the '__Secure-1PSID' cookie in the session object with the provided token
    session.cookies.set("__Secure-1PSID", token)
    # Sets the '__Secure-1PSIDTS' cookie in the session object
    session.cookies.set("__Secure-1PSIDTS", "sidts-CjIB3EgAEoPdfhjIdYb5GZqcCrLPQIZSE21xM-rpF2a0-n9Qi1ftFjCADY_hUb9tyNwiJRAA")
    # Creates a Bard object with the given token and session
    bard = Bard(token=token, session=session)

    # Calls the Bard object's "get_answer" method to specify not to use images in its response.
    # bard_output = bard.get_answer("Please keep your answers to a maximum of 100 words without using images.")['content']

    # Select if you're going to use the pepper or the PC microphone
    # True => pepper microphone; False => PC microphone
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_pepper_mic", dest="usePepper", type=bool, default=False, 
                        required=False, help="Select if you're using Pepper or PC mic")
    args = parser.parse_args()

    main(bard,args)
