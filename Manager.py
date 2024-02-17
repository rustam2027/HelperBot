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
    
    def read_names(self, group: Group) -> List[str]:
        table = self.connection.read("A5:B27", group.courses[0][1])
        names = []
        for name in table:
            if name[0] == "Вольнослушатели:":
                break
            names.append(Student(None, name[0], group.number, None))
        group.students = names
        print(names)

    def read_current_tasks(self, student):
        return None

    def read_tasks(self):
        pass

    
if __name__ == "__main__":
    manager = Manager()
    manager.read_names(192392)



        