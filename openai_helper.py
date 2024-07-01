import ast
import importlib

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

def add_message(openai_client, thread: object, user_input: str) -> None:
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
    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages.data[0].content[0].text.value
    print(f"\n{latest_message}\n")

def get_function_description(function_map: dict) -> list:
    """
    Provides the description and parameters for the tool call functions.
    
    Args:
        function_map (dict): A dictionary containing function names, descriptions, parameters, and required parameters.
    
    Returns:
        list: A list containing the function descriptions and parameters.
    """
    tool_objects = []
    for function_name, function_details in function_map.items():
        tool_objects.append({
            "type": "function",
            "function": {
                "name": function_name,
                "description": function_details["description"],
                "parameters": {
                    "type": "object",
                    "properties": function_details["parameters"],
                    "required": function_details["required"]
                }
            }
        })
    return tool_objects

def handle_tool_calls(openai_client, run: object, thread: object, function_map: dict) -> object:
    """
    Handles tool calls by extracting arguments and executing the corresponding function.
    
    Args:
        openai_client: The OpenAI client instance.
        run (object): The current run object.
        thread (object): The current thread object.
        function_map (dict): A dictionary containing function names, descriptions, parameters, and required parameters.
    
    Returns:
        object: Updated run object after processing tool calls.
    """
    tool_outputs = []
    
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        function_name = tool.function.name
        if function_name in function_map:
            argument_dictionary = ast.literal_eval(tool.function.arguments)
            function_details = function_map[function_name]
            argument_keys = function_details["parameters"].keys()
            arguments = [argument_dictionary.get(arg) for arg in argument_keys]
            
            # Dynamically import the function from the tools module
            module = importlib.import_module("tools")
            func = getattr(module, function_name)
            
            # Call the function and store the output
            try:
                output = func(*arguments)
            except Exception as e:
                output = str(e)

            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": output
            })
    
    if tool_outputs:
        try:
            run = openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        except Exception as e:
            print(f"Failed to submit tool outputs: {e}")
    
    return run
