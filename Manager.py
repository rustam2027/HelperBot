from typing import List, Dict
from Connection import Connection
from Group import Group
from Student import Student


class Manager:
    groups: Dict[str, Group]
    connection: Connection

    def __init__(self):
        self.connection = Connection()
        self.connection.connect()
        self.groups = dict()
        self.names_range = (5, 27)
        # TODO: Read groups from file
    
    def read_names(self, group: Group) -> None:
        start, end = self.names_range
        random_course_table = list(group.courses.items())[0]
        table = self.connection.read(f"A{start}:B{end}", random_course_table)
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:":
                break
            names.append(Student(None, name[0], group.number, None))
        group.students = names

    def addGroup(self, number: str, courses):
        self.groups[number] = Group(number, [], courses)

    def read_current_tasks(self):
        return None

    def read_tasks(self):
        pass

    def get_students(self, number: str) -> List[Student]:
        group = self.get_group(number)
        return group.students

    def get_group(self, number: str):
        return self.groups[number]

    def get_cell(self, student: Student, group: Group, task: str) -> str:
        students = [st.name for st in group.students]
        position = students.index(student.name)
        return str(self.names_range[0] + position)

    def write(self, student: Student, task: str, course_name: str) -> None:
        group = self.get_group(student.group)
        table_id = group.courses[course_name]
        self.connection.write("C" + self.get_cell(student, group, task), table_id, "п")


if __name__ == "__main__":
    manager = Manager()
    manager.read_names(192392)
    # manager.write()
