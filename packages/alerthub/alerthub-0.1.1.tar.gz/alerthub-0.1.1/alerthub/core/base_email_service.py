from abc import ABC, abstractmethod

class BaseEmailService(ABC):
    def __init__(self, user_credentials):
        self.user_credentials = user_credentials
    
    @abstractmethod
    def send_email(self, subject, body, to_addresses, cc_addresses=None, bcc_addresses=None, attachments=None):
        pass

    @abstractmethod
    def monitor_emails(self, folder='inbox', filters=None):
        pass

    @abstractmethod
    def delete_email(self, email_id):
        pass

    @abstractmethod
    def move_email(self, email_id, destination_folder):
        pass

    @abstractmethod
    def forward_email(self, email_id, to_addresses, additional_message=None):
        pass

    @abstractmethod
    def reply_email(self, email_id, message, reply_all=False):
        pass
