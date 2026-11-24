"""首頁三版（素材精緻版）：A 未來科技、B 黑白像素 Y2K、C 冰藍羽翼。
共用 home_build.py 的選單資料／mega menu／drawer／JS；三版互相切換（localStorage raid-notes-home）。
輸出：home.html（A）、home_b.html（B）、home_c.html（C）→ assemble.py 組成 index.html／index-b.html／index-c.html。
圖片：img/home/（素材來自版主 D:\\AI work sample，已去背／裁切／壓縮）。"""
import json
W = '/home/claude/work/'
src = open(W + 'home_build.py', encoding='utf8').read()
ns = {}
import os, shutil
if not os.path.exists(W + 'home.pre-acc.html'):  # 只用來抓「資料來源與授權」段落
    shutil.copy(W + 'home_a.html', W + 'home.pre-acc.html')
exec(src[:src.index("CSS = r'''")], ns)
CAT, FEATURED, mega, drawer, feat, count, credits = ns['CAT'], ns['FEATURED'], ns['mega'], ns['drawer'], ns['feat'], ns['count'], ns['credits']
feat = feat.replace('版主隊伍', '隊伍')
def block(s, key):
    i = s.index(key) + len(key); return s[i:s.index("'''", i)]
CSS_A = block(src, "\nCSS = r'''")
JS = block(src, "\nJS = r'''")
CSS_B = block(open(W + 'home_b_build.py', encoding='utf8').read(), "\nCSS = r'''")

IMG = 'img/home/'
PAGES = {'a': 'index.html', 'b': 'index-b.html', 'c': 'index-c.html'}
NAMES = {'a': '未來科技', 'b': '像素 Y2K', 'c': '冰藍羽翼'}
PARTY = [('MT', '槍刃', 'Gunbreaker', 'tank'), ('ST', '騎士', 'Paladin', 'tank'),
         ('H1', '占星', 'Astrologian', 'heal'), ('H2', '賢者', 'Sage', 'heal'),
         ('D1', '忍者', 'Ninja', 'dps'), ('D2', '武士', 'Samurai', 'dps'),
         ('D3', '機工', 'Machinist', 'dps'), ('D4', '繪靈', 'Pictomancer', 'dps')]
STATS = [('12', '零式', 'sv'), ('1', '極神', 'ex'), ('7', '絕境戰', 'ul'), (str(count), '副本總數', '')]
LEDE = '繁中服豆芽玩家第一次挑戰高難本，邊打邊做的筆記，整理起來方便記憶。時間軸小抄可以切換職位看減傷和站位；有些副本另外附攻略整理。從上方選單挑副本。'
NOTES = '''<li><b>版主筆記</b>是作者自己隊伍的減傷軸、站位和打法；<b>空白筆記</b>只有 Boss 技能時間軸和機制標籤，減傷、站位留給你自己填。</li>
    <li>版主筆記的減傷軸是照作者隊伍的組成排的，拿去用的話記得依你們的隊伍重新調整。</li>
    <li>小抄裡按「編輯減傷」就能改每個人放的技能，也能寫筆記、貼圖；改好的內容可以<b>匯出</b>成分享碼或檔案給隊友<b>匯入</b>。</li>'''


def redirect(cur):
    # 依右上角選的「風格」（raid-notes-skin）顯示對應首頁；標準＝A 版。?keep 可強制看目前這版
    return ('<script>(function(){var P={std:"a",future:"a",pixel:"b",crystal:"c"},F={a:"index.html",b:"index-b.html",c:"index-c.html"},k;'
            'try{k=localStorage.getItem("raid-notes-skin");if(!k)k={a:"future",b:"pixel",c:"crystal"}[localStorage.getItem("raid-notes-home")]}catch(e){}'
            f'var w=P[k];if(w&&w!=="{cur}"&&!/[?&]keep/.test(location.search))location.replace(F[w]+location.hash)}})()</script>')


def switcher(cur):
    btns = ''.join(f'<a href="{PAGES[k]}?keep" data-k="{k}"{" aria-current=\"page\"" if k == cur else ""}><b>{k.upper()}</b>{NAMES[k]}</a>' for k in PAGES)
    return (f'<nav class="sty" aria-label="首頁風格"><span>首頁風格</span>{btns}</nav>'
            '<script>document.querySelectorAll(".sty a").forEach(function(a){a.addEventListener("click",function(){try{localStorage.setItem("raid-notes-home",a.dataset.k)}catch(e){}})})</script>')


def party(cls=''):
    out = ''
    for slot, zh, en, role in PARTY:
        me = slot == 'ST'
        out += (f'<li class="pm {role}{" me" if me else ""}"><img src="{IMG}job/{en}.png" alt="" width="38" height="38" loading="lazy">'
                f'<span class="sl">{slot}</span><span class="jb">{zh}</span>{"<em>版主</em>" if me else ""}</li>')
    return f'<ul class="party {cls}" aria-label="隊伍">{out}</ul>'


SEARCH = [{'c': c, 'n': n, 'k': k, 'l': [[h, t] for h, t in links]}
          for k, _, _, g in CAT for _, _, items in g for c, n, links in items]
ROLES = [('team', '全隊', ''), ('mt', 'MT', 'tank'), ('st', 'ST', 'tank'), ('h1', 'H1', 'heal'), ('h2', 'H2', 'heal'),
         ('d1', 'D1', 'dps'), ('d2', 'D2', 'dps'), ('d3', 'D3', 'dps'), ('d4', 'D4', 'dps')]


