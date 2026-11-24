"""Blank-note data for ultimates and AAC heavyweight from cactbot, handling
branches (jump/forcejump), enrage sequences and per-phase clocks."""
import re, json, os, sys
import opencc
sys.path.insert(0, '/home/claude/work')
from gen_cb import trigger_tags, RESP, CIRC  # noqa
W = '/home/claude/work/'
S2T = opencc.OpenCC('s2t')
BAD = re.compile(r'enrage|wipe|fail|reset', re.I)
DROP = ['(cast)', '(damage)', '(hit)', '(hits)', '(jump)', '(telegraphs)', '(telegraph)', '(詠唱)', '(傷害)', '(命中)', '(跳)', '(预兆)', '(預兆)',
        '(咏唱)', '(伤害)', '(判定)']


def _pairs(ts, loc):
    a = ts.index(f"'locale': '{loc}'")
    b = ts.index("'replaceText': {", a)
    c = ts.index('\n      },', b)
    out = []
    for k, v in re.findall(r"^\s*'((?:[^'\\]|\\.)*)': '((?:[^'\\]|\\.)*)',", ts[b:c], re.M):
        k = k.replace("\\'", "'").replace('\\\\', '\\')
        v = v.replace("\\'", "'")
        if loc == 'cn':
            v = S2T.convert(v)
        try:
            out.append((re.compile(k, re.I), v))
        except re.error:
            pass
    out.sort(key=lambda kv: -len(kv[0].pattern))
    return out


def load_tr(ts):
    loc = 'tc' if "'locale': 'tc'" in ts else 'cn'
    pats = _pairs(ts, loc)
    if loc == 'tc' and "'locale': 'cn'" in ts:
        pats = pats + _pairs(ts, 'cn')
    return pats, loc


def walk(txt, prefer=None):
    lines = txt.split('\n')
    stop = next((i for i, l in enumerate(lines) if l.startswith('# IGNORED') or l.startswith('# ALL ENCOUNTER')), len(lines))
    lines = lines[:stop]
    labels = {}
    for i, l in enumerate(lines):
        m = re.match(r'^(\d+(?:\.\d+)?)\s+label\s+"([^"]+)"', l)
        if m:
            labels[m.group(2)] = (i, float(m.group(1)))
    ev, i, off, used = [], 0, 0.0, set()
    skipped_alts = set()
    steps = 0
    newphase, lastraw = False, 0.0
    while i < len(lines) and steps < 20000:
        steps += 1
        l = lines[i]
        lm = re.match(r'^(\d+(?:\.\d+)?)\s+label\s+"([^"]+)"', l)
        if lm and lm.group(2) in skipped_alts:
            # fell into an alternative branch we did not take: skip to next label not in that set
            j = i + 1
            while j < len(lines):
                m2 = re.match(r'^(\d+(?:\.\d+)?)\s+label\s+"([^"]+)"', lines[j])
                if m2 and m2.group(2) not in skipped_alts:
                    break
                j += 1
            if j >= len(lines):
                break
            last = ev[-1][0] if ev else 0
            off = (last + 6) - float(re.match(r'^(\d+(?:\.\d+)?)', lines[j]).group(1))
            i = j + 1
            continue
        if lm and BAD.search(lm.group(2)):
            break  # reached an enrage/wipe block by fall-through
        m = re.match(r'^(\d+(?:\.\d+)?)\s+"([^"]*)"(.*)$', l)
        if not m:
            i += 1
            continue
        wm = re.search(r'window (\d+(?:\.\d+)?)', m.group(3))
        if wm and float(wm.group(1)) >= 100 and ev and float(m.group(1)) - lastraw > 30:
            newphase = True
        lastraw = float(m.group(1))
        t = float(m.group(1)) + off
        name, rest = m.group(2), m.group(3)
        code = rest.split('#')[0] if not rest.strip().startswith('#') else ''
        if not name.startswith('--') and name.strip():
            ids = re.findall(r'[0-9A-F]{4,5}', rest)
            ev.append((t, name, ids, newphase, float(m.group(1))))
            newphase = False
        # jumps on this line and siblings at the same raw time
        raw = float(m.group(1))
        cands, forced = [], None
        k = i
        while k < len(lines):
            mk = re.match(r'^(\d+(?:\.\d+)?)\s+"[^"]*"(.*)$', lines[k])
            if not mk or abs(float(mk.group(1)) - raw) > 0.01:
                if k > i:
                    break
            if mk:
                for fj in re.finditer(r'(force)?jump\s+(?:"([^"]+)"|(\d+(?:\.\d+)?))', mk.group(2).split(' #')[0]):
                    tgt = fj.group(2) or fj.group(3)
                    if fj.group(1):
                        forced = tgt
                    else:
                        cands.append(tgt)
            k += 1
        target = None
        if forced:
            target = forced
        else:
            good = [c for c in cands if not BAD.search(c) and c != '0'] if raw > 1.0 else []
            if prefer:
                good.sort(key=lambda c: 0 if c in prefer else 1)
            if good:
                target = good[0]
                skipped_alts |= set(good[1:])
        if target and (target, round(raw, 1)) not in used:
            pass
        if target and (target, round(raw, 1)) not in used:
            used.add((target, round(raw, 1)))
            if target in labels and labels[target][0] < i:
                target = None
            if target and target in labels:
                li, lt = labels[target]
                off = t - lt
                lastraw = lt
                i = li + 1
                # drop events at the same instant as the jump line already recorded (label's first line repeats it)
                continue
            elif target and re.match(r"^\d", target):
                tv = float(target)
                if tv > raw:
                    j = next((x for x in range(len(lines)) if re.match(r'^(\d+(?:\.\d+)?)\s', lines[x]) and float(re.match(r'^(\d+(?:\.\d+)?)', lines[x]).group(1)) >= tv - 0.01), None)
                    if j is not None:
                        off = t - tv
                        lastraw = tv
                        i = j
                        continue
        i = k if k > i + 1 else i + 1
    # dedupe identical (time,name) produced by jump landing
    out = []
    for e in ev:
        if out and abs(out[-1][0] - e[0]) < 0.05 and out[-1][1] == e[1]:
            if e[3]:
                out[-1] = out[-1][:3] + (True, out[-1][4])
            continue
        out.append(e)
    return out


