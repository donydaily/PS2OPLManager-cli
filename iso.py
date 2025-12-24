import pycdlib
from pathlib import Path

def get_game_info(iso_path):
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)

    with iso.open_file_from_iso("/SYSTEM.CNF;1") as f:
        data = f.read().decode(errors="ignore")

    iso.close()

    game_id = "UNKNOWN"
    for line in data.splitlines():
        if "cdrom0:\\" in line.lower():
            game_id = line.split("\\")[1].split(";")[0]

    size = Path(iso_path).stat().st_size
    game_type = "DVD" if size > 700 * 1024 * 1024 else "CD"

    return game_id, game_type