def panel(title='快速入口', sub='QUICK START'):
    """互動面板：我的位置（小抄連結自動帶 #位置）＋副本搜尋＋重置倒數。"""
    rb = ''.join(f'<button type="button" role="radio" aria-checked="false" data-r="{r}" class="{c}">{t}</button>' for r, t, c in ROLES)
    return f'''<section class="cp" aria-label="{title}">
  <div class="cph"><b>{title}</b><small>{sub}</small></div>
  <div class="cpl">我的位置<span class="cpn">選好後，點進小抄會直接切到你的位置</span></div>
  <div class="roles" role="radiogroup" aria-label="我的位置">{rb}</div>
  <div class="cpl"><label for="q">找副本</label></div>
  <div class="srch"><input id="q" type="search" autocomplete="off" placeholder="M8S、絕亞、TEA…" aria-controls="res" aria-describedby="qh"><span id="qh" class="cpn">按 Enter 開第一個結果</span></div>
  <ul class="res" id="res" aria-live="polite"></ul>
  <div class="rst">
    <div><span>每日重置<small>每天 23:00</small></span><b data-cd="d">--:--:--</b></div>
    <div><span>每週重置<small>週二 16:00</small></span><b data-cd="w">--</b></div>
  </div>
</section>'''


PANEL_JS = '<script>{const D=' + json.dumps(SEARCH, ensure_ascii=False) + r''';
const K="raid-notes-role",ok=r=>/^(team|mt|st|h[12]|d[1-4])$/.test(r);
let role="team";try{const s=localStorage.getItem(K);if(ok(s))role=s}catch(e){}
const sheet=h=>/^[a-z0-9-]+\.html$/.test(h)&&!/^index/.test(h)&&!/-guide\.html$/.test(h);
const withRole=h=>{const b=h.split("#")[0];return sheet(b)&&role!=="team"?b+"#"+role:b};
function apply(){
  document.querySelectorAll(".roles button").forEach(b=>{const on=b.dataset.r===role;b.setAttribute("aria-checked",on);b.tabIndex=on?0:-1});
  document.querySelectorAll("a[href]").forEach(a=>{const h=a.getAttribute("href");if(sheet(h.split("#")[0]))a.setAttribute("href",withRole(h))});
}
document.querySelectorAll(".roles button").forEach((b,i,all)=>{
  b.addEventListener("click",()=>{role=b.dataset.r;try{localStorage.setItem(K,role)}catch(e){}apply();render()});
  b.addEventListener("keydown",e=>{const d={ArrowRight:1,ArrowDown:1,ArrowLeft:-1,ArrowUp:-1}[e.key];if(!d)return;e.preventDefault();const n=all[(i+d+all.length)%all.length];n.focus();n.click()});
});
const q=document.getElementById("q"),res=document.getElementById("res");
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let hits=[];
function render(){
  const v=q.value.trim().toLowerCase();
  hits=v?D.filter(x=>(x.c+" "+x.n).toLowerCase().includes(v)).slice(0,6):[];
  res.innerHTML=v&&!hits.length?'<li class="none">找不到這個副本</li>':hits.map(x=>'<li class="'+x.k+'"><span class="rc">'+esc(x.c)+'</span><span class="rn">'+esc(x.n)+'</span><span class="rl">'+x.l.map(l=>'<a href="'+esc(withRole(l[0]))+'">'+esc(l[1])+'</a>').join("")+'</span></li>').join("");
}
q.addEventListener("input",render);
q.addEventListener("keydown",e=>{if(e.key==="Enter"&&hits[0]){location.href=withRole(hits[0].l[0][0])}else if(e.key==="Escape"){q.value="";render()}});
const pad=n=>String(n).padStart(2,"0");
function next(dow){const n=new Date(),t=new Date(n);if(dow==null){t.setUTCHours(15,0,0,0);if(t<=n)t.setUTCDate(t.getUTCDate()+1)}else{t.setUTCHours(8,0,0,0);let a=(dow-t.getUTCDay()+7)%7;t.setUTCDate(t.getUTCDate()+a);if(t<=n)t.setUTCDate(t.getUTCDate()+7)}return t-n}
const cd=document.querySelectorAll("[data-cd]");
function tick(){cd.forEach(el=>{const ms=next(el.dataset.cd==="w"?2:null),s=Math.floor(ms/1000),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);
  el.textContent=el.dataset.cd==="w"?(d?d+" 天 ":"")+pad(h)+":"+pad(m):pad(h)+":"+pad(m)+":"+pad(s%60)})}
tick();setInterval(tick,1000);apply();
}</script>'''

# 面板共用版面（各版再覆寫外觀）
CP_BASE = r'''
.cp{position:relative;display:grid;gap:10px;padding:18px}
.cph{display:flex;align-items:baseline;gap:10px;margin-bottom:2px}
.cph b{font-size:1.05rem}.cph small{font-size:.62rem;letter-spacing:.2em;opacity:.7}
.cpl{font-size:.82rem;font-weight:700;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}
.cpn{font-size:.72rem;font-weight:400;opacity:.7}
.roles{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:5px}
.roles button{all:unset;box-sizing:border-box;cursor:pointer;text-align:center;padding:9px 0;min-height:40px;font-size:.78rem;font-weight:700;display:grid;place-items:center}
.roles button:focus-visible{outline:2px solid currentColor;outline-offset:2px}
@media (max-width:520px){.roles{grid-template-columns:repeat(5,minmax(0,1fr))}.roles button:first-child{grid-column:span 1}}
.srch{display:grid;gap:4px}
.srch input{font:inherit;font-size:16px;width:100%;padding:10px 12px;min-height:44px;color:inherit;background:transparent}
.srch input:focus{outline:none}
.res{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.res:empty{display:none}
.res li{display:grid;grid-template-columns:52px minmax(0,1fr);gap:2px 10px;align-items:center;padding:7px 10px}
.res .rc{grid-row:span 2;font-size:.74rem;font-weight:800}
.res .rn{font-weight:700}
.res .rl{display:flex;gap:6px;flex-wrap:wrap}
.res .rl a{font-size:.74rem;text-decoration:none;padding:2px 9px}
.res .none{display:block;font-size:.82rem;opacity:.75}
.rst{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}
.rst div{display:flex;flex-direction:column;gap:2px;padding:10px 12px}
.rst span{font-size:.74rem;display:flex;gap:6px;align-items:baseline}.rst small{opacity:.65;font-size:.66rem}
.rst b{font-variant-numeric:tabular-nums;font-size:1.25rem;white-space:nowrap}
'''


