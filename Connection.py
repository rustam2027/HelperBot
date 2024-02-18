import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from logger import log, log_error

AUTH_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


class Connection:

    def __init__(self):
        self.creds = None
        self.service = None

    def connect(self):
        log("Connecting")
        if os.path.exists("token.json"):
            log("File 'token.json' found!")
            self.creds = Credentials.from_authorized_user_file(
                "token.json", AUTH_SCOPE)
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
        log(f"Reading from table, sheet_id: {sheet_id}, range: {range}")
        try:
            resp = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=range).execute()
            return resp["values"]
        except HttpError as e:
            self.error_handler(e, sheet_id, range)

    def write(self, range: str, sheet_id: str, data: str) -> None:
        log(
            f"Writing to table, sheet_id: {sheet_id}, range: {range}, data: {data}")
        body = {
            'valueInputOption': 'RAW',
            'data': [
                {'range': range, 'values': [[data]]}
            ]
        }
        # can control updates
        try:
            self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=sheet_id, body=body).execute()
        except HttpError as e:
            self.error_handler(e, sheet_id, range)

    def app(self, range: str, sheet_id: str, data: list):
        log(
            f"Appending to table, sheet_id: {sheet_id}, range: {range}, data: {data}")
        body = {"values": data}
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id, valueInputOption="USER_ENTERED", range=range, body=body).execute()
        except HttpError as e:
            self.error_handler(e, sheet_id, range)

    def error_handler(self, error: HttpError, sheet_id: str, range: str):
        error_code = error.resp["status"]
        match(error_code):
            case "404":
                log_error(f"Error: sheet with id {sheet_id} was not found!")
            case "400":
                log_error(f"Error: range {range} is invalid!")
        log_error("Exit!")
        exit(0)


if __name__ == "__main__":
    conn = Connection()
    conn.connect()
    data = conn.read("A1:8A5", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")
    conn.write("A2", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k", "yyyy")
