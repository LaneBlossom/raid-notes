"""極永恆黑暗（Necron EX）攻略：子言姐姐 7.3 攻略整理，站位與標點對齊「子言姐姐 × XIVStrat 機制速覽」小抄。
自繪方形場地示意圖；藍色 ST 高亮。"""
import json

S = 220   # arena size
O = 10    # offset
COL = {'MT': '#64748b', 'ST': '#3b82f6', 'H1': '#16a34a', 'H2': '#16a34a',
       'D1': '#a16207', 'D2': '#a16207', 'D3': '#a16207', 'D4': '#a16207'}


def P(x, y):
    """x,y in 0..1 of arena"""
    return (O + x * S, O + 18 + y * S)


def svg(items, top='', bottom='', boss=True, circle=False, label=''):
    H = S + 48
    o = [f'<svg viewBox="0 0 {S+2*O} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">',
         '<defs><marker id="nxa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#3b82f6"/></marker></defs>']
    if top:
        o.append(f'<text x="{O+S/2}" y="12" text-anchor="middle" font-size="9.5" fill="currentColor">{top}</text>')
    x0, y0 = P(0, 0)
    if circle:
        o.append(f'<rect x="{x0}" y="{y0}" width="{S}" height="{S}" fill="#1b1430" stroke="#4b3b6b" stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{x0+S/2}" cy="{y0+S/2}" r="{S*0.36}" fill="#3a3046" stroke="#c9b48a" stroke-width="2.5"/>')
        o.append(f'<line x1="{x0+S/2}" y1="{y0+S*0.14}" x2="{x0+S/2}" y2="{y0+S*0.86}" stroke="#c9b48a" stroke-dasharray="3 3" opacity=".6"/>')
        o.append(f'<line x1="{x0+S*0.14}" y1="{y0+S/2}" x2="{x0+S*0.86}" y2="{y0+S/2}" stroke="#c9b48a" stroke-dasharray="3 3" opacity=".6"/>')
    else:
        o.append(f'<rect x="{x0}" y="{y0}" width="{S}" height="{S}" rx="4" fill="#2a2338" stroke="#c9b48a" stroke-width="2.5"/>')
        o.append(f'<circle cx="{x0+S/2}" cy="{y0+S/2}" r="{S*0.12}" fill="none" stroke="#5b4d70"/>')
    if boss:
        bx, by = P(0.5, 0)
        o.append(f'<rect x="{bx-22}" y="{by-9}" width="44" height="16" rx="4" fill="#111" stroke="#e5c07b" stroke-width="1.4"/>'
                 f'<text x="{bx}" y="{by+3}" text-anchor="middle" font-size="9" font-weight="700" fill="#e5c07b">Boss</text>')
    o += items
    if bottom:
        o.append(f'<text x="{O+S/2}" y="{H-4}" text-anchor="middle" font-size="9.5" fill="currentColor">{bottom}</text>')
    o.append('</svg>')
    return ''.join(o)


def pl(role, x, y, r=8.5):
    cx, cy = P(x, y)
    c = COL.get(role, '#a16207')
    ring = ' stroke="#fff" stroke-width="2.2"' if role == 'ST' else ' stroke="#fff" stroke-width="1"'
    fs = 7.5 if len(role) > 1 else 9
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + (1.5 if role=="ST" else 0)}" fill="{c}"{ring}/>'
            f'<text x="{cx:.1f}" y="{cy+2.8:.1f}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="#fff">{role}</text>')


def grp(roles, x, y, dx=0.075):
    n = len(roles)
    return ''.join(pl(r, x + (i - (n - 1) / 2) * dx, y) for i, r in enumerate(roles))


def txt(x, y, t, anchor='middle', col='#ffe08a', fs=9):
    cx, cy = P(x, y)
    return f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="{anchor}" font-size="{fs}" font-weight="700" fill="{col}" stroke="#000" stroke-width="2.4" paint-order="stroke">{t}</text>'


def mark(x, y, ch, col):
    cx, cy = P(x, y)
    return (f'<rect x="{cx-8}" y="{cy-8}" width="16" height="16" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>'
            f'<text x="{cx}" y="{cy+3.5}" text-anchor="middle" font-size="10" font-weight="800" fill="{col}">{ch}</text>')


def puddle(x, y, r=0.06):
    cx, cy = P(x, y)
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*S:.1f}" fill="#0b0712" stroke="#6b21a8" stroke-width="1.2"/>'


