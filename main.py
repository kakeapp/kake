# main.py

import os
from flask import Flask, redirect, render_template, request, url_for, session
import dotenv
import database
import utils
import atexit
import cake

"""
Install dependencies with
pip install -r requirements.txt

Run the program with
python wsgi.py
"""

dotenv.load_dotenv(".env")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
database.create_connection()
atexit.register(database.close_connection)

@app.context_processor
def inject_var():
    data = { 'nc': '', 'user_verified': False }
    try:
        if session['cakeList']:
            data['nc'] = str(len(list(session['cakeList'])))
    except:
        pass

    try:
        if session['accessToken']:
            data['user_verified'] = database.check_user_is_verified(session['accessToken'])
    except:
        pass

    return data

@app.route("/", methods=['GET'])
def landing_page():
    if request.args:
        accessToken = request.args["accessToken"]
        if accessToken:
            database.verify_user(accessToken)
            return redirect(url_for("landing_page"))
    return render_template("index.jinja2")

@app.errorhandler(404)
def not_found_404(_error):
    return render_template("404.jinja2", url=request.url)

@app.errorhandler(500)
def not_found_500(_error):
    return render_template("500.jinja2")

@app.route("/stop")
def stop():
    database.close_connection()
    return "Closing!"

@app.route("/send-token")
def send_token():
    try:
        if session['checkoutToken']:
            pass
    except:
        return ('', 404)
    utils.send_checkout_token(session['emailid'], session['checkoutToken'])
    return "Sent!"

@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email_id = request.form.get("emailid")
        passwd = request.form.get("passwd")

        if not database.check_email(email_id):
            return render_template("signup.jinja2", errr=True)

        accessToken = database.gen_token()
        session["accessToken"] = accessToken
        database.create_user(username=username, emailid=email_id, passwd=passwd, verify_url=request.url_root+url_for("landing_page", accessToken=accessToken), accessToken=accessToken)
        session['emailid'] = email_id
        session['signIn'] = True
        return redirect(url_for("landing_page"))
    else:
        return render_template("signup.jinja2")

@app.route("/cakes")
def cakes():
    try:
        if session['accessToken']:
            pass
    except:
        return redirect(url_for("login"))
    return render_template("cakes.jinja2", cakes=database.get_cakes())

@app.route("/add-cake/<int:cakeId>")
def add_cake(cakeId):
    cake.append_cake(cakeId)
    return ('', 200)

@app.route("/remove-cake/<int:cakeId>")
def remove_cake(cakeId):
    cake.rm_cake(cakeId)
    return ('', 200)

@app.route("/cart")
def cart():
    try:
        if session['accessToken']:
            pass
    except:
        return redirect(url_for("login"))
    try:
        if session['cakeList']:
            pass
    except:
        return render_template("cart.jinja2")

    try:
        if session['checkoutToken']:
            if len(list(session['cakeList'])) == 0:
                session.pop('checkoutToken')
        else:
            print(session['checkoutToken'])
    except:
        if len(list(session['cakeList'])) != 0:
            session['checkoutToken'] = database.gen_token()[:10]
            print(session['checkoutToken'])

    data = database.get_cart(list(session['cakeList']))
    return render_template("cart.jinja2", cost=data[0], cakes=data[1])

@app.route("/checkout", methods=['POST'])
def checkout():
    if request.method == "POST":
        token = request.form.get("token")
        if token == session['checkoutToken']:
            session['cakeList'] = []
            return render_template("checkout.jinja2", success=True)
        else:
            return render_template("checkout.jinja2")
    else:
        return redirect(url_for("landing_page"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing_page"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email_id = request.form.get("emailid")
        passwd = request.form.get("passwd")

        if database.check_email(email_id):
            return render_template("login.jinja2", errr=True)

        if not database.check_usr(email_id, passwd):
            return render_template("login.jinja2", wrong_passwd=True)

        session['accessToken'] = database.get_access_token(email_id, passwd)[0]
        session['emailid'] = email_id
        session['signIn'] = True
        return redirect(url_for("landing_page"))
    else:
        return render_template("login.jinja2")
