param(
  [string]$Path = 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex'
)
$lines = Get-Content -LiteralPath $Path
$sizes = 37,49,61,73,89,109,131,157,191,233
foreach($size in $sizes){
  $chunks = [math]::Ceiling($lines.Count / $size)
  Write-Output "Pass chunk_size=$size chunk_count=$chunks total_lines=$($lines.Count)"
  for($start=1; $start -le $lines.Count; $start += $size){
    $end = [Math]::Min($start + $size - 1, $lines.Count)
    Write-Output ("  {0}-{1}" -f $start,$end)
  }
}
