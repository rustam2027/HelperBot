from dataclasses import dataclass
from typing import Dict


@dataclass
class Student:
    github: Dict[str, str]
    tg: str
    name: str
    group: str
    chat_id: str
