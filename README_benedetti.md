# 🎙️ benedetti.py: Reciting Poetry with Pepper

The `benedetti.py` script allows you to interact with the **Pepper robot** by voice and have it **recite poems** by Mario Benedetti using expressive speech and gestures.

## ✨ How It Works

1. **Pepper listens** to your voice using its **frontal microphone**.
2. You say a **trigger word** like `"dedos"`, `"trato"`, `"coraza"`, `"salves"`, `"oro"` or `"casa"`.
3. Pepper interprets your request and performs a **poem recital** with **coordinated arm/head gestures**.
4. Pepper thanks you and optionally goes to rest mode after saying `"finalizar"`.

## 📋 Supported Triggers and Poems

| Trigger word | Poem title            | Description |
|--------------|------------------------|-------------|
| `dedos`      | Poema épico            | Humorístico gesto numérico |
| `coraza`     | Corazón coraza         | Amor y vulnerabilidad |
| `salves`     | No te salves           | Llamado a vivir intensamente |
| `trato`      | Hagamos un trato       | Confianza y compromiso |
| `oro`        | Si el oro perdiera...  | Amor eterno |
| `casa`       | Ésta es mi casa        | Reflexión existencial |
| `finalizar`  | —                      | Termina la sesión |

## ▶️ How to Run

1. Set the IP of your Pepper in the script:
   ```python
   ip = "192.168.1.82"
   ```
2. Run the script:
   ```bash
   python benedetti.py
   ```
3. Speak clearly into Pepper’s microphone.
4. The robot will record and interpret your speech, then perform the corresponding poem.

## 🛠️ Requirements

- **Python 2.7** (because of `naoqi`)
- Pepper SDK (`pynaoqi`)
- Packages: `speech_recognition`, `paramiko`, `scp`
- Pepper and your computer must be on the **same network**

## 💡 Notes

- The script uses **Pepper’s internal audio recorder** to capture `.wav` files.
- Files are transferred to your PC using `scp` via SSH (`nao`/`nao` credentials).
- The performance includes **synchronized gestures** (arms, head yaw/pitch) for expressivity.