def head(title_font_css, css, cur):
    return f'''<!doctype html>
<html lang="zh-Hant" data-home="{cur}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Raid Notes · FFXIV 高難筆記</title>
{redirect(cur)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{title_font_css}">
{'<link rel="preload" as="image" href="'+IMG+'banner.webp">' if cur == 'c' else ''}
<style>{css}</style>
</head>'''


def bar(logo, burger):
    nav = ''.join(mega(k, z, e, g) for k, z, e, g in CAT)
    return f'''<header class="bar"><div class="bari">
  <a class="logo" href="index.html" aria-label="Raid Notes 首頁">{logo}</a>
  <ul class="nav" aria-label="副本分類">{nav}</ul>
  <button type="button" class="burger" aria-label="開啟副本選單" aria-expanded="false" aria-controls="drawer">{burger}</button>
</div></header>
<div class="scrim" aria-hidden="true"></div>
<nav class="drawer" id="drawer" aria-label="副本選單"><button type="button" class="dclose burger" style="display:grid;position:absolute;top:14px;right:14px" aria-label="關閉選單">✕</button>{drawer()}</nav>'''


FOOT = '<footer>FINAL FANTASY XIV © SQUARE ENIX CO., LTD. All Rights Reserved. 個人非商業筆記。角色插圖為版主原創素材。</footer>'

# 共用：風格切換鈕＋隊伍（各版再覆寫外觀）
STY_BASE = r'''
.sty{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:55;display:flex;align-items:center;gap:4px;padding:5px;font:12px/1.2 "Noto Sans TC",system-ui,sans-serif}
.sty span{padding:0 8px;opacity:.75}
.sty a{display:flex;gap:5px;align-items:center;text-decoration:none;padding:6px 10px;color:inherit;white-space:nowrap}
.sty a b{font-weight:800}
@media (max-width:520px){.sty span{display:none}.sty a{padding:6px 8px}}
main{padding-bottom:90px!important}
main{overflow-x:clip}
.party{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:12px}
.pm{position:relative;display:grid;grid-template-columns:38px 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center;padding:10px 12px}
.pm img{grid-row:span 2;width:38px;height:38px}
.pm .sl{font-size:.7rem;letter-spacing:.12em;opacity:.75}
.pm .jb{font-weight:700}
.pm em{position:absolute;top:-9px;right:8px;font-style:normal;font-size:.68rem;font-weight:700;padding:1px 7px}
.stk{position:absolute;pointer-events:none;user-select:none}
'''

# ---------------------------------------------------------------- A 未來科技
CSS_A2 = CSS_A + STY_BASE + CP_BASE + r'''
:root{--tank:#5aa8ff;--heal:#3ee89a;--dps:#ff5e7a}
.hero{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.9fr);gap:clamp(20px,4vw,60px);align-items:center}
@media (max-width:860px){.hero{grid-template-columns:1fr}}
.pfw{position:relative;justify-self:end;width:min(100%,460px)}
.cp{border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(14px);clip-path:polygon(0 0,calc(100% - 22px) 0,100% 22px,100% 100%,22px 100%,0 calc(100% - 22px));box-shadow:inset 0 0 40px rgba(94,231,255,.08)}
.cp::before{content:"";position:absolute;left:0;top:0;width:44px;height:2px;background:var(--cy);box-shadow:0 0 10px var(--cy)}
.cph b{font-family:Orbitron,"Noto Sans TC",sans-serif;letter-spacing:.08em}.cph small{font-family:Orbitron,sans-serif;color:var(--cy)}
.roles button{border:1px solid var(--line);color:var(--fg);font-family:Orbitron,"Noto Sans TC",sans-serif;transition:all .2s}
.roles .tank{--r:var(--tank)}.roles .heal{--r:var(--heal)}.roles .dps{--r:var(--dps)}.roles button:first-child{--r:var(--cy)}
.roles button:hover{border-color:var(--r);color:var(--r)}
.roles button[aria-checked=true]{background:var(--r);border-color:var(--r);color:#05070d;box-shadow:0 0 14px color-mix(in srgb,var(--r) 60%,transparent)}
.srch input{border:1px solid var(--line);background:color-mix(in srgb,var(--bg) 60%,transparent)}
.srch input:focus{border-color:var(--cy);box-shadow:0 0 0 3px color-mix(in srgb,var(--cy) 25%,transparent)}
.res li{border:1px solid var(--line);background:color-mix(in srgb,var(--bg) 50%,transparent)}
.res .savage{--c:var(--sv)}.res .ex{--c:var(--ex)}.res .ult{--c:var(--ul)}
.res .rc{font-family:Orbitron,sans-serif;color:var(--c)}
.res .rl a{border:1px solid color-mix(in srgb,var(--c) 50%,transparent);color:var(--fg)}
.res .rl a:hover,.res .rl a:focus-visible{background:var(--c);color:#05070d;outline:none}
.rst div{border:1px solid var(--line);background:color-mix(in srgb,var(--bg) 50%,transparent)}
.rst b{font-family:Orbitron,sans-serif;color:var(--cy);text-shadow:0 0 12px color-mix(in srgb,var(--cy) 50%,transparent)}
@media (max-width:860px){.pfw{justify-self:stretch;width:100%;margin-top:10px}.stk.neon{display:none}}
.stk.neon{filter:drop-shadow(0 0 10px rgba(255,79,216,.6));animation:float 6s ease-in-out infinite}
.sec .ico{width:22px;height:auto;filter:drop-shadow(0 0 6px var(--cy))}
.party .pm{border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(8px);clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,0 100%);transition:transform .25s,border-color .25s}
.party .pm::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--r);box-shadow:0 0 10px var(--r)}
.party .tank{--r:var(--tank)}.party .heal{--r:var(--heal)}.party .dps{--r:var(--dps)}
.party .pm:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--r) 60%,transparent)}
.party .sl{font-family:Orbitron,sans-serif;color:var(--r)}
.party .me{border-color:color-mix(in srgb,var(--cy) 70%,transparent);box-shadow:inset 0 0 22px rgba(94,231,255,.15);clip-path:none}
.party .me em{background:var(--cy);color:#05070d;box-shadow:0 0 10px var(--cy)}
.sty{border:1px solid var(--line);background:color-mix(in srgb,var(--bg2) 85%,transparent);backdrop-filter:blur(12px);border-radius:999px;color:var(--fg)}
.sty a{border-radius:999px}.sty a b{font-family:Orbitron,sans-serif;color:var(--cy)}
.sty a:hover{background:color-mix(in srgb,var(--cy) 14%,transparent)}
.sty a[aria-current]{background:var(--cy);color:#05070d}.sty a[aria-current] b{color:#05070d}
'''

