import re, os, sys
from time import sleep
from getpass import getuser


def get_depts():
    """Returns list of departments from user input"""
    while True:
        depts = input("Please list the departments in order with a comma separated list:\n")
        if depts.find(",") != -1:
            break
    depts = depts.split(",")
    return [ dept.strip() for dept in depts ] # Clean up and return list


def make_report(depts_progress, curr_datetime):
    """Takes in iterable of dict to produce lines for report"""
    lines = []
    user = getuser() 
    lines.append("The report by {0} on {1} is as follows:\n".format(user, curr_datetime))
    for dept in depts_progress:
        lines.append("  Data migration progress for {0}: {1:0.1f}%\n".\
            format(dept["name"].upper(), dept["completion_ratio"] * 100))
    return lines


def parse_progress(drive, departments):
    """Searches through drive and evaluates progress of each project based on regex parsing of the folder name""" 
    try: 
        proj_folders = os.listdir(drive)
    except: 
        print("ERROR: Drive does not exist.")
        sleep(2)
        sys.exit(1)

    before = 0 # Number of chars preceding regex capture group in marker string
    after = len(departments) - 1 # Number of chars following regex capture group in marker string

    while after >= 0:
        for department in departments:
            re_str_filter = r"(?<=_(X|0|1){" + str(before) + r"})(0|1)(?=(X|0|1){" + str(after) + r"})"
            re_str_target = r"(?<=_(X|0|1){" + str(before) + r"})(1)(?=(X|0|1){" + str(after) + r"})"

            # Inputs for progress report
            progress = {
                "name": department,
                "completed_projects": 0,
                "total_projects": 0,
                "completion_ratio": 0
            }

            # Checks if subdir name is a marker folder; if so, it parses folder name 
            for folder in proj_folders:
                if re.search(re_str_filter, folder): 
                    progress["total_projects"] += 1
                    if re.search(re_str_target, folder):
                        progress["completed_projects"] += 1
                        progress["completion_ratio"] = progress["completed_projects"] / progress["total_projects"]
        
            # Adjusts capture group location in marker string
            before += 1
            after -= 1
            
            yield progress