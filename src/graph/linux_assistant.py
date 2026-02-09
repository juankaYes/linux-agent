from langgraph.graph import StateGraph, END
from agents.utils import find_AI_messages, get_streaming_message, stream_agent
from chains.agent_chains import CHAIN_AGENTS
from states.agents import AgentState
from my_logging.config import get_logger
from memory.configuration import config
logger = get_logger(__name__)

def orchestration(state: AgentState) -> AgentState:
    logger.info(f"Received user input: {state['user_input']}")
    response = CHAIN_AGENTS["orchestration"].invoke(state['user_input'])
    logger.info(response)
    state['intent'] = response.intent
    state['needs_clarification'] = response.needs_clarification
    state['cleaned_query'] = response.cleaned_query
    return state

def fail_query(state: AgentState) -> AgentState:
    logger.info(f"Failed to determine intent for user input: {state['user_input']}")
    state['response'] = "Your query seems a bit unclear. Could you please provide more details?"
    print(state['response'])
    return state

def reply(state: AgentState) -> AgentState:
    logger.info(f"Current state at 'reply' func:\n {state}")
    response = CHAIN_AGENTS[state['intent']].stream(state['cleaned_query'], config=config[state['intent']])
    for chunk in response:
        print(chunk)
        msg = find_AI_messages(chunk['model']['messages'], start_index=-1)
        if msg:
            stream_agent(msg[0])

    print()  # for newline after streaming
    state['response'] = get_streaming_message()
    logger.info(f"Final response for user input '{state['user_input']}': {state['response']}")
    return state

def format_reply(state: AgentState) -> AgentState:
    # This function can be used to format the final response if needed
    return state

# Creating graph
workflow = StateGraph(AgentState)

# Adding nodes
# workflow.add_node('query', query)
workflow.add_node('orchestration', orchestration)
workflow.add_node('fail_query', fail_query)
workflow.add_node('reply', reply)
workflow.add_node('format_reply', format_reply)
# Adding edges
workflow.add_conditional_edges('orchestration', lambda x: x['needs_clarification'], {False: 'reply', True: 'fail_query'})
workflow.add_edge("fail_query", END)
workflow.add_edge("reply", "format_reply")
workflow.add_edge("format_reply", END)

# Setting the entry point
workflow.set_entry_point('orchestration')
# from memory.agents_memory import GraphMemory
# Compiling the graph
# app = workflow.compile(checkpointer=GraphMemory)
app = workflow.compile()

