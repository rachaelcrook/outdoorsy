from database import get_entries, create_table, format_results, insert_csv_to_db, parse_delimiter
from colorama import Fore, Style


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
            input_path = input("Enter the path to the comma or tab delimited file you would like to upload: ")
            input_delimiter = input('Enter the delimiter "comma" or "tab" : ')
            delimiter = parse_delimiter(input_delimiter)
            try:
                insert_csv = insert_csv_to_db(input_path, delimiter)
            except FileNotFoundError:
                print(Fore.RED + f"no comma or tab delimited files were found at that path. Path entered was:"
                                 f" {input_path} Please verify a comma or tab delimited file exists"
                                 f" at this path and try again.")
                print(Style.RESET_ALL)
            except TypeError:
                print(Fore.RED + f"The delimiter specified must be either comma or tab."
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


if __name__ == "__main__":
    run_interactively()


