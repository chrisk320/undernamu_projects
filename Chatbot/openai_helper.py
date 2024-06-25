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

def add_message(openai_client, thread: object, user_input: str) -> object:
    """
    Adds a message to the thread.
    
    Args:
        openai_client: The OpenAI client instance.
        thread (object): The current thread object.
        user_input (str): The user's input message.
    
    Returns:
        object: The created message object.
    """
    return openai_client.beta.threads.messages.create(
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

def handle_tool_call(openai_client, run: object, thread: object) -> object:
    """
    Handles tool calls by extracting arguments and executing the corresponding function.
    
    Args:
        openai_client: The OpenAI client instance.
        run (object): The current run object.
        thread (object): The current thread object.
    
    Returns:
        object: Updated run object after processing tool calls.
    """
    from tools import get_product_info_by_criteria
    import ast

    tool_outputs = []
    
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_product_info_by_criteria":
            argument_dictionary = ast.literal_eval(tool.function.arguments)
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": get_product_info_by_criteria(
                    argument_dictionary.get('product_name'),
                    argument_dictionary.get('min_price'),
                    argument_dictionary.get('max_price'),
                    argument_dictionary.get('category'),
                    argument_dictionary.get('reference'),
                    argument_dictionary.get('in_stock')
                )
            })
    
    if tool_outputs:
        try:
            run = openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
    
    return run
