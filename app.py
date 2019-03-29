from flask import Flask, render_template, redirect, url_for, request, session,flash,g
from functools import wraps

import sqlite3
app = Flask(__name__, template_folder='template')
app.secret_key = "cool"
app.database = "sample.db"

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
@log_required
def world():
    g.db = connect_DB()
    cur = g.db.execute('select * from posts')
    posts = []
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or request.form['password'] != 'admin'):
            error = 'Invalid Credentials. Please try again.'
        else:
            session["logged_in"] = True
            flash("LOGGED IN")    
            return redirect(url_for('world'))
    return render_template('login.html', error=error)

@app.route("/logout")
@log_required
def logout():
    session.pop("logged_in", None)  
    flash("LOGGED OUT")    
    return redirect(url_for('world'))

def connect_DB():
    return sqlite3.connect("sample.db")

if __name__ == '__main__':
    app.run()
