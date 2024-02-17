from typing import List, Dict
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
        self.groups = dict()
        self.names_range = (5, 27)
        # TODO: Read groups from file
    
    def read_names(self, group: Group) -> List[str]:
        start, end = self.names_range
        random_course_table = list(group.courses.items())[0]
        table = self.connection.read(f"A{start}:B{end}", random_course_table) # <- полное говно
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:":
                break
            names.append(Student(None, name[0], group.number, None))
        group.students = names
        print(names)


    def addGroup(self, number: str, courses):
        self.groups.append(Group(number, [], courses))

    def read_current_tasks(self, student):
        return None

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
        group = self.get_group(number)
        return group.students

    def get_group(self, number: str):
        for group in self.groups:
            if group.number == number:
                return group
        return None


if __name__ == "__main__":
    manager = Manager()
    manager.read_tasks(Group("", [], {"A": Course("A", [], "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k", "")}), "A")



        
