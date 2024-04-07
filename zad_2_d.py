import re
import logging


def get_message_type(description, logger: logging.Logger):
    if re.search(r'authentication failure', description, re.IGNORECASE):
        logger.warning('Nieudane logowanie w: %s', description)
        return "Nieudane logowanie"
    elif re.search(r'failed password', description, re.IGNORECASE):
        logger.error('Błędne hasło w: %s', description)
        return "Błędne hasło"
    elif re.search(r'invalid user', description, re.IGNORECASE):
        logger.error('Błędna nazwa użytkownika w: %s', description)
        return "Błędna nazwa użytkownika"
    elif re.search(r'possible break-in attempt', description, re.IGNORECASE):
        logger.critical("Próba włamania w: %s", description)
        return "Próba włamania"
    elif re.search(r'connection closed', description, re.IGNORECASE):
        logger.info("Zamknięcie połączenia w: %s", description)
        return "Zamknięcie połączenia"
    elif re.search(r'accepted', description, re.IGNORECASE):
        logger.info("Udane logowanie w: %s", description)
        return "Udane logowanie"
    else:
        return "inne"
