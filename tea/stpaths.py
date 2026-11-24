"""P3 騎士 ST 一圖流：自繪 SVG（依版主筆記與魚子醬 P3 詳解整理）。"""
import math

R, C = 100, 120
ST = '#3b82f6'
MT = '#64748b'


def pt(deg, r):
    a = math.radians(deg)
    return (C + r * R * math.sin(a), C - r * R * math.cos(a))


def arena(extra, top='', bottom=''):
    o = ['<svg viewBox="0 0 240 250" xmlns="http://www.w3.org/2000/svg" role="img">',
         '<defs><marker id="sta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#3b82f6"/></marker></defs>',
         f'<circle cx="{C}" cy="{C}" r="{R}" fill="#3b3428" stroke="#b9975b" stroke-width="3"/>',
         f'<circle cx="{C}" cy="{C}" r="{R*.55}" fill="none" stroke="#6b5a3e" stroke-dasharray="3 3"/>']
    for deg in (318, 42, 222, 138, 270, 90):
        x, y = pt(deg, .86)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#c0392b" opacity=".75"/>')
    if top:
        o.append(f'<text x="{C}" y="12" text-anchor="middle" font-size="9.5" fill="currentColor">{top}</text>')
    if bottom:
        o.append(f'<text x="{C}" y="{C+R+15}" text-anchor="middle" font-size="9.5" fill="currentColor">{bottom}</text>')
    o += extra
    o.append('</svg>')
    return ''.join(o)


def boss(x, y, label, col='#e5c07b'):
    return (f'<rect x="{x-17:.1f}" y="{y-9:.1f}" width="34" height="18" rx="4" fill="#111" stroke="{col}" stroke-width="1.5"/>'
            f'<text x="{x:.1f}" y="{y+3.5:.1f}" text-anchor="middle" font-size="9" font-weight="700" fill="{col}">{label}</text>')


def me(x, y, label='ST', col=ST, r=9):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="#fff" stroke-width="1.6"/>'
            f'<text x="{x:.1f}" y="{y+3.3:.1f}" text-anchor="middle" font-size="{8 if len(label) > 1 else 10}" font-weight="800" fill="#fff">{label}</text>')


