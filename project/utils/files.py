import urllib
import requests
from project.utils.status import get_alias
def find(server, query, phone):
    return "http://%s:5000%s" % (get_alias(phone, server), requests.get("http://%s:5000/matchfile/%s/" % (get_alias(phone, server), urllib.urlencode(query))).json()["matches"][0])
