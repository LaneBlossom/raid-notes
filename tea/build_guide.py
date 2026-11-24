import re, json, sys
sys.path.insert(0,'/home/claude/work/tea')
from figs import FIGS, FIGMAP
D='/home/claude/work/'
sys.path.insert(0,D+'tea')
src=open(D+'tea-guide.orig.html',encoding='utf8').read()
data=json.load(open(D+'tea/data.json',encoding='utf8'))
H=json.load(open(D+'tea/hints.json',encoding='utf8'))
HT={"01:48":["換T"]}
ns={}
code=open(D+'tea/build.py',encoding='utf8').read()
exec(code[code.index("NAV_CSS="):code.index("# ---- M8S page")],ns)
NAV_CSS,nav=ns['NAV_CSS'],ns['nav']

# ---------- nav ----------
s=src
a=s.index('<nav class="sitenav"'); b=s.index('</nav>',a)+6
s=s[:a]+nav('tea-guide.html')+s[b:]
a=s.index('.sitenav{'); b=s.index('</style>',a)
s=s[:a]+NAV_CSS+s[b:]

# ---------- header ----------
s=s.replace('<title>絕亞 ST 騎士攻略</title>','<title>絕亞 繁中攻略整合</title>',1)
s=s.replace('<h1>絕亞 ST 騎士攻略</h1>','<h1>絕亞 繁中攻略整合</h1>',1)
s=s.replace('<p class="lede">每個階段只整理 ST 的跑位、要注意的細節，以及減傷和團減的時機。',
 '<p class="lede">每個階段依序是：<b>ST 一圖流</b>（P3、P4：騎士這段要跑哪、開什麼）、<b>機制與解法</b>（每個機制一張卡，點開看說明、示意圖和原影片截圖）、<b>時間軸</b>（含團減軸總表），每一塊都能單獨收起或展開。以 ST 騎士視角整理。',1)

MITS=["通用減","資源減","大減","鐵壁","聖盾陣","極致護衛","壁壘","神聖領域","預警","干預","盾陣","武裝戍衛","聖光幕簾","雪仇","全減傷"]
def ismit(x): return any(k in x for k in MITS)
POIRE=re.compile(r'^(一傳|二傳|三傳|疫苗|終審)')
def tags(r):
    t=[v for k,v in H if k in r['m'] and not POIRE.match(v)]+HT.get(r['t'],[])
    out=[]
    for x in t:
        if x not in out: out.append(x)
    return out

# burst column (guide P1 is sourced; others are general timings, flagged)
BURST={
 (0,"00:20"):('ST：瀑布讀條時吃藥，落地後爆發全開，約 2.5 GCD 後回去打本體',0),
 (2,"00:00"):('2 分鐘爆發轉好，可選中就開',1),
 (3,"00:11"):('亞歷山大可選中後爆發',1),
 (3,"03:25"):('先殺飛機，正義號疊到 13 層前殺掉；約 7 層起多用能力技',0),
 (4,"00:00"):('開場爆發',1),
}

POI={(2,'00:33'):'一傳（MT、H1、H2、D1、D3、D4）',(2,'00:44'):'一傳（ST、D2）',(2,'01:01'):'二傳',
 (2,'01:26'):'三傳・D 找 TH',(2,'02:05'):'終審排隊・藍橙綠紫',(2,'02:07'):'終審閉庭・疫苗＋同色毒'}
def timeline(pi):
    rows=[];phase=None;idx=-1
    for g in data:
        if g.get('part'): idx+=1
        if idx!=pi: continue
        rows.append(f'<tr class="gh"><th colspan="7">{g["g"]}</th></tr>')
        for r in g['rows']:
            tg=''.join(f'<span class="tag t-hint">{x}</span>' for x in tags(r)) or '—'
            act=[x for x in r.get('st',[]) if not ismit(x)]
            mit_self=[x for x in r.get('st',[]) if ismit(x)]
            team_st=[x[1] for x in r['c'] if x[0]=='ST']
            others=[f'{x[0]} {x[1]}' for x in r['c'] if x[0]!='ST']
            act_h=''.join(f'<span class="tag t-prov">ST</span>{x}<br>' for x in act)
            act_h+=''.join(f'<span class="tag t-mtk">MT</span>{x}<br>' for x in r.get('mt',[]))
            mit_h=''
            if team_st: mit_h+='<span class="tag t-team">團減</span>'+'＋'.join(team_st)+'<br>'
            if mit_self: mit_h+='<span class="tag t-mit">自身</span>'+'＋'.join(mit_self)+'<br>'
            if others: mit_h+='<span class="oth">其他：'+'、'.join(others)+'</span><br>'
            if r.get('nst') and '爆發' not in r['nst']: mit_h+=f'<span class="oth">ST：{r["nst"]}</span>'
            fb=''.join(f'<button type="button" class="figbtn'+(' rofig" data-roles="'+' '.join(x[3])+'"' if len(x)>3 else '"')+f' data-fig="{x[1]}">{x[2]}</button>' for x in FIGMAP if x[0] in r['m'])
            pz=POI.get((pi,r['t']))
            pz_h=(f'<div class="poi"><img src="{IC("vac_a" if "疫苗" in pz else "poison_a")}" alt="" width="18" height="24">{pz}</div>') if pz else ''
            if r.get('poi'):
                pr=''.join(f'<span class="poiro" data-ro="{k}"><b>{k.upper()}：</b>{r["poi"].get(k) or "這次不用傳"}</span>' for k in ['mt','st','h1','h2','d1','d2','d3','d4'])
                pz_h+=f'<div class="poit">{r["poi"]["team"]}<br>{pr}</div>'
            ri=rowicons(r['m'])
            m=pz_h+r['m']+(f'<div class="ics">{ri}</div>' if ri else '')+(f'<div class="fbs">{fb}</div>' if fb else '')+(f'<div class="nt">{r["n"]}</div>' if r.get('n') else '')
            bu=BURST.get((pi,r['t']))
            bu_h=(f'<span class="tag t-burst">爆發</span>{bu[0]}'+('<span class="gen">通用</span>' if bu[1] else '')) if bu else ''
            cl=(['me'] if (team_st or mit_self or act) else [])+(['poirow'] if pz else [])
            trc=f' class="{" ".join(cl)}"' if cl else ''
            rows.append(f'<tr{trc}><td>{r["t"]}</td><td>{m}</td><td>{tg}</td><td>{r.get("pos","")}</td><td>{act_h.rstrip("<br>") if act_h else ""}</td><td class="col-st">{mit_h}</td><td>{bu_h}</td></tr>')
    return ('<div class="tbl"><table class="tline"><thead><tr><th>時間</th><th>機制</th><th>標籤</th><th>站位</th><th>該放的技能</th><th class="col-st">減傷</th><th>爆發</th></tr></thead><tbody>'
            +''.join(rows)+'</tbody></table></div>')

