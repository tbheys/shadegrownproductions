# Scripts

## Gallery image compression

**Problem:** Encanto Road Production Stills and Behind the Scenes originals are ~3168×4752 px and ~2–3 MB each (~64 MB total), which is more than needed for lightbox viewing and slows loading.

**Approach:**

| Setting      | Value  | Reason |
|-------------|--------|--------|
| Max dimension | 1920 px | Lightbox rarely needs more than full‑HD width; keeps retina sharpness. |
| JPEG quality | 85     | Very small visible loss, large file-size reduction. |
| Source       | `*_orig.JPG` in `images/erps/` and `images/erbts/` | Originals stay untouched. |
| Output       | `erps001.jpg` … `erps008.jpg`, `erbts001.jpg` … `erbts018.jpg` | Names expected by `gallery.html`. |

**Run (from project root):**

```bash
python3 scripts/compress_gallery_images.py
```

Requires: `pip install Pillow`

**Result:** Compressed set is ~8 MB total instead of ~64 MB; lightbox images load much faster with minimal loss in fidelity.
