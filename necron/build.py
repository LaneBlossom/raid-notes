import sys, importlib.util
D = '/home/claude/work/'
sp = importlib.util.spec_from_file_location('necron', D + 'necron/necron.py'); N = importlib.util.module_from_spec(sp); sp.loader.exec_module(N)
ns = {}
code = open(D + 'tea/build.py', encoding='utf8').read()
exec(code[code.index("NAV_CSS="):code.index("# ---- M8S page")], ns)
NAV_CSS, nav = ns['NAV_CSS'], ns['nav']

CSS = '''
:root{--bg:#f6f4ef;--surface:#fff;--fg:#1f2430;--muted:#6b7280;--line:#e3dfd5;--accent:#3b6fd8;--st:#3b82f6;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161f;--surface:#1a2030;--fg:#e6eaf2;--muted:#9aa4b8;--line:#2c3446;--accent:#7aa6ff;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12161f;--surface:#1a2030;--fg:#e6eaf2;--muted:#9aa4b8;--line:#2c3446;--accent:#7aa6ff;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.7 "Noto Sans TC",system-ui,-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:16px clamp(14px,3vw,40px) 60px}
.eyebrow{font-size:.78rem;letter-spacing:.12em;color:var(--muted);margin-top:18px}
h1{font-size:clamp(1.5rem,3vw,2rem);margin:.2em 0 .3em}
.lede{color:var(--muted);max-width:78ch;margin:0 0 10px}
.src{font-size:.85rem;color:var(--muted)}
.src a{color:var(--accent)}
.team{border-left:3px solid var(--accent);background:var(--surface);border-radius:8px;padding:10px 14px;margin:12px 0;font-size:.9rem}
.jump{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 4px}
.jump button,.mtools button{font:inherit;font-size:.82rem;font-weight:700;padding:5px 12px;border-radius:8px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
.jsp{flex:1}
details.blk{margin-top:18px}
details.blk>summary{list-style:none;display:flex;align-items:center;gap:10px;cursor:pointer;padding:8px 0;border-bottom:2px solid var(--accent);font-size:1.25rem;font-weight:800}
details.blk>summary::-webkit-details-marker{display:none}
details.blk:not([open])>summary{border-bottom-color:var(--line)}
.bn{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--accent);color:#fff;font-size:.9rem}
.chev{margin-left:auto;width:10px;height:10px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .15s}
details.blk:not([open]) .chev{transform:rotate(-45deg)}
.spgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:12px}
.sp{border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--surface);align-self:start}
.sp h4{margin:0 0 6px;font-size:.95rem;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.sp .st{font-variant-numeric:tabular-nums;font-size:.72rem;padding:1px 6px;border-radius:5px;background:var(--st);color:#fff;white-space:nowrap}
.sp svg,.dfig svg{width:100%;height:auto;display:block;color:var(--muted)}
.sp ul,.mbody ul{margin:6px 0 0;padding-left:1.15em;font-size:.88rem;line-height:1.6}
.mtools{display:flex;gap:6px;justify-content:flex-end;margin:10px 0 8px}
.mlist{display:flex;flex-direction:column;gap:8px}
details.mcard{border:1px solid var(--line);border-radius:12px;background:var(--surface);overflow:hidden}
details.mcard>summary{list-style:none;display:flex;align-items:center;gap:8px;padding:11px 14px;cursor:pointer;font-weight:700}
details.mcard>summary::-webkit-details-marker{display:none}
details.mcard>summary:hover{background:color-mix(in srgb,var(--accent) 8%,transparent)}
.mt{flex:1}
.mbadge{font-size:.7rem;font-weight:700;padding:1px 7px;border-radius:999px;background:color-mix(in srgb,var(--accent) 18%,transparent);color:var(--accent)}
.mchev{width:8px;height:8px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);margin:0 4px 3px}
details.mcard:not([open]) .mchev{transform:rotate(-45deg);margin-bottom:0}
.mbody{padding:4px 16px 14px;border-top:1px solid var(--line)}
.mbody>p{margin:10px 0 4px}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:12px 0 2px}
.dfig{margin:0;border:1px solid var(--line);border-radius:10px;padding:8px}
.tlcta{display:inline-flex;gap:8px;align-items:center;margin-top:10px;padding:9px 16px;border-radius:10px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700}
.endnote{font-size:.8rem;color:var(--muted);margin-top:28px}
'''


def blk(n, title, inner, open_=True):
    return (f'<details class="blk" id="b{n}"{" open" if open_ else ""}><summary><span class="bn">{n}</span>{title}<span class="chev" aria-hidden="true"></span></summary>{inner}</details>')


