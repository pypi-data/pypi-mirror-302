# core/email_service_manager.py
from alerthub.core.services.gmail_service import GmailService
from alerthub.core.services.outlook_service import OutlookService
from alerthub.core.services.sendgrid_service import SendGridService
from alerthub.core.services.smtp_service import SMTPService

from alerthub.utils import constants

class EmailServiceManager:
    def __init__(self, service_type, user_credentials): 
        """
        Initializes the EmailServiceManager with the specified service type and user credentials.

        :param service_type: A string representing the type of email service to be used.
                            Possible values are 'gmail', 'outlook', 'sendgrid', and 'smtp'.
        :param user_credentials: A dictionary containing credentials required for the 
                                selected email service.
        """
        self.service = self._initialize_service(service_type, user_credentials)

    def _initialize_service(self, service_type, user_credentials):
        """
        Initializes an instance of the requested email service with the provided user credentials.

        :param service_type: A string representing the type of email service to be used.
                            Possible values are 'gmail', 'outlook', 'sendgrid', and 'smtp'.
        :param user_credentials: A dictionary containing credentials required for the 
                                selected email service.
        :return: An instance of the requested email service.
        :raises ValueError: If the provided service type is not supported.
        """
        if service_type == constants.CONST_GMAIL:
            return GmailService(user_credentials)
        elif service_type == constants.CONST_OUTLOOK:
            return OutlookService(user_credentials)
        elif service_type == constants.CONST_SENDGRID:
            return SendGridService(user_credentials)
        elif service_type == constants.CONST_SMTP:
            return SMTPService(user_credentials)
        else:
            raise ValueError("Unsupported email service type")

    def send_email(self, *args, **kwargs):
        return self.service.send_email(*args, **kwargs)

    def monitor_emails(self, *args, **kwargs):
        return self.service.monitor_emails(*args, **kwargs)

    def delete_email(self, *args, **kwargs):
        return self.service.delete_email(*args, **kwargs)

    def move_email(self, *args, **kwargs):
        return self.service.move_email(*args, **kwargs)

    def forward_email(self, *args, **kwargs):
        return self.service.forward_email(*args, **kwargs)

    def reply_email(self, *args, **kwargs):
        return self.service.reply_email(*args, **kwargs)
