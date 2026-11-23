"""Handwriting on the planner's inside pages, 2026-10-30 (user: 以 pdf 內頁為底圖，參考圖二～圖四「真人手寫感的手帳內容」來做 banner).
Pages come from 2027 煦暖曆 MEET MTSELF HERE_電子版手帳(跨頁).pdf rendered at 330 dpi (內頁快取/pNNN.png, 3846 x 2729 per spread;
coordinates here are page px at that size). Fonts are the macOS handwriting faces 手札體 Hannotate TC and 翩翩體 HanziPen TC
(+ Noteworthy / Bradley Hand for Latin). Every glyph gets its own size / angle / baseline jitter; pens multiply onto the paper
(gel: slight density wobble, pencil: grainy), highlighters sit under the ink, tape / photos / stickers on top."""
import glob, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

def _sys(name):
    g = sorted(glob.glob(f'/System/Library/AssetsV2/com_apple_MobileAsset_Font*/*/AssetData/{name}'))
    if not g: raise FileNotFoundError(name + ' (download it once in Font Book)')
    return g[0]
FONTS = {'hanno': (_sys('Hannotate.ttc'), 1), 'hanno_b': (_sys('Hannotate.ttc'), 3),
         'pen': (_sys('Hanzipen.ttc'), 1), 'pen_b': (_sys('Hanzipen.ttc'), 3),
         'note': ('/System/Library/Fonts/Noteworthy.ttc', 0), 'note_b': ('/System/Library/Fonts/Noteworthy.ttc', 1),
         'bradley': ('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf', 0)}
_fc = {}
def F(key, px):
    k = (key, int(round(px)))
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[key][0], k[1], index=FONTS[key][1])
    return _fc[k]

# pens / pencils / highlighters
BLACK, BLUE, RED, BROWN, GREEN = (38, 36, 44), (44, 72, 140), (196, 58, 52), (122, 82, 52), (70, 120, 90)
CARAMEL_P, SAGE_P, SKY_P, ROSE_P, SUN_P = (190, 128, 72), (128, 160, 120), (110, 160, 205), (225, 130, 140), (236, 182, 60)
HL_YELLOW, HL_PINK, HL_MINT, HL_BLUE, HL_ORANGE = (255, 232, 96), (255, 176, 196), (166, 226, 204), (160, 206, 244), (255, 200, 140)

class Page:
    """a spread plus drawing layers composited in creation order ('mul' = ink / highlighter, 'over' = tape, photos)"""
    def __init__(self, path):
        self.base = Image.open(path).convert('RGB'); self.size = self.base.size; self.layers = []
    def layer(self, mode='mul'):
        l = Image.new('RGBA', self.size, (0, 0, 0, 0)); self.layers.append((mode, l)); return l
    def render(self):
        b = np.asarray(self.base, np.float32) / 255
        for mode, l in self.layers:
            a = np.asarray(l, np.float32) / 255; al = a[..., 3:4]
            if mode == 'mul': b = b * (1 - al + al * a[..., :3])
            else: b = b * (1 - al) + a[..., :3] * al
        return Image.fromarray((b.clip(0, 1) * 255).astype(np.uint8))

def _noise(w, h, rng, scale=6, aniso=None):
    n = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    if aniso: im = im.filter(ImageFilter.GaussianBlur(aniso))
    return np.asarray(im, np.float32) / 255

