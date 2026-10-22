<#
  precheck.ps1 - pre-post check for @papercheques clips

  For every clip in inbox\ it reports:
    - duration, resolution, fps, audio yes/no
    - a contact sheet of the first second (6 frames, left to right = 0.00s to 0.83s)
    - flags:
        under 5 seconds
        same footage as something in posted\ (or another inbox clip)
        no permission found (no reuse word in the file name, and no permission in log.csv)

  Run it:
    powershell -ExecutionPolicy Bypass -File D:\cheques\tools\precheck.ps1
  Then open D:\cheques\checks\report.html in a browser.

  The first run is slow (it reads every file in posted\ once, ~7s per 4K clip).
  After that it remembers them in checks\hash-cache.txt, so only new clips are read.
#>
param(
    [string[]]$Inbox,
    [string[]]$Posted,
    [string]$Out,
    [string]$Log
)

# ---- rules -----------------------------------------------------------------
$MinSeconds      = 5      # shorter than this gets flagged
$MaxDistance     = 10     # how different two frames can be (0-64) and still count as the same shot
$SameFootage     = 0.25   # share of frames that match -> "same footage" (tested: real reuse 29-100%, unrelated clips 0-15%)
$MaybeSame       = 0.12   # share of frames that match -> "check by eye"
$PermissionWords = '拿了留痕', '随便拿', '可以拿', '原创素材'
$VideoExt        = '.mp4', '.mov', '.m4v', '.mkv', '.webm'
# -----------------------------------------------------------------------------

$root = Split-Path $PSScriptRoot -Parent
if (-not $Inbox)  { $Inbox  = @(Join-Path $root 'inbox') }
if (-not $Posted) { $Posted = @(Join-Path $root 'posted') }
if (-not $Out)    { $Out    = Join-Path $root 'checks' }
if (-not $Log)    { $Log    = Join-Path $root 'log.csv' }
[Console]::OutputEncoding = [Text.Encoding]::UTF8

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { Write-Host 'ffmpeg not found.'; exit 1 }

# Frame fingerprints. Each sampled frame (2 per second) is shrunk to 9x8 grey pixels and turned into a
# 64-bit "difference hash": survives resizing, re-encoding and light colour changes. A second hash is
# taken from the centre 9:16 crop, so a vertical edit cut out of a landscape clip still matches.
if (-not ('FrameHash' -as [type])) {
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Text;

public class FrameHash {
    public ulong[] H;   // hashes
    public int[] F;     // which sampled frame each hash came from

    // raw = grey frames of 18x8 bytes: left 9x8 = whole frame, right 9x8 = centre 9:16 crop
    public static FrameHash FromRaw(byte[] raw) {
        var h = new List<ulong>(); var f = new List<int>();
        int size = 18 * 8, n = raw.Length / size;
        for (int fr = 0; fr < n; fr++) {
            for (int half = 0; half < 2; half++) {
                int x0 = fr * size + half * 9;
                double sum = 0, sum2 = 0;
                for (int y = 0; y < 8; y++) for (int x = 0; x < 9; x++) {
                    double v = raw[x0 + y * 18 + x]; sum += v; sum2 += v * v;
                }
                double mean = sum / 72.0;
                if (Math.Sqrt(Math.Max(0, sum2 / 72.0 - mean * mean)) < 4.0) continue;  // flat frame (black, fog): no information
                ulong hash = 0; int bit = 0;
                for (int y = 0; y < 8; y++) for (int x = 0; x < 8; x++) {
                    int i = x0 + y * 18 + x;
                    if (raw[i] < raw[i + 1]) hash |= 1UL << bit;
                    bit++;
                }
                int pop = Pop(hash);
                if (pop < 6 || pop > 58) continue;  // near-uniform gradient: matches too many things
                h.Add(hash); f.Add(fr);
            }
        }
        return new FrameHash { H = h.ToArray(), F = f.ToArray() };
    }

    public string ToText() {
        var sb = new StringBuilder();
        for (int i = 0; i < H.Length; i++) {
            if (i > 0) sb.Append(',');
            sb.Append(H[i].ToString("x16")).Append(':').Append(F[i]);
        }
        return sb.ToString();
    }

    public static FrameHash Parse(string text) {
        var h = new List<ulong>(); var f = new List<int>();
        if (!string.IsNullOrEmpty(text)) {
            foreach (var p in text.Split(',')) {
                var kv = p.Split(':');
                h.Add(Convert.ToUInt64(kv[0], 16)); f.Add(int.Parse(kv[1]));
            }
        }
        return new FrameHash { H = h.ToArray(), F = f.ToArray() };
    }

    static int Pop(ulong x) {
        x = x - ((x >> 1) & 0x5555555555555555UL);
        x = (x & 0x3333333333333333UL) + ((x >> 2) & 0x3333333333333333UL);
        x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0FUL;
        return (int)((x * 0x0101010101010101UL) >> 56);
    }

    // share of a's frames that have a near-identical frame somewhere in b
    static double Share(FrameHash a, FrameHash b, int maxDist) {
        var all = new HashSet<int>(a.F);
        if (all.Count == 0 || b.H.Length == 0) return 0;
        var hit = new HashSet<int>();
        for (int i = 0; i < a.H.Length; i++) {
            if (hit.Contains(a.F[i])) continue;
            for (int j = 0; j < b.H.Length; j++) {
                if (Pop(a.H[i] ^ b.H[j]) <= maxDist) { hit.Add(a.F[i]); break; }
            }
        }
        return (double)hit.Count / all.Count;
    }

    // checked both ways, so a short post cut from a long source still scores high
    public static double Match(FrameHash a, FrameHash b, int maxDist) {
        return Math.Max(Share(a, b, maxDist), Share(b, a, maxDist));
    }
}
'@
}

