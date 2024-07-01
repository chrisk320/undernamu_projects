import os
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message, get_function_description, handle_tool_calls
from tools import FUNCTION_MAP

# Retrieve credentials from environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# OpenAI Assistant instructions
ASSISTANT_INSTRUCTIONS = ('''
    You are an assistant on the SK Medical website, a Thai medical distribution company, 
    that helps potential customers get information about medical drugs and supplies.
    Use your various function call tools to help answer customer's questions, but incorporate the information you get from them seamlessly.
    The customers do not need to know explicitly when and how you are using the function tool calls, but you should use them to assist.
    You should be helping them to find and buy products, and you should try to get them to purchase what they are looking for.
    Whenever they have decided upon a product for purchase, prompt them for the parameters you need for the create_invoice function, then prompt them again
    with the invoice details and ask them to confirm, after that you can call the function and create the invoice. Then, send a confirmation message.
''')
INITIAL_PROMPT = '''
    Greet the customer and briefly explain your capabilities, including your ability to help them search for products, compare them, and help them make a purchase.
'''

# Initialize OpenAI client and assistant
openai_client = OpenAI()
tools = get_function_description(FUNCTION_MAP)
assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
thread = openai_client.beta.threads.create()

# Send initial message
add_message(openai_client, thread, INITIAL_PROMPT)
run = create_run(openai_client, thread, assistant)

# Handle initial tool calls if required
while run.status == 'requires_action':
    run = handle_tool_calls(openai_client, run, thread, FUNCTION_MAP)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    signature = event['headers'].get('x-line-signature', '')

    # Validate the signature
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 403,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization'
            },
            'body': json.dumps('Invalid signature')
        }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        },
        'body': json.dumps('OK')
    }

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # Send the user message to the OpenAI assistant
    add_message(openai_client, thread, user_message)
    run = create_run(openai_client, thread, assistant)

    # Handle tool calls if required
    while run.status == 'requires_action':
        run = handle_tool_calls(openai_client, run, thread, FUNCTION_MAP)

    # Get the response message
    if run.status == 'completed':
        response_message = print_message(openai_client, thread)
    else:
        response_message = "I'm sorry, I couldn't process your request."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )
