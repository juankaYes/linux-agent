from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.utils import find_AI_messages, get_streaming_message, stream_agent
from chains.agent_chains import LinuxChain, PromptRefiningChain, OrchestrationChain
from langchain_core.messages import HumanMessage

class AgentState(TypedDict):
    user_input: str
    agent_input: Optional[str]
    prompt_type: Optional[str]
    response: Optional[str]


OrchestrationMapping = {
    "inconsistent": "fail_query",
    "consistent": "refining_prompt"
}

history = {'messages': []}

def orchestration(state: AgentState) -> AgentState:
    state['agent_input'] = state['user_input']
    response = OrchestrationChain.invoke({"messages": history['messages'] + [HumanMessage(content=state['user_input'])]})
    state['prompt_type'] = response
    return state

def fail_query(state: AgentState) -> AgentState:
    print("Sorry, thats not something I can help with.\n Please try again.")
    return state

def refining_prompt(state: AgentState) -> AgentState:
    response = PromptRefiningChain.invoke({"messages": history['messages'] + [HumanMessage(content=state['user_input'])]})
    print(response)
    state['agent_input'] = response
    return state

def reply(state: AgentState) -> AgentState:
    response = LinuxChain.stream({"messages": history['messages'] + [HumanMessage(content=state['agent_input'])]})
    for chunk in response:
        msg = find_AI_messages(chunk['messages'], start_index=-1)
        if msg:
            stream_agent(msg[0])

    print()  # for newline after streaming
    history['messages'].extend(chunk['messages'])
    state['response'] = get_streaming_message()
    return state

# Creating graph
workflow = StateGraph(AgentState)

# Adding nodes
# workflow.add_node('query', query)
workflow.add_node('orchestration', orchestration)
workflow.add_node('fail_query', fail_query)
workflow.add_node('refining_prompt', refining_prompt)
workflow.add_node('reply', reply)

# Adding edges
workflow.add_conditional_edges('orchestration', lambda x: x['prompt_type'], OrchestrationMapping)
workflow.add_edge("fail_query", END)
workflow.add_edge("refining_prompt", "reply")
workflow.add_edge("reply", END)

# Setting the entry point
workflow.set_entry_point('orchestration')

# Compiling the graph
app = workflow.compile()


