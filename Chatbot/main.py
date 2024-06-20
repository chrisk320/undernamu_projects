from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message, handle_tool_call
from tools import get_function_description

# Assistant instructions
ASSISTANT_INSTRUCTIONS = (
    "You are an assistant on the SK Medical website, a Thai medical distribution company, "
    "that helps potential customers get information about medical drugs and supplies."
)

def main() -> None:
    """
    Main function to run the assistant, interact with the user, and handle tool calls.
    """
    # Initialize OpenAI client
    openai_client = OpenAI()

    tools = get_function_description()
    assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
    thread = openai_client.beta.threads.create()

    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            break
        
        message = add_message(openai_client, thread, user_input)
        run = create_run(openai_client, thread, assistant)

        if run.status == 'requires_action':
            run = handle_tool_call(openai_client, run, thread)
        
        if run.status == 'completed':
            print_message(openai_client, thread)
        else:
            print(run.status)

if __name__ == "__main__":
    main()
