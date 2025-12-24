from pathlib import Path
import re

# Match: ul.SLUS_203.12.00
UL_RE = re.compile(r"ul\.(.+?)\.\d+")


def ulcfg_path(usb):
    return Path(usb) / "ul.cfg"


# -------------------------
# READ EXISTING TITLES
# -------------------------
def _parse_old_titles(usb):
    titles = {}
    cfg = ulcfg_path(usb)

    if not cfg.exists():
        return titles

    for line in cfg.read_text(errors="ignore").splitlines():
        try:
            gid, title, _ = line.split("|", 2)
            titles[gid] = title
        except ValueError:
            continue

    return titles


# -------------------------
# ADD GAME ENTRY
# -------------------------
def add_entry(usb, game_id, title, media):
    cfg = ulcfg_path(usb)
    cfg.parent.mkdir(parents=True, exist_ok=True)

    line = f"{game_id}|{title}|{media}\n"
    cfg.open("a").write(line)


# -------------------------
# LIST GAMES
# -------------------------
def list_games(usb):
    cfg = ulcfg_path(usb)

    if not cfg.exists():
        print("No ul.cfg found")
        return

    print(f"{'GAME ID':<12} {'MEDIA':<4} TITLE")
    print("-" * 40)

    for line in cfg.read_text(errors="ignore").splitlines():
        try:
            gid, title, media = line.split("|", 2)
            print(f"{gid:<12} {media:<4} {title}")
        except ValueError:
            continue


# -------------------------
# REBUILD ul.cfg
# -------------------------
def rebuild_cfg(usb):
    usb = Path(usb)
    titles = _parse_old_titles(usb)
    entries = {}

    for media in ("DVD", "CD"):
        folder = usb / media
        if not folder.exists():
            continue

        for f in folder.glob("ul.*.*"):
            m = UL_RE.match(f.name)
            if not m:
                continue

            gid = m.group(1)
            if gid not in entries:
                entries[gid] = {
                    "media": media,
                    "title": titles.get(gid, gid)
                }

    cfg = ulcfg_path(usb)
    with cfg.open("w") as out:
        for gid in sorted(entries):
            e = entries[gid]
            out.write(f"{gid}|{e['title']}|{e['media']}\n")

    print(f"✔ Rebuilt ul.cfg ({len(entries)} games)")


# -------------------------
# DELETE GAME
# -------------------------
def delete_game(usb, game_id):
    usb = Path(usb)
    removed_files = 0

    for media in ("DVD", "CD"):
        folder = usb / media
        if not folder.exists():
            continue

        for f in folder.glob(f"ul.{game_id}.*"):
            f.unlink()
            removed_files += 1

    cfg = ulcfg_path(usb)
    if cfg.exists():
        lines = cfg.read_text(errors="ignore").splitlines()
        new_lines = [
            l for l in lines
            if not l.startswith(game_id + "|")
        ]
        cfg.write_text("\n".join(new_lines) + ("\n" if new_lines else ""))

    if removed_files:
        print(f"✔ Deleted {game_id} ({removed_files} parts)")
    else:
        print(f"⚠ Game {game_id} not found")


# -------------------------
# RENAME GAME TITLE
# -------------------------
def rename_game(usb, game_id, new_title):
    cfg = ulcfg_path(usb)

    if not cfg.exists():
        print("No ul.cfg found")
        return

    lines = cfg.read_text(errors="ignore").splitlines()
    updated = []
    changed = False

    for line in lines:
        try:
            gid, title, media = line.split("|", 2)
            if gid == game_id:
                title = new_title
                changed = True
            updated.append(f"{gid}|{title}|{media}")
        except ValueError:
            continue

    cfg.write_text("\n".join(updated) + "\n")

    if changed:
        print(f"✔ Renamed {game_id}")
    else:
        print(f"⚠ Game {game_id} not found")


def get_games(usb):
    cfg = ulcfg_path(usb)
    games = []

    if not cfg.exists():
        return games

    for line in cfg.read_text(errors="ignore").splitlines():
        try:
            gid, title, media = line.split("|", 2)
            games.append({
                "id": gid,
                "title": title,
                "media": media
            })
        except ValueError:
            continue

    return games
