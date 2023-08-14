
from templated_mail.mail import BaseEmailMessage


class MaintainceReminderEmail(BaseEmailMessage):
    template_name = "emails/maintains_reminder.html"


