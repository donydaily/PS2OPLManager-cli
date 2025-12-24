import psutil
from pathlib import Path

def detect_ps2_usb():
    for p in psutil.disk_partitions(all=False):
        if "FAT" in p.fstype.upper():
            path = Path(p.mountpoint)
            if (path / "DVD").exists() or (path / "CD").exists():
                return path
    return None
