"""次元斷絕（34 固定）各號碼跑位一圖流：自繪 SVG。
依據：ぬけまる 次元斷絕解說（11:05～15:32）的站位、懺悔順序、骰子處理順序與親疏自行時機。"""
import math

R = 100
C = 120


def pt(deg, r):
    a = math.radians(deg)
    return (C + r * R * math.sin(a), C - r * R * math.cos(a))


P = {
    'NW': pt(318, .86), 'NE': pt(42, .86), 'SW': pt(222, .86), 'SE': pt(138, .86),
    'SWin': pt(222, .66), 'SEin': pt(138, .66),
    'NWlow': pt(296, .9), 'NElow': pt(64, .9),
    'W': pt(270, .9), 'E': pt(90, .9),
    'Wnear': pt(262, .78), 'Enear': pt(98, .78),
    'mid': (C, C),
}

# 每個號碼：顏色側、步驟（位置鍵, 說明）
SIDE = {1: 'o', 2: 'e', 3: 'o', 4: 'e', 5: 'o', 6: 'e', 7: 'o', 8: 'e'}


def steps(n):
    o = SIDE[n] == 'o'
    S = lambda a, b: a if o else b  # noqa
    side = S('左', '右')
    if n in (1, 2):
        return [
            (S('NW', 'NE'), f'開場站{S("左上（西北）", "右上（東北）")}紅點' + ('，<b>正面朝外圈</b>' if n == 1 else '')),
            (S('NW', 'NE'), f'第一輪骰子：{S("阿爾法之劍（扇形）", "突進")}，紅點站好就開親疏自行'),
            (S('W', 'E'), f'直接到{S("左邊", "右邊")}那側的懺悔（偏上或偏下，看出在哪），踩<b>第 3 次懺悔</b>'),
            ('mid', '回中央，照職責分攤淨化熱線'),
        ]
    if n in (3, 4):
        return [
            (S('SWin', 'SEin'), f'站{S("左下（西南）", "右下（東南）")}紅點<b>靠場內的那一側</b>，不管正義號在哪都固定'),
            (S('SWin', 'SEin'), '正義號超級跳最遠的人：<b>3、4 號只有離正義號遠的那一個會吃</b>，被跳的人正義號跳時開親疏自行'),
            (S('SW', 'SE'), '<b>被跳之後往外一步</b>站到紅點上，躲正義號接下來的攻擊'),
            (S('SW', 'SE'), f'第二輪骰子：{S("阿爾法之劍（扇形）", "突進")}，<b>留在紅點處理</b>'),
            (S('Wnear', 'Enear'), S('扇形打完就往 9 點附近移動，躲亞歷山大的<b>十字聖禮（大十字）</b>',
                                    '<b>飛機衝到一半就要開始跑</b>，往 3 點附近躲亞歷山大的<b>十字聖禮（大十字）</b>，非常急')),
            ('mid', '回中央，照職責分攤淨化熱線'),
        ]
    if n in (5, 6):
        return [
            (S('NWlow', 'NElow'), f'開場站{S("左上，比 1 號稍微下面", "右上，比 2 號稍微下面")}'),
            (S('W', 'E'), f'輪鋸飛出後直接到{S("左邊", "右邊")}那側的懺悔（偏上或偏下），踩<b>第 1 次懺悔</b>，踩完開親疏自行'),
            (S('NW', 'NE'), f'到{S("左上（西北）", "右上（東北）")}紅點，第三輪骰子：{S("阿爾法之劍（扇形）", "突進")}'),
            ('mid', '回中央，照職責分攤淨化熱線'),
        ]
    return [
        (S('NWlow', 'NElow'), f'開場站{S("左上，比 1 號稍微下面（和 5 號一起）", "右上，比 2 號稍微下面（和 6 號一起）")}'),
        (S('W', 'E'), f'輪鋸飛出後直接到{S("左邊", "右邊")}那側的懺悔（偏上或偏下）旁待命'),
        (S('W', 'E'), '踩<b>第 2 次懺悔</b>，踩完開親疏自行'),
        (S('SW', 'SE'), f'回{S("左下（西南）", "右下（東南）")}紅點（3、4 號原本的位置）引導飛機，第四輪骰子：{S("阿爾法之劍（扇形）", "突進")}'
                        + ('。<b>懺悔在比較上面時距離很遠，幾乎來不及到定位</b>，但<b>面朝外圈</b>和<b>親疏自行防擊退</b>一定要記得' if n == 7 else '。7 號先處理、8 號後處理，時間比 7 號充裕')),
        ('mid', '回中央，照職責分攤淨化熱線'),
    ]


CIRC = '①②③④⑤⑥'


