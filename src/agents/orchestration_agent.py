
from llm_models.enums import GeneralModels
from llm_models.factory import factory_model
from llm_models.info import ModelInfo

_model = ModelInfo(model=GeneralModels.QWEN2_5, tremperature=0.1) 
OrchestrationAgent = factory_model(model_info=_model)

