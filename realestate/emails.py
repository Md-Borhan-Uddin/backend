from datetime import datetime
from templated_mail.mail import BaseEmailMessage
from realestate.models import ScheduleMaintaines


class MaintainceReminderEmail(BaseEmailMessage):
    template_name = "email/maintains_reminder.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        
        user = context.get("user")
        schedule = ScheduleMaintaines.objects.get(user=user.id,create=datetime.today())
        context["username"] = user.username
        context["asset"] = schedule.asset.name
        context["realestate_name"] = schedule.real_estate.name
        return context

