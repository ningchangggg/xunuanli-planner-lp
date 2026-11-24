"""手帳落地頁 page.html（照旅行 v28 規範），2026-11-24。共用樣式 base.css 來自旅行頁，手帳專屬的放在 EXTRA。"""
css = open('base.css').read()
EXTRA = '''
.cd .tk p mark{color:inherit;background:linear-gradient(100deg,transparent 2%,rgba(248,222,96,.72) 4%,rgba(246,214,80,.6) 60%,rgba(248,222,96,.75) 96%,transparent 98%) no-repeat 0 72%/100% 58%;padding:0 3px;margin:0 -1px;border-radius:2px 5px 3px 6px}
.cd .tk .route b{font-size:15px}
#s05{background:var(--night);padding:36px 16px 28px}
#s05 .eyebrow{color:#E9A493}#s05 h2{color:#fff;margin-top:10px}#s05 .lead{color:#C9C1B5;margin-top:8px}
.ov6{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}
.ov6 figure{margin:0;background:#fff;border-radius:4px;overflow:hidden;box-shadow:0 6px 16px rgba(0,0,0,.35)}
.ov6 figure.w{grid-column:span 2}
.ov6 img{display:block;width:100%}
.ov6 figcaption{font-size:12.5px;color:#F3EEE5;background:#25324A;padding:6px 10px;letter-spacing:.08em}
.ov6 figcaption i{font-style:normal;font-family:Helvetica,Arial;font-size:9.5px;color:#E9A493;letter-spacing:.18em;margin-right:6px}
.how .mv.pt{width:392px;height:590px;background:#3a3532}
.how .mv.pt .ph{bottom:34px}
.how .mv.ls{width:432px;height:306px;margin-left:-20px;border-radius:0}
.how .mv.ls .stub{display:none}
.how .cap2{font-size:12px;color:var(--taupe);text-align:center;margin-top:10px;letter-spacing:.06em}
#s09{background:var(--paper2);color:var(--ink);padding:38px 16px 30px}
#s09 .eyebrow{color:var(--brick)}#s09 h2{color:var(--ink)}#s09 .lead{color:var(--text)}
.q12{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:9px}
.q12 div{background:#FFFDF8;border-radius:3px;padding:10px 11px 9px;box-shadow:0 3px 8px rgba(30,27,25,.08);position:relative;border-left:3px solid var(--c)}
.q12 div:before{content:"";position:absolute;right:10px;top:-5px;width:34px;height:11px;background:var(--c);opacity:.55;transform:rotate(-4deg)}
.q12 b{display:block;font-family:Helvetica,Arial;font-weight:400;font-size:10px;letter-spacing:.2em;color:var(--taupe)}
.q12 span{display:block;font-size:14.5px;color:var(--ink);margin-top:3px;letter-spacing:.04em}
#s10 .ph{background-image:url(img/four.jpg)}
#s11 .ph{background-image:url(img/spec.jpg)}
#s06x .shade{position:absolute;left:0;right:0;top:0;height:200px;background:linear-gradient(rgba(18,14,10,.5),transparent)}
#s06x .tx{top:28px}#s06x .tx .a{color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.5)}
#s13{padding:38px 0 34px;background:var(--paper)}
#s13 h2{margin-top:10px}#s13 .lead{margin-top:8px}
#s13 .ph{width:432px;height:324px;background:url(img/bag.jpg) center/cover;margin-top:20px}
'''

