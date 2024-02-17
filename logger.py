import datetime


def log(string: str) -> None:
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]: {string}")
