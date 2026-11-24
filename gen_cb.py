"""Generate blank-note data (rows grouped, tc names, ①② counts) and per-time tags
from cactbot timeline (.txt) + triggers/translations (.ts)."""
import re, json, sys, os
W = '/home/claude/work/'
CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'

RESP = {
    'tankBuster': '死刑', 'tankBusterSwap': '死刑換T', 'sharedTankBuster': '雙T分攤死刑',
    'tankCleave': '扇形死刑', 'aoe': 'AOE', 'bigAoe': '高傷AOE',
    'stackMarker': '分攤', 'stackMarkerOn': '分攤', 'stackMiddle': '分攤',
    'spread': '分散', 'knockback': '擊退', 'getOut': '遠離', 'getIn': '靠近',
    'getUnder': '貼近Boss', 'lookAway': '背對',
}
DROP_PAREN = ['(詠唱)', '(傷害)', '(命中)', '(跳)', '(預兆)', '(cast)', '(damage)', '(hit)', '(hits)', '(jump)', '(telegraphs)', '(telegraph)']


def load_tc(ts):
    a = ts.index("'locale': 'tc'")
    b = ts.index("'replaceText': {", a)
    c = ts.index('\n      },', b)
    body = ts[b:c]
    pairs = re.findall(r"^\s*'((?:[^'\\]|\\.)*)': '((?:[^'\\]|\\.)*)',", body, re.M)
    sync_body = ts[a:b]
    sync = dict(re.findall(r"'((?:[^'\\]|\\.)*)': '((?:[^'\\]|\\.)*)'", sync_body))
    out = []
    for k, v in pairs:
        k = k.replace("\\'", "'").replace('\\\\', '\\')
        out.append((re.compile(k), v.replace("\\'", "'")))
    out.sort(key=lambda kv: -len(kv[0].pattern))
    return out, sync


def trigger_tags(ts):
    """ability id -> set of tags from Responses.* triggers"""
    tags = {}
    for blk in re.split(r"\n    \{\n      id: '", ts):
        m = re.search(r'response: Responses\.(\w+)\(', blk)
        if not m or m.group(1) not in RESP:
            continue
        n = re.search(r"netRegex: \{[^}]*?id: (\[[^\]]*\]|'[^']*')", blk)
        if not n:
            continue
        typ = re.search(r"type: '(\w+)'", blk)
        for i in re.findall(r"'([0-9A-F]{4,5})'", n.group(1)):
            tags.setdefault(i, []).append(RESP[m.group(1)])
    return tags


def parse(txt):
    """linear walk; takes first branch, follows forcejump"""
    lines = txt.split('\n')
    stop = next((i for i, l in enumerate(lines) if l.startswith('# IGNORED') or l.startswith('# ALL ENCOUNTER')), len(lines))
    lines = lines[:stop]
    labels = {}
    for i, l in enumerate(lines):
        m = re.match(r'^(\d+(?:\.\d+)?)\s+label\s+"([^"]+)"', l)
        if m:
            labels[m.group(2)] = (i, float(m.group(1)))
    ev = []
    i, off, skip_first = 0, 0.0, False
    seen_jump = set()
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^(\d+(?:\.\d+)?)\s+"([^"]*)"(.*)$', l)
        if m:
            t = float(m.group(1)) + off
            name, rest = m.group(2), m.group(3)
            if skip_first:
                skip_first = False
            elif not name.startswith('--') and name.strip():
                ids = re.findall(r'[0-9A-F]{4,5}', rest.split('#')[0] + (rest.split('#')[1] if '#' in rest else ''))
                ev.append((t, name, ids))
            fj = re.search(r'forcejump "([^"]+)"', rest)
            if fj and fj.group(1) in labels and fj.group(1) not in seen_jump:
                seen_jump.add(fj.group(1))
                li, lt = labels[fj.group(1)]
                off = t - lt
                i = li + 1
                skip_first = True  # the label's first line is the same cast as the jump line
                continue
            if re.search(r'\bjump 0\b|forcejump', rest) and not fj:
                pass
        i += 1
    return ev


PRE = [('(stun for enrage)', '(enrage)'), ('(enrage cast)', '(enrage)'), ('(adds enrage)', '(小怪狂暴)'),
       ('Mana Explosion', '魔力爆炸'), ('Quadroboom Bombarian Special', '四分超豪華野蠻大亂擊')]
POST = [('(狂暴)', '（狂暴）'), ('(enrage)', '（狂暴）'), ('Enrage', '狂暴'), ('(處理 Debuff)', '處理 Debuff')]


def tr(name, pats):
    s = name
    for a, b in PRE:
        s = s.replace(a, b)
    for p, v in pats:
        s = p.sub(v, s)
    for d in DROP_PAREN:
        s = s.replace(' ' + d, '').replace(d, '')
    s = re.sub(r'\s*\((一|二|三|四|五|六|七|八)\)', '', s)
    s = re.sub(r'\s*\(圈 ?\d+\)', '', s)
    for a, b in POST:
        s = s.replace(a, b)
    s = s.replace('/', '／').replace(' x', ' ×').replace(' + ', '＋').replace(' (', '（').replace('(', '（').replace(')', '）').strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def fmt(t):
    t = max(0, round(t))
    return f'{t // 60:02d}:{t % 60:02d}'