TL_NOTE=['00:00＝開怪。','00:00＝第 1 發照準。','00:00＝Boss 可選中。','00:00＝時停。','00:00＝終審判決讀條。']

MECH={
'p1':'''<ul>
<li><b>生命液體（本體）與手</b>：瀑布落地後本體 HP 減半，手出現。本體和手都會打<b>坦克強攻擊</b>（死刑），兩隻要分開由兩個 T 拿。</li>
<li><b>水柱</b>：西、北、東三個水柱會放扇形，先一次有預兆、再一次無預兆，都要有人引導，不然會打到人群。</li>
<li><b>猜拳</b>：手會出拳，出布時手亮藍光。手要離本體一定距離以上才能猜拳。</li>
<li><b>分離之手、痛苦之手</b>：手會砸地兩次。痛苦之手原本要把本體和手的 HP 打平再吃，否則傷害很高。</li>
<li><b>普羅蒂恩波</b>：無預兆的扇形，跟坦克強攻擊幾乎同時。</li>
<li><b>藍球</b>：痛苦之手後，3 個水柱中有 2 個冒出藍球往本體移動。藍球碰到人偶以外的東西就團滅。</li>
<li><b>獵犬人偶</b>：會放排氣等 2 種範圍攻擊，被範圍技打到會移動。</li>
</ul>''',
'p3':'''<ul>
<li><b>時停</b>：時停結束後飛機劈最近的 3 人、正義號噴最近的 2 人，傷害不能重疊。身上的 debuff（近線、遠線、電＝加重罪、沒點名）決定你要站哪裡。</li>
<li><b>死刑</b>：神罰射線對一仇打一次並附魔法易傷，接著神聖之槍對當下的一仇打三次扇形。單吃要無敵，不然要換 T。</li>
<li><b>一運（時空潛行）</b>：綠球連線、黃圈放結晶；真心變金色後正義號噴火；之後集團罪分攤、飛機三刀、正義號超級跳最遠的人，最後是第二次死刑。</li>
<li><b>淨化熱線＋生命計算法</b>：次元斷絕的最後，淨化熱線（分攤）和生命計算法幾乎同時判定。生命計算法會點 2 個人（頭上讀秒），每個人的圈內要<b>剛好 3 人</b>，多或少都不行。</li>
<li><b>超級神聖（百萬神聖）×2</b>：接著連續兩次全體大傷害，要排團減。</li>
<li><b>火龍捲（J 風暴＋水波）</b>：DPS 檢測。正義號疊到 13 層前要打掉，約 7 層起壓力變大。</li>
<li><b>召喚亞歷山大</b>：火龍捲期間亞歷山大離場，飛機和正義號一起打，飛機先死。</li>
<li><b>神聖審判</b>：P3 轉 P4 的全體大傷害，雙 T 要開盾和減傷吃。</li>
</ul>''',
'p4':'''<ul>
<li><b>終審判決</b>：發 debuff，分成大光、大暗、小光、小暗。大光或大暗死掉會連帶小光或小暗一起死，等於團滅。</li>
<li><b>動靜</b>：禁止命令（靜）要完全不動，連在小隊頻道打字都算違令；行動命令（動）要一直移動或原地一直跳。</li>
<li><b>制導</b>：連續兩次，分散或兩人分攤，順序隨機。</li>
<li><b>加重誅罰＋誅罰</b>：加重誅罰對一仇打 3 次可雙人分攤的圓形死刑；誅罰對一仇打 1 次並附 30 秒物理易傷，所以誅罰前要換 T。全場共三次。</li>
<li><b>未來觀測（一測、二測）</b>：讀條時看自己的影子，影子身上的特效就是你等一下會被點的機制。</li>
<li><b>神聖大審判（地火）</b>：三個位置依序刷地火，要照順序穿過去。</li>
<li><b>株連</b>：隨機點一人的巨大傷害，8 人分攤，要做足減傷。</li>
<li><b>時間干涉（籠子）</b>：籠子依序落下，落下時裡面沒人就團滅。</li>
</ul>''',
}
P2_EXTRA='''<ul>
<li><b>巡航驅逐者（飛機）與殘暴正義號</b>：任一隻死掉另一隻會狂暴，兩隻血量要一起壓。</li>
<li><b>迴旋碎踢</b>：飛機正面扇形擊退。</li>
<li><b>電漿護盾</b>：飛機無敵、正面出盾，大約 3 個 GCD 內要打破，否則狂暴。</li>
<li><b>螺旋槳強風</b>：被打到的人會混亂、秒殺身邊隊友，躲在冰塊後面能擋住。</li>
</ul>'''

