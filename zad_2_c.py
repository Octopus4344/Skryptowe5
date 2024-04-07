import re


def get_user_from_log(log):
    try:
        description = log["description"]
        pattern = r'user (\S+)(?: \[.*\])?'
        match = re.search(pattern, description)
        if match:
            return match.group(1)
        else:
            return None
    except KeyError:
        print("No description")
        return None
