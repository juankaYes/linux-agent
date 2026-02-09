
from llm_models.enums import ChatModels
from llm_models.factory import factory_model
from llm_models.info import ModelInfo
from langchain.agents import create_agent
from commands.tools.run_command import run_command_tool
from commands.tools.system_info import get_system_info_tool
from prompts.roles import LINUX_AGENT_PROMPT
from memory.agents_memory import TroubleshootingAgentMemory
from langchain_core.messages import SystemMessage


_model = ModelInfo(model=ChatModels.QWEN2_5, keep_alive="1h") 
tools = [run_command_tool, get_system_info_tool]
llm = factory_model(model_info=_model)
TroubleshootingAgent = create_agent(model=llm, 
                                    tools=tools, 
                                    checkpointer=TroubleshootingAgentMemory,
                                    system_prompt=SystemMessage(LINUX_AGENT_PROMPT)
                                    )
