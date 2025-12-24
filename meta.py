from pathlib import Path

def rename_game(usb, game_id, new_title):
    cfg = Path(usb) / "ul.cfg"
    lines = cfg.read_text().splitlines()
    out = []
    for l in lines:
        gid, title, media = l.split("|")
        if gid == game_id:
            title = new_title
        out.append(f"{gid}|{title}|{media}")
    cfg.write_text("\n".join(out) + "\n")
