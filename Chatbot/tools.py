import requests
import json
import xmlrpc.client
from datetime import datetime
from config import ODOO_CONFIG, OPENFDA_API_KEY

# Global tool call function map
FUNCTION_MAP = { 
    "get_product_info_by_criteria": {
        "description": '''
            This function connects to an Odoo server, searches for products based on various criteria, and retrieves detailed information about these products.
            This is a database of the products you sell as SK_Medical, so if a customer is asking about what products you sell you should use this function.
            The information retrieved includes fields related to the product such as name, price, descriptions, category, reference numbers, units of measure, and application.
            The function returns a string with formatted information about all products that match the search criteria.
            All blank paramaters will be set to NONE
        ''',
        "parameters": {
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
        },
        "required": []
    },
    "search_openFDA_registrationlisting": {
        "description": '''
            This function connects to the USA FDA's openFDA registration and listing API and searches their database for records containing the search_term in the search_field, returning as many matches as the limit parameter allows.
            Use this function when customers ask for information about a medical device product and that information is not accessible by the Odoo API in the get_product_info_by_criteria function.
            We do not sell all the products contained within this database, and all the products we sell are not necessarily contained within this database.
            Upon Success (at least 1 record found), The function returns individual results as JSON by default.
            Upon Failure (no records found), the function returns an error message.
        ''',
        "parameters": {
            "search_field": {
                "type": "string",
                "description": '''
                    Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
                    openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
                    Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openfda sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
                    Exhaustive list of harmonized fields for the registration and listing endpoint of the form (search_field parameter value, explanation):
                        (products.openfda.device_name, This is the proprietary name, or trade name, of the cleared device.)
                        (proprietary_name, Proprietary or brand name or model number a product is marketed under.)
                        (products.openfda.regulation_number, The classification regulation in the Code of Federal Regulations (CFR) under which the device is identified, described, and formally classified. Covers various aspects of design, clinical evaluation, manufacturing, packaging, labeling, and postmarket surveillance of the specific medical device.)
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
                "description": "The maximum number of records returned. If you want to find as many records as possible, set to a high number."
            }
        },
        "required": ["search_field", "search_term", "limit"]
    },
    "search_openFDA_druglabel": {
        "description": '''
            This function connects to the USA FDA's openFDA drug label API and searches their database for records containing the search_term in the search_field, returning as many matches as the limit parameter allows.
            Use this function when customers ask for information about a drug and that information is not accessible by the Odoo API in the get_product_info_by_criteria function.
            Drug manufacturers and distributors submit documentation about their products to FDA in the Structured Product Labeling (SPL) format. The openFDA drug product labeling API returns data from this dataset. 
            The labels are broken into sections, such as indications for use (prescription drugs) or purpose (OTC drugs), adverse reactions, and so forth.
            The function returns individual results as JSON by default. Upon Failure (no records found), the function returns an error message.
        ''',
        "parameters": {
            "search_field": {
                "type": "string",
                "description": '''
                    Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
                    openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
                    Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openFDA sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
                    Exhaustive list of harmonized fields for the data label endpoint:
                    (openfda.brand_name, Brand or trade name of the drug product.)
                    (openfda.generic_name, Generic name(s) of the drug product.)
                    (openfda.manufacturer_name, Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC.)
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
                "description": "The maximum number of records returned."
            }
        },
        "required": ["search_field", "search_term", "limit"]
    },
    "create_invoice": {
        "description": '''
            This function creates an invoice for the specified partner and invoice lines in the Odoo database.
            The chatbot absolutely MUST confirm the parameters with the customer and send a message confirming that it could create the invoice, including what information it will create it with, before it actually calls the function. 
            It is crucial to avoid creating an invoice when it should not be created.
            The chatbot must send a confirmation message after it calls the function, again with a review of all the information it created it with so the customer can verify.
        ''',
        "parameters": {
            "partner_id": {
                "type": "integer",
                "description": '''
                    The partner ID for whom the invoice is being created.
                    This field must be confirmed with the customer before creating the invoice.
                '''
            },
            "delivery_address": {
                "type": "string",
                "description": '''
                    The delivery address for the invoice.
                    This field must be confirmed with the customer before creating the invoice.
                '''
            },
            "product_ids": {
                "type": "array",
                "items": {
                    "type": "integer"
                },
                "description": '''
                    List of product IDs to be included in the invoice.
                    This field must be confirmed with the customer before creating the invoice.
                '''
            },
            "quantities": {
                "type": "array",
                "items": {
                    "type": "integer"
                },
                "description": '''
                    List of quantities corresponding to the product IDs.
                    This field must be confirmed with the customer before creating the invoice.
                '''
            }
        },
        "required": ["partner_id", "delivery_address", "product_ids", "quantities"]
    }
}

