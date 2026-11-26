"""手帳落地頁「內頁怎麼使用」六個示範，2026-11-24。
阿寧：示範字體用 jf-liao-proportional；週計畫（生活瑣事、核取方塊打勾、時間點開會）、右側空白（畫畫＋甘特圖）、
月計畫（全頁攤平）、每月覺察引導、年計畫甘特圖（螢光筆畫區間再寫字）、顯化願景板。
底圖：2027 煦暖曆 MEET MTSELF HERE 電子版手帳 PDF 330 dpi（3846×2729 跨頁）。座標用 1000 寬預覽的值 × K。
每個示範是一串 step；第 k 張圖＝前 k 個 step，之後在 make_frames 做逐筆擦出動畫。
用法：python3 demo.py [week grid month reflect year vision]"""
import os, sys, math, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hand as H
JF = os.path.join(HERE, '..', 'fonts', 'jfliao_nohint.ttf')
for k in list(H.FONTS): H.FONTS[k] = (JF, 0)
H._fc.clear()
K = 3.846
INK, BLUE, RED, BROWN, GREEN = H.BLACK, H.BLUE, H.RED, H.BROWN, H.GREEN
LP = os.path.normpath(os.path.join(HERE, '..', '..', 'lp3', 'img'))

def W(l, x, y, t, px=62, col=INK, seed=0, rot=0.0):
    return H.write(l, x * K, y * K, t, 'hanno', px, col, 0.93, rot=rot, jit=0.8, track=0.03, seed=seed)
def CHK(l, x, y, seed=0, done=True):
    H.box(l, x * K, y * K, 40, INK, 5, seed)
    if done: H.check(l, x * K + 4, y * K - 14, 48, RED, 8, seed + 1)
def HL(l, x0, y0, x1, y1, col=H.HL_YELLOW, seed=0, a=0.5):
    H.highlight(l, x0 * K, y0 * K, x1 * K, y1 * K, col, a, seed)

# ------------------------------------------------------------ 1 週計畫左頁（p008 左，日：28 一 … 03 日）
def week():
    R = [40 + 95.6 * i for i in range(7)]   # 每天那一列的上緣
    def day(i, items):
        def f(pg):
            l = pg.layer()
            for j, it in enumerate(items):
                y = R[i] + 36 + j * 22
                kind, txt = it[0], it[1]
                x = 95
                if kind in ('c', 'o'):
                    CHK(l, x, y + 1, seed=i * 10 + j, done=(kind == 'c')); x += 16
                col = it[2] if len(it) > 2 else INK
                W(l, x, y, txt, 66, col, seed=i * 10 + j)
        return f
    def hl(i, j, x1, col):
        return lambda pg: HL(pg.layer(), 108, R[i] + 26 + j * 22, x1, R[i] + 40 + j * 22, col, seed=i)
    def dood(fn): return lambda pg: fn(pg.layer())
    return 'p008', [
        day(0, [('c', '10:00 週會（帶年終簡報）'), ('c', '回覆廠商的信'), ('t', '午餐和小美吃拉麵', BLUE)]),
        dood(lambda l: H.cup(l, 430 * K, (R[0] + 70) * K, 70, H.SKY_P, BROWN, 3)),
        day(1, [('t', '14:30 牙醫回診', RED), ('c', '繳電話費'), ('o', '下班去全聯：牛奶、雞蛋')]),
        hl(1, 0, 170, H.HL_PINK),
        day(2, [('c', '9:30 開會：明年計畫'), ('c', '整理桌面＋丟舊文件'), ('t', '晚上瑜伽 50 分鐘', GREEN)]),
        day(3, [('t', '跨年夜！和家人吃火鍋', RED), ('t', '倒數完許三個願望')]),
        hl(3, 0, 300, H.HL_ORANGE),
        dood(lambda l: (H.sparkle(l, 410 * K, (R[3] + 40) * K, 34, H.SUN_P, seed=5), H.star(l, 450 * K, (R[3] + 62) * K, 26, H.SUN_P, seed=6))),
        day(4, [('t', '2027 第一天，睡到自然醒'), ('t', '寫下今年三個願望 → 願景板', BLUE)]),
        dood(lambda l: H.sun(l, 440 * K, (R[4] + 52) * K, 34, H.SUN_P, seed=7)),
        day(5, [('c', '洗衣服、換床單'), ('c', '下午咖啡廳寫手帳'), ('o', '打電話給阿嬤')]),
        day(6, [('c', '準備下週便當'), ('t', '23:00 前上床睡覺', BROWN)]),
        dood(lambda l: H.heart(l, 445 * K, (R[6] + 50) * K, 28, H.ROSE_P, seed=9)),
    ], (0, 0, 1923, 2729)

