import Student
from typing import List
from typing import Tuple
from dataclasses import dataclass
import datetime


@dataclass
class Group:
    number: str
    students: List[Student]
    courses: List[Tuple[str, str]]  # name + table_id

    def get_semester(self):
        admission_year = self.number[0:2]

        # TODO: get correct semester
        return 2

    def get_course_list(self) -> list[str]:
        semester = self.get_semester()

