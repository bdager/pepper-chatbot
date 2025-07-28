import os
from google import genai
from google.genai import types
from .base_provider import BaseProvider
from dotenv import load_dotenv

load_dotenv()

class GeminiProvider(BaseProvider):
    """
    Gemini AI provider implementation.
    """
    
    def __init__(self):
        super().__init__()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.default_model = "gemini-2.5-flash-lite"
    
    def generate_response(self, prompt: str, system_prompt: str = "", model: str = None, **kwargs) -> str:
        """
        Generate a response using Gemini model.
        
        Args:
            prompt (str): The user's input/question
            system_prompt (str): System instructions for the AI
            model (str): Specific model to use (optional)
            **kwargs: Additional Gemini-specific parameters
            
        Returns:
            str: The AI's response
            
        Raises:
            Exception: If there's an error generating the response
        """
        try:
            model_to_use = model or self.default_model
            
            # Define the grounding tool
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )
            
            # Build configuration
            config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                ),
                tools=[grounding_tool],
                response_mime_type="text/plain",
            )
            
            # Add system instruction if provided
            if system_prompt:
                config.system_instruction = system_prompt
            
            response = self.client.models.generate_content(
                model=model_to_use,
                contents=prompt,
                config=config
            )
            
            if not response or not response.text:
                return "Error: No se pudo generar una respuesta"
            
            return self.clean_response(response.text)
            
        except Exception as e:
            print(f"Error al generar respuesta con Gemini: {e}")
            self.log_error(str(e))
            return "Error al procesar la solicitud de IA, revisa el log de errores"