# which sections (by h2 title prefix) go where; others -> solution
MECH_SEC={'機制講解','機制重點（ST 要懂的部分）','次元斷絕（34 固定法）機制講解'}
TL_SEC=lambda t:t.startswith('ST 減傷') or t=='P1 全機制時間軸'
DROP={'P1 全機制時間軸'}


import base64 as _b64
def IC(k): return 'data:image/png;base64,'+_b64.b64encode(open(D+f'tea/icons/{k}.png','rb').read()).decode()
def db(sym,bg,name,desc,fg='#fff',shape='sq',icon=None):
    if icon:
        ic=''.join(f'<img class="dbimg" src="{IC(k)}" alt="" width="24" height="32">' for k in icon.split())
        return f'<li><span class="dbis">{ic}</span><span><b>{name}</b>　{desc}</span></li>'
    return (f'<li><span class="dbi dbi-{shape}" style="background:{bg};color:{fg}" aria-hidden="true">{sym}</span>'
            f'<span><b>{name}</b>　{desc}</span></li>')
DEBUFF={
 'p1':[db('','','水屬性耐性降低','液體擺動（死刑）打完附上。吃到的 T 不能再吃普羅蒂恩波，否則要無敵',icon='waterdown'),
       db('','','窒息（Throttle）','6 個人被點，要用康復或光神曲解掉，否則時間到會死',icon='throttle')],
 'p15':[db('1','#2f6bd8','頭上號碼 1～8','追擊者出現的順序（藍點奇數、紅點偶數）。奇數吃阿爾法之劍（扇形），偶數吃超級衝擊（突進擊退）')],
 'p2':[db('','','最終判決（毒）α 藍・β 橙・γ 紫・δ 綠','一開始給 4 DPS 或 2T2H。碰到不同色會死，碰到沒毒的人會傳過去。終審排隊順序是藍 → 橙 → 綠 → 紫',icon='poison_a poison_b poison_c poison_d'),
       db('','','疫苗（右下有驚嘆號）','終審開庭後 8 人都會拿到一種顏色。終審閉庭時要有疫苗＋同色毒，否則團滅',icon='vac_a vac_b vac_c vac_d'),
       db('','','水分攤／雷分攤點名','雷 2 人分攤、水 3～4 人分攤，攤完原地留下水龍捲',icon='cwater clight'),
       db('','','水易傷／雷易傷','吃過那個屬性的分攤，下一次同屬性不能再吃',icon='waterdown lightdown'),
       db('','','混亂','被螺旋槳強風打到會混亂、秒殺身邊隊友，躲在冰塊後面就能擋住',icon='confused')],
 'p3':[db('','','時停','身上的 debuff 決定站位，時停期間不能動',icon='temporal'),
       db('','','近線（House Arrest）','綠紅箭頭朝內。到飛機和正義號中間、右邊 boss 正上方，跟連線的人靠近',icon='house'),
       db('','','遠線（Restraining Order）','藍色箭頭朝外。到場地正左（9 點），跟連線的人拉開',icon='restrain'),
       db('','','加重罪（電）','到正義號那側貼邊，判定前不能再吃任何傷害',icon='aggr'),
       db('—','#9aa4b8','沒點名','到左邊 boss 上方'),
       db('','','集團罪','和雙 T 一起三人分攤',icon='shared'),
       db('','','魔法易傷','神罰射線打完附上，所以死刑要無敵或換 T',icon='magvuln'),
       db('1','#2f6bd8','頭上號碼 1～8','次元斷絕的骰子號碼，奇數在左、偶數在右')],
 'p4':[db('','','大光（Contact Regulation）','橙色光芒，1 人。到 A 點方向盡量貼邊。死掉會連帶小光一起死',icon='lightbig'),
       db('','','小光（Contact Prohibition）','黃色箭頭，3 人。開場到 C 點上方集合',icon='lightsmall'),
       db('','','大暗（Escape Detection）','紫色，1 人。站 C 點正中。死掉會連帶小暗一起死',icon='darkbig'),
       db('','','小暗（Escape Prohibition）','藍白箭頭，3 人。開場到 C 點上方，盡量靠近大暗',icon='darksmall'),
       db('靜','#c2533a','禁止命令（靜）','boss 讀條，不是 debuff。讀條過半前按 ESC 取消選中，然後完全不動'),
       db('動','#3f8f6b','行動命令（動）','boss 讀條，不是 debuff。一直移動，或原地一直跳'),
       db('','','物理易傷','誅罰打完附上（30 秒），所以誅罰前要換 T',icon='physvuln'),
       db('影','#5b6475','未來觀測的影子','看自己影子身上的特效，就是等一下會被點的機制')],
}
ICONMAP=[["液體擺動","waterdown"],["最終判決（上毒）","poison_a poison_b poison_c poison_d"],["水雷分攤","cwater clight"],
 ["螺旋槳強風","confused"],["時停判定","house restrain aggr"],["神罰射線","magvuln"],["集團罪","shared"],
 ["誅罰（","physvuln"],["終審判決","lightbig lightsmall darkbig darksmall"],["時停","temporal"]]
def rowicons(m):
    ks=[]
    for kw,v in ICONMAP:
        if kw in m and not (kw=="時停" and m!="時停"):
            ks+= [k for k in v.split() if k not in ks]
    return ''.join(f'<img class="rowic" src="{IC(k)}" alt="" width="18" height="24">' for k in ks)
def dbbox(pid):
    if pid not in DEBUFF: return ''
    return ('<div class="dbox"><div class="dbh">要看的 debuff／buff</div><ul class="dbl">'+''.join(DEBUFF[pid])+
            '</ul><p class="dbn">狀態圖示取自遊戲（FFXIV Wiki）；色塊的是讀條或頭上標記，沒有狀態圖示。</p></div>')

