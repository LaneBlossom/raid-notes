"""Raid Notes 首頁：未來科技風＋頂部導覽列（hover 滑出大選單）＋手機側邊抽屜。"""
import re
W = '/home/claude/work/'
old = open(W + 'home.pre-acc.html', encoding='utf8').read()
credits = re.search(r'<p class="credits" id="credits">.*?</p>', old, re.S).group(0)

CAT = [
    ('savage', '零式', 'SAVAGE', [
        ('輕重量級', 'LIGHT-HEAVYWEIGHT', [
            ('M1S', '黑貓', [('m1s.html', '空白筆記')]), ('M2S', '蜂蜂小甜心', [('m2s.html', '空白筆記')]),
            ('M3S', '野蠻炸彈', [('m3s.html', '空白筆記')]), ('M4S', '狡雷', [('m4s.html', '空白筆記')])]),
        ('中重量級', 'CRUISERWEIGHT', [
            ('M5S', '青蛙舞者', [('m5s.html', '空白筆記')]), ('M6S', '糖彩狂潮', [('m6s.html', '空白筆記')]),
            ('M7S', '野蠻憎惡', [('m7s.html', '空白筆記')]),
            ('M8S', '呼嘯之劍', [('m8s.html', '版主筆記'), ('m8s-blank.html', '空白筆記')])]),
        ('重量級', 'HEAVYWEIGHT', [
            ('M9S', '致命美人', [('m9s.html', '空白筆記')]), ('M10S', '極限兄弟', [('m10s.html', '空白筆記')]),
            ('M11S', '霸王', [('m11s.html', '空白筆記')]), ('M12S', '林德布魯姆', [('m12s.html', '空白筆記')])]),
    ]),
    ('ex', '極神', 'EXTREME', [
        ('7.3', 'DAWNTRAIL', [('EX', '極永恆黑暗', [('necronx.html', '時間軸小抄'), ('necronx-guide.html', '攻略整合')])]),
    ]),
    ('ult', '絕境戰', 'ULTIMATE', [
        ('紅蓮・漆黑', 'SB / ShB', [
            ('UCOB', '絕巴哈', [('ucob.html', '空白筆記')]), ('UWU', '絕神兵', [('uwu.html', '空白筆記')]),
            ('TEA', '絕亞歷山大', [('tea.html', '版主筆記'), ('tea-blank.html', '空白筆記'), ('tea-guide.html', '攻略整合')])]),
        ('曉月・金曦', 'EW / DT', [
            ('DSR', '絕龍詩', [('dsr.html', '空白筆記')]), ('TOP', '絕歐米茄', [('top.html', '空白筆記')]),
            ('FRU', '絕伊甸', [('fru.html', '空白筆記')]), ('DMU', 'Dancing Mad', [('dmu.html', '空白筆記')])]),
    ]),
]
FEATURED = [
    ('TEA', '絕亞歷山大', '攻略整合', 'tea-guide.html', 'ULTIMATE', '每 P 的 ST 一圖流、機制卡、示意圖與時間軸', 'ult'),
    ('M8S', '呼嘯之劍', '版主筆記', 'm8s.html', 'SAVAGE', '版主隊伍的減傷軸、站位與打法（MMW、蘇帕）', 'savage'),
    ('EX', '極永恆黑暗', '攻略整合', 'necronx-guide.html', 'EXTREME', '7.3 極神：日服 L 團式，ST 一圖流＋全隊站位圖', 'ex'),
    ('TEA', '絕亞歷山大', '版主筆記', 'tea.html', 'ULTIMATE', '版主隊伍的時間軸、傳毒標記與減傷', 'ult'),
]


def links(ls):
    return ''.join(f'<a href="{h}" class="{"own" if t in ("版主筆記", "攻略整合") else ""}">{t}</a>' for h, t in ls)


