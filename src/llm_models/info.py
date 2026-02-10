
from typing import Optional, TypedDict
from pydantic import BaseModel, Field

from llm_models.enums import ChatModels, GeneralModels

class ModelInfo(TypedDict):
    model               : GeneralModels     = Field(GeneralModels.QWEN2_5, description="Name of the model")     # Specify the model name
    temperature         : Optional[float]   = Field(0.5, description="Temperature setting of the model")        # Validate model existence on initialization
    max_tokens          : Optional[int]     = Field(1000, description="Maximum tokens the model can generate")  # Adjust temperature for creativity 0: no creativity, 1: high creativity
    top_p               : Optional[float]   = Field(0.5, description="Nucleus sampling parameter")              # Adjust max tokens as needed
    top_k               : Optional[int]     = Field(50, description="Top-k sampling parameter")                 # Nucleus sampling parameter
    frequency_penalty   : Optional[float]   = Field(0, description="Frequency penalty setting")                 # Adjust frequency penalty to reduce repetition
    presence_penalty    : Optional[float]   = Field(0, description="Presence penalty setting")                  # Adjust presence penalty to encourage new topics
    stop                : Optional[list]    = Field(None, description="Stop sequences for the model")           # Define stop sequences if needed
    keep_alive          : Optional[str]     = Field(None, description="Keep the model instance alive")          # Keep the model instance alive for reuse

class ChatModelInfo(ModelInfo):
    model_name: ChatModels
    validate_model_on_init: Optional[bool]