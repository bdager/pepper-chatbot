# Pepper Chatbot 🤖

![Pepper robot](assets/pepper_2.png?raw=true)

This project enables natural language interaction with a **Pepper robot** using language models such as GPT, GEmini, LLaMA, etc. The chatbot pipeline supports speech recognition, question answering, and text-to-speech, and can run using the PC microphone or Pepper’s built-in microphone.


## Installation

This project requires both Python 3.10 and Python 2.7:

- **Python 3.10** is used for the main logic and language model interaction.
- **Python 2.7** is required for communication with Pepper using [pynaoqi](https://developer.softbankrobotics.com/pepper-naoqi-25/naoqi-developer-guide), which only supports Python 2.7.

### 1. System Dependencies

Install the following system libraries (linux system):

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev
sudo apt-get install libpython2.7
```

To avoid exporting the dynamic library path every time:

```bash
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
```

### 2. Python Dependencies

Install Python 3.10 dependencies:

```bash
pip install -r requirements.txt
```

### 3. pynaoqi Module

Make sure you have downloaded the `pynaoqi` module. In this repository, it is already included in the main directory tree.


## Running the Chatbot

### 1. Configure `pynaoqi`

Before running the chatbot, ensure the `pynaoqi` module is included in your environment:

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
```

> Replace `/path/to/` with the actual directory where you extracted the `pynaoqi` module.

### 2. Configure GPT API Key

Set your API key as an environment variable (e.g., for OpenAI GPT models):

```bash
export OPENAI_API_KEY="your_key_here"
```



## How to Use 🚀 

Once everything is set up, you can launch the main program using:

```bash
python main_gpt.py --IP <robot-ip-to-connect>
```

By default, the PC microphone is used. To use Pepper’s built-in microphone, run:

```bash
python main_gpt.py --use_pepper_mic=True
```

You will then be asked to specify the interaction language:

```bash
Please enter the desired language code (example 'es' for Spanish, 'en' for English):
```



## Interaction Flow

1. Touch Pepper's head to indicate you want to ask a question.
2. Pepper will prompt you when it's ready to listen.
3. Ask your question using voice.
4. The system processes your voice input, generates a response using the selected model, and makes Pepper speak the answer.



## Notes

- This system supports real-time interaction and requires both network access (for API calls) and local audio input/output.
- Ensure that Pepper is connected and reachable at the specified IP address (e.g., `192.168.x.x`).
- Log messages from `qimessaging` may appear at startup — this is expected behavior from the Pepper communication stack.

## Extras

The repository is organized into different modules depending on where the code is executed:

### 🎙️ Poetry with Pepper (`benedetti.py`)
This script allows Pepper to recite poems by **Mario Benedetti** using expressive speech and synchronized gestures. It's a great example of how to use Pepper's animation library combined with voice interaction. ([See README_benedetti.md](README_benedetti.md))

### 🤖 Robot-Side Scripts (`pepper-files/`)
Contains the lightweight Python 2.7 scripts that must be uploaded and executed directly on the **Pepper Robot**. This includes the bridge server that listens for commands from the web interface or external triggers. ([See pepper-files/README.md](pepper-files/README.md))

### 🖥️ AI Dedicated Server (`servergpu/`)
This folder contains the **Flask-based API** designed to run on a powerful external machine (GPU-enabled). It handles the heavy lifting: Speech-to-Text, LLM processing (GPT, Gemini, etc.), and response generation. ([See servergpu/README.md](servergpu/README.md))


