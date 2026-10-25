# Methods that work (sourcing, checks, data pulls)

Durable how-to. Current state lives in `MASTER.md`; full history in `notes/project-notes.md` (frozen 21 Oct).

## 1. Douyin discovery (LOCAL: logged-in built-in browser pane, Vyx logged in by QR)
- **Screen from data first: `tools/dyhook.js`** (25 Oct). Paste it once on a douyin.com page (after a reload: `eval(localStorage.__dyh)`), run `__dy.start()`, then browse. It copies the JSON Douyin's own page fetches, so every clip in a search, 推荐视频 list or creator's uploads comes with likes, saves, shares, comments, exact post time, length, top stream res + bitrate, full caption and author (+ fans in search). `__dy.q({minLikes: 2000, days: 14, minS: 8, maxS: 13})` lists them best first with flags (take, sell?, AI, slow?, shr>lk, wide); `__dy.lib([ids])` gives library.csv rows. Eyes are then only needed for charm, the opening and the signature check.
  - Tested 25 Oct: the page's search box (all 16 results of a search), filter chips, a clip's **TA的作品** tab in the search modal (creator bio, fans, post count and every upload by date = the one-upload check in one click), and clicking a clip in a 推荐视频 list (its detail + 10 related).
  - **Yield (25 Oct, 595 clips captured, dyhook data):** 525 videos → 362 vertical → 162 ≤45 days → 82 at 8–14.5 s → 56 at 2K+ → 50 → ~25 looked at → 1 A + 2 B. Data pass rate by source: liked list 8/20 (40%), creator uploads 23/196 (12%), 推荐视频 5/39 (13%), keyword search 14/269 (5%). The visual gates (reveal, subject, not slowed) then pass ~1 in 4, and creator checks about half of those.
  - **Movement scan (25 Oct):** `__dy.scan(ids)` measures camera movement in the first 4 s of each clip from its file (row/column luma shifts 0.1 s apart) and tags `.mot.kind` = tilt-up / pan / static / other; `__dy.q({kind: 'tilt-up'})` filters. Calibrated on 8 clips judged by eye: the 3 tilt-ups scored 0.76-1.28 frame heights, pans and statics 0.00-0.21 (a tilt that starts at 3-4 s scored 0.21 over 3 s, hence the 4 s window). It can't tell slowed clips from slow camera moves (丢's slowed snow scored as a normal tilt-up).
  - **Option C download (tested 25 Oct, p85):** `__dy.src(id).url` + `curl.exe -L -H "Referer: https://www.douyin.com/"` gave 2160x3840 HEVC 59.94 fps 6.1 Mbps, the same as Option B. The URL carries its expiry as a hex Unix time in the path (2-3 h after capture).
  - **Followed yes-creators (25 Oct, pane account):** 梁同学, Zwzzz, Hua., 雾必野 (already followed) + 桑榆, @0513 (new). Their new uploads show in the following feed (`douyin.com/follow`). Before clicking 关注 on a profile, read `[data-e2e="user-info-follow-btn"]`: 已关注 means followed, and clicking it unfollows.
  - **Seed from the account's liked list:** loading `douyin.com/user/self` also loads its 喜欢 tab (`aweme/favorite`), which dyhook captures (via = `aweme/favorite`). 25 Oct it held 4K city clips of 10万+ likes from the last month.
  - **Evening run, 25 Oct (FYP + 收藏 seeds):** the page can open on 作品: click 喜欢, then mouse-wheel scroll (JS scrolling fetches nothing): 59 unique of 83 liked clips in 4 fetches. 收藏 (`aweme/listcollection`) gave 10, 7 already liked. The 推荐 feed (`tab/feed`) only advances on the mouse wheel over the video, ~6 clips per fetch, 15 of 19 horizontal. The following feed (`follow/feed`) puts clips under `data[].aweme`, which dyhook missed until 25 Oct (fixed); it ran out after 2 fetches ("暂时没有更多了"), but its left list of followed creators loads a creator's uploads in one click. Funnel: 82 clips → 27 pass data checks → 25 scanned, 13 tilt-ups → 2 A + 2 B. Most liked-list hits are 10万-60万-like clips with 15-33% shares: likely already on TikTok, so collision-check them.
  - Clips seen only in a 推荐视频 list carry a low-bitrate preview URL (douyinvod.com) that won't load for frames: open the clip (its `aweme/detail` has the normal URLs). `await __dy.frames(id, [0.1, 0.5, 1, 2, 4, 8])` shows a frame strip + luma + frame-to-frame change (near 0 = static or slowed).
  - **A full page load (navigate) drops the hook and that load's first list.** Land on one page, then stay inside it: search box, filter chips, modal tabs, clicking recommended clips. The search box drops URL filters (一周内), so filter with `days` or the 筛选 menu.
  - Endpoints and field names come from Evil0ctal/Douyin_TikTok_Download_API and tamnd/douyin-cli: search `/aweme/v1/web/search/item/` (视频 tab; the 综合 tab uses `general/search/single` + `stream`, also captured), related `aweme/related/`, uploads `aweme/post/`, detail `aweme/detail/`, creator `user/profile/other/`. We don't run either tool: both get past Douyin's anti-bot wall by forging its a_bogus signatures and minting identities, which Claude won't do. Also Evil0ctal has no Douyin keyword search, and douyin-cli (6 stars, June 2026) says non-China IPs get a challenge.