def tower(x, y, n, r=0.075):
    cx, cy = P(x, y)
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*S:.1f}" fill="rgba(244,114,182,.18)" stroke="#f472b6" stroke-width="1.5"/>'
            f'<text x="{cx:.1f}" y="{cy-r*S-2:.1f}" text-anchor="middle" font-size="8" font-weight="700" fill="#f9a8d4">{n} 人</text>')


def arrow(a, b):
    (x1, y1), (x2, y2) = P(*a), P(*b)
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#3b82f6" stroke-width="2.4" marker-end="url(#nxa)"/>'


# ---------- diagrams ----------
def d_shock():
    return svg([pl('MT', .07, .07), pl('ST', .93, .07),
                txt(.07, .2, '① MT 左上吃', 'start'), txt(.93, .2, '② ST 挑釁後右上吃', 'end'),
                grp(['H1', 'D1', 'D3', 'H2', 'D2', 'D4'], .5, .6, .09),
                txt(.5, .75, '其他人在中間偏下，別站兩角', 'middle', '#cbd5e1')],
               top='青藍衝擊：二連扇形死刑', bottom='第二下沒有範圍提示', label='青藍衝擊站位')


def d_hands():
    """死之恐懼：固定方位（子言姐姐 × XIVStrat 小抄）。DPS 往上下引導、坦克補師往左右。"""
    pos = {'D1': (.32, .08), 'D2': (.68, .08), 'MT': (.08, .3), 'ST': (.92, .3),
           'H1': (.08, .66), 'H2': (.92, .66), 'D3': (.32, .92), 'D4': (.68, .92)}
    arr = [arrow((.32, .18), (.32, .01)), arrow((.68, .18), (.68, .01)), arrow((.32, .82), (.32, .99)), arrow((.68, .82), (.68, .99)),
           arrow((.18, .3), (.01, .3)), arrow((.18, .66), (.01, .66)), arrow((.82, .3), (.99, .3)), arrow((.82, .66), (.99, .66))]
    return svg(arr + [pl(r, *xy) for r, xy in pos.items()] + [txt(.5, .44, 'DPS 往上下引導', 'middle', '#cbd5e1'), txt(.5, .56, '坦克、補師往左右', 'middle', '#cbd5e1')],
               top='死之恐懼：固定方位引導黑手', bottom='黑泥位置會變，站自己方位、別踩黑泥', label='死之恐懼站位')


def d_memento():
    lane = []
    x0, y0 = P(0, 0)
    lane.append(f'<rect x="{x0+S*0.37}" y="{y0}" width="{S*0.13}" height="{S}" fill="rgba(147,51,234,.35)"/>')
    lane.append(f'<rect x="{x0+S*0.5}" y="{y0}" width="{S*0.13}" height="{S}" fill="rgba(147,51,234,.35)"/>')
    pos = {'MT': (.08, .71), 'ST': (.25, .71), 'D1': (.75, .07), 'D2': (.92, .07),
           'H1': (.75, .48), 'H2': (.92, .48), 'D3': (.75, .93), 'D4': (.92, .93)}
    return svg(lane + [txt(.2, .08, '黑翅膀側', 'middle', '#cbd5e1'), txt(.8, .25, '白翅膀側', 'middle', '#cbd5e1')]
               + [pl(r, *xy) for r, xy in pos.items()] + [txt(.03, .58, '黑側只有一排安全', 'start')],
               top='死亡警告＋黑暗一擊（例：黑翅膀在左）', bottom='在黑手縫隙中分散；左右顛倒時整組平移', label='死亡警告站位')


MK = {'1': (.37, .06, '#ff6b6b'), '2': (.63, .06, '#ffd166'), '3': (.42, .3, '#60a5fa'), '4': (.58, .3, '#c084fc'),
      'A': (.08, .36, '#ff6b6b'), 'B': (.92, .36, '#86efac'), 'C': (.24, .5, '#60a5fa'), 'D': (.76, .5, '#c084fc')}


