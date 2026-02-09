from agents import orchestration_agent, troubleshooting_agent, teacher_agent
from prompts.roles import USER_INPUT_DIAGNOSTIC_PROMPT
from schemas.llm_output import parse_llm_output
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def print_anything(x):
    print(x)
    return x

OrchestrationChain = (
                    RunnableLambda(lambda m: {'messages': [HumanMessage(content=m)]}) 
                    | orchestration_agent.OrchestrationAgent 
                    | RunnableLambda(lambda x: [m for m in x['messages'] if isinstance(m, AIMessage)][0].content)
                    | parse_llm_output
)

TroubleshootingChain = (
            RunnableLambda(lambda m: {'messages': [HumanMessage(content=m)]})
            | troubleshooting_agent.TroubleshootingAgent
) 

TeacherChain = (
            RunnableLambda(lambda m: {'messages': [HumanMessage(content=m)]})
            | teacher_agent.TeacherAgent
)

CHAIN_AGENTS = {
    "orchestration": OrchestrationChain,
    "troubleshooting": TroubleshootingChain,
    "teaching": TeacherChain
}
