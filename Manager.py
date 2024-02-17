from typing import List, Dict, Tuple
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
        group = self.groups[number]
        return group.students

    def get_cell(self, student: Student, group: Group, task: str) -> Tuple[str, str]:
        students = [st.name for st in group.students]
        position = students.index(student.name)
        row = str(self.names_range[0] + position)
        start = "C"
        column = chr(ord(start) + int(task) - 1)
        return row, column

    def write(self, student: Student, task: str, course_name: str) -> None:
        group = self.groups[student.group]
        table_id = group.courses[course_name].table_id_students
        row, column = self.get_cell(student, group, task)
        self.connection.write(column + row, table_id, "п")


if __name__ == "__main__":
    manager = Manager()
    # manager.read_names(192392)
    student = Student("", "Волк Александр Николаевич", "22126", [])


    # manager.write()