# ------------------------------------------------------------ 2 週計畫右頁方格：甘特圖＋畫畫（p008 右）
def grid():
    X0 = 520; c = 16.67          # 方格每格約 16.67（預覽）
    rows = [('資料整理', 0, 2, H.HL_MINT), ('寫簡報', 1, 4, H.HL_YELLOW), ('主管確認', 4, 5, H.HL_PINK), ('提案！', 5, 6, H.HL_ORANGE)]
    def title(pg):
        l = pg.layer(); W(l, X0, 72, 'W.01 年終提案進度', 84, INK, 1); H.underline(l, X0 * K, 820 * K, 78 * K, RED, 6, True, 2)
    def head(pg):
        l = pg.layer()
        for k, d in enumerate('MTWTFSS'):
            W(l, X0 + 150 + k * 2 * c + 10, 112, d, 60, BROWN, 10 + k)
    def bar(i):
        name, a, b, col = rows[i]
        def f(pg):
            l = pg.layer(); y = 140 + i * 2 * c
            W(l, X0, y + 7, name, 64, INK, 20 + i)
            HL(l, X0 + 150 + a * 2 * c + 3, y - 8, X0 + 150 + b * 2 * c - 3, y + 10, col, seed=30 + i, a=0.75)
        return f
    def mark(pg):
        l = pg.layer(); x = X0 + 150 + 5.5 * 2 * c
        H.star(l, x * K, 268 * K, 30, H.SUN_P, RED, 40); W(l, x - 50, 304, '週六交！', 64, RED, 41)
    def draw1(pg):
        l = pg.layer(); W(l, X0, 370, '今天的小確幸', 76, BLUE, 50)
        H.cup(l, 610 * K, 470 * K, 300, H.CARAMEL_P, BROWN, 51); W(l, 560, 565, '燕麥拿鐵', 62, BROWN, 52)
    def draw2(pg):
        l = pg.layer(); H.flower(l, 770 * K, 450 * K, 130, H.ROSE_P, H.SUN_P, 5, 53); H.leaf_sprig(l, 850 * K, 560 * K, 420, H.SAGE_P, 54)
        H.flower(l, 900 * K, 430 * K, 95, H.SKY_P, H.SUN_P, 6, 55); W(l, 730, 560, '路邊的花', 58, H.ROSE_P, 59)
    def draw3(pg):
        l = pg.layer(); H.cloud(l, 640 * K, 630 * K, 150, H.SKY_P, seed=56); H.sun(l, 880 * K, 620 * K, 70, H.SUN_P, 57)
        W(l, X0, 690, '散步 30 分鐘，天氣超好', 70, GREEN, 58)
    return 'p008', [title, head, bar(0), bar(1), bar(2), bar(3), mark, draw1, draw2, draw3], (1923, 0, 3846, 2729)

