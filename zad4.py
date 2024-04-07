import random

from zad_1 import file_reader
from zad_2_c import get_user_from_log


def get_random_logs_from_user(logs, user, n):
    logs_from_user = []
    for log in logs:
        if get_user_from_log(log) == user:
            logs_from_user.append(log)
    return random.sample(logs_from_user, min(n, len(logs_from_user)))


if __name__ == "__main__":
    for log in get_random_logs_from_user(file_reader("SSH.log"), "matlab", 5):
        print(log)
