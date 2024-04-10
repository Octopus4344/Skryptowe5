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
    connection_times = []
    open_time, close_time = None, None

    for log in logs:
        message_type = get_message_type(log["description"], logging.getLogger())

        if message_type == LogMessageType.CONNECTION_OPENED and open_time is None:
            open_time = log["time"]
        elif message_type == LogMessageType.CONNECTION_CLOSED and open_time is not None:
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
    users_logs = group_logs_by_user(logs)
    users_stats = {}

    for user, logs in users_logs.items():
        stats = get_stats(logs)
        if stats != (0, 0):
            users_stats[user] = stats

    return users_stats


def get_min_max_login(logs):
    users_logs = group_logs_by_user(logs)

    min_login = None
    min_login_users = []
    max_login = None
    max_login_users = []

    for user, logs in users_logs.items():
        login_times = 0
        for log in logs:
            message_type = get_message_type(log["description"], logging.getLogger())
            if message_type == LogMessageType.SUCCESSFUL_LOGIN:
                login_times += 1

        if min_login is None or login_times < min_login:
            min_login = login_times
            min_login_users = [user]
        elif login_times == min_login:
            min_login_users.append(user)

        if max_login is None or login_times > max_login:
            max_login = login_times
            max_login_users = [user]
        elif login_times == max_login:
            max_login_users.append(user)

    return min_login_users, max_login_users


def group_logs_by_user(logs):
    user_dict = {}

    for log in logs:
        user = get_user_from_log(log)
        if user is not None:
            if user not in user_dict:
                user_dict[user] = []
            user_dict[user].append(log)

    return user_dict


def group_logs_by_ip(logs):
    ips_dict = {}

    for log in logs:
        ip = get_ipv4s_from_log(log)
        if ip is not None and len(ip) == 1:
            index = ip[0]
            if index not in ips_dict:
                ips_dict[index] = []
            ips_dict[index].append(log)

    for ip in ips_dict:
        valid_logs = [log for log in ips_dict[ip] if log.get("time") is not None]

        ips_dict[ip] = sorted(valid_logs, key=lambda x: x["time"])

    return ips_dict


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)

    # 4a
    # for log in get_random_logs_from_user(file_reader("SSH_2k.log"), "matlab", 5):
    #     print(log)

    # 4b1
    print(get_stats(file_reader("SSH_2k.log")))

    # 4b2
    # for user, stats in get_stats_per_user(file_reader("SSH.log")).items():
    #     print(f"User: {user}, Mean: {stats[0]}, Stdev: {stats[1]}")

    # 4c
    # min_login, max_login = get_min_max_login(file_reader("SSH.log"))
    # print(f"Min log-ins: {min_login}")
    # print(f"Max log-ins: {max_login}")