# ------------------------------------------------------------ 3 月計畫跨頁（p007，2027 年 1 月）
def month():
    cols = [125, 250, 375, 500, 625, 750, 875]; rows = [33, 130, 227, 323, 420]
    def cell(day):
        off = 4                      # 1 日是週五 → 第一列索引 4
        i = day - 1 + off; return cols[i % 7], rows[i // 7]
    E = {1: [('t', '元旦', RED), ('t', '睡到飽')], 2: [('t', '大掃除', GREEN)], 4: [('c', '開工')], 5: [('t', '10:00', BLUE), ('t', '週會')], 6: [('c', '健檢')], 7: [('c', '繳卡費')], 8: [('t', '小美生日', RED)], 9: [('t', '看電影', BLUE)], 12: [('c', '寄包裹')], 14: [('t', '瑜伽', GREEN)], 18: [('c', '剪頭髮')], 20: [('t', '聚餐', BROWN)], 22: [('c', '還書')], 24: [('t', '爬山', GREEN)], 27: [('c', '交報告')], 30: [('t', '回老家', RED)],
         11: [('c', '牙醫')], 13: [('t', '健身 ×3', GREEN)], 15: [('c', '報稅資料')], 16: [('t', '看展', BLUE)], 19: [('t', '14:00', RED), ('t', '提案')],
         21: [('c', '讀完一本書')], 23: [('t', '京都訂房', BLUE)], 26: [('t', '月底結帳')], 29: [('c', '發薪水！')], 31: [('t', '月回顧', BROWN)]}
    steps = []
    def ent(days):
        def f(pg):
            l = pg.layer()
            for d in days:
                x, y = cell(d)
                for j, it in enumerate(E[d]):
                    xx = x + 12; yy = y + 46 + j * 24
                    if it[0] == 'c': CHK(l, xx, yy + 1, seed=d); xx += 17
                    W(l, xx, yy, it[1].replace('🎂', ''), 72, it[2] if len(it) > 2 else INK, seed=d)
        return f
    ds = sorted(E);
    for k in range(0, len(ds), 3): steps.append(ent(ds[k:k + 3]))
    def deco(pg):
        l = pg.layer()
        x, y = cell(8); H.heart(l, (x + 100) * K, (y + 62) * K, 22, H.ROSE_P, seed=1)
        x, y = cell(19); H.loop(l, (x + 50) * K, (y + 52) * K, 200, 110, RED, 6, 2)
        x, y = cell(23); HL(l, x + 8, y + 32, x + 112, y + 50, H.HL_BLUE, seed=3)
        x, y = cell(29); H.sparkle(l, (x + 100) * K, (y + 40) * K, 26, H.SUN_P, seed=4)
    def side(pg):
        l = pg.layer(); W(l, 14, 125, '本月目標', 68, RED, 70)
        for j, t in enumerate(['早睡早起', '存 1 萬', '讀 2 本書']):
            CHK(l, 14, 160 + j * 28, seed=71 + j, done=j != 1); W(l, 30, 160 + j * 28, t, 60, INK, 72 + j)
    def note(pg):
        l = pg.layer(); W(l, 20, 655, '一月：把生活慢慢排好，不急。', 84, BLUE, 80)
        H.washi(l, 900 * K, 640 * K, 420, 90, -6, (236, 200, 170), 'stripe', seed=81)
        H.leaf_sprig(l, 820 * K, 690 * K, 160, H.SAGE_P, 82)
    return 'p007', steps + [deco, side, note], (0, 0, 3846, 2729)

# ------------------------------------------------------------ 4 每月覺察引導（p005 右頁）
def reflect():
    def ans(y, txt, col=INK, seed=0):
        return lambda pg: W(pg.layer(), 772, y, txt, 62, col, seed)
    def words(pg):
        l = pg.layer()
        for k, (t, x) in enumerate([('忙碌', 560), ('在學習', 700), ('想慢下來', 860)]):
            W(l, x, 450, t, 66, BLUE, 30 + k); H.loop(l, (x + 40) * K, 442 * K, 200 if len(t) < 4 else 260, 70, RED, 5, 33 + k)
    def thank(pg):
        l = pg.layer(); W(l, 528, 608, '謝謝自己今天還是準時下班，', 58, INK, 40); W(l, 528, 636, '沒有把情緒帶回家。', 58, INK, 41)
        HL(l, 528, 624, 660, 640, H.HL_YELLOW, 42); H.heart(l, 860 * K, 630 * K, 30, H.ROSE_P, seed=43)
    def tape(pg):
        l = pg.layer(); H.washi(l, 900 * K, 36 * K, 380, 80, 8, (200, 220, 205), 'dot', seed=50)
    return 'p005', [ans(84, '工作、開會、\n還有很多待辦', INK, 1), ans(184, '下班後泡澡、\n週末去咖啡廳', GREEN, 2),
                    ans(284, '一直想做到最好，\n其實有點累了', RED, 3), words, thank, tape], (1923, 0, 3846, 2729)

# ------------------------------------------------------------ 5 年計畫甘特圖（p004）
def year():
    X0, CW = 62, 29.13        # 第 1 日欄左緣、每欄寬（預覽）
    Y = [69 + 52.5 * i for i in range(12)]
    B = [(0, 4, 22, '學日文 N4', H.HL_YELLOW), (1, 6, 14, '春節回老家', H.HL_PINK), (2, 1, 31, '每天走路 8000 步', H.HL_MINT),
         (3, 3, 7, '京都旅行', H.HL_BLUE), (4, 10, 28, '搬家準備', H.HL_ORANGE), (5, 12, 20, '證照考試', H.HL_PINK),
         (6, 1, 15, '存旅費', H.HL_MINT), (7, 7, 10, '生日', H.HL_YELLOW), (8, 1, 30, '健身每週三次', H.HL_BLUE),
         (9, 9, 17, '專案上線', H.HL_ORANGE), (10, 1, 20, '讀完六本書', H.HL_MINT), (11, 20, 31, '聖誕＋跨年', H.HL_PINK)]
    def bars(idx):
        def f(pg):
            l = pg.layer()
            for i in idx:
                m, a, b, t, col = B[i]; y = Y[m]
                HL(l, X0 + (a - 1) * CW + 2, y - 12, X0 + b * CW - 2, y + 12, col, seed=i, a=0.7)
        return f
    def labels(idx):
        def f(pg):
            l = pg.layer()
            for i in idx:
                m, a, b, t, col = B[i]; W(l, X0 + (a - 1) * CW + 8, Y[m] + 9, t, 76, INK, 10 + i)
        return f
    steps = []
    for k in range(0, 12, 3):
        steps += [bars(range(k, k + 3)), labels(range(k, k + 3))]
    def deco(pg):
        l = pg.layer(); H.star(l, (X0 + 7 * CW) * K, (Y[3] - 2) * K, 26, H.SUN_P, RED, 60)
        H.heart(l, (X0 + 10.6 * CW) * K, (Y[7]) * K, 24, H.ROSE_P, seed=61)
        H.sparkle(l, (X0 + 31.6 * CW) * K, (Y[11]) * K, 26, H.SUN_P, seed=62)
    return 'p004', steps + [deco], (0, 0, 3846, 2729)

# ------------------------------------------------------------ 6 顯化願景板（p003 左頁）
def _photo(n):
    im = Image.open(os.path.join(LP, f'p{n:03d}_1.jpg')).convert('RGB'); w, h = im.size
    return im.crop((0, int(h * 0.12), int(w * 0.66), h))
def vision():
    def quad(x, y, txt, col, seed):
        return lambda pg: W(pg.layer(), x, y, txt, 68, col, seed)
    def center(pg):
        l = pg.layer(); W(l, 182, 318, '2027 想成為', 60, BROWN, 20); W(l, 160, 352, '溫柔而堅定的人', 72, RED, 21)
        H.underline(l, 160 * K, 345 * K, 360 * K, RED, 6, True, 22)
    def pol1(pg):
        l = pg.layer('over'); H.polaroid(l, _photo(10), 395 * K, 210 * K, 520, 6, caption='京都 / 富士山', seed=30)
        H.washi(l, 395 * K, 130 * K, 260, 70, -4, (238, 214, 170), 'plain', seed=31)
    def pol2(pg):
        l = pg.layer('over'); H.polaroid(l, _photo(187), 110 * K, 555 * K, 480, -5, caption='一起去旅行', seed=32)
        H.washi(l, 110 * K, 480 * K, 240, 66, 5, (200, 220, 205), 'dot', seed=33)
    def deco(pg):
        l = pg.layer(); H.sparkle(l, 220 * K, 140 * K, 30, H.SUN_P, seed=40); H.heart(l, 450 * K, 600 * K, 30, H.ROSE_P, seed=41)
        H.leaf_sprig(l, 300 * K, 470 * K, 200, H.SAGE_P, 42); H.star(l, 60 * K, 150 * K, 24, H.SUN_P, seed=43)
    return 'p003', [quad(24, 96, '學會日文 N3\n讀完 12 本書\n每週寫手帳', INK, 1), quad(268, 96, '經營自己的\n小品牌', BLUE, 2),
                    quad(24, 420, '每天睡滿 7 小時\n跑完半馬！', GREEN, 3), quad(300, 430, '帶媽媽去旅行\n每月家庭聚餐', BROWN, 4),
                    center, pol1, pol2, deco], (0, 0, 1923, 2729)


# ------------------------------------------------------------ 7 扉頁送禮（p002 右頁 TO./DATE.），v11 03d
def gift():
    def to(pg): W(pg.layer(), 596, 120, '親愛的小美', 80, INK, 1)
    def date(pg): W(pg.layer(), 850, 120, '2026.12.25', 60, INK, 2)
    def note(pg):
        l = pg.layer(); W(l, 672, 271, '2027，換你好好寫自己了！', 66, RED, 3)
    def deco(pg):
        l = pg.layer(); H.heart(l, 848 * K, 262 * K, 30, H.ROSE_P, seed=4)
        H.underline(l, 672 * K, 830 * K, 279 * K, RED, 6, True, 5)
    return 'p002', [to, date, note, deco], (1923, 150, 3846, 1120)

DEMOS = dict(gift=gift, week=week, grid=grid, month=month, reflect=reflect, year=year, vision=vision)

def build(name, out):
    page, steps, crop = DEMOS[name]()
    os.makedirs(out, exist_ok=True)
    base = os.path.join(HERE, page + '.png')
    for k in range(len(steps) + 1):
        pg = H.Page(base)
        for s in steps[:k]: s(pg)
        im = pg.render().crop(crop)
        w = 1200; im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(os.path.join(out, f'{k:02d}.png'))
    print(name, len(steps), im.size)

if __name__ == '__main__':
    names = sys.argv[1:] or list(DEMOS)
    for n in names: build(n, os.path.join(HERE, 'steps', n))
