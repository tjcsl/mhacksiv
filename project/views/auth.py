from flask import render_template, session, url_for, redirect, request, flash
from project.models import User
from project.database import db_session
from project.utils.mail import sgclient
import uuid
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
import hashlib

def login():
    return render_template("login.html")

def process_register():
    if request.method == "POST":
        if request.form["email"] != request.form["email-confirm"]:
            flash("Error: your emails didn't match.", "danger")
        elif request.form["password"] != request.form["password-confirm"]:
            flash("Error: your passwords didn't match.", "danger")
        else:
            if User.query.filter(User.username == request.form["username"]).first() != None:
                flash("Error: that username is already taken.", "danger")
            elif User.query.filter(User.email == request.form["email"]).first() != None:
                flash("Error: that email is already in use.", "danger")
            else:
                for ch in request.form["username"]:
                    if ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_':
                        flash("Error: usernames may only use A-Z, a-z, 0-9, _, and -.", "danger")
                        return redirect("/login/")
                reguuid = uuid.uuid1()
                regmail = sendgrid.Mail()
                regmail.add_to(request.form["email"])
                regmail.set_subject("queri.me registration confirmation")
                regmail.set_from('noreply@queri.me')
                regmail.set_text("""Welcome to queri.me!

In order to complete your registration and activate your account, please click
this link to verify your email address: http://queri.me/verifyemail?user=%s&key=%s

-- the queri.me team
""" % (request.form["username"], reguuid))
                try:
                    sgclient.send(regmail)
                except:
                    flash("An error occurred sending your confirmation email. Please try again.", "danger")
                    return render_template("login.html")
                newuser = User(username=request.form["username"], email=request.form["email"],
                        pwhash=hashlib.sha256(request.form["password"]).hexdigest(),
                        reg_uuid=str(reguuid), enabled=False)
                db_session.add(newuser)
                db_session.commit()
                flash("Account successfully created. Please check your email for activation instructions.", "success")
                return redirect('/')
    return render_template("login.html")

def process_login():
    if request.method == "POST":
        if User.query.filter((User.username == request.form["username"]) | (User.email == request.form["username"])).first() == None:
            flash("Invalid username or password.", "danger")
        elif User.query.filter(((User.username == request.form["username"]) | (User.email == request.form["username"])) & (User.pwhash == hashlib.sha256(request.form["password"]).hexdigest())).first() == None:
            flash("Invalid username or password.", "danger")
        else:
            curruser = User.query.filter((User.username == request.form["username"]) | (User.email == request.form["username"])).first()
            if not curruser.enabled:
                flash("Your user is disabled.", "danger")
                return redirect('/login/')
            session["user_id"] = curruser.uid
            session["username"] = curruser.username
            session["admin"] = curruser.admin
            flash("Successfully logged in.", "success")
            return redirect('/')
    return render_template("login.html")

def verifyemail():
    if not request.args or not "key" in request.args or not "user" in request.args:
        return redirect('/')
    actuser = User.query.filter(User.username == request.args["user"]).first()
    if not actuser:
        return redirect('/')
    if actuser.enabled:
        flash("Account already enabled.", "warning")
        return redirect('/')
    if actuser.reg_uuid == request.args["key"]:
        actuser.enabled = True
        db_session.commit()
        flash("Account successfully activated. You're ready to log in!", "success")
        return redirect("/login/")
    return redirect('/')

def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('admin', None)
    return redirect('/')
