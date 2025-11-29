import os
from flask import Flask, request, render_template, session, redirect, url_for, send_file
from erasure import encode_file
from priority_retrieval import retrieve
from prefetch_ml import train_model, prefetch
from auth import validate_user
import pandas as pd
from datetime import datetime
from mimetypes import guess_type

app = Flask(__name__)
app.secret_key = "supersecretkey123"

LOG = "logs/access_log.csv"

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("cold_storage", exist_ok=True)
os.makedirs("cache", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # Get role from auth.py
        role = validate_user(user, pwd)

        if role:
            session["user"] = user
            session["role"] = role   # 'admin' / 'faculty' / 'student'
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")



# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- REQUIRE LOGIN ----------
@app.before_request
def require_login():
    allowed_routes = ["login", "static", "cached_file"]
    if "user" not in session and request.endpoint not in allowed_routes:
        return redirect(url_for("login"))


# ---------- HOME (UPLOAD + REQUEST) ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        # --- Upload ---
        if action == "upload":
            file = request.files["file"]
            if file:
                filepath = os.path.join("data", file.filename)
                file.save(filepath)
                encode_file(filepath, "cold_storage")
                return render_template("result.html",
                                       message=f"{file.filename} uploaded and encoded!")

        # --- Retrieve ---
        elif action == "request":
            filename = request.form.get("filename")
            role = session.get("role")

            if filename:
                # Reconstruct or get from cache
                file_path = retrieve(filename, role)

                # Log access
                timestamp = int(datetime.now().timestamp())
                log_entry = pd.DataFrame([[filename, role, timestamp]],
                                         columns=["filename", "role", "timestamp"])
                if os.path.exists(LOG):
                    df_existing = pd.read_csv(LOG)
                    log_entry = pd.concat([df_existing, log_entry], ignore_index=True)
                log_entry.to_csv(LOG, index=False)

                # ML prefetch (can be left on)
                model = train_model()
                try:
                    prefetch(model)
                except Exception as e:
                    print("[ML] Prefetch failed, but continuing normally:", e)


                # Show viewer page
                return redirect(url_for("view_file", filename=filename))

    files = os.listdir("data")
    return render_template("index.html", files=files)


# ---------- VIEW FILE PAGE (IFRAME) ----------
@app.route("/view/<filename>")
def view_file(filename):
    file_path = os.path.join("cache", filename)
    if not os.path.exists(file_path):
        return f"File {filename} not found in cache", 404

    return render_template("view.html", filename=filename)


# ---------- SERVE FILE TO IFRAME ----------
@app.route("/cached/<filename>")
def cached_file(filename):
    file_path = os.path.join("cache", filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    mime, _ = guess_type(file_path)
    return send_file(file_path, mimetype=mime or "application/octet-stream")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
