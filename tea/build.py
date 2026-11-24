import re
D='/home/claude/work/'
s=open(D+'m8s.html',encoding='utf8').read()
def r(o,n,c=1):
    global s
    assert s.count(o)==c,(o[:80],s.count(o)); s=s.replace(o,n)

NAV_CSS='''.sitenav{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:10px;font-size:12px;position:relative;z-index:30}
.sitenav a,.sitenav summary{font-weight:700;text-decoration:none;padding:4px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel,var(--surface));color:var(--muted);cursor:pointer}
.sitenav a[aria-current="page"]{background:var(--fg);border-color:var(--fg);color:var(--bg)}
.sitenav a:focus-visible,.sitenav summary:focus-visible{outline:2px solid var(--st);outline-offset:2px}
.sitenav .rsw{position:relative}
.sitenav summary{list-style:none;color:var(--fg);display:inline-flex;align-items:center;gap:6px}
.sitenav summary::-webkit-details-marker{display:none}
.sitenav summary .cat{font-size:10px;font-weight:800;padding:0 6px;border-radius:4px;background:color-mix(in srgb,var(--fg) 12%,transparent)}
.sitenav summary::after{content:"▾";font-size:10px;opacity:.7}
.sitenav .rmenu{position:absolute;left:0;top:calc(100% + 6px);min-width:220px;max-height:min(70vh,480px);overflow:auto;padding:8px;border:1px solid var(--line);border-radius:10px;background:var(--panel,var(--surface));box-shadow:0 10px 30px rgba(0,0,0,.25)}
.sitenav .rmenu .rg{font-size:10px;font-weight:800;letter-spacing:.1em;color:var(--muted);padding:6px 8px 2px}
.sitenav .rmenu a{display:block;border:0;border-radius:6px;padding:6px 8px;background:none;color:var(--fg)}
.sitenav .rmenu a:hover{background:color-mix(in srgb,var(--fg) 8%,transparent)}
.sitenav .rmenu a[aria-current="page"]{background:color-mix(in srgb,var(--st) 18%,transparent);color:var(--fg)}
.sitenav .vers{display:flex;flex-wrap:wrap;gap:6px}
'''
RAIDS=[("零式・輕重量級",[("M1S 黑貓",[("m1s.html","空白筆記")]),("M2S 蜂蜂小甜心",[("m2s.html","空白筆記")]),
                      ("M3S 野蠻炸彈",[("m3s.html","空白筆記")]),("M4S 狡雷",[("m4s.html","空白筆記")])]),
       ("零式・中重量級",[("M5S 青蛙舞者",[("m5s.html","空白筆記")]),("M6S 糖彩狂潮",[("m6s.html","空白筆記")]),
                      ("M7S 野蠻憎惡",[("m7s.html","空白筆記")]),
                      ("M8S 呼嘯之劍",[("m8s.html","版主筆記"),("m8s-blank.html","空白筆記")])]),
       ("零式・重量級",[("M9S 致命美人",[("m9s.html","空白筆記")]),("M10S 極限兄弟",[("m10s.html","空白筆記")]),
                      ("M11S 霸王",[("m11s.html","空白筆記")]),("M12S 林德布魯姆",[("m12s.html","空白筆記")])]),
       ("極神",[("極永恆黑暗",[("necronx.html","時間軸小抄"),("necronx-guide.html","攻略整合")])]),
       ("絕境戰",[("絕巴哈",[("ucob.html","空白筆記")]),("絕神兵",[("uwu.html","空白筆記")]),
                 ("絕亞歷山大",[("tea.html","版主筆記"),("tea-blank.html","空白筆記"),("tea-guide.html","攻略整合")]),
                 ("絕龍詩",[("dsr.html","空白筆記")]),("絕歐米茄",[("top.html","空白筆記")]),("絕伊甸",[("fru.html","空白筆記")]),
                 ("Dancing Mad（凱夫卡）",[("dmu.html","空白筆記")])])]
