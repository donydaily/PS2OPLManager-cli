import subprocess
from ulcfg import get_games, delete_game, rename_game, rebuild_cfg

def _fzf(lines, header):
    p = subprocess.Popen(
        ["fzf", "--ansi", "--header", header],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    out, _ = p.communicate("\n".join(lines))
    return out.strip()


def ui_main(usb):
    games = get_games(usb)
    if not games:
        print("No games found")
        return

    lines = [
        f"{g['id']:<12} {g['media']:<3} {g['title']}"
        for g in games
    ]

    sel = _fzf(lines, "🎮 Select Game")
    if not sel:
        return

    game_id = sel.split()[0]

    action = _fzf(
        ["✏ Rename", "🗑 Delete", "🔄 Rebuild ul.cfg", "Exit"],
        f"Game: {game_id}"
    )

    if action.startswith("✏"):
        new_title = input("New title: ")
        rename_game(usb, game_id, new_title)

    elif action.startswith("🗑"):
        if input(f"Delete {game_id}? (y/N): ").lower() == "y":
            delete_game(usb, game_id)

    elif action.startswith("🔄"):
        rebuild_cfg(usb)
