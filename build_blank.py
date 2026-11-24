import os
"""Build blank-note pages (timeline + mechanic tags only) from the built author pages.
Run after tea/build.py and tea/build_guide.py."""
import re, json, subprocess, sys
W = '/home/claude/work/'
sys.path.insert(0, W + 'tea')

BLANK_CSS = '''.blanknote{margin:10px 0 0;padding:10px 14px;border:1px dashed var(--line);border-left:4px solid var(--st);border-radius:8px;background:var(--panel);font-size:13px;line-height:1.6;color:var(--fg)}
.blanknote b{color:var(--st)}
'''
BLANK_NOTE = ('<div class="blanknote"><b>空白筆記</b>：只有 Boss 技能時間軸和機制標籤，減傷、站位都是空的。'
              '按「編輯減傷」填上你們隊伍的減傷，每一行也可以寫自己的筆記；填好後可以匯出分享碼給隊友匯入。'
              '設定只存在你自己的瀏覽器。</div>')

STRIP_JS = r'''
const fs=require('fs');const [src,out,mode]=process.argv.slice(2);
let text=fs.readFileSync(src,'utf8');
const a=text.indexOf('const data = [');const b=text.indexOf('\n];',a)+3;
eval(text.slice(a,b).replace('const data','global.data'));
for(const g of data){ if(mode==='strip'){delete g.rules;delete g.warn;}
  for(const r of g.rows){ if(mode!=='strip')continue;
    r.c=[];for(const k of ['st','mt','n','nst','pos','press','poi','tp'])delete r[k];}}
const ser=v=>{if(Array.isArray(v))return '['+v.map(ser).join(',')+']';if(v&&typeof v==='object')return '{'+Object.entries(v).map(([k,x])=>k+':'+ser(x)).join(',')+'}';return JSON.stringify(v)};
fs.writeFileSync(out,'const data = [\n'+data.map(g=>{const {rows,...h}=g;return ser(h).slice(0,-1)+(Object.keys(h).length?', ':'')+'rows:[\n'+rows.map(r=>'  '+ser(r)).join(',\n')+'\n]}'}).join(',\n')+'\n];\n');
'''
open(W + 'strip.js', 'w').write(STRIP_JS)


SETUP_CSS = """.setup{margin:10px 0 0;padding:12px 14px;border:1px solid var(--st);border-radius:10px;background:var(--panel);font-size:13px;line-height:1.6}
.setup h3{margin:0 0 6px;font-size:15px}
.setup .opts{display:flex;flex-wrap:wrap;gap:8px}
.setup button{font:inherit;font-weight:700;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);cursor:pointer}
.setup button.primary{background:var(--st);border-color:var(--st);color:var(--on-badge,#fff)}
.setup button.link{border:0;background:none;padding:0 4px;color:var(--st);text-decoration:underline;font-weight:600}
.setup .opts small{display:block;font-weight:400;color:var(--muted)}
.setup .solo{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px}
.setup select{font:inherit;padding:4px 6px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
.setup.flash{animation:setupflash 1s ease 2}
@keyframes setupflash{50%{box-shadow:0 0 0 4px color-mix(in srgb,var(--st) 40%,transparent)}}
"""
SETUP_JS = r"""<script>
(function(){
var K="__KEY__setup",box=document.getElementById("setup");if(!box)return;
function get(){try{return localStorage.getItem(K)}catch(e){return null}}
function set(v){try{v?localStorage.setItem(K,v):localStorage.removeItem(K)}catch(e){}}
function mk(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function btn(txt,cls,sub,fn){var b=mk("button",cls);b.type="button";b.append(document.createTextNode(txt));if(sub)b.append(mk("small",null,sub));b.onclick=fn;return b}
function jobName(sl){var j=JOBS[jobOf(sl)];return j?j.n:""}
function ask(){box.textContent="";box.append(mk("h3",null,"開始前先設定一下"),mk("p",null,"選好職業，按「編輯減傷」時才會列出對應的技能。"));
  var o=mk("div","opts");
  o.append(btn("排全隊視角","",'設定 8 人職業，排整隊的減傷軸',function(){window.onPartyDone=function(){set("party");done()};document.getElementById("party-btn").click()}));
  o.append(btn("只排個人視角","",'只選自己的職責和職業',solo));box.append(o)}
function solo(){var f=box.querySelector(".solo");if(f){f.remove();return}
  f=mk("div","solo");var sl=document.createElement("select");SLOTS.forEach(function(x){var op=mk("option",null,x);op.value=x;sl.append(op)});
  sl.value=role!=="team"?role.toUpperCase():"ST";var jb=jobSelect(jobOf(sl.value));
  sl.onchange=function(){var n=jobSelect(jobOf(sl.value));jb.replaceWith(n);jb=n};
  f.append(document.createTextNode("我是"),sl,jb,btn("確定","primary",null,function(){var s=sl.value,j=jb.value;
    if(j===DEF_PARTY[s])delete custom.party[s];else custom.party[s]=j;saveCustom();role=s.toLowerCase();set("solo");render();done()}));
  box.append(f)}
function done(){var m=get();box.textContent="";var p=mk("p");
  if(m==="solo"){var me=role!=="team"?role.toUpperCase():"";p.append(mk("b",null,"個人視角"),document.createTextNode("："+(me?"你是 "+me+" "+jobName(me)+"，畫面只顯示你自己的軸。":"")+"按「編輯減傷」開始填。"))}
  else p.append(mk("b",null,"全隊視角"),document.createTextNode("：8 人職業已設定，按「編輯減傷」開始排整隊的軸；上方「職責」可以切換看每個人。"));
  p.append(btn("重新設定","link",null,function(){set(null);ask()}));box.append(p)}
get()?done():ask();
var eb=document.getElementById("edit-btn"),old=eb.onclick;
eb.onclick=function(e){if(!get()&&!editing){box.scrollIntoView({behavior:"smooth",block:"center"});box.classList.remove("flash");void box.offsetWidth;box.classList.add("flash");toastMsg("先選要排全隊視角還是個人視角",2400);return}old.call(this,e)};
})();
</script>"""

