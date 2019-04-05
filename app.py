from flask import Flask, render_template, redirect, url_for, request, session,g
from functools import wraps
import pymongo
import bcrypt
from pymongo import MongoClient
from flask_mail import Mail

app = Flask(__name__, template_folder='template')
client = MongoClient('mongodb://localhost:27017/')
db = client['FTX']
mail = Mail()
mail.init_app(app)


def log_required(f):
    @wraps(f)
    def wrap(*args, **kwargs) :
        if('logged_in' in session) :
            return f(*args, **kwargs)
        else:
            return("you need to log in first")
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
    login_user = users.find_one({'username' : request.form.get("username")})
    Hpassword = request.form.get("password")
    if login_user:
        if bcrypt.hashpw(Hpassword.encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] =request.form.get("username")
            return redirect(url_for('world'))
        else:
            return("Invalid username/password")
    return render_template('index.html')

@app.route('/lostPassword')
def lostPassword():
    find_user_mail = users.find_one({'email' : request.form.get("email")})
    mail_user = request.form.get("email")
    if find_user_mail:
        msg = Message()
        msg.recipients = ["rohandeshpande832@gmail.com"]
        msg.add_recipient(find_user_mail)
        msg.html = "<b>testing</b>"
        mail.send(msg)

    else:
        return("Invalid email")
    return render_template('LostPassword.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            Hpassword = request.form['password'].encode('utf-8')
            hashpass = bcrypt.hashpw(Hpassword, bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : hashpass, 'email' : request.form['email'], 'institute' : request.form['Institute']})
            
            session['username'] = request.form.get("username")
            return redirect(url_for('world'))
        
        return("That username already exists!")

    return render_template('register.html')

@app.route("/logout")
@log_required
def logout():
    session.pop("logged_in", None)  
    return("LOGGED OUT")    
    return redirect(url_for('world'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
