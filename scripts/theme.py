"""Abhi.Designs brand tokens + font embedding. Edit colors here, re-run the scripts."""
import base64, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER = os.environ.get("GH_USER", "abhidesigns11")

BG = "#0a0a0a"        # near-black, like the logo
PANEL_BORDER = "#262626"
WHITE = "#ffffff"
MUTED = "#9a9a9a"
RED = "#e8232a"       # brand red
RED_HOT = "#ff5a5f"

# heatmap ramp: no activity -> most activity (black -> deep red -> brand red -> white)
PALETTE = ["#171717", "#4d0f13", "#8c1a1f", "#e8232a", "#ff5a5f", "#ffffff"]

STATIC = os.environ.get("STATIC") == "1"   # STATIC=1 -> no animation (for previews)


def font_face(family, weight, filename, text):
    """Return an @font-face rule with a subset of the font embedded as base64.
    GitHub blocks external fonts in README images, so the font must live inside the SVG."""
    path = os.path.join(ROOT, "assets", "fonts", filename)
    try:
        from fontTools import subset
        opts = subset.Options()
        opts.flavor = "woff"
        font = subset.load_font(path, opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        buf = io.BytesIO()
        subset.save_font(font, buf, opts)
        data, mime = buf.getvalue(), "font/woff"
    except ImportError:
        data, mime = open(path, "rb").read(), "font/ttf"
    b64 = base64.b64encode(data).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:{mime};base64,{b64});}}")
