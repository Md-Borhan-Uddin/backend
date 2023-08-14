
from twilio.rest import Client



account_sid = 'ACfb8beb96f6fd2b199a58bae478a225a9'
auth_token = 'b1fab4668370480db43ede744b425e7c'
client = Client(account_sid, auth_token)

def message(body:str,from_number:str, to_number:str):
    res = client.messages.create(
         body=body,
         from_=from_number,
         to=to_number
    )
    print(res)


class TwilloClient:
     def __init__(self,sid,token) -> None:
        self._sid = sid
        self._token = token
        self.client = Client(self._sid, self._token)
     
     def send_sms(self,body,to):
         res = client.messages.create(
         body=body,
         from_='+12343322273',
         to=to
     )
         
        
     

