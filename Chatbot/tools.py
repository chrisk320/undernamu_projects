import requests
import json
import xmlrpc.client

def get_product_info_by_criteria(name=None, min_price=None, max_price=None, category=None, reference=None, in_stock=None):
    # Replace these with your actual Odoo server details
    url = 'https://www.skmedical.co'
    db = 'sk-medical'
    username = 'aydenlamparski@gmail.com'
    password = 'f8d7d887c71d251feb493a5911dc3077c2676c4a'

    # Connect to the Odoo server
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    try:
        version = common.version()
        print(f"Connected to Odoo server version: {version['server_version']}")
    except Exception as e:
        return f"Failed to connect to the Odoo server: {e}"

    # Authenticate
    uid = common.authenticate(db, username, password, {})
    if not uid:
        return "Authentication failed"

    # Create a connection to the object endpoint
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Define the fields of interest
    fields_of_interest = [
        'name',              # Product name
        'list_price',        # Sales price
        'description',       # Description
        'description_sale',  # Sales description
        'description_purchase',  # Purchase description
        'categ_id',          # Product category
        'default_code',      # Internal reference
        'code',              # Reference
        'uom_id',            # Unit of Measure
        'qty_available',     # Quantity On Hand
        'x_studio_char_field_80a_1hlhqpi25'  # Application (custom field example)
    ]

    # Build domain for search criteria
    domain = []
    if name:
        domain.append(['name', 'ilike', name])
    if min_price:
        domain.append(['list_price', '>=', min_price])
    if max_price:
        domain.append(['list_price', '<=', max_price])
    if category:
        domain.append(['categ_id', '=', category])
    if reference:
        domain.append(['default_code', '=', reference])
    if in_stock is not None:
        domain.append(['qty_available', '>', 0])

    # Search for products by criteria and gather their details
    try:
        products = models.execute_kw(db, uid, password, 'product.product', 'search_read', 
                                     [domain], 
                                     {'fields': fields_of_interest, 'limit': 10})

        if not products:
            return "No products found with the given criteria."
        else:
            result = ""
            for product in products:
                result += "Product Information:\n"
                for key, value in product.items():
                    result += f"{key}: {value}\n"
                result += "\n" + "-"*50 + "\n"  # Separator between products
            return result
    except Exception as e:
        return f"Failed to retrieve products: {e}"

def search_openFDA_registrationlisting(search_field: str, search_term: str, limit: int) -> str:
    """
    Searches the openFDA registration listing endpoint with the given parameters.
    
    Args:
        search_field (str): The field to search within.
        search_term (str): The term to search for.
        limit (int): The maximum number of records to return.

    Returns:
        str: A JSON string of the search results if successful, None otherwise.
    """
    OPENFDA_API_KEY = "PHv7rqvg9a4Uu9o7Y1nd42FflWDHQYuocFRcvgit"
    url = f"https://api.fda.gov/device/registrationlisting.json?api_key={OPENFDA_API_KEY}&search={search_field}={search_term}&limit={limit}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(url)
        return None
    
def get_function_description() -> list:
    """
    Provides the description and parameters for the tool call functions.
    
    Returns:
        tool object: A list containing the function description and parameters.
    """
    
    #get_product_info_by_criteria
    function1_name = "get_product_info_by_criteria"
    function1_description = '''
        This function connects to an Odoo server, searches for products based on various criteria, and retrieves detailed information about these products.
        The information retrieved includes fields related to the product such as name, price, descriptions, category, reference numbers, units of measure, and application.
        The function returns a string with formatted information about all products that match the search criteria.
    '''
    function1_paramaters = {
        "product_name": {
            "type": "string",
            "description": '''
                The name or partial name of the product to search for.
                This field is case-insensitive and supports partial matches using the ilike operator.
                Example: product_name = "Glove"   This will match any product whose name contains "Glove".
            '''
        },
        "min_price": {
            "type": "number",
            "description": '''
                The minimum price of the product to search for.
                Example: min_price = 10.00   This will match any product with a price greater than or equal to 10.00.
            '''
        },
        "max_price": {
            "type": "number",
            "description": '''
                The maximum price of the product to search for.
                Example: max_price = 50.00   This will match any product with a price less than or equal to 50.00.
            '''
        },
        "category": {
            "type": "string",
            "description": '''
                The category of the product to search for.
                This field supports exact matches.
                Example: category = "Medical Supplies"   This will match any product in the "Medical Supplies" category.
            '''
        },
        "reference": {
            "type": "string",
            "description": '''
                The internal reference or code of the product to search for.
                This field supports exact matches.
                Example: reference = "SKU12345"   This will match any product with the internal reference "SKU12345".
            '''
        },
        "in_stock": {
            "type": "boolean",
            "description": '''
                Whether to search for products that are currently in stock.
                Example: in_stock = true   This will match any product that is currently in stock.
            '''
        }
    }
    function1_required = []

    function2_name = "search_openFDA_registrationlisting"
    function2_description = '''
        The API returns individual results as JSON by default. The JSON object has two sections:
        - meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
        - results: An array of matching results, dependent on which endpoint was queried.
        
        Understanding the output: 
        For search queries, the results section includes matching SPL reports returned by the API.
        Each SPL report consists of these major sections:
        - Standard SPL fields, including unique identifiers.
        - Product-specific fields, the order and contents of which are unique to each product.
        - An openfda section: An annotation with additional product identifiers, such as UPC and brand name, of the drug products listed in the labeling.
    '''
    function2_paramaters = {
        "search_field": {
            "type": "string",
            "description": '''
                If you don't specify a field to search, the API will search in every field.
                Harmonization: 
                Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
                openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
                Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openfda sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
                Exhaustive list of harmonized fields for the registration and listing endpoint:
                - regulation_number
                - openfda.device_name
                - device_class
                - medical_specialty_description
                - k_number
                - pma_number
            '''
        },
        "search_term": {
            "type": "string",
            "description": '''
                To search for records containing a word, search_term should be set to that word as a string.
                Advanced syntax:
                - Spaces: Queries use the plus sign + in place of the space character. Wherever you would use a space character, use a plus sign instead.
                - Grouping: To group several terms together, use parentheses ( ) and +OR+ or +AND+.
                - Wildcard search: Wildcard queries return data that contain terms matching a wildcard pattern. A wildcard operator is a placeholder that matches one or more characters. At this point, openFDA supports the * ("star") wildcard operator, which matches zero or more characters. You can combine wildcard operators with other characters to create a wildcard pattern.
                Example: search_term = "child*"   This example query looks in the endpoint for items whose search_field contains words that begin with child, case insensitive. This will include drugs with brand names that contain "Child", "Children", "Childrens" among others.
            '''
        },
        "limit": {
            "type": "integer",
            "description": "The maximum amount of records returned"
        }
    }
    function2_required = ["search_field", "search_term", "limit"]

    return [
        {
            "type": "function",
            "function": {
                "name": function1_name,
                "description": function1_description,
                "parameters": {
                    "type": "object",
                    "properties": function1_paramaters,
                    "required": function1_required
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": function2_name,
                "description": function2_description,
                "parameters": {
                    "type": "object",
                    "properties": function2_paramaters,
                    "required": function2_required
                }
            }
        },
    ]

def handle_tool_calls(openai_client, run: object, thread: object) -> object:
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
        if tool.function.name == "search_openFDA_registrationlisting":
            argument_dictionary = ast.literal_eval(tool.function.arguments)
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": get_product_info_by_criteria(
                    argument_dictionary.get('search_field'),
                    argument_dictionary.get('Search_term'),
                    argument_dictionary.get('limit')
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