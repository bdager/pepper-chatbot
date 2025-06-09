#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Script to make Pepper say a specific sentence, listen for a question, and respond to touch events.

This script MUST be run in Python2.7
'''
from naoqi import ALProxy
import time


def speak(sentence, language, IP="192.168.1.82"):
    print("I am in speak function")
    tts = ALProxy("ALTextToSpeech", IP, 9559)
    # Select user-selected language
    tts.setLanguage(str(language))
    full_string = "\\style=didactic\\" + str(sentence)
    # Choose the peper's speaking speed
    tts.setParameter("speed", 80)
    # Separate the paragraph at each '.' to make a short pause and be more understandable
    for segment in full_string.split('.'):
        tts.say(segment + "\\wait=10\\")

def listen(listen_time = 8, IP="192.168.1.82"):
    audioRecorder = ALProxy("ALAudioRecorder", IP, 9559)
    audioRecorder.stopMicrophonesRecording()
    # Configure the channels that need to be recorded
    channels = [0, 0, 1, 0]  # Front mic only [Left, Right, Front, Rear]
    # Start the recording of Pepper's front microphone at 16000Hz
    # in the specified wav file
    audioRecorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, channels)
    time.sleep(int(listen_time))
    audioRecorder.stopMicrophonesRecording()
    print("Record finished")

def wait_touch(language, IP="192.168.1.82"):
    touchSensors = ALProxy("ALTouch", IP, 9559)
    touched = False
    while not touched:
        status = touchSensors.getStatus()
        # Check if the head has been touched
        if status[0][1] == True:
            touched = True
            # Wait for a while to give time to pepper react in alive mode to the touch
            time.sleep(3)
            if language == "Spanish":
                speak("Ahora puedes hacerme una pregunta", language)
            else:
                speak("Okay you can ask me a question", language)

def switch_awareness(enable='Disable', IP="192.168.1.82"):
    awareness = ALProxy("ALBasicAwareness", IP, 9559)
    if enable == 'Enable':
        awareness.setEnabled(True)
        awareness.setStimulusDetectionEnabled('Touch', True)
    else:
        awareness.setStimulusDetectionEnabled('Touch', False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str, required=True)
    parser.add_argument("--sentence", type=str, default="")
    parser.add_argument("--language", type=str, default="Spanish")
    parser.add_argument("--listen_time", type=int, default=8)
    parser.add_argument("--IP", type=str, default="192.168.1.82")
    args = parser.parse_args()

    if args.action == "speak":
        speak(args.sentence, args.language, args.IP)
    elif args.action == "listen":
        listen(args.listen_time, args.IP)
    elif args.action == "wait_touch":
        wait_touch(args.language, args.IP)
    elif args.action == "switch_awareness":
        switch_awareness(args.sentence, args.IP)
