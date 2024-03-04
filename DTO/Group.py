from typing import List, Dict
from dataclasses import dataclass
from DTO.Student import Student
from DTO.Course import Course


@dataclass
class Group:
    number: str
    students: List[Student] | None
    courses: Dict[str, Course]
