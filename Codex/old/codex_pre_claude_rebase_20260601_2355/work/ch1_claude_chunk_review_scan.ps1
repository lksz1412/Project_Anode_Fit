param(
  [Parameter(Mandatory=$true)]
  [string]$TexPath,
  [Parameter(Mandatory=$true)]
  [string]$OutJson
)

$ErrorActionPreference = "Stop"

$lines = Get-Content -LiteralPath $TexPath
$chunkSizes = @(41, 53, 67, 79, 97, 113, 137, 163, 199, 251)
$patterns = [ordered]@{
  "xi_symbol" = "\\xi"
  "theta_symbol" = "\\theta"
  "theta_big" = "\\Theta"
  "plan_a" = "Plan A"
  "plan_b" = "Plan B"
  "solver_or_dae" = "solver|DAE|root-find|수치"
  "fitting" = "피팅|fitting|회귀|fit"
  "ch6" = "Ch\.6|Chapter 6"
  "process_marker" = "RB|Date:|Author:|재구성본|plan 2026|commit"
  "heaviside_or_step" = "Heaviside|step-function|0\\!\\to\\!1|0\\to1|threshold|switch"
  "single_L" = "\bL\b|L\\equiv|L="
  "Lq" = "L_q"
  "epsilon_floor" = "\\epsilon_Q|floor|하한"
  "volterra_fredholm" = "Volterra|Fredholm|ratio"
}

$passes = @()
foreach ($size in $chunkSizes) {
  $chunks = @()
  for ($start = 0; $start -lt $lines.Count; $start += $size) {
    $end = [Math]::Min($start + $size - 1, $lines.Count - 1)
    $chunkText = ($lines[$start..$end] -join "`n")
    $counts = [ordered]@{}
    foreach ($key in $patterns.Keys) {
      $counts[$key] = ([regex]::Matches($chunkText, $patterns[$key])).Count
    }
    $nonzero = @{}
    foreach ($key in $counts.Keys) {
      if ($counts[$key] -gt 0) { $nonzero[$key] = $counts[$key] }
    }
    $chunks += [pscustomobject]@{
      startLine = $start + 1
      endLine = $end + 1
      lineCount = $end - $start + 1
      nonzeroPatternCounts = $nonzero
    }
  }
  $totalCounts = [ordered]@{}
  foreach ($key in $patterns.Keys) {
    $totalCounts[$key] = 0
  }
  foreach ($chunk in $chunks) {
    foreach ($key in $chunk.nonzeroPatternCounts.Keys) {
      $totalCounts[$key] += [int]$chunk.nonzeroPatternCounts[$key]
    }
  }
  $passes += [pscustomobject]@{
    chunkSize = $size
    chunkCount = $chunks.Count
    chunks = $chunks
    totalPatternCounts = $totalCounts
  }
}

$refs = [regex]::Matches(($lines -join "`n"), "\\(?:eq)?ref\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$labels = [regex]::Matches(($lines -join "`n"), "\\label\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$cites = [regex]::Matches(($lines -join "`n"), "\\cite\{([^}]+)\}") | ForEach-Object {
  $_.Groups[1].Value -split "," | ForEach-Object { $_.Trim() }
} | Where-Object { $_ } | Sort-Object -Unique
$bibitems = [regex]::Matches(($lines -join "`n"), "\\bibitem\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

$result = [pscustomobject]@{
  texPath = (Resolve-Path -LiteralPath $TexPath).Path
  lineCount = $lines.Count
  chunkSizes = $chunkSizes
  passCount = $passes.Count
  passes = $passes
  labels = $labels.Count
  refs = $refs.Count
  missingRefs = @($refs | Where-Object { $_ -notin $labels })
  cites = $cites.Count
  bibitems = $bibitems.Count
  missingCites = @($cites | Where-Object { $_ -notin $bibitems })
  sha256 = (Get-FileHash -LiteralPath $TexPath -Algorithm SHA256).Hash
}

$result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $OutJson -Encoding UTF8
$result | ConvertTo-Json -Depth 4