def data_block(path, mode):
    subprocess.run(['node', W + 'strip.js', path, W + '_d.js', mode], check=True)
    return open(W + '_d.js', encoding='utf8').read()

def sub_between(s, start, end, new, after=0):
    a = s.index(start, after); b = s.index(end, a) + len(end)
    return s[:a] + new + s[b:]

def make(base, out, *, key_old, key_new, code_old, code_new, exp_old, exp_new,
         title, eyebrow, h1, sub, endnote, data, cur, spans=None, hints=None,
         keep_figs=True, roles_team=True, hint_t=None, alt=()):
    ns={};code=open(W+'tea/build.py',encoding='utf8').read();exec(code[code.index('NAV_CSS='):code.index('# ---- M8S page')],ns);nav=ns['nav']
    s = open(W + base, encoding='utf8').read()
    # nav
    s = re.sub(r'<nav class="sitenav".*?</nav>', nav(cur), s, count=1, flags=re.S)
    # data
    a = s.index('const data = ['); b = s.index('\n];\n', a) + 4
    s = s[:a] + data + s[b:]
    # roles: team only (author per-role pages removed)
    if roles_team:
        if 'const roles={team:{h:"· 全隊"}};' not in s:
            a = s.index('const roles={'); b = s.index('\n};\n', a) + 4
            s = s[:a] + 'const roles={team:{h:"· 全隊"}};\n' + s[b:]
    s = re.sub(r'const HINT_T=\{[^\n]*\};', lambda m: 'const HINT_T=' + json.dumps(hint_t or {}, ensure_ascii=False) + ';', s, count=1)
    if hints is not None:
        a = s.index('const HINTS=['); b = s.index('\n', a) + 1
        s = s[:a] + 'const HINTS=' + json.dumps(hints, ensure_ascii=False) + ';\n' + s[b:]
    if not keep_figs:
        for k in ('const FIG=', 'const FIGMAP=', 'const FIGCAP='):
            if k in s:
                a = s.index(k); b = s.index('\n', a) + 1
                s = s[:a] + k + ('[]' if k == 'const FIGMAP=' else '{}') + ';\n' + s[b:]
    # storage / share code / export name
    s = s.replace('"' + key_old, '"' + key_new).replace(code_old, code_new).replace(exp_old, exp_new)
    s = re.sub(r'const STRAT="[^"]*";', 'const STRAT="";', s, count=1)
    s = re.sub(r'const PALT=\[[^\]]*\];', 'const PALT=' + json.dumps(list(alt)) + ';', s, count=1)
    # header text
    s = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', s, count=1)
    s = re.sub(r'<div class="eyebrow">[^<]*</div>', f'<div class="eyebrow">{eyebrow}</div>', s, count=1)
    s = re.sub(r'<h1>.*?</h1>', f'<h1>{h1} <span id="h-role">· 全隊</span></h1>', s, count=1, flags=re.S)
    s = re.sub(r'<p class="sub">.*?</p>', f'<p class="sub">{sub}</p>' + BLANK_NOTE, s, count=1, flags=re.S)
    s = s.replace('</style>', BLANK_CSS + SETUP_CSS + '</style>', 1)
    s = s.replace(BLANK_NOTE, BLANK_NOTE + '<div class="setup" id="setup" aria-live="polite"></div>', 1)
    s = s.replace('ok.onclick=()=>partyPop.hidden=true;', 'ok.onclick=()=>{partyPop.hidden=true;window.onPartyDone&&window.onPartyDone()};', 1)
    assert 'window.onPartyDone' in s
    i = s.rindex('</script>') + len('</script>')
    s = s[:i] + SETUP_JS.replace('__KEY__', key_new) + s[i:]
    s = re.sub(r'<p class="endnote">.*?</p>', f'<p class="endnote">{endnote}</p>', s, count=1, flags=re.S)
    s = re.sub(r'\s*<p class="thanks">.*?</p>', '', s, flags=re.S)
    # spans
    if spans is not None:
        s = re.sub(r'\n\s*<button id="s-\d+" data-span="\d+"[^>]*>[^<]*</button>', '', s)
        btns = ''.join(f'\n      <button id="s-{i}" data-span="{i}" aria-pressed="false">{n}</button>' for i, n in enumerate(spans, 1))
        s = s.replace('<button id="s-all" data-span="all" aria-pressed="true">全部</button>',
                      '<button id="s-all" data-span="all" aria-pressed="true">全部</button>' + btns, 1)
        sp = '{all:"全部",' + ','.join(f'"{i}":"{n}"' for i, n in enumerate(spans, 1)) + '}'
        s = re.sub(r'sp=\{all:"全部"[^}]*\}', 'sp=' + sp, s, count=1)
        if not spans:
            s = s.replace('<div class="bar" role="group" aria-label="範圍">', '<div class="bar" role="group" aria-label="範圍" hidden>', 1)
    # release notes
    a = s.index('    <ol>', s.index('id="release"')); b = s.index('    </ol>', a) + len('    </ol>')
    s = s[:a] + '    <ol>\n      <li><b>v1.0</b><time>11/20</time><ul><li>空白筆記上線：Boss 技能時間軸＋機制標籤</li><li>減傷、站位、筆記自己填，可匯出匯入</li></ul></li>\n    </ol>' + s[b:]
    s = re.sub(r'<span>最新 v[0-9.]+・[0-9/]+</span>', '<span>最新 v1.0・11/20</span>', s, count=1)
    s = re.sub(r'const VER="v[0-9.]+";', 'const VER="v1.0";', s, count=1)
    open(W + out, 'w', encoding='utf8').write(s)
    print(out, len(s))

