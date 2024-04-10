import logging
import re
from enum import Enum


class LogMessageType(Enum):
    FAILED_AUTHENTICATION = "Nieudane logowanie"
    FAILED_PASSWORD = "Błędne hasło"
    INVALID_USER = "Błędna nazwa użytkownika"
    BREAK_IN_ATTEMPT = "Próba włamania"
    CONNECTION_CLOSED = "Zamknięcie połączenia"
    SUCCESSFUL_LOGIN = "Udane logowanie"
    CONNECTION_OPENED = "Otwarcie sesji"
    OTHER = "inne"


def get_message_type(description, logger: logging.Logger):
    if re.search(r'authentication failure', description, re.IGNORECASE):
        logger.warning('Nieudane logowanie w: %s', description)
        return LogMessageType.FAILED_AUTHENTICATION
    elif re.search(r'failed password', description, re.IGNORECASE):
        logger.error('Błędne hasło w: %s', description)
        return LogMessageType.FAILED_PASSWORD
    elif re.search(r'invalid user', description, re.IGNORECASE):
        logger.error('Błędna nazwa użytkownika w: %s', description)
        return LogMessageType.INVALID_USER
    elif re.search(r'possible break-in attempt', description, re.IGNORECASE):
        logger.critical("Próba włamania w: %s", description)
        return LogMessageType.BREAK_IN_ATTEMPT
    elif re.search(r'closed', description, re.IGNORECASE):
        logger.info("Zamknięcie połączenia w: %s", description)
        return LogMessageType.CONNECTION_CLOSED
    elif re.search(r'accepted', description, re.IGNORECASE):
        logger.info("Udane logowanie w: %s", description)
        return LogMessageType.SUCCESSFUL_LOGIN
    elif re.search(r'opened', description, re.IGNORECASE):
        logger.info("Otwarcie sesji w: %s", description)
        return LogMessageType.CONNECTION_OPENED
    else:
        return LogMessageType.OTHER