P = [
 dict(n='01', who='行程控上班族', h='開會、待辦、生活瑣事，都寫在同一頁', k1='寫在', v1='週計畫', k2='用來', v2='排行程',
      p='左頁<mark>排行程</mark>，右頁<mark>畫進度</mark>，<br>每打一個勾都<mark>好療癒</mark>。', img='q1'),
 dict(n='02', who='想更懂自己的人', h='每個月一個問題，一年後更懂自己', k1='寫在', v1='每月覺察', k2='用來', v2='認識自己',
      p='<mark>12 個自我覺察主題</mark>，<br>跟著提問寫，<mark>不怕空白頁</mark>。', img='q2'),
 dict(n='03', who='交換禮物', h='禮物預算一千，送一本陪他一整年的手帳', k1='附贈', v1='手帳袋', k2='送給', v2='同事朋友',
      p='<mark>不用猜</mark>他喜歡什麼，<br>一年的空白，<mark>留給他自己寫</mark>。', img='q3'),
 dict(n='04', who='聖誕禮物', h='送一個讓他寫滿 2027 的禮物', k1='寫在', v1='願景板', k2='用來', v2='許願明年',
      p='別人的禮物拆完就收起來，<br>這本他會<mark>每天打開</mark>，<br>寫下<mark>自己的一整年</mark>！', img='q4'),
]
cards = ''.join(f'''<div class="cd"><div class="ph" style="background-image:url(img/{x["img"]}.jpg)"><div class="ov"><div class="no en">NO. {x["n"]}</div><div class="who">{x["who"]}</div><h3>{x["h"]}</h3></div></div>
<div class="tk"><div class="route"><div>{x["k1"]}<b>{x["v1"]}</b></div><span class="pl">✈</span><div>{x["k2"]}<b>{x["v2"]}</b></div></div><div><p>{x["p"]}</p></div></div></div>''' for x in P)

def how(i, sid, h, lead, clip, cls, step, en, cap=''):
    return f'''<section id="{sid}" class="how{' alt' if i % 2 == 0 else ''}">
  <div class="eyebrow">HOW TO USE 0{i}</div>
  <h2>{h}</h2>
  <div class="lead">{lead}</div>
  <div class="mv {cls}"><div class="ph" data-clip="{clip}" style="background-image:url(gif/clips/{clip}/001.jpg)"></div>
    <div class="stub"><span class="en">STEP 0{i}</span><b>{step}</b><span class="en">{en}</span></div></div>{f'<div class="cap2">{cap}</div>' if cap else ''}
</section>
'''
Q = ['理解目前的生活狀態', '開始意識改變', '關於懷疑與拉扯', '慢下來的提醒', '為自己留時間', '不穩定的過程',
     '開始理解自己', '面對內在情緒', '看見自己的改變', '把改變帶回生活', '建立自己的節奏', '再次遇見自己']
CC = ['#B9CBB4', '#E8C7A6', '#AFC6D8', '#E3B7B9']
q12 = ''.join(f'<div style="--c:{CC[k % 4]}"><b>{k + 1:02d} MONTH</b><span>{t}</span></div>' for k, t in enumerate(Q))

