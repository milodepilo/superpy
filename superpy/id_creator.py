from random import randint
import os
import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# generate a random integer to be used as indentifier.
def unique_id():

    return randint(0, 100000)


# fucntion that assigns the indentifier to a product
# # and stores it in a CSV file.
def map_name_to_id(name, id):

    file_exist = os.path.exists("id_database.csv")
    headers = ["name", "id"]
    name_and_id = {
        "name": name,
        "id": id
    }

    if file_exist is not True:
        with open('id_database.csv', 'w', newline='') as database:
            dict_writer = csv.DictWriter(database, fieldnames=headers)
            dict_writer.writeheader()
            dict_writer.writerow(name_and_id)
            return name_and_id["id"]

    else:
        with open('id_database.csv', 'r+', newline='') as database:
            dict_reader = csv.DictReader(database)
            dict_writer = csv.DictWriter(database, fieldnames=headers)
            for row in dict_reader:
                if row['name'] == name:
                    return row["id"]
            dict_writer.writerow(name_and_id)
            return name_and_id["id"]


def return_id(item_name):

    with open("id_database.csv", 'r') as database:
        dict_reader = csv.DictReader(database)
        for row in dict_reader:
            if row['name'] == item_name:
                return row["id"]