from flask import Flask, request
from status import get_status
import requests
import twilio.twiml

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
    resp = twilio.twiml.Response()
    resp.record(timeout=10, transcribe=True, transcribeCallback='http://35.2.116.13:8080/rec', )
    return str(resp)

@app.route('/text', methods=['GET', 'POST'])
def text():
    b = request.form.get('Body','')
    phone = request.form.get('From','')
    wit = requests.get('https://api.wit.ai/message?v=20140905&q=%s' % b, headers={'Authorization':'Bearer L3VB34V6YTDFO4BRXNDQNAYMVOOF4BHB'}).text
    m = get_status(wit, phone)
    # Send to wit.ai for processing
    resp = twilio.twiml.Response()
    resp.message(m)
    return str(resp)

@app.route('/rec', methods=['POST'])
def rec():
    print request.form.get('TranscriptionText','')
    return ''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

