import os
import csv
import sys
import pandas as pd
import date_keeping
from tabulate import tabulate

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# set stdout as variable for easy use later on.
out = sys.stdout
# set the date from datetime.txt in variable today
today = date_keeping.return_date()


def add_data_to_csv(file_path, names_used_as_headers, data_to_be_added):
 
    file_exists = os.path.exists(file_path)

    if file_exists is not True:
        with open(file_path, "a", newline='') as f:
            dict_writer = csv.DictWriter(f,
                                         fieldnames=names_used_as_headers)
            dict_writer.writeheader()
            dict_writer.writerow(data_to_be_added)
    else:
        with open(file_path, "a", newline='') as f:
            dict_writer = csv.DictWriter(f,
                                         fieldnames=names_used_as_headers)
            dict_writer.writerow(data_to_be_added)


def remove_row_from_csv(file_path, name_of_item):
   

    header_names = [
        "id", "item_name", "buy_date", "buy_price", "expiration_date", "expired"
    ]
    matching_rows = []
    rest_of_rows = []
    final_output = []

    with open(file_path, "r") as read_file:
        dict_reader = csv.DictReader(read_file)
        for row in dict_reader:
            if row["item_name"] == name_of_item:
                matching_rows.append(row)
            else:
                rest_of_rows.append(row)
    sorted_on_exp_date = sorted(matching_rows,
                                key=lambda d: d["expiration_date"])

    for i in range(1, len(matching_rows)):
        rest_of_rows.append(sorted_on_exp_date[i])

    final_output = rest_of_rows

    with open(file_path, "w", newline='') as write_file:
        dict_writer = csv.DictWriter(write_file, fieldnames=header_names)
        dict_writer.writeheader()
        for key in final_output:
            dict_writer.writerow(key)


def get_row_from_csv(file_name, name_of_item):

    try:
        with open(file_name, "r") as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                if row["item_name"] == name_of_item:
                    return row
    except FileNotFoundError:
        print("File not found, get row from csv")
        sys.exit(1)


def check_stock(item_name):

    count = 0
    try:
        with open("inventory.csv", 'r') as inventory:
            dict_reader = csv.DictReader(inventory)
            for row in dict_reader:
                if row['item_name'] == item_name:
                    count += 1
            return count
    except FileNotFoundError:
        print("Inventory file non existent, nothing has been bought yet")
        sys.exit(1)


def get_inventory(args=[]):
    inventory = pd.read_csv("inventory.csv", header=0, index_col=False)
    inventory_dict = inventory.to_dict(orient='records')
    print(f"current inventory: \n{tabulate(inventory_dict, headers='keys')}")
