# @papercheques: read first (loaded in every local and cloud session)

Current state, findings and next steps: @MASTER.md

## Who / how to work
- Vyx (they/them) runs @papercheques, a faceless scenery/mood TikTok. The goal is clout (views/followers), not money. Vyx has limited coding: Vyx directs, Claude builds.
- Lead with the answer. Use step lists. Explain syntax/errors, not plan logic.
- Challenge weak ideas before building. Give one recommendation.
- Never claim something works unless it was checked.
- Label every number as sourced (say where) or estimate.
- Don't move or reorganise files without a yes. Don't bring up swimming.
- **Check status first:** Vyx posts and runs Content check lite on their own, so log.csv lags behind. Before planning posts, confirm what was already posted or rejected, then record it.

## Sessions: one-shot, GitHub is the memory
Vyx never reopens a finished session. Each new session starts from this file, MASTER.md and `git log -15 --stat --invert-grep --grep='^watch:'` (this hides the watch routine's data commits). Never rely on an earlier chat.
- **During a session:** push after every change of state (a clip in, a post made, a check result, a decision).
- **When Vyx says "end session":**
  1. `git pull --rebase`.
  2. Write every new fact, decision and open question into the file that owns it: MASTER.md (under the cap), log.csv, library/, docs/ or reports/.
  3. Commit and push to main. Check that `git ls-remote origin main` matches `git rev-parse HEAD`.
  4. Reply with a summary of 3–5 lines and the commit hash. If something couldn't be saved, say what.

## Hard rules (never break, whoever asks)
1. **Editing is OK, evading isn't** (Vyx, 21 Oct). Colour correction, exposure, denoise, re-export and trims are fine. Still banned: any change made to fool TikTok's duplicate matching (mirroring, speed changes, borders/overlays/noise added to dodge detection). Keep the untouched original and save edits as `pNN <content> edit.mp4`.
2. **Permission and credit:** only post clips whose creator allowed reuse (拿了留痕 / 随便拿 / 可以拿 / 原创素材 in the caption, or a yes by DM). Credit them. Prefer the original file. Permissions for p50–p72 were asked with "不剪辑、不加字" (no cutting/editing, no text). For those clips, keep the full length; colour correction only. New requests use the DM in `docs/methods.md` §3.
3. **Never play @papercheques videos in a browser, and scripts never load or download our own video pages (`/video/<id>`) or files** (confirmed 21 Oct). Allowed and expected: our profile page and the item_list post list, via `research/scripts/pull_account.py`. For other accounts: grid covers only, never hover tiles.
4. **Never ask for API keys or passwords in chat.** No third-party upload tools or anything that needs the TikTok login (e.g. "HD by Rein").

## Where work runs
- **Local (Vyx's PC, D:\cheques):** anything needing the Douyin login (built-in browser pane), the video files, ffmpeg or the PowerShell tools. That covers sourcing, downloads, pre-post checks and the library page. Python can't run from Claude's shell here.
- **Cloud (Claude Code on the web, this repo):** public TikTok data pulls, Python/numpy models and scheduled refreshes. It has no Douyin login and no video files.
- **The repo is the bridge.** Video files never go in it (see .gitignore).
- **Weekly routine** "papercheques weekly analysis": Saturdays 13:00 UTC (9 AM EDT / 8 AM EST), Sonnet 5.5, environment "Hi". It runs rival-analyst → self-analyst → editor and pushes to main. Manage it at https://claude.ai/code/routines/trig_01MAPoQSqFEPnTD3oJKjA9sL
- **Watch routine** "papercheques watch rvf5567": every 6 h until 5 Nov. It pulls @rvf5567 (probably kadzoo's new account, found 22 Oct) and kadzoo55871, appends snapshots to `research/data/watch/`, rewrites `reports/watch.md`, and pushes to main with commits starting "watch:". It wakes one standing session (session_01NHPNQzWwogn8UNzLaD8wuL since 25 Oct, Sonnet 5.5; it has no repo, so its routine prompt holds the full steps incl. add_repo + clone), because a routine created from chat starts with no repo. Delete the routine after 5 Nov: https://claude.ai/code/routines/trig_012ygYS68kuGA2j5qZHckaTV
- **Sounds routine** "papercheques Monday sounds": Mondays 07:35 Toronto time, Sonnet 5.5. It runs `research/scripts/trending_sounds.py` (sounds the network started using in the last 14 days that we haven't used; each row gets its video analytics: uses, views vs baseline; no song identification, and original sounds or uploads with no published link stay in), overwrites `reports/sounds.md`, adds `research/data/sounds/new_sounds_<date>.csv`, and pushes to main with commits starting "sounds:". It wakes one standing session (session_01L4My9cu3ULGtA7VJQsKUK5, Sonnet 5.5, steps in its first message). Song names come only from TikTok's own metadata (no outside lookup). Manage it at https://claude.ai/code/routines/trig_0189VersqgMcRxDuSeYsJjNg

## Agents (`.claude/agents/`)
| Agent | Job | Runs |
|---|---|---|
| scout | Find on-charm Douyin clips, screen them, download approved ones | local |
| gatekeeper | Pre-post checks and the post plan (sound, timing, caption) | local |
| rival-analyst | Track the competitor accounts: data pull, sounds, what's working | cloud |
| self-analyst | Analyse @papercheques posts against benchmarks and running tests | cloud (or local from log.csv) |
| editor | Fold reports into MASTER.md under the cap, commit, push | either |

## Files
`MASTER.md` current state · `docs/charm.md` aesthetic gate · `docs/methods.md` how-to · `reports/` the latest output of each agent (overwritten each run) · `research/` cloud analyses + data + scripts · `log.csv` every downloaded/posted clip · `audio/<date>/` reference audio of the top new sounds (`research/scripts/download_audio.py`, ~200 KB each; add the sound in the TikTok app when posting) · `library/` clip candidates + accounts · `tools/` PowerShell checks · `notes/project-notes.md` full history to 21 Oct (frozen; search it, don't load it whole).

## Updating MASTER.md (the moving doc)
1. **Pull first:** `git pull --rebase` before editing. Only one writer at a time.
2. **Overwrite, don't append.** Replace stale lines and move detail into the file that owns it (reports/, research/, docs/). Hard cap 8,000 bytes; a hook warns when it's over.
3. **Bump the "Updated" line**, then commit and push to main right away. If your environment only lets you push a `claude/` branch, push there and say so; the local session merges it.
4. **Old versions:** `git log -p MASTER.md`. Weekly snapshot tag `snapshot-YYYY-MM-DD`, made by a GitHub Action every Saturday at 15:00 UTC (cloud sessions can't push tags). No archive branches.
5. Agents write only their own report file. Only the main session or the editor agent edits MASTER.md.
