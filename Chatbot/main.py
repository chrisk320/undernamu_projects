from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message
from tools import get_function_description, handle_tool_calls

# Assistant instructions
ASSISTANT_INSTRUCTIONS = (
    "You are an assistant on the SK Medical website, a Thai medical distribution company, "
    "that helps potential customers get information about medical drugs and supplies."
)
INITIAL_PROMPT = "Introduce yourself and explain your capabilities to the user."


def main() -> None:
    """
    Main function to run the assistant, interact with the user, and handle tool calls.
    """
    # Initialize OpenAI client
    openai_client = OpenAI()

    tools = get_function_description()
    assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
    thread = openai_client.beta.threads.create()

    #intial message
    add_message(openai_client, thread, INITIAL_PROMPT)
    run = create_run(openai_client, thread, assistant)

    if run.status == 'requires_action':
        run = handle_tool_calls(openai_client, run, thread)
    
    if run.status == 'completed':
        print_message(openai_client, thread)
    else:
        print(run.status)

    #prompt-response loop
    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            break
        
        add_message(openai_client, thread, user_input)
        run = create_run(openai_client, thread, assistant)

        if run.status == 'requires_action':
            run = handle_tool_calls(openai_client, run, thread)
        
        if run.status == 'completed':
            print_message(openai_client, thread)
        else:
            print(run.status)

if __name__ == "__main__":
    main()
