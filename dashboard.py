from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("attacks.db")
    c = conn.cursor()

    c.execute("SELECT * FROM attacks ORDER BY time DESC")
    data = c.fetchall()

    conn.close()

    return render_template("dashboard.html", data=data)

app.run(port=5000)
