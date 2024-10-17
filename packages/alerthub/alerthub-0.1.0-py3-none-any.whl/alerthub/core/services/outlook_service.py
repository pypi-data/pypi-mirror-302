# core/services/outlook_service.py
from alerthub.core.base_email_service import BaseEmailService


class OutlookService(BaseEmailService):
    def __init__(self, user_credentials):
        super().__init__(user_credentials)
