from flask import Flask, render_template, request, redirect, url_for, flash
from pythonfiles.main_project import text_preprocessing
import dash_bootstrap_components as dbc
from dash import Dash
from Interactive_dashboard import update_index

app = Flask(__name__)

app.secret_key = "abcde"
ADMIN_ID = "admin123"
PASSWORD = "abc123"
session = {}
dash_app = Dash(server=app,external_stylesheets=[dbc.themes.BOOTSTRAP],routes_pathname_prefix="/dashboard/")

dash_app = update_index(dash_app)

@app.route("/",methods=['GET'])
def index():
    isLogin = False
    if "username" in session:
        isLogin = True
    return render_template("index.html", isLogin=isLogin)

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    if "username" not in session:
        redirect(url_for("login"))
    return render_template("index.html")


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
    session.clear() # remove everything in session
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8000,debug=True)
