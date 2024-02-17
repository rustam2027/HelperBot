from typing import List, Dict, Tuple

from Connection import Connection

from Course import Course
from Group import Group
from Student import Student

from logger import log

id_out = "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k"
id_in = "1eaxlXT7RoH5A_sRlgGGSj2oG7aWkVo4dap5EYhDpTBw"


class Manager:
    groups: Dict[str, Group]
    connection: Connection

    def __init__(self):
        log("Initing Manager")
        self.connection = Connection()
        self.connection.connect()
        self.groups = {"22126": Group("", [], {"A": Course("A", [], id_out, "")})}
        self.names_range = (5, 27)
        # TODO: Read groups from file

    def read_names(self, group: Group) -> None:
        log(f"Manager: Reading names for group {group}")
        start, end = self.names_range
        random_course_table = list(group.courses.values())[0].table_id_students
        table = self.connection.read(f"A{start}:B{end}", random_course_table)
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:":
                break
            names.append(Student("", name[0], group.number, []))
        group.students = names

    def addGroup(self, number: str, courses):
        log(f"Manager: adding group {number} with courses {courses}")
        self.groups[number] = Group(number, [], courses)

    def read_current_tasks(self, student: Student, course_name: str):
        group = self.groups[student.group]
        students = group.students
        all_tasks = self.read_tasks(group, course_name)
        for i in range(len(students)):
            if students[i].name == student.name:
                break
        num = i 
        start, end = self.names_range
        result = self.connection.read(f"C{start + num}:S{start + num}", group.courses[course_name].table_id_students)[0]
        answer = []
        for i in range(len(all_tasks)):
            if i >= len(result) or result[i] == "":
                answer.append(all_tasks[i])

        return answer

    def read_tasks(self, group: Group, name: str):
        log(f"Manager: Reading tasks for group {group.number} course {name}")
        result = self.connection.read(
            "C3:AA4", group.courses[name].table_id_students)
        # print(result[0])  # May be error
        tasks_list = []
        i = 0
        while i < len(result[0]) and result[0][i].isdigit():
            tasks_list.append(result[0][i])
            i += 1
        # print(tasks_list)
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
        log(f"Manager: Writing for {student.name}, course name {course_name}, number {task} ")
        group = self.groups[student.group]
        table_id = group.courses[course_name].table_id_students
        row, column = self.get_cell(student, group, task)
        self.connection.write(column + row, table_id, "п")


if __name__ == "__main__":
    manager = Manager()
    manager.read_tasks(manager.groups["22126"], "A")
    manager.read_names(manager.groups["22126"])
    student = Student("", "Колбасова Любовь Сергеевна", "22126", [])
    manager.write(student, "1", "A")
    result = manager.connection.read("F2", id_in)
    print(result)
    print(manager.read_current_tasks(student, "A"))

