import urllib
def find(server, query):
    return "http://%s:5000%s" % (server, requests.get("http://%s:5000/matchfile/%s/" % (server, urllib.urlencode(query))).json()["matches"][0])
