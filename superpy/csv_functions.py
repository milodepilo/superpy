import os
import csv
import sys
import pandas as pd
import date_keeping

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# set stdout as variable for easy use later on.
out = sys.stdout
# set the date from datetime.txt in variable today
today = date_keeping.return_date()


def add_data_to_csv(file_path, names_used_as_headers, data_to_be_added):
    """ Add data to a csv file

    this funcition is called by other functions to write data to csv files.
    The data is provided by the caller functions.

    arguments:

    file_path -- the path of the given csv file. str
    names_used_as_headers -- the names that will be used as headers. list
    data_to_be_added -- data that wil be written to the csv files. dict


    """
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
    """Function that removes a row from a csv file

    The function is called by other functions to remove a row from a given csv file. Mainly when an item is sold
    It reads the given csv file and when it encounters a row with the item that has to removed, it appends it to a list.
    The list then get sorted on expiration date, first in first out style, and the first row is removed.
    the list is then merged back with the rest of the rows, and written to csv.

    arguments:

    file_path -- path to the csv file
    name_of_item -- name of the item that was sold.


    """

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
        with open("f.csv", 'r') as inventory:
            dict_reader = csv.DictReader(inventory)
            for row in dict_reader:
                if row['item_name'] == item_name:
                    count += 1
            return count
    except FileNotFoundError:
        print("Inventory file non existent, nothing has been bought yet")
        sys.exit(1)


def get_inventory():
    inventory = pd.read_csv("inventory.csv", header=0, index_col=False)
    inventory_dict = inventory.to_dict(orient='records')
    return inventory_dict
