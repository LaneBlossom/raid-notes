"""版本 B：黑白電子像素＋Y2K。共用 home_build.py 的資料與選單結構。"""
W = '/home/claude/work/'
src = open(W + 'home_build.py', encoding='utf8').read()
ns = {}
exec(src[:src.index("CSS = r'''")], ns)
CAT, FEATURED, mega, drawer, feat, count, credits = ns['CAT'], ns['FEATURED'], ns['mega'], ns['drawer'], ns['feat'], ns['count'], ns['credits']

CSS = r'''
:root{--bg:#0a0a0a;--fg:#f2f2f2;--muted:#9a9a9a;--line:#f2f2f2;--soft:#2a2a2a;--inv-bg:#f2f2f2;--inv-fg:#0a0a0a;color-scheme:dark}
:root[data-theme="light"]{--bg:#f4f4f0;--fg:#0a0a0a;--muted:#5c5c5c;--line:#0a0a0a;--soft:#d9d9d4;--inv-bg:#0a0a0a;--inv-fg:#f4f4f0;color-scheme:light}
@media (prefers-color-scheme:light){:root:not([data-theme]){--bg:#f4f4f0;--fg:#0a0a0a;--muted:#5c5c5c;--line:#0a0a0a;--soft:#d9d9d4;--inv-bg:#0a0a0a;--inv-fg:#f4f4f0;color-scheme:light}}
*{box-sizing:border-box}
html{font-size:clamp(15px,calc(10px + .45vw),18px)}
body{margin:0;min-height:100vh;background:var(--bg);color:var(--fg);font-family:"DotGothic16","Noto Sans TC",monospace;
  background-image:radial-gradient(var(--soft) 1px,transparent 1.2px);background-size:8px 8px}
.px{font-family:"Press Start 2P","DotGothic16",monospace}
a{color:inherit}
/* menu bar */
.bar{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:3px solid var(--line)}
.bari{max-width:1240px;margin:0 auto;display:flex;align-items:stretch;gap:0;padding:0 clamp(12px,3vw,32px);height:52px;padding-right:150px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:"Press Start 2P",monospace;font-size:.72rem;padding-right:18px;margin-right:6px;border-right:3px solid var(--line)}
.logo i{width:16px;height:16px;background:var(--fg);box-shadow:4px 4px 0 var(--muted);animation:blink 1.2s steps(2) infinite}
@keyframes blink{50%{opacity:.2}}
.nav{display:flex;list-style:none;margin:0;padding:0}
.ni{display:flex}
.nb{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:8px;padding:0 16px;height:100%;border-right:3px solid var(--line)}
.nb .nzh{font-size:1rem}
.nb .nen{font-family:"Press Start 2P",monospace;font-size:.45rem;color:var(--muted)}
.car{display:none}
.nb:hover,.ni.open .nb,.nb:focus-visible{background:var(--inv-bg);color:var(--inv-fg);outline:none}
.ni.open .nb .nen,.nb:hover .nen{color:var(--inv-fg)}
/* dropdown window */
.mm{position:absolute;left:clamp(12px,3vw,32px);right:clamp(12px,3vw,32px);max-width:1180px;margin:0 auto;top:calc(100% + 6px);visibility:hidden;
  clip-path:inset(0 0 100% 0);transition:clip-path .36s steps(6),visibility 0s .36s}
.ni.open .mm{visibility:visible;clip-path:inset(-10px -10px -10px -10px);transition:clip-path .36s steps(6)}
.mmi{background:var(--bg);border:3px solid var(--line);box-shadow:8px 8px 0 var(--line)}
.mmh{display:flex;align-items:center;gap:10px;background:var(--inv-bg);color:var(--inv-fg);padding:6px 10px;font-family:"Press Start 2P",monospace;font-size:.6rem}
.mmh b{font-family:"DotGothic16",monospace;font-size:1rem;font-weight:400}
.mmh::after{content:"_ □ ✕";margin-left:auto;letter-spacing:.4em}
.hud{opacity:.8}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:0}
.col{padding:12px 14px;border-right:3px dashed var(--soft)}
.col:last-child{border-right:0}
.colh{display:flex;align-items:baseline;gap:8px;margin-bottom:8px;padding-bottom:6px;border-bottom:3px solid var(--line)}
.colh small,.dgh small{font-family:"Press Start 2P",monospace;font-size:.42rem;color:var(--muted)}
.col ul{list-style:none;margin:0;padding:0}
.col li,.dr{display:grid;grid-template-columns:52px 1fr;gap:2px 10px;align-items:center;padding:6px 6px}
.col li::before{content:"";display:none}
.col li:hover{background:var(--soft)}
.code{font-family:"Press Start 2P",monospace;font-size:.5rem;grid-row:span 2}
.nm{font-size:1rem}
.lk{display:flex;gap:6px;flex-wrap:wrap}
.lk a{font-size:.75rem;text-decoration:none;padding:0 6px;border:2px solid var(--line)}
.lk a.own{background:var(--fg);color:var(--bg)}
.lk a:hover,.lk a:focus-visible{background:var(--inv-bg);color:var(--inv-fg);outline:none}
.lk a.own:hover{background:var(--bg);color:var(--fg)}
.lk a::after{content:" ▶";font-size:.6em}
/* drawer */
.burger{all:unset;display:none;cursor:pointer;margin-left:auto;align-self:center;width:38px;height:34px;place-items:center;border:3px solid var(--line);font-family:"Press Start 2P",monospace;font-size:.6rem}
.drawer{position:fixed;inset:0 0 0 auto;width:min(88vw,380px);z-index:70;background:var(--bg);border-left:3px solid var(--line);transform:translateX(102%);transition:transform .35s steps(7);overflow:auto;padding:62px 14px 30px}
.drawer.open{transform:none}
.scrim{position:fixed;inset:0;z-index:60;background:repeating-conic-gradient(rgba(0,0,0,.5) 0 25%,transparent 0 50%) 0 0/4px 4px;opacity:0;pointer-events:none}
.scrim.open{opacity:1;pointer-events:auto}
.dc{border:3px solid var(--line);margin-bottom:10px;box-shadow:5px 5px 0 var(--line);background:var(--bg)}
.dc summary{list-style:none;padding:10px 12px;cursor:pointer;display:flex;gap:8px;align-items:baseline;background:var(--inv-bg);color:var(--inv-fg)}
.dc summary .nen{font-family:"Press Start 2P",monospace;font-size:.45rem}
.dg{padding:4px 8px 8px}.dgh{margin:6px 4px;color:var(--muted)}
@media (max-width:860px){.nav{display:none}.bar .burger{display:grid}.bari{padding-right:130px}}
/* hero */
main{max-width:1240px;margin:0 auto;padding:clamp(26px,5vw,60px) clamp(12px,3vw,32px) 40px}
.ticker{overflow:hidden;border:3px solid var(--line);background:var(--inv-bg);color:var(--inv-fg);white-space:nowrap;margin-bottom:28px}
.ticker span{display:inline-block;padding:6px 0;animation:tick 40s linear infinite;font-family:"Press Start 2P","DotGothic16",monospace;font-size:.6rem}
@keyframes tick{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.hero{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:28px;align-items:end}
@media (max-width:860px){.hero{grid-template-columns:1fr}}
.tag{font-family:"Press Start 2P",monospace;font-size:.55rem;color:var(--muted)}
.tag::before{content:"✦ "}
h1{font-family:"Press Start 2P",monospace;font-size:clamp(1.8rem,5.4vw,4rem);line-height:1.15;margin:.35em 0 .3em;text-shadow:4px 4px 0 var(--soft),8px 8px 0 var(--muted)}
h1 .cur{display:inline-block;width:.55em;height:.9em;background:var(--fg);vertical-align:-.05em;margin-left:.15em;animation:blink 1s steps(2) infinite}
.lede{font-size:1.05rem;line-height:1.9;margin:0;max-width:52ch}
.win{border:3px solid var(--line);background:var(--bg);box-shadow:8px 8px 0 var(--line)}
.win .tb{display:flex;align-items:center;background:var(--inv-bg);color:var(--inv-fg);padding:4px 8px;font-family:"Press Start 2P",monospace;font-size:.5rem}
.win .tb::after{content:"_ □ ✕";margin-left:auto;letter-spacing:.4em}
.lcd{display:grid;grid-template-columns:repeat(2,1fr);gap:0}
.lcd div{padding:12px 14px;border-right:3px solid var(--line);border-bottom:3px solid var(--line)}
.lcd div:nth-child(2n){border-right:0}.lcd div:nth-child(n+3){border-bottom:0}
.lcd b{display:block;font-family:"Press Start 2P",monospace;font-size:1.4rem;letter-spacing:.06em}
.lcd span{color:var(--muted);font-size:.85rem}
.star{position:absolute;font-size:22px;animation:tw 2.4s steps(3) infinite;pointer-events:none}
@keyframes tw{50%{opacity:.15;transform:scale(.6)}}
h2.sec{display:flex;align-items:center;gap:12px;margin:46px 0 16px;font-size:1.15rem;font-weight:400}
h2.sec::before{content:"";width:14px;height:14px;background:var(--fg)}
h2.sec small{font-family:"Press Start 2P",monospace;font-size:.45rem;color:var(--muted)}
h2.sec::after{content:"";flex:1;height:3px;background:repeating-linear-gradient(90deg,var(--fg) 0 6px,transparent 6px 10px)}
.feat{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px}
.ft{display:block;position:relative;text-decoration:none;border:3px solid var(--line);background:var(--bg);box-shadow:6px 6px 0 var(--line);transition:transform .15s steps(2),box-shadow .15s steps(2)}
.ft:hover,.ft:focus-visible{transform:translate(-3px,-3px);box-shadow:9px 9px 0 var(--line);outline:none}
.ft:active{transform:translate(3px,3px);box-shadow:3px 3px 0 var(--line)}
.ft .fk{display:flex;background:var(--inv-bg);color:var(--inv-fg);padding:4px 8px;font-family:"Press Start 2P",monospace;font-size:.45rem}
.ft .fk::after{content:"✕";margin-left:auto}
.ft .fc{position:absolute;right:10px;top:34px;font-family:"Press Start 2P",monospace;font-size:.55rem;color:var(--muted)}
.ft b{display:block;font-size:1.25rem;font-weight:400;margin:14px 14px 4px}
.ft .fv{display:inline-block;margin:0 14px;padding:0 6px;background:var(--fg);color:var(--bg);font-size:.8rem}
.ft p{margin:10px 14px 16px;color:var(--muted);font-size:.88rem;line-height:1.6}
.ft .go{position:absolute;right:12px;bottom:10px;font-family:"Press Start 2P",monospace;font-size:.6rem}
.notes{margin:0;padding:14px 18px 14px 34px;line-height:1.9;font-size:.92rem;list-style:square}
.credits{margin-top:30px;max-width:80ch;font-size:.82rem;line-height:1.8;color:var(--muted)}
footer{text-align:center;font-size:.72rem;color:var(--muted);padding:16px 0 40px;border-top:3px solid var(--line);max-width:1240px;margin:0 auto}
.rn-thm{top:10px!important;right:14px!important;z-index:80!important}
.rn-thm>button{border-radius:0!important;border:3px solid var(--line)!important;background:var(--bg)!important;font-family:"DotGothic16",monospace!important}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
'''