function Get-Videos([string[]]$Items, [switch]$Recurse) {
    foreach ($i in $Items) {
        if (Test-Path -LiteralPath $i -PathType Container) {
            Get-ChildItem -LiteralPath $i -File -Recurse:$Recurse |
                Where-Object { $VideoExt -contains $_.Extension.ToLower() }
        } elseif (Test-Path -LiteralPath $i -PathType Leaf) {
            Get-Item -LiteralPath $i
        }
    }
}

function Get-Info($File) {
    $json = & ffprobe -v error -show_entries 'format=duration:stream=codec_type,width,height,avg_frame_rate:stream_side_data=rotation' -of json $File.FullName | Out-String
    if ($LASTEXITCODE -ne 0 -or -not $json) { return $null }
    $p = $json | ConvertFrom-Json
    $v = @($p.streams | Where-Object { $_.codec_type -eq 'video' })[0]
    if (-not $v) { return $null }
    $w = [int]$v.width; $h = [int]$v.height
    $rot = @($v.side_data_list | Where-Object { $_.rotation } | ForEach-Object { [int]$_.rotation })[0]
    if ([math]::Abs($rot) -eq 90) { $w, $h = $h, $w }   # phone clips stored sideways
    $fps = 0
    if ($v.avg_frame_rate -match '^(\d+)/(\d+)$' -and [int]$Matches[2] -gt 0) { $fps = [int]$Matches[1] / [int]$Matches[2] }
    [pscustomobject]@{
        Seconds = [double]$p.format.duration
        Width   = $w
        Height  = $h
        Fps     = $fps
        Audio   = @($p.streams | Where-Object { $_.codec_type -eq 'audio' }).Count -gt 0
    }
}

$cacheFile = Join-Path $Out 'hash-cache.txt'
$cache = @{}
$cacheDirty = $false

function Get-FrameHash($File) {
    $key = '{0}|{1}|{2}' -f $File.Name, $File.Length, $File.LastWriteTimeUtc.Ticks
    if ($cache.ContainsKey($key)) { return [FrameHash]::Parse($cache[$key]) }
    $tmp = Join-Path $env:TEMP ('precheck_' + [guid]::NewGuid().ToString('N') + '.raw')
    $graph = "[0:v]fps=2,scale=288:-2:flags=area,format=gray,split[a][b];[a]scale=9:8:flags=area[x];" +
             "[b]crop=w='min(iw,ih*9/16)':h='min(ih,iw*16/9)',scale=9:8:flags=area[y];[x][y]hstack[o]"
    & ffmpeg -v error -nostdin -y -i $File.FullName -an -filter_complex $graph -map '[o]' -f rawvideo -pix_fmt gray $tmp
    $ok = ($LASTEXITCODE -eq 0) -and (Test-Path -LiteralPath $tmp)
    $fh = $null
    if ($ok) {
        $fh = [FrameHash]::FromRaw([IO.File]::ReadAllBytes($tmp))
        $cache[$key] = $fh.ToText()
        $script:cacheDirty = $true
    }
    Remove-Item -LiteralPath $tmp -ErrorAction SilentlyContinue
    return $fh
}

