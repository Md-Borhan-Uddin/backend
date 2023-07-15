from realestate.models import ScheduleMaintaines
from utils.twillo_client import message
from RMS.settings import TWILLIO_NUMBER


def notification():
    print('create membership')
    message('hi borhan',TWILLIO_NUMBER,'+966 55 507 5609')