# Methods that work (sourcing, checks, data pulls)

Durable how-to. Current state lives in `MASTER.md`; full history in `notes/project-notes.md` (frozen 21 Oct).

## 1. Douyin discovery (LOCAL: logged-in built-in browser pane, Vyx logged in by QR)
- **Best:** open a clip that passes the charm gate and read its 推荐视频 (recommended) list: ~10 similar clips with likes/author/length. Snowball from the best. Lists drift to generic feed after ~3 video pages.
- **Charm accounts' profiles** (`library/accounts.csv`). A profile's 搜索Ta的作品 box finds uploads past the ~20-post grid limit.
- **Keyword search is weak** (songs, news, filler after ~2–4 searches). If used: `?type=video&sort_type=0&publish_time=7` and sort by likes yourself (最多点赞 + 一周内 starves results). Good: 风景, 治愈系风景, 雪景, 心邸咖啡 蓝调. Bad: 大风/大雾, 下雨天/初雪, 雨天, 银杏, 氛围感.
- Detail JS: in page text find the line starting `发布时间` at i → likes t[i-5], comments t[i-4], saves t[i-3], shares t[i-2], caption t[i-6], author t[i+1], fans t[i+2]. Dims via video.videoWidth/Height.
- Douyin/TikTok video ID >> 32 = post time (Unix seconds, UTC).
- Saved scripts live in douyin.com localStorage (`__gsrc` grid sweep, `__sr` search list, `__rec2` details + recommended, `__fr2` frames at 480px, `__ov`/`__ovs` cover overlays). Overlay: append to document.documentElement, wait ~1.5 s, then screenshot.

## 2. Screening a clip before asking for it (sourcing rules v4)
1. Charm gate (`docs/charm.md`).
2. **Fresh:** this season's footage. Skip 反季 last-winter reposts.
3. **Small personal creators** who shoot their own footage. Skip footage-selling/sharing accounts (素材/教学 bios, 拿了留痕 captions) and aggregators (3+ posts/day from all over China).
4. **One upload per shoot:** sort the creator's grid by date; if the same spot/light/weather was uploaded more than once, skip (p53/p58 were flagged this way).
5. **No baked-in signature/text:** check frames at 1/4/8 s and the end at ≥480–540 px wide (Iuk, 7na. bake a cursive name at right-middle; contact sheets miss it). A clear umbrella with a real leaf is not an overlay.
6. **Shares > likes** = already passed around → backup only.
7. Vertical, not sideways (check the video page dims). Exclude #可灵AI / AI生成.
8. Reposts: identical first frame + identical length across accounts → only the earliest poster can give permission.

## 3. Permission → download → name
- Vyx DMs the creator (text below). Statuses in `library/library.csv`.
- **Download (Option B; yt-dlp gets 403 "Fresh cookies needed"):** open the video in the logged-in pane → pick the top quality in the player's 智能 menu (default may be 576x1024) → read `video.currentSrc` (zjcdn.com) → `curl.exe -L -H "Referer: https://www.douyin.com/" -o "D:\cheques\inbox\pNN <content>.mp4" "<src>"`. Files are HEVC + AAC, no watermark.
- **Name:** `pNN <content>.mp4`, next number after the highest in D:\cheques. Add a `log.csv` row (UTF-8 with BOM; in Excel save as "CSV UTF-8").
- **Pre-post check:** `powershell -ExecutionPolicy Bypass -File D:\cheques\tools\precheck.ps1` → `checks\report.html` (duration/res/audio, first-second sheet, <5 s flag, frame-hash duplicate vs posted\, permission vs log.csv).
- **Library page:** `powershell -ExecutionPolicy Bypass -File D:\cheques\tools\render_library.ps1` → `library\library.html` (phone-friendly).
- DM text (from 21 Oct; covers colour correction and trims): 你好！很喜欢你这条视频，想问一下可以发到我的TikTok（海外）账号吗？可能会稍微调色或剪短一点，不加字，文案里会注明你的抖音号。方便的话能发一下原片就更好了，谢谢！
  (Roughly: "May I post it on my overseas TikTok? I may lightly colour-correct or shorten it, no added text, and I'll credit your Douyin ID. The original file would be great.")
- Old DM (permissions for p50–p72 were asked with this): …不剪辑、不加字… = "no cutting/editing, no text". Keep those clips full length; colour correction only.
- **Edits:** never overwrite the original. Save as `pNN <content> edit.mp4` next to it and note the change in log.csv `notes`.

## 4. Posting gate
- **TikTok Studio web upload → "Content check lite"** (~10 min). PASS → no FYP flag 3/3 (p60, p64, p67). ERROR → p54 (not posted), p58 (flagged). Post only on a PASS (n small, keep scoring it).
- Post directly, hours apart. Credit the Douyin creator in the caption.

## 5. TikTok data
- **Bulk stats (CLOUD, Python):** `research/scripts/pull_items.py` pages `api/creator/item_list` from a profile's secUid; `pull_tech.py` / `pull_music.py` add encoding and sound fields; `own_account.py` prints our per-post table. Model: `python3 research/model/success_model.py` (needs numpy).
- **Logged-out profile facts (LOCAL browser):** `#__UNIVERSAL_DATA_FOR_REHYDRATION__` → `__DEFAULT_SCOPE__['webapp.user-detail'].userInfo` gives createTime, name-change times, language, bio, bioLink, stats. Loads even when the grid shows "Something went wrong".
- **Collision check (LOCAL):** dHash frame 1 of each candidate (9x8 + mirrored) on douyin.com; on a TikTok grid, reload covers with crossOrigin=anonymous, hash, flag Hamming ≤14, eyeball flagged pairs. Scripts in tiktok.com localStorage (`__c2`, refs `__refs3`). Only catches covers that are frame 1. Pinned posts break the date cutoff (use `__c2`).
- Short links: `curl -s -o /dev/null -w "%{redirect_url}" https://vt.tiktok.com/...` gives the full URL without loading the page.

## 6. Limits and stop signals (rule 4)
- Douyin: ~20–30 page loads per session; throttle carries over the same day. Signs: keyword search returns filler, video pages bounce to the jingxuan feed, "服务器出现问题".
- TikTok logged-out: ~3 profile loads per sitting. Signs: "Something went wrong" grid, WAF "Please wait...".
- On the first sign: stop for the day. No refresh loops, no workarounds.
- Token savers: small zooms (scale 0.4), browser_batch 2–4 pages per call, compact JS returns, pre-filter by likes/date before opening detail pages.
