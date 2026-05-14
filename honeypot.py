from flask import Flask, request
import sqlite3
import time

app = Flask(__name__)

DB = "attacks.db"

def get_severity(ip):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attacks WHERE iP=?", (ip,))
    count = c.fetchone()[0]

    conn.close()

    if count >= 8:
        return "HIGH - Brute Force"

    elif count >= 4:
        return "MEDIUM - Rapid Scan"

    elif count >= 2:
        return "LOW - Repeated Access"

    else:
        return "NORMAL"

def log(ip):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attacks WHERE iP=?", (ip,))
    count = c.fetchone()[0]

    if count <= 1:
        duration = "First hit"
    elif count <= 5:
        duration = "Short burst"
    else:
        duration = "Sustained attack"

    severity = get_severity(ip)

    info = f"{count} attacks | {duration}"

    c.execute(
        "INSERT INTO attacks VALUES (?, ?, ?, ?, ?)",
        (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            ip,
            2222,
            severity,
            info
        )
    )

    conn.commit()
    conn.close()

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch(path):
    ip = request.remote_addr
    log(ip)
    return "blocked", 403

app.run(host="0.0.0.0", port=2222)
