from settings.models import Membership
from realestate.emails import MaintainceReminderEmail
from RMS import settings
from utils.twillo_client import message, TwilloClient
from accounts.models import Notification
from django.utils import timezone
from datetime import timedelta


def membership_notification():
    qs = Membership.objects.get(is_pay=True,expire_date__lt=timezone.now())

    twillo = TwilloClient(settings.TWILLIO_SID,settings.TWILLIO_TOKEN)
    for item in qs:
        date = item.expire_date-timedelta(days=3)
        if date==timezone.now() or item.expire_date==timezone.now():
            to_phone = item.user.mobile_number
            username = item.user.username
            if date==timezone.now():
                body = f"Dear {username}, Your subscribed package will be expired on {item.expire_date}, please do not forget to renew your package or choose one of our available packages so you can use platform’s features"

            elif item.expire_date==timezone.now():
                body = f"Dear {username}, Your subscribed package is expired on {item.expire_date}, please renew your package or choose one of our available packages so you can use platform’s features"
            #send sms to phone
            # twillo.send_sms(body,'01749918181')

            #send email to user email
            MaintainceReminderEmail(context={
                'user':item.user,
                "username": username,
                "body":body
                }).send([item.user.email])

            #create notification 
            Notification.objects.create(
                subject = 'Schedule Maintains Reminder',
                body = body,
                to = item.user
            )
