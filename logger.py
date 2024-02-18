import datetime


WARNING = '\033[91m'
ENDC = '\033[0m'


def log(string: str) -> None:
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]: {string}")


def log_error(string: str) -> None:
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{WARNING}[{time}]: {string}{ENDC}")