def nav(cur):
    def a(h,t): return f'<a href="{h}"'+(' aria-current="page"' if h==cur else '')+f'>{t}</a>'
    me=None
    for cat,raids in RAIDS:
        for name,pages in raids:
            if any(h==cur for h,_ in pages): me=(cat,name,pages)
    menu=''.join(f'<div class="rg">{cat}</div>'+''.join(
        f'<a href="{pages[0][0]}"'+(' aria-current="page"' if me and name==me[1] else '')+f'>{name}</a>' for name,pages in raids) for cat,raids in RAIDS)
    summ=(f'<span class="cat">{me[0]}</span>{me[1]}' if me else '選副本')
    vers=''.join(a(h,t) for h,t in me[2]) if me else ''
    return ('<nav class="sitenav" aria-label="切換頁面">'+a("index.html","⌂ 首頁")+
            f'<details class="rsw"><summary aria-label="切換副本">{summ}</summary><div class="rmenu">{menu}</div></details>'+
            f'<div class="vers">{vers}</div>'
            '<script>document.addEventListener("click",function(e){document.querySelectorAll("details.rsw[open]").forEach(function(d){if(!d.contains(e.target))d.open=false})});document.addEventListener("keydown",function(e){if(e.key==="Escape")document.querySelectorAll("details.rsw[open]").forEach(function(d){d.open=false})})</script>'
            '</nav>')

# ---- M8S page: add nav ----
m8=s
m8=m8.replace('</style>',NAV_CSS+'</style>',1)
m8=m8.replace('  <header class="hd">\n','  <header class="hd">\n    '+nav('m8s.html')+'\n',1)
assert m8.count('sitenav" aria-label')==1
open(D+'m8s.html','w',encoding='utf8').write(m8)

# ---- TEA page ----
s=m8.replace(nav('m8s.html'),nav('tea.html'))
# data
a=s.index('const data = ['); b=s.index('\n];\n',a)+4
s=s[:a]+open(D+'tea/data.js',encoding='utf8').read()+s[b:]
# roles
a=s.index('const roles={'); b=s.index('\n};\n',a)+4
s=s[:a]+'const roles={team:{h:"· 全隊"}};\n'+s[b:]
# short / hints / figs
a=s.index('const SHORT={'); b=s.index('};\n',a)+3
s=s[:a]+'const SHORT={};\n'+s[b:]
a=s.index('const HINTS=['); b=s.index('\n',a)+1
s=s[:a]+'const HINTS='+open(D+'tea/hints.json',encoding='utf8').read().strip()+';\n'+s[b:]
a=s.index('HINTS.push('); b=s.index('\n',a)+1; s=s[:a]+s[b:]
r('const HINT_T={"09:13":["二二踩塔"]};','const HINT_T={"01:48":["換T"]};')
r('k==="剛刃一閃"&&r.m.includes("・終")','false')
import sys,json,base64
sys.path.insert(0,D+'tea'); from figs import FIGS,FIGMAP
FIGD={k:'data:image/jpeg;base64,'+base64.b64encode(open(D+f'tea/figimg/{k}.jpg','rb').read()).decode() for k in FIGS}
a=s.index('const FIG={'); b=s.index('\n',a)+1
s=s[:a]+'const FIG='+json.dumps(FIGD)+';\n'+s[b:]
a=s.index('const FIGMAP=['); b=s.index('\n',a)+1
s=s[:a]+'const FIGMAP='+json.dumps(FIGMAP,ensure_ascii=False)+';\n'+s[b:]
from figs import FIGPOS
a=s.index('const FIGPOS={'); b=s.index('\n',a)+1
s=s[:a]+'const FIGPOS='+json.dumps(FIGPOS)+';\n'+s[b:]
a=s.index('const FIGCAP={'); b=s.index('\n',a)+1
s=s[:a]+'const FIGCAP='+json.dumps({k:v[2] for k,v in FIGS.items()},ensure_ascii=False)+';\n'+s[b:]
r('{const fk=figOf(r); if(fk){const fb=el("button","figbtn","看圖");fb.type="button";fb.dataset.fig=fk;fb.dataset.alt=r.m+" 的站位圖";mh.append(fb)}}',
  'for(const x of FIGMAP.filter(x=>r.m.includes(x[0])&&(!x[3]||role==="team"||x[3].includes(role)))){const fb=el("button","figbtn",x[2]||"看圖");fb.type="button";fb.dataset.fig=x[1];fb.dataset.alt=r.m+" 的示意圖";mh.append(fb)}')
