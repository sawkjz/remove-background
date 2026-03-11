import os
import sys
import time
import traceback
import shutil
from pathlib import Path
from typing import Dict

EXTS = (".png", ".jpg", ".jpeg", ".webp")
EXIT_WORDS = {"exit", "quit"}
SESSION_CACHE: Dict[str, object] = {}


def read_closing_art() -> str:
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return (base_dir / "closing_art.txt").read_text(encoding="utf-8")


CLOSING_ART = read_closing_art()


def console_utf8() -> None:
    if os.name == "nt":
        os.system("chcp 65001 > nul")
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def w() -> int:
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def line(ch="═") -> str:
    return ch * w()


def header(model_name: str, quality: str) -> None:
    bow = "𖹭"
    print(line())
    print(bow.center(w()))
    print("@sawkjz".rjust(w()))
    print("⊹")
    print("⢠⡏⠉⠑⢄⠀ ⠀  ⡠⠋⠉⢱⡀")
    print("⡇⠙⠒⠒⠬⡗⢒⢮⠄⠒⠒⠁⢣")
    print("⠇⠀⠈⠁⢁⡷⠤⢮⠈⠁⠀⠀⡌")
    print("⠘⢄⣀⡰⢻⠁⠀⠘⡕⢄⣀⡰⠁⠀⊹")
    print("⠀⡎⠘⢀⠇⠀⠀⠀⢱⠈⠂⠡⠀")
    print("⠀⠑⢄⡜⠢⡀⠀⢀⠔⠇⡴⠃⠀")
    print("⠀⠀⠀⠑⠠⠚⠀⠓⠔⠋⠀⠀")
    print("⊹")
    print(line())
    print("Background Remover")
    print("Supported: .png .jpg .jpeg .webp")
    print("Commands: clear (clean screen), exit (close)\n")
    print("Drag and drop your image here or type the file name.")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def downloads_dir() -> Path:
    return Path.home() / "Downloads"


def norm(txt: str) -> str:
    return txt.strip().strip('"')


def resolve_input_path(txt: str) -> Path:
    txt = norm(txt)
    p = Path(txt).expanduser()
    if p.exists():
        return p.resolve()

    p2 = downloads_dir() / txt
    return p2.resolve()


def is_image(p: Path) -> bool:
    return p.suffix.lower() in EXTS


def output_path_for(input_path: Path) -> Path:
    base = input_path.with_name(f"{input_path.stem}_no_background.png")
    if not base.exists():
        return base
    i = 1
    while True:
        cand = input_path.with_name(f"{input_path.stem}_no_background_{i}.png")
        if not cand.exists():
            return cand
        i += 1


def get_session(model_name: str):
    if model_name in SESSION_CACHE:
        return SESSION_CACHE[model_name]
    from rembg import new_session

    print(f"Loading model '{model_name}'...")
    t0 = time.time()
    s = new_session(model_name)
    SESSION_CACHE[model_name] = s
    print(f"Model loaded in {time.time() - t0:.1f}s.")
    return s


def remove_bg(inp: Path, out: Path, session, quality: str) -> None:
    from rembg import remove

    data = inp.read_bytes()
    kwargs = {"session": session, "alpha_matting": quality == "high"}
    if quality == "high":
        kwargs.update(
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10,
        )
    out.write_bytes(remove(data, **kwargs))


def process_file(txt: str, model_name: str, quality: str) -> int:
    inp = resolve_input_path(txt)
    if not inp.exists():
        print(f"File not found: {inp}")
        return 1
    if not is_image(inp):
        print("Invalid format. Use: .png / .jpg / .jpeg / .webp")
        return 1

    out = output_path_for(inp)
    print(f"Input:  {inp}")
    print(f"Output: {out}")
    print("Removing background...")

    t0 = time.time()
    session = get_session(model_name)
    remove_bg(inp, out, session=session, quality=quality)
    print(f"Done in {time.time() - t0:.1f}s. Saved. ♡")
    return 0


def closing() -> None:
    print()
    print(CLOSING_ART)
    time.sleep(0.35)
    print("\nClosing...")


def cli_args() -> list[str]:
    return [arg for arg in sys.argv[1:] if arg.strip()]


def run_arg_mode(args: list[str], model_name: str, quality: str) -> int:
    status = 0
    for arg in args:
        status = process_file(arg, model_name, quality) or status
    return status


def main() -> int:
    console_utf8()

    model_name = "u2netp"
    quality = "fast"

    args = cli_args()
    if args:
        return run_arg_mode(args, model_name, quality)

    header(model_name, quality)

    while True:
        try:
            s = input("\nImage file/path: ").strip()
        except EOFError:
            print("\nInput stream closed.")
            return 0

        if not s:
            continue

        cmd = norm(s).lower()

        if cmd == "clear":
            clear_screen()
            header(model_name, quality)
            continue

        if cmd in EXIT_WORDS:
            closing()
            return 0

        process_file(s, model_name, quality)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        closing()
        raise SystemExit(0)
    except Exception as exc:
        print("\nUnexpected error:", exc)
        traceback.print_exc()
        if sys.stdin and sys.stdin.isatty():
            try:
                input("\nPress Enter to close...")
            except EOFError:
                pass
        raise SystemExit(1)
