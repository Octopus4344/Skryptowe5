import logging
import random
import statistics

from zad_1 import file_reader
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import LogMessageType
from zad_2_d import get_message_type


def get_random_logs_from_user(logs, user, n):
    logs_from_user = group_logs_by_user(logs).get(user)
    return random.sample(logs_from_user, min(n, len(logs_from_user)))


def get_stats_global(logs):
    connection_times = []
    logger = logging.getLogger()
    # Disable console logging
    logging.disable(logging.CRITICAL)

    for log in logs:
        print(log)
        if get_message_type(log["description"], logger) == LogMessageType.SUCCESSFUL_LOGIN:
            break


def get_stats_per_user(logs):
    users_logs = group_logs_by_ip(logs)
    users_stats = {}

    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    # Disable console logging
    logging.disable(logging.CRITICAL)

    for user, logs in users_logs.items():
        connection_times = []
        open_time, close_time = None, None

        for log in logs:
            message_type = get_message_type(log["description"], logger)

            if message_type == LogMessageType.SUCCESSFUL_LOGIN:
                open_time = log["time"]
            if message_type == LogMessageType.CONNECTION_CLOSED:
                close_time = log["time"]
                if open_time and close_time:
                    connection_times.append(close_time - open_time)
                    open_time, close_time = None, None

        if connection_times:
            users_stats[user] = (statistics.mean(connection_times), statistics.stdev(connection_times))
        else:
            users_stats[user] = (0, 0)


def get_min_max_login(logs):
    pass


def group_logs_by_user(logs):
    user_dict = {}

    for log in logs:
        user = get_user_from_log(log)
        if user:
            if user not in user_dict:
                user_dict[user] = []
            user_dict[user].append(log)

    return user_dict


def group_logs_by_ip(logs):
    ips_dict = {}

    for log in logs:
        ip = get_ipv4s_from_log(log)
        if ip and len(ip) == 1:
            index = ip[0]
            if index not in ips_dict:
                ips_dict[index] = []
            ips_dict[index].append(log)

    for ip in ips_dict:
        ips_dict[ip] = sorted(ips_dict[ip], key=lambda x: x["time"])
        for log in ips_dict[ip]:
            log_type = get_message_type(log["description"], logging.getLogger())
            if log_type == LogMessageType.SUCCESSFUL_LOGIN or log_type == LogMessageType.CONNECTION_CLOSED:
                if log["IPv4"] == "119.137.62.142":
                    print(log)
                print(log)

    return ips_dict


if __name__ == "__main__":
    # 4a
    # for log in get_random_logs_from_user(file_reader("SSH_2k.log"), "matlab", 5):
    #     print(log)

    # 4b
    # get_stats_global(file_reader("SSH_2k.log"))

    # 4c
    print(get_stats_per_user(file_reader("SSH_2k.log")))
