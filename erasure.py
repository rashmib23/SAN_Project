# erasure.py
import os

CHUNK_SIZE = 64 * 1024  # 1 KB per chunk (simple simulation)

def encode_file(filepath, output_dir):
    with open(filepath, "rb") as f:
        data = f.read()

    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]

    os.makedirs(output_dir, exist_ok=True)

    base = os.path.basename(filepath)
    for idx, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f"{base}.chunk{idx}"), "wb") as c:
            c.write(chunk)

    print(f"[EC] Encoded {filepath} into {len(chunks)} chunks")


def decode_file(filename, chunk_dir, output_file):
    # filename like "exam1.pdf"
    all_chunks = sorted(
        [c for c in os.listdir(chunk_dir) if c.startswith(filename)],
        key=lambda x: int(x.split("chunk")[-1])
    )

    if not all_chunks:
        raise FileNotFoundError(f"No chunks found for {filename} in {chunk_dir}")

    with open(output_file, "wb") as out:
        for chunk in all_chunks:
            with open(os.path.join(chunk_dir, chunk), "rb") as c:
                out.write(c.read())

    print(f"[EC] Reconstructed file: {output_file}")
