import os

from flask import Flask, session,request,render_template
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

@app.route("/signing_up",methods=["POST"] )
def signing_up():
    name = request.form.get("name")
    password = request.form.get("password")
    if name =="" or password =="":
        return render_template("sign_up.html", message = "Username and password can not be empty")
    elif db.execute("SELECT * FROM users WHERE name = :name", {"name": name}).rowcount == 1:
        return render_template("sign_up.html", message = "Username are already exist")
    db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                {"name": name, "password": password})
    db.commit()
    return render_template("success.html")

@app.route("/menu" , methods=["GET"] )
def menu():
    name = request.form.get("name")
    password = request.form.get("password")
    if 
    return render_template("menu.html")

@app.route("/books")
def sign_up():
    return render_template("books.html")