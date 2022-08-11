from tabulate import tabulate
from database import get_entries, create_table, insert_csv_to_db
from colorama import Fore, Style
import argparse

"""

This app.py file contains all the logic for command line arguments being passed as well running interactively
from the command line. 

To run interactively, run outdoorsy from the command line without flags.

To run the program with arguments run outdoorsy with the necessary flags to either upload a new file to the database,
view the current DB output with option flags to sort by name(default) or vehicle_type.

To see all command line arguments, run:
outdoorsy -h

Examples:

To upload a csv to the database.
outdoorsy -f /folder/file.csv -d comma

To view entries in the database sorted by Vehicle Type.
outdoorsy -v -s vehicle_type

To run in interactive mode:
outdoorsy

"""


def create_parser():
    """Creates the Argument Parser Object and
        adds all the required arguments to it.

        Returns:
            Parser

        """
    # create a parser object
    parser = argparse.ArgumentParser(description=
                                     "Outdoorsy Command Line tool for displaying Outdoorsy user information. "
                                     "Visit https://github.com/rachaelcrook/outdoorsy for more information",
                                     epilog="")

    # Defining arguments

    parser.add_argument("-f", "--file",
                        required=False,
                        help="Specify a new file to be uploaded to the Database. For example, C:\\folder\\file.csv"
                             " Note: file needs to be either comma or pipe delimited")

    parser.add_argument("-d", "--delimiter",
                        choices=['comma', 'pipe'],
                        required=False,
                        help="To upload a file to the Database, specify the delimiter used in the file")

    parser.add_argument("-v", "--view",
                        required=False, action='store_true',
                        help="View the Outdoorsy Customer Table from the Database. Sorted by Fullname by Default")

    parser.add_argument("-s", "--sort",
                        choices=['name', 'vehicle_type'],
                        required=False,
                        help="Sort the database table by the Outdoorsy Customer's Fullname or Vehicle Type ")
    return parser


def parse_args(args):
    # Creating the parser and parsing the arguments
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    return parsed_args


def run_interactively():
    menu = '''Please select one of the following options:
    1) Upload new file (comma or pipe delimited)
    2) View entries
    3) Exit.
    
    
    Your selection:  '''
    welcome = "Welcome to the Outdoorsy Interface"
    create_table()
    # using walrus operator to ask for user input directly in the while loop.
    while (user_input := input(menu)) != "3":
        if user_input == "1":
            input_path = input("Enter the path to the comma or pipe delimited file you would like to upload: ")
            input_delimiter = input('Enter the delimiter "comma" or "pipe" : ')
            delimiter = parse_delimiter(input_delimiter)
            try:
                insert_csv = insert_csv_to_db(input_path, delimiter)
            except FileNotFoundError:
                print(Fore.RED + f"no comma or pipe delimited files were found at that path. Path entered was:"
                                 f" {input_path} Please verify a comma or pipe delimited file exists"
                                 f" at this path and try again.")
                print(Style.RESET_ALL)
            except TypeError:
                print(Fore.RED + f"The delimiter specified must be either comma or pipe."
                                 f" The delimiter entered was: {input_delimiter} Please try again.")
                print(Style.RESET_ALL)
            else:
                print(Fore.RED + f"Something went terribly wrong and for some reason the file or delimiter "
                                 f"specified isn't working. The delimiter entered was:  {input_delimiter}"
                                 f" The path entered was: {input_path} Please try again.")
                print(Style.RESET_ALL)
        elif user_input == "2":
            select_info = input("Would you like to sort by Full Name (1) or by Vehicle Type (2)?  (1|2): ")
            if select_info == "1":
                results = get_entries('name')
                print(format_results(results))
            elif select_info == "2":
                sorted_by = "vehicle_type"
                results = get_entries(sorted_by)
                print(format_results(results))
            else:
                print(Fore.RED + "Invalid option, please try again!")
                print(Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid option, please try again!")
            print(Style.RESET_ALL)


"""

The format_result functions are used to format data returned from the database into a table displayed to the user
in a command line or terminal window. 

"""


def format_results(results):
    table = tabulate(
        results,
        headers=['First Name', 'Last Name', 'Email', 'Vehicle Type', 'Vehicle Name', 'Vehicle Length (in FT.)'],
        tablefmt='psql')

    return table


"""

Invalid Delimiter is a custom exception to be raised when an invalid delimited is specified when running interactively.
If an invalid delimiter is specified when running cli.py with arguments, an error message is returned automatically
via the argparse library.

"""


class InvalidDelimiter(Exception):
    pass


"""

The parse_delimiter function is referenced by cli.py and app.py when a delimiter is specified either with a 
command line argument or when running interactively. 

"""


def parse_delimiter(delimiter):
    if delimiter == "comma":
        delimiter = ","
    elif delimiter == "pipe":
        delimiter = "|"
    else:
        raise InvalidDelimiter

    return delimiter


if __name__ == "__main__":
    run_interactively()
