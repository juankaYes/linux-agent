from langchain_ollama import ChatOllama, OllamaLLM

from llm_models.enums import ChatModels
from llm_models.info import ModelInfo


def factory_model(model_info: ModelInfo) :
    """Initialize and return an Ollama model."""
    model_type = type(model_info['model'])
    model_name = str(model_info.pop('model').value)
    
    if model_type.__name__ == ChatModels.__name__:
        return ChatOllama(model=model_name, **model_info)
    return OllamaLLM(model=model_name, **model_info)
