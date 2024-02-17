import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

AUTH_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


def log(string: str) -> None:
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]: {string}")


class Connection:

    def __init__(self):
        self.creds = None
        self.service = None


    def connect(self):
        log("Connecting")
        if os.path.exists("token.json"):
            log("File 'token.json' found!")
            self.creds = Credentials.from_authorized_user_file("token.json", AUTH_SCOPE)
        if not self.creds or not self.creds.valid:
            log("File 'token.json' not found or not valid!")
            if self.creds and self.creds.expired and self.creds.refresh_token:
                log("Creds not valid")
                self.creds.refresh(Request())
            else:
                log("Creating new creds")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", AUTH_SCOPE
                )
                self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                log("Creating 'token.json'")
                token.write(self.creds.to_json())

        self.service = build("sheets", "v4", credentials=self.creds)


    def read(self, range: str, sheet_id: str):
        resp = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range).execute()
        name_list = [name[0] for name in resp["values"]]
        return name_list       


if __name__ == "__main__":
    conn = Connection()
    conn.connect()
    conn.read_names("A1:A5", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")

        