def tag(x, y, text, anchor='middle', col='#ffe08a'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="9.5" font-weight="700" fill="{col}" stroke="#000" stroke-width="2.4" paint-order="stroke">{text}</text>'


def arrow(a, b, col=ST, dash=False):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    d = ' stroke-dasharray="4 3"' if dash else ''
    return f'<line x1="{a[0]+ux*10:.1f}" y1="{a[1]+uy*10:.1f}" x2="{b[0]-ux*11:.1f}" y2="{b[1]-uy*11:.1f}" stroke="{col}" stroke-width="2.4"{d} marker-end="url(#sta)"/>'


def wm(deg, ch, col):
    x, y = pt(deg, .97)
    return f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="11" font-weight="800" fill="{col}" stroke="#000" stroke-width="2" paint-order="stroke">{ch}</text>'


# ---------- panels ----------
def p_timestop():
    Lb, Rb = (C - 32, C + 4), (C + 32, C + 4)
    ex = [boss(*Lb, '左 boss'), boss(*Rb, '右 boss'),
          me(Rb[0], Rb[1] - 26, '近'), me(Lb[0], Lb[1] - 26, '無'),
          me(*pt(270, .78), '遠'), me(*pt(90, .9), '電'),
          tag(Rb[0] + 12, Rb[1] - 38, '近線', 'start'), tag(Lb[0] - 12, Lb[1] - 38, '沒點名', 'end'),
          tag(pt(270, .78)[0] + 4, pt(270, .78)[1] + 22, '遠線', 'start'), tag(pt(90, .9)[0] - 4, pt(90, .9)[1] + 22, '電（正義號側）', 'end')]
    return arena(ex, top='兩隻 boss 一左一右（圖為範例）', bottom='電：去正義號那一側貼邊（不一定在右）')


def p_flame():
    J = (C - R + 20, C)
    MTp, STp = pt(270, .82), pt(238, .84)
    heart = pt(205, .45)
    ex = [boss(J[0] - 2, J[1] - 22, '正義號'),
          f'<text x="{heart[0]:.1f}" y="{heart[1]+5:.1f}" text-anchor="middle" font-size="16">💛</text>',
          tag(heart[0] + 14, heart[1] + 4, '真心', 'start'),
          me(*MTp, 'MT', MT), me(*STp, 'ST'),
          tag(MTp[0] + 14, MTp[1] + 4, 'MT 正義號面前紅點', 'start', '#cbd5e1'),
          tag(STp[0] + 14, STp[1] + 8, 'ST 往真心側偏', 'start')]
    return arena(ex, top='真心變金色後，雙 T 引導正義號噴火', bottom='對穿時走離場邊約 1/4 直徑的弧線')


def p_stack():
    out = pt(0, .99)
    STp, MTp = pt(270, .86), pt(282, .86)
    ex = [f'<text x="{out[0]:.1f}" y="{out[1]+12:.1f}" text-anchor="middle" font-size="16">💛</text>',
          tag(C, 44, '真心飛走的位置＝12 點'),
          me(*MTp, 'MT', MT), me(*STp, 'ST'),
          arrow((C, C), STp),
          tag(STp[0] + 14, STp[1] + 18, '雙 T 左邊貼邊（9 點）', 'start'),
          tag(STp[0] + 14, STp[1] + 31, '和集團罪 DPS 三人分攤', 'start')]
    return arena(ex, top='以真心飛走的位置為北', bottom='位置遠：等集團罪動畫判定再走')


def p_jump():
    STp = pt(90, .9)
    ex = [wm(0, 'A', '#ff6b6b'), wm(90, 'B', '#ffd166'), wm(180, 'C', '#6bcBff'), wm(270, 'D', '#c49bff'),
          me(*STp, 'ST'), arrow((C, C), STp),
          tag(STp[0] - 14, STp[1] + 22, 'B 點方向貼邊', 'end'),
          tag(C, C + 40, '其他人在飛機與 B 點之間', 'middle', '#cbd5e1'),
          tag(C, C + 53, '三刀後立刻遠離 B 點', 'middle', '#cbd5e1')]
    return arena(ex, top='飛機三刀 → 正義號超級跳最遠的人', bottom='飛機劈完第一下就開減傷')


def p_final():
    ex = [me(C - 12, C - 22, 'ST'), me(C + 12, C - 22, 'MT', MT), me(C, C - 42, 'D', '#a16207'),
          me(C - 12, C + 26, 'H', '#16a34a'), me(C + 12, C + 26, 'H', '#16a34a'), me(C, C + 46, 'D', '#a16207'),
          tag(C, C - 60, '上方：雙 T＋讀秒 DPS'), tag(C, C + 68, '下方：雙補＋讀秒 DPS', 'middle', '#cbd5e1')]
    return arena(ex, top='次元斷絕結束：淨化熱線＋生命計算法', bottom='▲ 亞歷山大（下）')


PANELS = [
    ('00:03', '時停（看自己的 debuff）', p_timestop,
     ['T 奶組站位，<b>以兩隻 boss 左右為準</b>：',
      '近線 → 右邊 boss <b>正上方</b>（飛機和正義號中間）',
      '沒點名 → 左邊 boss 上方',
      '遠線 → 場地正左（9 點）；左邊是飛機就站紅點內側，是正義號就貼邊',
      '電（加重罪）→ 正義號那側貼邊'], 'p3_ts_th'),
    ('00:21', '第一次死刑：ST 無敵', None,
     ['讀條到「罰」～「射」字之間開<b>神聖領域</b>，單吃 4 下（神罰射線 1＋神聖之槍 3）',
      '別太早開：最後一下神聖之槍在神罰射線落地後約 7 秒，神聖領域只有 10 秒，要在<b>落地前約 2～3 秒內</b>開才蓋得到',
      '吃完<b>退避</b>，仇恨還給 MT'], None),
    ('00:37', '一運開始（看自己的 debuff）', None,
     ['先看 A 或 C 點，確認亞歷山大在哪一邊',
      '<b>綠球連線</b>：到亞歷山大那半場，走到自己綠球的對側交叉拉線；在靠近亞歷山大的綠球旁等，真心開始炸就跑，<b>開聖盾陣</b>',
      '<b>黃圈</b>：照位置放結晶（先到先得），判定後衝刺往亞歷山大方向'], 'p3_green'),
    ('01:09', '噴火引導（雙 T 固定）', p_flame,
     ['MT 站正義號面前的紅點',
      '<b>ST 站正義號和它靠真心那側的紅點之間</b>（站錯容易被結晶破碎打死）',
      '雙 T 對穿時走離場邊約 1/4 直徑的弧線'], 'p3_st_heart'),
    ('01:21', '集團罪分攤（雙 T 固定）', p_stack,
     ['<b>以真心飛走的位置為 12 點</b>',
      '雙 T <b>無腦去左邊（9 點）貼邊</b>，和集團罪的 DPS 三人分攤',
      '距離比較遠，等集團罪動畫判定再走'], 'p3_half'),
    ('01:35', '超級跳（ST 固定引導）', p_jump,
     ['<b>ST 到 B 點方向貼邊</b>，引導正義號超級跳',
      '飛機劈完第一下就開<b>壁壘＋聖盾陣</b>（鐵壁可選）',
      '接著第二次死刑由 MT 無敵單吃，<b>ST 不用挑釁</b>'], 'p3_half'),
    ('02:09', '次元斷絕：看號碼', None,
     ['這段<b>看骰子號碼，不看職責</b>',
      '照自己的號碼看 <a href="#dimpaths">1～8 號跑位一圖流</a>'], None),
    ('02:50', '淨化熱線＋生命計算法', p_final,
     ['回中央，<b>ST 到上方</b>，和 MT、讀秒 DPS 三人一組',
      '開<b>聖光幕簾</b>'], 'dim_end'),
    ('03:02', '百萬神聖 ×2', None, ['第一個百萬神聖開<b>武裝戍衛</b>'], None),
    ('03:25', '火龍捲（DPS 檢測）', None,
     ['先殺飛機，再在正義號疊到 13 層前殺掉',
      '<b>雪仇等飛機死後再下</b>'], None),
    ('04:47', '神聖審判（轉 P4）', None,
     ['剩約 4 秒開<b>鐵壁＋聖盾陣</b>',
      '還有武裝戍衛的話也開，讓補師好回血'], None),
]


def section():
    cards = []
    for t, title, fn, lines, fig in PANELS:
        body = fn() if fn else ''
        li = ''.join(f'<li>{x}</li>' for x in lines)
        figb = f'<button class="figbtn" type="button" data-fig="{fig}">看原圖</button>' if fig else ''
        cards.append(f'<article class="sp{" txt" if not fn else ""}"><h4><span class="st">{t}</span>{title}{figb}</h4>{body}<ul>{li}</ul></article>')
    css = """<style>
.spgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:10px}
.sp{border:1px solid var(--line,#ddd);border-radius:10px;padding:10px;background:var(--panel,transparent)}
.sp.txt{align-self:start}
.sp h4{margin:0 0 6px;font-size:.95rem;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.sp .st{font-variant-numeric:tabular-nums;font-size:.75rem;padding:1px 6px;border-radius:5px;background:#3b82f6;color:#fff}
.sp h4 .figbtn{margin-left:auto}
.sp svg{width:100%;height:auto;display:block;color:var(--muted,#888)}
.sp ul{margin:6px 0 0;padding-left:1.1em;font-size:.85rem;line-height:1.55}
.spnote{font-size:.8rem;color:var(--muted,#888);margin:6px 0 0}
</style>"""
    return (css + '<section class="step nofig" id="stpaths"><div><h3 class="sh">P3 騎士 ST 一圖流</h3>'
            '<p class="spnote">照時間順序列出 ST 這一 P 要去哪、看哪個方向、開什麼。看 debuff 或號碼的機制只列 ST 可能拿到的情況；藍色是 ST。時間是 P3 開始後的時間。</p>'
            '<div class="spgrid">' + ''.join(cards) + '</div>'
            '<p class="spnote">示意圖由本站依版主筆記與魚子醬 P3 詳解重新繪製，位置為示意；「看原圖」是原影片截圖。</p></div></section>')


# ================= P4 =================
def p4_open():
    A, Cc = pt(0, .9), pt(180, .9)
    ex = [wm(0, 'A', '#ff6b6b'), wm(180, 'C', '#6bcBff'),
          boss(C, C - 52, 'boss'), tag(C + 22, C - 66, 'MT 拉向 A 點', 'start', '#cbd5e1'),
          me(A[0], A[1] + 6, '光', '#f5c542'), tag(A[0] + 14, A[1] + 10, '大光：A 點方向貼邊', 'start'),
          me(Cc[0], Cc[1] - 4, '暗', '#7c3aed'), tag(Cc[0] + 14, Cc[1] + 2, '大暗：C 點正中', 'start'),
          me(C - 16, C + 50, '小'), me(C + 2, C + 44, '小'), me(C + 18, C + 52, '小'),
          tag(C - 30, C + 30, '其他 6 人：C 點上方集合', 'start', '#cbd5e1'),
          tag(C - 30, C + 72, '小暗盡量靠近大暗', 'start', '#cbd5e1')]
    return arena(ex, top='上為 A 點', bottom='先處理動靜，再去 debuff 位置')


def p4_guide():
    ex = [wm(0, 'A', '#ff6b6b'), wm(180, 'C', '#6bcBff'),
          f'<line x1="{C-R+6}" y1="{C}" x2="{C+R-6}" y2="{C}" stroke="#b9975b" stroke-dasharray="4 3"/>',
          me(C - 30, C - 40), me(C + 2, C - 56, 'MT', MT), me(C + 32, C - 40, 'H', '#16a34a'), me(C - 2, C - 26, 'H', '#16a34a'),
          me(C - 30, C + 40, 'D', '#a16207'), me(C, C + 56, 'D', '#a16207'), me(C + 30, C + 40, 'D', '#a16207'), me(C + 2, C + 26, 'D', '#a16207'),
          tag(C, C - 76, '分散：T 和補師往上'), tag(C, C + 82, 'DPS 往下', 'middle', '#cbd5e1')]
    return arena(ex, top='制導 ×2：分散或兩人分攤，順序隨機', bottom='分攤：盡量 3～5 人一組')


P4PANELS = [
    ('00:00', '終審判決（看自己的 debuff）', p4_open,
     ['<b>大光</b> → A 點方向盡量貼邊；<b>大暗</b> → C 點正中',
      '<b>小光、小暗</b>（其他 6 人）→ C 點上方集合，小暗盡量靠近大暗',
      '大光或大暗死掉會連帶小光／小暗一起死＝團滅'], 'p4_open'),
    ('00:07', '動靜 ×2', None,
     ['<b>禁止命令（靜）</b>：讀條過半前按 ESC 取消選中，然後完全不動，連打字都不行',
      '<b>行動命令（動）</b>：一直移動或原地一直跳',
      '動靜判定後還有約 3 秒可以去 debuff 位置'], None),
    ('00:27', '制導 ×2', p4_guide,
     ['<b>分散</b>：ST 和 T、補師往上半場',
      '<b>分攤</b>：盡量 3～5 人一組，單吃會有全場 AOE'], 'p4_stack'),
    ('00:48', '一測（看自己的影子）', None,
     ['讀條時找沒人的地方看自己的影子，影子身上的特效就是等等被點的機制',
      '大圈 → 沒雷射的分身面前、圓形中間；電 → C 點旁沒雷射的安全區左邊；分攤和沒點名 → 同區右邊'], 'p4_obs1'),
    ('01:39', '第一次死刑：雙 T 分攤', None,
     ['加重誅罰打一仇 3 下，<b>雙 T 一起分攤</b>',
      'ST：<b>極致護衛＋鐵壁＋聖盾陣</b>，再給團隊<b>雪仇</b>',
      '三下打完雙 T 分開；<b>誅罰讀條結束前換好 T</b>，讓 MT 滿血吃誅罰'], 'p4_tb1'),
    ('02:03', '二測（看自己的影子）', None,
     ['大光 → A 點方向貼邊；大暗 → B 點；小光 → 大暗左上；小暗依近線／遠線／無點名分到大暗旁邊',
      '先處理 5 人分攤和超級跳，再光上暗下四四分攤，最後去月環分身腳下',
      '中間的分攤／分散開<b>聖光幕簾</b>'], 'p4_obs2_light'),
    ('03:18', '第二次死刑', None,
     ['照團隊安排誰吃；ST 的神聖領域<b>留到第三次</b>'], None),
    ('03:37', '地火 ①（三穿一）＋株連 ①', None,
     ['三穿一：第一火在左、第二火在右，第三火一定在中間，從中間穿到左邊',
      '株連 ① 開<b>雪仇</b>（目標減要在株連讀條結束前下）',
      '<b>株連讀條快到一半就挑釁</b>，準備吃第三次死刑'], 'p4_fire1'),
    ('04:03', '第三次死刑：ST 無敵', None,
     ['看到 <b>boss 背後發光</b>就按<b>神聖領域</b>',
      '吃完記得<b>退避</b>，接著雙 T 分散'], None),
    ('04:23', '地火 ②＋株連 ②', None,
     ['<b>聖光幕簾</b>要蓋到株連 ②',
      '地火結束站好定位後，株連讀條結束前開<b>武裝戍衛</b>'], 'p4_fire2'),
    ('04:54', '籠子', None,
     ['從 A、B 之間的籠子開始順時針落下，照隊伍排的順序（DPS 由低到高）踩 1～8 號',
      '籠子落下時裡面沒人＝團滅'], 'p4_cage'),
]


def section_p4():
    cards = []
    for t, title, fn, lines, fig in P4PANELS:
        body = fn() if fn else ''
        li = ''.join(f'<li>{x}</li>' for x in lines)
        figb = f'<button class="figbtn" type="button" data-fig="{fig}">看原圖</button>' if fig else ''
        cards.append(f'<article class="sp{" txt" if not fn else ""}"><h4><span class="st">{t}</span>{title}{figb}</h4>{body}<ul>{li}</ul></article>')
    return ('<section class="step nofig" id="stpaths4"><div><h3 class="sh">P4 騎士 ST 一圖流</h3>'
            '<p class="spnote">照時間順序列出 ST 這一 P 要去哪、開什麼。終審判決、一測、二測看自己的 debuff，所以列出每種情況；藍色是 ST。時間是 P4 開始後的時間。</p>'
            '<div class="spgrid">' + ''.join(cards) + '</div>'
            '<p class="spnote">示意圖由本站依版主筆記與魚子醬 P4 詳解重新繪製，位置為示意；「看原圖」是原影片截圖。</p></div></section>')


if __name__ == '__main__':
    open('/home/claude/work/stpaths_preview.html', 'w', encoding='utf8').write('<!doctype html><meta charset=utf-8><body style="font-family:sans-serif;background:#f6f1e7;color:#222;max-width:1100px;margin:20px auto">' + section())
    open('/home/claude/work/stpaths4_preview.html', 'w', encoding='utf8').write('<!doctype html><meta charset=utf-8><body style="font-family:sans-serif;background:#1a1d27;color:#e6eaf2;max-width:1100px;margin:20px auto">' + section().split('<section')[0] + section_p4())
