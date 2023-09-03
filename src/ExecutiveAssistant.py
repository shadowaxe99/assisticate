from EmailManager import EmailManager
from NaturalLanguageProcessor import NaturalLanguageProcessor
from CalendarManager import CalendarManager
from TaskManager import TaskManager
from NotificationManager import NotificationManager
from Scheduler import Scheduler


class ExecutiveAssistant:
    def __init__(self):
        self.email_manager = EmailManager('imap.gmail.com', 'username', 'password')
        self.nlp = NaturalLanguageProcessor()
        self.calendar_manager = CalendarManager('credentials.json', ['https://www.googleapis.com/auth/calendar'])
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager()
        self.scheduler = Scheduler()

    def process_emails(self):
        self.email_manager.connect_to_server()
        email_ids = self.email_manager.fetch_emails()
        emails = self.email_manager.parse_emails(email_ids)

        for email in emails:
            tokens = self.nlp.tokenize_text(email.get_payload())
            tokens = self.nlp.remove_stop_words(tokens)
            tokens = self.nlp.stem_tokens(tokens)

            intent = self.nlp.recognize_intent(tokens)
            entities = self.nlp.extract_entities(tokens)

            if intent == 'schedule_meeting':
                event = {
                    'summary': entities['summary'],
                    'start': {
                        'dateTime': entities['start_time'],
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': entities['end_time'],
                        'timeZone': 'America/Los_Angeles',
                    },
                }
                self.calendar_manager.create_event(self.calendar_manager.connect_to_api(), event)

            elif intent == 'create_task':
                task = self.task_manager.create_task(entities['title'], entities['due_date'], 'pending')
                self.task_manager.add_task(task)

            self.notification_manager.send_notification('AI Executive Assistant', 'Processed an email')

    def schedule_task(self, task):
        self.scheduler.schedule_task(task)

    def reschedule_task(self, task, new_due_date):
        self.scheduler.reschedule_task(task, new_due_date)

    def cancel_task(self, task):
        self.scheduler.cancel_task(task)

    def run(self):
        self.process_emails()


if __name__ == '__main__':
    assistant = ExecutiveAssistant()
    assistant.run()
}