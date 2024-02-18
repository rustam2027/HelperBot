from typing import List, Dict
from dataclasses import dataclass
from Data.Student import Student
from Data.Course import Course


@dataclass
class Group:
    number: str
    students: List[Student]
    courses: Dict[str, Course]

    def get_semester(self):
        admission_year = self.number[0:2]

        # TODO: get correct semester
        return 2

    def get_course_list(self):
        semester = self.get_semester()

