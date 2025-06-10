# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import paramiko
from scp import SCPClient
import speech_recognition as sr

# Dirección IP del robot Pepper
ip = "192.168.1.82"  # Cámbiala por la IP de tu robot si es diferente
port = 9559
motion = ALProxy("ALMotion", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)
tts = ALProxy("ALTextToSpeech", ip, port)
audioRecorder = ALProxy("ALAudioRecorder", ip, port)
tts.setLanguage("Spanish")

def speak(texto):
    full_string = "\\style=didactic\\" + str(texto)
    tts.say(full_string)

    
def listen(listen_time=10):
    """Graba audio del micrófono frontal de Pepper."""
    channels = [0, 0, 1, 0]  # Solo micrófono frontal
    audioRecorder.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000, channels)
    time.sleep(listen_time)
    audioRecorder.stopMicrophonesRecording()

def transcribir_audio_file(audio_path, idioma="es-ES"):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        # Llamada al servicio de Google Speech Recognition
        texto = recognizer.recognize_google(audio_data, language=idioma)
        return texto
    except sr.UnknownValueError:
        return "[Inaudible: no se pudo reconocer el habla]"
    except sr.RequestError as e:
        return "[Error de servicio: {}]".format(e)
    except FileNotFoundError:
        return "[Error: archivo de audio no encontrado]"
    except Exception as e:
        return "[Error inesperado: {}]".format(e)
    audioRecorder.stopMicrophonesRecording()

def elegir_poema(frase):
    frase = frase.lower()
    poema = "No te he entendido bien"
    seguir = True
    if "dedos" in frase:
        poema = [
            "Poema épico",
            "Con los dedos de la mano.",
            "los dedos de los pies,",
            "los cohones y la pola,",
            "todo suma veintitres,"
        ]
        poema = "\\pau=800\\".join(poema)
        # Habilitar rigidez del brazo derecho
        motion.setStiffnesses("RArm", 1.0)

        # Movimiento del brazo derecho hacia el pecho
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, -0.3, 1.5, 1.0]  # ajustar si quieres un gesto diferente
        speed = 0.2
        motion.setAngles(names, angles, speed)

        speak(poema)

        time.sleep(2)
        motion.setStiffnesses("RArm", 0.0)

    if "coraza" in frase:
        poema = [
            "Corazón coraza",
            "Este poema expresa la dualidad del amor y la vulnerabilidad emocional.",
            "Porque te tengo y no,",
            "porque te pienso,",
            "porque la noche está de ojos abiertos,",
            "porque la noche pasa y digo amor,",
            "porque has venido a recoger tu imagen,",
            "y eres mejor que todas tus imágenes,"
        ]
        poema = "\\pau=800\\".join(poema)
        # Habilitar rigidez del brazo derecho
        motion.setStiffnesses("RArm", 1.0)

        # Movimiento del brazo derecho hacia el pecho
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, -0.3, 1.5, 1.0]  # ajustar si quieres un gesto diferente
        speed = 0.2
        motion.setAngles(names, angles, speed)

        speak(poema)

        time.sleep(2)
        motion.setStiffnesses("RArm", 0.0)

    if "salves" in frase:
        poema = [
            "No te salves,",
            "Un llamado a vivir plenamente y no conformarse.",
            "No te quedes inmóvil,",
            "al borde del camino,",
            "no congeles el júbilo,",
            "no quieras con desgana,",
            "no te salves ahora,",
            "ni nunca"
        ]
        poema = "\\pau=800\\".join(poema)
        # Activar rigidez en ambos brazos
        motion.setStiffnesses(["LArm", "RArm"], 1.0)

        # Definir articulaciones y ángulos
        names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
        ]
        angles = [
            0.5, 0.2, -1.0, -1.0,   # brazo izquierdo
            0.5, -0.2, 1.0, 1.0     # brazo derecho
        ]
        speed = 0.2

        # Ejecutar gesto
        motion.setAngles(names, angles, speed)

        # Esperar a que se complete el movimiento
        time.sleep(1)

        speak(poema)

        # (opcional) Relajar brazos después
        time.sleep(2)
        motion.setStiffnesses(["LArm", "RArm"], 0.0)

    if "trato" in frase:
        poema = [
            "Hagamos un trato,",
            "Un poema sobre la confianza y el compromiso mutuo.",
            "Compañera,",
            "usted sabe,",
            "puede contar,",
            "conmigo,",
            "no hasta dos,",
            "o hasta diez,",
            "sino contar,",
            "conmigo,",
            "si alguna vez,",
            "advierte,",
            "que la miro a los ojos,",
            "y una veta de amor,",
            "reconoce en los míos,",
            "no alerte sus fusiles,",
            "ni piense qué delirio,",
            "a pesar de la veta,",
            "o tal vez porque existe,",
            "usted puede contar,",
            "conmigo"
        ]
        poema = "\\pau=800\\".join(poema)
        motion.setStiffnesses(["LArm", "RArm"], 1.0)

        # Posición de "abrazo"
        names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
        ]
        angles = [
            1.0, 0.3, -1.5, -1.0,   # brazo izquierdo
            1.0, -0.3, 1.5, 1.0     # brazo derecho
        ]
        speed = 0.2

        # Mover brazos y hablar
        motion.post.setAngles(names, angles, speed)
        speak(poema)

        time.sleep(2)

        # Opcional: relajar brazos
        motion.setStiffnesses(["LArm", "RArm"], 0.0)

    if "oro" in frase:
        poema = [
            "Si el oro perdiera su color,",
            "Reflexión sobre la eternidad del amor más allá del tiempo y las circunstancias.",
            "Si la esmeralda se opacara,",
            "si el oro perdiera su color,",
            "entonces, se acabaría,",
            "nuestro amor"
        ]
        poema = "\\pau=800\\".join(poema)
        # Activar la rigidez del cuello
        motion.setStiffnesses("Head", 1.0)

        speak(poema)

        # Inclinación hacia abajo
        motion.setAngles("HeadPitch", 0.4, 0.2)  # 0.4 radianes ≈ cabeza mirando al pecho
        time.sleep(1)

        # Inclinación hacia arriba
        motion.setAngles("HeadPitch", -0.3, 0.2)  # -0.3 radianes ≈ cabeza mirando ligeramente hacia arriba
        time.sleep(1)

        # Volver al centro
        motion.setAngles("HeadPitch", 0.0, 0.2)
        time.sleep(1)

        # (Opcional) relajar la cabeza
        motion.setStiffnesses("Head", 0.0)

    if "casa" in frase:
        poema = [
            "Ésta es mi casa,",
            "Una introspección sobre el hogar y la existencia,",
            "No cabe duda. Ésta es mi casa,",
            "aquí sucedo, aquí,",
            "me engaño inmensamente.",
            "Ésta es mi casa detenida en el tiempo"
        ]
        poema = "\\pau=800\\".join(poema)
        motion.setStiffnesses("Head", 1.0)
        

        # Girar a la izquierda
        motion.setAngles("HeadYaw", 0.8, 0.2)  # 0.8 radianes ≈ 45 grados
        time.sleep(1)

        # Girar a la derecha
        motion.setAngles("HeadYaw", -0.8, 0.2)
        time.sleep(1)

        # Volver al centro
        motion.setAngles("HeadYaw", 0.0, 0.2)
        time.sleep(1)

        # Relajar la cabeza (opcional)
        motion.setStiffnesses("Head", 0.0)
        speak(poema)

    if "finalizar" in frase:
        seguir = False
    return seguir

