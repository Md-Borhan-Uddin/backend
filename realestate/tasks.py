from django.utils import timezone

from accounts.models import Notification
from realestate.emails import MaintainceReminderEmail
from realestate.models import ScheduleMaintaines, ScheduleMaintainesStatue
from RMS import settings
from utils.twillo_client import TwilloClient


def maintains_notification():
    object = ScheduleMaintaines.objects.filter(status=ScheduleMaintainesStatue.ACTIVE)

    twillo = TwilloClient(settings.TWILLIO_SID, settings.TWILLIO_TOKEN)
    for item in object:
        if item.create <= timezone.now() or item.reminder_date <= timezone.now():
            to_phone = item.real_estate.user.mobile_number
            username = item.real_estate.user.username
            asset = item.asset.name
            realestate = item.real_estate.name
            if item.create <= timezone.now():
                body = f"Dear {username} ,Scheduled maintenance for  {asset} in {realestate} is due today, please update the maintenance status or change the maintenance date, from Modify Schedule Maintenance Feature"

            elif item.reminder_date == timezone.now():
                body = f"Dear {username}, Scheduled reminder for {asset} in {realestate} maintenance is today, please remember the maintenance date is {item.maintain_date}, and you can update the scheduled maintenance from Modify Schedule Maintenance Feature"
            # send sms to phone
            twillo.send_sms(body, to_phone)

            # send email to user email
            MaintainceReminderEmail(
                context={
                    "user": item.real_estate.user,
                    "username": username,
                    "asset": asset,
                    "realestate_name": realestate,
                    "body": body,
                }
            ).send([item.real_estate.user.email])

            # create notification
            Notification.objects.create(
                subject="Schedule Maintains Reminder",
                body=body,
                to=item.real_estate.user,
            )
