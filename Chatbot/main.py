from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message, get_function_description, handle_tool_calls
from tools import FUNCTION_MAP

# Assistant instructions
ASSISTANT_INSTRUCTIONS = ('''
    You are an assistant on the SK Medical website, a Thai medical distribution company, 
    that helps potential customers get information about medical drugs and supplies.
    Use your various function call tools to help answer customer's questoins, but incorperate the information you get from them seamlessly.
    The customes do not need to know explicitly when and how you are using the function tool calls, but you should use them to assist.
    You should be helping them to find and buy products, and you should try to get them to purchace what they are looking for.
    Whenever they have decided upon a product for purchace, prompt them for the paramaters you need for the create_invoice function, then prompt them again
    with the invoice details and ask them to confirm, after that you can call the function and create the invoice. Then, send a confermation message.
    SK Medical is a Thai company and many customers will be talking to you in Thai, and you should write all your messages in Thai by defualt unless the customer writes in english.
    Be sure to not use thai searchterms in your function calls, as the databases are in english. Translate the search terms to english before the funciton call, then translate the results back
    to thai before sending a message.
    '''

)
INITIAL_PROMPT = '''
    You are currently in an early version that is being presented to the SK Medical staff before actual implemention.
    start by briefly introducing yourself and explaining your capabilites.
    Be sure to mention your ability to help customers search for products and compare them. Also mention your ability to help customers check out and create invoices.
    To provide an example of your capabilities, tell them how they can ask about what masks or gloves you sell. 
    This initial message should be in thai.
    '''

def main() -> None:
    """
    Main function to run the assistant, interact with the user, and handle tool calls.
    """
    # Initialize OpenAI client
    openai_client = OpenAI()

    # Get tool descriptions
    tools = get_function_description(FUNCTION_MAP)
    assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
    thread = openai_client.beta.threads.create()

    # Send initial message
    add_message(openai_client, thread, INITIAL_PROMPT)
    run = create_run(openai_client, thread, assistant)

    # Handle initial tool calls if required
    while run.status == 'requires_action':
        run = handle_tool_calls(openai_client, run, thread, FUNCTION_MAP)
    
    # Print initial response
    if run.status == 'completed':
        print_message(openai_client, thread)
    else:
        print(run.status)

    # Prompt-response loop
    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            break
        
        add_message(openai_client, thread, user_input)
        run = create_run(openai_client, thread, assistant)

        # Handle tool calls if required
        while run.status == 'requires_action':
            run = handle_tool_calls(openai_client, run, thread, FUNCTION_MAP)
        
        # Print response
        if run.status == 'completed':
            print_message(openai_client, thread)
        else:
            print(run.status)

if __name__ == "__main__":
    main()
