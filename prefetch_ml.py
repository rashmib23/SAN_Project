import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

LOG = "logs/access_log.csv"

def train_model():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG) or os.path.getsize(LOG) == 0:
        df = pd.DataFrame(columns=["filename", "role", "timestamp"])
        df.to_csv(LOG, index=False)

    df = pd.read_csv(LOG)
    if df.empty:
        # No data yet, create dummy model
        model = RandomForestClassifier()
        return model

    # Simple training: filename -> role (simulation)
    df["role_num"] = df["role"].astype("category").cat.codes
    X = df.index.values.reshape(-1,1)  # use timestamp index as feature
    y = df["role_num"]
    model = RandomForestClassifier()
    model.fit(X, y)
    print("[ML] Model trained.")
    return model

def prefetch(model):
    # Simulate prefetch by just checking last file in log
    df = pd.read_csv(LOG)
    if df.empty:
        return
    next_file = df.iloc[-1]["filename"]
    print(f"[PREFETCH] Likely next file: {next_file}")
