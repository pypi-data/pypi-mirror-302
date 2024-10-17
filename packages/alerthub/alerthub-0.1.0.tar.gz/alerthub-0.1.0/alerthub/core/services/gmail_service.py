# core/services/gmail_service.py
from alerthub.core.base_email_service import BaseEmailService
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64

class GmailService(BaseEmailService):
    def __init__(self, user_credentials):
        """
        Initializes the GmailService with the provided user credentials.
        Validates and attempts to establish a connection to Gmail using OAuth2.
        
        :param user_credentials: A dictionary containing 'client_id', 'client_secret', and 'refresh_token'.
        """
        super().__init__(user_credentials)
        print("user_credentials", user_credentials)

        self.client_id = user_credentials.get('client_id')
        self.client_secret = user_credentials.get('client_secret')
        self.refresh_token = user_credentials.get('refresh_token')
        
        # Validate credentials
        self._validate_credentials()

        # Establish Gmail service connection
        self.service = self._connect_to_gmail()


    def _validate_credentials(self):
        """
        Validates the Gmail credentials to ensure all required fields are present.
        Raises an exception if any required field is missing.
        """
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Invalid Gmail credentials: 'client_id', 'client_secret', and 'refresh_token' are required.") 
        

    def _connect_to_gmail(self):
        """
        Establishes a connection to the Gmail service using OAuth2 credentials.
        Returns the Gmail service instance.
        """
        try:
            # Create credentials object
            credentials = Credentials(
                None,
                refresh_token=self.refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret,
                token_uri="https://oauth2.googleapis.com/token"
            )

            # Refresh the token if necessary
            credentials.refresh(Request())

            # Build the Gmail service using the refreshed credentials
            service = build('gmail', 'v1', credentials=credentials)
            return service
        
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Gmail: {e}")

    def send_email(self, subject, body, to_addresses, cc_addresses=None, bcc_addresses=None, attachments=None):
        """
        Sends an email with the provided subject, body, and recipients.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            to_addresses (list): List of email addresses to send the email to.
            cc_addresses (list, optional): List of email addresses to CC.
            bcc_addresses (list, optional): List of email addresses to BCC.
            attachments (list, optional): List of file paths to attach.

        Raises:
            ValueError: If the email sending fails.

        Returns:
            None
        """
        try:
            message = MIMEText(body)
            message['to'] = ', '.join(to_addresses)
            message['cc'] = ', '.join(cc_addresses) if cc_addresses else None
            message['bcc'] = ', '.join(bcc_addresses) if bcc_addresses else None
            message['from'] = 'your_email@gmail.com'  # Replace with your email
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            body = {'raw': raw_message}
            self.service.users().messages().send(userId="me", body=body).execute()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def monitor_emails(self, folder='inbox', filters=None):
        # Implementation for monitoring Gmail inbox
        pass

    def delete_email(self, email_id):
        # Implementation for deleting an email in Gmail
        pass

    def move_email(self, email_id, destination_folder):
        # Implementation for moving an email to a different folder
        pass

    def forward_email(self, email_id, to_addresses, additional_message=None):
        # Implementation for forwarding an email
        pass

    def reply_email(self, email_id, message, reply_all=False):
        # Implementation for replying to an email
        pass
