"""全站選單列（筆記頁、攻略頁用）：跟首頁同樣的 Logo＋零式／極神／絕境戰大選單＋手機漢堡。
class 全部加 gn- 前綴，避免跟小抄模板撞名；顏色吃各頁自己的變數，所以標準與三種風格都會自動配色。
用法：from gnav import bar; s = bar(s, 'm8s.html', guide=False)"""
import re
W = '/home/claude/work/'
_src = open(W + 'home_build.py', encoding='utf8').read()
_ns = {}
exec(_src[:_src.index("\nCSS = r'''")].replace("open(W + 'home.pre-acc.html'", "open(W + 'home_a.html'"), _ns)
CAT, mega, drawer = _ns['CAT'], _ns['mega'], _ns['drawer']


def _pref(h):
    h = re.sub(r'class="([^"]+)"', lambda m: 'class="' + ' '.join('gn-' + c for c in m.group(1).split()) + '"', h)
    return h.replace('id="mm-', 'id="gn-mm-').replace('aria-controls="mm-', 'aria-controls="gn-mm-')


NAV = _pref(''.join(mega(k, z, e, g) for k, z, e, g in CAT))
DRAWER = _pref(drawer())

CSS = r'''<style>
/* ===== 全站選單列 gn- ===== */
.gn{--gn-bg:var(--panel,var(--surface,#fff));--gn-a:var(--accent,var(--st,#3b6fd8));--gn-sv:#e2559a;--gn-ex:#14a89a;--gn-ul:#7c5cf0;
  position:sticky;top:0;z-index:58;margin:0 0 12px;background:color-mix(in srgb,var(--gn-bg) 86%,transparent);backdrop-filter:blur(12px) saturate(1.3);
  border-bottom:1px solid var(--line);color:var(--fg);font-family:"Noto Sans TC",system-ui,sans-serif;transition:transform .28s ease}
.gn.gn-hide{transform:translateY(-100%)}
.gn-in{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:16px;height:52px;padding:0 clamp(12px,2.5vw,28px)}
.gn.gn-pad .gn-in{padding-right:150px}
.gn-logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:inherit;font-family:var(--f-disp,inherit);font-weight:800;letter-spacing:.12em;font-size:.92rem;white-space:nowrap}
.gn-logo i{width:15px;height:15px;transform:rotate(45deg);border:2px solid var(--gn-a);background:color-mix(in srgb,var(--gn-a) 30%,transparent)}
.gn-nav{display:flex;gap:2px;list-style:none;margin:0;padding:0;height:100%}
.gn-ni{display:flex;align-items:center;height:100%}
.gn-ni[data-cat="savage"]{--c:var(--gn-sv)}.gn-ni[data-cat="ex"]{--c:var(--gn-ex)}.gn-ni[data-cat="ult"]{--c:var(--gn-ul)}
.gn-nb{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:7px;padding:7px 12px;border-radius:999px;font-size:.88rem}
.gn-nb .gn-nzh{font-weight:700}.gn-nb .gn-nen{font-size:.58rem;letter-spacing:.16em;color:var(--muted)}
.gn-car{width:6px;height:6px;border-right:1.5px solid var(--muted);border-bottom:1.5px solid var(--muted);transform:rotate(45deg) translateY(-2px);transition:transform .2s}
.gn-nb:hover,.gn-ni.gn-open .gn-nb,.gn-nb:focus-visible{background:color-mix(in srgb,var(--c) 14%,transparent);outline:none}
.gn-ni.gn-open .gn-car{transform:rotate(225deg)}
.gn-mm{position:absolute;left:0;right:0;top:100%;padding:8px clamp(12px,2.5vw,28px) 0;visibility:hidden;opacity:0;transform:translateY(-6px);transition:opacity .2s,transform .25s,visibility 0s .25s}
.gn-ni.gn-open .gn-mm{visibility:visible;opacity:1;transform:none;transition:opacity .2s,transform .25s}
.gn-mmi{max-width:1200px;margin:0 auto;padding:16px 18px 18px;background:var(--gn-bg);border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.18);border-top:3px solid var(--c)}
.gn-mmh{display:flex;align-items:baseline;gap:10px;margin-bottom:10px}.gn-mmh b{font-size:1.15rem;color:var(--c)}
.gn-hud{font-size:.62rem;letter-spacing:.22em;color:var(--muted)}
.gn-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.gn-colh{display:flex;align-items:baseline;gap:8px;padding-bottom:5px;margin-bottom:4px;border-bottom:1px solid var(--line);font-size:.9rem}
.gn-colh small,.gn-dgh small{font-size:.58rem;letter-spacing:.14em;color:var(--muted)}
.gn-col ul{list-style:none;margin:0;padding:0}
.gn-col li,.gn-dr{display:grid;grid-template-columns:50px 1fr;gap:2px 10px;align-items:center;padding:6px 8px;border-radius:10px}
.gn-col li:hover{background:color-mix(in srgb,var(--c) 9%,transparent)}
.gn-code{font-family:var(--f-disp,inherit);font-size:.72rem;font-weight:700;color:var(--c,var(--gn-a));grid-row:span 2}
.gn-nm{font-weight:700;font-size:.9rem}
.gn-lk{display:flex;gap:5px;flex-wrap:wrap}
.gn-lk a{font-size:.72rem;text-decoration:none;padding:1px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.gn-lk a.gn-own{color:var(--fg);border-color:color-mix(in srgb,var(--c,var(--gn-a)) 50%,transparent)}
.gn-lk a:hover,.gn-lk a:focus-visible{background:var(--c,var(--gn-a));color:#fff;border-color:transparent;outline:none}
.gn-lk a[aria-current]{background:var(--c,var(--gn-a));color:#fff;border-color:transparent}
.gn-burger{all:unset;display:none;cursor:pointer;margin-left:auto;width:38px;height:38px;place-items:center;border:1px solid var(--line);border-radius:10px}
.gn-burger span{display:block;width:16px;height:2px;background:var(--fg);box-shadow:0 5px 0 var(--fg),0 -5px 0 var(--fg)}
.gn-drawer{position:fixed;inset:0 0 0 auto;width:min(88vw,380px);z-index:70;background:var(--gn-bg);color:var(--fg);border-left:1px solid var(--line);transform:translateX(102%);transition:transform .3s;overflow:auto;padding:64px 14px 30px;font-family:"Noto Sans TC",system-ui,sans-serif}
.gn-drawer.gn-open{transform:none;box-shadow:0 0 40px rgba(0,0,0,.3)}
.gn-scrim{position:fixed;inset:0;z-index:69;background:rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:opacity .25s}
.gn-scrim.gn-open{opacity:1;pointer-events:auto}
.gn-dclose{all:unset;cursor:pointer;position:absolute;top:14px;right:14px;width:38px;height:38px;display:grid;place-items:center;border:1px solid var(--line);border-radius:10px}
.gn-dc{border:1px solid var(--line);border-radius:12px;margin-bottom:10px}
.gn-dc.gn-savage{--c:var(--gn-sv)}.gn-dc.gn-ex{--c:var(--gn-ex)}.gn-dc.gn-ult{--c:var(--gn-ul)}
.gn-dc summary{list-style:none;padding:11px 14px;cursor:pointer;display:flex;gap:8px;align-items:baseline}
.gn-dc summary .gn-nzh{font-weight:800;color:var(--c)}.gn-dc summary .gn-nen{font-size:.6rem;letter-spacing:.14em;color:var(--muted)}
.gn-dg{padding:0 8px 8px}.gn-dgh{font-size:.78rem;font-weight:700;color:var(--muted);margin:6px 4px}
@media (max-width:860px){.gn-nav{display:none}.gn-burger{display:grid}.gn.gn-pad .gn-in{padding-right:120px}.gn.gn-pad .gn-burger{margin-left:auto}}
/* 小抄頁的固定控制列在選單列出現時往下讓位 */
html:not([data-home]) .controls{top:var(--gn-off,0px)!important;transition:top .28s ease}
/* 舊的「首頁＋副本下拉」由全站選單列取代 */
.sitenav>a[href="index.html"],.sitenav>details.rsw{display:none!important}
/* 風格 */
html[data-skin="future"] .gn{border-bottom-color:color-mix(in srgb,var(--gn-a) 35%,transparent);box-shadow:0 1px 18px color-mix(in srgb,var(--gn-a) 18%,transparent)}
html[data-skin="future"] .gn-logo{font-family:Orbitron,"Noto Sans TC",sans-serif}
html[data-skin="future"] .gn-mmi{border-radius:0;clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,0 100%)}
html[data-skin="pixel"] .gn{border-bottom:3px solid var(--fg);background:var(--bg);backdrop-filter:none;--gn-sv:var(--fg);--gn-ex:var(--fg);--gn-ul:var(--fg)}
html[data-skin="pixel"] .gn *{border-radius:0!important}
html[data-skin="pixel"] .gn-logo{font-family:"Press Start 2P",monospace;font-size:.62rem;letter-spacing:.06em;font-weight:400}
html[data-skin="pixel"] .gn-logo i{transform:none;background:var(--fg);border-color:var(--fg)}
html[data-skin="pixel"] .gn-mmi{border:3px solid var(--fg);box-shadow:6px 6px 0 var(--fg);border-top-width:3px}
html[data-skin="pixel"] .gn-ni.gn-open .gn-nb,html[data-skin="pixel"] .gn-nb:hover{background:var(--fg);color:var(--bg)}
html[data-skin="pixel"] .gn-lk a:hover,html[data-skin="pixel"] .gn-lk a[aria-current]{color:var(--bg)}
html[data-skin="crystal"] .gn-logo{font-family:Cinzel,"Noto Serif TC",serif;letter-spacing:.14em;font-weight:700}
html[data-skin="crystal"] .gn-logo i{border-radius:3px;border:0;background:linear-gradient(135deg,#8ea6ff,#b9a3ff,#f5a8d6)}
html[data-skin="crystal"] .gn-mmi{border-radius:20px;border-top:1px solid var(--line);position:relative;overflow:hidden}
html[data-skin="crystal"] .gn-mmi::before{content:"";position:absolute;inset:0 0 auto;height:3px;background:linear-gradient(90deg,#8ea6ff,var(--c),#f5a8d6)}
html[data-skin="crystal"] .gn-nb{border-radius:999px}
@media (prefers-reduced-motion:reduce){.gn,.gn-mm,.gn-drawer{transition:none}}
</style>'''