- **Best seed:** open a clip that passes the charm gate and read its 推荐视频 (recommended) list: ~10 similar clips with likes/author/length. Snowball from the best. Lists drift to generic feed after ~3 video pages.
- **Charm accounts' profiles** (`library/accounts.csv`). A profile's 搜索Ta的作品 box finds uploads past the ~20-post grid limit.
- **Keyword search is weak** (songs, news, filler after ~2–4 searches). If used: `?type=video&sort_type=0&publish_time=7` and sort by likes yourself (最多点赞 + 一周内 starves results). Good: 风景, 治愈系风景, 雪景, 心邸咖啡 蓝调. Bad: 大风/大雾, 下雨天/初雪, 雨天, 银杏, 氛围感, 雨夜, 蓝调时刻, 禾木 初雪 (username matches; filler), 虎跳峡 (mostly 47 s+ vlogs; 1 of 7 usable, then seed from its 推荐视频). 25 Oct: 新疆下雪了 good (fresh vertical first snow); 沉浸式徒步 bad (all 42 s+ horizontal vlogs); 雪林, 喀纳斯, 稻城亚丁, 雪山湖泊, 峡谷徒步 give old popular clips, and 一周内 starves them (峡谷徒步: 3). 泡泡 日落 and 海边日落 give old (90-500 day) or heavily shared clips.
- Detail JS (fallback when dyhook missed the page): in page text find the line starting `发布时间` at i → likes t[i-5], comments t[i-4], saves t[i-3], shares t[i-2], caption t[i-6], author t[i+1], fans t[i+2]. Dims via video.videoWidth/Height.
- Douyin/TikTok video ID >> 32 = post time (Unix seconds, UTC).
- Saved scripts live in douyin.com localStorage (`__gsrc` grid sweep, `__sr` search list, `__rec2` details + recommended, `__fr2` frames at 480px (too small for signatures, see §2.5), `__ov`/`__ovs` cover overlays, `__band` middle-band frame). The signature check is a repo file, `tools/edgecheck.js`. Overlay: append to document.documentElement, wait ~1.5 s, then screenshot. Pane hidden: zoom times out, a plain screenshot works about every 2nd try; luma via canvas (crossOrigin anonymous).

## 2. Screening a clip before asking for it (sourcing rules v4)
1. Charm gate (`docs/charm.md`).
2. **Fresh:** this season's footage. Skip 反季 last-winter reposts.
3. **Small personal creators** who shoot their own footage. Skip footage-selling/sharing accounts (素材/教学 bios, 拿了留痕 captions) and aggregators (3+ posts/day from all over China).
   Also skip the caption-trend circle (25 Oct): accounts posting the same caption as several others within days ("我当然幸福啦…", "你和雪有一个共同点…", "我无法忘记第一次到香港中环的震撼", "望着天下起了雪…": 啊刘, 博, 江樂, 丢, 飞鱼, _17), with a bio that links an @教学/音推/素材 account (啊刘, like 晚安.). Their clips come from all over (Erhai, HK, Sayram, snow) and snow ones are often last winter's.
