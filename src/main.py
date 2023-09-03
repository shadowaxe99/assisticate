from EmailManager import EmailManager
from NaturalLanguageProcessor import NaturalLanguageProcessor
from CalendarManager import CalendarManager
from TaskManager import TaskManager
from NotificationManager import NotificationManager


def main():
    # Initialize all managers
    email_manager = EmailManager('imap.gmail.com', 'username', 'password')
    nlp = NaturalLanguageProcessor()
    calendar_manager = CalendarManager('credentials.json', ['https://www.googleapis.com/auth/calendar'])
    task_manager = TaskManager()
    notification_manager = NotificationManager()

    # Connect to email server
    email_manager.connect_to_server()

    # Fetch and parse emails
    email_ids = email_manager.fetch_emails()
    emails = email_manager.parse_emails(email_ids)

    # Process each email
    for email in emails:
        # Tokenize email text
        tokens = nlp.tokenize_text(email.get_payload())

        # Remove stop words
        tokens = nlp.remove_stop_words(tokens)

        # Stem tokens
        tokens = nlp.stem_tokens(tokens)

        # Recognize intent and extract entities
        intent = nlp.recognize_intent(tokens)
        entities = nlp.extract_entities(tokens)

        # Handle intent
        if intent == 'schedule_meeting':
            # Create event in calendar
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
            calendar_manager.create_event(calendar_manager.connect_to_api(), event)

        elif intent == 'create_task':
            # Create task and add it to task list
            task = task_manager.create_task(entities['title'], entities['due_date'], 'pending')
            task_manager.add_task(task)

        # Send notification to user
        notification_manager.send_notification('AI Executive Assistant', 'Processed an email')


if __name__ == '__main__':
    main()
