import argparse
import logging

from zad_1 import file_reader
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import get_message_type
from zad_4 import get_min_max_login
from zad_4 import get_random_logs_from_user
from zad_4 import get_stats
from zad_4 import get_stats_per_user


def main():
    parser = argparse.ArgumentParser(description="SSH Log Analyzer CLI")

    # Argumenty
    parser.add_argument("logfile", help="Path to the SSH log file")
    parser.add_argument("-l", "--loglevel",
                        choices=["debug", "info", "warn", "error", "critical", "none"],
                        help="Set the minimum logging level", default=logging.INFO)

    # Podkomendy
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    subparsers.add_parser("zad2b", help="Get IPv4 addresses from log file")
    subparsers.add_parser("zad2c", help="Get user names from log file")
    subparsers.add_parser("zad2d", help="Get message types from log file")

    zad4a_parser = subparsers.add_parser("zad4a", help="Get random logs from user")
    zad4a_parser.add_argument("user", help="Username to get logs for")
    zad4a_parser.add_argument("count", type=int, help="Number of random logs to retrieve")

    subparsers.add_parser("zad4b1", help="Get global statistics")
    subparsers.add_parser("zad4b2", help="Get statistics per user")
    subparsers.add_parser("zad4c", help="Get min and max login users")

    args = parser.parse_args()

    # Ustawienie poziomu logowania
    if args.loglevel == "none":
        logging.disable(logging.CRITICAL + 1)
    elif args.loglevel == "critical":
        logging.basicConfig(level=logging.CRITICAL)
    elif args.loglevel == "error":
        logging.basicConfig(level=logging.ERROR)
    elif args.loglevel == "warn":
        logging.basicConfig(level=logging.WARNING)
    elif args.loglevel == "info":
        logging.basicConfig(level=logging.INFO)
    elif args.loglevel == "debug":
        logging.basicConfig(level=logging.DEBUG)

    # Przekazanie argumentów i podkomend do odpowiednich funkcji
    logs = file_reader(args.logfile)
    if args.subcommand == "zad2b":
        for line in logs:
            print(get_ipv4s_from_log(line))
    elif args.subcommand == "zad2c":
        for line in logs:
            user = get_user_from_log(line)
            if user:
                print(user)
    elif args.subcommand == "zad2d":
        for line in logs:
            print(get_message_type(line["description"], logging.getLogger()))
    elif args.subcommand == "zad4a":
        for log in get_random_logs_from_user(logs, args.user, args.count):
            print(log)
    elif args.subcommand == "zad4b1":
        print(get_stats(logs))
    elif args.subcommand == "zad4b2":
        for user, stats in get_stats_per_user(logs).items():
            print(f"{user}: {stats}")
    elif args.subcommand == "zad4c":
        min_login, max_login = get_min_max_login(logs)
        print(f"Min log-ins: {min_login}")
        print(f"Max log-ins: {max_login}")


if __name__ == "__main__":
    main()