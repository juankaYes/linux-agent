from common.messages.terminal_messages import goodbye

if __name__ == "__main__":
    from graph.linux_assistant import app
    from graph.linux_assistant import AgentState

    while True:
        user_input = input("Enter your request for the linux system (/bye to exit): ")
        if user_input.strip().lower() == "/bye":
            break
        state = AgentState(user_input=user_input)
        state = app.invoke(input=state)
        # print(state)
    print("Linux Assistant session ended.\n", goodbye)