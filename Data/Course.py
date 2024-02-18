from dataclasses import dataclass
from typing import List


@dataclass
class Course:
    name: str
    tasks: List[str]
    table_id_students: str
    table_id_teachers: str