def tr(name, pats):
    s = name
    for p, v in pats:
        s = p.sub(v, s)
    for d in DROP:
        s = s.replace(' ' + d, '').replace(d, '')
    s = re.sub(r'\s*\((一|二|三|四|五|六|七|八|\d)\)', '', s)
    for a, b in [('Blue Screen', '藍屏'), ('Run: ****mi*', '代碼：＊能＊'), ('Wild Charge', '衝鋒分攤'), (' Baits', ' 誘導'), (' Stack', ' 分攤'),
                 ('(stacks)', '(分攤)'), (' Far', ' 遠'), (' Near', ' 近'), (' Puddle', ' 圈'), ('(Healer)', '(補師)'), ('(boss', '(Boss'),
                 ('Sabik', '薩比克'), ('"Start"', '開始')]:
        s = s.replace(a, b)
    if s == 'Start':
        s = '開怪'
    s = s.replace('(enrage)', '（狂暴）').replace('Enrage', '狂暴').replace('enrage', '狂暴')
    s = s.replace('/', '／').replace(' x', ' ×').replace(' + ', '＋').replace(' (', '（').replace('(', '（').replace(')', '）').strip()
    s = re.sub(r'\s+', ' ', s)
    if s.startswith('（') and s.endswith('）') and s.count('（') == 1:
        s = s[1:-1]
    return s


def fmt(t):
    t = max(0, round(t))
    return f'{t // 60:02d}:{t % 60:02d}'


WORDS = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7'}


def phase_bounds(txt, pats, manual=None):
    if manual:
        return [(rb, nm) for rb, nm in manual]
    lines = txt.split('\n')
    out = []
    for i, l in enumerate(lines):
        if l.startswith('# IGNORED') or l.startswith('# ALL ENCOUNTER') or re.match(r'^# P\d IGNORED|^# .*Enrage', l, re.I):
            if 'IGNORED' in l:
                break
            continue
        m = re.match(r'^#+\s*(?:Phase\s*([\d.]+|One|Two|Three|Four|Five|Six|Seven)|P(\d(?:\.\d)?))\b\s*[:\-–]?\s*(.*?)\s*#*\s*$', l, re.I)
        add = re.match(r'^#+\s*Adds Phase', l, re.I)
        if not (m or add):
            continue
        j = i + 1
        while j < len(lines) and not re.match(r'^\d', lines[j]):
            j += 1
        if j >= len(lines):
            continue
        rb = float(re.match(r'^(\d+(?:\.\d+)?)', lines[j]).group(1))
        if add:
            nm = '小怪階段'
            prev = out[-1][1].split(' ')[0] if out else 'P1'
            nm = prev + '.5 小怪'
        else:
            num = m.group(1) or m.group(2)
            num = WORDS.get(num.lower(), num)
            rest = tr(m.group(3) or '', pats).strip('"「」 ')
            rest = re.sub(r'[A-Za-z].*$', '', rest).strip(' ,，、') if re.search(r'[A-Za-z]{3,}', rest) else rest
            nm = ('P' + num + (' ' + rest if rest else '')).strip()
        if out and abs(out[-1][0] - rb) < 0.01:
            continue
        out.append((rb, nm))
    if out and out[0][1].startswith('P1') and not out[0][1].startswith('P1.'):
        out[0] = (0.0, out[0][1])
    if not out or out[0][0] > 0:
        out.insert(0, (0.0, 'P1'))
    return out


