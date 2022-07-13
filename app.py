from flask import Flask, redirect, render_template

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")