import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load the API key from the .env file
load_dotenv()


system_prompt = """
Your task is to answer friendly the question of the user in a JSON format output.
In the case the user is asking your name, you should answer "Pepper".

Example of the JSON format output:
{'respuesta': 'Hola, ¿en qué puedo ayudarte hoy?'}
"""


class GPTDescriptor:
    def __init__(self, model="gpt-4.1", max_tokens=300, temperature=0,
                 top_p=0.2):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        
    def generate_answer(self, user_query, test=False):
        """Generate an answer using the GPT model."""
        if test:
            return {
                "test": "test response"
            }
       
        user_inputs = [
            {"type": "text", "text": user_query},            
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
            print(f"An error occurred decoding chatgpt json response: {str(e)}")
