import json
import requests
from project.models import Phone, Alias
def get_alias(phone, shortname):
    phon = Phone.query.filter(Phone.phone_number == phone).first()
    if phon is None:
        return shortname
    alis = Alias.query.filter(Alias.uid == phon.uid and Alias._from == shortname).first()
    if alis is None:
        return shortname
    return alis.to

def get_status(wit_json, phone):
    wit_json = json.loads(wit_json)
    entities = wit_json["outcomes"][0]["entities"]
    server = entities["server"][0]["value"]
    status_entity = entities["status_item"][0]["value"]
    server = get_alias(phone, server)
    resp = requests.get("http://%s:5000/%s/" % (server, status_entity)).json()
    if type(resp["value"]) == list:
        return "\n".join([i["format_string"] % i["value"] for i in resp["value"]])
    else:
        return resp["format_string"] % resp["value"]
