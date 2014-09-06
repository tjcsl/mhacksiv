from flask import render_template, request, session, flash, redirect
from project.database import db_session
from project.models import Phone
import project.utils.twilioutil
import random
from project.models import User, Alias
from project.database import db_session

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

def delete_phone(pid):
    if "username" not in session:
        return redirect("/")
    phon = Phone.query.filter(Phone.pid == pid).first()
    if phon.uid != session["user_id"]:
        flash("Haha, no", "danger")
        return redirect("/")
    else:
        db_session.delete(phon)
        db_session.commit()
    flash("Phone deleted.", "success")
    return redirect("/account/")

def aliases():
    if "username" not in session:
        return redirect("/")
    aliaslist = [(i._from, i.to) for i in Alias.query.filter(Alias.uid == session["user_id"]).all()]
    return render_template("alias.html", aliases=aliaslist)

def addalias():
    if "username" not in session:
        return redirect("/")
    if not request.args or not "from" in request.args or not "to" in request.args:
        flash("path issue: %s %s" % (request.args["from"], request.args["to"]), "warning")
        return redirect("/account/alias/")
    if len(request.args["from"]) > 64 or len(request.args["to"]) > 64:
        flash("Alias field too long - max length is 64 characters.", "danger")
        return redirect("/account/alias/")
    nalias = Alias(uid=session["user_id"], _from=request.args["from"], to=request.args["to"])
    db_session.add(nalias)
    db_session.commit()
    flash("Your alias was added.", "success")
    return redirect("/account/alias/")
