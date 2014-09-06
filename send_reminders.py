from twilio.rest import TwilioRestClient
import project.utils.reminders

ACCOUNT_SID = "AC6a9746370384b26236aae71013aa35b2"
AUTH_TOKEN = "38b0bcc37788e553978c840929d54aa2"

def send_reminder(text, phone):
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(to=phone, from_="+15713646776", body=text)

def send_all_reminders():
    x = project.utils.reminders.get_needed_reminders()
    for i in x:
        send_reminder(i.text, i.phone)

send_all_reminders()
