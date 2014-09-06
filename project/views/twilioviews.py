from flask import request
import requests
from ..utils.status import get_status
from ..utils.reminders import create_reminder
import twilio.twiml
import json
from datetime import datetime

def call():
    resp = twilio.twiml.Response()
    resp.record(timeout=10, transcribe=True,
            transcribeCallback='http://queri.me/rec', )
    return str(resp)

def text():
    b = request.form.get('Body','')
    phone = request.form.get('From','')
    wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % b, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
    intent = json.loads(wit)['outcomes'][0]['intent']
    if intent == 'get_status':
        m = get_status(wit, phone)
    elif intent == 'remind':
        entities = json.loads(wit)['outcomes'][0]['entities']
        date = datetime.strptime(entities['time'][0]['value']['from'],"%Y-%m-%dT%H:%M:%S.Z")
        text = entities['message']
        m = create_reminder(date, text, phone)
    else:
        m = "Hmm? Try again please :("

    m = get_status(wit, phone)
    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

def rec():
    print request.form.get('TranscriptionText','')
    return ''
