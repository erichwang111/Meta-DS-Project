from flask import Flask, render_template, request, redirect, url_for, flash
from interactive_dashboard import create_dashboard
from dash import Dash
import dash_bootstrap_components as dbc

app = Flask(__name__)
app.secret_key = "abcd"
ADMIN_ID = "Administrator"
PASSWORD = "123"
session = {"username":ADMIN_ID}
dash_app = Dash(server=app, external_stylesheets=[dbc.themes.BOOTSTRAP], routes_pathname_prefix="/dashboard/")

dash_app = create_dashboard(dash_app)

@app.route("/",methods=['GET'])
def index():
    isLogin = False
    if "username" in session:
        isLogin = True
    return render_template("index.html",isLogin=isLogin)

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    pass

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if password == PASSWORD and username == ADMIN_ID:
            session["username"] = ADMIN_ID
            return redirect(url_for('dashboard'))
        else:
            flash("Password or Admin ID is incorrect")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout",methods=['GET'])
def logout():
    session.clear()
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8000,debug=True)
