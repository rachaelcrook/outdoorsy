# Outdoorsy Command-Line Tool

# Introduction

A demo command line tool for displaying information from a comma or pipe delimited file.

# Features

- Use as command-line tool interactively or by passing arguments
- Creates a local SQL Lite Database for storing files
- View database in a table format from the command-line
- Sort by "Name" or "Vehicle Type" columns (from sample files)

# Installation

Grab a copy of the code with pip:

```bash
pip install outdoorsy
```

# Usage

outdoorsy can be used to extract info from a Comma or Pipe delimited file in two ways:

- Command line/Terminal tool ran interactively `outdoorsy`
- Command line/Terminal tool ran with arguments `outdoorsy -h`

## 1. Command Line/Terminal tool

```bash
outdoorsy
```

Run outdoorsy -h to see the help output:

```bash
outdoorsy -h
```

usage:

```bash 
usage: outdoorsy [-h] [-f FILE] [-d {comma,pipe}] [-v] [-s {name,vehicle_type}]
```

Outdoorsy Command Line tool for displaying Outdoorsy user information.

### Arguments

```
options:
  -h, --help            show this help message and exit
  
  -f FILE, --file FILE  Specify a new file to be uploaded to the Database. For example, C:\folder\file.csv
                        Note: file needs to be either comma or pipe delimited
 
  -d {comma,pipe}, --delimiter {comma,pipe}
                        To upload a file to the Database, specify the delimiter used in the file
 
  -v, --view            View the Outdoorsy Customer Table from the Database. Sorted by Fullname by Default
 
  -s {name,vehicle_type}, --sort {name,vehicle_type}
                        Sort the database table by the Outdoorsy Customer's Fullname or Vehicle Type
                       
```

### Examples

#### Upload CSV file to database

```bash
outdoorsy -f C:\folder\file.csv -d comma
```

#### Upload Pipe delimited file to database

```bash
outdoorsy -f C:\folder\pipes.text -d pipe
```

#### View data that has previously been uploaded to the database

```bash
outdoorsy -v
```

#### View data sorted by Vehicle Type

```bash
outdoorsy -v -s vehicle_type
```

#### View data sorted by name

```bash
outdoorsy -v -s name
```

# License

This program is licensed with an [MIT License](https://github.com/rachaelcrook/outdoorsy/blob/main/LICENSE).