import os.path

from multiprocessing import Process
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from logger import log, log_error
from typing import Tuple
AUTH_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


class Connection:

    def __init__(self):
        self.creds = None
        self.service = None

    def __get_row_and_column__(self, cell: str) -> Tuple[str, str]:
        # this function doesnt work with cell with more than one letter
        row = ""
        i = 0
        while cell[i].isalpha():
            row += cell[i]
            i += 1
        column = cell[i:]

        return (int(column) - 1, ord(row) - 65)

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
            self.__error_handler__(e, sheet_id, range)

    def _write(self, range: str, sheet_id: str, data: str) -> None:
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
            self.__error_handler__(e, sheet_id, range)

    def write(self, range: str, sheet_id: str, data: str):
        p = Process(target=self._write, args=(
            range, sheet_id, data,), daemon=True)
        p.start()

    def app(self, range: str, sheet_id: str, data: list):
        log(
            f"Appending to table, sheet_id: {sheet_id}, range: {range}, data: {data}")
        body = {"values": data}
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id, valueInputOption="USER_ENTERED", range=range, body=body).execute()
        except HttpError as e:
            self.__error_handler__(e, sheet_id, range)

    def __error_handler__(self, error: HttpError, sheet_id: str, range: str):
        error_code = error.resp["status"]
        match(error_code):
            case "404":
                log_error(f"Error: sheet with id {sheet_id} was not found!")
            case "400":
                log_error(f"Error: range {range} is invalid!")
            case "403":
                log_error(
                    "Error: User have no premission, need reconnection with another account")
            case _:
                log_error("Error: Uknown")
                log_error(error)
        log_error("Exit!")
        exit(0)

    def copy(self, start_cell, end_cell, sheet_id):
        log(f"Coping in sheet {sheet_id} from {start_cell} to {end_cell}")
        start_row, start_column = self.__get_row_and_column__(start_cell)
        end_row, end_column = self.__get_row_and_column__(end_cell)

        source_start_row_index = start_row
        source_end_row_index = start_row + 1
        source_start_column_index = start_column
        source_end_column_index = start_column + 1

        destination_start_row_index = end_row
        destination_end_row_index = end_row + 1
        destination_start_column_index = end_column
        destination_end_column_index = end_column + 1

        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "copyPaste": {
                        "source": {
                            "sheetId": 0,
                            "startRowIndex": source_start_row_index,
                            "endRowIndex": source_end_row_index,
                            "startColumnIndex": source_start_column_index,
                            "endColumnIndex": source_end_column_index
                        },
                        "destination": {
                            "sheetId": 0,
                            "startRowIndex": destination_start_row_index,
                            "endRowIndex": destination_end_row_index,
                            "startColumnIndex": destination_start_column_index,
                            "endColumnIndex": destination_end_column_index
                        },
                        "pasteType": "PASTE_FORMULA"
                    }
                }
            ]
        }
        try:
            self.service.spreadsheets().batchUpdate(spreadsheetId=sheet_id,
                                                    body=batch_update_spreadsheet_request_body).execute()
        except HttpError as e:
            self.__error_handler__(
                e, sheet_id, range=f"{start_cell} -> {end_cell}")


if __name__ == "__main__":
    con = Connection()
    con.connect()
    # data = conn.read("A1:A5", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k")
    # conn.write("A2", "1mVc9THvtGtvRmK1tIaXkzxk2Cgy82BqWMWcRlO_PA6k", "yyyy")
    con.copy("F18", "F19", "1eaxlXT7RoH5A_sRlgGGSj2oG7aWkVo4dap5EYhDpTBw")
