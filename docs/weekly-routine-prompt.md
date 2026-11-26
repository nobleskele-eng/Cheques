# Weekly routine prompt (paste-in, 26 Nov)
Claude can't edit this routine (it was made outside Claude Code). To apply: open https://claude.ai/code/routines/trig_01MAPoQSqFEPnTD3oJKjA9sL, rename it "TikTok weekly scoreboard", replace the whole prompt with the block below, save. Keep the schedule, model and environment as they are.

```
This is the scheduled weekly scoreboard for my TikTok accounts (repo nobleskele-eng/Cheques). Mains: @chequethetime and @duskism; also @stayvyxed. The scenery accounts @papercheques and @sylvanism_ were dropped on 26 Nov: don't pull, score or write about them, and don't touch MASTER.md (frozen history). Nobody is watching this run, so work through it on your own and don't stop to ask questions.

1. Read CLAUDE.md first (it pulls in anime/STATE.md and accounts.md) and obey the hard rules.
   - What I authorise: fetching public profile pages and the item_list post list for my own accounts @stayvyxed, @chequethetime and @duskism, and for the anime editors I track: @smokinsasa7, @.sadaqatt and @zrivvn. Do it only through `python3 -I research/scripts/pull_account.py <handles>`; don't hand-roll curl/fetch commands for TikTok.
   - Off-limits: video pages (/video/<id>) and video files of any of my accounts (never load, play or download them).
   - The script stops at the first 403, captcha page, empty response or connection error. Don't re-run it or work around it (rule 4).
   - No logins, keys or third-party upload tools. Don't run the retired agents in .claude/agents/.
2. Setup: `git checkout main && git pull --rebase`.
3. Do these steps yourself, in order. Run each pull as its own command, so a block in one group doesn't stop the other:
   1) `python3 -I research/scripts/pull_account.py stayvyxed chequethetime duskism`
   2) `python3 -I research/scripts/pull_account.py smokinsasa7 .sadaqatt zrivvn`
   3) `python3 -I research/scripts/account_stats.py stayvyxed chequethetime duskism`. In accounts.md, update only the numbers: Followers, Median views (all settled posts, with the last 10 in brackets), Best 2026 and Latest. Tag each [C <date>] and keep the other columns and lines as they are. Replace the 'Studio screenshots wanted' line with every @stayvyxed, @chequethetime and @duskism post from the last 7 days (date UTC, views), so Vyx knows which Studio screens to send. Bump the accounts.md Updated line.
   4) `python3 -I research/scripts/refs_report.py smokinsasa7 .sadaqatt zrivvn`. It overwrites anime/refs.md; commit it as it is.
   Don't edit MASTER.md or any anime/ file other than anime/refs.md. If a pull stops early, still run steps 3 and 4 on what exists and mark missing numbers '? (pull failed)'.
4. Anything posted less than 24 hours before this run counts as 'still collecting': list it, but don't score it.
5. Push: before every push run `git pull --rebase`, then push to main. If pushing to main is refused, push to your claude/ branch instead and start your final message with 'NEEDS MERGE: <branch>'.
6. If a step fails (blocked pull, script error), still run the later steps on whatever data you have, and say what failed in your final message.
7. Final message, max 6 lines: coverage (videos pulled per account), one scoreboard line (followers and median views for @chequethetime, @duskism and @stayvyxed), the biggest change this week on the two mains, the best post this week from the tracked editors (account, views, x median, caption), where it was pushed, and anything that failed or needs Vyx.
```
