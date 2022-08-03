# importing required modules
import argparse
from outdoorsy import csv_dict_list

# create a parser object
parser = argparse.ArgumentParser(description="Outdoorsy Command Line tool for displaying user information.")

# add argument
# parser.add_argument("add", nargs='*', metavar="num", type=int,
#                     help="All the numbers separated by spaces will be added.")

# required arguments
parser.add_argument("-f", "--file", required=True,
                    help="Specify the file to be uploaded")

# parse the arguments from standard input
args = parser.parse_args()

# check if add argument has any input data.

# If it has, then print sum of the given numbers
# if len(args.add) != 0:
#     print(sum(args.add))

path = args.file
delimiter = ','

newdict = csv_dict_list(path, delimiter)

print(newdict)