r('el("span","hint","#"+h)','el("span","hint"+(/^(一傳|二傳|三傳|疫苗|終審)/.test(h)?" poi":""),"#"+h)')
s=s.replace('</style>','.hint.poi{background:#7a3fc4!important;color:#fff!important;border-color:#7a3fc4!important;font-weight:800}\n</style>',1)
r('function relevant(r){if(plainMode())return true;','function relevant(r){if(plainMode())return true;if(r.poi&&role!=="team"&&r.poi[role])return true;')
r('      if((editing||mitv==="on") && r.press','      if(r.poi){const pv=role==="team"?r.poi.team:r.poi[role];if(pv){const d=el("div","poiline");d.append(el("b",null,"☍ "+r.poi.k),document.createTextNode(" "+pv));mh.append(d)}}\n      if((editing||mitv==="on") && r.press')
s=s.replace('</style>','.poiline{display:block;margin-top:4px;font-size:.86em;font-weight:600;line-height:1.45;color:var(--fg);background:color-mix(in srgb,#7a3fc4 14%,transparent);border-left:3px solid #7a3fc4;border-radius:4px;padding:2px 7px}\n.poiline b{color:#7a3fc4;margin-right:2px}\n@media (prefers-color-scheme:dark){.poiline b{color:#b98cf0}}\n</style>',1)
s=s.replace('const HINT_T={"01:48":["換T"]};','const HINT_T={"01:48":["換T"]};\nconst _hint0=hintsOf;\nhintsOf=function(r){const h=_hint0(r);if(r.poi&&(role==="team"||r.poi[role]))h.push(r.poi.k==="終審"?"終審排隊":r.poi.k);return h};',1)
# storage keys / share code
s=s.replace('"m8s-','"tea-').replace('M8S1:','TEA1:').replace('M8S時間軸_','絕亞時間軸_')
assert s.count('const STRAT="MMW、蘇帕";')==1
s=s.replace('const STRAT="MMW、蘇帕";','const STRAT="ふうcだよ（P1）・ぬけまる（P1.5、P3 次元斷絕）・魚子醬（P2～P4）";')
assert 'm8s-' not in s and 'M8S1' not in s
# default party
s=re.sub(r'const DEF_PARTY=\{[^}]*\}','const DEF_PARTY={MT:"GNB",ST:"PLD",H1:"AST",H2:"SGE",D1:"NIN",D2:"SAM",D3:"MCH",D4:"PCT"}',s,count=1)
# phase-aware CD check
r('r._def=L;ROWBYID[id]=r;','r._def=L;r._pi=pi;r._pl=(grp.part||"").split(" ")[0]||PL[pi]||"";PL[pi]=PL[pi]||r._pl;ROWBYID[id]=r;')
r('const ROWBYID={};','const ROWBYID={},PL={};')
r('    const t=secOfT(x.t==="team"&&r.press?r.press:r.t);if(t==null)continue;(uses[hit[0]]=uses[hit[0]]||{cd:hit[1],ts:[]}).ts.push(t)}',
  '    const t0=secOfT(x.t==="team"&&r.press?r.press:r.t);if(t0==null)continue;const t=r._pi*100000+t0;(uses[hit[0]]=uses[hit[0]]||{cd:hit[1],ts:[]}).ts.push(t)}')
r('const fmtS=x=>String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0");',
  'const fmtS=x=>{const p=Math.floor(x/100000),y=x%100000;return (PL[p]?PL[p]+" ":"")+String(Math.floor(y/60)).padStart(2,"0")+":"+String(y%60).padStart(2,"0")};')
