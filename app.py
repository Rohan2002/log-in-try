from flask import Flask, render_template, redirect, url_for, request, session,flash,g
from functools import wraps
#from flask_pymongo import PyMongo
import pymongo
import bcrypt
from pymongo import MongoClient

import sqlite3
app = Flask(__name__, template_folder='template')
client = MongoClient('mongodb://localhost:27017/')
db = client['FTX']


def log_required(f):
    @wraps(f)
    def wrap(*args, **kwargs) :
        if('logged_in' in session) :
            return f(*args, **kwargs)
        else:
            flash("you need to log in first")
            return redirect(url_for('login'))
    return wrap
          
@app.route("/")
def world():
    if 'username' in session:
        return "You are logged in as: " + session['username']
    return render_template("index.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form.get("username")})
    Hpassword = request.form.get("password").encode('utf-8')
    hashpass = bcrypt.hashpw(Hpassword, login_user['password'])
    if login_user:
        if hashpass == login_user['password']:
            session['username'] =request.form.get("username")
            return redirect(url_for('world'))
        else:
            flash("Invalid username/password")
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            Hpassword = request.form['password'].encode('utf-8')
            hashpass = bcrypt.hashpw(Hpassword, bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form.get("username")
            return redirect(url_for('world'))
        
        flash("That username already exists!")

    return render_template('register.html')

@app.route("/logout")
@log_required
def logout():
    session.pop("logged_in", None)  
    flash("LOGGED OUT")    
    return redirect(url_for('world'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
