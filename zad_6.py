from zad_2_d import LogMessageType
from datetime import datetime
from datetime import timedelta
import zad_1


def brute_force_detector(logs, max_interval: timedelta, single_user_name: bool):
    unsuccessful_logs = []
    try:
        for log in logs:
            if log['message_type'] in (LogMessageType.OTHER,
                                       LogMessageType.CONNECTION_CLOSED,
                                       LogMessageType.SUCCESSFUL_LOGIN):
                print(log['message_type'], "-prawidlowe logowanie")
                continue
            print(log['message_type'], "-nieudane logowanie")
            for address in log['IPv4']:
                address_found, index = check_if_IPv4_already_on_the_list(address, unsuccessful_logs)
                if address_found:
                    if log['time'] - unsuccessful_logs[index]['last_time_detected'] > max_interval:
                        continue
                    if single_user_name:
                        if unsuccessful_logs[index]['user_name'] != log['user_name']:
                            unsuccessful_logs.append({'IPv4': address, 'count': 1, 'user_name': log['user_name'],
                                                      'last_time_detected': log['time']})
                            continue
                    unsuccessful_logs[index]['count'] += 1
                    unsuccessful_logs[index]['last_time_detected'] = log['time']
                else:
                    unsuccessful_logs.append(
                        {'IPv4': address, 'count': 1, 'user_name': log['user_name'], 'last_time_detected': log['time']})
        return unsuccessful_logs
    except KeyError:
        print("Niewlasciwa lista logów")
        return unsuccessful_logs


def check_if_IPv4_already_on_the_list(address, logs):
    try:
        for index, log in enumerate(logs):
            if log['IPv4'] == address:
                return True, index
        return False, -1
    except KeyError:
        print("Niewlasciwa lista")
        return False, -1


if __name__ == '__main__':
    list = zad_1.file_reader('plik.txt')
    for line in brute_force_detector(list, timedelta(hours=1), False):
        print(line)
