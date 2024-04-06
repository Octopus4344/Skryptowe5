import re


def get_ipv4s_from_log(line):
    try:
        description = line["description"]
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return re.findall(pattern, description)
    except KeyError:
        print("No description")
        return []