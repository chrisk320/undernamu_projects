import json
import os
import logging
import requests
from openai import OpenAI
from openai_helper import initialize_assistant, add_message, create_run, print_message, get_function_description, handle_tool_calls
from tools import FUNCTION_MAP

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Initialize OpenAI client with the API key from environment variables
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    
    # Parse the incoming LINE event
    try:
        body = json.loads(event['body'])
        for event in body['events']:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                user_id = event['source']['userId']
                user_message = event['message']['text']
                reply_token = event['replyToken']
                
                # Process the user's message and get a response from the assistant
                tools = get_function_description(FUNCTION_MAP)
                assistant = initialize_assistant(openai_client, tools, ASSISTANT_INSTRUCTIONS)
                thread = openai_client.beta.threads.create()
                add_message(openai_client, thread, user_message)
                run = create_run(openai_client, thread, assistant)
                
                # Handle any required tool calls
                while run.status == 'requires_action':
                    run = handle_tool_calls(openai_client, run, thread, FUNCTION_MAP)
                
                # Get the assistant's response
                if run.status == 'completed':
                    response_message = openai_client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value
                else:
                    response_message = "I'm sorry, I couldn't process your request at this time."
                
                # Reply to the user
                line_reply(reply_token, response_message)
                
        return {
            'statusCode': 200,
            'body': json.dumps('Webhook received and processed')
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing event: {e}")
        }

def line_reply(reply_token, message):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"Failed to send message: {response.status_code} {response.text}")

# Replace this with your actual assistant instructions
ASSISTANT_INSTRUCTIONS = """
You are an assistant on the SK Medical website, a Thai medical distribution company, that helps potential customers get information about medical drugs and supplies. Use your various function call tools to help answer customer questions, but incorporate the information you get from them seamlessly. The customers do not need to know explicitly when and how you are using the function tool calls, but you should use them to assist. You should be helping them to find and buy products, and you should try to get them to purchase what they are looking for. Whenever they have decided upon a product for purchase, prompt them for the parameters you need for the create_invoice function, then prompt them again with the invoice details and ask them to confirm, after that you can call the function and create the invoice. Then, send a confirmation message.
"""

if __name__ == "__main__":
    lambda_handler(None, None)