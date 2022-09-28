from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import sys
import csv
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Setting stdout in a variable for easier use later on (printing).
out = sys.stdout

# save the dat of today as an iso formatted string.
today = date.today().isoformat()


# function that creates a file with today's date, used by other functions.
def create_datetime_file():
    set_date_to_today()


# function that set the date stored in a datetime.txt to today's date.
def set_date_to_today(args=[]):
    with open('datetime.txt', 'r') as dateFileOld:
        old_date = dateFileOld.readlines
        if old_date != today:
            with open('datetime.txt', 'w') as datefile:
                datefile.write(today)
                check_for_expired_items(
                    message="invoking automatic expired check for the new date.\n")


# function that reads the date stored in datetime.txt and returns it.
def return_date():
    file_exists = os.path.exists('datetime.txt')
    if file_exists is not True:
        create_datetime_file()
        with open('datetime.txt', 'r') as datefile:
            return datefile.readline()
    else:
        with open('datetime.txt', 'r') as datefile:
            return datefile.readline()


# return the date of the day before the date stored in datetime.txt
def return_yesterdays_date():
    return date.fromisoformat(return_date()) - timedelta(1)


# fucntion that advances the date in datetime.txt and calls the check expired function.
def advance_date(args=[]):
    with open('datetime.txt', 'r') as datefile:
        old_date = datefile.readline()
        old_date = date.fromisoformat(old_date)
        new_date = old_date + timedelta(days=args.days)
        with open('datetime.txt', 'w') as new_datefile:
            new_datefile.write(new_date.isoformat())
    check_for_expired_items(
        message="\nYou have advanced the date, now checking for expired items in inventory\n\n")

# function that recedes the date in datetime.txt
def recede_date(args=[]):
    with open('datetime.txt', 'r') as datefile:
        old_date = datefile.readline()
        old_date = date.fromisoformat(old_date)
        new_date = old_date - timedelta(days=args.days)
        with open('datetime.txt', 'w') as new_datefile:
            new_datefile.write(new_date.isoformat())

# function that sets the date in datetime.txt to any given date
def set_date_to_given_date(args=[]):
    if validate_date(args.date) is False:
        return sys.stdout.write("dat is not in correct format, use the following formatting: yyyy-mm-dd")
    else:
        with open("datetime.txt", "w") as datefile:
            datefile.write(args.date)

# Validate the format of the date, and check if month is a zero leading decimal
def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        if len(date[5:-3]) != 2:
            return False
    except ValueError:
        return False

# Function that checks the invetory for expired items.
def check_for_expired_items(args=[], message=""):

    """Function that checks the inventory for expired items
    
    this function can be called on its own to check for expired items,
    but is also called by other functions as an automatic check.
    When called by other function, the message variable is provided by
    the calling function. It uses pandas for quick checking to
    see if the file has more than only the header inside of it.
    the rest of the csv actions are performed using pythons csv module.

    arguments:
    message -- 
    """

    file_exists = os.path.exists("inventory.csv")
    # this part prints out the message given to it when called by other functions.
    if len(message) != 0:
        out.write(message)
    if file_exists is not True:
        out.write("inventory.csv does not exist, check if this is correct.")
    else:
        # read the inventory into a pandas dataframe and check if it has more than one line(header).
        inventoryDF = pd.read_csv("inventory.csv")
        if len(inventoryDF) == "1":
            print(len(inventoryDF))
            return out.write("nothing in stock, nothing expired :)")
        else:
            header_names = [
                "id", "item_name", "buy_date", "buy_price", "expiration_date",
                "expired"
            ]
            # Initiating some empty list to append data to.
            expired = []
            not_expired = []
            all_items_with_expired_flag = [] # Used for all items but with the new added expired column.
            # open the inventory csv, checking each row for expiration
            with open("inventory.csv", "r") as inv:
                dict_reader = csv.DictReader(inv)
                for row in dict_reader:
                    if row["expiration_date"] < today:
                        row["expired"] = "True"
                        expired.append(row) # append to list if expired
                    else:
                        row["expired"] = "False"
                        not_expired.append(row) # append to list if not expired
            all_items_with_expired_flag = expired + not_expired

            # open the inventory file to write
            with open("inventory.csv", "w", newline="") as new_inv:
                dict_writer = csv.DictWriter(new_inv, fieldnames=header_names)
                dict_writer.writeheader()
                # write each dict in list to csv
                for dict in all_items_with_expired_flag:
                    dict_writer.writerow(dict)

            # opening expired.csv for writing/appending the dicts in the expired list
            with open("expired.csv", "a+", newline="") as expired_csv:
                dict_writer = csv.DictWriter(
                    expired_csv, fieldnames=header_names)
                if os.path.exists("expired.csv") is not True:
                    dict_writer.writeheader()
                    for dict in expired:
                        dict_writer.writrow(dict)
                else:
                    for dict in expired:
                        dict_writer.writerow(dict)

        # print message based on the result of the expired check.
        if len(expired) == 0:
            return out.write("nothing expired")
        return out.write(f"the follwing expired:\n{expired}")
