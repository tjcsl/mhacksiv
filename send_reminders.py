import project.utils.reminders
import project.utils.twilio

def send_all_reminders():
    x = project.utils.reminders.get_needed_reminders()
    print("Sending %d reminders" % len(x))
    for i in x:
        project.utils.twilio.send_text(i.phone, i.text)

send_all_reminders()
