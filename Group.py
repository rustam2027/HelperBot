from typing import List,  Dict
from dataclasses import dataclass
from Student import Student


@dataclass
class Group:
    number: str
    students: List[Student]
    courses: Dict

    def get_semester(self):
        admission_year = self.number[0:1]
        # TODO: get correct semester
        return 2

    def get_course_list(self) -> list[str]:
        semester = self.get_semester()
        match semester:
            case 1:
                return ['Python', 'C', 'ИСП']
            case 2:
                return ['Алгоритмы и структуры данных', 'АрхЭВМиНуП']
            case 3:
                pass
            case 4:
                pass
