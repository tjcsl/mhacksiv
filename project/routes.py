from project import app

from project.views import twilioviews, core, alias

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function,
                methods=["GET", "POST"])

add_url_routes((
    ('/internal/call', twilioviews.call),
    ('/internal/text', twilioviews.text),
    ('/internal/rec', twilioviews.rec),
    ('/', core.index),
    ('/about/', core.about),
    ('/u/alias/', alias.aliases)
))
