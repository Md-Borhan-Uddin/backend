
from templated_mail.mail import BaseEmailMessage


class MembershipReminderEmail(BaseEmailMessage):
    template_name = "emails/membership_reminder.html"

