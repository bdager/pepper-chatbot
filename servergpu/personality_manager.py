import json
import os
from typing import Dict, Optional

class PersonalityManager:
    """
    Clase para manejar las personalidades de la IA
    """
    
    def __init__(self, personalities_file: str = "personalities.json"):
        self.personalities_file = personalities_file
        self._personalities = None
        self._load_personalities()
    
    def _load_personalities(self):
        """
        Carga las personalidades desde el archivo JSON.
        """
        if os.path.exists(self.personalities_file):
            with open(self.personalities_file, 'r', encoding='utf-8') as file:
                self._personalities = json.load(file)
        else:
            # Error al cargar las personalidades
            raise FileNotFoundError(f"El archivo de personalidades {self.personalities_file} no existe")
    
    def get_personality(self, personality_id: str) -> Optional[Dict]:
        """
        Obtiene la configuración de la personalidad por ID.
        
        Args:
            personality_id (str): ID de la personalidad
            
        Returns:
            Optional[Dict]: Configuración de la personalidad (name, system_prompt) o (None, None) si no se encuentra
        """
        return self._personalities.get(str(personality_id), (None,None))
    
    def get_available_personalities(self) -> Dict:
        """
        Obtiene todas las personalidades disponibles.
        
        Returns:
            Dict: Todas las personalidades con el formato {id: {name: str, system_prompt: str}}
        """
        return self._personalities.copy()

if __name__ == "__main__":
    pm = PersonalityManager()
    print(pm.get_personality(10))