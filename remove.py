import argparse
import time
from pathlib import Path

from rembg import new_session, remove

EXTS = (".png", ".jpg", ".jpeg", ".webp")
EXIT_WORDS = {"sair", "exit", "clear"}


def eh_imagem(p: Path) -> bool:
    return p.suffix.lower() in EXTS


def downloads_dir() -> Path:
    # Windows: C:\Users\<user>\Downloads
    return Path.home() / "Downloads"


def normalizar_entrada(txt: str) -> str:
    return txt.strip().strip('"')


def resolver_entrada(txt: str) -> Path:
    txt = normalizar_entrada(txt)
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


def gerar_saida(entrada: Path) -> Path:
    base = entrada.with_name(f"{entrada.stem}_no_background.png")
    if not base.exists():
        return base

    i = 1
    while True:
        candidato = entrada.with_name(f"{entrada.stem}_no_background_{i}.png")
        if not candidato.exists():
            return candidato
        i += 1


def remover_fundo(entrada: Path, saida: Path, session) -> None:
    with entrada.open("rb") as f:
        input_bytes = f.read()

    # Removes background regardless of color
    output_bytes = remove(
        input_bytes,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )

    with saida.open("wb") as f:
        f.write(output_bytes)


def processar_arquivo(entrada_txt: str, session) -> int:
    entrada = resolver_entrada(entrada_txt)

    if not entrada.exists():
        print(f"File not found: {entrada}")
        return 1

    if not eh_imagem(entrada):
        print("Invalid format. Please use: .png / .jpg / .jpeg / .webp")
        return 1

    saida = gerar_saida(entrada)

    print(f"Input file:  {entrada}")
    print(f"Output file: {saida}")
    print("Removing background...")

    t0 = time.time()
    remover_fundo(entrada, saida, session=session)
    print(f"Processed in {time.time() - t0:.1f} seconds. Saving...")
    print("Background removed successfully! ♡")
    return 0


def interface_terminal(session) -> int:
    print("=" * 60)
    print("Background Remover")
    print("Drag and drop your image into this window or type the file name.")
    print("Supported: .png .jpg .jpeg .webp")
    print("Type 'clear' to close.")
    print("=" * 60)

    while True:
        entrada_txt = input("\nImage file/path: ").strip()
        if not entrada_txt:
            continue
        if normalizar_entrada(entrada_txt).lower() in EXIT_WORDS:
            print("Closing...")
            return 0

        processar_arquivo(entrada_txt, session=session)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove image background and save PNG with transparency, like a sticker ;)"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Image file path. If omitted, interactive terminal mode starts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session = new_session("u2net")

    if args.input:
        return processar_arquivo(args.input, session=session)

    return interface_terminal(session=session)


if __name__ == "__main__":
    raise SystemExit(main())
