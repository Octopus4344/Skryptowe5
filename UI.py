import logging
from datetime import timedelta

import typer

from zad_1 import file_reader
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import get_message_type
from zad_4 import get_min_max_login, get_random_logs_from_user, get_stats, get_stats_per_user
from zad_6 import brute_force_detector

app = typer.Typer(help="SSH Log Analyzer CLI")


@app.command("zad2b")
def zad2b(logfile: str):
    """
    Get IPv4 addresses from log file
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    for line in logs:
        print(get_ipv4s_from_log(line))


@app.command("zad2c")
def zad2c(logfile: str):
    """
    Get usernames from log file
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    for line in logs:
        user = get_user_from_log(line)
        if user:
            print(user)


@app.command("zad2d")
def zad2d(logfile: str):
    """
    Get message types from log file
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    for line in logs:
        print(get_message_type(line["description"], logging.getLogger()))


@app.command("zad4a")
def zad4a(logfile: str, user: str, count: int):
    """
    Get random logs from user
    :param logfile:
    :param user:
    :param count:
    :return:
    """
    logs = file_reader(logfile)
    for log in get_random_logs_from_user(logs, user, count):
        print(log)


@app.command("zad4b1")
def zad4b1(logfile: str):
    """
    Get global statistics
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    print(get_stats(logs))


@app.command("zad4b2")
def zad4b2(logfile: str):
    """
    Get statistics per user
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    for user, stats in get_stats_per_user(logs).items():
        print(f"{user}: {stats}")


@app.command("zad4c")
def zad4c(logfile: str):
    """
    Get min and max login users
    :param logfile:
    :return:
    """
    logs = file_reader(logfile)
    min_login, max_login = get_min_max_login(logs)
    print(f"Min log-ins: {min_login}")
    print(f"Max log-ins: {max_login}")


@app.command("zad6")
def zad6(logfile: str, max_interval: int, single_user_name: bool = False):
    """
    Brute force detector
    :param logfile:
    :param max_interval:
    :param single_user_name:
    :return:
    """
    logs = file_reader(logfile)
    for log in brute_force_detector(logs, timedelta(max_interval), single_user_name):
        print(log)


def main(logfile: str, loglevel: str = typer.Option("none", "--loglevel", "-l", help="Set the minimum logging level")):
    """
    Main function
    :param logfile:
    :param loglevel:
    :return:
    """
    if loglevel == "none":
        logging.disable(logging.CRITICAL + 1)
    else:
        logging.basicConfig(level=getattr(logging, loglevel.upper()))

    typer.echo(f"Processing logfile: {logfile}")


if __name__ == "__main__":
    app()