def blk(n,title,inner,pid):
    return (f'<details class="blk" id="{pid}-b{n}" open><summary class="bh"><span class="bn">{n}</span><span class="bt">{title}</span><span class="chev" aria-hidden="true"></span></summary>'
            f'<div class="bb">{inner}</div></details>')

POIJ=json.load(open(D+'tea/poison.json',encoding='utf8'))
def poitable():
    cols=[('00:33','一傳'),('00:44','一傳（ST／D2）'),('01:01','二傳'),('01:26','三傳'),('02:05','終審')]
    roles=['mt','st','h1','h2','d1','d2','d3','d4']
    head='<tr><th>職位</th>'+''.join(f'<th>{n}<span class="pw">{POIJ[t]["when"]}</span></th>' for t,n in cols)+'</tr>'
    body=''
    for ro in roles:
        cells=''
        for t,n in cols:
            v=POIJ[t].get(ro)
            if t=='00:33' and ro in('st','d2'): v='等碎踢讀條（看下一欄）'
            if t=='00:44' and ro not in('st','d2'): v='—'
            cells+=f'<td>{v or "—"}</td>'
        body+=f'<tr data-ro="{ro}"><th>{ro.upper()}</th>{cells}</tr>'
    chips=''.join(f'<button type="button" class="rochip" data-ro="{r}">{r.upper()}</button>' for r in roles)
    return ('<section class="step nofig"><div><h3 class="sh">各職位傳毒對照</h3>'
            '<p>點自己的職位，整行會亮起來，下面時間軸的傳毒提示也會換成你的（會記住你的選擇）。</p>'
            f'<div class="rochips" role="group" aria-label="選職位">{chips}</div>'
            f'<div class="tbl"><table class="poitbl"><thead>{head}</thead><tbody>{body}</tbody></table></div></div></section>')

import importlib.util as _iu
_sp=_iu.spec_from_file_location('dimpaths',D+'tea/dimpaths.py');_dm=_iu.module_from_spec(_sp);_sp.loader.exec_module(_dm)
_sp=_iu.spec_from_file_location('stpaths',D+'tea/stpaths.py');_st=_iu.module_from_spec(_sp);_sp.loader.exec_module(_st)
def _inner(sec_html):
    m=re.search(r'<section[^>]*>\s*<div>(.*)</div>\s*</section>\s*$',sec_html.strip(),flags=re.S)
    return m.group(1) if m else sec_html
def _svgfig(svg,cap):
    return f'<figure class="dfig">{svg}<figcaption>{cap}</figcaption></figure>'
# self-drawn diagrams per mechanic card (title prefix -> list of (svg, caption))
DIAG={
 '時停（依身上的 debuff 站位':[(_st.p_timestop(),'時停 T 奶組站位（依 debuff）')],
 '一運（時空潛行）':[(_st.p_flame(),'噴火引導：雙 T 位置'),(_st.p_stack(),'集團罪：雙 T 左邊分攤'),(_st.p_jump(),'超級跳：ST 到 B 點貼邊')],
 '淨化熱線＋生命計算法':[(_st.p_final(),'上下兩組各 3 人')],
 '開場：終審判決＋動靜':[(_st.p4_open(),'終審判決站位'),(_st.p4_guide(),'制導分散：T、補往上')],
}
def mcard(sec,pid,idx,extra_html='',extra_shots=''):
    title=re.search(r'<h[23][^>]*>(.*?)</h[23]>',sec).group(1)
    inner=_inner(sec)
    inner=re.sub(r'<h[23][^>]*>.*?</h[23]>','',inner,count=1)
    gals=re.findall(r'<div class="vgal">.*?</figure></div>',inner,flags=re.S)
    for g in gals: inner=inner.replace(g,'')
    shots=''.join(gals)+extra_shots
    nshot=shots.count('<figure class="vfig"')
    diag=''
    for k,v in DIAG.items():
        if title.startswith(k): diag='<div class="dgrid">'+''.join(_svgfig(s_,c) for s_,c in v)+'</div>'
    badges=(f'<span class="mbadge">圖解</span>' if (diag or extra_html) else '')+(f'<span class="mbadge m2">截圖 {nshot}</span>' if nshot else '')
    figs_=''.join(re.findall(r'<figure class="vfig">.*?</figure>',shots,flags=re.S))
    shots_h=(f'<details class="shots"><summary>原影片截圖（{nshot} 張）</summary><div class="vgal">{figs_}</div></details>') if nshot else ''
    return (f'<details class="mcard" id="{pid}-m{idx}"><summary><span class="mt">{title}</span>{badges}<span class="mchev" aria-hidden="true"></span></summary>'
            f'<div class="mbody">{inner}{diag}{extra_html}{shots_h}</div></details>')

