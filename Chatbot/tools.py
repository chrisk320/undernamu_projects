import requests
import json

# OpenFDA API Key
OPENFDA_API_KEY = "PHv7rqvg9a4Uu9o7Y1nd42FflWDHQYuocFRcvgit"

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
    Provides the description and parameters for the search_openFDA_registrationlisting function.
    
    Returns:
        list: A list containing the function description and parameters.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_openFDA_registrationlisting",
                "description": '''
                    The API returns individual results as JSON by default. The JSON object has two sections:
                    - meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
                    - results: An array of matching results, dependent on which endpoint was queried.
                    
                    Understanding the output: 
                    For search queries, the results section includes matching SPL reports returned by the API.
                    Each SPL report consists of these major sections:
                    - Standard SPL fields, including unique identifiers.
                    - Product-specific fields, the order and contents of which are unique to each product.
                    - An openfda section: An annotation with additional product identifiers, such as UPC and brand name, of the drug products listed in the labeling.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
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
                    },
                    "required": ["search_field", "search_term", "limit"]
                }
            }
        }
    ]
