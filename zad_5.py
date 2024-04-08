import argparse
import logging

from zad_1 import file_reader
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log


def main():
    parser = argparse.ArgumentParser(description="SSH Log Analyzer CLI")

    # Argumenty
    parser.add_argument("logfile", help="Path to the SSH log file")
    parser.add_argument("-l", "--loglevel",
                        choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL],
                        help="Set the minimum logging level", default=logging.INFO)

    # Podkomendy
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Podkomenda dla zadania 2b
    parser_task2b = subparsers.add_parser("task2b", help="Perform actions from task 2b")

    # Podkomenda dla zadania 2c
    parser_task2c = subparsers.add_parser("task2c", help="Perform actions from task 2c")

    # Podkomenda dla zadania 2d
    parser_task2d = subparsers.add_parser("task2d", help="Perform actions from task 2d")

    args = parser.parse_args()

    # Przekazanie argumentów i podkomend do odpowiednich funkcji
    logging.disable(args.loglevel)
    if args.subcommand == "task2b":
        for line in file_reader("SSH_2k.log"):
            print(get_ipv4s_from_log(line))
    elif args.subcommand == "task2c":
        for line in file_reader("SSH_2k.log"):
            user = get_user_from_log(line)
            if user:
                print(user)


if __name__ == "__main__":
    main()
