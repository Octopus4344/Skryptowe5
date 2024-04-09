import logging
from datetime import timedelta
from enum import Enum

import typer

from zad_1 import file_reader
from zad_2_b import get_ipv4s_from_log
from zad_2_c import get_user_from_log
from zad_2_d import get_message_type
from zad_4 import get_min_max_login, get_random_logs_from_user, get_stats, get_stats_per_user
from zad_6 import brute_force_detector


class LogLevels(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    NONE = "none"


app = typer.Typer(help="SSH Log Analyzer CLI")
logfile_path = {"path": "SSH.log"}


@app.command("zad2b")
def zad2b():
    """
    Get IPv4 addresses from log file
    """
    logs = file_reader(logfile_path["path"])
    for line in logs:
        print(get_ipv4s_from_log(line))


@app.command("zad2c")
def zad2c():
    """
    Get usernames from log file
    """
    logs = file_reader(logfile_path["path"])
    for line in logs:
        user = get_user_from_log(line)
        if user:
            print(user)


@app.command("zad2d")
def zad2d():
    """
    Get message types from log file
    """
    logs = file_reader(logfile_path["path"])
    for line in logs:
        print(get_message_type(line["description"], logging.getLogger()))


@app.command("zad4a")
def zad4a(user: str = "root", count: int = 3):
    """
    Get random logs from user
    """
    logs = file_reader(logfile_path["path"])
    for log in get_random_logs_from_user(logs, user, count):
        print(log)


@app.command("zad4b1")
def zad4b1():
    """
    Get global statistics
    """
    logs = file_reader(logfile_path["path"])
    print(get_stats(logs))


@app.command("zad4b2")
def zad4b2():
    """
    Get statistics per user
    """
    logs = file_reader(logfile_path["path"])
    for user, stats in get_stats_per_user(logs).items():
        print(f"{user}: {stats}")


@app.command("zad4c")
def zad4c():
    """
    Get min and max login users
    """
    logs = file_reader(logfile_path["path"])
    min_login, max_login = get_min_max_login(logs)
    print(f"Min log-ins: {min_login}")
    print(f"Max log-ins: {max_login}")


@app.command("zad6")
def zad6(max_interval: int = 1, single_user_name: bool = False):
    """
    Brute force detector
    """
    logs = file_reader(logfile_path["path"])
    for log in brute_force_detector(logs, timedelta(max_interval), single_user_name):
        print(log)


@app.callback()
def main(logfile: str = "SSH_2k.log", loglevel: LogLevels = LogLevels.NONE):

    if loglevel == LogLevels.NONE:
        logging.disable(logging.CRITICAL + 1)
    elif loglevel == LogLevels.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    elif loglevel == LogLevels.INFO:
        logging.basicConfig(level=logging.INFO)
    elif loglevel == LogLevels.WARNING:
        logging.basicConfig(level=logging.WARNING)
    elif loglevel == LogLevels.ERROR:
        logging.basicConfig(level=logging.ERROR)
    elif loglevel == LogLevels.CRITICAL:
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.disable(logging.CRITICAL + 1)


    logfile_path["path"] = logfile

    logging.basicConfig(level=loglevel.value)

    typer.echo(f"Processing logfile: {logfile}")


if __name__ == "__main__":
    app()
