# importing required modules
import argparse
import sys

from app import run_interactively
from database import get_entries, format_results, insert_csv_to_db, parse_delimiter

"""
This cli.py file contains all the logic for command line arguments being passed and references functions in app.py
which contains the logic for running interactively from the command line. 

To run interactively, run cli.py from the command line without flags.

To run the program with arguments run cli.py with the necessary flags to either upload a new file to the database,
view the current DB output with option flags to sort by name(default) or vehicle_type.

For example:

To upload a csv to the database.
cli.py -f /folder/file.csv -d comma

To view entries in the database sorted by Vehicle Type.
cli.py -v -s vehicle_type

To run in interactive mode:
cli.py

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


def main():
    if len(sys.argv) == 1:
        # Run interactively if no arguments are passed.
        run_interactively()

    args = parse_args(sys.argv[1:])
    print(sys.argv)

    if args.file and args.delimiter:
        input_path = args.file
        delimiter = parse_delimiter(args.delimiter)
        insert_csv_to_db(input_path, delimiter)

    if args.delimiter and not args.file:
        print("Please specify both a file and delimiter. For example: python cli.py -f comma.csv -d comma")

    if args.view and not args.sort:
        results = get_entries('name')
        print(format_results(results))

    if args.view and args.sort:
        sorted_by = args.sort
        if sorted_by == 'name':
            results = get_entries('name')
            print(format_results(results))
        elif sorted_by == 'vehicle_type':
            sorted_by = "vehicle_type"
            results = get_entries(sorted_by)
            print(format_results(results))
        else:
            print("Invalid option, please try again!")


if __name__ == "__main__":
    main()
