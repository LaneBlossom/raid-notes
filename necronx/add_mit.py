"""極永恆黑暗：本站建議減傷軸（預設隊伍 MT絕槍 ST騎士 H1占星 H2學者 D1武僧 D2武士 D3舞者 D4召喚）。
CD 檢查：P1.5 約 03:19、單人約 04:10 開始（cactbot），P2 開頭約 05:30（看打速）。
重跑：python3 necronx/add_mit.py（從 data.before-mit.js 產生 data.js）"""
import json, re
W = '/home/claude/work/necronx/'
PLAN = {
 # ---- P1
 '青藍衝擊（×2） ①': dict(mt=['大星雲', '剛玉之心'], st=['挑釁', '極致護衛', '聖盾陣'],
     n='二連魔法死刑：MT 左上吃第一下，ST 讀條中挑釁、到右上吃第二下，吃完 MT 挑回',
     nst='第二下沒有範圍提示，挑釁要在讀條期間按；極致護衛留到單人階段前會轉好', nmt='第一下會附 5 秒魔法易傷，吃完別急著挑回，等 ST 吃完'),
 '死之恐懼 ①': dict(c=[['MT', '雪仇'], ['D4', '昏亂'], ['H2', '野戰治療陣']], n='魔法全體，傷害不高，之後引導黑手'),
 '死之恐懼 ②': dict(c=[['ST', '雪仇'], ['D3', '防守之桑巴'], ['H1', '命運之輪']]),
 '青藍衝擊（×2） ②': dict(mt=['鐵壁', '偽裝', '剛玉之心'], st=['挑釁', '鐵壁', '聖盾陣'],
     nst='極致護衛還沒轉好（00:14 用過），用鐵壁＋聖盾陣；血線不穩可以改開神聖領域（整場只能用一次）',
     nmt='大星雲還沒轉好，用鐵壁＋偽裝'),
 '大十字 ①': dict(c=[['MT', '雪仇'], ['D4', '昏亂'], ['MT', '光之心'], ['ST', '聖光幕簾'], ['H2', '野戰治療陣']],
     n='高傷魔法全體，之後場地變圓形；聖光幕簾要先按、等補師補血觸發盾'),
 '中子環（×2） ①': dict(c=[['ST', '雪仇'], ['D3', '防守之桑巴'], ['D1', '牽制'], ['H1', '中間學派'], ['H2', '展開戰術']],
     n='兩下高傷魔法，接著進小怪階段，先補滿。桑巴 01:33 用過，這裡剛好轉好'),
 # ---- P1.5
 '壓潰（直線）': dict(st=['聖盾陣'], mt=['剛玉之心'], n='拉大黑手的 T 把直線往場外帶，小減傷就吃得下；鐵壁留給單人階段'),
 # ---- 單人
 '永世黑暗（×2）': dict(c=[['MT', '雪仇'], ['D4', '昏亂'], ['MT', '光之心'], ['H2', '野戰治療陣']], n='進異空間前的全體傷害'),
 '散佈': dict(nst='第一招一定要插言打斷，不然會死', nmt='第一招一定要插言打斷，不然會死'),
 '壓潰 ⑤': dict(st=['極致護衛', '壁壘', '聖盾陣'], mt=['大星雲', '剛玉之心'], n='坦克單人：之後每 7 秒一發壓潰，減傷輪著開，可以留爆發進來打'),
 '壓潰 ⑦': dict(st=['鐵壁', '聖盾陣'], mt=['鐵壁', '剛玉之心']),
 '壓潰 ⑨': dict(st=['聖盾陣'], mt=['偽裝', '剛玉之心'], nst='血量撐不住再交神聖領域'),
 # ---- P2
 '死之恐懼 ③': dict(c=[['ST', '雪仇'], ['D4', '昏亂'], ['H1', '命運之輪']]),
 '青藍衝擊（×2） ③': dict(mt=['大星雲', '剛玉之心'], st=['挑釁', '極致護衛', '聖盾陣'],
     nst='群體恐慌中間的死刑：挑釁到最右上角吃第二下，不踩 3 人塔；可以用保護幫補師擋'),
 '大十字 ②': dict(c=[['MT', '雪仇'], ['D1', '牽制'], ['D3', '防守之桑巴'], ['MT', '光之心'], ['ST', '聖光幕簾'], ['H2', '野戰治療陣']]),
 '中子環（×2） ②': dict(c=[['ST', '雪仇'], ['D4', '昏亂'], ['ST', '武裝戍衛'], ['H1', '大宇宙'], ['H2', '展開戰術']],
     n='最後兩下高傷，之後是狂暴', nst='武裝戍衛開了不能動，四角躲完回場中、站在大家前面再開'),
 '永世黑暗 （狂暴）': dict(n='狂暴，讀完沒打死就滅團'),
}
# ---- 站位：從攻略頁一圖流（necron/necron.py 的 PANELS）同步每個職位的說明 → 該列的 n<職位> 備註
import importlib.util, re as _re
_sp = importlib.util.spec_from_file_location('necron_guide', '/home/claude/work/necron/necron.py')
_N = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_N)
POSMAP = {'P1 00:14': ['青藍衝擊（×2） ①'], 'P1 00:29': ['死之恐懼（圈） ①', '死之恐懼（圈） ②', '死之恐懼（圈） ⑥'],
          'P1 00:52': ['死亡警告 ①', '死亡警告 ③'], 'P1 01:10': ['青藍二重波／青藍四重波 ①', '青藍二重波／青藍四重波 ②', '青藍二重波／青藍四重波 ③'],
          'P1 01:43': ['青藍衝擊（×2） ②'], 'P1 02:20': ['大十字 ①'], 'P1.5': ['壓潰（直線）'], '單人': ['小怪生成'],
          'P2 00:00': ['引導之翼 ②'], 'P2 02:06': ['群體恐慌'], 'P2 04:44': ['大十字 ②']}
ALLR = ['MT', 'ST', 'H1', 'H2', 'D1', 'D2', 'D3', 'D4']
POS = {}   # 列名 → {職位: 說明}
for t, title, svg, common, per in _N.PANELS:
    for row in POSMAP.get(t, []):
        for k, v in per.items():
            for r in k.split():
                POS.setdefault(row, {})[r] = _re.sub(r'<[^>]+>', '', v)
for row, d in POS.items():
    p = PLAN.setdefault(row, {})
    for r, v in d.items():
        key = 'n' + r.lower()
        p[key] = v + ('｜' + p[key] if p.get(key) else '')

s = open(W + 'data.before-mit.js', encoding='utf8').read()
used = set()
def ser(v): return json.dumps(v, ensure_ascii=False, separators=(',', ':'))
def rep(mo):
    m = mo.group(2)
    if m not in PLAN: return mo.group(0)
    used.add(m); p = PLAN[m]
    extra = f'c:{ser(p.get("c", []))}' + ''.join(f',{k}:{ser(p[k])}' for k in ['st', 'mt', 'n'] + ['n' + r.lower() for r in ALLR] if k in p)
    return mo.group(1) + extra + '}'
s = re.sub(r'(\{t:"[^"]*",m:"([^"]*)",)c:\[\]\}', rep, s)
miss = set(PLAN) - used
assert not miss, miss
open(W + 'data.js', 'w', encoding='utf8').write(s)
print('rows with plan:', len(used))
