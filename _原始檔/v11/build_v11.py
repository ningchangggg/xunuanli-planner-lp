"""手帳落地頁 v11（2026-11-26）：只產生 v11 新增／改版的區塊，其餘沿用 v10 說明圖。
新增：03／03a 受眾卡四張（每張疊一張她寫的那一頁紙條，名牌改紙膠帶）、03c 送禮範例開盒動圖、03d 先寫第一頁再送（扉頁手寫動圖）、
04a 寫不下去的三個瞬間、ch1–ch3 HOW TO USE 章節條、09 手帳人自我檢查表。共用樣式 base.css（旅行 v28）。"""
css = open('base.css').read()
EXTRA = r'''
@font-face{font-family:Liao;src:url(fonts/jfliao_nohint.ttf)}
:root{--tape:#E8C7A6;--tape2:#B9CBB4;--tape3:#AFC6D8;--tape4:#E3B7B9;--grid:rgba(140,132,125,.13)}
.hand{font-family:Liao,Cream,serif}
.tape{position:absolute;height:20px;background:var(--c,var(--tape));opacity:.86;
  clip-path:polygon(0 8%,4% 0,9% 10%,14% 2%,100% 0,97% 30%,100% 55%,96% 78%,100% 100%,6% 96%,0 100%,3% 70%,0 45%,4% 22%);
  box-shadow:0 1px 2px rgba(0,0,0,.06)}
.tape.dot{background-image:radial-gradient(rgba(255,255,255,.75) 1.4px,transparent 1.6px);background-size:7px 7px}
.gridpaper{background-color:#FFFDF8;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:12px 12px}
#s03{padding-bottom:0}#s03a{background:var(--paper2);padding:16px 0 26px}#s03 .cd:last-child{margin-bottom:10px!important}
#s03 .cd,#s03a .cd{margin-bottom:26px}#s03a .cd:last-child{margin-bottom:0}
.cd .ov .who{border:0;font-size:26px;color:var(--ink);padding:3px 14px 2px;position:relative;margin:6px 0 2px -4px;transform:rotate(-1.5deg);letter-spacing:.12em}
.cd .ov .who:before{content:"";position:absolute;inset:0;z-index:-1;background:var(--c,var(--tape));opacity:.95;
  clip-path:polygon(0 6%,3% 0,100% 4%,98% 35%,100% 62%,97% 100%,2% 96%,0 70%,2% 40%)}
.cd .ov{isolation:isolate}
.cd .ov h3{text-shadow:0 1px 8px rgba(0,0,0,.35)}
.cd .note{position:absolute;z-index:3;background:#FFFDF8;padding:7px 7px 8px;box-shadow:0 8px 18px rgba(20,16,12,.35)}
.cd .note img{display:block;width:100%}
.cd .note .tape{top:-11px;left:50%;width:74px;margin-left:-37px;transform:rotate(-3deg)}
.cd .note .lb{font-family:Liao;font-size:12.5px;color:#6E5A48;margin:5px 2px 0;letter-spacing:.04em}
.cd .tk{background-color:#FFFDF8;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:12px 12px;position:relative}
.cd .tk:before{content:"";position:absolute;right:18px;top:-8px;width:52px;height:16px;background:var(--c,var(--tape));opacity:.8;transform:rotate(4deg);
  clip-path:polygon(0 0,100% 6%,96% 50%,100% 100%,0 94%,4% 50%)}
.cd .tk .route{width:92px}.cd .tk .route b{font-size:15px}
.cd .tk p mark{color:inherit;background:linear-gradient(100deg,transparent 2%,rgba(248,222,96,.72) 4%,rgba(246,214,80,.6) 60%,rgba(248,222,96,.75) 96%,transparent 98%) no-repeat 0 72%/100% 58%;padding:0 3px;margin:0 -1px;border-radius:2px 5px 3px 6px}
/* 送禮範例 */
.gift{padding:36px 20px 30px;background:var(--paper)}
.gift h2{margin-top:10px}.gift .lead{margin-top:8px}
.gift .mv{position:relative;width:392px;margin:22px auto 0;border-radius:6px;overflow:visible}
.gift .mv .ph{width:392px;height:490px;background-size:cover;background-position:center;border-radius:6px;box-shadow:0 8px 22px rgba(30,27,25,.16)}
.gift .tag{position:absolute;left:-6px;top:16px;z-index:2;padding:4px 14px 3px;font-size:14px;color:var(--ink);letter-spacing:.12em;transform:rotate(-2deg)}
.gift .tag:before{content:"";position:absolute;inset:0;z-index:-1;background:var(--tape);clip-path:polygon(0 6%,3% 0,100% 4%,98% 50%,100% 100%,2% 96%,0 60%)}
.gift .tag{isolation:isolate}.gift .tag i{font-style:normal;font-family:"Helvetica Neue",Arial;font-size:10px;letter-spacing:.2em;margin-right:6px;color:#7A5A3C}
.inbox{margin:18px auto 0;width:392px;position:relative;padding:18px 18px 16px;box-shadow:0 6px 16px rgba(30,27,25,.1)}
.inbox .tape{top:-10px;left:22px;width:86px;transform:rotate(-4deg)}
.inbox .t{font-family:Liao;font-size:15px;color:#6E5A48;letter-spacing:.06em}
.inbox ol{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:10px 14px;margin-top:10px}
.inbox li{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--ink);letter-spacing:.04em}
.inbox li b{flex:none;width:22px;height:22px;border-radius:50%;border:1px solid var(--brick);color:var(--brick);font-family:"Helvetica Neue",Arial;font-size:11px;display:flex;align-items:center;justify-content:center}
.inbox .bag{margin-top:14px;padding-top:14px;border-top:1px dashed #D9CFC2}
.inbox .bag .im{width:100%;height:218px;background:url(img/n_bag.jpg) center 55%/cover;border-radius:4px;box-shadow:0 4px 12px rgba(30,27,25,.18)}.inbox .bag .tx{display:flex;align-items:baseline;gap:12px;margin-top:12px}.inbox .bag .tx>div:last-child{flex:1}
.inbox .bag .k{font-size:11.5px;color:var(--brick);letter-spacing:.2em}
.inbox .bag .v{font-size:15.5px;color:var(--ink);margin-top:2px;letter-spacing:.06em}
.inbox .bag .s{font-size:12.5px;color:var(--text);margin-top:3px;line-height:1.6}
#s03d{background:var(--paper2)}
#s03d .pg{position:relative;width:412px;margin:24px auto 0;padding:8px;background:#FFFDF8;box-shadow:0 10px 24px rgba(30,27,25,.16);transform:rotate(-1deg)}
#s03d .pg .ph{width:396px;height:200px;background-size:cover;background-position:center}
#s03d .pg .tape{top:-10px;width:70px}
#s03d .pg .tape.l{left:-14px;transform:rotate(-28deg);top:-2px}#s03d .pg .tape.r{right:-14px;transform:rotate(28deg);top:-2px;--c:var(--tape3)}
#s03d .steps3{display:flex;justify-content:center;gap:10px;margin-top:22px}
#s03d .steps3 div{flex:1;max-width:122px;text-align:center;background:#FFFDF8;border-radius:4px;padding:10px 6px 9px;box-shadow:0 3px 8px rgba(30,27,25,.08)}
#s03d .steps3 i{display:block;font-style:normal;font-family:"Helvetica Neue",Arial;font-size:9.5px;letter-spacing:.2em;color:var(--brick)}
#s03d .steps3 b{display:block;font-size:14.5px;color:var(--ink);margin-top:3px;letter-spacing:.06em}
#s03d .steps3 span{display:block;font-family:Liao;font-size:12px;color:#6E5A48;margin-top:2px}
/* 04a 痛點 */
#s04a{padding:38px 16px 32px;background:var(--paper2)}
#s04a h2{margin-top:10px}#s04a .lead{margin-top:8px}
.pain{margin-top:22px;display:flex;flex-direction:column;gap:18px}
.pain .row{display:flex;align-items:center;gap:8px}
.pain .st{flex:none;width:128px;min-height:104px;background:#FBEA9E;padding:14px 12px 12px;transform:rotate(-2.5deg);box-shadow:0 6px 12px rgba(30,27,25,.14);position:relative}
.pain .row:nth-child(2) .st{transform:rotate(2deg);background:#F7D2D2}.pain .row:nth-child(3) .st{transform:rotate(-1.5deg);background:#D8E6D2}
.pain .st:before{content:"";position:absolute;left:0;right:0;top:0;height:14px;background:rgba(0,0,0,.035)}
.pain .st i{font-style:normal;font-family:"Helvetica Neue",Arial;font-size:9px;letter-spacing:.22em;color:#8C6A4A}
.pain .st p{font-family:Liao;font-size:17px;line-height:1.45;color:#3A2B21;margin-top:5px}
.pain .ar{flex:none;width:22px;text-align:center;color:var(--brick);font-size:18px;font-family:"Helvetica Neue",Arial}
.pain .so{flex:1;background:#FFFDF8;border-radius:4px;overflow:hidden;box-shadow:0 6px 16px rgba(30,27,25,.1)}
.pain .so .im{height:98px;background-size:cover;background-position:center top;border-bottom:1px solid var(--line)}
.pain .so .tx{padding:9px 12px 10px}
.pain .so .k{font-size:10.5px;color:var(--brick);letter-spacing:.2em}
.pain .so .v{font-size:14.5px;line-height:1.55;color:var(--ink);margin-top:2px;letter-spacing:.03em}
#s04a .end{margin-top:24px;text-align:center;font-size:17px;color:var(--ink);letter-spacing:.08em}
#s04a .end span{background:linear-gradient(transparent 62%,rgba(188,68,60,.22) 62%)}
/* 章節條 */
.ch{background:var(--paper2);padding:34px 20px 4px;text-align:center}
.ch .lab{display:inline-block;position:relative;padding:4px 16px 3px;font-family:"Helvetica Neue",Arial;font-size:11px;letter-spacing:.3em;color:#5A4636;isolation:isolate;transform:rotate(-2deg)}
.ch .lab:before{content:"";position:absolute;inset:0;z-index:-1;background:var(--c);clip-path:polygon(0 8%,4% 0,100% 6%,97% 50%,100% 100%,3% 94%,0 55%)}
.ch .big{font-size:40px;color:var(--ink);letter-spacing:.2em;margin-top:12px;line-height:1.2}
.ch .sub{font-family:Liao;font-size:15px;color:#6E5A48;margin-top:6px;letter-spacing:.06em}
.ch .rule{margin:18px auto 0;width:160px;border-top:1px dashed #CBBFAF}
/* 09 檢查表 */
#s09{padding:38px 16px 34px;background:var(--paper)}
#s09 h2{margin-top:10px;color:var(--ink)}#s09 .eyebrow{color:var(--brick)}#s09 .lead{color:var(--text)}#s09 .lead{margin-top:8px}
.chk{position:relative;margin:24px 6px 0;padding:22px 20px 18px;box-shadow:0 8px 20px rgba(30,27,25,.12);transform:rotate(-.6deg)}
.chk>.tape{top:-10px;width:96px}.chk>.tape.l{left:24px;transform:rotate(-5deg)}.chk>.tape.r{right:24px;transform:rotate(4deg);--c:var(--tape2)}
.chk .hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px solid var(--ink);padding-bottom:8px}
.chk .hd b{font-size:17px;color:var(--ink);letter-spacing:.1em}.chk .hd span{font-family:"Helvetica Neue",Arial;font-size:9.5px;letter-spacing:.22em;color:var(--taupe)}
.chk ul{list-style:none}
.chk li{display:flex;align-items:center;gap:12px;padding:12px 2px;border-bottom:1px dashed #D9CFC2;font-size:15px;color:var(--ink);letter-spacing:.04em}
.chk li .bx{flex:none;width:20px;height:20px;border:1.6px solid #4A3D36;border-radius:3px;position:relative}
.chk li svg{position:absolute;left:-3px;top:-12px;width:32px;height:32px;overflow:visible}
.chk li svg path{fill:none;stroke:var(--brick);stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round}
.chk .res{margin-top:16px;text-align:center}
.chk .res .a{font-family:Liao;font-size:18px;color:#6E5A48}
.chk .res .b{font-size:21px;color:var(--ink);letter-spacing:.08em;margin-top:4px}
.chk .res .b span{background:linear-gradient(transparent 60%,rgba(248,222,96,.75) 60%)}
'''

