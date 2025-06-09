#!/usr/bin/python2
'''
Script to make pepper say a specific sentence.

This script MUST be run in Python2.7
'''
from naoqi import ALProxy
import sys
import time


IP = "192.168.10.116"

def speak(sentence, language):
    print("estoy en speak function")
    tts = ALProxy("ALTextToSpeech", IP, 9559)
    #selects user-selected language
    tts.setLanguage(str(language))
    
    full_string = "\\style=didactic\\" + str(sentence)
    
   
    #choosing the peper's speaking speed 
    tts.setParameter("speed", 80)
    
    #separate the paragraph at each '.' to make a short pause and be more understandable
    for segment in full_string.split('.'):
        tts.say(segment+"\\wait=10\\" )
        

def listen(listen_time = 8):
    audioRecorder = ALProxy("ALAudioRecorder", IP, 9559)
    audioRecorder.stopMicrophonesRecording()
    # Create recorder instance
    
    #Configures the channels that need to be recorded.
    channels = []
    channels.append(0); #Left
    channels.append(0); #Right
    channels.append(1); #Front
    channels.append(0); #Rear

    #Starts the recording of Pepper's front microphone at 16000Hz
    #in the specified wav file
    audioRecorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, channels)

    #Grabar audio 8 segundos
    time.sleep(int(listen_time))

    #Stops the recording and close the file.
    audioRecorder.stopMicrophonesRecording();
        
    print("Record finished")

def wait_touch(language):
    # Wait for touch
    touchSensors = ALProxy("ALTouch", IP, 9559)
    touched = False
    while not touched:
        status = touchSensors.getStatus()
        if status[0][1] == True: # Check if head has been touched
            touched = True
            time.sleep(2)
            if language=="Spanish":
                speak("Vale puedes hacerme una pregunta ",language)
            else :
                speak("Okay you can ask me a question ",language) 
                
    


def test(test_string):
    check = "This is being run in Python " + str(sys.version_info[0])
    check += test_string
    return check

def switch_awareness(enable='Disable'):
    awareness = ALProxy("ALBasicAwareness", IP, 9559)
    # Check if user wants to enable/disable the awareness module
    if enable=='Enable':
        awareness.setEnabled(True)
        awareness.setStimulusDetectionEnabled('Touch', True)
    else:
        # Pause awareness module
        #awareness.setEnabled(False)
        awareness.setStimulusDetectionEnabled('Touch', False)

switch_awareness('Disable')

