import pandas as pd
import os
import shutil
from sklearn.ensemble import RandomForestClassifier

LOG_PATH = "logs/access_log.csv"
COLD = "cold_storage/"
CACHE = "cache/"

def train_model():
    if not os.path.exists(LOG_PATH):
        print("[ML] No logs available yet.")
        return None

    df = pd.read_csv(LOG_PATH)

    # Feature engineering
    df['hour'] = df['timestamp'] % 24
    df['role_weight'] = df['role'].apply(lambda r: 1 if r.lower() == "faculty" else 0)

    X = df[['hour', 'role_weight']]
    y = df['filename']

    model = RandomForestClassifier()
    model.fit(X, y)

    print("[ML] Model trained.")
    return model


def prefetch(model):
    if model is None:
        print("[ML] No model → skipping prefetch.")
        return

    print("[ML] Predicting next likely file...")

    # Proper DataFrame with same column names as training
    sample_input = pd.DataFrame([[10, 1]], columns=['hour', 'role_weight'])

    pred = model.predict(sample_input)
    filename = pred[0]

    if filename in os.listdir(CACHE):
        print(f"[PREFETCH] Already in cache: {filename}")
        return

    # Simulate prefetch by copying first chunk to cache
    chunk_file = f"{COLD}/{filename}.chunk0"
    if os.path.exists(chunk_file):
        print(f"[PREFETCH] Caching predicted file: {filename}")
        shutil.copy(chunk_file, f"{CACHE}/{filename}")
    else:
        print(f"[PREFETCH] Predicted file not found in cold storage: {filename}")
