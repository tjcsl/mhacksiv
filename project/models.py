from sqlalchemy import Column, Integer, String, DateTime, Boolean
from project.database import Base

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(String(1024))
    phone = Column(String(24))

    def __init__(self, date=None, text=None, phone=None):
        self.date = date
        self.text = text
        self.phone = phone

    def __repr__(self):
        return "<Reminder on %s (%s)>" % (self.date, self.text)

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key = True)
    username = Column(String(32))
    pwhash = Column(String(128))
    reg_uuid = Column(String(37))
    enabled = Column(Boolean)
    phone = Column(String(24))

    def __init__(self, username=None, pwhash=None, reg_uuid=None, enabled=True,
            phone=None):
        self.username = username
        self.pwhash = pwhash
        self.reg_uuid = reg_uuid
        self.enabled = enabled
        self.phone = phone

    def __repr__(self):
        return "<User '%s' (id %d), phone: %s, enabled: %s" % (self.username,
                self.uid, self.phone, self.enabled)
