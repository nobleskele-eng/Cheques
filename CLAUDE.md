# Vyx's TikTok accounts: read first (loaded in every local and cloud session)

**Mains [V 26 Nov]: @chequethetime and @duskism** (anime). @stayvyxed wasn't named a main; its role stays as it was until Vyx says otherwise. Current state: @anime/STATE.md (@chequethetime, @stayvyxed) and @accounts.md (every account at a glance, plus the @duskism notes).
**Scenery dropped [V 26 Nov]:** @papercheques and @sylvanism_ are no longer worked on. Vyx: move completely away from the nature stuff. Don't plan, source, post, pull or analyse for them. MASTER.md and the other scenery files (see Files) are frozen history: search them, don't update them or plan from them.

## Who / how to work
- Vyx (they/them) runs the TikTok accounts below. The goal is clout (views/followers), not money. Vyx has limited coding: Vyx directs, Claude builds.
- **Answer line first (Vyx, 16 Nov):** every reply opens with one bold line that answers the question outright: yes/no, a number, or the pick. Several questions → one answer line per question, at the top of its section. Then step lists. Explain syntax/errors, not plan logic.
- Challenge weak ideas before building. Give one recommendation.
- Never claim something works unless it was checked.
- Label every number as sourced (say where) or estimate.
- Don't move or reorganise files without a yes. Don't bring up swimming.
- **Check status first:** Vyx posts on their own and sends Studio screenshots later, so `anime/log.csv` lags behind. Before planning posts, confirm what was already posted, then record it.

