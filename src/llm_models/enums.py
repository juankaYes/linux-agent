from enum import Enum

class GeneralModels(Enum):
    QWEN2_5 = "qwen2.5"
    LLaMA3 = "llama3"
    TINY_LLAMA = "tinyllama"
    LLAMA3_2_1B = "llama3.2:1b"

class ChatModels(Enum):
    QWEN2_5 = "qwen2.5"
    
class VisionModels(Enum):
    LLAMA3_2 = "llama3.2-vision"