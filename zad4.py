import random

from zad_1 import file_reader
from zad_2_c import get_user_from_log


def get_random_logs_from_user(logs, user, n):
    logs_from_user = group_logs_by_user(logs).get(user)
    return random.sample(logs_from_user, min(n, len(logs_from_user)))


def get_stats_global(logs):
    for log in logs:




def get_stats_per_user(logs):
    pass


def get_min_max_login(logs):
    pass


def group_logs_by_user(logs):
    user_dict = {}

    for log in logs:
        user = get_user_from_log(log)
        if user is not None:
            if user not in user_dict:
                user_dict[user] = []
            user_dict[user].append(log)

    return user_dict


if __name__ == "__main__":
    # 4a
    for log in get_random_logs_from_user(file_reader("SSH_2k.log"), "matlab", 5):
        print(log)
