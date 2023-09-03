import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailManager:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    def connect_to_server(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.server)
            self.mail.login(self.username, self.password)
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def fetch_emails(self):
        try:
            self.mail.select('inbox')
            result, data = self.mail.uid('search', None, "ALL")
            return data[0].split()
        except Exception as e:
            print(f"Failed to fetch emails: {e}")

    def parse_emails(self, email_ids):
        emails = []
        for id in email_ids:
            result, data = self.mail.uid('fetch', id, '(BODY[TEXT])')
            raw_email = data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            emails.append(email_message)
        return emails

    def compose_email(self, to, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        return msg.as_string()

    def send_email(self, to, subject, body):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.username, self.password)
            message = self.compose_email(to, subject, body)
            server.sendmail(self.username, to, message)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def reply_to_email(self, email, reply_subject, reply_body):
        try:
            reply_message = self.compose_email(email['From'], reply_subject, reply_body)
            reply_message['In-Reply-To'] = email['Message-ID']
            reply_message['References'] = email['Message-ID']
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, email['From'], reply_message.as_string())
            server.quit()
        except Exception as e:
            print(f"Failed to reply to email: {e}")

    def forward_email(self, email, forward_to):
        try:
            forward_message = self.compose_email(forward_to, email['Subject'], email.get_payload())
            forward_message['In-Reply-To'] = email['Message-ID']
            forward_message['References'] = email['Message-ID']
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, forward_to, forward_message.as_string())
            server.quit()
        except Exception as e:
            print(f"Failed to forward email: {e}")
}