nav = ''.join(mega(k, z, e, g) for k, z, e, g in CAT)
names = '　✦　'.join(f'{c} {n}' for _, _, _, g in CAT for _, _, items in g for c, n, _ in items)
JS_SRC = open(W + 'home_build.py', encoding='utf8').read()
JS = JS_SRC[JS_SRC.index("JS = r'''") + 9:JS_SRC.index("'''", JS_SRC.index("JS = r'''") + 9)]
feat_b = feat.replace('<span class="go" aria-hidden="true">→</span>', '<span class="go" aria-hidden="true">OPEN ▶</span>')
html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Raid Notes · FFXIV 高難筆記</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DotGothic16&family=Press+Start+2P&family=Noto+Sans+TC:wght@400;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="bar"><div class="bari">
  <a class="logo" href="index.html" aria-label="Raid Notes 首頁"><i aria-hidden="true"></i>RAID.NOTES</a>
  <ul class="nav" aria-label="副本分類">{nav}</ul>
  <button type="button" class="burger" aria-label="開啟副本選單" aria-expanded="false" aria-controls="drawer">MENU</button>
</div></header>
<div class="scrim" aria-hidden="true"></div>
<nav class="drawer" id="drawer" aria-label="副本選單"><button type="button" class="dclose burger" style="display:grid;position:absolute;top:12px;right:12px" aria-label="關閉選單">✕</button>{drawer()}</nav>
<main>
  <div class="ticker" aria-hidden="true"><span>{names}　✦　{names}　✦　</span></div>
  <div class="hero">
    <div style="position:relative">
      <span class="star" style="right:6%;top:-6px" aria-hidden="true">✦</span>
      <span class="star" style="right:18%;top:60px;animation-delay:.8s;font-size:14px" aria-hidden="true">✧</span>
      <div class="tag">FINAL FANTASY XIV // HIGH-END DUTY NOTES</div>
      <h1>RAID<br>NOTES<span class="cur" aria-hidden="true"></span></h1>
      <p class="lede">繁中服豆芽玩家第一次挑戰高難本，邊打邊做的筆記，整理起來方便記憶。時間軸小抄可以切換職位看減傷和站位；有些副本另外附攻略整理。從上方選單挑副本。</p>
    </div>
    <div class="win"><div class="tb">SYSTEM.STATUS</div><div class="lcd">
      <div><b>12</b><span>零式</span></div><div><b>01</b><span>極神</span></div>
      <div><b>07</b><span>絕境戰</span></div><div><b>{count}</b><span>副本總數</span></div>
    </div></div>
  </div>
  <h2 class="sec">版主整理<small>FEATURED</small></h2>
  <div class="feat">{feat_b}</div>
  <h2 class="sec">使用說明<small>README.TXT</small></h2>
  <div class="win"><div class="tb">README.TXT</div>
  <ul class="notes">
    <li><b>版主筆記</b>是作者自己隊伍的減傷軸、站位和打法；<b>空白筆記</b>只有 Boss 技能時間軸和機制標籤，減傷、站位留給你自己填。</li>
    <li>版主筆記的減傷軸是照作者隊伍的組成排的，拿去用的話記得依你們的隊伍重新調整。</li>
    <li>小抄裡按「編輯減傷」就能改每個人放的技能，也能寫筆記、貼圖；改好的內容可以<b>匯出</b>成分享碼或檔案給隊友<b>匯入</b>。</li>
  </ul></div>
  {credits}
</main>
<footer>FINAL FANTASY XIV © SQUARE ENIX CO., LTD. All Rights Reserved. 個人非商業筆記。</footer>
{JS}
</body>
</html>'''
open(W + 'home_b.html', 'w', encoding='utf8').write(html)
print('ok')
