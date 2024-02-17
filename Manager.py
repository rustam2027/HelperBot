from typing import List
from Connection import Connection
from Group import Group
from Student import Student


class Manager:
    groups: List[Group]
    connection: Connection

    def __init__(self):
        self.connection = Connection()
        self.connection.connect()
        self.groups = []
        # TODO: Read groups from file

    def addGroup(self, number: str, courses):
        self.groups.append(Group(number, [], courses))

    def read_names(self) -> List[str]:
        table = self.connection.read(
            "A5:B30", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")
        
        print(table)

    def read_current_tasks(self, student):
        pass

    def read_tasks(self):
        pass

    def get_students(self, number: str) -> List[Student]:
        for group in self.groups:
            if group.number == number:
                return group.students
        return None


if __name__ == "__main__":
    manager = Manager()
    manager.read_names()