def _pencil(w, h, rng, angle=35):
    """colored-pencil grain: noise smeared along `angle` (stroke direction) plus a little paper tooth, mostly covered"""
    n = Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8)).rotate(angle, expand=True)
    W_, H_ = n.size; n = n.resize((max(2, W_ // 9), H_), Image.BILINEAR).resize((W_, H_), Image.BICUBIC).rotate(-angle)
    n = np.asarray(n.crop(((n.width - w) // 2, (n.height - h) // 2, (n.width - w) // 2 + w, (n.height - h) // 2 + h)), np.float32) / 255
    tooth = _noise(w, h, rng, 2)
    return np.clip(0.62 + 2.6 * (n - n.mean()) + 0.35 * (tooth - 0.5), 0, 1)

def _ink(layer, mask, box, col, alpha, tex, rng):
    """put colour col through L-mask (box-sized) onto layer at box[0:2] with a pen texture"""
    m = np.asarray(mask, np.float32) / 255; h, w = m.shape
    if tex == 'gel': m = m * (0.86 + 0.14 * _noise(w, h, rng, 9))
    elif tex == 'pencil': m = m * _pencil(w, h, rng)
    elif tex == 'marker': m = m * (0.93 + 0.07 * _noise(w, h, rng, 20))
    a = Image.fromarray((m * alpha * 255).clip(0, 255).astype(np.uint8))
    tile = Image.new('RGBA', (w, h), col + (0,)); tile.putalpha(a)
    layer.alpha_composite(tile, (int(box[0]), int(box[1])))

def write(layer, x, y, text, font='hanno', px=60, col=BLACK, alpha=0.93, rot=0.0, jit=1.0, track=0.02, lead=None,
          tex='gel', seed=0, bold=0):
    """handwritten text, baseline starting at (x, y), rot = line angle in degrees (+ = rising); '\\n' starts a new line
    lead px lower. Returns the end point of the last line."""
    rng = np.random.default_rng(seed); lead = lead or px * 1.45
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for li, line in enumerate(text.split('\n')):
        lx, ly = x + li * lead * sa, y + li * lead * ca + rng.normal(0, px * 0.04 * jit)
        lx += rng.normal(0, px * 0.06 * jit) if li else 0
        d = 0.0; glyphs = []
        drift = rng.normal(0, 0.6 * jit)                                     # each line wanders a little
        for ch in line:
            if ch == ' ': d += px * 0.32; continue
            s = px * (1 + rng.normal(0, 0.045 * jit)); f = F(font, s); w = f.getlength(ch)
            a = rot + drift + rng.normal(0, 2.6 * jit)
            off = rng.normal(0, px * 0.04 * jit)
            gx, gy = lx + d * ca + off * sa, ly - d * sa + off * ca
            glyphs.append((ch, f, s, w, a, gx, gy)); d += w * (1 + rng.normal(0, 0.035 * jit)) + px * track
        if not glyphs: continue
        xs = [g[5] for g in glyphs]; ys = [g[6] for g in glyphs]
        x0, y0 = int(min(xs) - px * 1.5), int(min(ys) - px * 2.0); x1, y1 = int(max(xs) + px * 2.5), int(max(ys) + px * 1.2)
        mask = Image.new('L', (x1 - x0, y1 - y0), 0)
        for ch, f, s, w, a, gx, gy in glyphs:
            pad = int(s * 0.6); g = Image.new('L', (int(w + 2 * pad), int(s * 1.5 + 2 * pad)), 0)
            ImageDraw.Draw(g).text((pad, pad + s * 1.1), ch, font=f, fill=255, anchor='ls', stroke_width=bold, stroke_fill=255)
            g = g.rotate(a, resample=Image.BICUBIC, center=(pad + w / 2, pad + s * 0.75))
            mask.paste(ImageChops.lighter(mask.crop((int(gx - pad - x0), int(gy - s * 1.1 - pad - y0),
                       int(gx - pad - x0) + g.width, int(gy - s * 1.1 - pad - y0) + g.height)), g),
                       (int(gx - pad - x0), int(gy - s * 1.1 - pad - y0)))
        _ink(layer, mask.filter(ImageFilter.GaussianBlur(0.6)), (x0, y0), col, alpha, tex, rng)
        end = (lx + d * ca, ly - d * sa)
    return end

def text_w(text, font, px): return sum(F(font, px).getlength(c) for c in text) * 1.02

def _jitter_path(pts, rng, amp, step=18):
    out = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(xb - xa, yb - ya) / step))
        for i in range(n):
            t = i / n; out.append((xa + (xb - xa) * t, ya + (yb - ya) * t))
    out.append(pts[-1])
    walk = np.cumsum(rng.normal(0, amp * 0.35, (len(out), 2)), axis=0); walk -= np.linspace(walk[0], walk[-1], len(out))
    return [(p[0] + q[0], p[1] + q[1]) for p, q in zip(out, walk)]

def stroke(layer, pts, col=BLACK, w=7, alpha=0.9, tex='gel', seed=0, amp=3.0, closed=False):
    rng = np.random.default_rng(seed); pts = list(pts) + ([pts[0]] if closed else [])
    pts = _jitter_path(pts, rng, amp)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; x0, y0 = int(min(xs) - w * 3), int(min(ys) - w * 3)
    m = Image.new('L', (int(max(xs) - x0 + w * 3), int(max(ys) - y0 + w * 3)), 0); d = ImageDraw.Draw(m)
    q = [(p[0] - x0, p[1] - y0) for p in pts]; d.line(q, fill=255, width=int(w), joint='curve')
    for p in (q[0], q[-1]): d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=255)
    _ink(layer, m.filter(ImageFilter.GaussianBlur(0.7)), (x0, y0), col, alpha, tex, rng)

def fill(layer, draw_fn, box, col, alpha=0.75, tex='pencil', seed=0):
    """fill whatever draw_fn(draw, x0, y0) draws (white, in box coords) — colored-pencil shading by default"""
    rng = np.random.default_rng(seed); x0, y0, x1, y1 = [int(v) for v in box]
    m = Image.new('L', (x1 - x0, y1 - y0), 0); draw_fn(ImageDraw.Draw(m), x0, y0)
    _ink(layer, m.filter(ImageFilter.GaussianBlur(0.8)), (x0, y0), col, alpha, tex, rng)

def highlight(layer, x0, y0, x1, y1, col=HL_YELLOW, alpha=0.5, seed=0, slant=None):
    """a chisel highlighter swipe (multiply layer), a bit uneven, darker where the stroke starts and ends"""
    rng = np.random.default_rng(seed); h = y1 - y0; slant = h * 0.25 if slant is None else slant
    top = [(x0 + slant, y0)] + [(x0 + (x1 - x0) * t, y0 + rng.normal(0, h * 0.04)) for t in np.linspace(0.05, 0.95, 8)] + [(x1 + slant, y0)]
    bot = [(x1 - slant, y1)] + [(x1 - (x1 - x0) * t, y1 + rng.normal(0, h * 0.04)) for t in np.linspace(0.05, 0.95, 8)] + [(x0 - slant, y1)]
    bx0, by0 = int(x0 - h), int(y0 - h)
    m = Image.new('L', (int(x1 - x0 + 2 * h), int(3 * h)), 0)
    ImageDraw.Draw(m).polygon([(p[0] - bx0, p[1] - by0) for p in top + bot], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    xx = np.arange(a.shape[1])[None, :] + bx0
    a = a * (0.88 + 0.12 * _noise(a.shape[1], a.shape[0], rng, 4, aniso=None)) * (1 + 0.25 * (np.exp(-((xx - x0) / (h * 0.4)) ** 2) + np.exp(-((xx - x1) / (h * 0.4)) ** 2)))
    tile = Image.new('RGBA', m.size, col + (0,)); tile.putalpha(Image.fromarray((a.clip(0, 1) * alpha * 255).astype(np.uint8)))
    layer.alpha_composite(tile, (bx0, by0))

# ------------------------------------------------------------------ doodles
def check(layer, x, y, s=50, col=RED, w=8, seed=0):
    stroke(layer, [(x, y), (x + s * 0.35, y + s * 0.42), (x + s, y - s * 0.55)], col, w, 0.92, 'gel', seed, amp=1.5)

def box(layer, x, y, s=40, col=BLACK, w=5, seed=0):
    stroke(layer, [(x, y - s), (x + s, y - s), (x + s, y), (x, y), (x, y - s - 3)], col, w, 0.85, 'gel', seed, amp=1.2)

def strike(layer, x0, x1, y, col=BLACK, w=6, seed=0):
    stroke(layer, [(x0, y), (x1, y - 4)], col, w, 0.85, 'gel', seed, amp=2)

def underline(layer, x0, x1, y, col=RED, w=6, wavy=False, seed=0):
    if wavy: pts = [(x0 + (x1 - x0) * t, y + 8 * math.sin(t * 14)) for t in np.linspace(0, 1, 40)]
    else: pts = [(x0, y), (x1, y - 6)]
    stroke(layer, pts, col, w, 0.88, 'gel', seed, amp=1.5)

def loop(layer, cx, cy, rx, ry, col=RED, w=6, seed=0):
    """a hand-drawn circle around something, overshooting where it closes"""
    rng = np.random.default_rng(seed); a0 = rng.uniform(0, 6.28)
    pts = [(cx + rx * (1 + 0.04 * math.sin(3 * t)) * math.cos(a0 + t), cy + ry * math.sin(a0 + t)) for t in np.linspace(0, 6.28 * 1.12, 60)]
    stroke(layer, pts, col, w, 0.88, 'gel', seed, amp=2)

def star(layer, cx, cy, r, col=SUN_P, line=None, seed=0, w=5, alpha=0.85):
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(i * math.pi / 5), cy - (r if i % 2 == 0 else r * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
    fill(layer, lambda d, x0, y0: d.polygon([(p[0] - x0, p[1] - y0) for p in pts], fill=255), (cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), col, alpha, seed=seed)
    if line: stroke(layer, pts, line, w, 0.8, 'gel', seed, amp=1, closed=True)

def sparkle(layer, cx, cy, r, col=SUN_P, w=6, seed=0):
    """a four-point twinkle (concave sides), filled"""
    pts = []
    for k in range(32):
        t = k / 32 * 2 * math.pi; rr = r * (0.3 + 0.7 * abs(math.cos(2 * t)) ** 1.5)
        pts.append((cx + rr * math.sin(t), cy - rr * math.cos(t)))
    fill(layer, lambda d, x0, y0: d.polygon([(p[0] - x0, p[1] - y0) for p in pts], fill=255), (cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), col, 0.92, tex='marker', seed=seed)

def heart(layer, cx, cy, r, col=ROSE_P, line=None, seed=0, alpha=0.85):
    pts = [(cx + r * 16 * math.sin(t) ** 3 / 16, cy - r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16) for t in np.linspace(0, 6.28, 40)]
    fill(layer, lambda d, x0, y0: d.polygon([(p[0] - x0, p[1] - y0) for p in pts], fill=255), (cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2), col, alpha, seed=seed)
    if line: stroke(layer, pts, line, max(3, r / 9), 0.85, 'gel', seed, amp=1, closed=True)

def cloud(layer, cx, cy, r, col=SKY_P, line=None, seed=0, alpha=0.7):
    blobs = [(-0.9, 0.15, 0.55), (-0.35, -0.25, 0.7), (0.35, -0.15, 0.62), (0.9, 0.2, 0.5), (0, 0.25, 0.6)]
    def dr(d, x0, y0):
        for bx, by, br in blobs: d.ellipse([cx + (bx - br) * r - x0, cy + (by - br) * r - y0, cx + (bx + br) * r - x0, cy + (by + br) * r - y0], fill=255)
    fill(layer, dr, (cx - 1.6 * r, cy - 1.1 * r, cx + 1.6 * r, cy + 1.0 * r), col, alpha, seed=seed)

def sun(layer, cx, cy, r, col=SUN_P, seed=0):
    fill(layer, lambda d, x0, y0: d.ellipse([cx - r - x0, cy - r - y0, cx + r - x0, cy + r - y0], fill=255), (cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), col, 0.85, seed=seed)
    for i in range(8):
        a = i * math.pi / 4; stroke(layer, [(cx + 1.35 * r * math.cos(a), cy + 1.35 * r * math.sin(a)), (cx + 1.8 * r * math.cos(a), cy + 1.8 * r * math.sin(a))], col, max(5, r / 5), 0.9, 'marker', seed + i, amp=1)

def flower(layer, cx, cy, r, petal=ROSE_P, mid=SUN_P, n=5, seed=0):
    def dr(d, x0, y0):
        for i in range(n):
            a = i * 2 * math.pi / n; px_, py_ = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
            d.ellipse([px_ - r * 0.45 - x0, py_ - r * 0.45 - y0, px_ + r * 0.45 - x0, py_ + r * 0.45 - y0], fill=255)
    fill(layer, dr, (cx - r * 1.1, cy - r * 1.1, cx + r * 1.1, cy + r * 1.1), petal, 0.8, seed=seed)
    fill(layer, lambda d, x0, y0: d.ellipse([cx - r * 0.25 - x0, cy - r * 0.25 - y0, cx + r * 0.25 - x0, cy + r * 0.25 - y0], fill=255),
         (cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3), mid, 0.9, seed=seed + 1)

def leaf_sprig(layer, x, y, h, col=SAGE_P, seed=0):
    stroke(layer, [(x, y), (x + h * 0.05, y - h * 0.5), (x - h * 0.02, y - h)], col, max(4, h / 30), 0.85, 'pencil', seed, amp=2)
    for k in range(4):
        t = 0.25 + k * 0.2; yy = y - h * t; s = -1 if k % 2 else 1
        fill(layer, lambda d, x0, y0, yy=yy, s=s: d.ellipse([x + s * h * 0.02 - x0 + (0 if s > 0 else -h * 0.22), yy - h * 0.06 - y0, x + s * h * 0.02 - x0 + (h * 0.22 if s > 0 else 0), yy + h * 0.06 - y0], fill=255),
             (x - h * 0.3, yy - h * 0.1, x + h * 0.3, yy + h * 0.1), col, 0.75, seed=seed + k)

def arrow(layer, pts, col=BLACK, w=6, seed=0):
    stroke(layer, pts, col, w, 0.88, 'gel', seed, amp=2)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]; a = math.atan2(yb - ya, xb - xa); L = w * 4
    for s in (-1, 1):
        stroke(layer, [(xb, yb), (xb - L * math.cos(a + s * 0.5), yb - L * math.sin(a + s * 0.5))], col, w, 0.88, 'gel', seed + 3 + s, amp=1)

# ------------------------------------------------------------------ things stuck on the page ('over' layers)
def washi(layer, cx, cy, w, h, ang, col, pattern='plain', alpha=0.78, seed=0, col2=(255, 255, 255)):
    rng = np.random.default_rng(seed); t = Image.new('RGBA', (int(w), int(h)), col + (255,)); d = ImageDraw.Draw(t)
    if pattern == 'stripe':
        for x in range(-int(h), int(w), int(h * 0.5)): d.polygon([(x, h), (x + h * 0.25, h), (x + h * 0.25 + h, 0), (x + h, 0)], fill=col2 + (255,))
    elif pattern == 'dot':
        st = h / 3.2
        for yy in np.arange(st / 2, h, st):
            for xx in np.arange(st / 2 + (st / 2 if int(yy / st) % 2 else 0), w, st): d.ellipse([xx - st * 0.16, yy - st * 0.16, xx + st * 0.16, yy + st * 0.16], fill=col2 + (255,))
    elif pattern == 'grid':
        st = h / 4
        for xx in np.arange(0, w, st): d.line([(xx, 0), (xx, h)], fill=col2 + (255,), width=max(1, int(h / 40)))
        for yy in np.arange(0, h, st): d.line([(0, yy), (w, yy)], fill=col2 + (255,), width=max(1, int(h / 40)))
    a = np.full((int(h), int(w)), alpha, np.float32) * (0.93 + 0.07 * _noise(int(w), int(h), rng, 8))
    for e in (0, 1):                                                         # torn ends
        for yy in range(int(h)):
            k = int(abs(rng.normal(0, h * 0.05)) + h * 0.02)
            if e == 0: a[yy, :k] = 0
            else: a[yy, int(w) - k:] = 0
    t.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    t = t.rotate(ang, resample=Image.BICUBIC, expand=True)
    layer.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))

def _shadow_paste(layer, im, cx, cy, ang, blur=14, off=(8, 12), alpha=0.35):
    im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', im.size, (40, 30, 20, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    pad = blur * 3; big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(sh, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(big, (int(cx - im.width / 2 - pad + off[0]), int(cy - im.height / 2 - pad + off[1])))
    layer.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def polaroid(layer, photo, cx, cy, w, ang=0, border=0.06, bottom=0.2, caption=None, cap_font='pen', cap_col=BLACK, seed=0):
    """a printed photo with a white border (photo: PIL image, cropped to the wanted aspect)"""
    b = int(w * border); pw = w - 2 * b; ph = int(pw * photo.height / photo.width); hb = int(w * bottom) if caption is not None else b
    card = Image.new('RGBA', (w, ph + b + hb), (252, 250, 245, 255)); card.paste(photo.convert('RGB').resize((pw, ph), Image.LANCZOS), (b, b))
    if caption:
        tmp = Image.new('RGBA', card.size, (0, 0, 0, 0)); write(tmp, b + 6, ph + b + hb * 0.62, caption, cap_font, hb * 0.45, cap_col, seed=seed)
        card.alpha_composite(tmp)
    _shadow_paste(layer, card, cx, cy, ang)
    return card.size

def sticker(layer, draw_fn, cx, cy, r, ang=0, bg=(252, 250, 245)):
    """a round die-cut sticker: white border, draw_fn(layer, cx, cy, r) paints the art on a temp 'mul' layer"""
    s = int(r * 2.4); im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([s / 2 - r * 1.12, s / 2 - r * 1.12, s / 2 + r * 1.12, s / 2 + r * 1.12], fill=(255, 255, 255, 255))
    d.ellipse([s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r], fill=bg + (255,))
    art = Image.new('RGBA', (s, s), (0, 0, 0, 0)); draw_fn(art, s / 2, s / 2, r)
    a = np.asarray(art, np.float32) / 255; base = np.asarray(im, np.float32) / 255; al = a[..., 3:4]
    base[..., :3] = base[..., :3] * (1 - al + al * a[..., :3]); im = Image.fromarray((base * 255).astype(np.uint8))
    _shadow_paste(layer, im, cx, cy, ang, blur=8, off=(4, 6), alpha=0.3)

def darker(c, k=0.72): return tuple(int(v * k) for v in c)

def cup(layer, cx, cy, s, col=SKY_P, line=BROWN, seed=0):
    """a coffee cup with steam, s = cup height"""
    body = [(cx - s * 0.45, cy - s * 0.5), (cx + s * 0.45, cy - s * 0.5), (cx + s * 0.36, cy + s * 0.45), (cx - s * 0.36, cy + s * 0.45)]
    fill(layer, lambda d, x0, y0: d.polygon([(p[0] - x0, p[1] - y0) for p in body], fill=255), (cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6), col, 0.8, seed=seed)
    stroke(layer, body, line, max(4, s / 22), 0.85, 'gel', seed, amp=1, closed=True)
    stroke(layer, [(cx + s * 0.43, cy - s * 0.3), (cx + s * 0.68, cy - s * 0.25), (cx + s * 0.66, cy + s * 0.05), (cx + s * 0.4, cy + s * 0.1)], line, max(4, s / 22), 0.85, 'gel', seed + 1, amp=1)
    for k in (-1, 1):
        x = cx + k * s * 0.15
        stroke(layer, [(x + s * 0.06 * math.sin(t * 6), cy - s * 0.62 - t * s * 0.45) for t in np.linspace(0, 1, 12)], line, max(3, s / 28), 0.7, 'gel', seed + 2 + k, amp=0.5)