def build(rid, label, title_part):
    txt = open(W + f'cb/{rid}.txt', encoding='utf8').read()
    ts = open(W + f'cb/{rid}.ts', encoding='utf8').read()
    pats, sync = load_tc(ts)
    ttag = trigger_tags(ts)
    ev = parse(txt)
    rows = []  # dict t, last, name, n, tags
    for t, name, ids in ev:
        nm = tr(name, pats)
        # numbered variants like "Wicked Blaze 2" -> merge into base
        base = re.sub(r'\s*\d+$', '', nm) if re.search(r'[^\d×]\s*\d$', nm) else nm
        tags = []
        for i in ids:
            for g in ttag.get(i, []):
                if g not in tags:
                    tags.append(g)
        # merge with recent same-name row
        hit = None
        for r in reversed(rows[-4:]):
            if r['name'] == base and t - r['last'] <= 6.5:
                hit = r
                break
        if hit:
            hit['last'] = t; hit['n'] += 1
            for g in tags:
                if g not in hit['tags']:
                    hit['tags'].append(g)
            continue
        # same instant, different name -> combine
        if False and rows and rows[-1]['name'] != base and '＋' not in rows[-1]['name']:
            r = rows[-1]
            r['name'] = r['name'] + '＋' + base
            for g in tags:
                if g not in r['tags']:
                    r['tags'].append(g)
            continue
        rows.append(dict(t=t, last=t, name=base, n=1, tags=tags))
    # enrage handling
    for r in rows:
        if re.search(r'enrage|Enrage', r['name']) or '狂暴' in r['name']:
            r['tags'] = ['狂暴']
    # drop duplicate row just before an enrage row at the same second
    keep = []
    for r in rows:
        if keep and r['tags'] == ['狂暴'] and round(keep[-1]['t']) == round(r['t']):
            keep.pop()
        keep.append(r)
    rows = keep
    # occurrence counts
    total = {}
    for r in rows:
        total[r['name']] = total.get(r['name'], 0) + 1
    cnt = {}
    out_rows = []
    for r in rows:
        nm = r['name']
        cnt[nm] = cnt.get(nm, 0) + 1
        m = nm
        if r['tags'] == ['狂暴']:
            pass
        elif r['n'] >= 3:
            m += f'（×{r["n"]}）'
        elif r['n'] == 2:
            m += '（×2）'
        if total[nm] > 1:
            m += ' ' + CIRC[min(cnt[nm], 20) - 1]
        out_rows.append(dict(t=fmt(r['t']), sec=r['t'], m=m, base=nm, tags=r['tags']))
    # dedupe identical display times (shift is not wanted; keep both, HINT_T keyed by time merges)
    # grouping: split at gaps
    groups, cur = [], []
    for i, r in enumerate(out_rows):
        if cur:
            gap = r['sec'] - out_rows[i - 1]['sec']
            if (len(cur) >= 6 and gap >= 7) or len(cur) >= 11 or (len(cur) >= 3 and gap >= 18):
                groups.append(cur); cur = []
        cur.append(r)
    if cur:
        groups.append(cur)
    # group names: first non-AOE-ish mechanic
    gnames = []
    for g in groups:
        cand = [r for r in g if r['tags'] not in (['AOE'], ['高傷AOE'])] or g
        gnames.append(cand[0]['base'])
    js = ['const data = [']
    hint_t = {}
    for gi, (g, gn) in enumerate(zip(groups, gnames)):
        head = (f'part:{json.dumps(title_part, ensure_ascii=False)}, ' if gi == 0 else '') + f'g:{json.dumps(gn, ensure_ascii=False)}'
        rs = ',\n'.join('  {t:%s,m:%s,c:[]}' % (json.dumps(r['t']), json.dumps(r['m'], ensure_ascii=False)) for r in g)
        js.append('{' + head + ', rows:[\n' + rs + '\n]}' + (',' if gi < len(groups) - 1 else ''))
        for r in g:
            if r['tags']:
                hint_t.setdefault(r['t'], [])
                for x in r['tags']:
                    if x not in hint_t[r['t']]:
                        hint_t[r['t']].append(x)
    js.append('];')
    os.makedirs(W + label, exist_ok=True)
    open(W + f'{label}/data.js', 'w', encoding='utf8').write('\n'.join(js) + '\n')
    json.dump(hint_t, open(W + f'{label}/hint_t.json', 'w', encoding='utf8'), ensure_ascii=False)
    eng = sorted({r['m'] for r in out_rows if re.search(r'[A-Za-z]{3,}', r['m'])})
    print(label, len(out_rows), 'rows', len(groups), 'groups', 'tags', len(hint_t), 'boss', sync)
    if eng:
        print('  ENGLISH LEFT:', eng)


if __name__ == '__main__':
    for rid, lab, part in [('r1s', 'm1s', 'M1S 黑貓'), ('r2s', 'm2s', 'M2S 蜂蜂小甜心'), ('r3s', 'm3s', 'M3S 野蠻炸彈'),
                           ('r4s', 'm4s', 'M4S 狡雷'), ('r6s', 'm6s', 'M6S 糖彩狂潮'), ('r7s', 'm7s', 'M7S 野蠻憎惡')]:
        build(rid, lab, part)