def d_reap(kind, side):
    """kind: 'pair' (四重=兩人分攤) or 'quad' (二重=四人分攤); side: 'out' / 'in'。標點同 XIVStrat 小抄。"""
    it = []
    x0, y0 = P(0, 0)
    if side == 'out':
        it.append(f'<rect x="{x0+S*0.38}" y="{y0}" width="{S*0.24}" height="{S}" fill="rgba(125,211,252,.25)"/>')
    else:
        it.append(f'<rect x="{x0}" y="{y0}" width="{S*0.25}" height="{S}" fill="rgba(125,211,252,.25)"/>')
        it.append(f'<rect x="{x0+S*0.75}" y="{y0}" width="{S*0.25}" height="{S}" fill="rgba(125,211,252,.25)"/>')
    it += [mark(x, y, k, c) for k, (x, y, c) in MK.items()]
    if kind == 'quad':
        if side == 'out':
            it += [grp(['MT', 'H1'], .22, .6, .08), grp(['D1', 'D3'], .22, .7, .08), grp(['ST', 'H2'], .78, .6, .08), grp(['D2', 'D4'], .78, .7, .08)]
            where = '安全區在外：站 C、D 點'
        else:
            it += [grp(['MT', 'H1'], .38, .4, .08), grp(['D1', 'D3'], .38, .5, .08), grp(['ST', 'H2'], .62, .4, .08), grp(['D2', 'D4'], .62, .5, .08)]
            where = '安全區在內：站 3、4 點'
        t = '二重波＝4 人分攤'
    else:
        if side == 'out':
            it += [grp(['MT', 'D1'], .1, .46, .075), grp(['H1', 'D3'], .25, .6, .075),
                   grp(['H2', 'D4'], .75, .6, .075), grp(['D2', 'ST'], .9, .46, .075)]
            where = '安全區在外：站 A、C、D、B 點'
        else:
            it += [grp(['MT', 'D1'], .34, .16, .075), grp(['D2', 'ST'], .66, .16, .075),
                   grp(['H1', 'D3'], .38, .4, .075), grp(['H2', 'D4'], .62, .4, .075)]
            where = '安全區在內：站 1、3、4、2 點'
        t = '四重波＝2 人分攤'
    return svg(it, top=f'青藍之魂＋{t}', bottom=where, label=f'{t}{where}')


def d_cross():
    it = [grp(['MT', 'D1'], .32, .3, .08), grp(['ST', 'D2'], .68, .3, .08),
          grp(['H1', 'D3'], .32, .7, .08), grp(['H2', 'D4'], .68, .7, .08),
          txt(.5, .06, '圓形平台外＝即死', 'middle', '#fca5a5')]
    return svg(it, top='大十字：平台變圓形，兩人負責一區', bottom='踩塔的人別吃圓圈、放圓圈的人別踩塔', circle=True, boss=False, label='大十字分區')


def d_wing2():
    it = [pl('MT', .08, .08), pl('D1', .3, .08), pl('D2', .7, .08), pl('ST', .92, .08),
          pl('H1', .08, .3), pl('D3', .3, .3), pl('D4', .7, .3), pl('H2', .92, .3),
          txt(.5, .55, '放完圓圈到黑手中間集合', 'middle', '#cbd5e1'),
          txt(.5, .68, '直線出現後縱向走位躲', 'middle', '#cbd5e1')]
    return svg(it, top='P2 黑暗巨腕＋引導之翼：分散放圈', bottom='先找大黑手打不到的安全橫排', label='P2 引導之翼站位')


def d_macabre1():
    it = [tower(.5, .3, 4), tower(.5, .7, 4), grp(['MT', 'ST', 'D1', 'D2'], .5, .3, .055), grp(['H1', 'H2', 'D3', 'D4'], .5, .7, .055)]
    for p in [(.25, .06), (.75, .06), (.06, .38), (.06, .55), (.94, .38), (.94, .55), (.25, .94), (.75, .94)]:
        it.append(tower(*p, '', .06))
    return svg(it, top='群體恐慌 ①：兩座 4 人塔', bottom='踩塔附 4 秒魔法易傷，期間不能再踩', label='群體恐慌四人塔')


def d_macabre2():
    it = [tower(.08, .38, 2, .065), tower(.08, .6, 2, .065), tower(.92, .38, 2, .065), tower(.92, .6, 2, .065),
          grp(['D3', 'D4'], .2, .38), grp(['MT', 'H1'], .2, .6), grp(['D1', 'D2'], .8, .38), grp(['ST', 'H2'], .8, .6),
          txt(.5, .5, '死亡警告：無視翅膀，固定兩側', 'middle', '#cbd5e1'),
          txt(.62, .78, '易傷消失再踩！', 'middle', '#fca5a5')]
    return svg(it, top='群體恐慌 ②：兩人塔', bottom='ST＋H2 右側下方的塔', label='群體恐慌兩人塔')


