import os
import time
from erasure import decode_file

CACHE_DIR = "cache"
COLD_DIR = "cold_storage"

# Ensure cache exists
os.makedirs(CACHE_DIR, exist_ok=True)

def retrieve(filename, role):
    cache_path = os.path.join(CACHE_DIR, filename)

    # Check cache first
    if os.path.exists(cache_path):
        print(f"[CACHE HIT] Returned {filename} instantly")
        return cache_path

    print(f"[CACHE MISS] Need reconstruction...")

    # Priority logic
    if role.lower() in ["faculty", "admin"]:
        delay = 0  # high priority
    else:
        delay = 3  # simulate slower response for students

    print(f"[PRIORITY] Role={role}, Delay={delay}s")
    time.sleep(delay)

    reconstructed_file = decode_file(filename, COLD_DIR, cache_path)
    print(f"[DONE] {filename} reconstructed and cached.")
    return reconstructed_file
