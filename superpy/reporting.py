import date_keeping
import datetime
import pandas as pd
import os
import sys
from tabulate import tabulate

# setting some variables to see if files are already present.
bought_exists = os.path.exists('bought.csv')
sold_exists = os.path.exists('sold.csv')
if bought_exists is True:
    # reading bought.csv into a pandas dataframe.
    bought = pd.read_csv('bought.csv')
if sold_exists is True:
    # reading sold.csv into a pandas dataframe.
    sold = pd.read_csv("sold.csv")
# setting the day perceived as today in a variable for use further on.
today = date_keeping.return_date()

out = sys.stdout


def get_revenue(args):

    revenue = 0

    try:
        # if no date and no type was specified, return profit so far.
        if args.date == None and args.type == None:
            # sold.itterows is an iterable variable of all rows in the pandas dataframe.
            for index, row in sold.iterrows():
                revenue += row["sell_price"]
            return out.write(f"total revenue so far is: {revenue}")

        # return the profit for a given month.
        elif args.type == "month":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"][5:-3]
                if sellDate in args.date:
                    revenue += row["sell_price"]

        # return the profit for a given year.
        elif args.type == "year":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"][:3]
                if sellDate in args.date:
                    revenue += row["sell_price"]

        # return the profit for any given date.
        elif args.type == "date":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"]
                if sellDate in args.date:
                    revenue += row["sell_price"]

        # return the profit for the dat percieved as today in datetime.txt
        elif args.type == "today":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"]
                if sellDate == today:
                    revenue += row["sell_price"]

        # print out different messages based on the types and dates
        if args.type == "date" or args.type == "year" or args.type == "month":
            return out.write(f"revenue for {args.type}: {args.date} is: {revenue}")
        elif args.type == "today":
            return out.write(f"todays revenue so far is: {revenue}")
        else:
            return out.write(f"total revenue so far is: {revenue}")

    # if sold.csv is not found, return an error message.
    except NameError:
        return out.write("sold.csv is not found, check if if this is correct, e.g. no sales took place yet.")


def get_profit(args):

    profit = 0

    try:
        for index, row in sold.iterrows():
            sold["profit"] = sold["sell_price"] - sold["buy_price"]

        if args.type == None and args.type == None:
            for index, row in sold.iterrows():
                profit += row["profit"]

        if args.type == "month":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"][5:-3]
                if sellDate in args.date:
                    profit += row["profit"]

        elif args.type == "year":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"][:3]
                if sellDate in args.date:
                    profit += row["profit"]

        elif args.type == "date":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"]
                if sellDate in args.date:
                    profit += row["profit"]

        elif args.type == "today":
            for index, row in sold.iterrows():
                sellDate = row["sell_date"]
                if sellDate == today:
                    profit += row["profit"]

        if args.type == "date" or args.type == "year" or args.type == "month":
            return out.write(f"profit for {args.type}: {args.date} is: {profit}")
        elif args.type == "today":
            return out.write(f"todays profit so far is: {profit}")
        else:
            return out.write(f"total profit so far is: {profit}")

    except NameError:
        return out.write("sold.csv is not found, check if if this is correct, e.g. no sales took place yet.")


def export(args=[]):
    filename = f"superpy{date_keeping.return_date()}"
     
    try:
        with pd.ExcelWriter(f"export/{filename}.xlsx", mode="a") as writer:
            try:
                boughtDF = pd.read_csv("bought.csv")
                boughtDF.to_excel(writer, sheet_name="Bought")
            except FileNotFoundError:
                print("no bought.csv found")

            try:
                soldDF = pd.read_csv("sold.csv")
                soldDF.to_excel(writer, sheet_name="Sold")
            except FileNotFoundError:
                print("no sold.csv file found")

            try:
                inventoryDF = pd.read_csv("inventory.csv")
                inventoryDF.to_excel(writer, sheet_name="Inventory")
            except FileNotFoundError:
                print("no inventory.csv file found")

            try:
                expiredDF = pd.read_csv("expired.csv")
                expiredDF.to_excel(writer, sheet_name="Expired")
            except FileNotFoundError:
                print("no expired.csv file found")

    except FileNotFoundError:
        try:
            with pd.ExcelWriter(f"export/{filename}.xlsx") as writer:
                try:
                    boughtDF = pd.read_csv("bought.csv")
                    boughtDF.to_excel(writer, sheet_name="Bought")
                except FileNotFoundError:
                    print("no bought.csv found")

                try:
                    soldDF = pd.read_csv("sold.csv")
                    soldDF.to_excel(writer, sheet_name="Sold")
                except FileNotFoundError:
                    print("no sold.csv file found")

                try:
                    inventoryDF = pd.read_csv("inventory.csv")
                    inventoryDF.to_excel(writer, sheet_name="Inventory")
                except FileNotFoundError:
                    print("no inventory.csv file found")

                try:
                    expiredDF = pd.read_csv("expired.csv")
                    expiredDF.to_excel(writer, sheet_name="Expired")
                except FileNotFoundError:
                    print("no expired.csv file found")
        except IndexError:
            print("no csv files found, no sheets created.")
            pass

    except IndexError:
        print("no csv files found, no sheets created.")
        pass
    os.system("start " + f"export/{filename}.xlsx")
