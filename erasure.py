import os

CHUNK_SIZE = 1024  # 1 KB per chunk (simulation)

def encode_file(filepath, output_dir):
    with open(filepath, "rb") as f:
        data = f.read()

    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]

    os.makedirs(output_dir, exist_ok=True)

    for idx, chunk in enumerate(chunks):
        with open(f"{output_dir}/{os.path.basename(filepath)}.chunk{idx}", "wb") as c:
            c.write(chunk)

    print(f"[EC] Encoded {filepath} into {len(chunks)} chunks")


def decode_file(filename, chunk_dir, output_file):
    chunks = sorted([c for c in os.listdir(chunk_dir) if c.startswith(filename)])

    with open(output_file, "wb") as out:
        for chunk in chunks:
            with open(f"{chunk_dir}/{chunk}", "rb") as c:
                out.write(c.read())

    print(f"[EC] Reconstructed file: {output_file}")
