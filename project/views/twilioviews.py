from flask import request
import requests
from ..utils.status import get_status
from ..utils.reminders import create_reminder
import twilio.twiml
import json
import dateutil

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
    print json.loads(wit)
    if intent == 'get_status':
        m = get_status(wit, phone)
    elif intent == 'remind':
        try:
            entities = json.loads(wit)['outcomes'][0]['entities']
            date = dateutil.parser.parse(entities['time'][0]['value']['from'])
            text = entities['message'][0]['value']
            m = create_reminder(date, text, phone)
        except Exception, e:
            print str(e)
    else:
        m = "Hmm? Try again please :("

    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

def rec():
    print request.form.get('TranscriptionText','')
    return ''