function New-Sheet($File, $Info, [string]$Path) {
    # first second: 6 frames side by side (vertical clips) or 3x2 (landscape)
    $layout = if ($Info.Width -gt $Info.Height) { 'scale=-2:240,tile=3x2' } else { 'scale=-2:400,tile=6x1' }
    & ffmpeg -v error -nostdin -y -t 1 -i $File.FullName -an -vf "fps=6,$layout" -frames:v 1 -q:v 3 $Path
    return ($LASTEXITCODE -eq 0) -and (Test-Path -LiteralPath $Path)
}

# ---- go ----------------------------------------------------------------------
$inboxFiles  = @(Get-Videos $Inbox)
$inboxPaths  = $inboxFiles | ForEach-Object { $_.FullName }
$postedFiles = @(Get-Videos $Posted -Recurse | Where-Object { $inboxPaths -notcontains $_.FullName })
if ($inboxFiles.Count -eq 0) { Write-Host "No clips found in: $($Inbox -join ', ')"; exit }

$sheetDir = Join-Path $Out 'sheets'
New-Item -ItemType Directory -Force -Path $sheetDir | Out-Null
Get-ChildItem -LiteralPath $sheetDir -Filter 'sheet_*.jpg' | Remove-Item
if (Test-Path -LiteralPath $cacheFile) {
    foreach ($line in [IO.File]::ReadAllLines($cacheFile, [Text.Encoding]::UTF8)) {
        $parts = $line -split "`t"
        if ($parts.Count -eq 2) { $cache[$parts[0]] = $parts[1] }
    }
}

$logRows = @()
if (Test-Path -LiteralPath $Log) { $logRows = @(Import-Csv -LiteralPath $Log -Encoding UTF8) }

Write-Host "Reading $($postedFiles.Count) posted clips (cached ones are instant)..."
$refs = @()
$n = 0
foreach ($f in $postedFiles) {
    $n++
    Write-Progress -Activity 'Fingerprinting posted clips' -Status $f.Name -PercentComplete (100 * $n / $postedFiles.Count)
    $fh = Get-FrameHash $f
    if ($fh) { $refs += [pscustomobject]@{ Name = $f.Name; Where = 'posted'; Hash = $fh } }
}
Write-Progress -Activity 'Fingerprinting posted clips' -Completed

Write-Host "Checking $($inboxFiles.Count) inbox clips..."
$results = @()
$n = 0
foreach ($f in $inboxFiles) {
    $n++
    Write-Progress -Activity 'Checking inbox' -Status $f.Name -PercentComplete (100 * $n / $inboxFiles.Count)
    $info = Get-Info $f
    $sheetName = 'sheet_{0:d3}.jpg' -f $n
    $hasSheet = $info -and (New-Sheet $f $info (Join-Path $sheetDir $sheetName))
    $results += [pscustomobject]@{ File = $f; Info = $info; Sheet = $(if ($hasSheet) { "sheets/$sheetName" }); Hash = (Get-FrameHash $f); Flags = @(); Matches = @() }
}
Write-Progress -Activity 'Checking inbox' -Completed

# compare each inbox clip with everything in posted\ and with the other inbox clips
$pairs = @()
foreach ($r in $results) {
    $others = $refs + @($results | Where-Object { $_ -ne $r -and $_.Hash } |
        ForEach-Object { [pscustomobject]@{ Name = $_.File.Name; Where = 'inbox'; Hash = $_.Hash } })
    if ($r.Hash) {
        $r.Matches = @($others | ForEach-Object {
            $s = [FrameHash]::Match($r.Hash, $_.Hash, $MaxDistance)
            if ($s -ge 0.05) { $pairs += [pscustomobject]@{ clip = $r.File.Name; other = $_.Name; where = $_.Where; score = [math]::Round($s, 2) } }
            if ($s -ge $MaybeSame) { [pscustomobject]@{ Name = $_.Name; Where = $_.Where; Score = $s } }
        } | Sort-Object Score -Descending | Select-Object -First 3)
    }

    $flags = @()
    if (-not $r.Info) { $flags += [pscustomobject]@{ Level = 'red'; Text = "couldn't read this file" } }
    elseif ($r.Info.Seconds -lt $MinSeconds) { $flags += [pscustomobject]@{ Level = 'red'; Text = ('under {0}s ({1:0.0}s)' -f $MinSeconds, $r.Info.Seconds) } }
    if ($r.Hash -and $r.Hash.H.Length -eq 0) { $flags += [pscustomobject]@{ Level = 'amber'; Text = 'too dark/flat to fingerprint - duplicate check skipped' } }
    foreach ($m in $r.Matches) {
        $pct = [math]::Round(100 * $m.Score)
        if ($m.Score -ge $SameFootage) { $flags += [pscustomobject]@{ Level = 'red';   Text = "same footage as $($m.Where)\$($m.Name) ($pct% of frames match)" } }
        else                           { $flags += [pscustomobject]@{ Level = 'amber'; Text = "maybe same footage as $($m.Where)\$($m.Name) ($pct%) - check by eye" } }
    }
    $word = $PermissionWords | Where-Object { $r.File.Name.Contains($_) } | Select-Object -First 1
    $logged = $logRows | Where-Object { $_.file -eq $r.File.Name -and $_.permission } | Select-Object -First 1
    if ($logged)    { $flags += [pscustomobject]@{ Level = 'ok'; Text = "permission: $($logged.permission)" } }
    elseif ($word)  { $flags += [pscustomobject]@{ Level = 'ok'; Text = "permission word in title: $word" } }
    else            { $flags += [pscustomobject]@{ Level = 'red'; Text = 'no permission found - log how you got it' } }
    $r.Flags = $flags
}

