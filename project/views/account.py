from flask import render_template, request, session
import project.utils.twilio
import random

def account_view():
    if "username" not in session:
        return redirect("/")
    return render_template("account.html")

def add_phone():
    if "username" not in session:
        return redirect("/")
    phone = request.form["phone"]
    code = str(random.randint(0, 1000000)).zfill(6)
    project.utils.twilio.send_text(phone, "Your queri confirmation code is %s" % code)
    flash("Check your phone for a confirmation code.", "success")
    return render_template("account.html")

def aliases():
    if "username" not in session:
        return redirect("/")
    return render_template("alias.html")
