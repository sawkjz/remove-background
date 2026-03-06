import os
import sys
import time
import traceback
from pathlib import Path
from typing import Dict
import shutil

EXTS = (".png", ".jpg", ".jpeg", ".webp")
EXIT_WORDS = {"exit", "quit"}
SESSION_CACHE: Dict[str, object] = {}


# =========================
# Console / UI helpers
# =========================
def init_console_utf8() -> None:
    """Best-effort: make Windows console handle Unicode art."""
    if os.name == "nt":
        try:
            os.system("chcp 65001 > nul")
        except Exception:
            pass

    # Python 3.7+: allow forcing utf-8 if supported
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def term_width() -> int:
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def hr(ch: str = "═") -> str:
    return ch * term_width()


def center(line: str) -> str:
    return line.center(term_width())


def right(text: str) -> str:
    return text.rjust(term_width())


def clear_screen() -> None:
    # Works well on Windows Terminal / VSCode terminal; CMD also usually fine.
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")


def print_start_banner() -> None:
    bow = "╭──────────.★..─╮"
    print(hr())
    print(center(bow))
    print(right("@sawkjz"))
    print()
    print("┊ ⋆ ┊ . ┊ ┊")
    print("┊ ┊⋆ ┊ .")
    print("┊ ┊ ⋆˚ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭")
    print("✧. ┊ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭ ⁭")
    print("⋆ ★")
    print()
    print("⊹")
    print("⢠⡏⠉⠑⢄⠀ ⠀  ⡠⠋⠉⢱⡀")
    print("⡇⠙⠒⠒⠬⡗⢒⢮⠄⠒⠒⠁⢣")
    print("⠇⠀⠈⠁⢁⡷⠤⢮⠈⠁⠀⠀⡌")
    print("⠘⢄⣀⡰⢻⠁⠀⠘⡕⢄⣀⡰⠁⠀⊹")
    print("⠀⡎⠘⢀⠇⠀⠀⠀⢱⠈⠂⠡⠀")
    print("⠀⠑⢄⡜⠢⡀⠀⢀⠔⠇⡴⠃⠀")
    print("⠀⠀⠀⠑⠠⠚⠀⠓⠔⠋⠀⠀")
    print("⊹")
    print(hr())


