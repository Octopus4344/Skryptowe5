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


def get_stats(logs):
    logger = logging.getLogger()
    # Disable console logging
    logging.disable(logging.CRITICAL)

    connection_times = []
    open_time, close_time = None, None

    for log in logs:
        message_type = get_message_type(log["description"], logger)

        if message_type != LogMessageType.CONNECTION_CLOSED and not open_time:
            open_time = log["time"]
        elif message_type == LogMessageType.CONNECTION_CLOSED and open_time:
            close_time = log["time"]
            connection_times.append((close_time - open_time).total_seconds())
            open_time, close_time = None, None

    if len(connection_times) >= 2:
        return statistics.mean(connection_times), statistics.stdev(connection_times)
    elif len(connection_times) == 1:
        return connection_times[0], 0
    else:
        return 0, 0


def get_stats_per_user(logs):
    users_logs = group_logs_by_ip(logs)
    users_stats = {}

    logger = logging.getLogger()
    # Disable console logging
    logging.disable(logging.CRITICAL)

    for user, logs in users_logs.items():
        users_stats[user] = get_stats(logs)

    return users_stats


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
        valid_logs = [log for log in ips_dict[ip] if log.get("time") is not None]

        ips_dict[ip] = sorted(valid_logs, key=lambda x: x["time"])

    return ips_dict


if __name__ == "__main__":
    # 4a
    # for log in get_random_logs_from_user(file_reader("SSH_2k.log"), "matlab", 5):
    #     print(log)

    # 4b1
    print(get_stats(file_reader("SSH_2k.log")))

    # 4b2
    for user, stats in get_stats_per_user(file_reader("SSH.log")).items():
        print(f"User: {user}, Mean: {stats[0]}, Stdev: {stats[1]}")