def download_audio(remote_path, local_path):
    """Copia por SCP un archivo desde Pepper a tu PC."""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, 'nao', 'nao', allow_agent=False, look_for_keys=False)               # usuario y contraseña por defecto
        scp = SCPClient(ssh.get_transport())
        scp.get(remote_path, local_path)               # descarga el fichero
        scp.close()
    except paramiko.SSHException as e:
        print("Error de conexión SSH: {}".format(e))
    except Exception as e:
        print("Otro error: {}".format(e))
    ssh.close()

if __name__ == "__main__":
    motion.wakeUp()
    seguir = True
    audioRecorder.stopMicrophonesRecording()
    while seguir:
        posture.goToPosture("StandInit", 0.5)
        # 1) Pepper saluda
        speak("Hola, soy Pepper, ¿qué quieres que te recite?")
        # 2) Pepper graba 5 segundos de audio
        listen(5)
        # 3) Descargo el audio grabado a mi máquina local
        download_audio("/home/nao/test.wav", "pepper_audio.wav")
        print(":marca_de_verificación_blanca: Audio descargado localmente como pepper_audio.wav")
        resultado = transcribir_audio_file("pepper_audio.wav")
        print(resultado)
        seguir=elegir_poema(resultado)

    # Activar rigidez
    motion.setStiffnesses(["LArm", "RArm"], 1.0)

    # Configurar posiciones
    names = [
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"
    ]

    angles = [
        0.2, -0.1, 1.5, 1.0,     # Brazo derecho levantado
        1.4, 0.5, -1.5, -1.0     # Brazo izquierdo en jarras
    ]

    speed = 0.2

    # Ejecutar movimiento
    motion.setAngles(names, angles, speed)

    speak("Muchas gracias por escucharme hoy")

    # Esperar y relajar
    time.sleep(3)
    motion.setStiffnesses(["LArm", "RArm"], 0.0)
