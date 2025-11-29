import os
import pandas as pd
from erasure import encode_file
from priority_retrieval import retrieve
from prefetch_ml import train_model, prefetch

LOG = "logs/access_log.csv"

# --------------------------
# 1. Encode input files
# --------------------------
print("\n=== ENCODING SAMPLE FILES ===")
for file in os.listdir("data"):
    encode_file(f"data/{file}", "cold_storage")

# --------------------------
# 2. Simulate user requests
# --------------------------
requests = [
    ("exam1.pdf", "faculty"),
    ("assignment1.pdf", "student"),
    ("research1.pdf", "student"),
]

print("\n=== PROCESSING REQUESTS ===")
log_entries = []

for filename, role in requests:
    retrieve(filename, role)

    log_entries.append([filename, role, len(log_entries)])

df = pd.DataFrame(log_entries, columns=["filename", "role", "timestamp"])
df.to_csv(LOG, index=False)

# --------------------------
# 3. Train ML model
# --------------------------
model = train_model()

# --------------------------
# 4. Perform ML Prefetch
# --------------------------
prefetch(model)
print("\n=== DEMO COMPLETE ===")
