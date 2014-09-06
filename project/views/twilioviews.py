from flask import request, redirect
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
    resp.say("Hello!")
    with resp.gather(numDigits=1, action="/internal/handle-key", method="POST") as g:
        g.say("To get the status of a machine or set a reminder, press 1.")
    return str(resp)

def handle_key():
    digit_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
    if digit_pressed == "1":
        resp.say("Make your request, then press any key.")
        resp.record(timeout=10, action='http://queri.me/internal/rec')
    elif digit_pressed == "0":
        resp.play("http://a.tumblr.com/tumblr_mascpn4kyJ1qejfr7o1.mp3")
    elif digit_pressed == "4":
        resp.play("http://queri.me/static/MLG.mp3")
    else:
        return redirect('/internal/call')
    return str(resp)

def do_wit(body, phone):
    if not recording:
        wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % body, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
    if recording:
        wit = requests.post('https://api.wit.ai/speech', headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB', 'Content-Type': 'audio/wav'}, files={'file.wav':body}).text
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
    resp = twilio.twiml.Response()
    recording = requests.get(request.form.get('RecordingUrl',''), stream=True).content
    m = do_wit(recording,request.form.get('From',''),recording=True)
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(from_="+15172194225", to=request.form.get('From',''), body=m)
    return ''