def mega(key, zh, en, groups):
    cols = ''
    for gz, ge, items in groups:
        rows = ''.join(f'<li><span class="code">{c}</span><span class="nm">{n}</span><span class="lk">{links(ls)}</span></li>' for c, n, ls in items)
        cols += f'<div class="col"><div class="colh"><b>{gz}</b><small>{ge}</small></div><ul>{rows}</ul></div>'
    return (f'<li class="ni" data-cat="{key}"><button type="button" class="nb" aria-expanded="false" aria-controls="mm-{key}">'
            f'<span class="nzh">{zh}</span><span class="nen">{en}</span><span class="car" aria-hidden="true"></span></button>'
            f'<div class="mm" id="mm-{key}" role="region" aria-label="{zh}"><div class="mmi"><div class="mmh"><span class="hud">// {en}</span><b>{zh}</b></div>'
            f'<div class="cols">{cols}</div></div></div></li>')


def drawer():
    out = ''
    for key, zh, en, groups in CAT:
        inner = ''
        for gz, ge, items in groups:
            inner += f'<div class="dg"><div class="dgh">{gz}<small>{ge}</small></div>' + ''.join(
                f'<div class="dr"><span class="code">{c}</span><span class="nm">{n}</span><span class="lk">{links(ls)}</span></div>' for c, n, ls in items) + '</div>'
        out += f'<details class="dc {key}"><summary><span class="nzh">{zh}</span><span class="nen">{en}</span></summary>{inner}</details>'
    return out


feat = ''.join(
    f'<a class="ft {k}" href="{h}"><span class="fk">{tag}</span><span class="fc">{c}</span><b>{n}</b><span class="fv">{v}</span><p>{d}</p><span class="go" aria-hidden="true">→</span></a>'
    for c, n, v, h, tag, d, k in FEATURED)
count = sum(len(items) for _, _, _, g in CAT for _, _, items in g)