def page_a():
    neon = [('neon1', 'left:-46px;top:-40px;width:92px;animation-delay:-2s'), ('neon3', 'right:-34px;top:38%;width:72px;animation-delay:-4s'),
            ('neon2', 'left:-30px;bottom:-30px;width:64px')]
    stk = ''.join(f'<img class="stk neon" src="{IMG}{n}.webp" alt="" aria-hidden="true" style="{s}">' for n, s in neon)
    stats = ''.join(f'<div class="stat {c}"><b>{n}</b><span>{t}</span></div>' for n, t, c in STATS)
    return head('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap', CSS_A2, 'a') + f'''
<body>
{bar('<i aria-hidden="true"></i>RAID NOTES', '<span></span>')}
<main>
  <div class="hero">
    <div>
      <div class="tag">FINAL FANTASY XIV · HIGH-END DUTY NOTES</div>
      <h1>RAID NOTES</h1>
      <p class="lede">{LEDE}</p>
      <div class="stats">{stats}</div>
    </div>
    <div class="pfw">{stk}{panel()}</div>
  </div>
  <h2 class="sec">版主整理<small>FEATURED</small></h2>
  <div class="feat">{feat}</div>
  <h2 class="sec">使用說明<small>HOW TO USE</small></h2>
  <ul class="notes">
    {NOTES}
  </ul>
  {credits}
</main>
{FOOT}
{JS}
{PANEL_JS}
</body>
</html>'''

# ---------------------------------------------------------------- B 黑白像素 Y2K
CSS_B2 = CSS_B + STY_BASE + CP_BASE + r'''
:root{--inv:1}:root[data-theme="light"]{--inv:0}
@media (prefers-color-scheme:light){:root:not([data-theme]){--inv:0}}
.hero{grid-template-columns:minmax(0,1.25fr) minmax(0,.85fr);align-items:center}
@media (max-width:860px){.hero{grid-template-columns:1fr}.stk.y2k{display:none}}
.pfw{position:relative;justify-self:end;width:min(100%,460px)}
.pfw .win{margin:0}
.cp{padding:14px 16px 16px}
.cph{display:none}
.cpl{font-family:"DotGothic16",monospace;font-weight:400}
.roles button{border:3px solid var(--line);font-family:"Press Start 2P",monospace;font-size:.55rem;font-weight:400;background:var(--bg);color:var(--fg)}
.roles button:first-child{font-family:"DotGothic16",monospace;font-size:.8rem}
.roles button:hover{background:var(--soft)}
.roles button[aria-checked=true]{background:var(--inv-bg);color:var(--inv-fg)}
.srch input{border:3px solid var(--line);font-family:"DotGothic16",monospace;background:var(--bg)}
.srch input:focus{box-shadow:4px 4px 0 var(--line)}
.res li{border:3px solid var(--line);background:var(--bg)}
.res .rc{font-family:"Press Start 2P",monospace;font-size:.5rem;font-weight:400}
.res .rn{font-weight:400}
.res .rl a{border:2px solid var(--line);color:var(--fg)}
.res .rl a:hover,.res .rl a:focus-visible{background:var(--inv-bg);color:var(--inv-fg);outline:none}
.rst div{border:3px solid var(--line);background:var(--inv-bg);color:var(--inv-fg)}
.rst b{font-family:"Press Start 2P",monospace;font-size:.9rem;font-weight:400;line-height:1.6}
@media (max-width:860px){.pfw{justify-self:stretch;width:100%;margin-top:6px}.stk.px{display:none}}
.stk.px{width:44px;filter:invert(var(--inv));animation:tw 2.4s steps(3) infinite;image-rendering:pixelated}
.stk.y2k{filter:invert(var(--inv));opacity:.9}
.lcd2{margin-top:22px;max-width:440px}
.lcd2 .lcd{grid-template-columns:repeat(4,1fr)}
.lcd2 .lcd div{border-bottom:0;border-right:3px solid var(--line);padding:10px 12px}.lcd2 .lcd div:last-child{border-right:0}
.lcd2 .lcd b{font-size:1.05rem}
@media (max-width:520px){.lcd2 .lcd{grid-template-columns:repeat(2,1fr)}.lcd2 .lcd div:nth-child(2){border-right:0}.lcd2 .lcd div:nth-child(-n+2){border-bottom:3px solid var(--line)}}
h2.sec img{width:22px;filter:invert(var(--inv))}
.party .pm{border:3px solid var(--line);background:var(--bg);box-shadow:5px 5px 0 var(--line)}
.party .pm img{filter:grayscale(1) contrast(1.25);image-rendering:pixelated}
.party .sl{font-family:"Press Start 2P",monospace;font-size:.5rem;color:var(--muted)}
.party .jb{font-weight:400;font-size:1.05rem}
.party .me{background:var(--inv-bg);color:var(--inv-fg)}.party .me .sl{color:var(--inv-fg)}
.party .me img{filter:none}
.party .me em{background:var(--bg);color:var(--fg);border:3px solid var(--line);font-family:"DotGothic16",monospace;font-weight:400}
.sty{border:3px solid var(--line);background:var(--bg);box-shadow:5px 5px 0 var(--line);font-family:"DotGothic16",monospace;color:var(--fg)}
.sty a b{font-family:"Press Start 2P",monospace;font-size:.6rem;font-weight:400}
.sty a:hover{background:var(--soft)}
.sty a[aria-current]{background:var(--inv-bg);color:var(--inv-fg)}
'''

