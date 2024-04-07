import sys
from typing import List, Dict
from datetime import datetime
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import get_message_type
import re

def file_reader(file_name):
    # analyzed_lines : List[Dict[]] = []
    analyzed_lines = []
    try:
        with open(file_name, "r") as file:
            file.seek(0)
            while True:
                current_line = file.readline()
                if current_line:
                    analyzed_lines.append(line_analyzer(current_line))
                else:
                    break
        return analyzed_lines
    except FileNotFoundError:
        print("Niewlasciwa nazwa pliku")


def line_analyzer(line) -> dict:
    dictionary = dict()
    dictionary['time'] = get_time(line)
    dictionary['host_name'] = get_host_name(line)
    dictionary['app_component'] = get_app_component(line)
    dictionary['PID'] = get_pid(line)
    dictionary['description'] = get_description(line)
    dictionary['IPv4'] = get_ipv4s_from_log(dictionary)
    dictionary['user_name'] = get_user_from_log(dictionary)
    dictionary['message_type'] = get_message_type(dictionary['description'])
    return dictionary


def get_time(line):
    # split_line = line.split()
    # date = " ".join(split_line[:3])
    # # rest = " ".join(split_line[3:])
    # date_time = datetime.strptime(date, "%b %d %H:%M:%S")
    # return date_time
    pattern = r'^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})'
    match = re.search(pattern, line)
    if match:
        return datetime.strptime(match.group(1),"%b %d %H:%M:%S")
    else:
        return None


def get_host_name(line):
    pattern = r'\b\w{3} \d{1,2} \d{2}:\d{2}:\d{2} (\w+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None


def get_app_component(line):
    pattern = r'(\w+)\[\d+\]:'
    match = re.search(pattern,line)
    if match:
        return match.group(1)
    else:
        return None
   # return line.split()[4].split("[")[0].strip()


def get_pid(line):
    pattern = r'\[(\d+)\]:'
    match = re.search(pattern,line)
    if match:
        return match.group(1)
    else:
        return None
    #return line.split()[4].split("[")[1].split("]")[0].strip()


def get_description(line):
    pattern = r'\[\d+\]:\s*(.*$)'
    match = re.search(pattern,line)
    if match:
        return match.group(1)
    else:
        return None
    # split_line = line.split(":")
    # desc = " ".join(split_line[3:])
    # return desc[1:]


if __name__ == "__main__":
    try:
        file_name = input("Podaj nazwe pliku: ")
        file_lines = file_reader(file_name)
        for line in file_lines:
            print(line)
    except IndexError:
        print("Prosze podac nazwe pliku")
