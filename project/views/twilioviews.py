from flask import request, redirect
import requests
from ..utils.status import get_status
from ..utils.reminders import create_reminder
from ..utils.twilioutil import send_text
from ..utils.files import find
import twilio.twiml
from twilio.rest import TwilioRestClient
import json
import dateutil.parser
from flask import request
from project.models import Phone

ACCOUNT_SID = "ayylmao"
AUTH_TOKEN = "ayylmao"

def call():
    resp = twilio.twiml.Response()
    phone = request.form.get("From", "")
    phon = Phone.query.filter(Phone.phone_number == phone).first()
    if phon is None or not phon.is_confirmed:
        send_text(phone, "Register an account at http://queri.me/login/")
        with resp.gather(numDigits=1, action="/internal/handle-key-2", method="POST") as g:
            g.say("Please register your phone number at our website. Check your text messages for a link.")
        return str(resp)

    resp.say("Hello!")
    with resp.gather(numDigits=1, action="/internal/handle-key", method="POST") as g:
        g.say("To get the status of a machine or set a reminder, press 1.")
    return str(resp)

def handle_key_2():
    digit_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
    if digit_pressed == "0":
        resp.play("http://a.tumblr.com/tumblr_mascpn4kyJ1qejfr7o1.mp3")
    elif digit_pressed == "4":
        resp.play("http://queri.me/static/MLG.mp3")
    elif digit_pressed == "2":
        # 22884646#*
        resp.gather(numDigits=9, action="/internal/konami", method="POST", finishOnKey='')
    else:
        return redirect('/internal/call')
    return str(resp)

def konami():
    digits_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
    if digits_pressed == "2884646#*":
        resp.play("http://queri.me/static/contra.mp3")
        return str(resp)
    return ''

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
    elif digit_pressed == "2":
        # 22884646#*
        resp.gather(numDigits=9, action="/internal/konami", method="POST", finishOnKey='')
    else:
        return redirect('/internal/call')
    return str(resp)

def do_wit(body, phone, recording=False):
    try:
        if not recording:
            wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % body, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
        if recording:
            wit = requests.post('https://api.wit.ai/speech', headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB', 'Content-Type': 'audio/wav'}, data=body).text
        print wit
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
        elif intent == 'find_file':
            entities = jso['outcomes'][0]['entities']
            server = entities['filelocation'][0]['value']
            filename = entities['filename'][0]['value']
            m = find(server, filename)
        else:
            m = "Hmm? Try again please :("
    except Exception, e:
        print str(e)
        m = "Sorry, something bad happened. Try again a bit later."
    return m

def text():
    b = request.form.get('Body','')
    phone = request.form.get('From','')
    try:
        m = do_wit(b, phone)
    except:
        m = "Sorry, something bad happened. Try again a bit later."

    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

def rec():
    resp = twilio.twiml.Response()
    print repr(request.form)
    recording = requests.get(request.form.get('RecordingUrl',''), stream=True).content
    m = do_wit(recording,request.form.get('From',''),recording=True)
    resp.say(m)
    return str(resp)