for pi,pid in enumerate(['p1','p15','p2','p3','p4']):
    a=s.index(f'<section class="panel" id="panel-{pid}"')
    nxt=[s.find(f'<section class="panel" id="panel-{q}"') for q in ['p15','p2','p3','p4'] if s.find(f'<section class="panel" id="panel-{q}"')>a]
    b=min(nxt) if nxt else s.index('<p class="src">參考影片')
    panel=s[a:b]
    head=panel[:panel.index('<section class="step')]
    secs=re.findall(r'\s*<section class="step[^"]*">.*?</section>',panel,flags=re.S)
    tail=panel[panel.rindex('</section>'):]
    mech=[];sol=[];tl=[];mit=[]
    dim_shots=''
    for sec in secs:
        title=re.search(r'<h2>(.*?)</h2>',sec).group(1)
        sec=sec.replace('<h2>','<h3 class="sh">',1).replace('</h2>','</h3>',1)
        if title in DROP: continue
        if title.startswith('次元斷絕：原影片截圖'):
            dim_shots=''.join(re.findall(r'<div class="vgal">.*?</figure></div>',sec,flags=re.S)); continue
        if title.startswith('團減軸'): mit.append(sec)
        elif title in MECH_SEC and not title.startswith('次元斷絕'): mech.append(sec)
        elif TL_SEC(title): tl.append(sec)
        else: sol.append(sec)
    mech_h=MECH.get(pid,'')
    if pid=='p2': mech_h=''.join(_inner(x) for x in mech)+P2_EXTRA; mech=[]
    # P1: lift the direction box
    pre=[]
    if pid=='p1':
        m=re.search(r'\s*<p class="skill"[^>]*><b>方向：</b>.*?</p>',head,flags=re.S)
        head=head.replace(m.group(0),'')
        pre.append('<section class="step nofig"><div><h3 class="sh">打法與方向</h3>'+m.group(0).strip().replace(' style="margin-top:8px"','')+
          '<p style="margin-top:8px">完全不管獵犬人偶，也不打平本體和手的血量，只打本體，約 1:09 轉場。</p></div></section>')
    cards=[]
    # overview card: debuff box + mechanic summary
    ov=dbbox(pid)+(mech_h and f'<div class="mov">{mech_h}</div>')+''.join(_inner(x) for x in mech)
    if ov.strip():
        cards.append(f'<details class="mcard" id="{pid}-m0" open><summary><span class="mt">機制速覽</span><span class="mbadge m3">先看這張</span><span class="mchev" aria-hidden="true"></span></summary><div class="mbody">{ov}</div></details>')
    for i,sec in enumerate(pre+sol,1):
        t=re.search(r'<h3[^>]*>(.*?)</h3>',sec).group(1)
        if t.startswith('次元斷絕'):
            cards.append(mcard(sec,pid,i,extra_html=_dm.section().split('</style>',1)[0]+'</style><h4 class="dsub" id="dimpaths">1～8 號跑位一圖流</h4>'+_inner(_dm.section().split('</style>',1)[1]).replace('<h3 class="sh">次元斷絕：1～8 號跑位一圖流</h3>','').replace('id="dimpaths"','id="dimpaths-sec"'),extra_shots=dim_shots))
        else:
            cards.append(mcard(sec,pid,i))
    if pid=='p2': cards.append(f'<details class="mcard" id="{pid}-mpoi"><summary><span class="mt">各職位傳毒對照</span><span class="mchev" aria-hidden="true"></span></summary><div class="mbody">'+_inner(poitable()).replace('<h3 class="sh">各職位傳毒對照</h3>','')+'</div></details>')
    tools='<div class="mtools"><button type="button" data-cards="open">展開全部機制</button><button type="button" data-cards="close">全部收起</button></div>'
    blocks=[]
    if pid in ('p3','p4'):
        sec=_st.section() if pid=='p3' else _st.section_p4()
        css_part=sec.split('</style>',1)[0]+'</style>' if '<style>' in sec else ''
        body=_inner(sec.split('</style>',1)[1] if '<style>' in sec else sec)
        body=re.sub(r'<h3 class="sh">[^<]*</h3>','',body,count=1)
        blocks.append(('ST 一圖流',css_part+body))
    blocks.append(('機制與解法',tools+'<div class="mlist">'+''.join(cards)+'</div>'))
    mit_h=(f'<details class="shots mitsum"><summary>團減軸總表（只看團減的話看這張）</summary>'+''.join(_inner(x).replace('<h3 class="sh">','<h3 class="sh" hidden>',1) for x in mit)+'</details>') if mit else ''
    tl_h=(f'<p class="src">{TL_NOTE[pi]}時間是技能判定時間，會隨打速前後差幾秒。<span class="tag t-team">團減</span>＝ST 給全隊的，<span class="tag t-mit">自身</span>＝ST 自己的；淡藍底的行是 ST 要按東西的地方。爆發欄標<span class="gen">通用</span>的是攻略沒寫、一般打法的時機，跟團確認。</p>'
          +mit_h+timeline(pi)+''.join(tl))
    blocks.append(('時間軸',tl_h))
    jump=(f'<div class="jump" role="group" aria-label="跳到">'+''.join(
        f'<button type="button" data-go="{pid}-b{n}">{t}</button>' for n,(t,_) in enumerate(blocks,1))+'<span class="jsp"></span><button type="button" data-all="open">全部展開</button><button type="button" data-all="close">全部收合</button></div>')
    newp=head.rstrip()+'\n'+jump+'\n'+'\n'.join(blk(n,t,h,pid) for n,(t,h) in enumerate(blocks,1))+'\n  '
    s=s[:a]+newp+tail+s[b:]