CSS = r'''
:root{--bg:#05070d;--bg2:#0a0f1c;--panel:rgba(12,20,38,.72);--line:rgba(110,231,255,.16);--fg:#e8f3ff;--muted:#8aa0bf;
  --cy:#5ee7ff;--mg:#ff4fd8;--sv:#ff6b8b;--ex:#3ee8c0;--ul:#b58cff;--glow:0 0 18px rgba(94,231,255,.35);color-scheme:dark}
:root[data-theme="light"]{--bg:#eef3fa;--bg2:#e3ebf6;--panel:rgba(255,255,255,.82);--line:rgba(20,80,140,.16);--fg:#0b1626;--muted:#4b5d78;
  --cy:#0891b2;--mg:#c026d3;--sv:#e11d48;--ex:#0d9488;--ul:#7c3aed;--glow:0 0 14px rgba(8,145,178,.25);color-scheme:light}
@media (prefers-color-scheme:light){:root:not([data-theme]){--bg:#eef3fa;--bg2:#e3ebf6;--panel:rgba(255,255,255,.82);--line:rgba(20,80,140,.16);--fg:#0b1626;--muted:#4b5d78;
  --cy:#0891b2;--mg:#c026d3;--sv:#e11d48;--ex:#0d9488;--ul:#7c3aed;--glow:0 0 14px rgba(8,145,178,.25);color-scheme:light}}
*{box-sizing:border-box}
html{font-size:clamp(15px,calc(10px + .45vw),18px)}
body{margin:0;min-height:100vh;color:var(--fg);font-family:"Noto Sans TC",system-ui,sans-serif;
  background:radial-gradient(1200px 700px at 80% -10%,rgba(94,231,255,.12),transparent 60%),radial-gradient(900px 600px at -10% 40%,rgba(255,79,216,.08),transparent 60%),linear-gradient(180deg,var(--bg),var(--bg2));background-attachment:fixed}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:48px 48px;
  mask-image:radial-gradient(ellipse at 50% 0%,#000 30%,transparent 80%);opacity:.55}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:repeating-linear-gradient(180deg,rgba(255,255,255,.025) 0 1px,transparent 1px 3px)}
a{color:inherit}
.mono{font-family:"Orbitron","Rajdhani",ui-monospace,monospace}
/* ---- top bar ---- */
.bar{position:sticky;top:0;z-index:50;backdrop-filter:blur(14px) saturate(1.3);background:color-mix(in srgb,var(--bg) 78%,transparent);border-bottom:1px solid var(--line)}
.bar::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:linear-gradient(90deg,transparent,var(--cy),var(--mg),transparent);opacity:.7}
.bari{max-width:1280px;margin:0 auto;display:flex;align-items:center;gap:18px;padding:0 clamp(14px,3vw,36px);height:64px;padding-right:150px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:Orbitron,sans-serif;font-weight:800;letter-spacing:.18em;font-size:1rem}
.logo i{width:26px;height:26px;border:2px solid var(--cy);transform:rotate(45deg);box-shadow:var(--glow);position:relative}
.logo i::after{content:"";position:absolute;inset:5px;background:var(--mg);box-shadow:0 0 12px var(--mg)}
.nav{display:flex;gap:4px;list-style:none;margin:0;padding:0;height:100%}
.ni{position:static;height:100%;display:flex;align-items:center}
.nb{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:8px;padding:0 14px;height:100%;position:relative}
.nb .nzh{font-weight:800;font-size:1rem}
.nb .nen{font-family:Orbitron,sans-serif;font-size:.6rem;letter-spacing:.2em;color:var(--muted)}
.car{width:6px;height:6px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);align-self:center;transition:transform .25s}
.nb::after{content:"";position:absolute;left:14px;right:14px;bottom:0;height:2px;background:var(--c,var(--cy));transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.2,.8,.2,1);box-shadow:0 0 10px var(--c,var(--cy))}
.ni[data-cat="savage"]{--c:var(--sv)}.ni[data-cat="ex"]{--c:var(--ex)}.ni[data-cat="ult"]{--c:var(--ul)}
.ni.open .nb::after,.nb:hover::after,.nb:focus-visible::after{transform:scaleX(1)}
.ni.open .car{transform:rotate(225deg)}
.nb:focus-visible{outline:2px solid var(--cy);outline-offset:-4px}
/* mega menu */
.mm{position:absolute;left:0;right:0;top:100%;visibility:hidden;opacity:0;transform:translateY(-10px);clip-path:inset(0 0 100% 0);
  transition:opacity .25s,transform .35s cubic-bezier(.2,.8,.2,1),clip-path .4s cubic-bezier(.2,.8,.2,1),visibility 0s .4s}
.ni.open .mm{visibility:visible;opacity:1;transform:none;clip-path:inset(0 0 -40px 0);transition:opacity .25s,transform .35s cubic-bezier(.2,.8,.2,1),clip-path .45s cubic-bezier(.2,.8,.2,1)}
.mmi{max-width:1280px;margin:0 auto;padding:22px clamp(14px,3vw,36px) 26px;background:var(--bg2);backdrop-filter:blur(18px);
  border:1px solid var(--line);border-top:0;border-radius:0 0 18px 18px;box-shadow:0 30px 60px rgba(0,0,0,.35);position:relative}
.mmi::before{content:"";position:absolute;left:0;top:0;width:3px;bottom:0;background:var(--c);box-shadow:0 0 14px var(--c);border-radius:0 0 0 18px}
.mmh{display:flex;align-items:baseline;gap:12px;margin-bottom:14px}
.mmh b{font-size:1.4rem;color:var(--c)}
.hud{font-family:Orbitron,sans-serif;font-size:.68rem;letter-spacing:.25em;color:var(--muted)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.colh{display:flex;align-items:baseline;gap:8px;padding-bottom:8px;margin-bottom:6px;border-bottom:1px dashed var(--line)}
.colh small,.dgh small{font-family:Orbitron,sans-serif;font-size:.58rem;letter-spacing:.18em;color:var(--muted)}
.col ul{list-style:none;margin:0;padding:0}
.col li,.dr{display:grid;grid-template-columns:54px 1fr;gap:2px 10px;align-items:center;padding:7px 8px;border-radius:10px;
  opacity:0;transform:translateX(-8px);transition:opacity .3s,transform .35s,background .2s}
.ni.open .col li{opacity:1;transform:none}
.ni.open .col li:nth-child(2){transition-delay:.04s}.ni.open .col li:nth-child(3){transition-delay:.08s}.ni.open .col li:nth-child(4){transition-delay:.12s}
.col li:hover{background:color-mix(in srgb,var(--c) 10%,transparent)}
.code{font-family:Orbitron,sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.06em;color:var(--c,var(--cy));grid-row:span 2}
.nm{font-weight:700}
.lk{display:flex;gap:6px;flex-wrap:wrap}
.lk a{font-size:.75rem;text-decoration:none;padding:1px 8px;border-radius:6px;border:1px solid var(--line);color:var(--muted);transition:all .2s}
.lk a.own{border-color:color-mix(in srgb,var(--c,var(--cy)) 55%,transparent);color:var(--fg)}
.lk a:hover,.lk a:focus-visible{background:var(--c,var(--cy));color:#05070d;border-color:transparent;box-shadow:0 0 12px var(--c,var(--cy));outline:none}
/* mobile drawer */
.burger{all:unset;display:none;cursor:pointer;margin-left:auto;width:40px;height:40px;place-items:center;border:1px solid var(--line);border-radius:10px}
.burger span{display:block;width:18px;height:2px;background:var(--fg);box-shadow:0 6px 0 var(--fg),0 -6px 0 var(--fg)}
.drawer{position:fixed;inset:0 0 0 auto;width:min(88vw,380px);z-index:70;background:var(--bg2);border-left:1px solid var(--line);transform:translateX(102%);transition:transform .4s cubic-bezier(.2,.8,.2,1);overflow:auto;padding:70px 16px 30px}
.drawer.open{transform:none;box-shadow:-30px 0 60px rgba(0,0,0,.4)}
.scrim{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.45);opacity:0;pointer-events:none;transition:opacity .3s}
.scrim.open{opacity:1;pointer-events:auto}
.dc{border:1px solid var(--line);border-radius:12px;margin-bottom:10px;background:var(--panel)}
.dc.savage{--c:var(--sv)}.dc.ex{--c:var(--ex)}.dc.ult{--c:var(--ul)}
.dc summary{list-style:none;padding:12px 14px;cursor:pointer;display:flex;gap:8px;align-items:baseline}
.dc summary .nzh{font-weight:800;color:var(--c)}.dc summary .nen{font-family:Orbitron,sans-serif;font-size:.6rem;letter-spacing:.2em;color:var(--muted)}
.dg{padding:0 10px 10px}.dgh{font-size:.8rem;font-weight:700;color:var(--muted);margin:6px 4px}
.dr{opacity:1;transform:none}
@media (max-width:860px){.nav{display:none}.bar .burger{display:grid}.bari{padding-right:130px}}
/* hero */
main{position:relative;z-index:1;max-width:1280px;margin:0 auto;padding:clamp(30px,6vw,70px) clamp(14px,3vw,36px) 50px}
.tag{font-family:Orbitron,sans-serif;font-size:.7rem;letter-spacing:.35em;color:var(--cy)}
.tag::before{content:"";display:inline-block;width:28px;height:1px;background:var(--cy);vertical-align:middle;margin-right:10px;box-shadow:var(--glow)}
h1{font-family:Orbitron,sans-serif;font-weight:900;font-size:clamp(2.6rem,7vw,5.2rem);letter-spacing:.06em;margin:.15em 0 .2em;line-height:1;
  background:linear-gradient(90deg,var(--fg) 0%,var(--cy) 55%,var(--mg) 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 22px rgba(94,231,255,.25))}
.lede{max-width:62ch;color:var(--muted);font-size:1.02rem;line-height:1.85;margin:0}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 0}
.stat{position:relative;padding:10px 16px 10px 14px;border:1px solid var(--line);background:var(--panel);clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,0 100%)}
.stat b{font-family:Orbitron,sans-serif;font-size:1.3rem;color:var(--cy);display:block;line-height:1.1}
.stat span{font-size:.75rem;color:var(--muted)}
.stat.sv b{color:var(--sv)}.stat.ex b{color:var(--ex)}.stat.ul b{color:var(--ul)}
.hint{margin-top:14px;font-size:.8rem;color:var(--muted)}
.hint kbd{font-family:Orbitron,sans-serif;font-size:.7rem;border:1px solid var(--line);border-radius:5px;padding:1px 6px}
h2.sec{display:flex;align-items:baseline;gap:12px;margin:46px 0 14px;font-size:1.2rem}
h2.sec small{font-family:Orbitron,sans-serif;font-size:.62rem;letter-spacing:.3em;color:var(--muted)}
.feat{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.ft{position:relative;display:block;text-decoration:none;padding:18px 18px 20px;border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(8px);
  clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,18px 100%,0 calc(100% - 18px));transition:transform .3s,border-color .3s,box-shadow .3s}
.ft.savage{--c:var(--sv)}.ft.ex{--c:var(--ex)}.ft.ult{--c:var(--ul)}
.ft::before{content:"";position:absolute;left:0;top:0;width:40%;height:2px;background:var(--c);box-shadow:0 0 12px var(--c);transition:width .4s}
.ft:hover,.ft:focus-visible{transform:translateY(-3px);border-color:color-mix(in srgb,var(--c) 60%,transparent);outline:none}
.ft:hover::before,.ft:focus-visible::before{width:100%}
.fk{font-family:Orbitron,sans-serif;font-size:.6rem;letter-spacing:.25em;color:var(--c)}
.fc{float:right;font-family:Orbitron,sans-serif;font-weight:800;font-size:.8rem;color:var(--muted)}
.ft b{display:block;font-size:1.25rem;margin:8px 0 2px}
.fv{display:inline-block;font-size:.75rem;font-weight:700;padding:1px 8px;border-radius:5px;background:color-mix(in srgb,var(--c) 22%,transparent);color:var(--c)}
.ft p{margin:10px 0 0;color:var(--muted);font-size:.86rem;line-height:1.6}
.go{position:absolute;right:16px;bottom:12px;font-family:Orbitron,sans-serif;color:var(--c);transition:transform .3s}
.ft:hover .go{transform:translateX(4px)}
.notes{margin:0;padding:16px 18px 16px 34px;border:1px solid var(--line);background:var(--panel);border-radius:4px;color:var(--muted);line-height:1.8;font-size:.9rem}
.notes b{color:var(--fg)}
.credits{margin-top:34px;max-width:80ch;font-size:.8rem;line-height:1.7;color:var(--muted)}
footer{position:relative;z-index:1;text-align:center;font-size:.72rem;color:var(--muted);padding:20px 0 40px;font-family:Orbitron,"Noto Sans TC",sans-serif;letter-spacing:.06em}
.rn-thm{top:14px!important;right:16px!important;z-index:80!important}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
'''

