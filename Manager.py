import glob
import json
from typing import List, Dict, Tuple

from Connection import Connection

from Data.Course import Course
from Data.Group import Group
from Data.Student import Student

from logger import log


class Manager:
    groups: Dict[str, Group]
    connection: Connection

    def __init__(self):
        log("Initing Manager")

        self.connection = Connection()
        self.connection.connect()
        self.groups = {}
        self._init_groups()
        self.names_range = (5, 60)
        self.internal_start = 2

        for group in self.groups.keys():
            self._read_names_(self.groups[group])

    def _init_groups(self) -> None:
        log(f"Manager: init groups from init_1.json")

        for filename in glob.glob('AdminData/*.json'):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                group, course = data['group'], data['course']
                course_to_add = Course(course, None, data['id_out'], data['id_in'])
                if group in self.groups:
                    courses = self.groups[group].courses
                    if course not in courses:
                        courses[course] = course_to_add
                else:
                    self.groups[group] = Group(group, None, {course: course_to_add})

    def _read_names_(self, group: Group) -> None:
        log(f"Manager: Reading names for group {group.number}")

        start, end = self.names_range
        random_course_table = list(group.courses.values())[0].table_id_students
        table = self.connection.read(f"A{start}:B{end}", random_course_table)
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:" or name[0] == "Максимальный балл за задачу":
                break
            names.append(Student({}, "", name[0], group.number, []))
        group.students = names

    def addGroup(self, number: str, courses):
        log(f"Manager: adding group {number} with courses {courses}")

        self.groups[number] = Group(number, [], courses)

    def read_current_tasks(self, student: Student, course_name: str):
        log(
            f"Manager: Reading current tasks for student {student.name}, for course {course_name}")

        group = self.groups[student.group]
        students = group.students

        all_tasks = self.read_tasks(group, course_name)
        i = 0
        for i in range(len(students)):
            if students[i].name == student.name:
                break
        num = i
        start, _ = self.names_range

        result = self.connection.read(
            f"C{start + num}:S{start + num}", group.courses[course_name].table_id_students)[0]

        answer = []
        for i in range(len(all_tasks)):
            if i >= len(result) or result[i] == "":
                answer.append(all_tasks[i])
        return answer

    def read_tasks(self, group: Group, name: str) -> List:
        log(f"Manager: Reading tasks for group {group.number} course {name}")
        result = self.connection.read(
            "C3:AA4", group.courses[name].table_id_students)

        tasks_list = []
        i = 0
        while i < len(result[0]) and result[0][i].isdigit():
            tasks_list.append(result[0][i])
            i += 1
        return tasks_list

    def get_students(self, number: str) -> List[Student]:
        group = self.groups[number]
        return group.students

    def _get_cell_(self, student: Student, group: Group, task: str) -> Tuple[str, str]:
        students = [st.name for st in group.students]
        position = students.index(student.name)
        row = str(self.names_range[0] + position)
        start = "C"
        column = chr(ord(start) + int(task) - 1)
        return row, column

    def receive(self, student: Student, task: str, course_name: str):
        log(f"Manager: Reciecing task {task}, from {student.name}, at course {course_name}")

        group = self.groups[student.group]

        self._write_(student, group, task, course_name, "п")

        table_id = group.courses[course_name].table_id_teachers

        self.connection.app(
            "A2", table_id, [[task, student.name, student.tg, student.github[course_name], "", "не распределена"]])

    def _write_(self, student: Student, group: Group, task: str, course_name: str, value: str) -> None:
        log(f"Manager: Writing for {student.name}, course name {course_name}, number {task} ")

        table_id = group.courses[course_name].table_id_students
        row, column = self._get_cell_(student, group, task)

        self.connection._write(column + row, table_id, value)


def test_1():
    student_1 = Student({"Algorithms": "@HUI"}, "@HUI", "Колбасова Любовь Сергеевна", "22126", None)
    student_2 = Student({"C++": "@HUIII"}, "@HUIII", "Салимов Рустам Аскарович", "22126", None)
    manager.receive(student_1, "4", "Algorithms")
    manager.receive(student_2, "4", "C++")


def test_2():
    student_1 = Student("@hui", {"Algorithms": "@HUII", "C++": "@HUIII"}, "Колбасова Любовь Сергеевна", "22126", None)
    print(manager.read_current_tasks(student_1, "Algorithms"))
    print(manager.read_current_tasks(student_1, "C++"))


def test_3():
    for group in manager.groups.keys():
        for student in manager.groups[group].students:
            print(student)


def test_4():
    print(manager.read_tasks(manager.groups["22126"], "Algorithms"))


if __name__ == "__main__":
    manager = Manager()
    test_1()
    test_2()
    test_3()
    test_4()
