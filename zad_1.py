import logging
import re
import sys
from datetime import datetime

from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import get_message_type

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

stdout_handler.setLevel(logging.DEBUG)
stderr_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s: %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


def file_reader(file_name):
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


def file_reader_new(file_name):
    analyzed_lines = []
    file_content = []
    try:
        with open(file_name, "r") as file:
            file.seek(0)
            while True:
                current_line = file.readline()
                if current_line:
                    analyzed_lines.append(line_analyzer(current_line))
                    file_content.append(current_line)
                else:
                    break
        return analyzed_lines, file_content
    except FileNotFoundError:
        print("Niewlasciwa nazwa pliku")


def line_analyzer(line) -> dict:
    logger.debug("Przeczytano %d bajtów: %s", len(line), line)
    dictionary = dict()
    dictionary['time'] = get_time(line)
    dictionary['host_name'] = get_host_name(line)
    dictionary['app_component'] = get_app_component(line)
    dictionary['PID'] = get_pid(line)
    dictionary['description'] = get_description(line)
    dictionary['IPv4'] = get_ipv4s_from_log(dictionary)
    dictionary['user_name'] = get_user_from_log(dictionary)
    dictionary['message_type'] = get_message_type(dictionary['description'], logger)
    return dictionary


def get_time(line):
    pattern = r'^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})'
    match = re.search(pattern, line)
    if match:
        return datetime.strptime(match.group(1), "%b %d %H:%M:%S")
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
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None


def get_pid(line):
    pattern = r'\[(\d+)\]:'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None


def get_description(line):
    pattern = r'\[\d+\]:\s*(.*$)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":
    try:
        file_name = input("Podaj nazwe pliku: ")
        file_lines, lines = file_reader_new(file_name)
        for dic, line in zip(file_lines, lines):
            print(line)
            print(dic)
    except IndexError:
        print("Prosze podac nazwe pliku")
