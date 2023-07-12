from realestate.models import ScheduleMaintaines, ScheduleMaintainesStatue
from utils.twillo_client import message, TwilloClient
from datetime import datetime
from RMS import settings
from realestate.emails import MaintainceReminderEmail
from accounts.models import Notification


def maintains_notification():
    
    object = ScheduleMaintaines.objects.filter(status=ScheduleMaintainesStatue.ACTIVE)

    twillo = TwilloClient(settings.TWILLIO_SID,settings.TWILLIO_TOKEN)
    for item in object:
        if item.create==datetime.today() or item.reminder_date==datetime.today():
            to = item.real_estate.user.mobile_number
            username = item.real_estate.user.username
            asset = item.asset.name
            realestate = item.real_estate.name
            body = f"Dear {username} ,Scheduled maintenance for  {asset} in {realestate} is due today, please update the maintenance status or change the maintenance date, from Modify Schedule Maintenance Feature"

            #send sms to phone
            twillo.send_sms(body,to)

            #send email to user email
            MaintainceReminderEmail(context={'user':item.real_estate.user}).send([item.real_estate.user.email])

            #create notification 
            Notification.objects.create(
                subject = 'Schedule Maintains Reminder',
                body = body,
                to = item.real_estate.user
            )


