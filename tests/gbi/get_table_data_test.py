from app_server.routes.tableinfo import get_table_data, convert_to_dict_of_lists

from app_server import app

with app.app_context():
    res = get_table_data('customer_table')
    res = convert_to_dict_of_lists(res)
    print(res)