import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

AUTH_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]



class Connection:

    def __init__(self):
        self.creds = None
        self.service = None


    def connect(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", AUTH_SCOPE)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", AUTH_SCOPE
                )
                self.creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(self.creds.to_json())

        self.service = build("sheets", "v4", credentials=self.creds)


    def read_names(self, range: str, sheet_id: str):
        resp = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range).execute()
        print(resp)



if __name__ == "__main__":
    conn = Connection()
    conn.connect()
    conn.read_names("A1:C2", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")

        

