import argparse
import buy_and_sell
import date_keeping
import reporting
import csv_functions



def main():
    # Create parser.
    parser = argparse.ArgumentParser(prog="main.py",
                                    description="""Welcome to SuperPy!
                                    The supermarket CLI solution""")
    # Create subparsers.
    subparsers = parser.add_subparsers()


    # Below you will see a repetitive creating of subparsers, only the first has full descriptions.

    # Create subparser for the buy command wiht aliases and help.
    buyParser = subparsers.add_parser("buy", aliases=["b"], help="buy an item")
    # Add arguments to the subparser.
    buyParser.add_argument("item_name", type=str, help="name of the item")
    buyParser.add_argument("price", type=float, help="buying price")
    buyParser.add_argument("expiration_date", type=str)
    # Set the default function for this subparser.
    buyParser.set_defaults(func=buy_and_sell.item_bought)

    # Create subparser for the sell command.
    sellParser = subparsers.add_parser("sell", aliases=["s"], help="sell an item")
    sellParser.add_argument("item_name", type=str)
    sellParser.add_argument("price", type=float)
    sellParser.set_defaults(func=buy_and_sell.item_sold)

    # Create subparser for the set_today command.
    setTodayParser = subparsers.add_parser("set_today", aliases=["dt"],
                                        help="Set the date to today")
    setTodayParser.set_defaults(func=date_keeping.set_date_to_today)

    # Create subparser for the recede_date command.
    recedeDateParser = subparsers.add_parser("recede_date", aliases=["dr"],
                                            help="recede the date by an ammount of days")
    recedeDateParser.add_argument("days", type=int, help="the ammount of days")
    recedeDateParser.set_defaults(func=date_keeping.recede_date)

    # Create subparser for the advance_date command.
    advanceDateParser = subparsers.add_parser("advance_date", aliases=["da"],
                                            help="advance the date by an ammount of days")
    advanceDateParser.add_argument("days", type=int, help="the ammount of days")
    advanceDateParser.set_defaults(func=date_keeping.advance_date)

    # Create subparser for the set_given_date command.
    setDateToGivenDateParser = subparsers.add_parser(
        "set_given_date", aliases=["dd"], help="set the date to the specified date.")
    setDateToGivenDateParser.add_argument(
        "date", type=str, help="specify the date")
    setDateToGivenDateParser.set_defaults(func=date_keeping.set_date_to_given_date)

    # Create subparser for the revenue command.
    revenueParser = subparsers.add_parser("revenue", aliases=[
                                        "r"], help="get the revenue, for any given date or range of dates")
    revenueParser.add_argument("-t", "--type", type=str, choices=[
                            "month", "date", "year", "today"], help="specify which type of data you want to enter")
    revenueParser.add_argument(
        "-d", "--date", type=str, help="sepcify over which month, date or year you want to get the revenue")
    revenueParser.set_defaults(func=reporting.get_revenue)

    # Create subparser for the profit command.
    profitParser = subparsers.add_parser("profit", aliases=[
                                        "p"], help="get the profit for any given date or range of dates")
    profitParser.add_argument("-t", "--type", type=str, choices=[
        "month", "date", "year", ], help="specify which type of data you want to enter")
    profitParser.add_argument(
        "-d", "--date", type=str, help="sepcify over which month, date or year you want to get the profit")
    profitParser.set_defaults(func=reporting.get_profit)

    # Create subparser for check_for_expired_command.
    checkExpiredParser = subparsers.add_parser("check_for_expired", aliases=[
                                            "c"], help="check for expired items in the inventory")
    checkExpiredParser.set_defaults(func=date_keeping.check_for_expired_items)

    # Parse the args :)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