CSS='''
.mtools{display:flex;gap:6px;justify-content:flex-end;margin:2px 0 8px}
.mtools button{font:inherit;font-size:.8rem;padding:4px 10px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--fg);cursor:pointer}
.mlist{display:flex;flex-direction:column;gap:8px}
details.mcard{border:1px solid var(--line);border-radius:12px;background:var(--surface,transparent);overflow:hidden}
details.mcard>summary{list-style:none;display:flex;align-items:center;gap:8px;padding:11px 14px;cursor:pointer;font-weight:700}
details.mcard>summary::-webkit-details-marker{display:none}
details.mcard>summary:hover{background:color-mix(in srgb,var(--accent,#7aa6ff) 8%,transparent)}
details.mcard>summary:focus-visible{outline:2px solid var(--accent,#7aa6ff);outline-offset:-2px}
.mcard .mt{flex:1;min-width:0}
.mbadge{font-size:.7rem;font-weight:700;padding:1px 7px;border-radius:999px;background:color-mix(in srgb,var(--accent,#7aa6ff) 18%,transparent);color:var(--accent,#7aa6ff);white-space:nowrap}
.mbadge.m2{background:color-mix(in srgb,var(--muted) 18%,transparent);color:var(--muted)}
.mbadge.m3{background:color-mix(in srgb,#e8bf4a 22%,transparent);color:#c99a1c}
.mchev{width:8px;height:8px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .15s;margin:0 4px 3px 4px}
details.mcard:not([open]) .mchev{transform:rotate(-45deg);margin-bottom:0}
.mbody{padding:2px 16px 14px;border-top:1px solid var(--line)}
.mbody>ul,.mbody>p{margin:10px 0}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:10px 0}
.dfig{margin:0;border:1px solid var(--line);border-radius:10px;padding:8px}
.dfig svg{width:100%;height:auto;display:block;color:var(--muted)}
.dfig figcaption{font-size:.8rem;color:var(--muted);text-align:center;margin-top:4px}
.dsub{margin:14px 0 4px;font-size:.95rem}
details.shots{margin-top:12px;border-top:1px dashed var(--line);padding-top:8px}
details.shots>summary{cursor:pointer;font-size:.85rem;color:var(--muted);font-weight:700;width:max-content}
details.shots>summary:hover{color:var(--fg)}
details.shots .vgal{margin-top:8px}
details.mitsum{margin:4px 0 12px;border-top:0;padding-top:0}
details.mitsum>summary{font-size:.9rem}
.mov ul{margin:6px 0}

.blk{display:flex;flex-direction:column;gap:4px;padding-top:6px}
.bh{display:flex;align-items:center;gap:10px;font-family:var(--f-display);font-weight:700;font-size:1.35rem;padding:10px 0 6px;border-bottom:2px solid var(--st);margin:0;cursor:pointer;list-style:none;user-select:none}
.bh::-webkit-details-marker{display:none}
.bh:hover .bt{color:var(--st)}
.bh:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.chev{margin-left:auto;width:10px;height:10px;border-right:2.5px solid var(--muted);border-bottom:2.5px solid var(--muted);transform:rotate(45deg);transition:transform .15s}
details.blk:not([open]) .chev{transform:rotate(-45deg)}
details.blk:not([open]) .bh{border-bottom-color:var(--line)}
details.blk>.bb{padding-top:4px}
.jsp{flex:1}
.bn{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--st);color:var(--surface);font-family:var(--f-body);font-size:.95rem}
.bb{display:flex;flex-direction:column;gap:18px}
.bb>.step:first-child{border-top:0;padding-top:12px}
.sh{font-family:var(--f-display);font-size:1.15rem;margin:0 0 6px;text-wrap:balance}
.jump{display:flex;flex-wrap:wrap;gap:6px}
.jump button{font:inherit;font-size:.85rem;font-weight:700;padding:4px 12px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
.jump button:hover{border-color:var(--st)}
.wrap{max-width:1160px!important}
.lede,.step>div>p,.step>div>ul{max-width:80ch}
table.tline{min-width:1040px;table-layout:fixed}
table.tline th:nth-child(1){width:66px}table.tline th:nth-child(2){width:180px}table.tline th:nth-child(3){width:110px}
table.tline th:nth-child(4){width:230px}table.tline th:nth-child(5){width:150px}table.tline th:nth-child(6){width:170px}table.tline th:nth-child(7){width:150px}
table.tline tr.gh th{background:color-mix(in srgb,var(--fg) 8%,transparent);color:var(--fg);font-weight:700;padding:6px 8px}
table.tline tr.me td{background:color-mix(in srgb,var(--st) 7%,transparent)}
table.tline tr.me td.col-st{background:color-mix(in srgb,var(--st) 14%,transparent)}
.nt{font-size:.8rem;color:var(--muted);margin-top:2px}
.oth{font-size:.8rem;color:var(--muted)}
.t-hint{background:var(--surface);color:var(--fg);border:1px solid var(--line)}
.t-team{background:#2f8f8a}.t-mtk{background:var(--mt)}
.fbs{display:flex;flex-wrap:wrap;gap:4px;margin-top:3px}
.figbtn{font:inherit;font-size:.72rem;font-weight:700;padding:0 8px;border-radius:999px;border:1px solid var(--accent);background:transparent;color:var(--accent);cursor:pointer;line-height:1.7}
.figbtn:hover,.figbtn:focus-visible,.figbtn[aria-expanded="true"]{background:var(--accent);color:var(--surface);outline:none}
.figpop{position:fixed;z-index:30;background:#111;border-radius:12px;padding:6px;box-shadow:0 12px 32px rgba(0,0,0,.4);max-width:min(600px,calc(100vw - 24px))}
.figpop img,.figpop svg{display:block;width:auto;height:auto;max-width:min(588px,calc(100vw - 36px));max-height:min(64vh,520px);border-radius:8px}
.figpop svg{width:min(420px,calc(100vw - 36px));background:#fff}
.figpop p{color:#ddd;font-size:.75rem;margin:5px 4px 1px}
.dbox{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-top:12px}
.dbh{font-weight:700;font-size:.9rem;color:var(--muted);margin-bottom:6px}
.dbl{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(380px,100%),1fr));gap:8px 22px}
.dbl li{display:flex;gap:9px;align-items:flex-start;font-size:.88rem;line-height:1.55}
.dbi{flex:0 0 auto;display:inline-grid;place-items:center;width:24px;height:24px;font-size:.78rem;font-weight:800;border-radius:5px;box-shadow:inset 0 0 0 1.5px rgba(0,0,0,.25);margin-top:1px}
.dbi-circle{border-radius:50%}
.dbis{flex:0 0 auto;display:flex;gap:2px}
.dbimg{display:block;width:24px;height:32px}
.ics{display:flex;flex-wrap:wrap;gap:2px;margin-top:3px}
.rowic{display:block;width:18px;height:24px}
.dbn{font-size:.75rem;color:var(--muted);margin-top:8px}
.vgal{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr));gap:14px;margin-top:14px;max-width:none}
figure.vfig{margin:0;padding:8px;display:flex;flex-direction:column}
.vfig img{display:block;width:100%;height:auto;border-radius:6px}
.vfig figcaption{font-size:.85rem;line-height:1.55;color:var(--fg);margin-top:6px}
.vsrc{display:block;font-size:.72rem;color:var(--muted);margin-top:2px}
.poi{display:flex;width:fit-content;align-items:center;gap:5px;font-size:.8rem;font-weight:800;color:#fff;background:#7a3fc4;border-radius:6px;padding:2px 8px 2px 4px;margin-bottom:4px}
.poi img{width:14px;height:19px}
table.tline tr.poirow td:first-child{box-shadow:inset 4px 0 0 #7a3fc4}
table.tline tr.poirow td{background:color-mix(in srgb,#7a3fc4 8%,transparent)}
.poit{font-size:.78rem;line-height:1.5;color:var(--fg);margin:2px 0 4px}
.poiro{display:none;font-weight:700}
.poiro.on{display:inline}
.rochips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 10px}
.rochip{font:inherit;font-size:.85rem;font-weight:700;padding:3px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
.rochip[aria-pressed="true"]{background:#7a3fc4;border-color:#7a3fc4;color:#fff}
table.poitbl{min-width:900px}
table.poitbl th .pw{display:block;font-weight:400;font-size:.72rem;color:var(--muted)}
table.poitbl tbody th{white-space:nowrap}
table.poitbl tr.on td,table.poitbl tr.on th{background:color-mix(in srgb,#7a3fc4 14%,transparent)}
table.poitbl tr.on th{box-shadow:inset 4px 0 0 #7a3fc4}
.gen{display:inline-block;margin-left:4px;font-size:.7rem;font-weight:700;padding:0 6px;border-radius:999px;border:1px dashed var(--muted);color:var(--muted)}
'''
s=s.replace('</style>\n<link',CSS+'</style>\n<link',1)

