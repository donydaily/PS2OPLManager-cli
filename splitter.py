from pathlib import Path
from tqdm import tqdm

CHUNK = 1024 * 1024 * 1024

def split_iso(src, dst_dir, prefix):
    dst_dir.mkdir(parents=True, exist_ok=True)

    with open(src, "rb") as f:
        part = 0
        while True:
            data = f.read(CHUNK)
            if not data:
                break
            out = dst_dir / f"{prefix}.{part:02d}"
            with open(out, "wb") as o:
                o.write(data)
            part += 1
