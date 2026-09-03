$env:PYTHONIOENCODING='utf-8'
$root='D:\Projects\Project_Anode_Fit'
$tsv=Join-Path $root 'Claude\results\handoffs\v1027-phase-1.1-inventory\iter_1\inventory_raw.tsv'
$out=Join-Path $root 'Claude\results\V1027_HISTORY_INVENTORY.md'
$rows=New-Object System.Collections.Generic.List[object]
foreach($line in (Get-Content $tsv)){ if(-not $line){continue}; $p=$line -split "`t"; $rel=$p[0].Substring($root.Length+1) -replace '\\','/'; $rows.Add([pscustomobject]@{path=$p[0];rel=$rel;lines=[int]$p[1];hash=$p[2];bytes=[long]$p[3]}) }
$byRel=@{}; foreach($r in $rows){$byRel[$r.rel]=$r}

$procMap=@(
 @('PHASE_A0-A5|PHASE_A0_|PHASE_A1_|PHASE_A3-A5','Fable v2~v10(세부: v2 이전 06-06 sec6-statmech, 추정)'),
 @('PHASE_CH3_|CH[345]_D2B','Fable v2~v10(세부: v2 이전 06-07 ch3~5 overhaul, 추정)'),
 @('PHASE_CM','Fable v2~v10(세부: v2 이전 06-08 connective-masterequation, 추정)'),
 @('PHASE_DEEP_REVIEW','Fable v2~v10(세부: 미상, 추정)'),
 @('PHASE_F\d|PHASE_F_','Fable v2~v10(세부: 미상 F0~F9, 추정)'),
 @('PHASE_FRR','Fable v2~v10(세부: 06-10 full-rereview, 추정)'),
 @('PHASE_MERGE','Fable v2~v10(세부: v2 이전 06-09 merge, 추정)'),
 @('PHASE_R0-R5|PHASE_R[0-9]_','Fable v2~v10(세부: 미상 R0~R9, 추정)'),
 @('PHASE_TBR','Fable v2~v10(세부: 06-10 textbook-rewrite, 추정)'),
 @('PHASE_V2_','Fable v2~v10(세부: v2)'),
 @('PHASE_V5RR','Fable v2~v10(세부: v5RR)'),
 @('PHASE_V5','Fable v2~v10(세부: v5)'),
 @('PHASE_V6','Fable v2~v10(세부: v6)'),
 @('PHASE_W_','Fable v2~v10(세부: v2 이전 06-06 register-revision, 추정)'),
 @('PHASE_G_','Fable v2~v10(세부: v2 이전 06-06 sec8-10, 추정)'),
 @('PHASE_TXB','Fable v2~v10(세부: v2 이전 06-06 textbook-form, 추정)'),
 @('PHASE_2TRACK','Fable v2~v10(세부: v9 2track 06-30)'),
 @('PHASE_REWORK','Fable v2~v10(세부: v10 rework 06-30)'),
 @('PHASE8_v7|V7_9x9x1x1','Fable v2~v10(세부: v7)'),
 @('PHASE8_v8|V8_LEDGER','Fable v2~v10(세부: v8)'),
 @('GRAPH_VERIFY','v1.0.10'),
 @('FABLE_REAUDIT','v1.0.12(fable reaudit)'),
 @('research/CH2_v3','Fable v2~v10(세부: Ch2 v3 survey 06-30)'),
 @('research/radius','Fable v2~v10(세부: radius survey 06-30)'),
 @('builds/ch1v10','Fable v2~v10(세부: v10)')
)
function Ver($rel){
 if($rel -eq 'CLAUDE.md'){return '횡단'}
 if($rel -like 'Claude/results/handoffs/*'){return '본 arc'}
 if($rel -eq 'Claude/plans/2026-09-02-v2-master-plan.md'){return '본 arc'}
 if($rel -eq 'Claude/docs/INDEX.md' -or $rel -eq 'Claude/plans/INDEX.md'){return '횡단'}
 if($rel -like 'Claude/plans/MASTER_ROADMAP*'){return 'Fable v2~v10(세부: 미상 — 무날짜 파일명, 추정)'}
 if($rel -like 'Claude/docs/Fable_점검/*'){return '횡단(v3→v1.0.11 감사 · 작성 v1.0.12 시점)'}
 if($rel -eq 'Claude/jcp_extract.txt'){return '횡단'}
 if($rel -match '^Claude/old/_archive/graphite_ica_ch1_(Fable|Opus)_v(\d)\.tex$'){return "Fable v2~v10(세부: v$($Matches[2]))"}
 if($rel -like 'Claude/old/*'){return '구트랙 RB'}
 if($rel -match '^Claude/docs/v1\.0\.26'){return 'v1.0.26'}
 if($rel -match '^Claude/docs/v(1\.0\.\d+(\.\d)?)/'){return "v$($Matches[1])"}
 if($rel -like 'Claude/results/comp_v24/*'){return 'v1.0.24'}
 if($rel -like 'Claude/results/comp_v26_data/*'){return 'v1.0.26'}
 if($rel -match '^Claude/results/PHASE_FB\d_RESULT'){return 'v1.0.24.1'}
 if($rel -match '^Claude/results/PHASE_V\d[BC]?_RESULT'){return 'v1.0.24(추정: completeness-validation V0~V3)'}
 if($rel -match '^Claude/results/V1024_FEEDBACK'){return 'v1.0.24.1'}
 if($rel -match 'V10(\d\d)_'){return "v1.0.$($Matches[1])"}
 if($rel -match '^Claude/plans/(\d{4})-(\d{2})-(\d{2})-(.+)\.md$'){
   $mm=$Matches[2];$dd=$Matches[3];$name=$Matches[4]
   if($name -match 'v10(\d\d)'){return "v1.0.$($Matches[1])"}
   if($name -match 'fable-reaudit'){return 'v1.0.12(fable reaudit → v12 저작)'}
   if($name -match 'anodefit'){return 'v1.0.23(추정: 날짜 07-18)'}
   if($name -match 'v5RR'){return 'Fable v2~v10(세부: v5RR)'}
   if($name -match 'ch1v(\d)'){return "Fable v2~v10(세부: v$($Matches[1]) 2track)"}
   if($name -match '-v(\d)(-|$)'){return "Fable v2~v10(세부: v$($Matches[1]))"}
   if($name -match 'rework-broadening'){return 'Fable v2~v10(세부: v10 rework)'}
   if([int]$mm -eq 6 -and [int]$dd -ge 10){return "Fable v2~v10(세부: 날짜 06-$dd)"}
   return "Fable v2~v10(세부: v2 이전 $mm-$dd, 추정)"
 }
 if($rel -match '^Claude/results/process/HANDOVER_2026-(\d{2})-(\d{2})_(.+)\.md$'){ $mm=$Matches[1];$dd=$Matches[2];$name=$Matches[3]; if($name -match '-v(\d)-'){return "Fable v2~v10(세부: v$($Matches[1]))"}; if([int]$mm -eq 6 -and [int]$dd -ge 10){return "Fable v2~v10(세부: 날짜 06-$dd)"}; return "Fable v2~v10(세부: v2 이전 $mm-$dd, 추정)" }
 foreach($m in $procMap){ if($rel -match $m[0]){return $m[1]} }
 if($rel -like 'Claude/skills/*'){return '횡단'}
 return '미측정(귀속 규칙 밖)'
}
function Kind($rel){
 $n=[IO.Path]::GetFileName($rel)
 if($rel -like 'Claude/results/handoffs/v1027-*'){return '통제(본 arc)'}
 if($rel -like 'Claude/results/handoffs/*'){ if($n -match '\.json$'){return '시드(판독·json)'}; return '시드(판독)'}
 if($n -cmatch '^HANDOVER'){return '인계'}
 if($n -cmatch '^INDEX'){return 'INDEX'}
 if($rel -match '^Claude/plans/' -or $n -cmatch '^PLAN_' -or $rel -match '/plans/'){ if($n -cmatch '(^|-)master(-plan|\.md)|MASTER'){return '마스터플랜'}; return '세부 계획서' }
 if($n -cmatch 'REFERENCE_LEDGER'){return '서지 원장'}
 if($n -cmatch 'REFLEDGER_DRAFT'){return '서지 원장(초안)'}
 if($n -cmatch 'LEDGER|STEP_LOG|CHANGE_LOG'){return 'ledger'}
 if($n -cmatch 'RESULT'){return 'Result'}
 if($n -cmatch 'MERGE_READINESS'){return '감사(머지 판정)'}
 if($n -cmatch 'CLOSING'){return '클로징'}
 if($n -cmatch 'AUDIT|REVIEW|TRIAGE|INSPECT'){return '감사'}
 if($n -match '\.tex$'){return '원문 tex'}
 if($n -cmatch 'DATA_ADDENDUM'){return '기타(데이터 정정 addendum)'}
 if($n -cmatch 'DOC_EDIT_REPORT|T13_T14'){return 'Result(집행 보고)'}
 if($n -cmatch 'CASCADE_TODO'){return '기타(지시서)'}
 if($n -cmatch 'ARCHIVE_NOTE'){return '기타(폴더 지위)'}
 if($n -cmatch 'TOUCHUP_NOTE'){return '기타(검증 기록)'}
 if($n -match '\.py$'){return '기타(코드)'}
 if($n -match '\.log$'){return '기타(로그)'}
 if($n -match '\.json$'){return '기타(데이터)'}
 if($n -eq 'jcp_extract.txt'){return '조사(원문 추출)'}
 if($n -match '\.txt$'){return '기타(텍스트)'}
 if($n -eq 'SKILL.md'){return '기타(스킬)'}
 if($n -eq 'CLAUDE.md'){return '통제(프로젝트 지침)'}
 return '조사'
}
# ---- R1~R7 Read Coverage map ----
$COVMAP=@{}
function AddRC($p,$tag){ if($COVMAP.ContainsKey($p)){ $COVMAP[$p]=@($COVMAP[$p])+@($tag) } else { $COVMAP[$p]=@($tag) } }
$BR='Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md'; $S='Claude/docs/v1.0.25.1/_sections/'; $F='Claude/docs/Fable_점검/'
$r1=@($BR,'Claude/docs/INDEX.md',"${F}FABLE_AUDIT_01_history_v3-v1011.md","${F}FABLE_AUDIT_note_A1_v3-v5.md","${F}FABLE_AUDIT_note_A2_v5-v7.md","${F}FABLE_AUDIT_note_A3_v7-v9.md","${F}FABLE_AUDIT_note_A4_v9-v1011.md","${F}FABLE_AUDIT_note_A5_ch2-code.md",'Claude/docs/v1.0.15/CLOSING_v1.0.15.md','Claude/docs/v1.0.10/HANDOVER_v1.0.11.md','Claude/docs/v1.0.13/HANDOVER_v1.0.13.md','Claude/docs/v1.0.14/HANDOVER_v1.0.14.md','Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md','Claude/docs/v1.0.15/HANDOVER_v1.0.15.md','Claude/docs/v1.0.16/HANDOVER_v1.0.16.md','Claude/docs/v1.0.17/HANDOVER_v1.0.17.md','Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md','Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md','Claude/docs/v1.0.19/HANDOVER_v1.0.19.md','Claude/results/process/HANDOVER_2026-06-07_ch2-5-overnight.md','Claude/results/process/HANDOVER_2026-06-10_ch1-textbook-rewrite.md','Claude/results/process/HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md','Claude/results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md','Claude/plans/INDEX.md')
foreach($p in $r1){AddRC $p 'R1'}
$r2=@($BR,'Claude/docs/v1.0.20/HANDOVER_v1.0.20.md','Claude/docs/v1.0.21/HANDOVER_v1.0.21.md','Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md','Claude/docs/v1.0.23/results/HANDOVER_v23.md','Claude/docs/v1.0.25.1/results/HANDOVER_v24.md','Claude/docs/v1.0.25.1/results/HANDOVER_v25.md','Claude/docs/v1.0.25.1/results/V1025_1_TOUCHUP_NOTE.md','Claude/docs/v1.0.25.1/results/INDEX_v25.md','Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md','Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md','Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md','Claude/plans/2026-07-16-v1021-master-plan.md','Claude/plans/2026-07-17-v1022-master-plan.md','Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md','Claude/plans/2026-07-18-anodefit-MASTER-plan.md','Claude/plans/2026-07-18-v1024-completeness-validation-plan.md','Claude/plans/2026-07-22-v1024-feedback-revision-plan.md','Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md')
foreach($p in $r2){AddRC $p 'R2'}
foreach($p in @('Claude/results/comp_v26_data/README.md','Claude/results/comp_v26_data/out_skew/summary_skew.json','Claude/results/comp_v26_data/skew_log.txt','Claude/results/comp_v26_data/out_versions/build.log','Claude/docs/v1.0.26A-regsol/README.md','Claude/docs/v1.0.26B-gallery/README.md')){AddRC $p 'R2(추가)'}
$r3=@($BR,'CLAUDE.md','Claude/docs/v1.0.15/CLOSING_v1.0.15.md','Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md',"${F}FABLE_AUDIT_01_history_v3-v1011.md",'Claude/docs/v1.0.18.2/ROADMAP_future_physics.md','Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md','Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md','Claude/plans/2026-07-18-anodefit-MASTER-plan.md','Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md','Claude/docs/v1.0.25.1/results/HANDOVER_v25.md')
foreach($p in $r3){AddRC $p 'R3'}
foreach($p in @('Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex','Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex',"${S}ch1_sec02a_part0.tex","${S}common_preamble_v1024.tex","${S}ch1_appE_selfconsistent.tex","${S}ch1_sec16b_lcoomega.tex","${S}ch1v22_bib.tex",'Claude/docs/INDEX.md','Claude/docs/v1.0.21/HANDOVER_v1.0.21.md','Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md','Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md','Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md','Claude/plans/2026-07-17-v1022-master-plan.md','Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md','Claude/docs/v1.0.25.1/results/PHASE_R1_RESULT.md')){AddRC $p 'R3(grep)'}
AddRC 'Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md' 'R3(glob)'
$r4a=@('ch1_sec00_intro','ch1_sec01_n0n1','ch1_sec02a_part0','ch1_sec02b_part0','ch1_sec03_center','ch1_sec04_hys','ch1_sec05_width','ch1_sec05b_gr2L','ch1_sec06_eqpeak','ch1_sec07_broadening','ch1_sec08_lag','ch1_sec09_tail','ch1_sec10_sum','ch2_sec00_intro','ch2_sec01_partition','ch2_sec02_config','ch2_sec03_vibel','ch2_sec04_einstein','ch2_sec05_mixing','ch2_sec06_limits','ch2_sec07_revheat','ch2_sec08_synthesis','ch2_sec09_method','ch2_sec10_closing','ch1_sec18_inputs','ch1_appA_signcheck','ch1_appB_codemap','ch1_appE_selfconsistent','ch1v22_bib')
AddRC $BR 'R4a'; foreach($n in $r4a){AddRC "$S$n.tex" 'R4a'}
AddRC 'Claude/docs/v1.0.25/_sections/ch1_sec05_width.tex' 'R4a(diff)'; AddRC 'Claude/docs/v1.0.25/_sections/ch1_sec06_eqpeak.tex' 'R4a(diff)'
AddRC "${S}ch1_preamble.tex" 'R4a(grep)'; AddRC "${S}ch2_preamble.tex" 'R4a(grep)'
$r4b=@('ch1_sec11_lcointro','ch1_sec12_lcocenter','ch1_sec13_lcohys','ch1_sec14_lcodecomp','ch1_sec15_lcoelec','ch1_sec16_lcopeak','ch1_sec16b_lcoomega','ch1_sec17_msmr','ch2v22_sec00_intro','ch2v22_notation','ch2v22_bib','ch3v22_sec00_intro','ch3v22_notation','ch3v22_sec01_map','ch3v22_sec02_cases','ch3v22_sec02b_sifr','ch3v22_sec03_blend','ch3v22_sec04_mech','ch3v22_sec05_code','ch3v22_bib','ch1_appD_si','ch2_appA_traps','ch2_appB_codemap')
AddRC $BR 'R4b'; foreach($n in $r4b){AddRC "$S$n.tex" 'R4b'}
AddRC 'Claude/docs/v1.0.25/_sections/ch3v22_sec02b_sifr.tex' 'R4b'; AddRC 'Claude/docs/v1.0.25.1/appendix_phase_separation.tex' 'R4b'
foreach($p in @('Claude/docs/v1.0.25.1/ch1_graphite_v1.0.24.tex','Claude/docs/v1.0.25.1/ch2_lco_v1.0.24.tex','Claude/docs/v1.0.25.1/ch3_si_v1.0.24.tex',"${S}common_preamble_v1024.tex","${S}ch2_sec03_vibel.tex","${S}ch1_sec04_hys.tex","${S}ch1_sec05b_gr2L.tex","${S}ch1_sec06_eqpeak.tex",'Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md','Claude/docs/v1.0.25.1/results/INDEX_v25.md','Claude/docs/v1.0.25.1/results/V1025_DOC_EDIT_REPORT.md','Claude/docs/v1.0.25.1/results/V1025_T13_T14_REPORT.md')){AddRC $p 'R4b(부분)'}
$r5=@($BR,'Claude/docs/v1.0.18.2/ROADMAP_future_physics.md','Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md','Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md','Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md')
foreach($p in $r5){AddRC $p 'R5'}; foreach($n in @('ch1_sec02a_part0','ch1_sec02b_part0','ch1_sec03_center','ch1_sec04_hys','ch1_sec05_width','ch1_sec05b_gr2L','ch1_sec06_eqpeak','ch1_sec07_broadening','ch2_sec01_partition','ch2_sec02_config','ch2_sec05_mixing','ch2_sec07_revheat')){AddRC "$S$n.tex" 'R5'}
AddRC 'Claude/docs/v1.0.25.1/appendix_phase_separation.tex' 'R5(보조)'; foreach($n in @('ch2_sec03_vibel','ch2_sec04_einstein','ch2_sec06_limits','ch2_sec08_synthesis','ch1_sec16b_lcoomega','ch1v22_bib','ch2v22_bib','ch3v22_bib')){AddRC "$S$n.tex" 'R5(보조)'}; AddRC 'Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md' 'R5(보조)'
AddRC "${S}ch1_sec13_lcohys.tex" 'R5(부분)'; AddRC "${S}ch1_sec10_sum.tex" 'R5(grep)'
$r6=@($BR,'Claude/docs/v1.0.18.2/ROADMAP_future_physics.md','Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md','Claude/docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md','Claude/docs/v1.0.22/results/comp_v23/SURV3_convex_inverse.md','Claude/docs/v1.0.22/results/comp_v23/SURV4_bifurcation_stochastic.md',"${F}FABLE_AUDIT_01_history_v3-v1011.md",'Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md','Claude/docs/v1.0.25.1/appendix_phase_separation.tex')
foreach($p in $r6){AddRC $p 'R6'}; foreach($n in @('ch1_appE_selfconsistent','ch1_sec01_n0n1','ch1_sec04_hys','ch1_sec05_width','ch1_sec08_lag','ch1_sec09_tail','ch1_sec13_lcohys','ch3v22_sec04_mech')){AddRC "$S$n.tex" 'R6'}
AddRC "${S}ch1_sec00_intro.tex" 'R6(보강)'; AddRC "${S}ch2_sec07_revheat.tex" 'R6(보강)'; AddRC "${S}ch2_sec05_mixing.tex" 'R6(부분)'; foreach($n in @('ch1v22_bib','ch2v22_bib','ch3v22_bib')){AddRC "$S$n.tex" 'R6(grep)'}
$r7=@($BR,"${S}ch1v22_bib.tex","${S}ch2v22_bib.tex","${S}ch3v22_bib.tex",'Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md','Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md','Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md','Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md','Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md','Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md','Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md')
foreach($p in $r7){AddRC $p 'R7'}; AddRC 'Claude/docs/v1.0.25.1/appendix_phase_separation.tex' 'R7(부분)'
# ---- hash groups ----
$hg=@{}; foreach($g in ($rows | Group-Object hash | Where-Object {$_.Count -gt 1})){ $hg[$g.Name]=@($g.Group) }
function VerKey($rel){ if($rel -match 'v1\.0\.(\d+)(?:\.(\d))?/'){ $a=[int]$Matches[1]*10; if($Matches[2]){$a+=[int]$Matches[2]}; return $a }; return 9999 }
function Canon($m){ $s=@($m | Sort-Object @{e={VerKey $_.rel}},@{e={$_.rel}}); return $s[0] }
function DupNote($r){ if(-not $hg.ContainsKey($r.hash)){return ''}; $m=$hg[$r.hash]; $c=Canon $m; if($c.rel -eq $r.rel){ $o=@($m | Where-Object {$_.rel -ne $r.rel} | ForEach-Object {$_.rel}) -join ' · '; return "고유본(사본 $($m.Count-1): $o)" } else { return "사본(고유본 = $($c.rel))" } }
# ---- master \input parse ----
$inputMap=@{}; $inputOrder=[ordered]@{}
foreach($m in @('ch1_graphite_v1.0.24.tex','ch2_lco_v1.0.24.tex','ch3_si_v1.0.24.tex')){ $tag=$m.Substring(0,3); $ml=Get-Content (Join-Path $root "Claude\docs\v1.0.25.1\$m"); $ord=@(); for($k=0;$k -lt $ml.Count;$k++){ $l=$ml[$k]; if($l -match '^\s*%'){continue}; if($l -match '\\input\{_sections/([^}]+)\}'){ $nm=$Matches[1]; $ord+="L$($k+1) $nm"; if(-not $inputMap.ContainsKey($nm)){$inputMap[$nm]=@()}; $inputMap[$nm]+="$tag L$($k+1)" } }; $inputOrder[$m]=$ord }
function Build($r){ $leaf=[IO.Path]::GetFileName($r.rel); if($leaf -match '^ch[123]_.*_v1\.0\.24\.tex$'){return '마스터'}; if($leaf -eq 'appendix_phase_separation.tex'){return '미포함·독립(\documentclass L13)'}; $nm=$leaf -replace '\.tex$',''; if($inputMap.ContainsKey($nm)){ return '포함(' + ($inputMap[$nm] -join ', ') + ')' }; return '미포함·orphan' }
# ---- group assignment ----
$assigned=@{}; $groups=[ordered]@{}
function Sel($id,$regex){ $sel=@($rows | Where-Object { $_.rel -match $regex -and -not $assigned.ContainsKey($_.rel) } | Sort-Object rel); foreach($r in $sel){ $assigned[$r.rel]=$id }; $groups[$id]=$sel }
Sel 'vi'    '^Claude/docs/INDEX\.md$|^Claude/plans/INDEX\.md$|^Claude/docs/v[^/]+/results/INDEX_v[^/]*\.md$'
Sel 'xv'    '^Claude/results/handoffs/'
Sel 'i'     '^Claude/plans/[^/]+\.md$'
Sel 'ii'    '^Claude/docs/.+/PLAN_[^/]*\.md$|^Claude/docs/v1\.0\.20/plans/2026-07-16-v1020-master-plan\.md$'
Sel 'iii'   '/HANDOVER[^/]*\.md$'
Sel 'iv'    '^Claude/docs/Fable_점검/[^/]+\.md$'
Sel 'v'     'CLOSING_v1\.0\.15\.md$'
Sel 'xii'   'V102[0-3]_REFERENCE_LEDGER\.md$'
Sel 'x'     'PHASE_DIAG_REFS67_DOSSIER\.md$|^Claude/jcp_extract\.txt$'
Sel 'xi'    '^Claude/docs/v1\.0\.26[AB][^/]*/README\.md$|^Claude/results/comp_v26_data/(README\.md|out_versions/build\.log|[^/]+\.py|out_skew/summary_skew\.json|skew_log\.txt)$'
Sel 'xvii'  '^Claude/old/_archive/graphite_ica_ch1_(Fable_v2|Fable_v3|Opus_v4|Opus_v5|Opus_v6)\.tex$'
Sel 'xvi'   '^Claude/docs/v1\.0\.25\.1/([^/]+\.tex|_sections/[^/]+\.tex)$'
Sel 'xviii' '^Claude/docs/v1\.0\.25/([^/]+\.tex|_sections/[^/]+\.tex)$'
Sel 'vii'   '^Claude/results/.*LEDGER[^/]*\.md$|^Claude/docs/v[^/]+/results/[^/]*LEDGER[^/]*\.md$|^Claude/old/.*LEDGER[^/]*\.md$|^Claude/docs/v1\.0\.20/results/STEP_LOG_P\d\.md$'
Sel 'viii'  '^Claude/(docs|results|old)/.*((MERGE_READINESS|CHANGE_LOG|AUDIT_LINEAGE|DATA_ADDENDUM|DOC_EDIT_REPORT|T13_T14|CASCADE_TODO|ARCHIVE_NOTE|TOUCHUP_NOTE)[^/]*\.md|_RESULT[^/]*\.md|/RESULT_P\d[^/]*\.md)$'
Sel 'ix'    '^Claude/results/comp_v24/([^/]+\.md|lit_raw/[^/]+\.md|sintef_data/SOURCES\.md)$|^Claude/results/comp_v26_data/[^/]+\.md$|^Claude/docs/v1\.0\.22/results/comp_(v23|SM2|FR)/|ROADMAP_future_physics\.md$|^Claude/docs/v1\.0\.20/results/(FIGS_PICK_JUDGMENT|DIRECTION_[^/]+|V1020_STYLE_RUBRIC|CODE_IMPL_REPORT|INTERCHAPTER_REPORT|V1020_KICKOFF_SURVEY_[^/]+|V1020_P1_CITATION_BASELINE)\.md$|^Claude/docs/v1\.0\.20/results/comp_P7_review/TRIAGE_P7\.md$|V1013_TERMS_POLICY\.md$|V1014_TONE_AUDIT\.md$|^Claude/results/process/V1010_INSPECT_draft_C3\.md$'
Sel 'xiii'  'REFLECT_SEED_TABLE\.md$'
Sel 'xix'   '^CLAUDE\.md$'
# ---- emit ----
$OUTL=New-Object System.Collections.Generic.List[string]
function Add($s){ $OUTL.Add($s) | Out-Null }
function Emit($id,$title,$def,$expect,$extra,$withBuild,$rowsOverride){
  $g=$groups[$id]; $n=$g.Count; $sum=($g | Measure-Object lines -Sum).Sum
  Add ''; Add "### ($id) $title"; Add ''; Add "- 정의: $def"; Add "- 기대치(출처): $expect"; Add "- 실측: **$n 파일 · $sum 줄**(TSV)"; Add ''
  $list = if($rowsOverride){$rowsOverride}else{$g}
  if($withBuild){ Add '| # | path | 줄수 | 빌드 포함/미포함 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |'; Add '|---|---|---|---|---|---|---|---|' } else { Add '| # | path | 줄수 | 버전 귀속 | 문서 종류 | 판독 정독(R#) | 비고 |'; Add '|---|---|---|---|---|---|---|' }
  $i=0
  foreach($r in $list){ $i++; $rc= if($COVMAP.ContainsKey($r.rel)){ @($COVMAP[$r.rel] | Select-Object -Unique) -join '·' } else {'—'}
    $notes=@(); if($extra -and $extra.ContainsKey($r.rel)){$notes+=$extra[$r.rel]}; $d=DupNote $r; if($d){$notes+=$d}
    $note=($notes -join ' ; '); if(-not $note){$note='—'}
    if($withBuild){ Add "| $i | ``$($r.rel)`` | $($r.lines) | $(Build $r) | $(Ver $r.rel) | $(Kind $r.rel) | $rc | $note |" } else { Add "| $i | ``$($r.rel)`` | $($r.lines) | $(Ver $r.rel) | $(Kind $r.rel) | $rc | $note |" }
  }
}
$hdr=@'
# V1027_HISTORY_INVENTORY — v1.0.27 작업 챕터 1 · Phase 1.1 · Step 1 인벤토리(OUT-INV)

