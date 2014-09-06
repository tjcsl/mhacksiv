from flask import render_template, session, url_for, redirect

def index():
    return render_template("index.html")
