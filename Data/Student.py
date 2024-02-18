from dataclasses import dataclass
from typing import List 


@dataclass
class Student:
    github: str
    tg: str
    name: str
    group: str
    tasks: List[str]
