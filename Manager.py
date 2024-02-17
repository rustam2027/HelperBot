from typing import List, Dict, Tuple
from Connection import Connection
from Course import Course
from Group import Group
from Student import Student


class Manager:
    groups: Dict[str, Group]
    connection: Connection

    def __init__(self):
        self.connection = Connection()
        self.connection.connect()
        self.groups = {"22126": Group("", [], {"A": Course("A", [], "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k", "")})}
        self.names_range = (5, 27)
        # TODO: Read groups from file
    
    def read_names(self, group: Group) -> None:
        start, end = self.names_range
        random_course_table = group.courses["A"].table_id_students
        table = self.connection.read(f"A{start}:B{end}", random_course_table)
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:":
                break
            names.append(Student("", name[0], group.number, []))
        group.students = names

    def addGroup(self, number: str, courses):
        self.groups[number] = Group(number, [], courses)

    def read_current_tasks(self, student: Student, course_name: str):
        group = self.groups[student.group]
        tasks: List[int] = self.read_tasks(group, course_name)


    def read_tasks(self, group: Group, name: str):
        result = self.connection.read("C3:AA4", group.courses[name].table_id_students)
        print(result[0])  # May be error
        tasks_list = []
        i = 0
        while i < len(result[0]) and result[0][i].isdigit():
            tasks_list.append(result[0][i])
            i += 1
        print(tasks_list)
        return tasks_list

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
    manager.read_tasks(manager.groups["22126"], "A")
    manager.read_names(manager.groups["22126"])
    student = Student("", "Васько Мария Богдановна", "22126", [])
    manager.write(student, "1", "A")
