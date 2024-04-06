import re


def get_user_from_log(log):
    try:
        description = log["description"]
        pattern = r'user (\S+)(?: \[.*\])?'
        return re.search(pattern, description)
    except KeyError:
        print("No description")
        return None

