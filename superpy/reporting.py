import date_keeping
import datetime
import pandas as pd
import os
import sys

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
    """ Function that returns the revenue for any given day or date range.

    this function uses the panda dataframes to report back the revenue for any
    given date or date range.It iterates over al rows in the sold.csv file, 
    checks if the date is in the args.date and adds the selling price to the revenue variable.
    once completed it returns a format string  with the revenue
    based on the args.date

    variables:

    args.date -- date specified by the user on the cli
    args.type -- the type of date specified: [month, year, date, today]
    revenue -- variable used to keep track of the revenue

    """

    revenue = 0

    try:
        # if no date and no type was specified, return profit so far.
        if args.date == None and args.type == None:
            for index, row in sold.iterrows(): # sold.itterows is an iterable variable of all rows in the pandas dataframe.
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
    """ Function that returns the profit for a given date/daterange
    
    This function is almost the same as the revenue function, it makes use of the pandas dataframes at the top of the file.
    The only difference is that it subtracts the buy price from the sell price, before adding the solution of that to a profit variable.

    variables:

    args.date -- date specified by the user on the cli
    args.type -- the type of date specified: [month, year, date, today]
    profit -- variable used to keep track of the profit
    
    
    """

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
