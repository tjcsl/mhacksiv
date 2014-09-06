from flask import request
import requests
from ..utils.status import get_status
from ..utils.reminders import create_reminder
import twilio.twiml
from twilio.rest import TwilioRestClient
import json
import dateutil.parser

ACCOUNT_SID = "ayylmao"
AUTH_TOKEN = "ayylmao"

def call():
    resp = twilio.twiml.Response()
    resp.record(timeout=10, transcribe=True,
            transcribeCallback='http://queri.me/internal/rec', )
    return str(resp)

def do_wit(body, phone):
    wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % body, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
    jso = json.loads(wit)
    print str(jso)
    intent = jso['outcomes'][0]['intent']
    if intent == 'get_status':
        m = get_status(wit, phone)
    elif intent == 'remind':
        entities = jso['outcomes'][0]['entities']
        date = dateutil.parser.parse(entities['time'][0]['value']['from'])
        text = entities['message'][0]['value']
        m = create_reminder(date, text, phone)
    else:
        m = "Hmm? Try again please :("
    return m

def text():
    b = request.form.get('Body','')
    phone = request.form.get('From','')
    m = do_wit(b, phone)

    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

def rec():
    print request.form.get('TranscriptionText','')
    m = do_wit(request.form.get('TranscriptionText',''),request.form.get('From',''))
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(from_="+15172194225", to=request.form.get('From',''), body=m)
    return ''
