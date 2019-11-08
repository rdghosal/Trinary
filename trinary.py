#!/usr/bin/env python3
import os, re, sys, argparse
from time import sleep
from datetime import datetime
from helpers import parse_progress, make_report, get_depts


DEFAULT_PATH = os.path.join(os.getcwd(), "TrinaryLog")


def run(drive, path, to_console):

    # Setup folder for log
    if path == DEFAULT_PATH and not os.path.exists(path):
        os.mkdir(path)
    elif not os.path.isdir(path) or not os.path.exists(path):
        print("ERROR: The input path {0} does not exist".format(path))
        sleep(2)
        sys.exit(1)

    # Get and format timestamp for report 
    current_datetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    departments = get_depts()
    lines = make_report(parse_progress(drive, departments), current_datetime)

    log_path = os.path.join(path, "trinary_log.txt")
    if to_console:
        print()
        for line in lines: print(line, end="")
    else:
        with open(log_path, "a", encoding="utf-8") as log:
            log.writelines(lines)
            log.write("\n---\n\n")
    
        print("{0} has been updated".format(log_path))

    print()
    input("Press any key to exit the program.")
    sys.exit(0)


if __name__ == "__main__":

    description = """Trinary reads through folder/file names in an input drive
                    and outputs a progress report based on permutations of a patterned string"""

    parser = argparse.ArgumentParser(description=description) # Appears with -h (help)
    parser.add_argument("-d", "--drive", required=True)
    parser.add_argument("-p", "--path", nargs="?", default=DEFAULT_PATH,\
         help="Path for report; if not specified folder is generated in current working directory")
    parser.add_argument("-c", "--console", action="store_true", help="Print report to console")

    args = parser.parse_args()

    drive = args.drive
    path = args.path
    to_console = True if args.console else False

    run(drive, path, to_console)