> 작성 = 작업 sub(Fable 5.1), 2026-09-03. 통제 문서 = `Claude/plans/2026-09-02-v2-master-plan.md`(v5.2) Phase 1.1 Step 1(L303–316) · 지시 = `Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md`. 실측 원본 = `Claude/results/handoffs/v1027-phase-1.1-inventory/iter_1/inventory_raw.tsv`(2,651행 · 절대경로·줄수·SHA256·바이트) · 작업 기록 = 같은 폴더 `work_log.md`. 검수·확정·commit 은 master 소관(본 문건은 확정 전 산출이며 계획서·기존 문건은 무변경).

## 0. 머리

- **목적**: 작업 챕터 1(이력 통합)의 정독 대상 전건을 실물(path·줄수·hash)로 고정한다 — Step 2 정독 배정표의 모집단. 마스터 플랜 Phase 1.1 Step 1 (i)~(xvi) + brief §4 (xvii)·(xviii) + 부속 (xix) 루트 `CLAUDE.md`(brief §3.4).
- **실측 일시**: 2026-09-03 09:34:39 +09:00 (PowerShell 7 · 작업 디렉터리 `D:\Projects\Project_Anode_Fit\Claude` · `Codex/` 0회 접근 · git 명령 0회).
- **실측 명령**(brief §3.1 그대로 · 재현 가능 · 읽기 전용):

