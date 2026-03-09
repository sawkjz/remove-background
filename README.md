# *Background Remover (Python)*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011-informational)](#)

A simple Python script to remove image backgrounds using **rembg** (ONNX) and save the result as a **transparent PNG**.

## Features
- Removes background and outputs **PNG with transparency**
- If you type only a filename, it searches inside **Downloads** (Windows)
- Accepts a full path (you can also **drag & drop** the file into the terminal)
- Supported formats: `.png`, `.jpg`, `.jpeg`, `.webp`

## Requirements
- Python **3.10+** (recommended: **3.12**)
- Windows 11 (should work on other OS with minor changes)

## Installation (CPU - recommended)
```bash
py -m pip install -U pip
py -m pip install "rembg[cpu]" pillow
```

If you have an NVIDIA GPU + CUDA properly configured:

```bash
py -m pip install "rembg[gpu]" pillow
```

## Usage
Run the script:

```bash
py remove.py
```

Then enter:
- A full image path (you can drag and drop into terminal), or
- Only the file name to search in your `Downloads` folder.

The output image is saved in the same folder with the suffix `_no_background.png`.

You can also run with the image path directly:

```bash
py remove.py "C:\Users\YourUser\Downloads\photo.jpg"
```

Use faster/default mode:

```bash
py remove.py --model u2netp --quality fast
```

Use higher quality edges (slower):

```bash
py remove.py --model u2net --quality high
```

## Build .exe (Windows)
Install PyInstaller:

```bash
py -m pip install pyinstaller
```

### Option A (recommended): faster startup and smaller executable file (`onedir`)
This creates a folder distribution. The main `.exe` is smaller and opens faster.

```bash
py -m PyInstaller --clean --onedir --console --name background_remover --icon assets/icon.ico --copy-metadata rembg --copy-metadata pymatting --exclude-module matplotlib --exclude-module scipy --exclude-module pandas --exclude-module IPython remove.py
```

Output:
- `dist\background_remover\background_remover.exe`

### Option B: single file (`onefile`)
More portable (single file), but usually heavier and slower to start.

```bash
py -m PyInstaller --clean --onefile --console --name background_remover --icon assets/icon.ico --copy-metadata rembg --copy-metadata pymatting remove.py
```

Output:
- `dist\background_remover.exe`

When executed, it opens a terminal interface where the user can:
- Drag and drop an image file, or
- Type the file name/path manually.

### Performance tips
- Default model is now `u2netp` (faster startup and processing).
- Use default mode `--quality fast` for speed.
- Use `--quality high` only when you need better edge refinement.
- First run may still be slower due to model/cache initialization.

## How Background Removal Works
This project uses `rembg` with the `u2net` model, which performs **AI foreground segmentation**.

Important:
- It does **not** remove only dark colors.
- It predicts the subject/object mask and removes background of **any color**.
- `alpha matting` is enabled in the script to improve edge quality (hair, soft borders, and semi-transparent details).
