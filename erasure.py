import os

CHUNK_SIZE = 64 * 1024  # 64 KB per chunk for PDF stability

def encode_file(filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "rb") as f:
        data = f.read()
    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f"{os.path.basename(filepath)}.chunk{idx:04d}"), "wb") as c:
            c.write(chunk)
    print(f"[EC] Encoded {filepath} into {len(chunks)} chunks")

def decode_file(filename, chunk_dir, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    chunks = sorted([c for c in os.listdir(chunk_dir) if c.startswith(filename)])
    if not chunks:
        print(f"[ERROR] No chunks found for {filename}")
        return None
    with open(output_file, "wb") as out:
        for chunk in chunks:
            with open(os.path.join(chunk_dir, chunk), "rb") as c:
                out.write(c.read())
    print(f"[EC] Reconstructed file: {output_file}")
    return output_file
