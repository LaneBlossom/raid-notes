import shutil, os
W='/home/claude/work/'; R='/home/claude/m8s/'
head=open('/tmp/head.txt',encoding='utf8').read() if os.path.exists('/tmp/head.txt') else None
head=open(W+'page_head.txt',encoding='utf8').read()

CB='<a href="https://github.com/OverlayPlugin/cactbot">cactbot</a>（Copyright 2017-2024 cactbot contributors，依 <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a> 使用，<a href="LICENSES/cactbot-LICENSE.txt">授權全文</a>）'
NAME_TC='技能名稱用 cactbot 的繁中服翻譯。'
NAME_CN='技能名稱用 cactbot 的國服翻譯轉繁體（繁中服還沒開這個副本）。'
TEA_SRC='打法、減傷和影片截圖整理自ふうcだよ、ぬけまる、魚子醬的攻略影片（連結見<a href="tea-guide.html">攻略整合</a>頁）；次元斷絕和 ST 一圖流是本站依影片重新繪製。'
PAGE={
 'm5s':('技能名稱對照繁中服攻略站。',''),
 'm8s':('技能名稱對照 xivstrat。','打法照 MMW、蘇帕；「看圖」的站位圖取自猫猫窝攻略组「機制速覽」。'),
 'm8s-blank':('技能名稱對照 xivstrat。','預設標籤沿用版主筆記（MMW、蘇帕的打法）；「看圖」的站位圖取自猫猫窝攻略组「機制速覽」。'),
 'tea':('技能名稱照國服翻譯轉繁體。',TEA_SRC),
 'tea-blank':('技能名稱照國服翻譯轉繁體。','預設標籤沿用版主筆記。'+TEA_SRC),
 'tea-guide':('技能名稱照國服翻譯轉繁體，騎士技能名稱依繁中服。',TEA_SRC),
}
for k in ['m9s','m10s','m11s','m12s','dmu']: PAGE[k]=(NAME_CN,'')
_NX='打法照子言姐姐「7.3攻略 永远之暗悲惶歼灭战」（日服野隊 L 團式）；示意圖由本站依影片重新繪製。'
PAGE['necronx']=(NAME_TC,'預設 # 標籤依'+_NX)
PAGE['necronx-guide']=(NAME_TC,_NX)
def credit(f):
    nm,src=PAGE.get(f,(NAME_TC,''))
    items='<li><b>時間軸</b>：來自 '+CB+'。本站有修改：轉成網頁格式、換算時間、合併連續招式、重新分段，並從觸發器產生預設標籤。本站不是 cactbot 官方專案。</li>'
    items+='<li>'+nm.replace('技能名稱','<b>技能名稱</b>',1)+'</li>'
    if src:
        items+='<li><b>打法與圖片</b>：'+src+'著作權屬原作者，本站只作非商業引用；作者不希望被引用的話請到 <a href="https://github.com/LaneBlossom/raid-notes/issues">GitHub</a> 告知，會立刻移除。</li>'
    items+='<li><b>遊戲素材</b>：技能名稱、狀態圖示和遊戲畫面 © SQUARE ENIX，依 FINAL FANTASY XIV 素材使用授權非商業使用，本站與 Square Enix 無關。</li>'
    return ('<details class="sitecredit" style="margin:14px 0 0;font-size:11.5px;color:var(--muted)">'
            '<summary style="cursor:pointer;opacity:.85">FINAL FANTASY XIV © SQUARE ENIX CO., LTD. All Rights Reserved. 個人非商業筆記 · <u>資料來源與授權</u></summary>'
            '<ul style="margin:6px 0 0;padding-left:1.2em;line-height:1.7">'+items+'</ul></details>')

SE=' FINAL FANTASY XIV © SQUARE ENIX CO., LTD. All Rights Reserved. <a href="index.html#credits">資料來源與授權</a>'
for f in ['m1s','m2s','m3s','m4s','m5s','m6s','m7s','m8s','m8s-blank','tea','tea-blank','tea-guide','m9s','m10s','m11s','m12s','ucob','uwu','dsr','top','fru','dmu','necronx','necronx-guide']:
    s=open(W+f+'.html',encoding='utf8').read()
    if f=='tea-guide':
        a='非商業的隊伍攻略用途。</p>'; assert s.count(a)==1
        s=s.replace(a,'非商業的隊伍攻略用途。</p>\n'+credit(f))
        s=open(W+'theme_head.html',encoding='utf8').read()+s
        i2=s.rindex('</body>'); s=s[:i2]+open(W+'theme_body.html',encoding='utf8').read()+s[i2:]
    else:
        if f=='necronx-guide':
            s=open(W+'theme_head.html',encoding='utf8').read()+s
            i2=s.rindex('</body>'); s=s[:i2]+open(W+'theme_body.html',encoding='utf8').read()+s[i2:]
        i=s.index('<p class="endnote">'); j=s.index('</p>',i)+4
        s=s[:j]+'\n  '+credit(f)+s[j:]
    open(R+f+'.html','w',encoding='utf8').write(head+s)
TH=open(W+'theme_head.html',encoding='utf8').read(); TB=open(W+'theme_body.html',encoding='utf8').read()
h=open(W+'home.html',encoding='utf8').read()
h=h.replace('<head>','<head>\n'+TH,1).replace('</body>',TB+'</body>',1)
open(R+'index.html','w',encoding='utf8').write(h)
os.makedirs(R+'LICENSES',exist_ok=True)
shutil.copy(W+'cb/LICENSE',R+'LICENSES/cactbot-LICENSE.txt')
print('assembled')
