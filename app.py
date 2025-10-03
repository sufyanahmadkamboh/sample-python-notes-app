from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("notes.db")

app = Flask(__name__)
app.secret_key = "change-me-in-prod"  # needed for flash messages

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created_at TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    conn = get_db()
    notes = conn.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content", "").strip()
    if not content:
        flash("Please write something before adding a note.")
        return redirect(url_for("index"))
    conn = get_db()
    conn.execute("INSERT INTO notes (content, created_at) VALUES (?, ?)", (content, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    flash("Note added!")
    return redirect(url_for("index"))

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    flash("Note deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