def build(src, label, phases_mode, phase_names=None, min_gap=45, manual=None):
    txt = open(W + f'cb/{src}.txt', encoding='utf8').read()
    ts = open(W + f'cb/{src}.ts', encoding='utf8').read()
    pats, loc = load_tr(ts)
    ttag = trigger_tags(ts)
    ev = walk(txt, PREFER.get(label))
    rows = []
    bounds = phase_bounds(txt, pats, manual)
    if NAMES.get(label):
        if len(NAMES[label]) == len(bounds):
            bounds = [(rb, nm) for (rb, _), nm in zip(bounds, NAMES[label])]
        else:
            print('  PHASE COUNT MISMATCH', label, [b[1] for b in bounds])
    for t, name, ids, np_, raw in ev:
        ph_i = max([k for k, (rb, _) in enumerate(bounds) if rb <= raw + 0.01] or [0])
        nm = tr(name, pats)
        base = re.sub(r'\s*\d+$', '', nm) if re.search(r'[^\d×]\s*\d$', nm) else nm
        base = re.sub(r'\s+\d+（[^）]*）$', '', base)
        tags = []
        for i in ids:
            for g in ttag.get(i, []):
                if g not in tags:
                    tags.append(g)
        hit = None
        for r in ([] if (rows and rows[-1]['ph'] != ph_i) else reversed(rows[-4:])):
            if r['name'] == base and t - r['last'] <= 6.5:
                hit = r
                break
        if hit:
            hit['last'] = t; hit['n'] += 1
            for g in tags:
                if g not in hit['tags']:
                    hit['tags'].append(g)
            continue
        rows.append(dict(t=t, last=t, name=base, n=1, tags=tags, ph=ph_i))
    for r in rows:
        if '狂暴' in r['name']:
            r['tags'] = ['狂暴']
    # phases
    phases = [[]]
    for r in rows:
        if phases_mode and phases[-1] and r['ph'] != phases[-1][-1]['ph']:
            phases.append([])
        phases[-1].append(r)
    if not phases_mode:
        phases = [rows]
    total = {}
    for r in rows:
        total[r['name']] = total.get(r['name'], 0) + 1
    cnt = {}
    groups = []  # (part or None, gname, rows)
    for pi, ph in enumerate(phases):
        t0 = ph[0]['t'] if (phases_mode and pi > 0) else 0.0
        if phases_mode and pi == 0:
            t0 = 0.0
        disp = []
        for r in ph:
            cnt[r['name']] = cnt.get(r['name'], 0) + 1
            m = r['name']
            if r['tags'] != ['狂暴'] and r['n'] >= 2:
                m += f'（×{r["n"]}）'
            if total[r['name']] > 1:
                m += ' ' + CIRC[min(cnt[r['name']], 20) - 1]
            disp.append(dict(t=fmt(r['t'] - t0), sec=r['t'], m=m, base=r['name'], tags=r['tags']))
        cur = []
        first = True
        for i, r in enumerate(disp):
            if cur:
                gap = r['sec'] - disp[i - 1]['sec']
                if (len(cur) >= 6 and gap >= 7) or len(cur) >= 11 or (len(cur) >= 3 and gap >= 18):
                    groups.append((pi if first else None, cur)); first = False; cur = []
            cur.append(r)
        if cur:
            groups.append((pi if first else None, cur))
    js = ['const data = [']
    hint_t = {}
    pnames = []
    pcount, seenp = 0, {}
    for gi, (pstart, g) in enumerate(groups):
        cand = [r for r in g if r['tags'] not in (['AOE'], ['高傷AOE'])] or g
        gn = cand[0]['base']
        head = ''
        if pstart is not None:
            if phases_mode:
                pn = bounds[ph[0]['ph']][1] if False else bounds[phases[pstart][0]['ph']][1]
            else:
                pn = phase_names[0]
            pnames.append(pn.split(' ')[0])
            head = f'part:{json.dumps(pn, ensure_ascii=False)}, '
        head += f'g:{json.dumps(gn, ensure_ascii=False)}'
        rs = ',\n'.join('  {t:%s,m:%s,c:[]}' % (json.dumps(r['t']), json.dumps(r['m'], ensure_ascii=False)) for r in g)
        js.append('{' + head + ', rows:[\n' + rs + '\n]}' + (',' if gi < len(groups) - 1 else ''))
        if pstart is not None:
            pcount += 1
        for r in g:
            key = f"{pcount}-{r['t']}"
            seenp[key] = seenp.get(key, 0) + 1
            if seenp[key] > 1:
                key += '#' + str(seenp[key])
            if r['tags']:
                hint_t[key] = r['tags']
    js.append('];')
    os.makedirs(W + label, exist_ok=True)
    open(W + f'{label}/data.js', 'w', encoding='utf8').write('\n'.join(js) + '\n')
    json.dump(hint_t, open(W + f'{label}/hint_t.json', 'w', encoding='utf8'), ensure_ascii=False)
    json.dump(dict(loc=loc, phases=pnames if phases_mode else []), open(W + f'{label}/meta.json', 'w'), ensure_ascii=False)
    eng = sorted({r['m'] for g in groups for r in g[1] if re.search(r'[A-Za-z]{3,}', r['m'])})
    print(label, loc, len(rows), 'rows', len(phases), 'phases', [fmt(p[-1]['last'] - (p[0]['t'] if i else 0)) for i, p in enumerate(phases)])
    if eng:
        print('  ENGLISH:', eng[:12])


