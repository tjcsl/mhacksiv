from flask import render_template, session, url_for, redirect, request, flash
from project.models import User
from project.database import db_session
from project.utils.mail import sgclient
import uuid
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
import hashlib

def users():
    if "username" not in session:
        return redirect('/')
    if not session["admin"]:
        flash("Hey, no peeking!", "warning")
        return redirect('/')
    rawusers = User.query.order_by(User.uid).all()
    users = [(u.uid, u.username, u.email, u.enabled, u.admin) for u in rawusers]
    return render_template("admin-users.html", users=users)

def delete(uid):
    duser = User.query.filter(User.uid == uid).first()
    if duser is None:
        flash("No such user.", "danger")
        return redirect('/admin/users/')
    db_session.delete(duser)
    db_session.commit()
    flash("Deleted user.", "success")
    return redirect('/admin/users/')

def disable(uid):
    u = User.query.filter(User.uid == uid).first()
    if u is None:
        flash("No such user.", "danger")
        return redirect('/admin/users/')
    u.enabled = False
    db_session.commit()
    flash("Disabled user.", "success")
    return redirect('/admin/users/')

def enable(uid):
    u = User.query.filter(User.uid == uid).first()
    if u is None:
        flash("No such user.", "danger")
        return redirect('/admin/users/')
    u.enabled = True
    db_session.commit()
    flash("Disabled user.", "success")
    return redirect('/admin/users/')

def promote(uid):
    u = User.query.filter(User.uid == uid).first()
    if u is None:
        flash("No such user.", "danger")
        return redirect('/admin/users/')
    u.admin = True
    db_session.commit()
    flash("Promoted user.", "success")
    return redirect('/admin/users/')

def demote(uid):
    u = User.query.filter(User.uid == uid).first()
    if u is None:
        flash("No such user.", "danger")
        return redirect('/admin/users/')
    u.admin = False
    db_session.commit()
    flash("Demoted user.", "success")
    return redirect('/admin/users/')
