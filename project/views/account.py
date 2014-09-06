from flask import render_template, request, session, flash
from project.database import db_session
from project.models import Phone
import project.utils.twilioutil
import random

def account_view():
    if "username" not in session:
        return redirect("/")
    return render_template("account.html", phones=Phone.query.filter(Phone.uid == session["user_id"]).all())

def add_phone():
    if "username" not in session:
        return redirect("/")
    phone = request.form["phone"]
    code = str(random.randint(0, 1000000)).zfill(6)
    project.utils.twilioutil.send_text(phone, "Your queri confirmation code is %s" % code)
    phon = Phone(session["user_id"], phone, code)
    db_session.add(phon)
    db_session.commit()
    flash("Check your phone for a confirmation code.", "success")
    return render_template("account.html")

def confirm_phone():
    if "username" not in session:
        return redirect("/")
    phone = request.form["phone"]
    code = request.form["code"]
    phon = Phone.query.filter(Phone.phone_number == phone and Phone.confirmation == code).first()
    if phon is None:
        flash("No phone found.", "danger")
        return render_template("account.html")
    phon.is_confirmed = True
    db_session.commit()
    flash("Phone <!-- illuminati --> confirmed.", "success")
    return render_template("account.html")

def aliases():
    if "username" not in session:
        return redirect("/")
    return render_template("alias.html")
