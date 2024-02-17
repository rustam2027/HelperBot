from Typing import List
from Connection import Connection


class Manager:
    groups: List[Group]
    connection: Connection

    def __init__(self):
        self.connection = Connection()
        self.connection.connect()
    
    def read_names(self) -> List[str]:
        table = self.connection.read("A5:B27", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")
        print(table)

    def read_current_tasks(self, student):
        pass

    def read_tasks(self):
        pass

    
if __name__ == "__main__":
    manager = Manager()
    manager.

        