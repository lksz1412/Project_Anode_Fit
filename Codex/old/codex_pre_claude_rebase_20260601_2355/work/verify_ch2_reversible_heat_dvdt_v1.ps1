param(
  [Parameter(Mandatory=$true)]
  [string]$TexPath
)

$ErrorActionPreference = "Stop"

$text = Get-Content -Raw -LiteralPath $TexPath
$lines = $text -split "`r?`n"

$labels = [regex]::Matches($text, "\\label\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$refs = [regex]::Matches($text, "\\(?:eq)?ref\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$bibitems = [regex]::Matches($text, "\\bibitem\{([^}]+)\}") | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$cites = [regex]::Matches($text, "\\cite\{([^}]+)\}") | ForEach-Object {
  $_.Groups[1].Value -split "," | ForEach-Object { $_.Trim() }
} | Where-Object { $_ } | Sort-Object -Unique

$missingRefs = @($refs | Where-Object { $_ -notin $labels })
$missingCites = @($cites | Where-Object { $_ -notin $bibitems })

$patterns = [ordered]@{
  "xi_symbol" = "\\xi"
  "Codex" = "Codex"
  "audit_lower" = "audit"
  "Ralph" = "Ralph"
  "solver" = "solver"
  "fallback" = "fallback"
  "korean_regression" = "회귀"
  "zero_to_one_ascii" = "0 -> 1"
  "step_function" = "step-function"
  "Vapp_entropy_direct" = "V_\{n,\\app\}.*entropy coefficient"
}

$patternCounts = [ordered]@{}
foreach ($key in $patterns.Keys) {
  $patternCounts[$key] = ([regex]::Matches($text, $patterns[$key])).Count
}

$requiredPatterns = [ordered]@{
  "h_eq_definition" = "h_n\^\{\\eqs\}"
  "h_dyn_definition" = "h_n\^\{\\dyn\}"
  "h_app_definition" = "h_n\^\{\\app\}"
  "qrev" = "\\dot Q_\{\\rev,n\}"
  "qirr" = "\\dot Q_\{\\irr,n\}"
  "tail_spectrum" = "A_L\(\\lambda;T,\\psi\)"
  "charge_balance_fixed_q" = "\\left\(\\frac\{\\partial V_\{n,\\eqs\}\}\{\\partial T\}\\right\)_q"
}

$requiredCounts = [ordered]@{}
foreach ($key in $requiredPatterns.Keys) {
  $requiredCounts[$key] = ([regex]::Matches($text, $requiredPatterns[$key])).Count
}

$xelatex = Get-Command xelatex -ErrorAction SilentlyContinue

[pscustomobject]@{
  TexPath = (Resolve-Path -LiteralPath $TexPath).Path
  Lines = $lines.Count
  SHA256 = (Get-FileHash -LiteralPath $TexPath -Algorithm SHA256).Hash
  BeginCount = ([regex]::Matches($text, "\\begin\{")).Count
  EndCount = ([regex]::Matches($text, "\\end\{")).Count
  OpenBraceCount = ([regex]::Matches($text, "\{")).Count
  CloseBraceCount = ([regex]::Matches($text, "\}")).Count
  LabelCount = $labels.Count
  RefCount = $refs.Count
  MissingRefs = $missingRefs
  CiteCount = $cites.Count
  BibitemCount = $bibitems.Count
  MissingCites = $missingCites
  PatternCounts = $patternCounts
  RequiredCounts = $requiredCounts
  Xelatex = if ($xelatex) { $xelatex.Source } else { "NOT_FOUND" }
}
