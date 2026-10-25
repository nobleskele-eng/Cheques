# list_links.ps1 - rebuilds D:\cheques\library\links.md: every Douyin clip link on record
# (library.csv + log.csv), marking the ones already downloaded: a pNN row in log.csv, or a file in
# inbox\ or posted\ whose name holds the video ID (e.g. douyinsaver.com-<id>.mp4).
# "posted" = a TikTok link or POSTED in the log.csv notes. Our own TikTok posts are not linked
# (hard rule 3: never play them in a browser).
# Run: powershell -ExecutionPolicy Bypass -File D:\cheques\tools\list_links.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$lib = @(Import-Csv (Join-Path $root 'library\library.csv') -Encoding UTF8)
$log = @(Import-Csv (Join-Path $root 'log.csv') -Encoding UTF8)

function Get-Id([string]$s) { if ($s -match '(7\d{18})') { $Matches[1] } }   # Douyin video IDs start with 7
function Cell([string]$s) { (($s -replace '\|', '/') -replace '\s+', ' ').Trim() }

$clips = [ordered]@{}
function Get-Clip([string]$Id) {
    if (-not $clips.Contains($Id)) {
        $clips[$Id] = [pscustomobject]@{ Id = $Id; P = 0; Got = ''; Creator = ''; Status = ''; What = ''; Posted = $false }
    }
    $clips[$Id]
}

foreach ($r in $log) {
    $id = Get-Id $r.source_link
    if (-not $id) { continue }
    $c = Get-Clip $id
    $c.Got = $r.file
    if ($r.file -match '^p(\d+) (.+)\.\w+$') { $c.P = [int]$Matches[1]; $c.Got = "p$($Matches[1])"; $c.What = $Matches[2] }
    $c.Creator = $r.creator
    $c.Posted = ($r.tiktok_link -match '/video/7') -or ($r.notes -cmatch '\bPOSTED\b')
}
foreach ($r in $lib) {
    $id = Get-Id $r.link
    if (-not $id) { $id = Get-Id $r.video_id }
    if (-not $id) { continue }
    $c = Get-Clip $id
    if (-not $c.Creator) { $c.Creator = $r.creator }
    $c.Status = $r.status
    if ($r.type) { $c.What = $r.type }
}
foreach ($d in 'inbox', 'posted') {
    $dir = Join-Path $root $d
    if (-not (Test-Path -LiteralPath $dir)) { continue }
    foreach ($f in Get-ChildItem -LiteralPath $dir -File -Recurse) {
        $id = Get-Id $f.Name
        if (-not $id) { continue }
        $c = Get-Clip $id
        if (-not $c.Got) { $c.Got = "$d file, no pNN" }
    }
}

$all = @($clips.Values)
$got = @($all | Where-Object { $_.Got } | Sort-Object @{ e = { if ($_.P) { $_.P } else { 9999 } } }, Id)
$not = @($all | Where-Object { -not $_.Got } | Sort-Object Status, Creator)

$sb = New-Object Text.StringBuilder
[void]$sb.AppendLine('# Clip links')
[void]$sb.AppendLine('')
[void]$sb.AppendLine(('Rebuilt {0} by `tools/list_links.ps1` from `library/library.csv`, `log.csv` and the file names in inbox\ and posted\. **{1} clips, {2} downloaded.** log.csv starts at p48, so earlier posts only show up if they are in the library. "posted" = a TikTok link or POSTED in the log.csv notes; our TikTok posts are not linked here (hard rule 3).' -f (Get-Date -Format 'yyyy-MM-dd'), $all.Count, $got.Count))
[void]$sb.AppendLine('')
[void]$sb.AppendLine("## Downloaded ($($got.Count))")
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| File | Creator | Douyin link | Status | What |')
[void]$sb.AppendLine('|---|---|---|---|---|')
foreach ($c in $got) {
    $parts = @()
    if ($c.Posted) { $parts += 'posted' }
    if ($c.Status) { $parts += Cell $c.Status }
    $status = $parts -join ' / '
    [void]$sb.AppendLine(('| {0} | {1} | [{2}](https://www.douyin.com/video/{2}) | {3} | {4} |' -f (Cell $c.Got), (Cell $c.Creator), $c.Id, $status, (Cell $c.What)))
}
[void]$sb.AppendLine('')
[void]$sb.AppendLine("## Not downloaded ($($not.Count))")
[void]$sb.AppendLine('')
[void]$sb.AppendLine('| Creator | Douyin link | Status | What |')
[void]$sb.AppendLine('|---|---|---|---|')
foreach ($c in $not) {
    [void]$sb.AppendLine(('| {0} | [{1}](https://www.douyin.com/video/{1}) | {2} | {3} |' -f (Cell $c.Creator), $c.Id, (Cell $c.Status), (Cell $c.What)))
}
$out = Join-Path $root 'library\links.md'
[IO.File]::WriteAllText($out, $sb.ToString(), (New-Object Text.UTF8Encoding $false))
Write-Host "$($all.Count) clips, $($got.Count) downloaded -> $out"
