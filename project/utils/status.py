import json
import requests
def get_alias(phone, shortname):
    return shortname

def get_status(wit_json, phone):
    wit_json = json.loads(wit_json)
    entities = wit_json["outcomes"][0]["entities"]
    server = entities["server"][0]["value"]
    status_entity = entities["status_item"][0]["value"]
    server = get_alias(phone, server)
    resp = requests.get("http://%s:5000/%s/" % (server, status_entity)).json()
    if type(resp)["value"] == list:
        return "\n".join([i["format_string"] % i["value"] for i in resp])
    else:
        return resp["format_string"] % resp["value"]
