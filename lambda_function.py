import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message
from tools import get_function_description, handle_tool_calls

# LINE Bot credentials from environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# OpenAI Assistant instructions
ASSISTANT_INSTRUCTIONS = (
    "You are an assistant on the SK Medical website, a Thai medical distribution company, "
    "that helps potential customers get information about medical drugs and supplies."
)
INITIAL_PROMPT = "Introduce yourself and explain your capabilities to the user."

# Initialize OpenAI client and assistant
openai_client = OpenAI()
tools = get_function_description()
assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
thread = openai_client.beta.threads.create()

# Initial message to OpenAI assistant
add_message(openai_client, thread, INITIAL_PROMPT)
run = create_run(openai_client, thread, assistant)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    signature = event['headers']['x-line-signature']
    handler.handle(body, signature)
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # Send the user message to the OpenAI assistant
    add_message(openai_client, thread, user_message)
    run = create_run(openai_client, thread, assistant)
    
    if run.status == 'requires_action':
        run = handle_tool_calls(openai_client, run, thread)
    
    if run.status == 'completed':
        response_message = print_message(openai_client, thread)
    else:
        response_message = "I'm sorry, I couldn't process your request."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )
