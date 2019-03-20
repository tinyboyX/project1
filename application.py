import os

from flask import Flask, session,render_template,request
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

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signing_up",methods=["POST"] )
def signing_up():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == None or password = None
        return render_template("signup.html", message = "Username and password can not be empty")
    elif db.execute("SELETE * FROM users WHERE name = :name",{"name":name}).fetch
        return render_template("signup.html", message = "Username and password can not be empty")
    db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                    {"name": name, "password": password})
    db.commit()
    return render_template("login.html")