def svg(n):
    col = '#3b82f6' if SIDE[n] == 'o' else '#e11d48'
    st = steps(n)
    out = [f'<svg viewBox="0 0 240 250" role="img" aria-label="{n} 號跑位圖" xmlns="http://www.w3.org/2000/svg">']
    out.append('<defs><marker id="ah%d" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="%s"/></marker></defs>' % (n, col))
    out.append(f'<circle cx="{C}" cy="{C}" r="{R}" fill="#3b3428" stroke="#b9975b" stroke-width="3"/>')
    out.append(f'<circle cx="{C}" cy="{C}" r="{R*.55}" fill="none" stroke="#6b5a3e" stroke-width="1" stroke-dasharray="3 3"/>')
    # red dots
    for k in ('NW', 'NE', 'SW', 'SE'):
        x, y = P[k]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#c0392b" stroke="#fff" stroke-width="1"/>')
    # 懺悔：左右各一個，偏上或偏下隨機（虛線＝可能的位置）
    for deg in (292, 248, 68, 112):
        x, y = pt(deg, .9)
        out.append(f'<rect x="{x-8:.1f}" y="{y-8:.1f}" width="16" height="16" rx="3" fill="rgba(167,139,250,.18)" stroke="#a78bfa" stroke-width="1.6" stroke-dasharray="3 2"/>')
    # bosses
    out.append(f'<text x="{C}" y="{C+R+14}" text-anchor="middle" font-size="10" fill="currentColor">▲ 亞歷山大（固定在下）</text>')
    out.append(f'<text x="{C}" y="12" text-anchor="middle" font-size="9.5" fill="currentColor">正義號・追擊者：左上或右上（隨機）</text>')
    # path
    pts = []
    for k, _ in st:
        p = P[k]
        if not pts or pts[-1] != p:
            pts.append(p)
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        out.append(f'<line x1="{a[0]+ux*9:.1f}" y1="{a[1]+uy*9:.1f}" x2="{b[0]-ux*10:.1f}" y2="{b[1]-uy*10:.1f}" stroke="{col}" stroke-width="2.5" marker-end="url(#ah{n})"/>')
    # step badges (group same positions)
    lab = {}
    for i, (k, _) in enumerate(st):
        lab.setdefault(P[k], []).append(CIRC[i])
    for (x, y), ls in lab.items():
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{col}" stroke="#fff" stroke-width="1.5"/>')
        out.append(f'<text x="{x:.1f}" y="{y+3.5:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">{n}</text>')
        tx = x + (12 if x < C else -12)
        anc = 'start' if x < C else 'end'
        if abs(x - C) < 1:
            tx, anc = x + 12, 'start'
        out.append(f'<text x="{tx:.1f}" y="{y-8:.1f}" text-anchor="{anc}" font-size="11" font-weight="700" fill="#ffe08a" stroke="#000" stroke-width="2.5" paint-order="stroke">{"".join(ls)}</text>')
    out.append('</svg>')
    return ''.join(out)


def section():
    cards = []
    for n in range(1, 9):
        li = ''.join(f'<li><b>{CIRC[i]}</b> {t}</li>' for i, (_, t) in enumerate(steps(n)))
        cards.append(f'<article class="dp"><h4><span class="dn {"o" if SIDE[n]=="o" else "e"}">{n}</span> 號</h4>{svg(n)}<ol>{li}</ol></article>')
    css = """<style>
.dpgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:10px}
.dp{border:1px solid var(--line,#ddd);border-radius:10px;padding:10px;background:var(--panel,transparent)}
.dp h4{margin:0 0 6px;font-size:1rem;display:flex;align-items:center;gap:6px}
.dp .dn{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;color:#fff;font-weight:800}
.dp .dn.o{background:#3b82f6}.dp .dn.e{background:#e11d48}
.dp svg{width:100%;height:auto;display:block;color:var(--muted,#888)}
.dp ol{list-style:none;margin:6px 0 0;padding:0;font-size:.85rem;line-height:1.55}
.dp ol li{margin:2px 0}
.dpnote{font-size:.8rem;color:var(--muted,#888);margin:6px 0 0}
</style>"""
    return (css + '<section class="step nofig" id="dimpaths"><div><h3 class="sh">次元斷絕：1～8 號跑位一圖流</h3>'
            '<p class="dpnote">上為北，亞歷山大固定在南（下）。懺悔之間固定一左一右，但每邊會<b>隨機偏上或偏下</b>（圖上虛線框是兩種可能的位置），踩懺悔的人看當下出在哪就去哪。奇數（藍）走左邊、偶數（紅）走右邊；圓圈數字是步驟順序。'
            '骰子處理順序：1→2→3→4→5→6→7→8，奇數吃追擊者的阿爾法之劍（扇形，面朝外圈），偶數吃突進。超級跳只會跳 3、4 號裡離正義號遠的一個人。4 號的飛機突進之後緊接著亞歷山大的十字聖禮（大十字），3 號扇形打完就走，4 號飛機衝到一半就要跑。'
            '最後的淨化熱線照職責分攤：雙 T＋讀秒 DPS 在中央偏上、雙補＋讀秒 DPS 在中央偏下，沒讀秒的 DPS 不要進。</p>'
            '<div class="dpgrid">' + ''.join(cards) + '</div>'
            '<p class="dpnote">示意圖由本站依 ぬけまる 次元斷絕解說（34 固定，原案ハムカツ）重新繪製，位置為示意，實際請對照影片。</p></div></section>')


if __name__ == '__main__':
    open('/home/claude/work/dimpaths_preview.html', 'w', encoding='utf8').write('<!doctype html><meta charset=utf-8><body style="font-family:sans-serif;background:#f6f1e7;color:#222;max-width:1100px;margin:20px auto">' + section())
