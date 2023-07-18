from realestate.models import ScheduleMaintaines
from utils.twillo_client import message
from RMS import settings


def notification():
    print('create membership')
    message('hi borhan',settings.TWILLIO_NUMBER,'+966 55 507 5609')