def note(src, x, y, w, rot, lb, c='--tape'):
    return (f'<div class="note" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
            f'<span class="tape" style="--c:var({c})"></span><img src="{src}"><div class="lb">{lb}</div></div>')

P = [
 dict(n='01', who='行程控上班族', c='--tape', h='開會、待辦、生活瑣事，都寫在同一頁', k1='寫在', v1='週計畫', k2='用來', v2='排行程',
      p='左頁<mark>排行程</mark>，右頁<mark>畫進度</mark>，<br>每打一個勾都<mark>好療癒</mark>。', img='img/q1.jpg',
      note=note('img/n_week.jpg', 12, 12, 158, -3, '她的週計畫'),),
 dict(n='02', who='想更懂自己的人', c='--tape2', h='每月覺察引導，<br>不只忙碌安排生活、也靜心傾聽自己', k1='寫在', v1='每月覺察', k2='用來', v2='認識自己',
      p='<mark>12 個自我覺察主題</mark>，<br>跟著提問寫，<mark>不怕不知道怎麼寫</mark>。', img='img/q2.jpg',
      note=note('img/n_reflect.jpg', 164, 10, 258, 2.5, '她的 1 月覺察', '--tape2')),
 dict(n='03', who='每年寫到三月的人', c='--tape3', h='年初買了新手帳，翻到四月就是空白', k1='寫在', v1='年計畫', k2='用來', v2='寫完一年',
      p='一個跨頁排好 <mark>12 個月</mark>，<br>翻開就知道<mark>自己走到哪了</mark>。', img='img/q4.jpg',
      note=note('img/n_year.jpg', 60, 4, 322, -1.5, '這次，一路寫到 12 月', '--tape3')),
 dict(n='04', who='聖誕交換禮物', c='--tape4', h='預算一千，想送得精美又有心意', k1='附贈', v1='皮革手帳袋', k2='送給', v2='知心好友',
      p='扉頁寫上<mark>他的名字</mark>，<br>就是<mark>只給他的</mark>一本。', img='img/q4gift.jpg', note=''),
]
def card(x):
    return f'''<div class="cd" style="--c:var({x["c"]})"><div class="ph" style="background-image:url({x["img"]})">{x["note"]}<div class="ov"><div class="no en">NO. {x["n"]}</div><div class="who">{x["who"]}</div><h3>{x["h"]}</h3></div></div>
<div class="tk"><div class="route"><div>{x["k1"]}<b>{x["v1"]}</b></div><div>{x["k2"]}<b>{x["v2"]}</b></div></div><div><p>{x["p"]}</p></div></div></div>'''