JS = r'''<script>(function(){var G=document.querySelector('.gn');if(!G)return;
var items=[].slice.call(G.querySelectorAll('.gn-ni')),hover=matchMedia('(hover:hover)').matches,t=null;
function close(ex){items.forEach(function(n){if(n!==ex){n.classList.remove('gn-open');n.querySelector('.gn-nb').setAttribute('aria-expanded','false')}})}
function open(n){close(n);n.classList.add('gn-open');n.querySelector('.gn-nb').setAttribute('aria-expanded','true')}
items.forEach(function(n){var b=n.querySelector('.gn-nb');
 if(hover){n.addEventListener('mouseenter',function(){clearTimeout(t);open(n)});n.addEventListener('mouseleave',function(){t=setTimeout(function(){n.classList.remove('gn-open');b.setAttribute('aria-expanded','false')},180)})}
 b.addEventListener('click',function(){n.classList.contains('gn-open')?close():open(n)});
 n.addEventListener('focusout',function(e){if(!n.contains(e.relatedTarget)){n.classList.remove('gn-open');b.setAttribute('aria-expanded','false')}})});
var D=document.querySelector('.gn-drawer'),S=document.querySelector('.gn-scrim'),B=G.querySelector('.gn-burger');
function dr(o){D.classList.toggle('gn-open',o);S.classList.toggle('gn-open',o);B.setAttribute('aria-expanded',o);if(o)D.querySelector('summary').focus()}
B.addEventListener('click',function(){dr(!D.classList.contains('gn-open'))});S.addEventListener('click',function(){dr(false)});
D.querySelector('.gn-dclose').addEventListener('click',function(){dr(false);B.focus()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){var o=G.querySelector('.gn-ni.gn-open');close();if(o)o.querySelector('.gn-nb').focus();if(D.classList.contains('gn-open')){dr(false);B.focus()}}});
document.addEventListener('click',function(e){if(!e.target.closest('.gn-ni'))close()});
/* 往下捲收起、往上捲出現；小抄的固定控制列跟著讓位 */
var R=document.documentElement,last=scrollY,h=G.offsetHeight;
function off(){R.style.setProperty('--gn-off',G.classList.contains('gn-hide')||scrollY<1?'0px':h+'px')}
addEventListener('scroll',function(){var y=scrollY;if(Math.abs(y-last)<6)return;
 if(y>last&&y>h*2&&!G.querySelector('.gn-open')){G.classList.add('gn-hide')}else if(y<last){G.classList.remove('gn-hide')}last=y;off()},{passive:true});
addEventListener('resize',function(){h=G.offsetHeight;off()});off();
})();</script>'''