# header text
r('<title>M8S 版主筆記</title>','<title>絕亞 版主筆記</title>')
r('<div class="eyebrow">AAC Cruiserweight M4 Savage · 呼嘯之劍 · 門神＋本體</div>','<div class="eyebrow">The Epic of Alexander (Ultimate) · 絕亞歷山大討滅戰 · 繁中服野團打法</div>')
r('<h1>M8S 版主筆記 ','<h1>絕亞 版主筆記 ')
r('<p class="sub">每一行的時間是 Boss 技能的判定時間，「軸 xx:xx 按」是隊伍排的按鍵時間。圈數字是這招第幾次出現。門神狼頭之後的時間會隨狼打多快前後差幾秒。</p>',
  '<p class="sub">每個階段各自從 00:00 算起：P1 從開怪、P1.5 從第一發照準、P2 從 Boss 可選中、P3 從時停、P4 從終審判決讀條。時間是技能判定時間，實際會隨打速前後差幾秒。詳細跑位看上面的「絕亞 攻略」。</p>')
# span buttons
r('''      <button id="s-1" data-span="1" aria-pressed="false">前半 · 門神</button>
      <button id="s-2" data-span="2" aria-pressed="false">後半 · 本體</button>''','''      <button id="s-1" data-span="1" aria-pressed="false">P1</button>
      <button id="s-2" data-span="2" aria-pressed="false">P1.5</button>
      <button id="s-3" data-span="3" aria-pressed="false">P2</button>
      <button id="s-4" data-span="4" aria-pressed="false">P3</button>
      <button id="s-5" data-span="5" aria-pressed="false">P4</button>''')
r('sp={all:"全部","1":"前半","2":"後半"}','sp={all:"全部","1":"P1","2":"P1.5","3":"P2","4":"P3","5":"P4"}')
r('const names={team:"全隊",st:"ST",mt:"MT",d1:"D1",d2:"D2",d3:"D3",d4:"D4"}','const names={team:"全隊",st:"ST",mt:"MT",h1:"H1",h2:"H2",d1:"D1",d2:"D2",d3:"D3",d4:"D4"}')
# arena hidden
r('<section class="arena closed" id="arena" aria-labelledby="arena-h">','<section class="arena closed" id="arena" aria-labelledby="arena-h" style="display:none">')
# endnote / thanks
a=s.index('<p class="endnote">'); b=s.index('</p>',a)+4
s=s[:a]+'<p class="endnote">時間照 cactbot 的絕亞時間軸換算。打法與減傷整理自 ふうcだよ（P1）、ぬけまる（P1.5、P3 次元斷絕）、魚子醬（P2～P4）的攻略影片。技能名稱照國服翻譯轉繁體，台服可能略有不同。</p>'+s[b:]
if '<p class="thanks">' in s:
    a=s.index('<p class="thanks">'); b=s.index('</p>',a)+4
    s=s[:a]+s[b:]
# release notes
a=s.index('    <ol>',s.index('id="release"')); b=s.index('    </ol>',a)+len('    </ol>')
s=s[:a]+'    <ol>\n      <li><b>v1.3</b><time>11/20</time><ul><li>P3 兩次死刑：第一次 ST 無敵 4 下，第二次 MT 無敵</li></ul></li>\n      <li><b>v1.2</b><time>11/10</time><ul><li>選職位後顯示自己的傳毒對象和時機</li><li>P3、P4 加影片站位截圖（滑鼠指過去看）</li><li>傳毒標籤改成依職位顯示；P2、P3 誤標的集團罪改回生命計算法</li></ul></li>\n      <li><b>v1.1</b><time>11/10</time><ul><li>P2～P4 改用版主隊伍團減軸，預設隊伍改成這次組成</li><li>ST 減傷改用騎士技能名</li><li>P2 加影片標點截圖（滑鼠指過去看）</li><li>一傳／二傳／三傳／終審用紫色標籤標出</li></ul></li>\n      <li><b>v1.0</b><time>11/08</time><ul><li>絕亞時間軸小抄上線：P1、P1.5、P2、P3、P4 全機制</li><li>ST 騎士減傷照攻略排好</li><li>可切換職責、編輯減傷、分享碼、筆記</li></ul></li>\n    </ol>'+s[b:]
s=re.sub(r'<span>最新 v[0-9.]+・[0-9/]+</span>','<span>最新 v1.3・11/20</span>',s,count=1)
s=re.sub(r'const VER="v[0-9.]+";','const VER="v1.3";',s,count=1)
open(D+'tea.html','w',encoding='utf8').write(s)
print(len(s))