CB = '時間照 cactbot 的時間軸換算（以開怪為 00:00），技能名稱用 cactbot 的繁中服翻譯。實際時間會隨打速前後差幾秒。'

# ---- M8S blank (from author page) ----
make('m8s.html', 'm8s-blank.html', key_old='m8s-', key_new='m8sb-', code_old='M8S1:', code_new='M8SB1:', alt=['M8S1:'],
     exp_old='M8S時間軸_', exp_new='M8S空白筆記_',
     title='M8S 空白筆記', eyebrow='AAC Cruiserweight M4 Savage · 呼嘯之劍 · 空白筆記',
     h1='M8S 空白筆記', sub='每一行是 Boss 技能的判定時間，圈數字是這招第幾次出現。門神狼頭之後的時間會隨打速前後差幾秒。',
     endnote='時間照 cactbot 的 M8S 時間軸換算。預設的 # 機制標籤沿用版主筆記（MMW、蘇帕的打法），打法不同可以在編輯模式自己改。「看圖」的站位圖取自猫猫窝攻略组的機制速覽。',
     data=data_block(W + 'm8s.html', 'strip'), cur='m8s-blank.html')

# ---- TEA blank ----
make('tea.html', 'tea-blank.html', key_old='tea-', key_new='teab-', code_old='TEA1:', code_new='TEAB1:', alt=['TEA1:'],
     exp_old='絕亞時間軸_', exp_new='絕亞空白筆記_',
     title='絕亞 空白筆記', eyebrow='The Epic of Alexander (Ultimate) · 絕亞歷山大討滅戰 · 空白筆記',
     h1='絕亞 空白筆記', sub='每個階段各自從 00:00 算起：P1 從開怪、P1.5 從第一發照準、P2 從 Boss 可選中、P3 從時停、P4 從終審判決讀條。時間會隨打速前後差幾秒。',
     endnote='時間照 cactbot 的絕亞時間軸換算，技能名稱照國服翻譯轉繁體，繁中服可能略有不同。預設的 # 機制標籤沿用版主筆記（ふうcだよ、ぬけまる、魚子醬的攻略影片），打法不同可以在編輯模式自己改。',
     data=data_block(W + 'tea.html', 'strip'), cur='tea-blank.html')