JOBS = [
    ('unending_coil_ultimate', 'ucob', True), ('ultima_weapon_ultimate', 'uwu', True),
    ('dragonsongs_reprise_ultimate', 'dsr', True), ('the_omega_protocol', 'top', True),
    ('futures_rewritten', 'fru', True), ('dancing_mad', 'dmu', True),
    ('r9s', 'm9s', False), ('r10s', 'm10s', True), ('r11s', 'm11s', True), ('r12s', 'm12s', True),
    ('necron-ex', 'necronx', True),
    ('r4s', 'm4s', True), ('r6s', 'm6s', True), ('r7s', 'm7s', True),
]
NAMES = {
    'uwu': ['P1 迦樓羅', 'P2 伊弗利特', 'P3 泰坦', 'P4 轉場', 'P5 究極武器'],
    'dsr': ['P1 騎士團', 'P1.5 奧爾什方', 'P2 騎神托爾丹', 'P3 尼德霍格', 'P4 邪龍之眼', 'P4.5 奧爾什方', 'P5 騎神托爾丹 II', 'P6 雙龍', 'P6.5 邪龍之眼', 'P7 龍威騎神托爾丹'],
    'top': ['P1 歐米茄', 'P2 歐米茄M／F', 'P3 歐米茄', 'P4 藍屏', 'P5 代碼：＊能＊', 'P6 阿爾法歐米茄'],
    'fru': ['P1 絕命戰士', 'P2 濕婆・米特隆', 'P2.5 小怪', 'P3 暗之巫女', 'P4 雙人', 'P5 潘朵拉・米特隆'],
    'dmu': ['P1 凱夫卡', 'P2 神・凱夫卡', 'P3 卡奧斯＆艾克斯迪司', 'P4 凱夫卡＋卡奧斯＋新生艾克斯迪司', 'P5 凱夫卡'],
    'm12s': ['P1 林德布魯姆', 'P2 林德布魯姆 II'],
}
PREFER = {'necronx': {'solo-phase-tank'}}
MANUAL = {'necronx': [(0, 'P1'), (199, 'P1.5 小怪'), (250, '單人（坦克）'), (1000, 'P2')],
          'm12s': [(0, 'P1'), (3000, 'P2')],
          'm4s': [(0, 'P1 前半'), (396, 'P2 後半')],
          'm6s': [(0, 'P1 前半'), (217, 'P2 小怪'), (428, 'P3 後半')],
          'm7s': [(0, 'P1'), (158, 'P2 牆上'), (369, 'P3')],
          'm10s': [(0, 'P1 輪流'), (161.5, 'P2 雙人')],
          'm11s': [(0, 'P1'), (1359.5, 'P2 場地分裂'), (1490, 'P3')], 'ucob': [(0, 'P1 雙塔尼亞'), (400, 'P2 奈爾'), (1000, 'P3 至尊巴哈姆特'), (1500, 'P4 三巨頭'), (2300, 'P5 黃金巴哈姆特')]}
if __name__ == '__main__':
    only = sys.argv[1:]
    for src, lab, ph in JOBS:
        if only and lab not in only:
            continue
        build(src, lab, ph, phase_names=None if ph else [lab.upper()], manual=MANUAL.get(lab))