def d_macabre3():
    it = [pl('MT', .05, .05), pl('ST', .95, .05), tower(.18, .12, 3, .07), tower(.82, .12, 3, .07),
          tower(.18, .88, 3, .07), tower(.82, .88, 3, .07),
          grp(['H2', 'D1', 'D2'], .78, .3, .075), grp(['H1', 'D3', 'D4'], .22, .7, .075),
          txt(.06, .18, '① MT 最左上', 'start'), txt(.94, .42, '② ST 挑釁最右上', 'end'),
          txt(.5, .55, '先踩右上、左下，MT 吃完再踩剩下兩座', 'middle', '#cbd5e1')]
    return svg(it, top='群體恐慌 ③：青藍衝擊＋三人塔', bottom='最後暗黑死腕回場中', label='群體恐慌三人塔')


# ---------- content ----------
ST_PANELS = [
    ('P1 00:14', '青藍衝擊（死刑換 T）', d_shock(),
     ['MT 先在<b>左上角</b>開減傷吃第一下（附 5 秒魔法易傷）',
      'ST 在 boss <b>讀條期間挑釁</b>，到<b>右上角</b>吃第二下（沒有範圍提示）',
      'ST 吃完後 MT 挑回來；之後每次都照這個流程']),
    ('P1 00:29', '死之恐懼：引導黑手', d_hands(),
     ['全屏 AOE 後出 8 灘黑泥，<b>不要踩</b>（附 1 分鐘易傷；中間的泥消失前踩到會流血）',
      'ST 固定在<b>右側偏上</b>，把黑手的直線往<b>右邊場外</b>引導（DPS 往上下、坦克補師往左右）']),
    ('P1 00:40', '暗黑死腕', None,
     ['先到場中，再看哪一側觸手<b>沒發光</b>，去那一側的<b>內側</b>躲']),
    ('P1 00:52', '死亡警告＋黑暗一擊', d_memento(),
     ['雙 T 去<b>黑色翅膀</b>那一側，其他 6 人去白色那側',
      '黑翅膀那側只有一排安全，<b>MT 在左、ST 在右並排</b>；左右顛倒時整組平移，不用鏡像',
      '在黑手縫隙中分散吃黑暗一擊（圓圈）']),
    ('P1 01:10', '青藍之魂＋二重／四重波', d_reap('pair', 'out'),
     ['讀條時看 boss 胸前的範圍，<b>記住內或外</b>（傷害延後）',
      '<b>四重波</b>＝2 人分攤：ST＋D2，安全在外站 <b>B 點</b>、在內站 <b>2 點</b>',
      '<b>二重波</b>＝4 人分攤：ST、H2、D2、D4 右組，安全在外站 <b>D 點</b>、在內站 <b>4 點</b>']),
    ('P1 01:43', '引導之翼＋青藍衝擊 ②', None,
     ['在剛剛引導的黑手位置放圓圈，再用同樣站位把新黑手往場外引導（這次可以躲）',
      '青藍衝擊 ②：一樣 ST 挑釁到右上角吃第二下']),
    ('P1 02:20', '大十字', d_cross(),
     ['高傷 AOE 後場地變圓形，站出圓外即死',
      'ST＋D2 負責<b>右上</b>那一區：踩塔和放圓圈互斥、躲旋轉直線（3-2-1 倒數）',
      '最後兩波圓圈後去<b>四角</b>躲距離衰減；中子環開減傷']),
    ('P1.5', '小怪階段', None,
     ['大黑手要 T 拉，把直線（擊潰）<b>往場外</b>引導，開一般減傷就吃得下',
      '全員先集火大黑手；進度條滿 100 會滅團']),
    ('單人', '異空間（坦克）', None,
     ['黑手第一招<b>散佈</b>一定要用<b>插言／沉默</b>打斷，不然會死',
      '接著連續壓潰，開減傷；可以留爆發進來打',
      '擊殺後跳平台走進光柱，解除死亡宣告']),
    ('P2 00:00', '黑暗巨腕＋引導之翼', d_wing2(),
     ['先看大黑手在哪，找<b>安全的橫排</b>，千萬別被抓走',
      'ST 在<b>最右上</b>放圈，之後到黑手中間集合，等直線出現再縱向走位']),
    ('P2 00:40', '青藍連魂＋靈魂輪轉', None,
     ['記住 4 個範圍的<b>內／外</b>；轉輪停下後從<b>最下方</b>的圖示開始依序放',
      '順序永遠是 1234 循環（例如 3412），不會倒過來',
      '最後一波同時判定分攤，照青藍之魂的站位（ST 在右）']),
    ('P2 01:18', '青藍環波', None,
     ['看哪個光圈<b>先變大</b>，靠近它躲環形；同時躲大黑手的橫向直線',
      '最後還有一次青魂＋分攤，路線遠時開衝刺']),
    ('P2 02:06', '群體恐慌（踩塔）', d_macabre3(),
     ['① 上方 4 人塔：MT、ST、D1、D2',
      '② 死亡警告：無視翅膀固定兩側，<b>ST＋H2 踩右側下方 2 人塔</b>（等易傷消失）',
      '③ 青藍衝擊：<b>ST 挑釁到最右上角</b>吃第二下，不踩 3 人塔',
      '騎士可以保護一個補師，炸塔時讓補師用三段 LB 救場']),
    ('P2 04:44', '大十字 ②・中子環 ②', None,
     ['同 P1：ST＋D2 右上區，最後去四角；中子環後狂暴「永世黑暗」']),
]

