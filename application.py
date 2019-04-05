import os
import requests
from flask import Flask, session,render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/signing_up", methods = ["POST"])
def signing_up():
    name = request.form.get('name')
    password = request.form.get('password')
    if name == "" or password == "":
        return render_template("signup.html", message = "Username and password can not be empty")
    elif " " in name:
        return render_template("signup.html", message = "Username can not contain space bar")
    elif db.execute("SELECT * FROM users WHERE username = :name",{"name": name}).rowcount == 1:
        return render_template("signup.html", message ="This username is not available")
    db.execute("INSERT INTO users (username, password) VALUES (:name, :password)", {"name":name, "password":password})
    db.commit()
    return render_template("success.html")

@app.route("/loging_in", methods = ["POST"])
def loging_in():
    name = request.form.get('name')
    password  = request.form.get('password')
    if db.execute("SELECT * FROM users WHERE username = :name AND password = :password",{"name": name, "password":password}).rowcount == 1:
        session["logged_in"] = True
        session["username"] = name
        return redirect("/menu")
    else:
        return render_template("login.html", message = "Your username or password is incorrect!")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/books")
def books():
    return render_template("books.html")