def get_product_info_by_criteria(name=None, min_price=None, max_price=None, category=None, reference=None, in_stock=None):
    """
    Retrieves product information based on the given criteria from an Odoo server.

    Args:
        name (str, optional): The name or partial name of the product.
        min_price (float, optional): The minimum price of the product.
        max_price (float, optional): The maximum price of the product.
        category (str, optional): The category of the product.
        reference (str, optional): The internal reference or code of the product.
        in_stock (bool, optional): Whether to search for products that are currently in stock.

    Returns:
        str: Formatted information about matching products or an error message.
    """
    # Replace these with your actual Odoo server details
    url = ODOO_CONFIG["url"]
    db = ODOO_CONFIG["db"]
    username = ODOO_CONFIG["username"]
    password = ODOO_CONFIG["password"]

    # Connect to the Odoo server
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    try:
        version = common.version()
    except Exception as e:
        return f"Failed to connect to the Odoo server: {e}"

    # Authenticate
    uid = common.authenticate(db, username, password, {})
    if not uid:
        return "Authentication failed"

    # Create a connection to the object endpoint
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

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
            result = []
            for product in products:
                product_info = {key: value for key, value in product.items()}
                result.append(product_info)
            return json.dumps(result, indent=4)
    except Exception as e:
        return f"Failed to retrieve products: {e}"

def create_invoice(partner_id, delivery_address, product_ids, quantities):
    """
    Create an invoice for the specified partner and invoice lines.
    
    Args:
        partner_id (int): The partner ID for whom the invoice is being created.
        delivery_address (str): The delivery address for the invoice.
        product_ids (list): List of product IDs to be included in the invoice.
        quantities (list): List of quantities corresponding to the product IDs.
    
    Returns:
        str: Result message.
    """
    # Retrieve Odoo server details from the configuration file
    url = ODOO_CONFIG['url']
    db = ODOO_CONFIG['db']
    username = ODOO_CONFIG['username']
    password = ODOO_CONFIG['password']

    # Authenticate
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        return "Authentication failed"

    # Create a connection to the object endpoint
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Prepare invoice lines in the required format
    invoice_lines = [(0, 0, {'product_id': product_id, 'quantity': quantity, 'price_unit': models.execute_kw(db, uid, password, 'product.product', 'read', [[product_id]], {'fields': ['list_price']})[0]['list_price']}) for product_id, quantity in zip(product_ids, quantities)]

    # Create the invoice
    try:
        invoice_id = models.execute_kw(db, uid, password, 'account.move', 'create', [{
            'partner_id': partner_id,
            'move_type': 'out_invoice',  # 'out_invoice' for customer invoice
            'invoice_date': datetime.today().strftime('%Y-%m-%d'),  # Set the invoice date to today
            'invoice_line_ids': invoice_lines
        }])
        return f"Invoice created successfully. Invoice ID: {invoice_id}"
    except Exception as e:
        return f"Failed to create invoice: {e}"

def search_openFDA_druglabel(search_field, search_term, limit):
    '''
    
    '''
    url = f"https://api.fda.gov/drug/label.json?api_key={OPENFDA_API_KEY}&search={search_field}:{search_term}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data (status code: {response.status_code}) - {e}"

def search_openFDA_registrationlisting(search_field: str, search_term: str, limit: int) -> str:
    """
    Searches the openFDA registration listing endpoint with the given parameters.
    
    Args:
        search_field (str): The field to search within.
        search_term (str): The term to search for.
        limit (int): The maximum number of records to return.

    Returns:
        str: A JSON string of the search results if successful, an error message otherwise.
    """
    url = f"https://api.fda.gov/device/registrationlisting.json?api_key={OPENFDA_API_KEY}&search={search_field}:{search_term}&limit={limit}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data (status code: {response.status_code}) - {e}"
