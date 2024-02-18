class Student:

    def __init__(self, chat_id: str):
        self.chat_id: str = chat_id
        self.tg: str = ""
        self.github_urls: dict = {}
        self.name: str = ""
        self.group: str = ""
