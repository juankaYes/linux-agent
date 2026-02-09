
from llm_models.enums import ChatModels
from llm_models.factory import factory_model
from llm_models.info import ModelInfo
from langchain.agents import create_agent
from memory.agents_memory import OrchestrationAgentMemory
from prompts.roles import USER_INPUT_DIAGNOSTIC_PROMPT
from schemas.llm_output import LLMOrchestrationOutput
from langchain_core.messages import SystemMessage

_model = ModelInfo(model=ChatModels.QWEN2_5, tremperature=0) 
OrchestrationModel = factory_model(model_info=_model)

OrchestrationAgent = create_agent(model=OrchestrationModel, 
                                  checkpointer=OrchestrationAgentMemory,
                                #   response_format=LLMOrchestrationOutput,
                                  system_prompt=SystemMessage(USER_INPUT_DIAGNOSTIC_PROMPT),
                                  
                                  )

