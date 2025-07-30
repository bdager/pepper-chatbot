from .base_provider import BaseProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider

# Registry of available providers
AVAILABLE_PROVIDERS = {
    'gemini': GeminiProvider,
    'openai': OpenAIProvider,
}

def get_provider(provider_name: str) -> BaseProvider:
    """
    Factory function to get the appropriate provider instance.
    
    Args:
        provider_name (str): Name of the provider ('gemini', 'openai', etc.)
        
    Returns:
        BaseProvider: Instance of the requested provider
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider_name.lower() not in AVAILABLE_PROVIDERS:
        available_providers = ', '.join(AVAILABLE_PROVIDERS.keys())
        raise ValueError(f"Provider '{provider_name}' no soportado. Providers disponibles: {available_providers}")
    
    return AVAILABLE_PROVIDERS[provider_name.lower()]()

def get_available_providers():
    """
    Get list of available providers.
    
    Returns:
        list: List of available provider names
    """
    return list(AVAILABLE_PROVIDERS.keys())