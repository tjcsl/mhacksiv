from project import app

from project.views import twilio

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function,
                methods=["GET", "POST"])

add_url_routes((
    ('/internal/call', twilio.call),
    ('/internal/text', twilio.text),
    ('/internal/rec', twilio.rec)
))
