# SINTEF Zenodo 20086298 — GITT + p-OCV+hold(평형 프로토콜) 다운로드 (resume·재실행 안전)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$dir = "D:\Projects\Project_Anode_Fit\Claude\results\comp_v26_data\raw"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$log = "D:\Projects\Project_Anode_Fit\Claude\results\comp_v26_data\dl_log.txt"
function Log($m) { $t = Get-Date -Format 'HH:mm:ss'; "$t $m" | Tee-Object -FilePath $log -Append }

try {
  $rec = Invoke-RestMethod -Uri "https://zenodo.org/api/records/20086298" -TimeoutSec 120
} catch {
  Log "API FAIL: $($_.Exception.Message)"; exit 2
}
Log "record OK, files=$($rec.files.Count)"
# 평형 프로토콜만: p-ocvhold(전 전극·소형) + gitt(gitthold 제외, 전 전극·평형)
$want = $rec.files | Where-Object {
  ($_.key -match '(?i)ocvhold') -or (($_.key -match '(?i)gitt') -and ($_.key -notmatch '(?i)gitthold'))
} | Sort-Object { $_.size }
Log "선택 파일 $($want.Count)개:"
$want | ForEach-Object { Log ("  {0,-72} {1,7:N1}MB" -f $_.key, ($_.size/1MB)) }

$done = 0; $skip = 0; $fail = 0
foreach ($f in $want) {
  $out = Join-Path $dir $f.key
  if ((Test-Path $out) -and ((Get-Item $out).Length -eq $f.size)) { $skip++; continue }  # resume: 완결분 스킵
  $url = $f.links.self
  $tmp = "$out.part"
  try {
    Log "다운로드 $($f.key) ($([math]::Round($f.size/1MB,1))MB)..."
    Invoke-WebRequest -Uri $url -OutFile $tmp -TimeoutSec 3600
    if ((Get-Item $tmp).Length -eq $f.size) { Move-Item -Force $tmp $out; $done++; Log "  OK" }
    else { Log "  크기 불일치 — 재시도 대상"; $fail++ }
  } catch { Log "  FAIL: $($_.Exception.Message)"; $fail++ }
}
Log "완료: 신규 $done · 스킵(기존) $skip · 실패 $fail"
if ($fail -gt 0) { exit 1 } else { exit 0 }
