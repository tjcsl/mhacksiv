from flask import render_template
def account_view():
    return render_template("account.html")

def aliases():
    return render_template("alias.html")
