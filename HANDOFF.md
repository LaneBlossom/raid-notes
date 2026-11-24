# Raid Notes 交接說明（2026-11-24）

## 網站
- Repo：https://github.com/LaneBlossom/raid-notes（main 分支＝GitHub Pages）
- 網址：https://laneblossom.github.io/raid-notes/
- 規則：**改完先給版主預覽，版主說「上傳」才 push**。更新紀錄寫精簡，不列感謝名單。
- 版主：繁中服 ST 騎士（PLD）。隊伍：MT 槍刃、ST 騎士、H1 占星、H2 賢者、D1 忍者、D2 武士、D3 機工、D4 繪靈。

## 原始檔（build-src 分支）
網頁是由腳本產生的，原始檔放在 `build-src` 分支（不影響網站）。把它 clone 到 `/home/claude/work`，即可照下面流程重建：

```
cd /home/claude/work
cp m8s.before-nav.html m8s.html
python3 tea/build.py          # m8s.html、tea.html（版主筆記）＋導覽列 RAIDS
python3 tea/build_guide.py    # tea-guide.html（絕亞攻略整合，含 ST 一圖流、次元斷絕圖）
python3 build_blank.py        # 全部空白筆記（M1S～M12S、絕本、極神）
python3 necron/build.py       # necronx-guide.html（極永恆黑暗攻略）
python3 assemble.py           # 組裝到 raid-notes repo（路徑在檔內 R=）
```
- `m8s.before-nav.html`：所有時間軸頁的共用模板（減傷編輯、站位／標籤／打法編輯、筆記圖、匯出檔案、主題）。
- `gen_cb.py`、`gen2.py`：從 cactbot 時間軸（`cb/`）產生空白筆記資料；gen2 支援分支、分 P、PREFER（如極神選坦克分支）。
- `tea/`：絕亞資料、提示、圖片（figimg、icons）、`stpaths.py`（P3／P4 ST 一圖流）、`dimpaths.py`（次元斷絕 1～8 號）。
- `necron/necron.py`：極永恆黑暗攻略內容與示意圖（子言姐姐影片整理）。
- `home.html`＝目前首頁；`home_build.py`＝版本 A（未來科技）；`home_b_build.py`＝版本 B（黑白像素 Y2K）。
- `theme_head.html`／`theme_body.html`：全站共用主題選單（只剩 跟系統／淺色／深色，key＝`raid-notes-theme`）。

## 進行中的工作
1. **首頁改版（未上傳）**：做了兩版給版主挑
   - A：未來科技（深藍黑、霓虹青／洋紅、網格、切角卡片）
   - B：黑白電子像素＋Y2K（點陣、像素字、老電腦視窗、跑馬燈、✦）
   - 兩版都是頂部導覽列＋hover 滑出大選單（mega menu），手機為右側抽屜。
   - 版主想參考自己的素材：在 **DESKTOP-SSVFFFR 的 `D:\AI work sample`**（舊對話連到公司電腦 desktop-guanlin，讀不到）。
   - 下一步：讀素材 → 版主選 A／B 或混搭 → 換掉 `home.html` → 視需要把風格延伸到其他頁。
2. **主題**：舊的特別版主題（櫻花、手帳、武士道…）已從選單拿掉（未上傳）。
3. **次元斷絕一圖流**：還沒對照 ぬけまる 影片後半各號碼視角（15:32～20:15）。
4. **絕亞 P1／P1.5／P2** 還沒有 ST 一圖流和自繪示意圖。
5. **P4 第一次死刑換 T 細節**、**籠子 T 的號碼**：待版主看影片確認。

## 已上傳的最新版本
commit d76ef7c：極永恆黑暗攻略、P3／P4 ST 一圖流、攻略頁重排、零式分段、首頁手帳風（已被改版中）、各頁資料來源。

## 小技巧
- Chrome 截圖若一直逾時：Chrome 視窗要在前景、不要最小化。
- B 站字幕可在影片頁用 JS 抓 `api.bilibili.com/x/player/wbi/v2` 的 `ai-zh` 字幕。
- git push 若 403：`git remote set-url origin https://github.com/LaneBlossom/raid-notes` 再推。
