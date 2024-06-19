from openai import OpenAI

# Initialize OpenAI client and define model
OPENAI_CLIENT = OpenAI()
ASSISTANT_INSTRUCTIONS = "You are an assistant on the SK Medical website, a Thai medical distribution company,that helps potential customers get information about medical drugs and supplies."

def search_openFDA_registrationlisting(search_field, search_term, limit):
    url = f"https://api.fda.gov/device/registrationlisting.json?api_key={API_KEY}&search={search_field}:{search_term}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(url)
        return None

def get_function_description():   
    return [
        {
        "type": "function",
        "function": {
            "name": "search_openFDA_registrationlisting",
            "description": '''
                Function Explination:
         The API returns individual results as JSON by default. The JSON object has two sections:
            meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
            results: An array of matching results, dependent on which endpoint was queried.
             understanding the output: 
        For search queries, the results section includes matching SPL reports returned by the API.
        Each SPL report consists of these major sections:
            Standard SPL fields, including unique identifiers.
            Product-specific fields, the order and contents of which are unique to each product.
            An openfda section: An annotation with additional product identifiers, such as UPC and brand name, of the drug products listed in the labeling.
                ''',
            "parameters": {
            "type": "object",
            "properties": {
                "search_field": {
                "type": "string",
                "description": '''search_field peramater explination:
        If you don't specify a field to search, the API will search in every field.
        Harmonization: 
            Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
            openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
            Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openfda sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
            Exaustive list of harmonized fields for the registration and listing endpoint:
                regulation_number
                device_name
                device_class
                medical_specialty_description
                k_number
                pma_number
                    '''
                },
                "search_term": {
                "type": "string",
                "description": '''
                    search_term perameter explination:
        To search for records containing a word, search_term should be set to that word as a string
        Advanced syntax:
            Spaces: Queries use the plus sign + in place of the space character. Wherever you would use a space character, use a plus sign instead.
            Grouping: To group several terms together, use parentheses ( ) and +OR+ or +AND+.
            Wildcard search: Wildcard queries return data that contain terms matching a wildcard pattern. A wildcard operator is a placeholder that matches one or more characters. At this point, openFDA supports the * ("star") wildcard operator, which matches zero or more characters. You can combine wildcard operators with other characters to create a wildcard pattern.
                Example: search_term = "child*"   This example query looks in the endpoint for items whose search_field contains words that begin with child, case insensitive. This will include drugs with brand names that contain "Child", "Children", "Childrens" among others.

                     '''
                },
                "limit": {
                "type": "integer",
                "description": "The maximum amount of records returned"
                }
            },
            "required": ["search_field", "search_term", "limit"]
            }
        }
        }
    ]

def initalize_assistant(tools):
    assistant = OPENAI_CLIENT.beta.assistants.create(
    name="SK Medical Chatbot",
    instructions= ASSISTANT_INSTRUCTIONS,
    tools = tools,
    model="gpt-4o",
    )
    return assistant


def main():
    tools = get_function_description()
    assistant = initalize_assistant(tools)
    #create thread
    thread = OPENAI_CLIENT.beta.threads.create()

    #prompt - answer loop
    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            break
        
        messages = message = OPENAI_CLIENT.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content= user_input
        )

        run = OPENAI_CLIENT.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
    
        if run.status == 'completed':
            messages = OPENAI_CLIENT.beta.threads.messages.list(
            thread_id=thread.id
            )
            print("\n" + messages.data[0].content[0].text.value + "\n")
        else:
            print(run.status)
        
        # Define the list to store tool outputs
        tool_outputs = []
        
        # Loop through each tool in the required action section
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_current_temperature":
                tool_outputs.append({
                "tool_call_id": tool.id,
                "output": "57"
                })
            elif tool.function.name == "get_rain_probability":
                tool_outputs.append({
                "tool_call_id": tool.id,
                "output": "0.06"
                })
        
        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = OPENAI_CLIENT.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")
        
        if run.status == 'completed':
            messages = OPENAI_CLIENT.beta.threads.messages.list(
                thread_id=thread.id
            )
            print("\n" + messages.data[0].content[0].text.value + "\n")
        else:
            print(run.status)

if __name__ == "__main__":
    main()
