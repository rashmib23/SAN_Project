# priority_retrieval.py
import os
import time
from erasure import decode_file

CACHE_DIR = "cache"
COLD_DIR = "cold_storage"

def retrieve(filename, role):
    """
    Returns full path of the reconstructed or cached file.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cached_path = os.path.join(CACHE_DIR, filename)

    # If file already fully reconstructed in cache
    if os.path.exists(cached_path) and os.path.getsize(cached_path) > 0:
        print(f"[CACHE HIT] {filename} from cache ({role})")
        return cached_path

    print(f"[CACHE MISS] Need reconstruction for {filename} ...")

    # Priority delay
    if str(role).lower() in ["faculty", "admin"]:
        delay = 0
    else:
        delay = 3

    print(f"[PRIORITY] Role={role}, Delay={delay}s")
    time.sleep(delay)

    # Reconstruct from chunks into cache
    decode_file(filename, COLD_DIR, cached_path)
    print(f"[DONE] {filename} reconstructed and cached at {cached_path}")

    return cached_path
