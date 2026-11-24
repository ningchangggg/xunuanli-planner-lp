"""封面兩種款式輪播（v10）：開窗款 four.jpg ↔ 素面款 麻豆照片 974，各停 1.8 秒、淡入淡出 0.4 秒，標籤用凝書體烤進畫面。"""
import os, sys, shutil
from PIL import Image, ImageOps, ImageDraw, ImageFont
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1]
im = ImageOps.exif_transpose(Image.open(P + '/四本手帳/2027煦暖曆系列_毛片-974.jpg')).convert('RGB')
w, h = im.size; y0 = int(h * 0.53 - w / 2)
B = im.crop((0, y0, w, y0 + w)).resize((1080, 1080), Image.LANCZOS)
A = Image.open(D + '/img/four.jpg').convert('RGB').resize((1080, 1080), Image.LANCZOS)
CN = ImageFont.truetype(D + '/fonts_cream.otf', 44)
EN = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
def label(img, zh, en, idx):
    img = img.copy(); d = ImageDraw.Draw(img, 'RGBA')
    x, y = 45, 1080 - 45 - 132
    tw = max(d.textlength(zh, font=CN) + 30, d.textlength(en, font=EN) + len(en) * 5)
    d.rounded_rectangle((x, y, x + tw + 60, y + 132), 10, fill=(252, 250, 246, 235))
    d.rectangle((x, y, x + 8, y + 132), fill=(188, 68, 60, 255))
    d.text((x + 32, y + 22), zh, font=CN, fill=(28, 38, 51), spacing=0)
    ex = x + 32
    for ch in en:
        d.text((ex, y + 86), ch, font=EN, fill=(188, 68, 60)); ex += d.textlength(ch, font=EN) + 5
    for k in range(2):
        cx = 1080 - 80 + k * 30; cy = 1080 - 60
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(255, 255, 255, 240 if k == idx else 110))
    return img
LA = label(A, '風景開窗款', 'WINDOW COVER', 0)
LB = label(B, '經典素面款', 'CLASSIC COVER', 1)
od = D + '/gif/clips/f_style'; shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
fr = [LA] * 27 + [Image.blend(LA, LB, (i + 1) / 7) for i in range(6)] + [LB] * 27 + [Image.blend(LB, LA, (i + 1) / 7) for i in range(6)]
for i, f in enumerate(fr): f.save(f'{od}/{i + 1:03d}.jpg', quality=92)
print(len(fr))
