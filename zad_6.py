from datetime import timedelta

import zad_1
from zad_2_d import LogMessageType


def brute_force_detector(logs, max_interval: timedelta, single_user_name: bool):
    unsuccessful_logs = []
    try:
        for log in logs:
            if log['message_type'] not in (LogMessageType.OTHER,
                                           LogMessageType.CONNECTION_CLOSED,
                                           LogMessageType.SUCCESSFUL_LOGIN) and log['IPv4']:
                for address in log['IPv4']:
                    unsuccessful_logs=check_IP_address(address, unsuccessful_logs, log, single_user_name, max_interval)
        return remove_single_attempts(unsuccessful_logs)
    except KeyError:
        print("Niewlasciwa lista logów")
        return unsuccessful_logs


def remove_single_attempts(unsuccessful_logs):
    return [log for log in unsuccessful_logs if log['count'] > 1]


def check_if_IPv4_already_on_the_list(address, logs):
    try:
        for index, log in enumerate(logs):
            if log['IPv4'] == address:
                return True, index
        return False, -1
    except KeyError:
        print("Niewlasciwa lista")
        return False, -1


def check_IP_address(address, unsuccessful_logs, log, single_user_name, max_interval):
    address_found, index = check_if_IPv4_already_on_the_list(address, unsuccessful_logs)
    if address_found:
        if log['time'] - unsuccessful_logs[index]['last_time_detected'] > max_interval:
            return unsuccessful_logs
        if single_user_name:
            if unsuccessful_logs[index]['user_name'] != log['user_name']:
                unsuccessful_logs.append({'IPv4': address, 'count': 1, 'user_name': log['user_name'],
                                          'last_time_detected': log['time']})
                return unsuccessful_logs
        unsuccessful_logs[index]['count'] += 1
        unsuccessful_logs[index]['last_time_detected'] = log['time']
    else:
        unsuccessful_logs.append(
            {'IPv4': address, 'count': 1, 'user_name': log['user_name'],
             'last_time_detected': log['time']})
    return unsuccessful_logs



if __name__ == '__main__':
    list = zad_1.file_reader('plik.txt')
    for line in brute_force_detector(list, timedelta(hours=1), True):
        print(line)
