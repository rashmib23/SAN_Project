
import os
import time
from erasure import decode_file

CACHE_DIR = "cache/"
COLD_DIR = "cold_storage/"

def retrieve(filename, role):
    # Check cache first
    if filename in os.listdir(CACHE_DIR):
        print(f"[CACHE HIT] Returned {filename} instantly")
        return

    print(f"[CACHE MISS] Need reconstruction...")

    chunk_dir = COLD_DIR

    # Priority logic
    if role.lower() in ["faculty", "admin"]:
        delay = 0       # high priority
    else:
        delay = 3       # simulate slow response for students

    print(f"[PRIORITY] Role={role}, Delay={delay}s")
    time.sleep(delay)

    decode_file(filename, chunk_dir, f"cache/{filename}")
    print(f"[DONE] {filename} reconstructed and cached.")
