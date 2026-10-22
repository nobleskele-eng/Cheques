# render_library.ps1 - rebuilds D:\cheques\library\library.html from library.csv + covers\<id>.jpg
# Shows every clip except ones marked "not good enough" or already downloaded ("permission yes ...").
# Run: powershell -ExecutionPolicy Bypass -File D:\cheques\tools\render_library.ps1
$ErrorActionPreference = 'Stop'
$lib = 'D:\cheques\library'
$rows = [System.Collections.ArrayList]@(Import-Csv "$lib\library.csv" -Encoding UTF8)
function HtmlEnc([string]$s) { [Net.WebUtility]::HtmlEncode($s) }
$show = @($rows | Where-Object { $_.status -notlike '*not good enough*' -and $_.status -notlike 'permission yes*' })
# DM text = docs/methods.md section 3 (new wording from 21 Oct: allows colour correction and trims)
$dm = '你好！很喜欢你这条视频，想问一下可以发到我的TikTok（海外）账号吗？可能会稍微调色或剪短一点，不加字，文案里会注明你的抖音号。方便的话能发一下原片就更好了，谢谢！'
$sb = New-Object Text.StringBuilder
[void]$sb.Append(@"
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clip library</title>
<style>
:root{--bg:#f5f4f0;--card:#fff;--ink:#1c1c1c;--mute:#666;--line:#e3e1db;--a:#1f6f43;--b:#8a5a00;--c:#7a2e2e;--p:#2d5bd1;--btn:#1c1c1c;--btnink:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--card:#1e1e1e;--ink:#eee;--mute:#a3a3a3;--line:#2e2e2e;--a:#6fcf97;--b:#f2c94c;--c:#eb8a8a;--p:#8fb0ff;--btn:#eee;--btnink:#111}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
main{max-width:760px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:4px 0 2px}.sub{color:var(--mute);margin:0 0 14px}
.dm{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:18px}
.dm b{display:block;margin-bottom:4px}.dm p{margin:0;user-select:all}
.card{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:12px}
.card img{width:96px;height:auto;max-height:170px;object-fit:cover;border-radius:6px;flex:none;background:#000}
.card.land img{width:150px}
.body{min-width:0;flex:1}.top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.type{font-weight:600}.tier{font-size:12px;font-weight:700;padding:1px 7px;border-radius:999px;border:1px solid currentColor;flex:none}
.tA{color:var(--a)}.tB{color:var(--b)}.tC{color:var(--c)}.tP{color:var(--p)}
.who{color:var(--mute);font-size:13px;margin:2px 0 6px}.cap{font-size:13px;margin:0 0 6px;word-break:break-all}
.stats{font-size:13px;margin:0 0 6px}.note{font-size:13px;color:var(--mute);margin:0 0 8px}
a.go{display:inline-block;background:var(--btn);color:var(--btnink);text-decoration:none;border-radius:6px;padding:5px 12px;font-size:13px;font-weight:600}
h2{font-size:15px;margin:22px 0 8px;color:var(--mute);text-transform:uppercase;letter-spacing:.04em}
.acc{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:12px}
.acc img{width:100%;height:auto;border-radius:6px;display:block;margin:8px 0;background:#000}
.acc p{font-size:13px;margin:0 0 6px}.charm{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:18px;font-size:14px}
.charm ol{margin:6px 0 0;padding-left:20px}.charm li{margin-bottom:3px}
</style></head><body><main>
<h1>Clip library</h1>
<p class="sub">$($show.Count) clips · updated $(Get-Date -Format 'd MMM yyyy') · p50-p52 already downloaded · all need permission + a TikTok collision check before download</p>
<div class="charm"><b>Charm checklist (v3, 18 Oct)</b><ol>
<li>Weather or light does the work: rain, fog, snow, wind, or blue hour (lights on, navy sky), or a soft golden/pink glow.</li>
<li>Seen from street level or a window: walking, on a bridge, behind glass. No drone shots, no sky-only shots.</li>
<li>Muted, slightly dark, film-like grade. No saturated orange sunsets or bright flowers.</li>
<li>Something moves: rain, mist drifting, traffic, a train, wind.</li>
<li>Cities, cars, taxis and wet roads are fine. People can be tiny in frame, never the subject.</li>
<li>Vertical, real footage, the look is visible in the first second.</li>
</ol></div>
<div class="dm"><b>DM to send (tap and hold to copy)</b><p>$(HtmlEnc $dm)</p></div>
"@)
# Scout batches use status "to contact - batch YYYY-MM-DD": newest batch first
$batchDates = @($show | ForEach-Object { if ($_.status -match 'batch (\d{4}-\d{2}-\d{2})') { $Matches[1] } } | Sort-Object -Unique -Descending)
$dyn = foreach ($d in $batchDates) {
  $lbl = [datetime]::ParseExact($d, 'yyyy-MM-dd', $null).ToString('d MMM', [Globalization.CultureInfo]::InvariantCulture)
  @{ name = "Batch $lbl - DM these first"; tag = 'A'; rows = @($show | Where-Object { $_.status -like "*batch $d*" -and $_.tier -eq 'A' }) }
  @{ name = "Batch $lbl - backup"; tag = 'B'; rows = @($show | Where-Object { $_.status -like "*batch $d*" -and $_.tier -ne 'A' }) }
}
$groups = @($dyn) + @(
  @{ name = 'Batch 21 Oct - Chongqing accounts you sent'; tag = 'A'; rows = @($show | Where-Object { $_.status -like '*NEW batch 21 Oct*' -and $_.tier -eq 'A' }) },
  @{ name = 'Batch 21 Oct - backup'; tag = 'B'; rows = @($show | Where-Object { $_.status -like '*NEW batch 21 Oct*' -and $_.tier -eq 'B' }) },
  @{ name = 'Batch 20 Oct - summer glow, fireworks, sea (fresh, small creators)'; tag = 'A'; rows = @($show | Where-Object { $_.status -like '*NEW batch 20 Oct*' -and $_.tier -eq 'A' }) },
  @{ name = 'Batch 20 Oct - format to mine (pick a fresh day)'; tag = 'B'; rows = @($show | Where-Object { $_.status -like '*NEW batch 20 Oct*' -and $_.tier -eq 'B' }) },
  @{ name = 'Batch 19 Oct - fresh first snow and blue hour, small creators (DM these first)'; tag = 'A'; rows = @($show | Where-Object { $_.status -like '*NEW batch 19 Oct*' -and $_.tier -eq 'A' }) },
  @{ name = 'Batch 19 Oct - backup'; tag = 'B'; rows = @($show | Where-Object { $_.status -like '*NEW batch 19 Oct*' -and $_.tier -eq 'B' }) },
  @{ name = 'Your picks'; tag = 'P'; rows = @($show | Where-Object { $_.status -like '*potential*' }) },
  @{ name = 'New - closest to your picks'; tag = 'A'; rows = @($show | Where-Object { $_.status -eq 'to contact' -and $_.tier -eq 'A' }) },
  @{ name = 'New - good, one weakness'; tag = 'B'; rows = @($show | Where-Object { $_.status -eq 'to contact' -and $_.tier -eq 'B' }) },
  @{ name = 'New - big numbers, person-focused'; tag = 'C'; rows = @($show | Where-Object { $_.status -eq 'to contact' -and $_.tier -eq 'C' }) }
)
foreach ($g in $groups) {
    if (-not $g.rows.Count) { continue }
    [void]$sb.Append("<h2>$($g.name)</h2>")
    foreach ($r in $g.rows) {
        $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$lib\covers\$($r.video_id).jpg"))
        $land = if ($r.shape -eq 'LANDSCAPE') { ' land' } else { '' }
        $badge = if ($g.tag -eq 'P') { 'pick' } else { $g.tag }
        [void]$sb.Append(@"
<div class="card$land"><img src="data:image/jpeg;base64,$b64" alt="first frame">
<div class="body"><div class="top"><span class="type">$(HtmlEnc $r.type)</span><span class="tier t$($g.tag)">$badge</span></div>
<div class="who">$(HtmlEnc $r.creator) · $(HtmlEnc $r.creator_followers) followers · posted $($r.posted_utc) · $($r.length_s)s · $(HtmlEnc $r.shape)</div>
<p class="cap">$(HtmlEnc $r.caption)</p>
<p class="stats">&#9829; $(HtmlEnc $r.likes) · saves $(HtmlEnc $r.saves) · shares $(HtmlEnc $r.shares) · comments $(HtmlEnc $r.comments)</p>
<p class="note">$(HtmlEnc $r.ownership). $(HtmlEnc $r.risks)</p>
<a class="go" href="$($r.link)">Open on Douyin</a></div></div>
"@)
    }
}
$accFile = "$lib\accounts.csv"
if (Test-Path $accFile) {
    $accs = @(Import-Csv $accFile -Encoding UTF8 | Where-Object { $_.tier -ne 'C' })
    [void]$sb.Append("<h2>Accounts to mine ($($accs.Count)) - top posts by likes</h2>")
    foreach ($a in $accs) {
        $img = "$lib\accounts\$($a.img).jpg"
        $tag = if (Test-Path $img) { "<img src=`"data:image/jpeg;base64,$([Convert]::ToBase64String([IO.File]::ReadAllBytes($img)))`" alt=`"top posts`">" } else { '' }
        [void]$sb.Append(@"
<div class="acc"><div class="top"><span class="type">$(HtmlEnc $a.name)</span><span class="tier t$($a.tier)">$($a.tier)</span></div>
<div class="who">$(HtmlEnc $a.followers) followers · $(HtmlEnc $a.total_likes) likes · IP $(HtmlEnc $a.ip)</div>
<p>$(HtmlEnc $a.look)</p>$tag
<p class="stats">&#9829; $(HtmlEnc $a.top_hits)</p>
<p class="note">$(HtmlEnc $a.ownership). Next: $(HtmlEnc $a.next)</p>
<a class="go" href="$($a.link)">Open profile</a></div>
"@)
    }
}
[void]$sb.Append('</main></body></html>')
[IO.File]::WriteAllText("$lib\library.html", $sb.ToString(), (New-Object Text.UTF8Encoding $false))
"csv rows: $($rows.Count)  shown: $($show.Count)"
