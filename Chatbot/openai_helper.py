def initialize_assistant(openai_client, tools: list, instructions: str) -> object:
    """
    Initializes the OpenAI assistant with the given tools and instructions.
    
    Args:
        openai_client: The OpenAI client instance.
        tools (list): List of tools for the assistant.
        instructions (str): Instructions for the assistant.
    
    Returns:
        object: The initialized assistant object.
    """
    return openai_client.beta.assistants.create(
        name="SK Medical Chatbot",
        instructions=instructions,
        tools=tools,
        model="gpt-4o",
    )

def add_message(openai_client, thread: object, user_input: str):
    """
    Adds a message to the thread.
    
    Args:
        openai_client: The OpenAI client instance.
        thread (object): The current thread object.
        user_input (str): The user's input message.
    """
    openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

def create_run(openai_client, thread: object, assistant: object) -> object:
    """
    Creates and polls a new run for the given thread and assistant.
    
    Args:
        openai_client: The OpenAI client instance.
        thread (object): The current thread object.
        assistant (object): The assistant object.
    
    Returns:
        object: The created run object.
    """
    return openai_client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

def print_message(openai_client, thread: object) -> None:
    """
    Prints the latest message from the thread.
    
    Args:
        openai_client: The OpenAI client instance.
        thread (object): The current thread object.
    """
    message = openai_client.beta.threads.messages.list(thread_id=thread.id)
    print("\n" + message.data[0].content[0].text.value + "\n")