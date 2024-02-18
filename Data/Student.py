from dataclasses import dataclass


@dataclass
class Student:
    github: str
    tg: str
    name: str
    group: str


"""
class Student:

    def __init__(self, chat_id: str):
        self.chat_id: str = chat_id
        self.tg: str = ""
        self.github: dict = {}
        self.name: str = ""
        self.group: str = ""
"""