OLDJS=s[s.index("  function show(){"):s.index("  show();\n")+len("  show();\n")]
NEWJS='''
  function show(id){
    id=id||(location.hash||'#p1').slice(1);
    if(!panels.some(function(p){return p.dataset.tab===id})) id='p1';
    panels.forEach(function(p){p.hidden=p.dataset.tab!==id});
    tabs.forEach(function(a){ if(a.getAttribute('href')==='#'+id) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
  }
  tabs.forEach(function(a){a.addEventListener('click',function(e){
    e.preventDefault();var id=a.getAttribute('href').slice(1);show(id);
    try{history.replaceState(null,'','#'+id)}catch(_){}
    var n=document.querySelector('nav.tabs');try{window.scrollTo(0,0)}catch(_){}
  })});
  window.addEventListener('hashchange',function(){show()});
  show();
'''
s=s.replace(OLDJS,NEWJS,1)

JS='''
var FIGSRC=__FIGSRC__;
var pop=document.createElement('div');pop.className='figpop';pop.hidden=true;pop.setAttribute('role','dialog');document.body.appendChild(pop);
var cur=null,pinned=false;
function srcEl(k){var f=FIGSRC[k];if(!f)return null;var sel=f[0]==='img'?'img[alt^="'+f[1]+'"]':'svg[aria-label^="'+f[1]+'"]';return document.querySelector(sel)}
function place(b){var r=b.getBoundingClientRect(),w=pop.offsetWidth,h=pop.offsetHeight,vw=innerWidth,vh=innerHeight;
  var x=Math.min(Math.max(8,r.left),vw-w-8),y=r.bottom+6;if(y+h>vh-8)y=Math.max(8,r.top-h-6);pop.style.left=x+'px';pop.style.top=y+'px'}
function showFig(b){var k=b.dataset.fig,e=srcEl(k);if(!e)return;cur=b;pop.innerHTML='';
  var n;if(e.tagName.toLowerCase()==='img'){n=document.createElement('img');n.src=e.src;n.alt=e.alt}else{n=e.cloneNode(true);n.removeAttribute('id')}
  pop.appendChild(n);var c=document.createElement('p');c.textContent=FIGSRC[k][2];pop.appendChild(c);pop.hidden=false;place(b)}
function hideFig(){pop.hidden=true;if(cur)cur.setAttribute('aria-expanded','false');cur=null;pinned=false}
document.addEventListener('mouseover',function(e){var b=e.target.closest&&e.target.closest('.figbtn');if(b&&!pinned)showFig(b)});
document.addEventListener('mouseout',function(e){var b=e.target.closest&&e.target.closest('.figbtn');if(b&&!pinned&&!(e.relatedTarget&&b.contains(e.relatedTarget)))hideFig()});
document.addEventListener('click',function(e){var b=e.target.closest('.figbtn');
  if(b){e.stopPropagation();if(pinned&&cur===b){hideFig();return}showFig(b);pinned=true;b.setAttribute('aria-expanded','true');return}
  if(pinned&&!pop.contains(e.target))hideFig()},true);
document.addEventListener('keydown',function(e){if(e.key==='Escape')hideFig()});
addEventListener('scroll',function(){if(!pop.hidden&&cur)place(cur)},{passive:true});
function setRo(ro){[].forEach.call(document.querySelectorAll('.rochip'),function(c){c.setAttribute('aria-pressed',c.dataset.ro===ro?'true':'false')});
  [].forEach.call(document.querySelectorAll('.poitbl tr[data-ro]'),function(t){t.classList.toggle('on',t.dataset.ro===ro)});[].forEach.call(document.querySelectorAll('.poiro'),function(t){t.classList.toggle('on',t.dataset.ro===ro)});[].forEach.call(document.querySelectorAll('.rofig'),function(t){t.hidden=t.dataset.roles.split(' ').indexOf(ro)<0});try{localStorage.setItem('tea-guide-ro',ro)}catch(_){}}
try{setRo(localStorage.getItem('tea-guide-ro')||'st')}catch(_){setRo('st')}
document.addEventListener('click',function(e){var c=e.target.closest('.rochip');if(c)setRo(c.dataset.ro)});
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-go]');
  if(b){var el=document.getElementById(b.dataset.go);if(el){el.open=true;el.scrollIntoView({behavior:'smooth',block:'start'})}return}
  var a=e.target.closest('[data-all]');
  if(a){var pn=a.closest('.panel');[].forEach.call(pn.querySelectorAll('details.blk,details.mcard'),function(d){d.open=a.dataset.all==='open'})}
  var c=e.target.closest('[data-cards]');
  if(c){var bl=c.closest('.blk');[].forEach.call(bl.querySelectorAll('details.mcard'),function(d){d.open=c.dataset.cards==='open'})}
  var h=e.target.closest('a[href^="#"]');
  if(h&&h.getAttribute('href').length>1){var t=document.getElementById(h.getAttribute('href').slice(1));
    if(t&&!t.classList.contains('panel')&&t.closest('.panel')){e.preventDefault();var d=t;while(d){if(d.tagName==='DETAILS')d.open=true;d=d.parentElement}t.scrollIntoView({behavior:'smooth',block:'start'})}}
});
'''
JS=JS.replace('__FIGSRC__',json.dumps({k:list(v) for k,v in FIGS.items()},ensure_ascii=False))
s=s.replace('  show();\n})();','  show();\n'+JS+'})();',1)
s=s.replace('nav.tabs{position:sticky;','.bh{scroll-margin-top:60px}.blk{scroll-margin-top:60px}\nnav.tabs{position:sticky;',1)