JS = r'''<script>
(function(){
  var items=[].slice.call(document.querySelectorAll('.ni')),hover=matchMedia('(hover:hover)').matches,t=null;
  function close(except){items.forEach(function(n){if(n!==except){n.classList.remove('open');n.querySelector('.nb').setAttribute('aria-expanded','false')}})}
  function open(n){close(n);n.classList.add('open');n.querySelector('.nb').setAttribute('aria-expanded','true')}
  items.forEach(function(n){var b=n.querySelector('.nb');
    if(hover){n.addEventListener('mouseenter',function(){clearTimeout(t);open(n)});n.addEventListener('mouseleave',function(){t=setTimeout(function(){n.classList.remove('open');b.setAttribute('aria-expanded','false')},180)})}
    b.addEventListener('click',function(){n.classList.contains('open')?close():open(n)});
    n.addEventListener('focusout',function(e){if(!n.contains(e.relatedTarget)){n.classList.remove('open');b.setAttribute('aria-expanded','false')}});
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){var o=document.querySelector('.ni.open');close();if(o)o.querySelector('.nb').focus();dr(false)}});
  document.addEventListener('click',function(e){if(!e.target.closest('.ni'))close()});
  var D=document.querySelector('.drawer'),S=document.querySelector('.scrim'),B=document.querySelector('.burger');
  function dr(o){D.classList.toggle('open',o);S.classList.toggle('open',o);B.setAttribute('aria-expanded',o);if(o)D.querySelector('summary').focus()}
  B.addEventListener('click',function(){dr(!D.classList.contains('open'))});S.addEventListener('click',function(){dr(false)});
  document.querySelector('.dclose').addEventListener('click',function(){dr(false);B.focus()});
})();
</script>'''

