from google.oauth2 import service_account
from googleapiclient.discovery import build


class CalendarManager:
    def __init__(self, credentials_file, scopes):
        self.credentials_file = credentials_file
        self.scopes = scopes

    def connect_to_api(self):
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=self.scopes
        )
        service = build('calendar', 'v3', credentials=creds)
        return service

    def create_event(self, service, event):
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event['id']
}