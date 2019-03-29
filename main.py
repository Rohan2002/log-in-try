from flask import Flask, render_template, redirect, url_for, request, session,flash
from functools import wraps

app = app = Flask(__name__, template_folder='template')
app.secret_key = "cool"

def log_required(f):
    @wraps(f)
    def wrap(*args, **kwargs) :
        if('logged_in' in session) :
            return f(**args, **kwargs)
        else:
            flash("you need to log in first")
            return redirect(url_for('login'))
    return wrap


@app.route("/")
def world():
    return render_template("index.html")

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
def logout():
    session.pop("logged_in", None)  
    flash("LOGGED OUT")    
    return redirect(url_for('world'))

if __name__ == '__main__':
    app.run()
