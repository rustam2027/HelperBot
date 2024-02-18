from typing import List, Dict
from dataclasses import dataclass
from Data.Student import Student
from Data.Course import Course


@dataclass
class Group:
    number: str
    students: List[Student]
    courses: Dict[str, Course]

