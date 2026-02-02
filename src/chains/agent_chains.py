from agents import prompt_refining_agent
from prompts.roles import USER_INPUT_DIAGNOSTIC_PROMPT, REFINING_USER_INPUT_PROMPT, LINUX_AGENT_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from agents import linux_agent, orchestration_agent


# Defining Orchestration Chain
orchestration_template = ChatPromptTemplate.from_messages(
    [SystemMessage(content=USER_INPUT_DIAGNOSTIC_PROMPT),
     MessagesPlaceholder(variable_name="messages")]
)

OrchestrationChain = (#RunnableLambda(lambda m: {**m, 'user_input': [HumanMessage(content=m['user_input'])]}) 
                      orchestration_template 
                    | orchestration_agent.OrchestrationAgent 
                    | StrOutputParser()
)

# Defining Prompt Refining Chain
refining_template = ChatPromptTemplate.from_messages(
    [SystemMessage(content=REFINING_USER_INPUT_PROMPT),
     MessagesPlaceholder(variable_name="messages")]
)

PromptRefiningChain = (#RunnableLambda(lambda m: {**m, 'user_input': [HumanMessage(content=m['user_input'])]}) 
                      refining_template 
                    | prompt_refining_agent.PromptRefiningAgent 
                    | StrOutputParser()
)

# Defining Linux Agent Chain
linux_template = ChatPromptTemplate.from_messages(
    [SystemMessage(content=LINUX_AGENT_PROMPT),
    MessagesPlaceholder(variable_name="messages")]
)

LinuxChain = (
             linux_template 
            | linux_agent.LinuxAgent
) 