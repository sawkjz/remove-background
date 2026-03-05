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
