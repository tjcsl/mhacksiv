from sqlalchemy import Column, Integer, String, DateTime
from project.database import Base

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(String(1024))

    def __init__(self, date=None, text=None):
        self.date = date
        self.text = text

    def __repr__(self):
        return "<Reminder on %s (%s)>" % (self.date, self.text)
