import re


def get_message_type(description):
    if re.search(r'authentication failure', description, re.IGNORECASE):
        return "Nieudane logowanie"
    elif re.search(r'failed password', description, re.IGNORECASE):
        return "Błędne hasło"
    elif re.search(r'invalid user', description, re.IGNORECASE):
        return "Błędna nazwa użytkownika"
    elif re.search(r'possible break-in attempt', description, re.IGNORECASE):
        return "Próba włamania"
    elif re.search(r'connection closed', description, re.IGNORECASE):
        return "Zamknięcie połączenia"
    elif re.search(r'accepted', description, re.IGNORECASE):
        return "Udane logowanie"
    else:
        return "inne"
