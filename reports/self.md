# Self report, run 2026-10-22 (NO FRESH PULL)
**Pull blocked:** the cloud permission layer denied the profile/item_list fetch and Python runs. Nothing was retried (rule 4). Numbers below come from `research/data/papercheques_videos.csv` (pulled 21 Oct, 39 posts, 3-21 Oct) and log.csv. Rates were hand-computed. Sourced: csv.

## Last 10 posts (views as of the 21 Oct pull)
| post | UTC date | views | like% | share% | save% | len | sound | sched? | tier |
|---|---|---|---|---|---|---|---|---|---|
| 16 Oct (?) | 10-16 12:03 | 668 | 5.1 | 0.00 | 0.15 | 8s | оригинальный звук | n | not pulled |
| p48 | 10-18 00:18 | 709 | 2.5 | 0.00 | 0.28 | 6s | original sound | n | not pulled |
| p49 | 10-18 03:50 | 353 | 4.2 | 0.00 | 0.00 | 7s | original sound - F | y (+3h, log) | not pulled |
| p60 | 10-19 01:25 | 712 | 4.1 | 0.00 | 0.56 | 11s | Not Allowed | n | not pulled |
| p64 | 10-20 03:37 | 687 | 2.5 | 0.29 | 0.15 | 7s | original sound | n | not pulled |
| p67 | 10-20 03:46 | 159 | 8.2 | 0.00 | 0.00 | 9s | âm thanh gốc | n | not pulled |
| ? | 10-21 02:42 | 705 | 4.5 | 0.14 | 0.00 | 7s | original sound | n | not pulled |
| ? | 10-21 03:24 | 703 | 5.0 | 0.14 | 0.43 | 7s | whats on your nasty old mind | n | not pulled |
| ? | 10-21 04:06 | 715 | 3.9 | 0.00 | 0.14 | 7s | âm thanh gốc | n | not pulled |
| p71/p72? | 10-21 06:00 | 690 | 4.8 | 0.00 | 0.29 | 9s | оригинальный звук | y (+~114 min, ID vs time) | not pulled |

Proven-sound list: none of these 10 match it (no "yuji", "oscncs" etc.). Tier: encoding csv not refreshed. Earlier data shows 0/39 had 1080p.

## Recipe test (MASTER §3)
**Too early. New-recipe n = 0 confirmed.** p65, p66 and p68-p70 have no tiktok_link, and the four 21 Oct posts are not mapped to p-numbers or recipe fields (edit file, sound, length). Old baseline holds: median 712 views, 5.2% likes, 0.00% shares. The last 10 give a median of about 700 views and 4.5% likes, so there is no direction yet. Milestone (>=10-15% likes/view): not met. Best of all 39 is about 8.6%. p67's 8.2% is on 159 views, which is noise.

## Watch list
- Ceiling: no post above ~720 in the last 10 (record is still 2,207, 10 Oct). The low outliers (p49 353, p67 159) are both the second post within hours of another.
- FYP flag after a PASS: none known (p64 and p67 unflagged per log).
- 1080p: not checkable without a pull.
- Still collecting (<24 h): none that I can tell. The data is from 21 Oct and the latest post was 06:00 UTC that day. The four 21 Oct counts may have grown since.

## Unmatched (Vyx to fill in)
The four 21 Oct posts above (video IDs ending ...98946070, ...98956737, ...98967534, ...98967576), and every post before p48 (log.csv has no link). Nothing was written to log.csv because no match was certain.

## Suggested MASTER changes
- Add "self pull blocked 22 Oct; data is as of 21 Oct" to §7.
- §5: still need tiktok_links for the 4 posts of 21 Oct, and a note of which were made with the new recipe.
- Rerun the pull locally or from a session that is allowed to fetch the profile page.