def bar(s, cur, guide=False):
    """把全站選單列插在頁面主體最前面（sitenav 所在的 <body> 之後）。"""
    nav = NAV.replace(f'href="{cur}"', f'href="{cur}" aria-current="page"')
    drw = DRAWER.replace(f'href="{cur}"', f'href="{cur}" aria-current="page"')
    html = (CSS + f'<header class="gn{" gn-pad" if guide else ""}"><div class="gn-in">'
            '<a class="gn-logo" href="index.html" aria-label="Raid Notes 首頁"><i aria-hidden="true"></i>RAID NOTES</a>'
            f'<ul class="gn-nav" aria-label="副本分類">{nav}</ul>'
            '<button type="button" class="gn-burger" aria-label="開啟副本選單" aria-expanded="false" aria-controls="gn-drawer"><span></span></button>'
            '</div></header><div class="gn-scrim" aria-hidden="true"></div>'
            f'<nav class="gn-drawer" id="gn-drawer" aria-label="副本選單"><button type="button" class="gn-dclose" aria-label="關閉選單">✕</button>{drw}</nav>')
    i = s.index('<nav class="sitenav"')
    b = s.rfind('<body', 0, i)
    b = s.index('>', b) + 1 if b >= 0 else s.rindex('<div class="wrap">', 0, i)
    s = s[:b] + html + s[b:]
    j = s.rfind('</body>')
    return s + JS if j < 0 else s[:j] + JS + s[j:]