```powershell
$env:PYTHONIOENCODING='utf-8'
$root = 'D:\Projects\Project_Anode_Fit\Claude'
$out  = 'D:\Projects\Project_Anode_Fit\Claude\results\handoffs\v1027-phase-1.1-inventory\iter_1\inventory_raw.tsv'
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
$files = Get-ChildItem -Path $root -Recurse -File -Include *.md,*.tex,*.txt,*.log,*.json,*.py
$files += Get-Item 'D:\Projects\Project_Anode_Fit\CLAUDE.md'
$files | ForEach-Object {
  $h = (Get-FileHash -Algorithm SHA256 -Path $_.FullName).Hash
  "$($_.FullName)`t$((Get-Content -Path $_.FullName).Count)`t$h`t$($_.Length)"
} | Out-File -FilePath $out -Encoding utf8
(Get-Content $out).Count      # → 2651
```

- **모집단 정의**: 파일 단위 · 확장자 `.md .tex .txt .log .json .py` · `Claude/**` 재귀 + 루트 `CLAUDE.md` 1본 = 2,651행. 경로 표기는 `Claude/` 상대(루트 파일만 `CLAUDE.md`). png·pdf·html·npz·aux·csv 등 확장자 밖 파일은 모집단 밖(§5·§8 에 존재·바이트만). 본 Step 산출 3본(OUT-INV·TSV·work_log)은 TSV 생성 뒤 작성되어 TSV 에 없다.
- **줄수 정의**: `(Get-Content -Path).Count` = 개행 분리 행 수(마지막 개행 뒤 빈 문자열은 계수하지 않음). Read 도구 행 번호(R1~R7·brief·마스터 플랜이 적은 수치)는 파일이 개행으로 끝나면 마지막 빈 행을 1행 더 표시하므로 **TSV 값 = 그 표기 − 1** 인 경우가 대부분이다(확정 근거: `CLAUDE.md` 88 ↔ R3 89 · `docs/INDEX.md` 196 ↔ 197 · `INDEX_v25.md` 138 ↔ 139 — 세 파일 모두 trailing CRLF 개행 실측 True, work_log §2). 본 문건의 모든 줄수는 TSV 값이며 타 출처 수치는 §3 에서 병기·차이 기록.
- **4-tier 규약**: 확정(path:line 첨부) / 근거 미발견 / 추정 / 미검증. `[sub 판단]` = 본 작업 sub 의 판단(사용자·master 결정 아님).
- **열 어휘**: 문서 종류 ∈ {마스터플랜 / 세부 계획서 / 인계 / 감사 / 클로징 / INDEX / ledger / Result / 조사 / 서지 원장 / 원문 tex / 시드(판독) / 통제(본 arc) / 기타} — 어휘 밖 세부는 괄호. **매핑 규칙**(파일명 패턴 → 종류, `[sub 판단]`): `HANDOVER*`→인계 · `INDEX*`→INDEX · `*REFERENCE_LEDGER*`→서지 원장(`REFLEDGER_DRAFT`→서지 원장(초안)) · `*LEDGER*`/`STEP_LOG_*`/`*CHANGE_LOG*`→ledger · `*RESULT*`→Result · `MERGE_READINESS*`→감사(머지 판정) · `*AUDIT*`/`*REVIEW*`/`*TRIAGE*`/`*INSPECT*`→감사 · `CLOSING*`→클로징 · `plans/`·`PLAN_*`→마스터플랜(파일명에 `master`/`MASTER`)·세부 계획서 · `.tex`→원문 tex · `results/handoffs/`→시드(판독)·통제(본 arc) · `DATA_ADDENDUM`→기타(데이터 정정 addendum) · `DOC_EDIT_REPORT`/`T13_T14`→Result(집행 보고) · `CASCADE_TODO`→기타(지시서) · `ARCHIVE_NOTE`→기타(폴더 지위) · `TOUCHUP_NOTE`→기타(검증 기록) · `.py`/`.log`/`.json`→기타(코드/로그/데이터) · 그 밖의 `.md`→조사.
- **버전 귀속 규칙**(`[sub 판단]`): `docs/v1.0.NN(.M)/`→v1.0.NN(.M) · `docs/v1.0.26A/B`→v1.0.26 · `Claude/old/**`→구트랙 RB(단 `old/_archive/graphite_ica_ch1_{Fable,Opus}_vN.tex` 5본 = Fable v2~v10 세부 vN) · `results/comp_v24/`→v1.0.24 · `results/comp_v26_data/`→v1.0.26 · `V10NN_*`→v1.0.NN · `results/PHASE_FB*`→v1.0.24.1 · `results/PHASE_V0~V3*`→v1.0.24(추정) · `plans/` = 파일명 `v10NN` 우선, 없으면 날짜(2026-06-10 이후 = Fable v2~v10 세부 vN/날짜, 06-09 이전 = "v2 이전 — 추정") · `results/process/PHASE_*` 등 무버전 파일 = 계획서명·날짜 대응 추정(표에 "추정" 명기) · `results/handoffs/`·본 arc 계획서→본 arc · INDEX 2본·`Fable_점검`·`CLAUDE.md`·`jcp_extract.txt`→횡단. "추정" 이 붙은 귀속은 실물 정독 없이 이름·날짜로 추론한 것이며 Step 2 정독에서 확정 대상이다.
- **판독 정독(R#) 열**: R1~R7 각 「Read Coverage」 절(work_log Read Coverage 표의 행 범위)에서만 채웠다. 표기 = `R#`(배정 전문) · `R#(추가)`/`R#(보조)`/`R#(보강)`(배정 밖 전문) · `R#(부분)`(행 범위 부분) · `R#(diff)`(diff 출력만) · `R#(grep)`/`R#(glob)`(매치 행·존재 확인만) · `—`(미정독). R3 의 `_sections/*.tex` 전건 grep 과 R7 의 `_sections` 53본 + 마스터 3본 기계 스캔은 파일별 태그로 붙이지 않고 §7 말미에 일괄 기록했다.
- **중복 처리 규칙**: 한 파일은 한 군에만 계수한다. 우선순위 = (vi) > (xv) > (i) > (ii) > (iii) > (iv) > (v) > (xii) > (x) > (xi) > (xvii) > (xvi) > (xviii) > (vii) > (viii) > (ix) > (xiii) > (xix). 다른 군 정의에도 걸리는 파일은 그 군 머리에 "→ (정본 군)" 으로 참조만 적는다. hash 가 같은 사본은 각각 별개 파일로 계수하되 비고에 고유본/사본을 표시한다(§4 규칙).

## 1. 군별 인벤토리 표
'@
foreach($l in ($hdr -split "`r?`n")){Add $l}
$nI=@{
 'Claude/plans/2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md'='plans/INDEX.md:51 ★MASTER 표기(파일명 규칙상 세부 계획서)';
 'Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md'='plans/INDEX.md:18 ★MASTER 표기(파일명 규칙상 세부 계획서) · A8';
 'Claude/plans/2026-07-04-v1014-tone-rigor-appendix-figures-plan.md'='docs/INDEX.md:130 "마스터플랜 =" 표기(파일명 규칙상 세부 계획서)';
 'Claude/plans/2026-07-05-v1015-code-doc-sync-master-plan.md'='docs/INDEX.md:117 마스터플랜';
 'Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md'='docs/INDEX.md:67 "계획 =" · plans/INDEX.md:40 직전 완결';
 'Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md'='(xiii) reflect 계획서 실물 = 이 파일(R2 DQ-3)';
 'Claude/plans/2026-09-02-v2-master-plan.md'='본 arc 통제 문서(v5.2) · §2.9·brief 집계 시점엔 미존재(§2.8 L189 "신규 예정")';
 'Claude/plans/MASTER_ROADMAP_v3.md'='plans/INDEX.md:57 "마스터/로드맵(역대)"';
 'Claude/plans/MASTER_ROADMAP_CH2_v1.md'='plans/INDEX.md:57 "마스터/로드맵(역대)"';
 'Claude/plans/2026-07-18-anodefit-MASTER-plan.md'='B7';
 'Claude/plans/2026-06-08-ch1-ch2-connective-masterequation-revision-plan.md'='파일명 글로브 *master* 에는 걸리나(masterequation) 마스터플랜 아님 [sub 판단]';
 'Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md'='B6'
}
Emit 'i' '`Claude/plans/*.md` 전건' '`Claude/plans/` 직계 `.md` 전건(날짜 계획서 + `INDEX.md` + `MASTER_ROADMAP_*` + 본 arc 계획서). 하위 폴더 없음(실측). `INDEX.md` 는 (vi) 우선 규칙으로 (vi) 에 계수 — 본 표 = 92 행, (i) 정의상 전건 = 92 + INDEX 1 = 93' '93 파일·10,383줄(1g 실측 I-6:15) · brief 90/9,567 · v1 sub 91/9,503 · master 92/9,567(§2.9 L195) — 차이 열거 = §3.1' $nI $false $null
$nII=@{ 'Claude/docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md'='v1.0.20 한정 위치 규약(docs/INDEX.md:53 · plans/INDEX.md:38)' }
Emit 'ii' '`Claude/docs/**/PLAN_*.md` + v1.0.20 마스터 플랜' '`docs/**/PLAN_*.md` 전건(v1.0.20 P0~P8 9본 · v1.0.22 R1/R2/R3/R5/RA/FR 6본) + `docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md`' '15 + 1(brief §4 · §2.9 L196 · 1g I-6:15 "PLAN_* 15") — 일치' $nII $false $null
$nIII=@{
 'Claude/old/Archive_oldtrack/HANDOVER_RB_2026-05-31.md'='구트랙(별도 표시)';'Claude/old/Archive_oldtrack/HANDOVER_RB_2026-06-02.md'='구트랙(별도 표시)';'Claude/old/Archive_oldtrack/HANDOVER_RB_2026-06-02b.md'='구트랙(별도 표시)';
 'Claude/results/comp_v26_data/HANDOVER_regsol_investigation.md'='A7 · `comp_v26_data/README.md:23` "착수 시점 인계(서비스 장애로 실행 차단됐던 기록)" = stale(R2)';
 'Claude/docs/v1.0.25.1/results/HANDOVER_v25.md'='A5';'Claude/docs/v1.0.25.1/results/HANDOVER_v24.md'='A6(brief 는 v1.0.25.1 사본을 인용)';
 'Claude/docs/v1.0.10/HANDOVER_v1.0.11.md'='v1.0.10 폴더에 v1.0.11 인계가 있음(파일명·폴더 불일치 — 관찰)'
}
Emit 'iii' '`HANDOVER*.md` 전건(old/ 제외 25 + old/ 3)' '파일명 `HANDOVER*.md` 전건. old/ 3본 = 구트랙 별도 표시. hash 사본 판정 = §4(`HANDOVER_v24.md` ×4 · `HANDOVER_v25.md` ×2)' '25/1,612(old 제외) + old 3 = 28(brief §4 · §2.9 L197 · 1g) — 차이 열거 = §3.2' $nIII $false $null
$nIV=@{ 'Claude/docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md'='A9';'Claude/docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md'='note_A1';'Claude/docs/Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md'='note_A2';'Claude/docs/Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md'='note_A3';'Claude/docs/Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md'='note_A4';'Claude/docs/Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md'='note_A5';'Claude/docs/Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md'='§2.9 L198 미검독(02)';'Claude/docs/Fable_점검/FABLE_AUDIT_03_code_fitness.md'='§2.9 L198 미검독(03)' }
Emit 'iv' '`Claude/docs/Fable_점검/*.md`' 'Fable 이력 전수감사 8본(01·02·03·note A1~A5)' '8·885줄(brief §4 · 1g) — 일치(줄수 정의 무관하게 합계 일치)' $nIV $false $null
Emit 'v' '`CLOSING_v1.0.15.md`' 'v1.0.15 버전 클로징(헌법 3종)' '106줄(brief §4 · A10) → 실측 105(줄수 정의 −1)' @{'Claude/docs/v1.0.15/CLOSING_v1.0.15.md'='A10 · docs/INDEX.md:127 "다음 버전 착수 전 필독"'} $false $null
$nVI=@{ 'Claude/docs/INDEX.md'='A2 · brief 197 → 실측 196(정의 −1)';'Claude/plans/INDEX.md'='A3 · brief 65 → 실측 69: 스테일 표기(자체 L5–8)이나 v1.0.27 행 L10–13 이 추가돼 있음(I-3 정독 확정) — +4 는 실제 갱신';'Claude/docs/v1.0.25.1/results/INDEX_v25.md'='brief 139 → 실측 138(정의 −1) · I-4 전문 정독' }
Emit 'vi' 'INDEX 전건' '`docs/INDEX.md` · `plans/INDEX.md` · `docs/v*/results/INDEX_v*.md` 전건' '197·65·139(+기타) — 실측 196·69·138 + `INDEX_v1022`·`INDEX_v23`·`INDEX_v24`×4·`INDEX_v25`×2' $nVI $false $null
$nVII=@{}
foreach($r in $groups['vii']){ if($r.rel -match 'STEP_LOG_P'){$nVII[$r.rel]='추가 발견(스텝 이력 = ledger 성격 · v1.0.20 위치 규약)'} elseif($r.rel -match 'REFLEDGER_DRAFT'){$nVII[$r.rel]='추가 발견(패턴 `*LEDGER*` 매치 · 서지 원장 초안)'} elseif($r.rel -like 'Claude/old/*'){$nVII[$r.rel]='구트랙(old/ 하위 — 마스터 플랜 정의 밖 · 패턴 매치로 등재, DQ-5)'} elseif($r.rel -match 'V1024_REFLECT_EXECUTION_LEDGER'){$nVII[$r.rel]='(xiii) 대상 · 계수는 (vii)'} elseif($r.rel -match 'V1025_CHANGE_LEDGER'){$nVII[$r.rel]='(viii) 정의에도 해당 · 계수는 (vii)'} }
$nVII['Claude/results/V1024_EXECUTION_LEDGER.md']='§2.8 L179 12-col 실례'; $nVII['Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md']='§2.8 L179 12-col 실례'
Emit 'vii' 'ledger 전건' '`Claude/results/**/*LEDGER*.md` + `docs/v*/results/*LEDGER*.md` + (추가 발견) `old/**/*LEDGER*.md` 구트랙 · `docs/v1.0.20/results/STEP_LOG_P*.md`. 서지 원장 4본은 (xii) 에 계수(→ (xii))' '30(results 2·process 26·research 2) + docs 측 미실측(brief §4 · §2.9 L201) — 실측: results 30 ✓(2·26·2, 1,075줄) + docs 측 12(REFERENCE 4 제외) + STEP_LOG 8 + old/ 31' $nVII $false $null
$nVIII=@{}
foreach($r in $groups['viii']){ $lf=[IO.Path]::GetFileName($r.rel); if($r.rel -like 'Claude/old/*'){$nVIII[$r.rel]='구트랙(old/ 하위 — 패턴 매치로 등재, DQ-5)'} elseif($lf -match '^RESULT_P\d'){$nVIII[$r.rel]='추가 발견(`PHASE_` 접두 없는 Result · v1.0.20 위치 규약)'} elseif($lf -match 'TOUCHUP_NOTE'){$nVIII[$r.rel]='추가 발견 — A4 · docs/INDEX.md:12 "현행 권위 기록"'} elseif($lf -match '_RESULT' -and $lf -notmatch '^PHASE_'){$nVIII[$r.rel]='추가 발견(`PHASE_*_RESULT` 패턴 밖 Result)'} }
$nVIII['Claude/docs/v1.0.25.1/ARCHIVE_NOTE.md']='v1.0.25 절 S1~S6 추기본(INDEX_v25.md:93) · v1.0.25 폴더본(109)과 hash 상이'
$nVIII['Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md']='동결 아카이브 권위 기록(docs/INDEX.md:25)'
Emit 'viii' '각 버전 MERGE_READINESS·CHANGE_LOG·PHASE_*_RESULT·AUDIT_LINEAGE·DATA_ADDENDUM·DOC_EDIT_REPORT·T13_T14·CASCADE_TODO·ARCHIVE_NOTE' '파일명 패턴 매치 `.md` 전건(`docs/`·`results/`·`old/`). `*CHANGE_LEDGER*` 는 (vii) 에 계수(→ (vii)) · `INDEX_v*` → (vi) · `HANDOVER*` → (iii) · `handoffs/**/fix_change_log.md` → (xv). 추가 발견 = `RESULT_P*`·비-`PHASE_` `*_RESULT*`·`V1025_1_TOUCHUP_NOTE`' '미실측(brief §4)' $nVIII $false $null
$nIX=@{ 'Claude/results/process/V1010_INSPECT_draft_C3.md'='추가 발견 — §5 `C3_graph_check/`·`C3_pdf_render/` 지위 근거(L14–15·23)';'Claude/results/comp_v24/sintef_data/SOURCES.md'='추가 발견(comp_v24 하위 폴더)';'Claude/docs/v1.0.18.2/ROADMAP_future_physics.md'='B1';'Claude/results/comp_v24/IMPROVEMENT_DIRECTIONS.md'='B2';'Claude/results/comp_v24/LIT_ADVANCE_SYNTHESIS.md'='B3';'Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md'='B4';'Claude/docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md'='B5';'Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md'='A11';'Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md'='A12 · R2: L80 `</content>` 잔존 문자열';'Claude/results/process/V1014_TONE_AUDIT.md'='종류 = 감사(brief 는 조사 문서군에 배정 — 군은 (ix) 유지)';'Claude/results/process/V1013_TERMS_POLICY.md'='brief 명시';'Claude/results/comp_v26_data/MULTI_DATASET_REVIEW.md'='§2.9 L202 미검독' }
foreach($r in $groups['ix']){ if($r.rel -match 'comp_v24/lit_raw/'){$nIX[$r.rel]='추가 발견(comp_v24 하위 폴더)'} elseif($r.rel -match 'comp_SM2/SM2_DRAFTS/'){$nIX[$r.rel]='추가 발견(`comp_SM2/*.md` 패턴 밖 tex 초안)'} elseif($r.rel -match 'v1\.0\.20/results/(CODE_IMPL_REPORT|INTERCHAPTER_REPORT|V1020_KICKOFF_SURVEY|V1020_P1_CITATION_BASELINE)'){$nIX[$r.rel]='추가 발견(v1.0.20 results 상위 md — brief 명시 4종 밖)'} }
Emit 'ix' '조사 문서군' '`results/comp_v24/*.md`(+lit_raw·sintef_data/SOURCES) · `results/comp_v26_data/*.md`(README → (xi) · HANDOVER → (iii)) · `docs/v1.0.22/results/comp_v23/*.md` · `comp_SM2/**` · `comp_FR/**` · `docs/v1.0.18.2/ROADMAP_future_physics.md` · `docs/v1.0.20/results/`(FIGS_PICK·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC + 추가 발견 상위 md) · `V1013_TERMS_POLICY` · `V1014_TONE_AUDIT` · (추가 발견) `V1010_INSPECT_draft_C3.md`' '미실측(brief §4)' $nIX $false $null
$nX=@{ 'Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md'='brief 50 → 실측 49(정의 −1) · Assumptions 5·10';'Claude/jcp_extract.txt'='brief 724 → 실측 725(+1 — 정의와 반대 방향 · 파일 개행 구조 미조사, 미검증) · JCP PDF 존재 = `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` 2,075,558 B(열지 않음)' }
Emit 'x' 'dossier · jcp_extract(+ JCP PDF 존재)' '`old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` · `Claude/jcp_extract.txt` · JCP PDF 는 모집단 밖 — 존재·바이트만 비고에' '50줄 · 724줄(brief §4)' $nX $false $null
$nXI=@{ 'Claude/docs/v1.0.26A-regsol/README.md'='brief 199 → 198(정의 −1)';'Claude/docs/v1.0.26B-gallery/README.md'='brief 193 → 192(정의 −1)';'Claude/results/comp_v26_data/README.md'='brief 50 → 49(정의 −1) · I-7 L20–35 토픽 정독';'Claude/results/comp_v26_data/out_versions/build.log'='brief 36 = 36(일치) · R2 DQ-2 A/B 수치 원천';'Claude/results/comp_v26_data/test_skew_regsol.py'='README.md:30 폐기(실행 금지)';'Claude/results/comp_v26_data/out_skew/summary_skew.json'='추가 발견(R2 Read Coverage +2 · README.md:30 폐기분 산출 "빈 JSON")';'Claude/results/comp_v26_data/skew_log.txt'='추가 발견(R2 Read Coverage +3)';'Claude/results/comp_v26_data/regsol_kernel.py'='§2.8 L181';'Claude/results/comp_v26_data/build_two_versions.py'='README.md:20';'Claude/results/comp_v26_data/make_version_docs.py'='README.md:21';'Claude/results/comp_v26_data/analyze_sintef.py'='README.md:24 미실행(잔여 과제)' }
Emit 'xi' 'v1.0.26 실물' '`docs/v1.0.26A-regsol/README.md` · `docs/v1.0.26B-gallery/README.md` · `results/comp_v26_data/README.md` · `out_versions/build.log` + 조사 스크립트 `.py` 목록 + (추가 발견) R2 가 읽은 `out_skew/summary_skew.json`·`skew_log.txt`' '199·193·50·36(brief §4)' $nXI $false $null
$nXII=@{ 'Claude/docs/v1.0.20/results/V1020_REFERENCE_LEDGER.md'='brief 55 → 54(정의 −1)';'Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md'='brief 38 → 37(정의 −1)';'Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md'='brief 33 → 32(정의 −1)';'Claude/docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md'='brief 33 → 32(정의 −1) · V1022 와 hash 동일(R7 md5 대조와 일치)' }
Emit 'xii' '서지 원장 4본' '`docs/v1.0.2N/results/V102N_REFERENCE_LEDGER.md` (N=0..3) · hash 사본 판정 §4' '55·38·33·33(brief §4)' $nXII $false $null
Emit 'xiii' 'reflect 계획서 · V1024_REFLECT_EXECUTION_LEDGER(실물 경로 확인)' '2026-07-19 reflect 계획서(→ (i) 계수) · `V1024_REFLECT_EXECUTION_LEDGER.md` ×4(→ (vii) 계수) · (추가 발견·본 군 계수) `REFLECT_SEED_TABLE.md` ×4' '미실측(brief §4)' @{'Claude/docs/v1.0.24/results/REFLECT_SEED_TABLE.md'='추가 발견 · INDEX_v25.md:83 사양 원천(승계) — addendum A4·A7 이 supersede';'Claude/docs/v1.0.24.1/results/REFLECT_SEED_TABLE.md'='추가 발견';'Claude/docs/v1.0.25/results/REFLECT_SEED_TABLE.md'='추가 발견';'Claude/docs/v1.0.25.1/results/REFLECT_SEED_TABLE.md'='추가 발견'} $false $null
Add ''; Add '실물 경로 확인(계수는 각 정본 군):'; Add ''; Add '| 항목 | 실물 path | 줄수 | 계수 군 |'; Add '|---|---|---|---|'
Add "| reflect 계획서 | ``Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md`` | $($byRel['Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md'].lines) | (i) |"
foreach($v in @('v1.0.24','v1.0.24.1','v1.0.25','v1.0.25.1')){ $k="Claude/docs/$v/results/V1024_REFLECT_EXECUTION_LEDGER.md"; Add "| V1024_REFLECT_EXECUTION_LEDGER | ``$k`` | $($byRel[$k].lines) | (vii) — hash $($byRel[$k].hash.Substring(0,12)) (4본 동일) |" }
Add ''; Add '### (xiv) git untracked 21건 — §5 참조(모집단 밖 png·html 포함이라 본 표에는 줄수 열 없음)'
$nXV=@{ 'Claude/results/handoffs/v1027-phase-1.1-inventory/brief.md'='추가 발견 — 본 Step 지시서(brief 정의 (xv) 밖 · 통제(본 arc))';'Claude/results/handoffs/2026-09-02-v2-master-plan/wf/go_1g_check_2026-09-03.txt'='I-6 전문 정독 · 1g 실측 대조 원본';'Claude/results/handoffs/2026-09-02-v2-master-plan/wf/fix_change_log.md'='(viii) `CHANGE_LOG` 패턴에도 매치 — 계수는 (xv)';'Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R7_reference_master_map.json'='R7 json(3,833줄)' }
foreach($r in $groups['xv']){ if($r.rel -match '/wf/R\d[ab]?_' -and $r.rel -match '\.md$'){ $nXV[$r.rel]='시드 — 정독 대상 아님(Read Coverage 절만 토픽 정독, work_log)' } }
Emit 'xv' '판독 산출(시드 등재 — 정독 대상 아님)' '`Claude/results/handoffs/2026-09-02-v2-master-plan/**` 전건(brief·audit_checklist·iter_1/*·wf/*) + (추가 발견) 본 Step brief' '시드 등재(brief §4)' $nXV $false $null
$nXVI=@{ "${S}ch1_preamble.tex"='brief §3.2 기대 "지원 4본 = \input 되는 빌드 포함" 과 상이 — 헤더 L2–3 "graphite_ica_ch1_v1.0.21.tex 가 \input" (v1.0.21 잔재) · 현행 마스터 3본 어디에도 \input 0(Grep `\input{` v1.0.25.1 전 tex — 마스터 3본 외 0건) → orphan';"${S}ch2_preamble.tex"='동상 — 헤더 L2–3 "graphite_ica_ch2_v1.0.21.tex 가 \input" · 현행 \input 0 → orphan';"${S}common_preamble_v1024.tex"='마스터 3본이 \input(ch1 L10·ch2 L8·ch3 L8) · 헤더 L2 는 "common_preamble_v1022.tex" 로 표기(파일명 불일치 — 관찰, DQ-12) · L3 "= 구 ch1_preamble ∪ ch2_preamble"';"${S}ch1v22_partT_divider.tex"='지원(Part T 구획) · ch1 L39 \input';"${S}ch1_appD_si.tex"='orphan(기대와 일치 · R4b DQ-3)';'Claude/docs/v1.0.25.1/appendix_phase_separation.tex'='독립 부록 — 자체 `\documentclass` L13·`\begin{document}` L41 · `_sections` 밖';"${S}ch1_sec00_intro.tex"='A13';"${S}ch1_appE_selfconsistent.tex"='A14';"${S}ch2_sec05_mixing.tex"='[C-92] warnbox L230–238(§2.0 L66)';"${S}ch3v22_sec04_mech.tex"='GS-1 L89–99(§2.0 L67)';"${S}ch3v22_sec03_blend.tex"='GS-2 L251–266(§2.0 L67)' }
Emit 'xvi' '현행 tex 60(v1.0.25.1) — 빌드 포함/미포함 열' '`docs/v1.0.25.1/*.tex`(마스터 3 + 독립 부록 1) + `_sections/*.tex` 56. 빌드 열 = 마스터 3본의 비주석 `\input{_sections/…}` 실측(§6). `results/comp_R1/**/*.tex` 30본은 경쟁 초안이라 현행 tex 밖(§8)' '60·9,214줄(brief §4 · 1g A2) — 일치. 빌드 기대 = 포함 58 / 미포함 2(orphan `ch1_appD_si` + 독립 부록) → **실측 = 마스터 3 + 포함 53 + 미포함 4(독립 1 + orphan 3)** — `ch1_preamble`·`ch2_preamble` 가 기대와 달리 \input 되지 않음(§6·§8.1)' $nXVI $true $null
$nXVII=@{}; foreach($r in $groups['xvii']){ $nXVII[$r.rel]="Assumptions 23 바이트 일치($($r.bytes) B) · 1.4 Step 11 정독 대상 · 본 Step 내용 미검독" }
Emit 'xvii' '유실 자산 원문 tex 5본' '`old/_archive/graphite_ica_ch1_{Fable_v2,Fable_v3,Opus_v4,Opus_v5,Opus_v6}.tex`' '5본 존재(Assumptions 23 · 1g A23 5/5)' $nXVII $false $null
$diffRows=@(); $a25=@{}; foreach($r in $groups['xviii']){ $a25[($r.rel -replace '^Claude/docs/v1\.0\.25/','')]=$r }; $a251=@{}; foreach($r in $groups['xvi']){ $a251[($r.rel -replace '^Claude/docs/v1\.0\.25\.1/','')]=$r }
$nXVIII=@{}; foreach($k in ($a25.Keys | Sort-Object)){ if($a251.ContainsKey($k) -and $a25[$k].hash -ne $a251[$k].hash){ $diffRows+=$a25[$k]; $nXVIII[$a25[$k].rel]="v1.0.25.1 대비 hash 상이 · 줄수 $($a25[$k].lines) → $($a251[$k].lines)" } }
Emit 'xviii' 'v1.0.25 base tex 60 — 합계 + v1.0.25.1 대비 hash 상이 파일만 행 등재' '`docs/v1.0.25/*.tex` + `_sections/*.tex`(60본 전건 계수 · 행은 hash 상이 파일만)' '60(brief §4) · 1g A3 "diff 파일 10 = sections 3 + masters 3 + ARCHIVE_NOTE + PDF 3" → tex 만 대조 = 6(일치: sections 3 + masters 3) · 비-tex 대조(md/py/json): `ARCHIVE_NOTE.md` 109→118 상이 · `V1025_1_TOUCHUP_NOTE.md` 는 v1.0.25.1 에만 존재' $nXVIII $false $diffRows
$s25=($groups['xviii'] | Measure-Object lines -Sum).Sum
Add ''; Add "v1.0.25 tex 60 합계 = $s25 줄(v1.0.25.1 9,214 대비 −$(9214-$s25)) · 60본 중 hash 동일 $((60-$diffRows.Count)) · 상이 $($diffRows.Count)."
Emit 'xix' '루트 `CLAUDE.md`(brief §3.4 부속)' '`D:\Projects\Project_Anode_Fit\CLAUDE.md` 1본 — 별도 경로로 측정(Codex/ 무접근)' 'brief·§2.0 A1 90 · R3 실측 89 → **정본 88**(TSV 정의; §3.4)' @{'CLAUDE.md'='A1 · 7,380 B · trailing CRLF 개행 True(R3 89 = Read 표기 +1)'} $false $null
# ---- §2 totals ----
Add ''; Add '## 2. 합계'; Add ''; Add '| 군 | 파일 수(계수) | 줄수 | 비고 |'; Add '|---|---|---|---|'
$tot=0; $totL=0
foreach($id in @('i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xv','xvi','xvii','xviii','xix')){ $g=$groups[$id]; $c=$g.Count; $s=($g | Measure-Object lines -Sum).Sum; $tot+=$c; $totL+=$s; $nb=''; if($id -eq 'i'){$nb='INDEX.md 는 (vi) 계수 → (i) 정의상 93'}; if($id -eq 'xiii'){$nb='계획서·ledger 는 (i)/(vii) 계수'}; if($id -eq 'xviii'){$nb='행은 hash 상이 6본만'}; Add "| ($id) | $c | $s | $nb |" }
Add "| (xiv) | 21(png 5 · 폴더 3 · Codex 13) | — | 모집단 밖(§5) |"
Add "| **합계(TSV 계수)** | **$tot** | **$totL** | TSV 2,651행 중 등재 $tot · 미등재 $($rows.Count-$tot)(§8.3) |"
Add ''; Add '중복 처리 규칙 적용 결과: 한 파일이 두 군 정의에 걸린 경우 = `plans/INDEX.md`((i)∩(vi) → (vi)) · `HANDOVER_regsol_investigation.md`((iii)∩(ix) → (iii)) · `comp_v26_data/README.md`((ix)∩(xi) → (xi)) · `V102N_REFERENCE_LEDGER` 4본((vii)∩(xii) → (xii)) · `V1025_CHANGE_LEDGER` ×2((vii)∩(viii) → (vii)) · `V1024_REFLECT_EXECUTION_LEDGER` ×4((vii)∩(xiii) → (vii)) · reflect 계획서((i)∩(xiii) → (i)) · `INDEX_v*`((vi)∩(viii) → (vi)) · `fix_change_log.md`((viii)∩(xv) → (xv)) · `V1014_TONE_AUDIT`(종류 감사 · 군 (ix)).'
# ---- §3 prose ----
$sec3=@'

## 3. brief §3-C · 마스터 플랜 §2.9 수치와의 차이(실측 정본 확정)

### 3.1 plans — 실측 정본 = **93 파일 · 10,384 줄**(TSV · `Claude/plans/*.md` 직계 전건 · 하위 폴더 없음)

정본 구성(실측): 날짜 계획서 90(2026-05-29 ~ 2026-09-02) + `INDEX.md` 1(69줄) + `MASTER_ROADMAP_*` 2(320·131줄) = 93.

| 출처 | 수치 | 실측과의 차이 | 차이를 만든 파일명·줄수 |
|---|---|---|---|
| 1g 실측(I-6 `go_1g_check_2026-09-03.txt`:15, 09:24) | 93 / 10,383 | 파일 0 · 줄 +1 | 파일 미특정 — 1g 는 파일별 줄수를 남기지 않았다. [추정] 1g(09:24)~본 실측(09:34) 사이 `2026-09-02-v2-master-plan.md`(812줄 · v5.2 표기) 갱신. 미검증(DQ-9) |
| master 재실측(§2.9 L195 · Assumptions 12 L608) | 92 / 9,567 | 파일 +1 · 줄 +817 | [확정] `2026-09-02-v2-master-plan.md` 812줄 — 집계 시점 미존재(§2.8 L189 "신규 예정 … master 최종 저장") · [확정] `plans/INDEX.md` 65 → 69 (+4: v1.0.27 행 L10–13 추가, I-3 정독) → 9,567 + 812 + 4 = 10,383 = 1g 값 · 잔여 +1 = 위 행과 동일(미특정) |
| brief §3-C(§2.9 L195 인용) | 90 / 9,567 | 파일 +3 · 줄 +817 | 줄수가 master 와 동일하므로 [추정] 건수만 `MASTER_ROADMAP_*` 2본(320·131) 또는 `INDEX.md` 계수 기준 차이 · 근거 미발견 |
| v1 sub(§2.9 L195) | 91 / 9,503 | 파일 +2 · 줄 +881 | [추정] 91 = 날짜 계획서 89 + `MASTER_ROADMAP_*` 2(`INDEX.md` 제외) · 9,503 ≈ 9,567 − 65(INDEX) + 1(정의 차) — 근거 미발견 |

### 3.2 HANDOVER — 실측 정본 = **old/ 제외 25 파일 · 1,612 줄** · old/ 포함 **28 · 1,915**

- 1g(I-6:15) 25/1,612 · master §2.9 L197 25/1,612 · Assumptions 12 L608 25/1,612 — **일치**(확정).
- brief §3-C "28본(old/ 제외)·1,612줄" → **오기 확정**: 28 은 old/ 3본 포함 건수이고 1,612 는 old/ 제외 줄수다(건수·줄수의 기준 불일치). old/ 3본 = `HANDOVER_RB_2026-05-31.md` 90 · `HANDOVER_RB_2026-06-02.md` 129 · `HANDOVER_RB_2026-06-02b.md` 84 = 303줄 → 1,612 + 303 = 1,915.
- 25 의 구성: `docs/` 20(v1.0.10~v1.0.25.1 — `HANDOVER_v24.md` ×4 · `HANDOVER_v25.md` ×2 포함) + `results/comp_v26_data/` 1 + `results/process/` 4. hash 고유본 = 25 − 3(v24 사본) − 1(v25 사본) = 21본(§4).

### 3.3 PLAN_* — 실측 정본 = **15 파일 · 645 줄** + `2026-07-16-v1020-master-plan.md` 207줄

- brief "15 + 1" · §2.9 L196 "15 + 1" · 1g A11/12 "PLAN_* 15" — **일치**(확정). 줄수는 brief 미실측 → 본 실측이 첫 정본.

### 3.4 `CLAUDE.md` — 실측 정본 = **88 줄**(7,380 B)

| 출처 | 수치 | 판정 |
|---|---|---|
| TSV(본 실측, `(Get-Content).Count`) | 88 | **정본**(brief §3.1 줄수 정의) |
| R3 Read Coverage(`R3_binding_decisions_and_lost_directions.md`:368 "1–89(전건) · brief 표기 90줄, 실측 89행") | 89 | 같은 파일의 Read 도구 표기(+1) — 파일 끝 CRLF 개행 실측 True(확정) |
| brief §3.4 · 마스터 플랜 §2.0 L43 "90(R3 실측 89)" | 90 | 근거 미발견(작성 시점 실물이 다른 것인지 오기인지 미검증) |

### 3.5 그 밖의 brief §4 기대치 대조(줄수 정의 −1 이 아닌 것만 굵게)

| 군 | 기대 | 실측 | 판정 |
|---|---|---|---|
| (iv) Fable | 8·885 | 8·885 | 일치(1g 도 885 — 1g 가 같은 정의로 측정했다는 증거) |
| (v) CLOSING | 106 | 105 | 정의 −1 |
| (vi) INDEX | 197·65·139 | 196·**69**·138 | docs·v25 는 정의 −1 · **plans/INDEX.md +4 = 실제 갱신**(v1.0.27 행) |
| (vii) results ledger | 30(2·26·2) | 30(2·26·2)·1,075 | 일치 |
| (x) dossier·jcp | 50·724 | 49·**725** | dossier 정의 −1 · **jcp_extract +1**(방향 반대 — 미검증, 개행 구조 미조사) |
| (xi) v1.0.26 | 199·193·50·36 | 198·192·49·36 | 정의 −1(build.log 는 일치) |
| (xii) 서지 원장 | 55·38·33·33 | 54·37·32·32 | 정의 −1 |
| (xvi) 현행 tex | 60·9,214 | 60·9,214 | 일치(1g A2 동일) |
| (xviii) v1.0.25 tex | 60 · diff 10(1g A3, tex+md+pdf) | 60·9,207 · tex diff 6 | 일치(10 − ARCHIVE_NOTE 1 − PDF 3 = 6) |
| (xvii) 유실 원문 | 5본·바이트 5종 | 5본 · 183,693/205,225/218,389/153,592/156,166 B | 일치(Assumptions 23) |
| untracked | Claude 8 / Codex 13 | Claude 8 존재 확인 / Codex 13 무접근 | §5 |
'@
foreach($l in ($sec3 -split "`r?`n")){Add $l}
# ---- §4 hash groups ----
Add ''; Add '## 4. hash 중복 그룹(TSV SHA256 동일 · 전건)'; Add ''
Add '고유본 규칙(brief §3.3): 가장 이른 버전 폴더(`v1.0.NN(.M)` 최소)의 것 = 계보상 원본. 버전 폴더가 없는 구성원끼리는 경로 정렬 최상(예: `old/` < `results/`) — 같은 폴더 안 동명이물(예: `REVIEW_LEDGER_CH2_10ROUND*` 2본)은 DQ-4 로 표면화. 이 규칙을 현행 tex 60 에 적용하면 v1.0.24 사본이 고유본이 되므로 **정독 경로는 현행 `v1.0.25.1` 을 쓰되 등록부 표기는 DQ-4** 에서 확정한다. 표기 = 동일 파일명이면 "동명 파일명 @ 폴더 목록", 아니면 전체 경로.'
Add ''; Add "그룹 수 = $($hg.Count) · 관련 파일 수 = $(($hg.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum)"; Add ''
Add '| # | hash(앞 16) | n | 줄수 | 고유본 | 사본 |'; Add '|---|---|---|---|---|---|'
$gi=0
foreach($key in ($hg.Keys | Sort-Object @{e={-$hg[$_].Count}},@{e={$_}})){ $gi++; $m=$hg[$key]; $c=Canon $m; $others=@($m | Where-Object {$_.rel -ne $c.rel})
  $leafs=@($m | ForEach-Object {[IO.Path]::GetFileName($_.rel)} | Select-Object -Unique)
  $canonTxt='`' + $c.rel + '`'
  if($leafs.Count -eq 1){ $othersTxt=(@($others | ForEach-Object { ([IO.Path]::GetDirectoryName($_.rel) -replace '\\','/') })) -join ' · '; $sab='동명 `' + $leafs[0] + '` @ ' + $othersTxt } else { $sab=(@($others | ForEach-Object { '`' + $_.rel + '`' })) -join ' · ' }
  Add "| $gi | $($key.Substring(0,16)) | $($m.Count) | $($c.lines) | $canonTxt | $sab |" }
# ---- §5 untracked ----
$sec5=@'

## 5. git untracked 21건(세션 시작 스냅샷 · brief §3.5 · git 미실행 — 존재·크기·참조만 실측)

### 5.1 Claude 측 8건

| # | path | 실물(존재·바이트·mtime) | 지위 | 근거(4-tier) |
|---|---|---|---|---|
| 1 | `Claude/docs/v1.0.17/figs/graph_suite_v1017.png` | 존재 · 223,035 B · 2026-09-02 16:49 | **유효(재생성 가능 산출물)** [sub 판단] | 확정: 같은 폴더 tracked 스크립트 `Claude/docs/v1.0.17/graph_suite_v1017.py:37` `OUT = r"…\v1.0.17\figs\graph_suite_v1017.png"` · `results/process/V1017_EXECUTION_LEDGER.md:19` "v1.0.16 → v1.0.17 복제(… figs)" (간접) · `docs/INDEX.md`·`HANDOVER_v1.0.17.md` 직접 언급 = 근거 미발견 |
| 2 | `Claude/docs/v1.0.17/sample_test_v1017.png` | 존재 · 281,441 B · 2026-09-02 16:48 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.17/sample_test_v1017.py:12` "Output: sample_test_v1017.png" · `:28` OUT 경로 |
| 3 | `Claude/docs/v1.0.18.1/figs/graph_suite_v1018_1.png` | 존재 · 223,076 B · 2026-09-02 16:47 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.1/graph_suite_v1018_1.py:37` · `V1018_EXECUTION_LEDGER.md:31` "v1.0.17 → v1.0.18.1 복제(… figs)" (간접) |
| 4 | `Claude/docs/v1.0.18.1/sample_test_v1018_1.png` | 존재 · 281,771 B · 2026-09-02 16:49 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.1/sample_test_v1018_1.py:12,28` |
| 5 | `Claude/docs/v1.0.18.2/figs/graph_suite_v1018_2.png` | 존재 · 223,131 B · 2026-09-02 16:47 | 유효(재생성 가능 산출물) [sub 판단] | 확정: `Claude/docs/v1.0.18.2/graph_suite_v1018_2.py:37` |
| 6 | `Claude/results/process/C3_graph_check/` | 폴더 · 1 파일: `c3_graphite_lco_check.png`(157,313 B · 2026-07-02 01:38) | **유효(v1.0.10 문제점검 C3 실행 그래프 · 참조 문서 존재)** [sub 판단] | 확정: `Claude/results/process/V1010_INSPECT_draft_C3.md:14` "별도 임시 위치 `Claude/results/process/C3_graph_check/c3_graphite_lco_check.png`에 직접 실행 결과 생성 후 육안 판독" · `:23` 동일 경로 인용 |
| 7 | `Claude/results/process/C3_pdf_render/` | 폴더 · 50 파일: `ch1-01.png`~`ch1-35.png`(35) · `ch2-01.png`~`ch2-13.png`(13) · `ch1_contact_sheet.png`(1,832,571 B) · `ch2_contact_sheet.png`(706,435 B) · 전부 2026-07-02 01:38–01:39 | **유효(추정 상향)** — 폴더명 직접 참조 0 · 내용 대응 확정 [sub 판단] | 확정(내용 대응): `V1010_INSPECT_draft_C3.md:15` "Ch1 PDF 35쪽, Ch2 PDF 13쪽을 `pdftoppm`으로 렌더링해 contact sheet 및 핵심 페이지를 육안 판독" — 페이지 수 35/13 · contact sheet 2 · 시각(#6 과 동일 분) 일치 · 폴더명 문자열 검색(`C3_pdf_render`, `Claude/results/**` 전 파일) = 0건(근거 미발견) → 지위는 추정 |
| 8 | `Claude/results/regsol_test/` | 폴더 · 2 파일: `gr_regsol_vs_logistic.png`(244,903 B · 2026-07-27 01:07) · `regsol_view.html`(331,010 B · 2026-07-27 01:19) | **폐기** | 확정: `Claude/results/comp_v26_data/README.md:31` "`regsol_decision.html` · `../regsol_test/` — 위 폐기분 기반"(§ "⚠️ 폐기 (실행하지 말 것)" L26–31, I-7) |

관찰(판정 아님): #1~#5 의 mtime 은 전부 2026-09-02 16:47–16:49 로 같은 세션의 일괄 재생성으로 보인다(추정 · 실행 주체 미상). 같은 폴더의 `Claude/docs/v1.0.18.2/sample_test_v1018_2.png`(282,079 B · 2026-09-02 16:49)와 세 폴더의 `figs/P4_lco_heat_validation.png`(98,479 B · 2026-09-02 16:47–16:49)는 스냅샷의 untracked 목록에 없으므로 tracked 로 추정된다(git 미실행 — 미검증, DQ-14). png 는 열지 않았다.

### 5.2 Codex 측 13건 — 지위 고정 "Codex 소관 · 무접근(판정 안 함)" · 열람 0

| # | path | 지위 |
|---|---|---|
| 1 | `Codex/work/agent_reports/` | Codex 소관 · 무접근(판정 안 함) |
| 2 | `Codex/work/audit_runtime/` | Codex 소관 · 무접근(판정 안 함) |
| 3 | `Codex/work/literature/` | Codex 소관 · 무접근(판정 안 함) |
| 4 | `Codex/work/local_remote_pdf_compare_v10182/` | Codex 소관 · 무접근(판정 안 함) |
| 5 | `Codex/work/phase004/` | Codex 소관 · 무접근(판정 안 함) |
| 6 | `Codex/work/phase005/` | Codex 소관 · 무접근(판정 안 함) |
| 7 | `Codex/work/phase006/` | Codex 소관 · 무접근(판정 안 함) |
| 8 | `Codex/work/phase007/` | Codex 소관 · 무접근(판정 안 함) |
| 9 | `Codex/work/phase010_sources/` | Codex 소관 · 무접근(판정 안 함) |
| 10 | `Codex/work/scripts/` | Codex 소관 · 무접근(판정 안 함) |
| 11 | `Codex/work/source_archives/` | Codex 소관 · 무접근(판정 안 함) |
| 12 | `Codex/work/source_snapshots/` | Codex 소관 · 무접근(판정 안 함) |
| 13 | `Codex/work/tools/` | Codex 소관 · 무접근(판정 안 함) |

`Codex/` 는 읽기·디렉터리 목록 조회 포함 0회 접근(존재 여부조차 본 sub 는 확인하지 않았다 — 목록은 brief §3.5 전사).
'@
foreach($l in ($sec5 -split "`r?`n")){Add $l}
# ---- §6 ----
Add ''; Add '## 6. 현행 tex 60 — 마스터별 `\input` 순서와 빌드 포함/미포함(§3.2)'; Add ''
Add '마스터 tex 3본(I-8 전문 정독)의 비주석 행 `\input{_sections/…}` 실측(`Grep ^[^%]*\input\{` — `docs/v1.0.25.1/**/*.tex` 전건에서 마스터 3본 외 매치 0 → 중첩 `\input` 없음). 각 마스터는 먼저 `common_preamble_v1024`(L10/L8/L8)를 `\input` 하고 본문 절을 순서대로 `\input` 한다.'
foreach($m in $inputOrder.Keys){ Add ''; Add ('### ' + $m + ' — `\input` ' + @($inputOrder[$m]).Count + '건'); Add ''; Add ((@($inputOrder[$m] | ForEach-Object { '`' + $_ + '`' })) -join ' → ') }
$inc=@($groups['xvi'] | Where-Object { (Build $_) -like '포함*' }); $orph=@($groups['xvi'] | Where-Object { (Build $_) -eq '미포함·orphan' }); $mas=@($groups['xvi'] | Where-Object { (Build $_) -eq '마스터' }); $ind=@($groups['xvi'] | Where-Object { (Build $_) -like '미포함·독립*' })
$c1=@($inputOrder['ch1_graphite_v1.0.24.tex']).Count; $c2=@($inputOrder['ch2_lco_v1.0.24.tex']).Count; $c3=@($inputOrder['ch3_si_v1.0.24.tex']).Count
Add ''; Add "### 집계 — 마스터 $($mas.Count) · 빌드 포함 $($inc.Count) · 미포함 $($orph.Count+$ind.Count)(독립 부록 $($ind.Count) + orphan $($orph.Count)) = $($mas.Count+$inc.Count+$orph.Count+$ind.Count)/60"; Add ''
Add ('- `_sections` 56 중 `\input` 되는 고유 파일 = ' + $inputMap.Keys.Count + ' (ch1 ' + $c1 + ' + ch2 ' + $c2 + ' + ch3 ' + $c3 + ' = ' + ($c1+$c2+$c3) + ' 건, `common_preamble_v1024` 3회 중복 제거).')
Add ('- orphan ' + $orph.Count + ' = ' + ((@($orph | ForEach-Object { '`' + [IO.Path]::GetFileName($_.rel) + '`' })) -join ' · ') + ' — `ch1_appD_si` 는 기대(brief §3.2 · R4b DQ-3)와 일치; `ch1_preamble`·`ch2_preamble` 는 **기대(지원 4본 = 빌드 포함)와 상이**: 두 파일 헤더 L2–3 이 각각 `graphite_ica_ch1_v1.0.21.tex`·`graphite_ica_ch2_v1.0.21.tex` 가 `\input` 한다고 적은 v1.0.21 잔재이며, `common_preamble_v1024.tex`:3 이 "= 구 ch1_preamble ∪ ch2_preamble" 로 흡수했음을 명시한다(확정). 지원 파일로 실제 `\input` 되는 것은 `common_preamble_v1024`(마스터 3본)와 `ch1v22_partT_divider`(ch1 L39) 2본뿐.')
Add '- `INDEX_v25.md`:32 는 ch1 마스터의 `\input` 을 34 로 기재 — 본 실측(비주석 `\input{_sections/…}`)은 33. 차이 1 의 원인 = 근거 미발견(집계 기준 차이 추정 · 마스터 파일은 v1.0.25 → v1.0.25.1 에서 표시 버전만 변경).'
Add '- 독립 부록 `appendix_phase_separation.tex` = 자체 `\documentclass` L13 · `\begin{document}` L41 · `_sections` 밖 · `\input` 0(확정) → 미포함·독립.'
Add '- 마스터 플랜 §2.9 L203 "미정독 = ch1v22_partT_divider·ch1_preamble·ch2_preamble·common_preamble_v1024(grep 만) + 마스터 3본 → 배정 = 2.1 Step 14" 는 orphan 2본을 정독 대상으로 유지할지 재검토 대상(DQ-3).'
# ---- §7 coverage ----
Add ''; Add '## 7. 판독 커버리지 대조(R1~R7 Read Coverage 파일 집합 ⊆ OUT-INV)'; Add ''
Add '| 파일 | R# 태그 | TSV 존재 | OUT-INV 군 | 판정 |'; Add '|---|---|---|---|---|'
$cntAll=0;$cntIn=0;$cntOut=0;$cntAbs=0
foreach($k in ($COVMAP.Keys | Sort-Object)){ $cntAll++; $tags=@($COVMAP[$k] | Select-Object -Unique) -join '·'; $ex=$byRel.ContainsKey($k); if(-not $ex){$cntAbs++; $st='실물 부재 → R# 경로 오기 후보'; $gr='—'} elseif($assigned.ContainsKey($k)){$cntIn++; $st='등재'; $gr="($($assigned[$k]))"} else {$cntOut++; $st='실물 존재 · OUT-INV 군 밖'; $gr='미등재'}; Add "| ``$k`` | $tags | $(if($ex){'있음'}else{'없음'}) | $gr | $st |" }
Add ''; Add "**판정**: R1~R7 Read Coverage 열거 파일 $cntAll 건 중 등재 $cntIn · 군 밖 $cntOut · 실물 부재 $cntAbs → ⊆ $(if($cntOut -eq 0 -and $cntAbs -eq 0){'성립'}else{'불성립(예외 위 열거)'})."
Add ''; Add '일괄 기록(파일별 태그 미부여): R3 = `docs/v1.0.25.1/_sections/*.tex` 전건 키워드 grep + `Claude/**/*.md` `D21`·`D22` grep(매치 파일은 위 표에 `R3(grep)` 태그) · R4a = `_sections` LCO·Si·notation·divider·ch2 부록·`appendix_phase_separation.tex` 카운트 grep · R5·R6 = `_sections` 전건 키워드 grep · R7 = `_sections` 53본(bib 제외) + 마스터 3본 기계 스캔(`\cite`·절 제목·키워드 빈도, 전문 정독 아님). 이들은 (xvi) 60본 전건이 OUT-INV 에 있으므로 ⊆ 에 영향 없음. R# 가 적은 행 범위 상한(예: R1 `docs/INDEX.md` L1–197)은 TSV 줄수(196)와 +1 차이가 나며 이는 §0 줄수 정의 차이다(경로 오기 아님).'
# ---- §8 ----
$un=@($rows | Where-Object { -not $assigned.ContainsKey($_.rel) })
$sec8=@'

## 8. 부재·미검독 명시

### 8.1 부재(기대했으나 실물 없음)

- 기대 항목 중 실물 부재 = **0건**. 모든 군의 기대 파일이 존재한다(§7 실물 부재 0 포함).
- 기대와 **다른** 실측(부재 아님): brief §3.2 "지원 4본은 `\input` 되는 빌드 포함 파일" → `ch1_preamble.tex`·`ch2_preamble.tex` 는 `\input` 0 = orphan(§6). 빌드 포함 58/미포함 2 기대 → 실측 56(마스터 3 + 포함 53)/4.

### 8.2 미검독(이 Step 에서 열지 않은 것 — 추정 금지)

- 본 sub 가 내용을 읽은 파일 = work_log 「Read Coverage」 표 전건뿐(brief · 마스터 플랜 지정 행 범위 · INDEX 3 · 1g txt · comp_v26 README L20–35 · 마스터 tex 3 · R1~R7 Read Coverage 절 · preamble 3본 · `V1010_INSPECT_draft_C3.md`). 그 밖의 OUT-INV 등재 파일 전부 = 존재·줄수·hash·바이트만 측정, **내용 미검독**(조사 문서군·ledger·Result·계획서 본문·tex 본문·판독 산출 본문 포함).
- png·pdf·html 은 열지 않았다(존재·바이트·mtime 만). `Codex/` 0회 접근.
- 버전 귀속에 "추정" 이 붙은 행(날짜·이름 추론)은 Step 2 정독에서 확정 대상.

### 8.3 모집단 안이지만 OUT-INV 군 밖(미등재 — 계수만)
'@
foreach($l in ($sec8 -split "`r?`n")){Add $l}
Add ''; Add "TSV 2,651 − 등재 $tot = 미등재 $($un.Count) 파일 · $(($un | Measure-Object lines -Sum).Sum) 줄. 폴더별(상위 3단계):"; Add ''; Add '| 폴더 | 파일 | 줄수 | 내용(확장자 계수) |'; Add '|---|---|---|---|'
foreach($g in ($un | Group-Object { $s=$_.rel -split '/'; if($s.Count -ge 3){ $s[0..2] -join '/' } else { $s[0..($s.Count-2)] -join '/' } } | Sort-Object Name)){ $ext=(@($g.Group | Group-Object { [IO.Path]::GetExtension($_.rel) } | Sort-Object Name | ForEach-Object { "$($_.Name) $($_.Count)" })) -join ' · '; Add "| ``$($g.Name)`` | $($g.Count) | $(($g.Group | Measure-Object lines -Sum).Sum) | $ext |" }
$sec8b=@'

주요 미등재 항목의 성격(전부 내용 미검독 · 등재 여부는 DQ-6·DQ-10·DQ-11):
- `results/comp_v24/` 비-md(`.py` 29 · `.json` 16 · `.txt` 7 — lco_data provenance 등) · `results/comp_v26_data/` 비-md(json 9 · log 2 ; `.py` 8 은 (xi) 등재).
- `docs/v1.0.22/results/` 의 `comp_AUD`(4)·`comp_R2`~`comp_R8`·`comp_RV`(3) = 경쟁 저작 초안·검수 보고 84본(md·tex) · `docs/v1.0.20/results/` 의 `comp_P2/P4/P7_figs/P7_review/Q2/Q3` 97본(md·tex·py·txt·json) 및 `snapshot_*.json`.
- `docs/v1.0.10 ~ v1.0.24.1` 구버전 폴더의 tex·py·log·md(FITTING_GUIDE·CODE_GUIDE 등) — 현행 아님 · `docs/v1.0.25*/results/comp_R1/**`(경쟁 초안 tex·md 각 30·13) · `docs/v1.0.25*/` 의 코드·게이트·가이드(`Anode_Fit_v1.0.24.py` 1,917 · `test_gates_*.py` 4 · `tools_*.py` 4 · `CODE_GUIDE_v24.md` · `FITTING_GUIDE.md`).
- `old/**` 잔여(구트랙 tex·md·py — ledger·Result·HANDOVER·dossier·유실 원문 5본은 등재) · `results/builds/**`·`results/research/**` 잔여(경쟁 빌드 로그·tex·조사 카드) · `results/code/Anode_Fit_v11_final.py` · `results/process/` 의 비-ledger·비-Result md(`V1017_REVIEW_COMPLETE`·`V1017_FIXLIST_CONSOLIDATED` 등) · `results/MISSING_CONTENT_REVIEW.md`.
- `Claude/skills/competition-cherrypick-authoring/SKILL.md`(98줄 · 스킬 사본 — 이력 문서 아님).
- `Claude/results/` 상위 md 4본(군 정의 밖): `Step 1 — 인벤토리 파일 생성(OUT-INV).md`(35줄 — 본 arc Step 1 이력 · master 산출 · TSV 시점 09:34 에 이미 존재; 1g A22 `Step*=0` 은 GO 직전 값) · `V1024_PROGRESS_SUMMARY.md`(51) · `_FINAL_README.md`(25) · `MISSING_CONTENT_REVIEW.md`(93 · `docs/INDEX.md`:193 참조).

### 8.4 모집단 밖(확장자 밖)

- png·pdf·npz·aux·out·toc·html·csv·ps1·bat·pyc 는 계수하지 않았다(§5 의 untracked 실물·JCP PDF·v1.0.25.1 PDF 3종 포함 — PDF 페이지 102/30/22 는 1g A15 기록을 전사, 본 sub 미측정).
- 본 Step 산출 3본(`V1027_HISTORY_INVENTORY.md` · `iter_1/inventory_raw.tsv` · `iter_1/work_log.md`)은 TSV 생성 뒤 작성되어 TSV 에 없다.

## 9. Decision Queue(결정 필요 — 본 sub 는 진행하지 않음 · 기본값 명시)

| # | 항목 | 내용·근거 | 기본값(본 문건 적용) |
|---|---|---|---|
| DQ-1 | 문서 종류 매핑 확정 | 14종 어휘 밖 세부(감사(머지 판정)·Result(집행 보고)·기타(…)·서지 원장(초안))를 §0 매핑 규칙으로 부여 — master 확정 필요 | §0 규칙 그대로 |
| DQ-2 | 버전 귀속 "추정" 행 | `plans/` 2026-05-29~06-09 계획서(v2 이전) · `results/process/PHASE_*` 계보(F0~F9·R0~R9·DEEP_REVIEW 등 계획서 대응 미확정) · `anodefit-*` 2본(07-18 → v1.0.23 추정) · `MASTER_ROADMAP_*` 2본(무날짜) — Step 2 정독 배정 시 실물 정독으로 확정 | 표에 "추정" 명기·유지 |
| DQ-3 | orphan preamble 2본의 정독 대상 여부 | `ch1_preamble`·`ch2_preamble` 는 v1.0.21 잔재 orphan(§6) — §2.9 L203 은 "지원 4본" 을 2.1 Step 14 정독 배정. 정독 유지(계보 확인용) vs 제외 | 등재 유지 · 빌드 열 "미포함·orphan" |
| DQ-4 | hash 사본 고유본 표기 | 규칙(가장 이른 버전 폴더)을 현행 tex 60 에 적용하면 v1.0.24 사본이 고유본 — 정독은 현행 경로(v1.0.25.1) · 등록부 표기는? · 같은 폴더 동명이물(`old/Archive_oldtrack/REVIEW_LEDGER_CH2_10ROUND{,_CLAUDE_rerun_5-29}.md`) 고유본 | §4 규칙 그대로(경로 정렬 최상) · tex 는 비고에 "정독은 현행 경로" |
| DQ-5 | `old/**` ledger 31·Result 33 등재 범위 | (vii)·(viii) 패턴이 `old/` 에도 매치 — 마스터 플랜 정의는 "각 버전"·`results/**`·`docs/vN/results/` 라 `old/` 는 정의 밖. 구트랙 별도 표시로 등재 vs 제외 | 등재(구트랙 RB 표시) |
| DQ-6 | (ix) 미등재 하위군 | `docs/v1.0.22/results/comp_AUD·R2~R8·RV` 84 · `docs/v1.0.20/results/comp_*` 97 · `comp_P7_review/REVIEW_*` 11 — 조사 문서군 편입 여부 | §8.3 계수만 |
| DQ-7 | untracked png 5 처리 | 재생성 가능 산출물(§5.1 #1~#5) — git 추적/무시/삭제는 사용자 결정 | 지위 "유효" 기재만 |
| DQ-8 | `C3_pdf_render/` 50장 보존 | 참조 문서 있으나 폴더명 직접 참조 0 · 총 ~15 MB 추정(개별 바이트 합산 미실시) | 지위 "유효(추정)" 기재만 |
| DQ-9 | plans 10,384 vs 1g 10,383 | +1 파일 미특정 — master 가 1g 시점 파일별 수치를 보유하면 대조 | 실측 정본 10,384 |
| DQ-10 | `comp_v24` 비-md 52본 등재 | py 29·json 16·txt 7 — 2.6·3.1 데이터 판정에 재사용 가능(Assumptions 14) | §8.3 계수만 |
| DQ-11 | `Claude/skills/…/SKILL.md` | 군 밖 · 이력 문서 아님 | 미등재 |
| DQ-12 | `common_preamble_v1024.tex`:2 헤더 파일명 표기 `common_preamble_v1022.tex` | 문건 결함 후보(파일명 불일치) — 수정 X · 등록부/GAP 단계에서 다룸 | 관찰만 기재 |
| DQ-13 | (xi) 추가 발견 2본 | R2 Read Coverage +2·+3(`out_skew/summary_skew.json`·`skew_log.txt`, README.md:30 폐기분 산출) 을 ⊆ 유지 목적으로 (xi) 등재 | 등재(폐기분 표시) |
| DQ-14 | `sample_test_v1018_2.png`·`figs/P4_lco_heat_validation.png` tracked 여부 | mtime 2026-09-02 인데 untracked 목록에 없음 → tracked 추정 · git 필요(master) | 관찰만 기재 |
| DQ-15 | OUT-INV 생성 방식 | 본 문건의 §1·§2·§4·§6·§7·§8.3 표는 TSV 를 읽는 생성 스크립트(세션 스크래치패드 `gen_outinv.ps1` · 휘발 · 프로젝트 밖)로 산출 — 인라인 실행이 명령 길이 제한에 걸려 스크립트 파일 경유. 프로젝트 안 신규 파일은 3본뿐 | 스크래치패드 사용(work_log 기록) |
'@
foreach($l in ($sec8b -split "`r?`n")){Add $l}
$OUTL | Out-File -FilePath $out -Encoding utf8
"written: $out lines=$((Get-Content $out).Count)"
"groups:"; foreach($id in $groups.Keys){ "  ($id) n=$($groups[$id].Count) lines=$(($groups[$id] | Measure-Object lines -Sum).Sum)" }
"assigned total=$tot totalLines=$totL unassigned=$($un.Count)"
"xvi build: masters=$($mas.Count) inc=$($inc.Count) orphan=$($orph.Count) indep=$($ind.Count)"
"coverage: all=$cntAll in=$cntIn out=$cntOut absent=$cntAbs"
"hash groups=$($hg.Count)"
"ver-rule-miss: " + ((@($rows | Where-Object { $assigned.ContainsKey($_.rel) -and (Ver $_.rel) -eq '미측정(귀속 규칙 밖)' } | ForEach-Object {$_.rel})) -join ', ')