nav = ''.join(mega(k, z, e, g) for k, z, e, g in CAT)
html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Raid Notes · FFXIV 高難筆記</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="bar"><div class="bari">
  <a class="logo" href="index.html" aria-label="Raid Notes 首頁"><i aria-hidden="true"></i>RAID NOTES</a>
  <ul class="nav" aria-label="副本分類">{nav}</ul>
  <button type="button" class="burger" aria-label="開啟副本選單" aria-expanded="false" aria-controls="drawer"><span></span></button>
</div></header>
<div class="scrim" aria-hidden="true"></div>
<nav class="drawer" id="drawer" aria-label="副本選單"><button type="button" class="dclose burger" style="display:grid;position:absolute;top:14px;right:14px" aria-label="關閉選單">✕</button>{drawer()}</nav>
<main>
  <div class="tag">FINAL FANTASY XIV · HIGH-END DUTY NOTES</div>
  <h1>RAID NOTES</h1>
  <p class="lede">繁中服豆芽玩家第一次挑戰高難本，邊打邊做的筆記，整理起來方便記憶。時間軸小抄可以切換職位看減傷和站位；有些副本另外附攻略整理。從上方選單挑副本。</p>
  <div class="stats">
    <div class="stat sv"><b>12</b><span>零式</span></div>
    <div class="stat ex"><b>1</b><span>極神</span></div>
    <div class="stat ul"><b>7</b><span>絕境戰</span></div>
    <div class="stat"><b>{count}</b><span>副本總數</span></div>
  </div>
  <h2 class="sec">版主整理<small>FEATURED</small></h2>
  <div class="feat">{feat}</div>
  <h2 class="sec">使用說明<small>HOW TO USE</small></h2>
  <ul class="notes">
    <li><b>版主筆記</b>是作者自己隊伍的減傷軸、站位和打法；<b>空白筆記</b>只有 Boss 技能時間軸和機制標籤，減傷、站位留給你自己填。</li>
    <li>版主筆記的減傷軸是照作者隊伍的組成排的，拿去用的話記得依你們的隊伍重新調整。</li>
    <li>小抄裡按「編輯減傷」就能改每個人放的技能，也能寫筆記、貼圖；改好的內容可以<b>匯出</b>成分享碼或檔案給隊友<b>匯入</b>。</li>
  </ul>
  {credits}
</main>
<footer>FINAL FANTASY XIV © SQUARE ENIX CO., LTD. All Rights Reserved. 個人非商業筆記。</footer>
{JS}
</body>
</html>'''
open(W + 'home.html', 'w', encoding='utf8').write(html)
print('ok', count)