MECH = [
    ('青藍衝擊（死刑換 T）', '對一仇的二連高傷扇形。第一下附 5 秒魔法易傷，不開無敵吃不下第二下。',
     ['MT 左上角開減傷吃第一下', 'ST 在讀條期間挑釁，到右上角吃第二下（沒有範圍提示）', 'MT 再挑回；固定流程每次都一樣'],
     [d_shock()]),
    ('死之恐懼（引導黑手）', '全屏 AOE 後出 8 灘黑泥，長出黑手時有傷害（附 1 分鐘易傷）。黑手對最近的人放不可迴避的直線，附 1 秒物理易傷，吃到兩條就死。',
     ['固定方位：D1、D2 在上，D3、D4 在下，MT、H1 在左，ST、H2 在右', '<b>DPS 往上下</b>、<b>坦克和補師往左右</b>把直線引出場外',
      '黑泥位置每次不同，站在自己方位附近避開；中間的黑泥在消失前不能踩，踩到附 15 秒流血'],
     [d_hands()]),
    ('暗黑死腕', 'Boss 先打兩側矩形，再用發光的觸手補一次大範圍矩形。',
     ['先去場中', '看哪側觸手沒發光，去那一側的內側'], []),
    ('死亡警告＋黑暗一擊', 'Boss 兩側翅膀一黑一白。讀條後打場中矩形，留下黑泥：黑翅膀側長 4 隻手、白翅膀側長 1 隻手。同時黑暗一擊點全員圓圈。',
     ['雙 T 去黑翅膀側，其他 6 人去白翅膀側（不用看分組、不用換位）', '白翅膀側分三排：D1、D2 最上排，H1、H2 中間，D3、D4 最下排；黑翅膀側只有一排安全，MT、ST 並排',
      'MT 永遠在 ST 左邊；H1、D1、D3 永遠在 H2、D2、D4 左邊；左右顛倒時平移不鏡像',
      '先判定圓圈再判定黑手；黑手判定後可以再互相拉開一點'], [d_memento()]),
    ('青藍之魂＋二重／四重波（分組分攤）', '讀條時 boss 胸前顯示範圍（打兩側＝安全在內、打中間＝安全在外），傷害延後。接著二重波＝4 人分攤、四重波＝2 人分攤（點 4 個 T 奶或 4 個 DPS）。',
     ['<b>二重波（4 人）</b>：MT、H1、D1、D3 左組，ST、H2、D2、D4 右組；安全在外站 C、D 點，在內站 3、4 點',
      '<b>四重波（2 人）</b>：安全在外 MT＋D1 站 A、H1＋D3 站 C、H2＋D4 站 D、ST＋D2 站 B；在內依序換成 1、3、4、2 點',
      '第二次青魂的安全區一定和第一次相反'],
     [d_reap('pair', 'out'), d_reap('quad', 'out'), d_reap('pair', 'in'), d_reap('quad', 'in')]),
    ('引導之翼', '點全員放圓圈，圓圈判定後原地長黑手，再對最近的人放直線（這次可以躲）。',
     ['到剛剛引導黑手的位置放圓圈', '用同樣站位把新黑手往場外引導，再躲開'], []),
    ('大十字', '全屏高傷 AOE 後場地變圓形，站在圓外即死。兩條旋轉直線（變色＋3-2-1 倒數後判定）、4 座塔、點 4 個 T 奶或 4 個 DPS 的圓圈各兩波。最後點兩波圓圈後是距離衰減，再接中子環。',
     ['兩人負責一區：MT＋D1 左上、ST＋D2 右上、H1＋D3 左下、H2＋D4 右下', '踩塔的人不能吃圓圈，放圓圈的人不能踩塔；漏塔會全屏 AOE＋疊層流血',
      '第二輪圓圈後去四角躲距離衰減，記得減傷'], [d_cross()]),
    ('小怪階段（進度條）', 'Boss 不可選中，場上出現小黑手和大黑手，進度條滿 100 會被永世黑暗強制滅團。',
     ['小黑手只放可躲的直線，躲就好', '大黑手要 T 拉，把直線引導到場外；全員先集火大黑手'], []),
    ('異空間（單人階段）', '全員被吸入異空間，附 50 秒死亡宣告，依職業打不同的黑手。打完跳平台走進光柱解除。',
     ['<b>坦克</b>：散佈一定要用插言／沉默打斷；之後連續壓潰，開減傷', '<b>補師</b>：直線會給自己和黑手流血，邊奶自己邊打，減速可以驅散',
      '<b>DPS</b>：兩隻黑手放可躲的直線，之後會狂暴，平均打血，看誰讀狂暴先打死誰'], []),
    ('黑暗巨腕＋引導之翼（P2）', '場地兩側伸出大黑手放橫向直線，被抓到要再打一次異空間。接著點全員放圓圈。',
     ['先看大手在哪，找安全的橫排', '照站位分散放圈，放完到黑手中間集合，直線出現後縱向走位', '同時有暗黑死腕：看發光手臂，往反方向躲'],
     [d_wing2()]),
    ('青藍連魂＋靈魂輪轉（記憶）', '連續儲存 4 種範圍（打兩側、打中間、圓形、環形），轉輪停下後從最下方的圖示開始依序釋放，最後一波同時判定分組分攤。',
     ['用「內／外」記 4 個範圍', '順序是 1234 的循環（如 3412、2341），不會出現 4321', '二重＝4 人分攤、四重＝2 人分攤，最後一波的內外決定站字母點或數字點'], []),
    ('青藍環波', '場上 5 個光圈，先變大的那個放環形。同時大黑手放橫向直線，最後接一次青魂＋分攤。',
     ['靠近先變大的光圈躲環形', '一邊躲環一邊躲大黑手', '路線遠時開衝刺'], []),
    ('群體恐慌（踩塔）', '場上出現多人塔，塔裡有幾個圈就要幾個人踩。踩塔附 4 秒魔法易傷，期間再踩就死。',
     ['① 4 人塔：MT、ST、D1、D2 上；H1、H2、D3、D4 下', '② 死亡警告無視翅膀固定兩側，踩兩人塔（等易傷消失）',
      '③ 青藍衝擊：MT 最左上、ST 最右上；其他人先踩右上與左下的三人塔，MT 吃完再踩剩下兩座', '最後暗黑死腕回場中'],
     [d_macabre1(), d_macabre2(), d_macabre3()]),
]

