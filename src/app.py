from flask import Flask, render_template, request
from EmailManager import EmailManager
from NaturalLanguageProcessor import NaturalLanguageProcessor
from CalendarManager import CalendarManager
from TaskManager import TaskManager
from NotificationManager import NotificationManager

app = Flask(__name__)

email_manager = EmailManager('imap.gmail.com', 'username', 'password')
nlp = NaturalLanguageProcessor()
calendar_manager = CalendarManager('credentials.json', ['https://www.googleapis.com/auth/calendar'])
task_manager = TaskManager()
notification_manager = NotificationManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    user_command = request.form['user_command']

    # Tokenize user command
    tokens = nlp.tokenize_text(user_command)

    # Remove stop words
    tokens = nlp.remove_stop_words(tokens)

    # Stem tokens
    tokens = nlp.stem_tokens(tokens)

    # Recognize intent and extract entities
    intent = nlp.recognize_intent(tokens)
    entities = nlp.extract_entities(tokens)

    # Handle intent
    response = ''
    if intent == 'schedule_meeting':
        # Create event in calendar
        service = calendar_manager.connect_to_api()
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
        calendar_manager.create_event(service, event)
        response = 'Meeting scheduled successfully.'

    elif intent == 'create_task':
        # Create task and add it to task list
        task = task_manager.create_task(entities['title'], entities['due_date'], 'pending')
        task_manager.add_task(task)
        response = 'Task created successfully.'

    # Send notification to user
    notification_manager.send_notification('AI Executive Assistant', response)

    return response

if __name__ == '__main__':
    app.run(debug=True)