def page_b():
    names = '　✦　'.join(f'{c} {n}' for _, _, _, g in CAT for _, _, items in g for c, n, _ in items)
    feat_b = feat.replace('<span class="go" aria-hidden="true">→</span>', '<span class="go" aria-hidden="true">OPEN ▶</span>')
    px = [('pix3', 'left:-30px;top:-34px'), ('pix1', 'right:-26px;top:34%;animation-delay:.6s'),
          ('pix0', 'right:-22px;bottom:-26px;animation-delay:1.8s')]
    stk = ''.join(f'<img class="stk px" src="{IMG}{n}.webp" alt="" aria-hidden="true" style="{s}">' for n, s in px)
    lcd = ''.join(f'<div><b>{n.zfill(2)}</b><span>{t}</span></div>' for n, t, _ in STATS)
    return head('https://fonts.googleapis.com/css2?family=DotGothic16&family=Press+Start+2P&family=Noto+Sans+TC:wght@400;700&display=swap', CSS_B2, 'b') + f'''
<body>
{bar('<i aria-hidden="true"></i>RAID.NOTES', 'MENU')}
<main>
  <div class="ticker" aria-hidden="true"><span>{names}　✦　{names}　✦　</span></div>
  <div class="hero">
    <div style="position:relative">
      <img class="stk y2k" src="{IMG}y2k9.webp" alt="" aria-hidden="true" style="right:4%;top:-10px;width:46px">
      <img class="stk y2k" src="{IMG}y2k10.webp" alt="" aria-hidden="true" style="right:16%;top:70px;width:60px">
      <div class="tag">FINAL FANTASY XIV // HIGH-END DUTY NOTES</div>
      <h1>RAID<br>NOTES<span class="cur" aria-hidden="true"></span></h1>
      <p class="lede">{LEDE}</p>
      <div class="win lcd2"><div class="tb">SYSTEM.STATUS</div><div class="lcd">{lcd}</div></div>
    </div>
    <div class="pfw">{stk}<div class="win"><div class="tb">QUICK.START</div>{panel('快速入口', 'PRESS START')}</div></div>
  </div>
  <h2 class="sec">版主整理<small>FEATURED</small></h2>
  <div class="feat">{feat_b}</div>
  <h2 class="sec">使用說明<small>README.TXT</small></h2>
  <div class="win"><div class="tb">README.TXT</div>
  <ul class="notes">
    {NOTES}
  </ul></div>
  {credits}
</main>
{FOOT}
{JS}
{PANEL_JS}
</body>
</html>'''

