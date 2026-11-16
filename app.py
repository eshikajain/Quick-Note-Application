
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Change this secret before deploying publicly
app.secret_key = "quick-notes-development-secret-key"


# Database connection
def get_db_connection():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create tables and upgrade existing database
def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = [
        row["name"] for row in
        conn.execute("PRAGMA table_info(notes)").fetchall()
    ]

    if "user_id" not in columns:
        conn.execute("ALTER TABLE notes ADD COLUMN user_id INTEGER")

    conn.commit()
    conn.close()


# Check whether user is logged in
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Please login first"}), 401
        return function(*args, **kwargs)
    return wrapper


# Home page
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must have at least 6 characters.")
            return redirect(url_for("register"))

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Email already registered. Please login.")
            return redirect(url_for("register"))

        conn.close()
        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("home"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Get logged-in user's notes
@app.route("/api/notes", methods=["GET"])
@login_required
def get_notes():
    conn = get_db_connection()

    notes = conn.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()

    conn.close()
    return jsonify([dict(note) for note in notes])


# Add a new note
@app.route("/api/notes", methods=["POST"])
@login_required
def add_note():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO notes (content, user_id) VALUES (?, ?)",
        (content, session["user_id"])
    )

    conn.commit()

    note = conn.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?",
        (cursor.lastrowid, session["user_id"])
    ).fetchone()

    conn.close()
    return jsonify(dict(note)), 201


# Edit an existing note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
@login_required
def edit_note(note_id):
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        "UPDATE notes SET content = ? WHERE id = ? AND user_id = ?",
        (content, note_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note updated successfully"})


# Delete an existing note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note deleted successfully"})


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