CHECK = '<svg viewBox="0 0 32 32"><path d="M4 17 C7 19 10 23 12 27 C16 18 22 9 31 2"/></svg>'
ITEMS = [('待辦寫在手背上，洗完手就不見了', True), ('手機備忘錄超過 300 則', True), ('年初許的願望，年底才想起來', True),
         ('喜歡文具，卻捨不得用', False), ('想好好過一年，不知道從哪開始', False)]
chk = ''.join(f'<li><span class="bx">{CHECK if on else ""}</span>{t}</li>' for t, on in ITEMS)

def ch(sid, n, big, sub, c):
    return f'''<section id="{sid}" class="ch"><span class="lab" style="--c:var({c})">CHAPTER {n}</span><div class="big">{big}</div><div class="sub">{sub}</div><div class="rule"></div></section>'''

body = f'''
<section id="s03">
  <div class="eyebrow">誰適合這本手帳？</div>
  <h2>聖誕禮物 x 交換禮物<br><span class="mark">送禮送到心坎裡</span></h2>
  <div class="lead">一天寫一點，365 天，<br>一整年都是他自己的樣子。</div>
  {card(P[0])}{card(P[1])}
</section>
<section id="s03a">{card(P[2])}{card(P[3])}</section>
<section id="s03c" class="gift">
  <div class="eyebrow">送禮範例</div>
  <h2>打開盒子的那一刻，<br><span class="mark">就是禮物</span></h2>
  <div class="lead">掀開純白外盒，先看到一張試筆紙，<br>再看見今年的那一本。</div>
  <div class="mv"><div class="tag"><i>GIFT BOX</i>純白禮盒</div><div class="ph" data-clip="f_open" style="background-image:url(gif/clips/f_open/001.jpg)"></div></div>
  <div class="inbox gridpaper"><span class="tape dot"></span><div class="t">盒子裡有什麼？</div>
    <ol><li><b>1</b>純白外盒</li><li><b>2</b>一張試筆紙</li><li><b>3</b>2027 手帳</li><li><b>4</b>皮革燙金手帳袋</li></ol>
    <div class="bag"><div class="im"></div><div class="tx"><div><div class="k">聖誕加碼</div><div class="v">送皮革燙金手帳袋</div></div><div class="s">燙金 MEET MYSELF HERE，<br>手帳、筆、便利貼一起收好。</div></div></div>
  </div>
</section>
<section id="s03d" class="gift">
  <div class="eyebrow">送禮小撇步</div>
  <h2>先寫第一頁，<br><span class="mark">再把它送出去</span></h2>
  <div class="lead">扉頁留了 TO. 和 DATE.，<br>寫上他的名字，就是只給他的一本。</div>
  <div class="pg"><span class="tape l"></span><span class="tape r"></span><div class="ph" data-clip="hw_gift" style="background-image:url(gif/clips/hw_gift/001.jpg)"></div></div>
  <div class="steps3"><div><i>TO.</i><b>寫他的名字</b><span>親愛的小美</span></div><div><i>DATE.</i><b>寫送出那天</b><span>2026.12.25</span></div><div><i>NOTE</i><b>留一句話</b><span>換你好好寫自己</span></div></div>
</section>
<section id="s04a">
  <div class="eyebrow">寫不下去的三個瞬間</div>
  <h2>買了手帳，<br><span class="mark">卻總是寫不下去？</span></h2>
  <div class="lead">不是你不夠自律，<br>是空白頁沒有告訴你從哪裡開始。</div>
  <div class="pain">
    <div class="row"><div class="st"><i>STUCK 01</i><p>空白頁，<br>不知道要寫什麼</p></div><div class="ar">→</div>
      <div class="so"><div class="im" style="background-image:url(img/t_reflectq.jpg)"></div><div class="tx"><div class="k">每月覺察</div><div class="v">每個月三個提問，<br>跟著回答就好</div></div></div></div>
    <div class="row"><div class="st"><i>STUCK 02</i><p>一週好亂，<br>不知道怎麼排</p></div><div class="ar">→</div>
      <div class="so"><div class="im" style="background-image:url(img/t_week2.jpg)"></div><div class="tx"><div class="k">週計畫</div><div class="v">一天一格，時間、待辦、<br>小事分開寫</div></div></div></div>
    <div class="row"><div class="st"><i>STUCK 03</i><p>一年過完，<br>想不起做了什麼</p></div><div class="ar">→</div>
      <div class="so"><div class="im" style="background-image:url(img/t_year2.jpg)"></div><div class="tx"><div class="k">年計畫</div><div class="v">12 個月排在一個跨頁，<br>一眼看完這一年</div></div></div></div>
  </div>
  <div class="end"><span>不用很會寫，跟著頁面走就好</span></div>
</section>
{ch('ch1', '01', '一週', '時間、待辦、生活瑣事', '--tape')}
{ch('ch2', '02', '一個月', '月計畫攤開，再聽聽自己', '--tape2')}
{ch('ch3', '03', '一整年', '從年計畫，寫到願景板', '--tape3')}
<section id="s09">
  <div class="eyebrow">手帳人自我檢查表</div>
  <h2>你是不是，<br><span class="mark">也需要一本手帳？</span></h2>
  <div class="chk gridpaper"><span class="tape l"></span><span class="tape r"></span>
    <div class="hd"><b>2027 手帳需求檢查</b><span>SELF CHECK</span></div>
    <ul>{chk}</ul>
    <div class="res"><div class="a">勾了兩個以上？</div><div class="b"><span>2027，你需要一本手帳</span></div></div>
  </div>
</section>
'''
html = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<style>
{css}
{EXTRA}
</style></head><body>
{body}
</body></html>'''
open('page.html', 'w').write(html)
print('ok', len(html))
