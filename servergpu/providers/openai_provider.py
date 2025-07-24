import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from .base_provider import BaseProvider

# Load the API key from the .env file
load_dotenv()

class OpenAIProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.model = "gpt-4.1"
        self.max_tokens = 300
        self.temperature = 0
        self.top_p = 0.2
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        
    def generate_response(self, prompt: str, system_prompt: str = "", test: bool = False):
        """Generate an answer using the GPT model."""
        if test:
            return {
                "test": "test response"
            }
       
        user_inputs = [
            {"type": "text", "text": prompt},            
        ]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_inputs}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=self.temperature, # controls randomness
                max_completion_tokens=self.max_tokens, # controls response length)
                top_p=self.top_p, # controls diversity, adjusts probability distribution
                frequency_penalty=0, # affect repetition
                presence_penalty=0, # affect repetition                
            )

            chatgpt_response_json = response.choices[0].message.content.strip()
            return json.loads(chatgpt_response_json)

        except Exception as e:
            print(f"Ha ocurrido un error: {str(e)}")
            self.log_error(str(e))
            return "Error al generar respuesta, revisa el log de errores"