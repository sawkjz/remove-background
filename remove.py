from pathlib import Path
from rembg import remove
from PIL import Image
import time

EXTS = (".png", ".jpg", ".jpeg", ".webp")

def eh_imagem(p: Path) -> bool:
    return p.suffix.lower() in EXTS

def downloads_dir() -> Path:
    # Windows: C:\Users\<user>\Downloads
    return Path.home() / "Downloads"

def resolver_entrada(txt: str) -> Path:
    txt = txt.strip().strip('"')
    p = Path(txt)

    if p.is_absolute() and p.exists():
        return p

    p_downloads = downloads_dir() / txt
    return p_downloads

def gerar_saida(entrada: Path) -> Path:
    return entrada.with_name(f"{entrada.stem}_no_background.png")

if __name__ == "__main__":
    entrada_txt = input('Enter the file name or path (.png / .jpg / .jpeg / .webp): ').strip().strip('"')
    entrada = resolver_entrada(entrada_txt)

    if not entrada.exists():
        print(f"File not found: {entrada}")
        raise SystemExit(1)

    if not eh_imagem(entrada):
        print("Invalid format. Please use: .png / .jpg / .jpeg / .webp")
        raise SystemExit(1)

    saida = gerar_saida(entrada)

    print(f"Input file:  {entrada}")
    print(f"Output file: {saida}")
    print("Removing background...")
    t0 = time.time()

    img = Image.open(entrada)
    out = remove(img)

    print(f"Processed in {time.time() - t0:.1f} seconds. Saving...")
    out.save(saida)

    print("Background removed successfully! 🎀")