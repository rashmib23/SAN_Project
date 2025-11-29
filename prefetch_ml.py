import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from erasure import decode_file

LOG_PATH = "logs/access_log.csv"
COLD = "cold_storage"
CACHE = "cache"

def train_model():
    if not os.path.exists(LOG_PATH):
        print("[ML] No logs yet, skipping training.")
        return None

    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("[ML] Log file empty, skipping training.")
        return None

    # Simple features
    df['hour'] = df['timestamp'] % 24
    df['role_weight'] = df['role'].apply(lambda r: 1 if str(r).lower() == "faculty" else 0)

    X = df[['hour', 'role_weight']]
    y = df['filename']

    model = RandomForestClassifier()
    model.fit(X, y)
    print("[ML] Model trained.")
    return model


def prefetch(model):
    if model is None:
        return

    print("[ML] Predicting likely-to-be-accessed file...")
    sample_input = pd.DataFrame([[10, 1]], columns=['hour', 'role_weight'])
    filename = model.predict(sample_input)[0]

    cache_path = os.path.join(CACHE, filename)

    # If already in cache and non-empty → done
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        print(f"[PREFETCH] {filename} already cached.")
        return

    # ✅ Check if chunks exist in cold storage first
    chunks = [c for c in os.listdir(COLD) if c.startswith(filename)]
    if not chunks:
        print(f"[PREFETCH] Skipping {filename}: no chunks found in {COLD}")
        return

    try:
        print(f"[PREFETCH] Reconstructing {filename} into cache...")
        decode_file(filename, COLD, cache_path)
        print(f"[PREFETCH] Prefetch completed for {filename}")
    except FileNotFoundError as e:
        # Extra safety: if decode fails, don't kill the app
        print(f"[PREFETCH] Error during prefetch for {filename}: {e}")