# ---- M5S blank (new raid) ----
make('tea.html', 'm5s.html', key_old='tea-', key_new='m5sb-', code_old='TEA1:', code_new='M5SB1:',
     exp_old='絕亞時間軸_', exp_new='M5S空白筆記_',
     title='M5S 空白筆記', eyebrow='AAC Cruiserweight M1 Savage · 阿卡狄亞零式登天鬥技場 中重量級1 · 空白筆記',
     h1='M5S 空白筆記', sub='每一行是 Boss 技能的判定時間（以開怪為 00:00），圈數字是這招第幾次出現。',
     endnote='時間照 cactbot 的時間軸換算（以開怪為 00:00），技能名稱對照繁中服攻略站（FF14 繁中高難攻略）。預設的 # 機制標籤是本站整理的機制說明，不是照特定攻略組的打法，可以在編輯模式自己改。實際時間會隨打速前後差幾秒。', data=data_block(W + 'm5s/data.js', 'keep'), cur='m5s.html', spans=[],
     hints=json.load(open(W + 'm5s/hints.json', encoding='utf8')), keep_figs=False)

# ---- M1S–M4S, M6S, M7S blank (auto from cactbot) ----
AUTO = [('m1s', 'M1S', '黑貓', 'AAC Light-heavyweight M1 Savage · 阿卡狄亞零式登天鬥技場 輕重量級1',
         '中段「暴風裂／剪指甲」兩種順序隨機，這裡照其中一種排。'),
        ('m2s', 'M2S', '蜂蜂小甜心', 'AAC Light-heavyweight M2 Savage · 阿卡狄亞零式登天鬥技場 輕重量級2', ''),
        ('m3s', 'M3S', '野蠻炸彈', 'AAC Light-heavyweight M3 Savage · 阿卡狄亞零式登天鬥技場 輕重量級3', ''),
        ('m4s', 'M4S', '狡雷', 'AAC Light-heavyweight M4 Savage · 阿卡狄亞零式登天鬥技場 輕重量級4', '轉場後的時間會隨打速前後差幾秒。'),
        ('m6s', 'M6S', '糖彩狂潮', 'AAC Cruiserweight M2 Savage · 阿卡狄亞零式登天鬥技場 中重量級2', '小怪階段的時間會隨打速前後差幾秒。'),
        ('m7s', 'M7S', '野蠻憎惡', 'AAC Cruiserweight M3 Savage · 阿卡狄亞零式登天鬥技場 中重量級3', '')]
