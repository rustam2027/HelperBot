from dataclasses import dataclass


@dataclass
class Student:
    github: dict
    tg: str
    name: str
    group: str
    chat_id: str


"""
class Student:

    def __init__(self, chat_id: str):
        self.chat_id: str = chat_id
        self.tg: str = ""
        self.github: dict = {}
        self.name: str = ""
        self.group: str = ""
"""