# ---------------------------------------------------------------- C 冰藍羽翼
CSS_C = STY_BASE + CP_BASE + r'''
:root{--bg:#f3f2ff;--bg2:#e9e8ff;--panel:rgba(255,255,255,.72);--line:rgba(111,120,220,.22);--fg:#25224a;--muted:#6a6796;
  --ice:#5b7cff;--lav:#9b7cf5;--pink:#ec8fc6;--sv:#e2559a;--ex:#14a89a;--ul:#7c5cf0;--tank:#4f7dff;--heal:#22b07a;--dps:#e0527a;
  --shadow:0 18px 40px rgba(80,80,170,.16);--glass:blur(14px) saturate(1.4);color-scheme:light}
:root[data-theme="dark"]{--bg:#0d0f2e;--bg2:#151842;--panel:rgba(28,32,80,.62);--line:rgba(160,170,255,.2);--fg:#ecebff;--muted:#a3a6d6;
  --ice:#8ea6ff;--lav:#b9a3ff;--pink:#f5a8d6;--sv:#f07ab2;--ex:#45d6c4;--ul:#a88bff;--tank:#7fa3ff;--heal:#5ad7a0;--dps:#f07f9d;--shadow:0 18px 44px rgba(0,0,0,.4);color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme]){--bg:#0d0f2e;--bg2:#151842;--panel:rgba(28,32,80,.62);--line:rgba(160,170,255,.2);--fg:#ecebff;--muted:#a3a6d6;
  --ice:#8ea6ff;--lav:#b9a3ff;--pink:#f5a8d6;--sv:#f07ab2;--ex:#45d6c4;--ul:#a88bff;--tank:#7fa3ff;--heal:#5ad7a0;--dps:#f07f9d;--shadow:0 18px 44px rgba(0,0,0,.4);color-scheme:dark}}
*{box-sizing:border-box}
html{font-size:clamp(15px,calc(10px + .45vw),18px)}
body{margin:0;min-height:100vh;color:var(--fg);font-family:"Noto Sans TC",system-ui,sans-serif;
  background:radial-gradient(900px 600px at 90% 10%,color-mix(in srgb,var(--lav) 18%,transparent),transparent 60%),radial-gradient(800px 600px at 0% 70%,color-mix(in srgb,var(--ice) 14%,transparent),transparent 60%),var(--bg);background-attachment:fixed}
a{color:inherit}
.serif{font-family:"Cinzel","Noto Serif TC",serif}
/* bar */
.bar{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 72%,transparent);backdrop-filter:var(--glass);border-bottom:1px solid var(--line)}
.bari{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:18px;padding:0 clamp(14px,3vw,36px);height:64px;padding-right:150px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:Cinzel,serif;font-weight:700;letter-spacing:.14em;font-size:1.05rem}
.logo img{width:26px;height:26px;animation:spin 14s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.nav{display:flex;gap:2px;list-style:none;margin:0;padding:0;height:100%}
.ni{display:flex;align-items:center;height:100%}
.ni[data-cat="savage"]{--c:var(--sv)}.ni[data-cat="ex"]{--c:var(--ex)}.ni[data-cat="ult"]{--c:var(--ul)}
.nb{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;transition:background .2s}
.nb .nzh{font-weight:700}
.nb .nen{font-family:Cinzel,serif;font-size:.62rem;letter-spacing:.16em;color:var(--muted)}
.car{width:6px;height:6px;border-right:1.5px solid var(--muted);border-bottom:1.5px solid var(--muted);transform:rotate(45deg) translateY(-2px);transition:transform .25s}
.nb:hover,.ni.open .nb,.nb:focus-visible{background:color-mix(in srgb,var(--c) 14%,transparent);outline:none}
.ni.open .car{transform:rotate(225deg)}
.mm{position:absolute;left:0;right:0;top:calc(100% + 8px);padding:0 clamp(14px,3vw,36px);visibility:hidden;opacity:0;transform:translateY(-8px) scale(.99);transition:opacity .25s,transform .35s cubic-bezier(.2,.8,.2,1),visibility 0s .35s}
.ni.open .mm{visibility:visible;opacity:1;transform:none;transition:opacity .25s,transform .35s cubic-bezier(.2,.8,.2,1)}
.mmi{max-width:1180px;margin:0 auto;padding:20px 22px 22px;background:color-mix(in srgb,var(--bg) 97%,transparent);backdrop-filter:var(--glass);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.mmi::before{content:"";position:absolute;inset:0 0 auto;height:3px;background:linear-gradient(90deg,var(--ice),var(--c),var(--pink))}
.mmh{display:flex;align-items:baseline;gap:12px;margin-bottom:12px}
.mmh b{font-size:1.35rem;color:var(--c);font-family:"Noto Serif TC",serif}
.hud{font-family:Cinzel,serif;font-size:.68rem;letter-spacing:.24em;color:var(--muted)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.colh{display:flex;align-items:baseline;gap:8px;padding-bottom:6px;margin-bottom:6px;border-bottom:1px solid var(--line)}
.colh small,.dgh small{font-family:Cinzel,serif;font-size:.6rem;letter-spacing:.16em;color:var(--muted)}
.col ul{list-style:none;margin:0;padding:0}
.col li,.dr{display:grid;grid-template-columns:54px 1fr;gap:2px 10px;align-items:center;padding:7px 8px;border-radius:12px;transition:background .2s}
.col li:hover{background:color-mix(in srgb,var(--c) 9%,transparent)}
.code{font-family:Cinzel,serif;font-size:.74rem;font-weight:700;color:var(--c,var(--ice));grid-row:span 2}
.nm{font-weight:700}
.lk{display:flex;gap:6px;flex-wrap:wrap}
.lk a{font-size:.75rem;text-decoration:none;padding:1px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted);transition:all .2s}
.lk a.own{border-color:color-mix(in srgb,var(--c,var(--ice)) 50%,transparent);color:var(--fg);background:color-mix(in srgb,var(--c,var(--ice)) 8%,transparent)}
.lk a:hover,.lk a:focus-visible{background:var(--c,var(--ice));color:#fff;border-color:transparent;outline:none}
.burger{all:unset;display:none;cursor:pointer;margin-left:auto;width:40px;height:40px;place-items:center;border:1px solid var(--line);border-radius:50%;background:var(--panel)}
.burger span{display:block;width:16px;height:2px;border-radius:2px;background:var(--fg);box-shadow:0 5px 0 var(--fg),0 -5px 0 var(--fg)}
.drawer{position:fixed;inset:0 0 0 auto;width:min(88vw,380px);z-index:70;background:var(--bg);border-left:1px solid var(--line);transform:translateX(102%);transition:transform .4s cubic-bezier(.2,.8,.2,1);overflow:auto;padding:70px 16px 30px}
.drawer.open{transform:none;box-shadow:var(--shadow)}
.scrim{position:fixed;inset:0;z-index:60;background:rgba(30,30,80,.35);backdrop-filter:blur(2px);opacity:0;pointer-events:none;transition:opacity .3s}
.scrim.open{opacity:1;pointer-events:auto}
.dc{border:1px solid var(--line);border-radius:16px;margin-bottom:10px;background:var(--panel)}
.dc.savage{--c:var(--sv)}.dc.ex{--c:var(--ex)}.dc.ult{--c:var(--ul)}
.dc summary{list-style:none;padding:12px 14px;cursor:pointer;display:flex;gap:8px;align-items:baseline}
.dc summary .nzh{font-weight:800;color:var(--c)}.dc summary .nen{font-family:Cinzel,serif;font-size:.62rem;letter-spacing:.16em;color:var(--muted)}
.dg{padding:0 10px 10px}.dgh{font-size:.8rem;font-weight:700;color:var(--muted);margin:6px 4px}
@media (max-width:860px){.nav{display:none}.bar .burger{display:grid}.bari{padding-right:130px}}
/* hero */
.hero{position:relative;height:clamp(360px,44vw,600px);overflow:hidden;isolation:isolate}
.hero>img.bn{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:72% 40%;z-index:-2;animation:drift 24s ease-in-out infinite alternate}
@keyframes drift{to{transform:scale(1.06) translateX(-1.5%)}}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,color-mix(in srgb,var(--bg) 88%,transparent) 0%,color-mix(in srgb,var(--bg) 55%,transparent) 38%,transparent 62%),linear-gradient(0deg,var(--bg) 0%,transparent 22%)}
.hi{max-width:1240px;height:100%;margin:0 auto;padding:0 clamp(14px,3vw,36px);display:flex;flex-direction:column;justify-content:center}
.hi>div{max-width:560px}
.tag{font-family:Cinzel,serif;font-size:.72rem;letter-spacing:.3em;color:var(--ice);display:flex;align-items:center;gap:10px}
.tag img{width:18px}
h1{font-family:Cinzel,serif;font-weight:700;font-size:clamp(2.8rem,7vw,5.4rem);letter-spacing:.04em;margin:.12em 0 .18em;line-height:1;
  background:linear-gradient(100deg,var(--ice) 0%,var(--lav) 55%,var(--pink) 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 4px 18px color-mix(in srgb,var(--lav) 35%,transparent))}
.lede{color:var(--fg);opacity:.86;font-size:1rem;line-height:1.9;margin:0}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}
.stat{display:flex;align-items:baseline;gap:6px;padding:6px 14px;border-radius:999px;background:var(--panel);backdrop-filter:var(--glass);border:1px solid var(--line)}
.stat b{font-family:Cinzel,serif;font-size:1.1rem;color:var(--ice)}.stat span{font-size:.78rem;color:var(--muted)}
.stat.sv b{color:var(--sv)}.stat.ex b{color:var(--ex)}.stat.ul b{color:var(--ul)}
.petal{position:absolute;top:-8%;width:var(--w,26px);z-index:0;opacity:.85;animation:fall var(--d,14s) linear infinite;animation-delay:var(--dl,0s);pointer-events:none}
@keyframes fall{0%{transform:translate(0,0) rotate(0)}100%{transform:translate(-120px,110vh) rotate(320deg)}}
@media (max-width:700px){.hero{height:auto}.hero>img.bn{position:relative;height:230px;object-position:80% 40%;display:block}
  .hero::before{background:linear-gradient(0deg,var(--bg) 0%,transparent 40%);height:230px;inset:0 0 auto}.hi{padding-top:0;margin-top:-30px}}
main{position:relative;max-width:1240px;margin:0 auto;padding:10px clamp(14px,3vw,36px) 50px}
h2.sec{display:flex;align-items:center;gap:10px;margin:48px 0 16px;font-size:1.22rem;font-family:"Noto Serif TC",serif}
h2.sec img{width:22px}
h2.sec small{font-family:Cinzel,serif;font-size:.64rem;letter-spacing:.26em;color:var(--muted)}
h2.sec::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent)}
/* 版主卡 */
.cpw{position:relative;margin-top:-70px;z-index:2}
@media (max-width:700px){.cpw{margin-top:18px}}
.cpw .fl1{right:-14px;top:-26px;width:58px;transform:rotate(18deg)}
.cpw .fl2{left:-16px;bottom:-18px;width:46px}
.cp{border-radius:26px;background:color-mix(in srgb,var(--bg) 78%,transparent);backdrop-filter:var(--glass);border:1px solid var(--line);box-shadow:var(--shadow);padding:22px 24px;
  grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);column-gap:28px}
.cp>*{grid-column:1}
.cph{grid-column:1/-1}
.cph b{font-family:"Noto Serif TC",serif;font-size:1.15rem}.cph small{font-family:Cinzel,serif;color:var(--muted)}
.rst{grid-column:2;grid-row:2/span 5;grid-template-columns:1fr;align-content:start;margin:0}
@media (max-width:760px){.cp{grid-template-columns:1fr}.rst{grid-column:1;grid-row:auto;grid-template-columns:1fr 1fr}}
.roles button{border-radius:12px;background:var(--panel);border:1px solid var(--line);color:var(--fg);transition:all .2s}
.roles .tank{--r:var(--tank)}.roles .heal{--r:var(--heal)}.roles .dps{--r:var(--dps)}.roles button:first-child{--r:var(--lav)}
.roles button:hover{border-color:var(--r);color:var(--r)}
.roles button[aria-checked=true]{background:var(--r);border-color:transparent;color:#fff;box-shadow:0 6px 16px color-mix(in srgb,var(--r) 35%,transparent)}
.srch input{border-radius:14px;border:1px solid var(--line);background:var(--panel)}
.srch input:focus{border-color:var(--ice);box-shadow:0 0 0 4px color-mix(in srgb,var(--ice) 18%,transparent)}
.res li{border-radius:14px;border:1px solid var(--line);background:var(--panel)}
.res .savage{--c:var(--sv)}.res .ex{--c:var(--ex)}.res .ult{--c:var(--ul)}
.res .rc{font-family:Cinzel,serif;color:var(--c)}
.res .rl a{border-radius:999px;border:1px solid color-mix(in srgb,var(--c) 45%,transparent);color:var(--fg)}
.res .rl a:hover,.res .rl a:focus-visible{background:var(--c);color:#fff;outline:none}
.rst div{border-radius:18px;background:linear-gradient(135deg,color-mix(in srgb,var(--ice) 14%,var(--panel)),color-mix(in srgb,var(--lav) 12%,var(--panel)));border:1px solid var(--line)}
.rst b{font-family:Cinzel,serif;font-size:1.6rem;background:linear-gradient(100deg,var(--ice),var(--lav));-webkit-background-clip:text;background-clip:text;color:transparent}
.party .pm{border-radius:18px;background:var(--panel);backdrop-filter:var(--glass);border:1px solid var(--line);transition:transform .25s,box-shadow .25s}
.party .pm:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.party .pm img{border-radius:50%;padding:3px;background:radial-gradient(circle,color-mix(in srgb,var(--r) 25%,transparent),transparent 70%)}
.party .tank{--r:var(--tank)}.party .heal{--r:var(--heal)}.party .dps{--r:var(--dps)}
.party .sl{font-family:Cinzel,serif;font-weight:700;color:var(--r)}
.party .me{border-color:color-mix(in srgb,var(--ice) 55%,transparent);background:linear-gradient(135deg,color-mix(in srgb,var(--ice) 16%,var(--panel)),var(--panel))}
.party .me em{border-radius:999px;background:linear-gradient(90deg,var(--ice),var(--lav));color:#fff}
/* featured */
.feat{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.ft{position:relative;display:block;text-decoration:none;padding:18px 18px 22px;border-radius:22px;background:var(--panel);backdrop-filter:var(--glass);border:1px solid var(--line);overflow:hidden;transition:transform .3s,box-shadow .3s}
.ft.savage{--c:var(--sv)}.ft.ex{--c:var(--ex)}.ft.ult{--c:var(--ul)}
.ft::before{content:"";position:absolute;right:-40px;top:-40px;width:130px;height:130px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--c) 30%,transparent),transparent 70%);transition:transform .5s}
.ft:hover,.ft:focus-visible{transform:translateY(-4px);box-shadow:var(--shadow);outline:none}
.ft:hover::before{transform:scale(1.6)}
.fk{font-family:Cinzel,serif;font-size:.62rem;letter-spacing:.22em;color:var(--c)}
.fc{float:right;font-family:Cinzel,serif;font-weight:700;font-size:.8rem;color:var(--muted)}
.ft b{display:block;font-size:1.25rem;margin:8px 0 4px;font-family:"Noto Serif TC",serif}
.fv{display:inline-block;font-size:.74rem;font-weight:700;padding:1px 10px;border-radius:999px;background:color-mix(in srgb,var(--c) 16%,transparent);color:var(--c)}
.ft p{margin:10px 0 0;color:var(--muted);font-size:.86rem;line-height:1.65}
.go{position:absolute;right:16px;bottom:12px;color:var(--c);transition:transform .3s}
.ft:hover .go{transform:translateX(4px)}
.notes-w{position:relative}
.notes{margin:0;padding:18px 22px 18px 38px;border-radius:22px;background:var(--panel);backdrop-filter:var(--glass);border:1px solid var(--line);color:var(--muted);line-height:1.9;font-size:.92rem}
.notes b{color:var(--fg)}
.notes-w .peek{position:absolute;right:10px;top:-74px;width:96px}
@media (max-width:600px){.notes-w .peek{display:none}}
.credits{margin-top:34px;max-width:80ch;font-size:.8rem;line-height:1.7;color:var(--muted)}
footer{text-align:center;font-size:.72rem;color:var(--muted);padding:20px 14px 40px}
.rn-thm{top:14px!important;right:16px!important;z-index:80!important}
.sty{border:1px solid var(--line);background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:var(--glass);border-radius:999px;box-shadow:var(--shadow)}
.sty a{border-radius:999px}.sty a b{font-family:Cinzel,serif;color:var(--lav)}
.sty a:hover{background:color-mix(in srgb,var(--lav) 14%,transparent)}
.sty a[aria-current]{background:linear-gradient(90deg,var(--ice),var(--lav));color:#fff}.sty a[aria-current] b{color:#fff}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.petal{display:none}}
'''

