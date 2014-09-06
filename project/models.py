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
    email = Column(String(64))
    pwhash = Column(String(128))
    reg_uuid = Column(String(37))
    enabled = Column(Boolean)
    phone = Column(String(24))

    def __init__(self, username=None, email=None, pwhash=None, reg_uuid=None, enabled=True,
            phone=None):
        self.username = username
        self.email = email
        self.pwhash = pwhash
        self.reg_uuid = reg_uuid
        self.enabled = enabled
        self.phone = phone

    def __repr__(self):
        return "<User '%s' (id %d), phone: %s, enabled: %s" % (self.username,
                self.uid, self.phone, self.enabled)

class Alias(Base):
    __tablename__ = 'aliases'
    aid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    _from = Column(String(64))
    to = Column(String(64))

    def __init__(self, uid=None, _from=None, to=None):
        self.uid = uid
        self._from = _from
        self.to = to

    def __repr__(self):
        return "<Alias %s to %s (uid %d)" % (self._from, self.to, self.uid)

class Phone(Base):
    __tablename__ = 'phones'
    pid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    phone_number = Column(String(24))
    confirmation = Column(String(7))
    is_confirmed = Column(Boolean)

    def __init__(self, uid=None, phone_number=None, confirmation=None):
        self.uid = uid
        self.phone_number = phone_number
        self.confirmation = confirmation
        self.is_confirmed = False

    def __repr__(self):
        return "<Phone (who_was=%d) %s confirm %s>" % (self.uid, self.phone_number, self.confirmation)
