import mysql.connector
from flask import Flask, redirect, render_template

# Configure application
app = Flask(__name__)

# Connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="todo_list",
  password="0000",
  database="todo_list"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM huesta")

myvar = mycursor.fetchall()

print(myvar)

@app.route("/")
def index():
    return render_template("index.html", myvar=myvar)