# Report

## The Experience
The first thing I want to talk about is the whole experience of this assignment which was quite difficult at times but also lots of fun.
In the beginning I struggeled quite a lot deciding how I was going to tackle this project and what methods to use and in which order to write it. This resulted in me rewriting big parts of code multipple times. I first started out with the argparse part, but i thought it was a little bit cumbersome to use the cli to test my code and functions, so I wrote all of the functions first and once those were all complete and working I started working on the argparse module.

### argparse
I have though about how to implement this for quite a while, and thanks to a question of a fellow student I decided to use subparsers so that you can use the set_default method:
`buyParser.set_defaults(func=buy_and_sell.item_bought)`
this felt as a revelation to me becaus befor it tought about usiing conditions on the input to check which argument was used(e.g if arg[0] = "...." then do this function). The set_default eliminated al this hassle.

### id_creator and database
Becuase my previous job expiriences in both retail and in the broadcasting world, which both make extensive use of id's I wanted to come up with a solution to generate unique id's for every item and store them in a database. i use the functions `def unique_id():` and `def map_name_to_id(name, id):` to map item names to an id and store them in a database, and if they already exist, return the existing id.

### automatic expired check, and keyword arguments.
In the `def advance_date(args=[]):` fucntion there is a built in check that checks the inventory for expired items. the `check_for_expired_items()` fucntion itself makes use of keyword arguments in te form of a message. The caller fucntion puts a message there so the user knows from which function the check was done:
`message="\nYou have advanced the date, now checking for expired items in inventory\n\n"`

### Tabulate
I made use of tabulate to simply style any table that are returned to the user.

### Export
there is also a function to export all the .csv files into a xslx workbook.

### Improvements
While I was writing my manual I did come across some things that I could improve if i wanted to, but this assingment is already taking a lot of time.
one of thes things is the following: I make use of this line quite a lot to see if a file already exists:
`file_exists = os.path.exists("inventory.csv")`
and based on the outcome of the following condition run different blocks of code.
` if file_exists is not True:`

this means that i have 2 almost similair blocks of code, which could be one: 
```
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
```
below you can see a block which I altered during the writing of the manual:
```
    with open("expired.csv", "a+", newline="") as expired_csv:
                dict_writer = csv.DictWriter(
                    expired_csv, fieldnames=header_names)
                if os.stat("expired.csv").st_size ==0:
                    dict_writer.writeheader()
                    for dict in expired:
                        dict_writer.writrow(dict)
                else:
                    for dict in expired:
                        dict_writer.writerow(dict)
```

it uses this line `if os.stat("expired.csv").st_size ==0:`to check whether the file is empty combined with using the a+ mode of opening the file.