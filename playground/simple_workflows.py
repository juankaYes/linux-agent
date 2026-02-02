from langchain_ollama import OllamaLLM, ChatOllama
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.tools import tool
import subprocess


orchestration_prompt = """
You are an orchestration agent.

Your task is to decide which tool must be executed to fulfill the user's request.
Make sure the format is a valid command, with spaces between command, options and arguments.
Be careful with interactive commands, use flags to make them non-interactive.
Remember you don't have sudo permissions

Rules:
- You must NOT generate any type of content.
- You must ONLY produce tool calls.
- You must NOT use writing operations.
- If no tool is needed, produce an empty response.

User Request: {query}
"""

agent_prompt = """
You are expert linux assistant terminal. 

Your task is to decide which tool must be executed to fulfill the user's request
by troubleshooting the linux system, or providing relevant information.
Make sure the command's formats are valid, with spaces between command, options and arguments.
In order to provide accurate information to the user, you must first know which Operating System is running.
Execute as many commands as needed to fulfill the user's request.

Once the commands are executed, analyze the results and provide a summary, explanations and next steps if any.
In case is needed to execute more commands, do it.
In case of writing operations, you will suggeste to the user to execute them and why you suggest it.

Rules:
- Use flags to make interactive commands non-interactive.
- You don't have sudo permissions.
- Always reply in english, no chinese.
"""

analyzer_prompt = """
You are an analysis agent.
Your task is to analyse the result of commands executed on a linux system.
Summarize the important parts of the results, explain them and give next steps if any.
Reply in english, no chinese.
Analyze the following command results:
{tools_results}
"""

@tool
def run_command_tool(command: str) -> str:
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e}"
    
tools = [run_command_tool]
tools_graph = {tool.name: tool for tool in tools}

# Simple LLM Chain that takes user input, generates tool calls, executes them and analyzes the results
def simple_llm_chain(user_input):
        
    template = PromptTemplate.from_template(orchestration_prompt)
    messages = [SystemMessage(content=orchestration_prompt),
                HumanMessage(content="Check the disk usage and memory status of the system.")]
    llm = ChatOllama(model="qwen2.5")

    # ORchestration chain
    orchestration_template = ChatPromptTemplate.from_template(orchestration_prompt)
    orchestration_llm = llm.bind_tools(tools)
    orchestration_chain = orchestration_template | orchestration_llm # 1st chain -> generates tool calls

    response = orchestration_chain.invoke(user_input)

    # Executor - execute tool calls
    tools_responses = []
    for tool_call in response.tool_calls:
        tools_responses.append(tools_graph[tool_call['name']].invoke(tool_call['args']['command']))

    # Analyzer chain
    template = PromptTemplate.from_template(analyzer_prompt)
    analyzer_llm = OllamaLLM(model="qwen2.5")

    analyzer_chain = template | analyzer_llm # 2nd chain -> analyzes tool results
    response = analyzer_chain.stream(input={"tools_results": '\n'.join(tools_responses)})

    for chunk in response:
        print(chunk, end="", flush=True)


#TODO add history and save it to a file
# history = []  # List to store the conversation history
# history.append(HumanMessage(content=user_input))
# history.append(response)
# with open("conversation_history.json", "w") as f:
#     json.dump([msg.model_dump() for msg in history], f, indent=4])

# Using Runnables
from langchain_core.runnables import RunnablePassthrough, Runnable


# Runable to parse first LLM output and execute the tools
class ExecutorRunnable(Runnable):
    def invoke(self, input, config):
        print("\n\n--- ORCHESTRATION RUNNABLE ---\n")
        print("User Input:", input)
        # print("Config:", config)
        tools_result = []
        for tool_call in input.tool_calls:
            tools_result.append(tools_graph[tool_call['name']].invoke(tool_call['args']['command']))

        return {'tools_results': '\n'.join(tools_result)}

# Simple Runnable that chains everything together
def runnable(user_input):
    llm = ChatOllama(model="qwen2.5")
    orchestration_llm = llm.bind_tools(tools)
    analyzer_llm = OllamaLLM(model="qwen2.5")

    analyzer_template = PromptTemplate.from_template(analyzer_prompt)
    orchestration_template = ChatPromptTemplate.from_template(orchestration_prompt)
    linux_assistant = (   orchestration_template 
                        | orchestration_llm
                        | ExecutorRunnable() 
                        | analyzer_template 
                        | analyzer_llm
                        )

    response = linux_assistant.stream(user_input)
    for chunk in response:
        print(chunk, end="", flush=True)
    print()

def agent(user_input):
    llm = ChatOllama(model="qwen2.5")
    agent = create_agent(model=llm, tools=tools)
    template = ChatPromptTemplate.from_messages([
        SystemMessage(content=agent_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    agent = template | agent
    response = agent.invoke(input={'messages':[HumanMessage(content=user_input)]})
    
    agent = create_agent()
    for msg in response['messages']:
        if isinstance(msg, AIMessage):
            print("AI:", msg.content)

# from pydantic import BaseModel, Field

# class Answer(BaseModel):
#     title: str = Field(..., description="Title of the answer")
#     confidence: float = Field(..., description="Confidence level of the answer")
#     reasoning: str = Field(..., description="Reasoning behind the answer")

# class CommandOutput(BaseModel):
#     command: str = Field(..., description="The command that was executed")
#     result: str = Field(..., description="The output of the command")
#     is_error: bool = Field(..., description="Indicates if the command failed")
#     reason_if_error: str = Field(None, description="Reason for the error if any")

# Building: Not working yet
def agent_structured_output(user_input):
    llm = ChatOllama(model="qwen2.5")
    agent = create_agent(model=llm, tools=tools)
    template = ChatPromptTemplate.from_messages([
        SystemMessage(content=agent_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    agent = template | agent
    response = agent.invoke(input={'messages':[HumanMessage(content=user_input)]})
    llm = llm.with_structured_output(CommandOutput)
    template = ChatPromptTemplate.from_messages([
        SystemMessage(content="Summarize the conversation in a structured format."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    agent = template | llm
    response = agent.invoke(input={'messages': response['messages']})

    print("\n\nSTRUCTURED OUTPUT:\n")
    print(response)


from pydantic import BaseModel, Field
if __name__ == "__main__":
    from time import time
    user_input = input("Enter your request for the linux system: ")
    print("\n\n--- SIMPLE LLM CHAIN ---\n")
    start_time = time()
    simple_llm_chain(user_input)
    print("Time taken for SIMPLE LLM CHAIN:", time() - start_time)
    print("\n\n--- RUNNABLE CHAIN ---\n")
    start_time = time()
    runnable(user_input)
    print("Time taken for RUNNABLE CHAIN:", time() - start_time)
    print("\n\n--- AGENT ---\n")
    start_time = time()
    agent(user_input)
    print("Time taken for AGENT:", time() - start_time)
    # print("\n\n--- AGENT ---\n")
    # agent_structured_output(user_input)