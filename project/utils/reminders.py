from project.database import db_session
from project.models import Reminder
from datetime import datetime

def create_reminder(date, text, phone):
    x = Reminder(date, text, phone)
    db_session.add(x)
    db_session.commit()
    return "Reminder created."

def get_needed_reminders():
    stuff = Reminder.query.filter(Reminder.date < datetime.now()).all()
    for i in stuff:
        db_session.delete(i)
    db_session.commit()
    return stuff
