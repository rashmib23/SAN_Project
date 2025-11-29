from flask import Flask, request, render_template, send_file
import os
from datetime import datetime
import pandas as pd
from erasure import encode_file
from priority_retrieval import retrieve
from prefetch_ml import train_model, prefetch

app = Flask(__name__)

DATA_DIR = "data"
COLD_DIR = "cold_storage"
CACHE_DIR = "cache"
LOG = "logs/access_log.csv"

# Ensure folders exist
for folder in [DATA_DIR, COLD_DIR, CACHE_DIR, "logs"]:
    os.makedirs(folder, exist_ok=True)

# Ensure log has headers
if not os.path.exists(LOG) or os.path.getsize(LOG) == 0:
    pd.DataFrame(columns=["filename","role","timestamp"]).to_csv(LOG, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    files = os.listdir(DATA_DIR)
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filepath = os.path.join(DATA_DIR, file.filename)
        file.save(filepath)
        encode_file(filepath, COLD_DIR)
        return f"{file.filename} uploaded and encoded!"
    return "No file uploaded", 400

@app.route("/request_file/<filename>/<role>")
def request_file(filename, role):
    path = retrieve(filename, role)
    if path is None or not os.path.exists(path):
        return "Error: file not found", 404

    # Log access
    try:
        df_existing = pd.read_csv(LOG)
    except pd.errors.EmptyDataError:
        df_existing = pd.DataFrame(columns=["filename","role","timestamp"])

    timestamp = int(datetime.now().timestamp())
    df_new = pd.DataFrame([[filename, role, timestamp]], columns=["filename","role","timestamp"])
    df = pd.concat([df_existing, df_new], ignore_index=True)
    df.to_csv(LOG, index=False)

    # ML prefetch simulation
    model = train_model()
    prefetch(model)

    # Serve PDF inline
    return send_file(path, mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
