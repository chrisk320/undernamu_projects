import xmlrpc.client
from datetime import datetime

# Replace these with your actual Odoo server details
URL = 'https://www.skmedical.co'
DB = 'sk-medical'
USERNAME = 'aydenlamparski@gmail.com'
PASSWORD = 'f8d7d887c71d251feb493a5911dc3077c2676c4a'

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
    # Authenticate
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    if not uid:
        return "Authentication failed"

    # Create a connection to the object endpoint
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))

    # Prepare invoice lines in the required format
    invoice_lines = [(0, 0, {'product_id': product_id, 'quantity': quantity, 'price_unit': models.execute_kw(DB, uid, PASSWORD, 'product.product', 'read', [[product_id]], {'fields': ['list_price']})[0]['list_price']}) for product_id, quantity in zip(product_ids, quantities)]

    # Create the invoice
    try:
        invoice_id = models.execute_kw(DB, uid, PASSWORD, 'account.move', 'create', [{
            'partner_id': partner_id,
            'move_type': 'out_invoice',  # 'out_invoice' for customer invoice
            'invoice_date': datetime.today().strftime('%Y-%m-%d'),  # Set the invoice date to today
            'invoice_line_ids': invoice_lines
        }])
        return f"Invoice created successfully. Invoice ID: {invoice_id}"
    except Exception as e:
        return f"Failed to create invoice: {e}"

def main():
    # Example usage
    partner_id = 1  # Replace with the actual partner ID
    delivery_address = "123 Medical Street, Bangkok"  # Example delivery address
    product_ids = [9301]  # Replace with actual product IDs
    quantities = [2]  # Quantities corresponding to product IDs

    print(create_invoice(partner_id, delivery_address, product_ids, quantities))

if __name__ == "__main__":
    main()




# import xmlrpc.client

# def get_product_info_by_criteria(name=None, min_price=None, max_price=None, category=None, reference=None, in_stock=None):
#     # Replace these with your actual Odoo server details
#     url = 'https://www.skmedical.co'
#     db = 'sk-medical'
#     username = 'aydenlamparski@gmail.com'
#     password = 'f8d7d887c71d251feb493a5911dc3077c2676c4a'

#     # Connect to the Odoo server
#     common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#     try:
#         version = common.version()
#     except Exception as e:
#         return f"Failed to connect to the Odoo server: {e}"

#     # Authenticate
#     uid = common.authenticate(db, username, password, {})
#     if not uid:
#         return "Authentication failed"

#     # Create a connection to the object endpoint
#     models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

#     # Define the fields of interest
#     fields_of_interest = [
#         'name',              # Product name
#         'list_price',        # Sales price
#         'description',       # Description
#         'description_sale',  # Sales description
#         'description_purchase',  # Purchase description
#         'categ_id',          # Product category
#         'default_code',      # Internal reference
#         'code',              # Reference
#         'uom_id',            # Unit of Measure
#         'qty_available',     # Quantity On Hand
#         'x_studio_char_field_80a_1hlhqpi25'  # Application (custom field example)
#     ]

#     # Build domain for search criteria
#     domain = []
#     if name:
#         domain.append(['name', 'ilike', name])
#     if min_price:
#         domain.append(['list_price', '>=', min_price])
#     if max_price:
#         domain.append(['list_price', '<=', max_price])
#     if category:
#         domain.append(['categ_id', '=', category])
#     if reference:
#         domain.append(['default_code', '=', reference])
#     if in_stock is not None:
#         domain.append(['qty_available', '>', 0])

#     # Search for products by criteria and gather their details
#     try:
#         products = models.execute_kw(db, uid, password, 'product.product', 'search_read', 
#                                      [domain], 
#                                      {'fields': fields_of_interest, 'limit': 10})

#         if not products:
#             return "No products found with the given criteria."
#         else:
#             result = ""
#             for product in products:
#                 result += "Product Information:\n"
#                 for key, value in product.items():
#                     result += f"{key}: {value}\n"
#                 result += "\n" + "-"*50 + "\n"  # Separator between products
#             return result
#     except Exception as e:
#         return f"Failed to retrieve products: {e}"

# # Example usage
# print(get_product_info_by_criteria(name='Glove', min_price=50, max_price=100, in_stock=True))

