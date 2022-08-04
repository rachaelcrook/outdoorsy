# importing required modules
import argparse

from database import get_entries, format_results, insert_csv_to_db, parse_delimiter


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
                        required=False,
                        help="View the Outdoorsy Customer Table from the Database. Sorted by Fullname by Default")

    parser.add_argument("-s", "--sort",
                        choices=['name', 'vehicle_type'],
                        required=False,
                        help="Sort the database table by the Outdoorsy Customer's Fullname or Vehicle Type ")
    return parser


def main():
    # Creating the parser and parsing the arguments
    parser = create_parser()
    args = parser.parse_args()

    if args.file:
        input_path = args.file
        if args.delimiter:
            input_delimiter = args.delimiter
            delimiter = parse_delimiter(input_delimiter)
            insert_csv_to_db(input_path, delimiter)
        else:
            # Print error to console
            print("You have entered an invalid option for the delimiter, please choose either comma or pipe.")
        return

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