body = f'''
<section id="s03">
  <div class="eyebrow">誰適合這本手帳？</div>
  <h2>聖誕禮物 x 交換禮物<br><span class="mark">送禮送到心坎裡</span></h2>
  <div class="lead">一天寫一點，365 天，<br>一整年都是他自己的樣子。</div>
  {cards}
</section>
<section id="s03b"><div class="xm"><div class="sh"></div>
  <i class="sp" style="left:8%;top:14%"></i><i class="sp" style="left:88%;top:20%"></i><i class="sp" style="left:93%;top:72%"></i><i class="sp" style="left:5%;top:78%"></i><i class="sp" style="left:50%;top:6%"></i>
  <div class="en sm">CHRISTMAS DELIVERY</div><div class="big">✈ 聖誕節前到貨</div></div></section>
<section id="s04">
  <div><div class="n">365</div><div class="c">天的空白</div></div>
  <div><div class="n">12</div><div class="c">個自我覺察主題</div></div>
  <div><div class="n">4<small>色</small></div><div class="c">霧面皮革封面</div></div>
</section>
{how(1, 's05a', '時間、待辦、生活瑣事，<br>一週排在同一頁', '左頁一天一格，寫下開會時間、<br>打勾完成的事，還有今天的小事。', 'hw_week', 'pt', '寫週計畫', 'WEEKLY')}
{how(2, 's05b', '右頁方格，<br>畫進度也畫心情', '用螢光筆畫甘特圖追進度，<br>空白處畫一杯咖啡、一朵花。', 'hw_grid', 'pt', '畫方格頁', 'GRID')}
{how(3, 's06', '月計畫攤開，<br>整個月一眼看完', '精裝 180 度平攤，<br>寫到中間也不卡手。', 'hw_month', 'ls', '寫月計畫', 'MONTHLY', '整個跨頁攤平，打勾、圈起來、螢光筆都放得下')}
<section id="s06x" class="full">
  <div class="ph" data-clip="f_flat" style="background-image:url(gif/clips/f_flat/001.jpg)"></div><div class="shade"></div>
  <div class="tx"><div class="a">翻開就平攤，<br>不用一直壓著寫</div></div>
</section>
{how(4, 's06a', '每個月一個問題，<br>陪你慢慢認識自己', '跟著提問回答，<br>用三個詞形容現在的自己。', 'hw_reflect', 'pt', '每月覺察', 'MONTHLY THEME')}
{how(5, 's06b', '年計畫甘特圖，<br>螢光筆畫出一整年', '先用螢光筆畫出區間，<br>再寫上那段時間要完成的事。', 'hw_year', 'ls', '年計畫', 'YEARLY', '12 個月排在同一個跨頁，一年的節奏一眼就懂')}
{how(6, 's06c', '顯化願景板，<br>把想要的一年貼出來', '寫下願望、貼上照片，<br>每次翻開都記得為什麼出發。', 'hw_vision', 'pt', '願景板', 'VISION BOARD')}
<section id="s07" class="full">
  <div class="ph" data-clip="f_window" style="background-image:url(gif/clips/f_window/001.jpg)"></div><div class="shade"></div>
  <div class="tx"><div class="a">封面三格窗，<br>框住每天的小風景</div><div class="b">開窗封面可以換卡片，<br>也能拿起來，框住眼前的生活。</div></div>
</section>
<section id="s08" class="full">
  <div class="ph" data-clip="f_flip" style="background-image:url(gif/clips/f_flip/001.jpg)"></div><div class="shade"></div>
  <div class="tx"><div class="a">翻開這一年，<br>先寫給自己</div></div>
</section>
<section id="s09">
  <div class="eyebrow en">12 MONTHS</div>
  <h2>一年十二個提問</h2>
  <div class="lead">每個月一張照片、一個主題，跟著寫就好。</div>
  <div class="q12">{q12}</div>
</section>
<section id="s10">
  <div class="eyebrow">四種封面</div>
  <h2>四種顏色，陪他的每一天</h2>
  <div class="lead">霧面皮革，開窗款與經典素面款。</div>
  <div class="ph"></div>
  <div class="sw">
    <div><i style="background:#E9E3D6"></i>晨曦米白<small>CREAM</small></div>
    <div><i style="background:#C68E5C"></i>沙丘暖杏<small>APRICOT</small></div>
    <div><i style="background:#8FA9BE"></i>靜海霧藍<small>MIST</small></div>
    <div><i style="background:#56685A"></i>森語墨綠<small>FOREST</small></div>
  </div>
  <div class="nt">實拍色彩依螢幕顯示略有差異</div>
</section>
<section id="s11">
  <div class="ph"></div>
  <div class="stub"><div class="hd"><span class="en">MEET MYSELF HERE 2027</span><span class="en">A5 JOURNAL</span></div>
    <div class="row"><span class="k">尺寸</span><span class="v">A5（15 × 21 公分）</span></div>
    <div class="row"><span class="k">封面</span><span class="v">霧面皮革，風景開窗款／經典素面款</span></div>
    <div class="row"><span class="k">裝訂</span><span class="v">精裝，180 度平攤</span></div>
    <div class="row"><span class="k">紙張</span><span class="v">100g 模造紙，適合書寫</span></div>
    <div class="row"><span class="k">內頁</span><span class="v">年計畫、月計畫、53 週週計畫、12 個覺察主題、願景板</span></div>
  </div>
</section>
<section id="s12" class="full">
  <div class="ph" style="background-image:url(img/desk.jpg)"></div><div class="shade"></div>
  <div class="tx"><div class="a">寫字本身，<br>就是一段安靜的時間</div><div class="b">每天留十分鐘給自己，<br>一年後翻開，會遇見更懂自己的人。</div></div>
</section>
<section id="s13">
  <div class="eyebrow">聖誕加碼</div>
  <h2>送皮革燙金手帳袋</h2>
  <div class="lead">燙金 MEET MYSELF HERE，<br>手帳、筆、便利貼一起收好帶出門。</div>
  <div class="ph"></div>
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