def page_c():
    stats = ''.join(f'<div class="stat {c}"><b>{n}</b><span>{t}</span></div>' for n, t, c in STATS)
    petals = ''.join(f'<img class="petal" src="{IMG}{n}.webp" alt="" aria-hidden="true" style="left:{x}%;--w:{w}px;--d:{d}s;--dl:{dl}s">'
                     for n, x, w, d, dl in [('cry5', 30, 24, 16, -2), ('cry6', 52, 20, 19, -9), ('cry5', 74, 18, 14, -5), ('cry6', 90, 26, 21, -14), ('cry7', 64, 16, 12, -7)])
    return head('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+TC:wght@600;700&family=Noto+Sans+TC:wght@400;500;700;800&display=swap', CSS_C, 'c') + f'''
<body>
{bar(f'<img src="{IMG}cry4.webp" alt="" aria-hidden="true">Raid Notes', '<span></span>')}
<section class="hero" aria-label="首頁主視覺">
  <img class="bn" src="{IMG}banner.webp" alt="版主角色：在雲海上抱著盾牌沉睡的羽翼騎士，遠方是水晶城堡" width="1900" height="633">
  {petals}
  <div class="hi"><div>
    <div class="tag"><img src="{IMG}cry7.webp" alt="" aria-hidden="true">FINAL FANTASY XIV · HIGH-END DUTY NOTES</div>
    <h1>Raid Notes</h1>
    <p class="lede">{LEDE}</p>
    <div class="stats">{stats}</div>
  </div></div>
</section>
<main>
  <div class="cpw">
    <img class="stk fl1" src="{IMG}cry5.webp" alt="" aria-hidden="true">
    <img class="stk fl2" src="{IMG}cry0.webp" alt="" aria-hidden="true">
    {panel('快速入口', 'QUICK START')}
  </div>
  <h2 class="sec"><img src="{IMG}cry2.webp" alt="" aria-hidden="true">版主整理<small>FEATURED</small></h2>
  <div class="feat">{feat}</div>
  <h2 class="sec"><img src="{IMG}cry3.webp" alt="" aria-hidden="true">使用說明<small>HOW TO USE</small></h2>
  <div class="notes-w"><img class="peek" src="{IMG}pose4.webp" alt="" aria-hidden="true" loading="lazy">
  <ul class="notes">
    {NOTES}
  </ul></div>
  {credits}
</main>
{FOOT}
{JS}
{PANEL_JS}
</body>
</html>'''


for name, fn in [('home.html', page_a), ('home_b.html', page_b), ('home_c.html', page_c)]:
    open(W + name, 'w', encoding='utf8').write(fn())
    print('wrote', name)
