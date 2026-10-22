# @papercheques: read first (loaded in every local and cloud session)

Current state, findings and next steps: @MASTER.md

## Who / how to work
- Vyx (they/them) runs @papercheques, a faceless scenery/mood TikTok. The goal is clout (views/followers), not money. Vyx has limited coding: Vyx directs, Claude builds.
- Lead with the answer. Use step lists. Explain syntax/errors, not plan logic.
- Challenge weak ideas before building. Give one recommendation.
- Never claim something works unless it was checked.
- Label every number as sourced (say where) or estimate.
- Don't move or reorganise files without a yes. Don't bring up swimming.

## Hard rules (never break, whoever asks)
1. **Editing is OK, evading isn't** (Vyx, 21 Oct). Colour correction, exposure, denoise, re-export and trims are fine. Still banned: any change made to fool TikTok's duplicate matching (mirroring, speed changes, borders/overlays/noise added to dodge detection). Keep the untouched original and save edits as `pNN <content> edit.mp4`.
2. **Permission and credit:** only post clips whose creator allowed reuse (拿了留痕 / 随便拿 / 可以拿 / 原创素材 in the caption, or a yes by DM). Credit them. Prefer the original file. Permissions for p50–p72 were asked with "不剪辑、不加字" (no cutting/editing, no text). For those clips, keep the full length; colour correction only. New requests use the DM in `docs/methods.md` §3.
3. **Never play @papercheques videos in a browser, and scripts never load or download our own video pages or files** (confirmed 21 Oct). Use post lists and page data only. For other accounts: grid covers only, never hover tiles.
4. **Don't get around captchas or anti-bot checks.** TikTok "Please wait..."/"Something went wrong" or Douyin "服务器出现问题" means stop for the day.
5. **Never ask for API keys or passwords in chat.** No third-party upload tools or anything that needs the TikTok login (e.g. "HD by Rein").

## Where work runs
- **Local (Vyx's PC, D:\cheques):** anything needing the Douyin login (built-in browser pane), the video files, ffmpeg or the PowerShell tools. That covers sourcing, downloads, pre-post checks and the library page. Python can't run from Claude's shell here.
- **Cloud (Claude Code on the web, this repo):** public TikTok data pulls, Python/numpy models and scheduled refreshes. It has no Douyin login and no video files.
- **The repo is the bridge.** Video files never go in it (see .gitignore).
- **Weekly routine** "papercheques weekly analysis": Saturdays 13:00 UTC (9 AM EDT / 8 AM EST), Sonnet 5.5, environment "Hi". It runs rival-analyst → self-analyst → editor and pushes to main. Manage it at https://claude.ai/code/routines/trig_01MAPoQSqFEPnTD3oJKjA9sL

## Agents (`.claude/agents/`)
| Agent | Job | Runs |
|---|---|---|
| scout | Find on-charm Douyin clips, screen them, download approved ones | local |
| gatekeeper | Pre-post checks and the post plan (sound, timing, caption) | local |
| rival-analyst | Track the competitor accounts: data pull, sounds, what's working | cloud |
| self-analyst | Analyse @papercheques posts against benchmarks and running tests | cloud (or local from log.csv) |
| editor | Fold reports into MASTER.md under the cap, commit, push | either |

## Files
`MASTER.md` current state · `docs/charm.md` aesthetic gate · `docs/methods.md` how-to · `reports/` the latest output of each agent (overwritten each run) · `research/` cloud analyses + data + scripts · `log.csv` every downloaded/posted clip · `library/` clip candidates + accounts · `tools/` PowerShell checks · `notes/project-notes.md` full history to 21 Oct (frozen; search it, don't load it whole).

## Updating MASTER.md (the moving doc)
1. **Pull first:** `git pull --rebase` before editing. Only one writer at a time.
2. **Overwrite, don't append.** Replace stale lines and move detail into the file that owns it (reports/, research/, docs/). Hard cap 8,000 bytes; a hook warns when it's over.
3. **Bump the "Updated" line**, then commit and push to main right away. If your environment only lets you push a `claude/` branch, push there and say so; the local session merges it.
4. **Old versions:** `git log -p MASTER.md`. Weekly snapshot tag `snapshot-YYYY-MM-DD`. No archive branches.
5. Agents write only their own report file. Only the main session or the editor agent edits MASTER.md.
