from flask import request
import requests
from ..utils.status import get_status
import twilio.twiml

def call():
    resp = twilio.twiml.Response()
    resp.record(timeout=10, transcribe=True,
            transcribeCallback='http://mhacksiv.herokuapp.com/rec', )
    return str(resp)

def text():
    b = request.form.get('Body','')
    phone = request.form.get('From','')
    wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % b, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
    m = get_status(wit, phone)
    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

def rec():
    print request.form.get('TranscriptionText','')
    return ''
