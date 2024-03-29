from project import app

from project.views import twilioviews, core, account, auth, admin

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function,
                methods=["GET", "POST"])

add_url_routes((
    ('/internal/call', twilioviews.call),
    ('/internal/text', twilioviews.text),
    ('/internal/rec', twilioviews.rec),
    ('/internal/handle-key', twilioviews.handle_key),
    ('/internal/handle-key-2', twilioviews.handle_key_2),
    ('/internal/konami', twilioviews.konami),
    ('/', core.index),
    ('/about/', core.about),
    ('/account/alias/', account.aliases),
    ('/account/alias/add/', account.addalias),
    ('/account/alias/del/<int:aid>', account.delalias),
    ('/account/phones/', account.phone_view),
    ('/account/phones/add/', account.add_phone),
    ('/account/phones/confirm/', account.confirm_phone),
    ('/account/phones/del/<int:pid>/', account.delete_phone),
    ('/login/', auth.login),
    ('/login/register/', auth.process_register),
    ('/login/login/', auth.process_login),
    ('/verifyemail/', auth.verifyemail),
    ('/logout/', auth.logout),
    ('/admin/users/', admin.users),
    ('/admin/users/delete/<int:uid>/', admin.delete),
    ('/admin/users/enable/<int:uid>/', admin.enable),
    ('/admin/users/disable/<int:uid>/', admin.disable),
    ('/admin/users/promote/<int:uid>/', admin.promote),
    ('/admin/users/demote/<int:uid>/', admin.demote)
))
