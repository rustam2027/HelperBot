from Typing import List
from Connection import Connection
from Group import Group


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

