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
    aliaslist = [(i._from, i.to, i.aid) for i in Alias.query.filter(Alias.uid == session["user_id"]).all()]
    return render_template("alias.html", aliases=aliaslist)

def addalias():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        if not "from" in request.form or not "to" in request.form:
            return redirect("/account/alias/")
        if len(request.form["from"]) > 64 or len(request.form["to"]) > 64:
            flash("Alias field too long - max length is 64 characters.", "danger")
            return redirect("/account/alias/")
        nalias = Alias(uid=session["user_id"], _from=request.form["from"], to=request.form["to"])
        db_session.add(nalias)
        db_session.commit()
        flash("Your alias was added.", "success")
    return redirect("/account/alias/")

def delalias(aid):
    if "username" not in session:
        return redirect("/")
    tdalias = Alias.query.filter(Alias.aid == aid).first()
    if tdalias.uid != session["user_id"]:
        flash("You don't own that alias!", "danger")
        return redirect('/account/alias/')
    db_session.delete(tdalias)
    db_session.commit()
    flash("Your alias was deleted.", "success")
    return redirect("/account/alias/")