LB_CSS = """.lbx{position:fixed;inset:0;z-index:100;background:rgba(8,9,12,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:16px;cursor:zoom-out}
.lbx[hidden]{display:none}
.lbx img{width:96vw;height:84vh;object-fit:contain;border-radius:8px;box-shadow:0 10px 40px rgba(0,0,0,.6);background:#000}
.lbx p{margin:0;color:#ddd;font-size:.85rem;text-align:center;max-width:90vw}
.lbx .nv{position:fixed;top:50%;transform:translateY(-50%);width:44px;height:64px;border:0;border-radius:10px;background:rgba(255,255,255,.12);color:#fff;font-size:28px;cursor:pointer}
.lbx .nv:hover,.lbx .nv:focus-visible{background:rgba(255,255,255,.25);outline:none}
.lbx .pv{left:12px}.lbx .nx{right:12px}
.lbx .x{position:fixed;top:12px;right:12px;width:40px;height:40px;border:0;border-radius:50%;background:rgba(255,255,255,.15);color:#fff;font-size:22px;cursor:pointer}
.zoomable{cursor:zoom-in}
.figpop img{cursor:zoom-in}
"""
LB_JS = """<script>
(function(){
  var sel='main img:not(.dbimg):not(.rowic), .wrap img:not(.dbimg):not(.rowic), section img:not(.dbimg):not(.rowic)';
  function list(){return [].slice.call(document.querySelectorAll(sel)).filter(function(i){return !i.closest('.figpop')&&!i.closest('.lbx')&&!i.closest('nav')})}
  list().forEach(function(i){i.classList.add('zoomable');i.title=i.title||'點一下放大'});
  var box=document.createElement('div');box.className='lbx';box.hidden=true;box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label','放大圖片');
  var im=document.createElement('img'),cap=document.createElement('p');
  var pv=document.createElement('button');pv.className='nv pv';pv.type='button';pv.textContent='‹';pv.setAttribute('aria-label','上一張');
  var nx=document.createElement('button');nx.className='nv nx';nx.type='button';nx.textContent='›';nx.setAttribute('aria-label','下一張');
  var x=document.createElement('button');x.className='x';x.type='button';x.textContent='×';x.setAttribute('aria-label','關閉');
  box.append(im,cap,pv,nx,x);document.body.appendChild(box);
  var L=[],k=-1,last=null;
  function show(src,alt,arr,idx){L=arr||[];k=idx==null?-1:idx;im.src=src;im.alt=alt||'';cap.textContent=alt||'';pv.hidden=nx.hidden=!(L.length>1&&k>=0);box.hidden=false;x.focus()}
  function step(d){if(k<0||!L.length)return;k=(k+d+L.length)%L.length;show(L[k].src,L[k].alt,L,k)}
  function close(){box.hidden=true;im.src='';if(last)try{last.focus()}catch(e){}}
  document.addEventListener('click',function(e){
    var t=e.target;if(!t||t.tagName!=='IMG')return;
    if(t.closest('.lbx'))return;
    if(t.closest('.figpop')){e.stopPropagation();last=document.activeElement;show(t.src,t.alt);return}
    if(!t.classList.contains('zoomable'))return;
    var arr=list();last=t;show(t.src,t.alt,arr,arr.indexOf(t))},true);
  box.addEventListener('click',function(e){if(e.target===pv){step(-1)}else if(e.target===nx){step(1)}else close()});
  document.addEventListener('keydown',function(e){if(box.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowLeft')step(-1);else if(e.key==='ArrowRight')step(1)});
})();
</script>"""
s = s.replace('</style>', LB_CSS + '</style>', 1)
i = s.rindex('</body>')
s = s[:i] + LB_JS + '\n' + s[i:]
open(D+'tea-guide.html','w',encoding='utf8').write(s)
print(len(s))
