<#
  precheck.ps1 - pre-post check for @papercheques clips

  For every clip in inbox\ it reports:
    - duration, resolution, fps, audio yes/no
    - a contact sheet of the first second (6 frames, left to right = 0.00s to 0.83s)
    - flags:
        under 5 seconds
        same footage as something in posted\ (or another inbox clip)
        no permission found (no reuse word in the file name, and no permission in log.csv)
        creator signature: small white text baked in near the edges (e.g. 韬 "Tao" bottom-centre,
          Iuk / 7na. right-middle). It takes the darkest value of each pixel over 24 frames: the
          scene moves and goes dark, a signature stays put and stays white. Flagged clips get a crop
          (left: what stays fixed, right: the real frame at full resolution). Same method as
          tools\edgecheck.js, which the scout runs on Douyin before asking.

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
$SigRed          = 80     # signature: thin fixed white strokes in one spot near the edges (known signatures 96-317,
$SigLook         = 25     #   clean moving shots 0-13; static shots also score, because lit windows stay put too)
$SigSpot         = 0.4    # share of all fixed strokes in the frame that sit in that spot (signatures 0.47-1.0; static shots mostly <0.4)
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

# Signature check. raw = n grey frames of w x h. m = darkest value of each pixel across them.
# A stroke pixel is white-ish (>=120) and >=40 brighter than the pixels 4 px away on both sides,
# across or up-down: thin lines like handwriting, not the edge of a bright area.
# Score = most stroke pixels in any 80x80 spot inside the edge band (outer 15% left/right, 12% top/bottom).
if (-not ('SigCheck' -as [type])) {
Add-Type -TypeDefinition @'
public class SigCheck {
    public static byte[] Min(byte[] raw, int w, int h) {
        int n = w * h, frames = raw.Length / n;
        var m = new byte[n];
        for (int i = 0; i < n; i++) m[i] = 255;
        for (int f = 0; f < frames; f++) {
            int o = f * n;
            for (int i = 0; i < n; i++) if (raw[o + i] < m[i]) m[i] = raw[o + i];
        }
        return m;
    }

    // returns { score, stroke pixels in the whole frame, spot centre x, spot centre y }
    public static int[] Score(byte[] m, int w, int h) {
        const int d = 4, t = 40, bright = 120, cell = 40;
        int cw = (w + cell - 1) / cell, ch = (h + cell - 1) / cell;
        var cells = new int[cw * ch];
        int x0 = (int)(w * 0.15), x1 = (int)(w * 0.85), y0 = (int)(h * 0.12), y1 = (int)(h * 0.88), all = 0;
        for (int y = d; y < h - d; y++) for (int x = d; x < w - d; x++) {
            int v = m[y * w + x]; if (v < bright) continue;
            bool across = v - m[y * w + x - d] >= t && v - m[y * w + x + d] >= t;
            bool updown = v - m[(y - d) * w + x] >= t && v - m[(y + d) * w + x] >= t;
            if (!across && !updown) continue;
            all++;
            if (x >= x0 && x < x1 && y >= y0 && y < y1) continue;
            cells[(y / cell) * cw + x / cell]++;
        }
        int top = 0, tx = 0, ty = 0;
        for (int cy = 0; cy < ch - 1; cy++) for (int cx = 0; cx < cw - 1; cx++) {
            int s = cells[cy * cw + cx] + cells[cy * cw + cx + 1] + cells[(cy + 1) * cw + cx] + cells[(cy + 1) * cw + cx + 1];
            if (s > top) { top = s; tx = (cx + 1) * cell; ty = (cy + 1) * cell; }
        }
        return new int[] { top, all, tx, ty };
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

$sigCacheFile = Join-Path $Out 'signature-cache.txt'
$sigCache = @{}
$sigDirty = $false
$markDir = Join-Path $Out 'marks'
$inv = [Globalization.CultureInfo]::InvariantCulture

# Signature check (see SigCheck above). Clips that score SigLook or more also get a crop in checks\marks\.
function Get-Signature($File, $Info) {
    $key = '{0}|{1}|{2}' -f $File.Name, $File.Length, $File.LastWriteTimeUtc.Ticks
    $id = [BitConverter]::ToString([Security.Cryptography.MD5]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($key))).Replace('-', '').Substring(0, 12)
    $img = Join-Path $markDir "$id.jpg"
    if ($sigCache.ContainsKey($key)) {
        $v = $sigCache[$key] -split ','
        $sig = [pscustomobject]@{ Score = [int]$v[0]; All = [int]$v[1]; X = [int]$v[2] / 1000; Y = [int]$v[3] / 1000; Image = $null }
        if ($sig.Score -lt $SigLook) { return $sig }
        if (Test-Path -LiteralPath $img) { $sig.Image = "marks/$id.jpg"; return $sig }
    }
    if ($Info.Seconds -lt 0.5) { return $null }

    # 24 frames spread over the clip, short side 1080 (never upscaled)
    $k = [math]::Min(1.0, 1080.0 / [math]::Min($Info.Width, $Info.Height))
    $w = 2 * [int][math]::Round($Info.Width * $k / 2); $h = 2 * [int][math]::Round($Info.Height * $k / 2)
    $rate = (24 / $Info.Seconds).ToString('0.####', $inv)
    $tmp = Join-Path $env:TEMP ('precheck_' + [guid]::NewGuid().ToString('N') + '.raw')
    & ffmpeg -v error -nostdin -y -i $File.FullName -an -vf "fps=$rate,scale=${w}:${h}:flags=area,format=gray" -f rawvideo -pix_fmt gray $tmp
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $tmp)) { return $null }
    $m = [SigCheck]::Min([IO.File]::ReadAllBytes($tmp), $w, $h)
    $r = [SigCheck]::Score($m, $w, $h)
    $sig = [pscustomobject]@{ Score = $r[0]; All = $r[1]; X = $r[2] / $w; Y = $r[3] / $h; Image = $null }

    if ($sig.Score -ge $SigLook) {
        # crop of the spot, 30% x 14% of the short side: fixed pixels (left) next to the real middle frame (right)
        New-Item -ItemType Directory -Force -Path $markDir | Out-Null
        [IO.File]::WriteAllBytes($tmp, $m)
        $S = [math]::Min($Info.Width, $Info.Height)
        $cw = 2 * [int]($S * 0.15); $ch = 2 * [int]($S * 0.071)
        $cx = [int][math]::Max(0, [math]::Min($Info.Width - $cw, $sig.X * $Info.Width - $cw / 2))
        $cy = [int][math]::Max(0, [math]::Min($Info.Height - $ch, $sig.Y * $Info.Height - $ch / 2))
        $crop = "crop=${cw}:${ch}:${cx}:${cy},format=yuv420p"
        $mid = ($Info.Seconds / 2).ToString('0.###', $inv)
        & ffmpeg -v error -nostdin -y -f rawvideo -pix_fmt gray -s "${w}x${h}" -i $tmp -ss $mid -i $File.FullName `
            -filter_complex "[0:v]scale=$($Info.Width):$($Info.Height),$crop[a];[1:v]$crop[b];[a][b]hstack" -frames:v 1 -q:v 3 $img
        if (($LASTEXITCODE -eq 0) -and (Test-Path -LiteralPath $img)) { $sig.Image = "marks/$id.jpg" }
    }
    Remove-Item -LiteralPath $tmp -ErrorAction SilentlyContinue
    $sigCache[$key] = '{0},{1},{2},{3}' -f $sig.Score, $sig.All, [int](1000 * $sig.X), [int](1000 * $sig.Y)
    $script:sigDirty = $true
    return $sig
}

function Get-Where($X, $Y) {
    $v = if ($Y -lt 0.33) { 'top' } elseif ($Y -gt 0.67) { 'bottom' } else { 'middle' }
    $h = if ($X -lt 0.33) { 'left' } elseif ($X -gt 0.67) { 'right' } else { 'centre' }
    "$v-$h"
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
if (Test-Path -LiteralPath $sigCacheFile) {
    foreach ($line in [IO.File]::ReadAllLines($sigCacheFile, [Text.Encoding]::UTF8)) {
        $parts = $line -split "`t"
        if ($parts.Count -eq 2) { $sigCache[$parts[0]] = $parts[1] }
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
    $sig = if ($info) { Get-Signature $f $info }
    $results += [pscustomobject]@{ File = $f; Info = $info; Sheet = $(if ($hasSheet) { "sheets/$sheetName" }); Hash = (Get-FrameHash $f); Sig = $sig; Flags = @(); Matches = @() }
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
    if ($r.Sig) {
        $s = $r.Sig; $where = Get-Where $s.X $s.Y
        $spot = if ($s.All -gt 0) { $s.Score / $s.All } else { 0 }
        if ($s.Score -ge $SigRed -and $spot -ge $SigSpot) { $flags += [pscustomobject]@{ Level = 'red'; Text = "creator signature likely at $where (score $($s.Score)) - check the crop; never post a baked-in name" } }
        elseif ($s.Score -ge $SigLook) { $flags += [pscustomobject]@{ Level = 'amber'; Text = "fixed white detail at $where (score $($s.Score)$(if ($spot -lt $SigSpot) { ', static shot' })) - check the crop for a signature" } }
        else { $flags += [pscustomobject]@{ Level = 'ok'; Text = "no signature found (score $($s.Score))" } }
    } elseif ($r.Info) { $flags += [pscustomobject]@{ Level = 'amber'; Text = 'signature check failed - check the edges by eye' } }
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
    if ($r.Sig -and $r.Sig.Image) {
        [void]$sb.Append("<p class='note'>Signature check: left = what stays fixed across the clip, right = the real middle frame at full resolution</p><img src='$($r.Sig.Image)' alt='signature check'>")
    }
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
if ($sigDirty) {
    $lines = $sigCache.GetEnumerator() | ForEach-Object { "$($_.Key)`t$($_.Value)" }
    [IO.File]::WriteAllLines($sigCacheFile, [string[]]$lines, (New-Object Text.UTF8Encoding $false))
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
