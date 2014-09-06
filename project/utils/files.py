import urllib
import requests
from project.utils.status import get_alias
def find(server, query, phone):
    server = get_alias(phone, server)
    query = urllib.urlencode(query)
    r = requests.get("http://%s:5000/matchfile/%s/" % (server, query))
    return r.json()["matches"][0]
