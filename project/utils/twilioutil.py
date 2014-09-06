from twilio.rest import TwilioRestClient
ACCOUNT_SID = "ayylmao"
AUTH_TOKEN = "ayylmao"

def send_text(phone, text):
    client = TwilioRestClient(ACCOUxtNT_SID, AUTH_TOKEN)
    client.messages.create(to=phone, from_="+15172194225", body=text)
