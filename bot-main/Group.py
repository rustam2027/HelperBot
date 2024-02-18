import Student
from typing import List
from dataclasses import dataclass
import Course


@dataclass
class Group:
    number: str
    students: List[Student]
    courses: List[Course]  # name + table_id

    def get_semester(self):
        admission_year = self.number[0:2]

        # TODO: get correct semester
        return 2

    def get_course_list(self):
        semester = self.get_semester()

