# AI Executive Assistant

This project is an AI-powered executive assistant that can handle scheduling tasks via email, similar to Clara Labs' assistant.

## Features

- Connects to an email server to fetch and process emails
- Uses natural language processing to tokenize, remove stop words, stem, recognize intent, and extract entities from email text
- Integrates with Google Calendar API to create events
- Manages tasks, including creating, adding, viewing, updating, and removing tasks
- Sends notifications to the user

## User Flow

1. The assistant connects to the email server and fetches new emails.
2. It processes each email by tokenizing the text, removing stop words, stemming the tokens, and extracting intent and entities.
3. Based on the recognized intent, the assistant performs the corresponding action:
   - If the intent is to schedule a meeting, it creates an event in the user's Google Calendar.
   - If the intent is to create a task, it adds the task to the task list.
4. After processing each email, the assistant sends a notification to the user.

## How to Run

1. Install the necessary libraries by running `pip install -r requirements.txt`.
2. Set up the email server connection parameters in the `EmailManager.py` file.
3. Set up the Google Calendar API credentials in the `CalendarManager.py` file.
4. Run the main script by running `python main.py`.

## Note

This is a command-line application. The user interface is a command-line interface and does not have any user prompts. The messages printed to the console are clear and easy to understand.
# assisticate