CLOSING_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⢴⣴⡶⠶⠾⠞⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⡄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣦⣦⠶⠟⠋⠀⠀⣀⠀⠀⠀⠉⠙⢿⡆⠀⠘⣷⣀⣤⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⢘⣿⣧⡀⠀⠀⣷⠛⠙⠛⠲⢤⡀⠀⢰⡿⠀⠀⢀⣤⡄⠀⠀⠀⢸⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⡧⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⢸⡇⠀⠀⢻⡏⠉⠉⠙⠛⠷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣄⢸⡏⠈⢿⡆⠐⣿⠀⠀⠀⠀⠀⣿⠀⣽⡇⠀⢀⡾⢻⡿⠀⠀⠀⠺⠇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣿⣤⣤⣤⡄⠀⠐⣿⡀⠀⠀⠀⢀⡿⠁⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠸⣯⠀⢽⡇⠀⠀⠀⣴⠏⠀⣿⠃⣰⡟⠁⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣦⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⣤⣤⡼⠏⠀⠀⠉⠓⠶⠛⠉⠀⠀⠘⠛⠋⠀⠀⠹⢇⠀⠀⢠⣦⣶⠄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠷⠿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣤⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣀⠀⠀⠀
⣰⠶⠶⣦⣀⠀⢀⡞⠁⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠂⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠋⠀⠸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⡶⣄⠀⠀⠀⠀⣠⠞⣩⠟⠀⠀⠀
⢸⡇⠀⠈⠹⠿⠏⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠸⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⡿⠁⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⢹⣇⠀⠀⣾⠇⣸⠇⠀⠀⠀⠀
⠈⠻⣦⣀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⣿⠀⠀⠀⠈⠻⣶⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡄⠹⣷⡼⢋⡾⠃⠀⠀⠀⠀⠀
⠀⠀⠈⠛⠷⣦⠄⢰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⡇⠀⠀⠀⠀⠀⠀⠻⢢⣄⣀⣀⣀⣀⣀⣀⣀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠐⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣧⣠⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⣠⠖⢻⡇⠀⠀⠀⢸⡯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣿⠈⠛⠁⢀⡞⠁⠀⠀⠀⢺⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⣠⠟⠁⠀⠀⠀⠀⠘⠏⡀⠀⠀⠀⢠⣤⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⡷⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⠀⠀⢀⣴⣤⠀⠀⠀⠀⠈⠛⢶⠃⠀⠀⠀⠀⠀⡀⠀⣼⠏⠀⠀⠀⠘⠿⣾⠿⠂⠀⠀⠀⣀⡄⠀⠀⠀⠀⠀⠘⠿⠿⠃⠀⠀⠀⠀⠀⣦⣄⣄⣤⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⣷⠶⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠛⠛⣿⠟⠁⡀⠀⣠⣴⠀⠀⠀⠀⠀⣰⡿⠻⣧⡀⠀⠀⠀⠀⠀⢀⡤⢀⡴⣶⣇⠀⣿⡍⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣧⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⣰⣧⠞⢻⠃⠀⠀⠀⠀⠘⠉⠀⠀⠈⠛⠀⠀⠀⠀⠀⠘⠛⠋⠀⠋⠉⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⠟⢿⡄⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠿⢦⣤⣤⣤⠀⠀⠀⢀⡀⠀⠀⠀⠀⣠⠞⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣆⠀⢠⣴⡆⠀⠀⠀⠀⠈⠛⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡿⠀⠀⠀⠀⠀⠀⠀⢰⣟⠛⢷⣄⣀⡴⠁⣴⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣤⣀⡀⠀⢿⠠⣿⣾⣿⢻⡇⠀⠀⠀⠀⠀⠀⠀⠹⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢋⡀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠉⠉⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⡈⢹⣿⢷⣿⣾⣿⣿⠇⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣆⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣇⢸⣿⣿⢽⣿⣿⡏⣸⠃⠀⠀⠀⠀⠀⣼⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⡀⠀⠀⠀⠀⠀⠀⠉⠹⡶⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣯⣿⠃⣿⣿⣿⢺⠇⠀⠀⠀⠀⣠⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣄⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠿⣦⣿⣿⢇⡎⠀⠀⠀⣠⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄
⠀⠀⠀⠀⠀⠀⠀⣠⡀⠈⠻⢷⡾⠀⠀⢀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⣠⠏⡽
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣦⣄⢸⢿⠀⣴⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⢼⡏⠉⠛⠛⠛⠁⢰⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡉⢿⣿⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣀⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀⡿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢷⣄⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠈⠻⣦⣤⣀⠸⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⣿⡄⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⡄⠀⠀⠀⠀⠀⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⣹⡂⠀⠀⠀⠀⠠⣶⠿⢛⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠻⠷⣶⣄⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠁⠀⢘⡅⠀⠀⣠⣶⡷⠀⠀⢸⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡃⠀⠀⠙⢷⣄⠀⠀⠀⠀⠀⠈⣱⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠈⣷⠀⣺⠟⠋⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠘⠿⣦⣴⣶⣶⡾⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⠻⢷⣤⣀⣹⠞⠁⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⡇⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⢺⡀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""".strip("\n")


def print_closing_sequence() -> None:
    # Optional: a little breathing room before the final message
    print()
    print(CLOSING_ART)
    time.sleep(0.35)
    print("\nClosing...")


# =========================
# Core logic
# =========================
def is_image_file(p: Path) -> bool:
    return p.suffix.lower() in EXTS


def downloads_dir() -> Path:
    # Windows: C:\Users\<user>\Downloads
    return Path.home() / "Downloads"


def normalize_input(txt: str) -> str:
    return txt.strip().strip('"')


def resolve_input_path(txt: str) -> Path:
    txt = normalize_input(txt)
    p = Path(txt).expanduser()

    # 1) Absolute or relative path exactly as typed
    if p.exists():
        return p.resolve()

    # 2) If only a file name was typed, try Downloads
    p_downloads = downloads_dir() / txt
    if p_downloads.exists():
        return p_downloads.resolve()

    # Return best guess for error message
    return p_downloads.resolve()


def generate_output_path(input_path: Path) -> Path:
    base = input_path.with_name(f"{input_path.stem}_no_background.png")
    if not base.exists():
        return base

    i = 1
    while True:
        candidate = input_path.with_name(f"{input_path.stem}_no_background_{i}.png")
        if not candidate.exists():
            return candidate
        i += 1


def get_session(model_name: str):
    if model_name in SESSION_CACHE:
        return SESSION_CACHE[model_name]

    from rembg import new_session

    print(f"Loading model '{model_name}'...")
    t0 = time.time()
    session = new_session(model_name)
    SESSION_CACHE[model_name] = session
    print(f"Model loaded in {time.time() - t0:.1f}s.")
    return session


def remove_background(input_path: Path, output_path: Path, session, quality: str) -> None:
    from rembg import remove

    with input_path.open("rb") as f:
        input_bytes = f.read()

    kwargs = {"session": session}

    # Fast mode skips alpha matting and is significantly faster.
    if quality == "high":
        kwargs.update(
            {
                "alpha_matting": True,
                "alpha_matting_foreground_threshold": 240,
                "alpha_matting_background_threshold": 10,
                "alpha_matting_erode_size": 10,
            }
        )
    else:
        kwargs["alpha_matting"] = False

    # AI segmentation removes background regardless of color.
    output_bytes = remove(input_bytes, **kwargs)

    with output_path.open("wb") as f:
        f.write(output_bytes)


def process_file(input_text: str, model_name: str, quality: str) -> int:
    input_path = resolve_input_path(input_text)

    if not input_path.exists():
        print(f"File not found: {input_path}")
        return 1

    if not is_image_file(input_path):
        print("Invalid format. Please use: .png / .jpg / .jpeg / .webp")
        return 1

    output_path = generate_output_path(input_path)

    print(f"Input file:  {input_path}")
    print(f"Output file: {output_path}")
    print("Removing background...")

    t0 = time.time()
    session = get_session(model_name)
    remove_background(input_path, output_path, session=session, quality=quality)
    print(f"Processed in {time.time() - t0:.1f} seconds. Saving...")
    print("Background removed successfully! ♡")
    return 0


def terminal_interface(model_name: str, quality: str) -> int:
    print_start_banner()
    print("Background Remover")
    print("Drag and drop your image into this window or type the file name.")
    print("Supported: .png .jpg .jpeg .webp")
    print(f"Mode: model={model_name} quality={quality}")
    print("To close use 'clear'")
    print(hr())

    while True:
        input_text = input("\nImage file/path: ").strip()
        if not input_text:
            continue

        cmd = normalize_input(input_text).lower()

        if cmd == "clear":
            clear_screen()
            print_start_banner()
            print("Background Remover")
            print("Drag and drop your image into this window or type the file name.")
            print("Supported: .png .jpg .jpeg .webp")
            print(f"Mode: model={model_name} quality={quality}")
            print("Commands: clear (clean screen), exit/quit (close)")
            print(hr())
            continue

        if cmd in EXIT_WORDS:
            print_closing_sequence()
            return 0

        process_file(input_text, model_name=model_name, quality=quality)


def main() -> int:
    init_console_utf8()

    model_name = "u2netp"
    quality = "fast"

    return terminal_interface(model_name=model_name, quality=quality)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")

        try:
            print_closing_sequence()
        except Exception:
            pass
        raise SystemExit(0)
    except Exception as exc:
        print("\nUnexpected error:", exc)
        print("\nDetails:")
        traceback.print_exc()
        if sys.stdin and sys.stdin.isatty():
            input("\nPress Enter to close...")
        raise SystemExit(1)