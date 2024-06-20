# undernamu_projects

Update: Got the assistant working and it is able to call the openFDA tool function. I separated the code into a few files and added comments. I also created a virtual environment for the dependencies.

Instructions for terminal (cd into Chatbot first):

1. Activate the virtual environment

    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Run the chatbot

    ```
    python3 main.py
    ```

File Structure:

- `main.py`  
  This is the main entry point of the project. It initializes the OpenAI client, sets up the assistant, and handles user interaction in a loop.
  
- `openai_helper.py`  
  This module contains helper functions for interacting with the OpenAI API, including functions to initialize the assistant, add messages, create runs, print messages, and handle tool calls.
  
- `tools.py`  
  This module contains functions for interacting with the openFDA API, including the function to search the openFDA registration listing endpoint and get function descriptions. Any more functions we want the chatbot to have access to will be added in here.

To-do:

- Make sure the openfda functions work properly and fix the parameter descriptions to be necessary and correct
- Integrate Thai FDA documents
- Add Odoo API function calls
