# Instrucciones para ejecutar el código del servidor

## Crear y configurar venv (entorno de python)

Crear entorno

```bash
python -m venv .venv
```

Usar entorno

```bash
. .venv/bin/activate
```

Instalar las dependencias del archivo requirements.txt

```bash
pip install -r requirements.txt
```

## 🔑 Configurar Variables de Entorno

Para configurar las claves API de los diferentes proveedores de IA:

1. **Duplicar el archivo de ejemplo** (situado en /providers):
   ```bash
   cp .env.example .env
   ```

2. **Editar el archivo `.env`** con tus claves API:
   ```bash
   # Gemini AI Provider
   GEMINI_API_KEY="tu_clave_api_de_gemini_aqui"
   
   # OpenAI Provider
   OPENAI_API_KEY="tu_clave_api_de_openai_aqui"
   
   # Otros providers...
   ```

3. **Verificar que el archivo `.env` esté en `.gitignore`** para mantener tus claves seguras.

> ⚠️ **Importante**: Nunca compartas tus claves API públicamente. El archivo `.env` debe mantenerse privado.

## 📖 Uso

### Endpoint Principal

```
GET /procesar_recibir_respuesta?provider=gemini&personalidad=1
```

**Parámetros:**

-   `provider` (requerido): Nombre del provider (`gemini`, `openai`)
-   `personalidad` (opcional): ID de personalidad (1-4, default: 4)
-   `archivo` (opcional): Archivo de audio (default: test.wav)

### Endpoints Informativos

-   `GET /` - Información completa del sistema

### Ejemplos de Uso

```bash
# Usar Gemini con de cuidador de ancianos
curl "http://localhost:5000/procesar_recibir_respuesta?provider=gemini&personalidad=1"

# Usar personalidad de cuidador de niños
curl "http://localhost:5000/procesar_recibir_respuesta?provider=gemini&personalidad=2"
```

## 🎭 Personalidades Disponibles

1. **Pepper Cuidador de Ancianos**: Asistente calmado, paciente y empático para personas mayores
2. **Pepper Cuidador de Niños**: Amigo robótico, curioso y juguetón para niños
3. **Pepper Profesor de Secundaria**: Asistente educativo formal y motivador para estudiantes
4. **Pepper Personalidad Neutra**: Robot asistente neutro, servicial y directo

## 🔌 Agregar Nuevos Providers

1. Crear clase heredando de `BaseProvider`:

```python
# providers/mi_provider.py
from .base_provider import BaseProvider

class MiProvider(BaseProvider):
    def generate_response(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        # Tu implementación aquí
```

2. Registrar en `providers/__init__.py`:

```python
from .mi_provider import MiProvider

providers = {
    'gemini': GeminiProvider,
    'mi_provider': MiProvider,  # Agregar aquí
}
```

## 🎨 Agregar Nuevas Personalidades

Editar `personalities.json`:

```json
{
    "6": {
        "name": "Mi Nueva Personalidad",
        "system_prompt": "Tu system prompt personalizado aquí..."
    }
}
```

## Manejo de errores

Si hay algun error al ejecutar un provider se guardará dicho error en un archivo autogenerado llamado `errores.log`