HINTS = [["青藍衝擊", "死刑換T"], ["死之恐懼（圈）", "DPS上下・坦奶左右"], ["死之恐懼", "AOE＋黑泥"], ["暗黑死腕", "先中間→沒發光那側內側"],
         ["死亡警告", "雙T黑翅膀側"], ["黑暗一擊", "分散圓圈"], ["青藍之魂", "記內外"], ["青藍連魂", "記4個內外"],
         ["靈魂輪轉", "從最下方開始"], ["青藍二重波／青藍四重波", "二重4人CD/34・四重2人ABCD/1234"], ["二重青藍浪潮／四重青藍浪潮", "二重4人CD/34・四重2人ABCD/1234"],
         ["引導之翼", "放圈→引導黑手"], ["大十字（圈）", "圓圈"], ["大十字（直線）", "旋轉直線"], ["大十字（斜角）", "四角距離衰減"],
         ["大十字", "高傷AOE・分區"], ["放電（塔）", "踩塔"], ["中子環", "高傷AOE"], ["黑暗巨腕", "找安全橫排"],
         ["青藍環波", "靠近先變大的圈"], ["群體恐慌", "踩塔4→2→3"], ["散佈", "打斷！"], ["壓潰（直線）", "引導到場外"]]

if __name__ == '__main__':
    json.dump(HINTS, open('/home/claude/work/necronx/hints.json', 'w', encoding='utf8'), ensure_ascii=False)
    print('ok')