for lab, up, boss, eb, extra in AUTO:
    _mp = W + lab + '/meta.json'
    _ph = json.load(open(_mp))['phases'] if os.path.exists(_mp) else []
    if len(_ph) > 1:
        extra = '分成 ' + '、'.join(_ph) + '，每段各自從 00:00 算起（之後每段從該段的第一招算）。' + extra
    make('tea.html', lab + '.html', key_old='tea-', key_new=lab + 'b-', code_old='TEA1:', code_new=up + 'B1:',
         exp_old='絕亞時間軸_', exp_new=up + '空白筆記_',
         title=up + ' 空白筆記', eyebrow=eb + ' · 空白筆記', h1=up + ' 空白筆記',
         sub='每一行是 Boss 技能的判定時間（以開怪為 00:00），圈數字是這招第幾次出現，（×N）是連續打 N 下。' + extra,
         endnote='時間軸、技能名稱和死刑／AOE／分攤等 # 標籤都是從 cactbot 的時間軸和觸發器自動整理的，不是照特定攻略組的打法；技能名稱用 cactbot 的繁中服翻譯。實際時間會隨打速前後差幾秒。',
         data=data_block(W + lab + '/data.js', 'keep'), cur=lab + '.html', spans=_ph if len(_ph) > 1 else [], hints=[], keep_figs=False,
         hint_t=json.load(open(W + lab + '/hint_t.json', encoding='utf8')))

# ---- ultimates + AAC heavyweight (auto from cactbot, gen2.py) ----
AUTO2 = [('ucob', '絕巴哈', 'The Unending Coil of Bahamut (Ultimate)'),
         ('uwu', '絕神兵', "The Weapon's Refrain (Ultimate)"),
         ('dsr', '絕龍詩', "Dragonsong's Reprise (Ultimate)"),
         ('top', '絕歐米茄', 'The Omega Protocol (Ultimate)'),
         ('fru', '絕伊甸', 'Futures Rewritten (Ultimate)'),
         ('dmu', 'Dancing Mad', 'Dancing Mad (Ultimate) · 凱夫卡'),
         ('m9s', 'M9S', 'AAC Heavyweight M1 Savage · 致命美人'),
         ('m10s', 'M10S', 'AAC Heavyweight M2 Savage · 極限兄弟'),
         ('m11s', 'M11S', 'AAC Heavyweight M3 Savage · 霸王'),
         ('m12s', 'M12S', 'AAC Heavyweight M4 Savage · 林德布魯姆'),
         ('necronx', '極永恆黑暗', "The Minstrel's Ballad: Necron's Embrace · 7.3 極神")]
for lab, nm, eb in AUTO2:
    meta = json.load(open(W + lab + '/meta.json'))
    cn = meta['loc'] == 'cn'
    ph = meta['phases']
    sub = ('每個 P 各自從 00:00 算起（P1 從開怪，之後每個 P 從該 P 的第一招算），' if len(ph) > 1 else '每一行是 Boss 技能的判定時間（以開怪為 00:00），') + \
          '圈數字是這招第幾次出現，（×N）是連續打 N 下。有隨機分支的地方只列其中一種順序。'
    end = ('時間軸、技能名稱和死刑／AOE／分攤等 # 標籤都是從 cactbot 的時間軸和觸發器自動整理的，不是照特定攻略組的打法；' +
           ('技能名稱是國服翻譯轉繁體（繁中服還沒開這個副本），之後繁中服的名稱可能不同。' if cn else '技能名稱用 cactbot 的繁中服翻譯。') +
           '實際時間會隨打速前後差幾秒。')
    up = lab.upper()
    make('tea.html', lab + '.html', key_old='tea-', key_new=lab + 'b-', code_old='TEA1:', code_new=up + 'B1:',
         exp_old='絕亞時間軸_', exp_new=nm.replace(' ', '') + '空白筆記_',
         title=nm + ' 空白筆記', eyebrow=eb + ' · 空白筆記', h1=nm + ' 空白筆記', sub=sub, endnote=end,
         data=data_block(W + lab + '/data.js', 'keep'), cur=lab + '.html', spans=ph if len(ph) > 1 else [],
         hints=json.load(open(W + lab + '/hints.json', encoding='utf8')) if os.path.exists(W + lab + '/hints.json') else [], keep_figs=False,
         hint_t=json.load(open(W + lab + '/hint_t.json', encoding='utf8')))

# author pages accept codes/files from their blank versions
for f, a in [('m8s.html', 'M8SB1:'), ('tea.html', 'TEAB1:')]:
    t = open(W + f, encoding='utf8').read()
    assert t.count('const PALT=[];') == 1, f
    open(W + f, 'w', encoding='utf8').write(t.replace('const PALT=[];', 'const PALT=["%s"];' % a))

