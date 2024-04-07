import sys
from datetime import datetime
from typing import List, Dict


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
    return dictionary


def get_time(line):
    split_line = line.split()
    date = " ".join(split_line[:3])
    # rest = " ".join(split_line[3:])
    date_time = datetime.strptime(date, "%b %d %H:%M:%S")
    return date_time


def get_host_name(line):
    return line.split()[3].strip()


def get_app_component(line):
    return line.split()[4].split("[")[0].strip()


def get_pid(line):
    return line.split()[4].split("[")[1].split("]")[0].strip()


def get_description(line):
    desc = line.split(":")[3]
    return desc[1:]


if __name__ == "__main__":
    try:
        file_name = input("Podaj nazwe pliku: ")
        file_lines = file_reader(file_name)
        for line in file_lines:
            print(line)
    except IndexError:
        print("Prosze podac nazwe pliku")