st = ''.join(
    f'<article class="sp"><h4><span class="st">{t}</span>{title}</h4>{svg or ""}<ul>{"".join(f"<li>{x}</li>" for x in lines)}</ul></article>'
    for t, title, svg, lines in N.ST_PANELS)
cards = ''
for i, (title, desc, how, figs) in enumerate(N.MECH, 1):
    badge = '<span class="mbadge">圖解</span>' if figs else ''
    dg = ('<div class="dgrid">' + ''.join(f'<figure class="dfig">{f}</figure>' for f in figs) + '</div>') if figs else ''
    cards += (f'<details class="mcard" id="m{i}"><summary><span class="mt">{title}</span>{badge}<span class="mchev" aria-hidden="true"></span></summary>'
              f'<div class="mbody"><p>{desc}</p><ul>{"".join(f"<li>{x}</li>" for x in how)}</ul>{dg}</div></details>')

body = f'''<div class="wrap">
{nav('necronx-guide.html')}
<div class="eyebrow">THE MINSTREL'S BALLAD: NECRON'S EMBRACE · 7.3 極神 · ST 騎士視角</div>
<h1>極永恆黑暗 攻略整合</h1>
<p class="lede">子言姐姐／XIVStrat 的打法，站位和標點照他們的「機制速覽」小抄，不用看分組換位、觀察成本最低。依序是 <b>ST 一圖流</b>（騎士要跑哪、看哪個方向）、<b>機制與解法</b>（每個機制一張卡，點開看說明和示意圖）、<b>時間軸</b>。整體難度不高，難點在後半的青藍連魂和群體恐慌。</p>
<p class="src">來源：<a href="https://www.bilibili.com/video/BV1xWatzpEdU/">子言姐姐「7.3攻略 永远之暗悲惶歼灭战」</a>、<a href="https://xivstrat.cn/07/necron">XIVStrat 永远之暗悲惶歼灭战（機制速覽小抄、場地標點）</a>。技能名稱用繁中服（cactbot 繁中翻譯），影片裡的國服名稱如「槍之衝擊」＝青藍衝擊、「暗之死腕」＝暗黑死腕、「群體恐慌」相同。</p>
<div class="team"><b>固定分組</b>：MT＋D1、ST＋D2、H1＋D3、H2＋D4 兩兩一組；分左右時 MT、H1、D1、D3 在左，ST、H2、D2、D4 在右。<b>標點</b>（同 XIVStrat 場地標點）：A、B 在左右兩側，C、D 在 A、B 內側偏下；1、2 在北邊內側，3、4 在 1、2 下方。</div>
<div class="jump" role="group" aria-label="跳到"><button type="button" data-go="b1">ST 一圖流</button><button type="button" data-go="b2">機制與解法</button><button type="button" data-go="b3">時間軸</button><span class="jsp"></span><button type="button" data-all="open">全部展開</button><button type="button" data-all="close">全部收合</button></div>
{blk(1, 'ST 一圖流', '<p class="src">照時間順序列出 ST 要去哪、開什麼。藍色是 ST；示意圖上方為 Boss（北）。</p><div class="spgrid">' + st + '</div>')}
{blk(2, '機制與解法', '<div class="mtools"><button type="button" data-cards="open">展開全部機制</button><button type="button" data-cards="close">全部收起</button></div><div class="mlist">' + cards + '</div>')}
{blk(3, '時間軸', '<p>完整時間軸（含 P1、小怪、單人坦克分支、P2）和 # 機制標籤，在時間軸小抄頁；那頁也可以自己排減傷、寫筆記。</p><a class="tlcta" href="necronx.html">打開時間軸小抄 →</a>')}
<p class="endnote">示意圖由本站依子言姐姐的攻略影片與 XIVStrat 機制速覽小抄重新繪製，位置為示意。</p>
</div>'''

JS = '''<script>
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-go]');if(b){var el=document.getElementById(b.dataset.go);if(el){el.open=true;el.scrollIntoView({behavior:'smooth',block:'start'})}return}
  var a=e.target.closest('[data-all]');if(a){document.querySelectorAll('details.blk,details.mcard').forEach(function(d){d.open=a.dataset.all==='open'});return}
  var c=e.target.closest('[data-cards]');if(c){document.querySelectorAll('details.mcard').forEach(function(d){d.open=c.dataset.cards==='open'})}
});
</script>'''

html = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>極永恆黑暗 攻略整合</title><style>' + CSS + NAV_CSS + '</style></head><body>' + body + JS + '</body></html>')
open(D + 'necronx-guide.html', 'w', encoding='utf8').write(html)
print(len(html))
