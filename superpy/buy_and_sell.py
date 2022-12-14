import os
from date_keeping import return_date
from csv_functions import add_data_to_csv
from csv_functions import remove_row_from_csv
from csv_functions import check_stock
from csv_functions import get_row_from_csv
from id_creator import return_id
from id_creator import map_name_to_id
from id_creator import unique_id
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
out = sys.stdout


def item_bought(args):
   

    # Names used as header in bought.csv
    header_names = [
        "id", "item_name", "buy_date", "buy_price", "expiration_date",
        "expired"
    ]
    # Data to be written to bought.csv
    item_data = {
        "id": map_name_to_id(args.item_name, unique_id()),
        "item_name": args.item_name,
        "buy_date": return_date(),
        "buy_price": args.price,
        "expiration_date": args.expiration_date,
        "expired": "Null"
    }

    # write the data to the bought.csv file
    add_data_to_csv("bought.csv", header_names, item_data)
    # write the data to the inventory.cs file
    add_data_to_csv("inventory.csv", header_names, item_data)


def item_sold(args):
    
    # Names used as header in sold.csv
    header_names = [
        "id", "item_name", "expiration_date", "buy_date", "buy_price",
        "sell_date", "sell_price", "expired"
    ]

    # Data to be written to sold.csv
    item_data = {
        "id": return_id(args.item_name),
        "item_name": args.item_name,
        "sell_date": return_date(),
        "sell_price": args.price
    }

    # check if the item is in stock if not return
    if check_stock(args.item_name) == 0:        
        return out.write("item out of stock")

    # get data from the bought.csv and join it with the sold data    
    buy_data = get_row_from_csv("bought.csv", args.item_name)
    # sold.csv now also contains info from when the item was bought
    complete_data = item_data | buy_data

    # write the data to the sold.csv and remove it from inventory
    add_data_to_csv("sold.csv", header_names, complete_data)
    remove_row_from_csv("inventory.csv", args.item_name)
