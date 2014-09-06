from twilio.rest import TwilioRestClient
import project.utils.reminders

ACCOUNT_SID = "ayylmao"
AUTH_TOKEN = "ayylmao"

def send_reminder(text, phone):
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(to=phone, from_="+15172194225", body=text)

def send_all_reminders():
    x = project.utils.reminders.get_needed_reminders()
    print("Sending %d reminders" % len(x))
    for i in x:
        send_reminder(i.text, i.phone)

send_all_reminders()
