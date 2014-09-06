from flask import render_template, session, url_for, redirect

def login():
    return render_template("login.html")