# ---- report ------------------------------------------------------------------
function ConvertTo-Html5([string]$s) { [Net.WebUtility]::HtmlEncode($s) }
$sb = New-Object Text.StringBuilder
[void]$sb.Append(@"
<!doctype html><html><head><meta charset="utf-8"><title>Pre-post check</title>
<style>
body{font:14px/1.45 system-ui,sans-serif;margin:24px;background:#f6f6f4;color:#1b1b1b}
.clip{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px 16px;margin:0 0 16px}
.name{font-weight:600;word-break:break-all}.meta{color:#555;margin:2px 0 8px}
.flag{display:inline-block;border-radius:4px;padding:1px 8px;margin:0 6px 6px 0;font-size:13px}
.red{background:#fde2e1;color:#8a1c17}.amber{background:#fdf0d5;color:#7a4b00}.ok{background:#e3f1e4;color:#1d5b26}
img{max-width:100%;border-radius:4px;display:block}.note{color:#666}
</style></head><body>
<h2>Pre-post check</h2>
<p class="note">$(Get-Date -Format 'yyyy-MM-dd HH:mm') &middot; $($results.Count) inbox clips vs $($refs.Count) posted clips &middot; contact sheet = first second, left to right 0.00s &rarr; 0.83s</p>
"@)
foreach ($r in $results) {
    $i = $r.Info
    $meta = if ($i) { '{0:0.0}s &middot; {1}x{2} &middot; {3:0.##} fps &middot; audio: {4}' -f $i.Seconds, $i.Width, $i.Height, $i.Fps, $(if ($i.Audio) { 'yes' } else { 'no' }) } else { 'unreadable' }
    [void]$sb.Append("<div class='clip'><div class='name'>$(ConvertTo-Html5 $r.File.Name)</div><div class='meta'>$meta</div><div>")
    foreach ($fl in $r.Flags) { [void]$sb.Append("<span class='flag $($fl.Level)'>$(ConvertTo-Html5 $fl.Text)</span>") }
    [void]$sb.Append('</div>')
    if ($r.Sheet) { [void]$sb.Append("<img src='$($r.Sheet)' alt='first second'>") }
    [void]$sb.Append('</div>')
}
[void]$sb.Append('</body></html>')
$reportPath = Join-Path $Out 'report.html'
[IO.File]::WriteAllText($reportPath, $sb.ToString(), (New-Object Text.UTF8Encoding $false))
$pairs | Sort-Object score -Descending | Export-Csv -LiteralPath (Join-Path $Out 'matches.csv') -NoTypeInformation -Encoding UTF8

if ($cacheDirty) {
    $lines = $cache.GetEnumerator() | ForEach-Object { "$($_.Key)`t$($_.Value)" }
    [IO.File]::WriteAllLines($cacheFile, [string[]]$lines, (New-Object Text.UTF8Encoding $false))
}

# ---- console summary ---------------------------------------------------------
Write-Host ''
foreach ($r in $results) {
    $worst = if ($r.Flags.Level -contains 'red') { 'FIX ' } elseif ($r.Flags.Level -contains 'amber') { 'LOOK' } else { 'OK  ' }
    $len = if ($r.Info) { '{0,5:0.0}s' -f $r.Info.Seconds } else { '    ?' }
    Write-Host "$worst $len  $($r.File.Name)"
    foreach ($fl in $r.Flags | Where-Object { $_.Level -ne 'ok' }) { Write-Host "            - $($fl.Text)" }
}
Write-Host ''
Write-Host "Report: $reportPath"
