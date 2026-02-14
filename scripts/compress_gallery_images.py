#!/usr/bin/env python3
"""
Compress Encanto Road gallery images for faster lightbox loading.

Strategy:
- Source: images/erps/*_orig.JPG and images/erbts/*_orig.JPG (large originals)
- Output: images/erps/erps001.jpg … erps008.jpg, images/erbts/erbts001.jpg … erbts018.jpg
- Resize: longest edge 1920px (enough for HD/retina in lightbox; originals are 3168×4752)
- JPEG quality: 85 (minimal visible loss, large size reduction)

Run from project root: python3 scripts/compress_gallery_images.py
"""

import os
import re
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Need Pillow: pip install Pillow")
    raise SystemExit(1)

# Config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAX_EDGE = 1920
JPEG_QUALITY = 85

ERPS_DIR = PROJECT_ROOT / "images" / "erps"
ERBTS_DIR = PROJECT_ROOT / "images" / "erbts"
ERPS_ORIG_PATTERN = re.compile(r"^erps(\d+)_orig\.(JPG|jpg)$", re.I)
ERBTS_ORIG_PATTERN = re.compile(r"^erbts(\d+)_orig\.(JPG|jpg)$", re.I)


def resize_and_save(img_path: Path, out_path: Path) -> None:
    img = Image.open(img_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    if w <= MAX_EDGE and h <= MAX_EDGE:
        img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
        return
    if w >= h:
        new_w, new_h = MAX_EDGE, int(h * MAX_EDGE / w)
    else:
        new_w, new_h = int(w * MAX_EDGE / h), MAX_EDGE
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def process_dir(directory: Path, pattern: re.Pattern, prefix: str) -> list[Path]:
    saved = []
    for f in sorted(directory.iterdir()):
        if not f.is_file():
            continue
        m = pattern.match(f.name)
        if not m:
            continue
        num = m.group(1)
        out_name = f"{prefix}{num}.jpg"
        out_path = directory / out_name
        resize_and_save(f, out_path)
        saved.append(out_path)
    return saved


def main() -> None:
    os.chdir(PROJECT_ROOT)
    all_saved = []
    if ERPS_DIR.is_dir():
        all_saved.extend(process_dir(ERPS_DIR, ERPS_ORIG_PATTERN, "erps"))
    if ERBTS_DIR.is_dir():
        all_saved.extend(process_dir(ERBTS_DIR, ERBTS_ORIG_PATTERN, "erbts"))
    if not all_saved:
        print("No *_orig.JPG files found in images/erps or images/erbts.")
        return
    print(f"Wrote {len(all_saved)} compressed images (max edge {MAX_EDGE}px, quality {JPEG_QUALITY}).")
    for p in all_saved:
        print(f"  {p.relative_to(PROJECT_ROOT)} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