4. **One upload per shoot:** sort the creator's grid by date; if the same spot/light/weather was uploaded more than once, skip (p53/p58 were flagged this way).
5. **No baked-in signature/text:** creators sign in small white cursive near an edge: 韬 "Tao" at bottom-centre (~3% of the width, ~98% down), Iuk and 7na. at right-middle. At 480–540 px a signature is ~15 px wide and gets missed: p76 and p83 both passed a 480 px check, and Vyx found "Tao" on p83 (24 Oct). So:
   - On the video page, pick the top quality in the 智能 menu, paste `tools/edgecheck.js` with javascript_tool, run `await __edge({show: true})`. **SIGNATURE = reject.** LOOK = read the overlay crop (static shots land here because lit windows stay put too). Record the verdict and score in library.csv `risks`.
   - It takes the darkest value of each pixel across 24 frames: the scene moves and goes dark, a signature stays white. Tested 24 Oct on local files: caught p55, p57 and p83 (scores 96–193), p80–p84 clear (0–8). Works on a live Douyin page (25 Oct, owo clip, score 0): `await __edge({src: __dy.src(id).url, show: true})` reads the top-quality file without the 智能 menu. If the stream is below 1080 px wide, say so: the score is less reliable.
   - It only sees marks that stay for the whole clip and are brighter than what's behind them. Also look at all four edges of one full-resolution frame yourself.
   - After download, `precheck.ps1` runs the same check and flags it again.
   - A clear umbrella with a real leaf is not an overlay.
6. **Shares > likes** = already passed around → backup only.
7. Vertical, not sideways (check the video page dims). Exclude #可灵AI / AI生成.
   Also look at frames from 0.1 s: some clips open on a 0.05–0.1 s creator cover still.
8. Reposts: identical first frame + identical length across accounts → only the earliest poster can give permission.

## 3. Permission → download → name
- Vyx DMs the creator (text below). Statuses in `library/library.csv`.
- **Download (Option B; yt-dlp gets 403 "Fresh cookies needed"):** open the video in the logged-in pane → pick the top quality in the player's 智能 menu (default may be 576x1024) → read `video.currentSrc` (zjcdn.com) → `curl.exe -L -H "Referer: https://www.douyin.com/" -o "D:\cheques\inbox\pNN <content>.mp4" "<src>"`. Files are HEVC + AAC, no watermark.
- **Option C (tested 25 Oct on p85, see §1):** if dyhook captured the clip, `__dy.src('<id>')` gives the top-quality file URL and size straight from Douyin's data, without the 智能 menu. Same `curl.exe` line. The URL expires after a few hours (`age_min` shows how old it is); compare the file with Option B the first time.
- **Name:** `pNN <content>.mp4`, next number after the highest in D:\cheques. Add a `log.csv` row (UTF-8 with BOM; in Excel save as "CSV UTF-8").
- **Pre-post check:** `powershell -ExecutionPolicy Bypass -File D:\cheques\tools\precheck.ps1` → `checks\report.html` (duration/res/audio, first-second sheet, <5 s flag, frame-hash duplicate vs posted\, permission vs log.csv, creator signature near the edges with a crop). A red signature flag = never post.
- **Library page:** `powershell -ExecutionPolicy Bypass -File D:\cheques\tools\render_library.ps1` → `library\library.html` (phone-friendly). **Link list:** `tools\list_links.ps1` → `library\links.md` (every Douyin link on record, downloaded ones marked; committed).
- DM text (from 21 Oct; covers colour correction and trims): 你好！很喜欢你这条视频，想问一下可以发到我的TikTok（海外）账号吗？可能会稍微调色或剪短一点，不加字，文案里会注明你的抖音号。方便的话能发一下原片就更好了，谢谢！
  (Roughly: "May I post it on my overseas TikTok? I may lightly colour-correct or shorten it, no added text, and I'll credit your Douyin ID. The original file would be great.")