## Accounts (Vyx, 16 Nov; @duskism 18 Nov; mains and scenery drop 26 Nov)
| Account | What | Notes live in | Hard rules |
|---|---|---|---|
| @chequethetime | **main**; anime edits, simpler; the test lab | `anime/STATE.md` | 1, 3, 4 |
| @duskism | **main**; stretched, chopped aesthetic anime compilations; new 18 Nov, first post 20 Nov | `accounts.md` | 1, 3, 4 |
| @stayvyxed | anime edits (Vyx in AE), oldest/largest; has a hate-speech warning; not named a main | `anime/STATE.md` | 1, 3, 4 |
Dropped: @papercheques and @sylvanism_ (scenery, 26 Nov; rule 3 still covers them while they're up), @starzarchive1 (16 Nov). A clip goes on one account only (duplicate matching).

## Sessions: one-shot, GitHub is the memory
Vyx never reopens a finished session. Each new session starts from this file (it pulls in `anime/STATE.md` and `accounts.md`) and `git log -15 --stat --invert-grep --grep='^watch:'` (this hides the old watch routine's data commits). Never rely on an earlier chat.
- **During a session:** push after every change of state (a post made, a Studio read, a check result, a decision).
- **When Vyx says "end session":**
  1. `git pull --rebase`.
  2. Write every new fact, decision and open question into the file that owns it: `anime/STATE.md` (under its cap), `anime/log.csv`, `accounts.md`, `anime/research/`, docs/ or reports/.
  3. Commit and push to main. Check that `git ls-remote origin main` matches `git rev-parse HEAD`.
  4. Reply with a summary of 3–5 lines and the commit hash. If something couldn't be saved, say what.

## Hard rules (never break, whoever asks)
1. **Editing is OK, evading isn't** (Vyx, 21 Oct). Colour correction, exposure, denoise, re-export and trims are fine. Still banned: any change made to fool TikTok's duplicate matching (mirroring, speed changes, borders/overlays/noise added to dodge detection). Keep the untouched original and save edits as `pNN <content> edit.mp4`. In anime edits, speed ramps and overlays are craft, not evasion; the ban is on changes made to dodge detection.
2. **Permission and credit (scenery accounts): dormant since the scenery drop (26 Nov).** Kept in case scenery ever returns: only post clips whose creator allowed reuse (拿了留痕 / 随便拿 / 可以拿 / 原创素材 in the caption, or a yes by DM). Credit them. Prefer the original file. Permissions for p50–p72 were asked with "不剪辑、不加字" (no cutting/editing, no text). For those clips, keep the full length; colour correction only. New requests use the DM in `docs/methods.md` §3.
3. **Never play our videos (any of our accounts) in a browser, and scripts never load or download our own video pages (`/video/<id>`) or files** (confirmed 21 Oct; all accounts since 16 Nov). Allowed and expected: our profile pages and the item_list post list, via `research/scripts/pull_account.py`. For other accounts: grid covers only, never hover tiles.
4. **Never ask for API keys or passwords in chat.** No third-party upload tools or anything that needs the TikTok login (e.g. "HD by Rein"). The one exception, @sylvanism_ in AdsPower (Vyx, 12 Nov), lapsed with the scenery drop. @papercheques never goes into AdsPower.

## Where work runs
- **Local (Vyx's PC, D:\cheques):** the video files, After Effects, ffmpeg and the PowerShell tools. Python runs here (checked 12 Nov), but TikTok blocks its requests from this IP; pull our post list in the browser pane instead. The pane is signed in to TikTok as @papercheques (seen 16 Nov). Profile headers load there, but grids and follow lists don't. (The Douyin login was only for scenery sourcing.)
- **Cloud (Claude Code on the web, this repo):** public TikTok data pulls, Python/numpy models and scheduled refreshes. It has no video files.
- **The repo is the bridge.** Video files never go in it (see .gitignore).
- **Weekly routine** "papercheques weekly analysis": Saturdays 13:00 UTC (8 AM EST / 9 AM EDT), Sonnet 5.5, environment "Hi". New scope (Vyx, 26 Nov): pull @stayvyxed, @chequethetime and @duskism, then `account_stats.py` fills the numbers in `accounts.md`; pull the tracked anime editors @smokinsasa7, @.sadaqatt and @zrivvn, and `refs_report.py` writes `anime/refs.md`; push to main. Claude can't edit this routine: the new prompt waits in `docs/weekly-routine-prompt.md` for Vyx to paste. **Until then its stored prompt still lists the scenery jobs. A run that reads this: skip rival-analyst, self-analyst and editor, leave MASTER.md alone, and leave @papercheques and @sylvanism_ out of every pull and scoreboard (Vyx, 26 Nov).** Manage it at https://claude.ai/code/routines/trig_01MAPoQSqFEPnTD3oJKjA9sL
- **Sounds routine** "papercheques Monday sounds" (trig_0189VersqgMcRxDuSeYsJjNg): **disabled 26 Nov.** It only tracked the scenery network's sounds. Its standing session (session_01L4My9cu3ULGtA7VJQsKUK5) is idle. Output stays in `reports/sounds.md` and `research/data/sounds/`; commits starting "sounds:" are history. Manage it at https://claude.ai/code/routines/trig_0189VersqgMcRxDuSeYsJjNg
- **Watch routine** (trig_012ygYS68kuGA2j5qZHckaTV): gone since 8 Nov. Data in `research/data/watch/` and `reports/watch.md`; commits starting "watch:" are history.

## Agents (`.claude/agents/`)
All five are **retired (26 Nov)**: scout, gatekeeper, rival-analyst, self-analyst and editor were built for @papercheques and MASTER.md. Don't run them. Their files stay until Vyx OKs removing them. There are no anime agents yet.

## Files
**Live:** `anime/` @chequethetime + @stayvyxed (STATE.md, log.csv with Studio numbers, references.csv, refs.md weekly tracked-editor table, research/) · `accounts.md` every account at a glance + @duskism notes · `research/duskism-niche-2026-11-19.md` · `research/scripts/` (live: `pull_account.py`, `account_stats.py`, `refs_report.py`) · `research/data/<handle>_*.csv` · `docs/methods.md` §4–6 (Studio check, TikTok data pulls, stop signals) · `docs/weekly-routine-prompt.md`.
**Frozen scenery history (26 Nov):** `MASTER.md` · `log.csv` · `library/` · `docs/charm.md` · `docs/methods.md` §1–3 (Douyin) · `reports/` · `audio/` · `tools/` · `research/model/` and the scenery analyses in `research/` · `notes/project-notes.md` (to 21 Oct; search it, don't load it whole).

## Updating the state docs
1. **Pull first:** `git pull --rebase` before editing. Only one writer at a time.
2. **Overwrite, don't append.** Replace stale lines and move detail into the file that owns it (`anime/research/`, research/, docs/). `anime/STATE.md` cap: 6,000 bytes.
3. **Bump the "Updated" line**, then commit and push to main right away. If your environment only lets you push a `claude/` branch, push there and say so; the local session merges it.
4. **Old versions:** `git log -p <file>`. Weekly snapshot tag `snapshot-YYYY-MM-DD`, made by a GitHub Action every Saturday at 15:00 UTC (cloud sessions can't push tags). No archive branches.
5. **MASTER.md is frozen** (26 Nov): don't edit it.
