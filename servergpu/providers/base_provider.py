from abc import ABC, abstractmethod
import logging

class BaseProvider(ABC):
    """
    Abstract base class for AI providers.
    All providers must implement this interface.
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
        logging.basicConfig(filename='errores.log', level=logging.ERROR)
    
    def log_error(self, error: str):
        logging.error(error)
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        """
        Generate a response using the AI model.
        
        Args:
            prompt (str): The user's input/question
            system_prompt (str): System instructions for the AI
            **kwargs: Additional provider-specific parameters
            
        Returns:
            str: The AI's response
            
        Raises:
            Exception: If there's an error generating the response
        """
        pass
    
    
    def clean_response(self, response: str) -> str:
        """
        Clean and normalize the response text.
        This method can be overridden by specific providers if needed.
        
        Args:
            response (str): Raw response from the AI
            
        Returns:
            str: Cleaned response
        """
        if not response or response.strip() == '':
            return "Puedes repetir la pregunta"
        
        # Remove accents for text-to-speech compatibility
        result = response.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'ny')
        return result.strip()