- Old DM (permissions for p50–p72 were asked with this): …不剪辑、不加字… = "no cutting/editing, no text". Keep those clips full length; colour correction only.
- **Edits:** never overwrite the original. Save as `pNN <content> edit.mp4` next to it and note the change in log.csv `notes`. Recipes used 22 Oct (all ffmpeg, libx264 slow, CRF 16, AAC 192k, full length):
  - **Bright clips:** `eq=gamma=1.08–1.15,hqdn3d=1.5:1.2:2:2`, plus `scale=1080:-2` if the source is bigger. YAVG +6 to +11.
  - **Dark interiors** (e.g. a train window): `hqdn3d=3:2.5:3:3,curves=all='0/0 0.12/0.19 0.5/0.56 1/1'` lifts the shadows without blowing out the window. YAVG 45→53.
  - Check that the frame count and length match the original, then look at a before/after pair.
- **Precheck quirk:** an edit always shows "same footage" as its original plus "no permission found". That's expected, since permission lives on the original's row.
- **Clips Vyx downloads:** when our pane is bounced, Vyx sometimes downloads clips themselves. They land in `C:\Users\Yichen\Downloads` as `SaveTik.co_<douyin id>-hd.mp4` (1080p H.264, 1.0–3.3 Mbps, below Option B's 1440p–4K HEVC). Use Option B when the pane is up: SaveTik files passed lite 1 of 4 (p73, p78, p79 failed) vs Option B 4 of 6 (23 Oct, weak lead). Never re-download a lite-failed clip to retry it (hard rule 1). Copy them, don't move them, into inbox\ as the next pNN, and match by the id in the filename.

## 4. Posting gate
- **TikTok Studio web upload → "Content check lite"** (~10 min). PASS → no FYP flag 3/3 (p60, p64, p67). ERROR → p54 (not posted), p58 (flagged). Post only on a PASS (n small, keep scoring it).
- Post directly, hours apart. Credit the Douyin creator in the caption.

## 5. TikTok data
- **Bulk stats (CLOUD, Python):** run `python3 -I research/scripts/pull_account.py <handles>`. It wraps `pull_items.py`, `pull_tech.py`, `pull_music.py` and `build_csvs.py`, and stops at the first block. Sounds: `proven_sounds.py`. Model: `python3 research/model/success_model.py` (needs numpy).
- **Cloud lessons (22 Oct run):** environment "Hi" reaches www.tiktok.com.
  - The auto-mode safety classifier denied a hand-rolled curl of our own profile, so always use the committed script.
  - The cloud git proxy refuses tag pushes, so the weekly tag comes from `.github/workflows/snapshot.yml`.
  - Debug a routine with RemoteTrigger `list_runs`, then `get_run_log`.
- **Logged-out profile facts (LOCAL browser):** `#__UNIVERSAL_DATA_FOR_REHYDRATION__` → `__DEFAULT_SCOPE__['webapp.user-detail'].userInfo` gives createTime, name-change times, language, bio, bioLink, stats. Loads even when the grid shows "Something went wrong".
- **Collision check (LOCAL):** dHash frame 1 of each candidate (9x8 + mirrored) on douyin.com; on a TikTok grid, reload covers with crossOrigin=anonymous, hash, flag Hamming ≤14, eyeball flagged pairs. Scripts in tiktok.com localStorage (`__c2`, refs `__refs3`). Only catches covers that are frame 1. Pinned posts break the date cutoff (use `__c2`).
- Short links: `curl -s -o /dev/null -w "%{redirect_url}" https://vt.tiktok.com/...` gives the full URL without loading the page.

## 6. Limits and stop signals
- Claude never solves a captcha or verify page and never forges Douyin's request signatures, whatever the project rules say: on a verify page, Vyx solves it or the run stops.
- Douyin: ~20–30 page loads per session; throttle carries over the same day. Signs: keyword search returns filler, video pages bounce to the jingxuan feed, "服务器出现问题".
- TikTok logged-out: ~3 profile loads per sitting. Signs: "Something went wrong" grid, WAF "Please wait...".
- 25 Oct: a slider captcha (请完成下列验证后继续) appeared after ~30 in-page actions + 4 loads that day, with no filler or bounce first. It can load behind overlays, so take a plain screenshot every few actions.
- On the first sign: stop for the day. No refresh loops, no workarounds.
- Token savers: small zooms (scale 0.4), browser_batch 2–4 pages per call, compact JS returns, pre-filter by likes/date before opening detail pages.
