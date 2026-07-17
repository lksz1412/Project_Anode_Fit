# SEAM_PLAN — 이음매·구획 전환표 (v1.0.22 R2 · O-A 초안)

> 지위: `comp_R2/A_seams/` 신규 초안. 마스터 소스(`.tex`) 미수정 — 집행은 페이블 마스터가 diff 1:1 로그로 수행.
> 대조 정본: `results/R1B_SWEEP_LIST.md`(T1 20·T2 53·T3 5 = 78건, 파일:행 1:1) + `plans/PLAN_R1_reorg.md` Step 14.
> 원문 대조: `_sections/*.tex` 전문 실독(2026-07-17). **개정안의 모든 `\ref`/`\eqref` 라벨은 원문에서 직접 확인한 실존 라벨만.**

## 0. 전환 원칙과 호칭 규약

**신 구조**(마스터 `ch1_graphite_v1.0.22.tex`가 조립):
`Part 0`(통계역학 기초 = `ch1_sec02a/02b`, 절 제목에 "(Part 0)" 명시·라벨 `sec:sm-found`) →
`Part I`(흑연 곡선 사슬 = `ch1_sec00~10`) →
`Part T`(흑연 열특성 = `ch2_sec00~10`, divider `ch1v22_partT_divider`가 "Part T" 표제 출력) → `§18` → 부록 4본.
LCO(`ch1_sec11~17`)는 **별도 마스터 `ch2_lco_v1.0.22.tex` = 신 Chapter 2**. (Part 0/I/T 명칭은 `ch1_sec00_intro` 21~25행이 이미 본문에서 확립.)

**호칭 규약**(본 표 전체 일관 적용):

| 상황 | 구 지칭 | 개정 호칭 | 참조 기제 |
|---|---|---|---|
| **T1** — Part I·Part 0·부록 파일이 구 "Chapter 2"(열특성) 지칭 | `Chapter 2 …` | `Part T …` + `\S\ref`/`\eqref`(Part T 라벨) | 같은 문서(동일 마스터) live 참조 |
| **T2** — Part T 파일이 구 "Chapter 1"(흑연/Part 0) 지칭 | `Chapter 1 §N …` | Part 0 은 `Part 0(\S\ref{sec:sm-…})`, 흑연 §1~10 은 `\S\ref{…}`(필요 시 "Part I"/"앞 파트" 방향어) | 같은 문서 live 참조 |
| **T2 자기 구지칭** | `Chapter 2 종합식` | `본 파트 종합식` | Part T 자체 라벨(무변경) |
| **T3** — Part T 파일이 구 "Chapter 1 §11~17"(LCO) 지칭 | `Chapter 1 §N …` | `Chapter 2 \S\ref{sec:lco-…}` | **xr 장 간**(`ch1_graphite` 의 `\externaldocument{ch2_lco_v1.0.22}` 8행이 해소) |
| **장 전역 규약**(부호·방향 라벨) | `Chapter 1 의 규약` | `본 장의 규약` | 신 Ch1 = 흑연 곡선+Part 0+Part T 전체 |

- "본 장" = 신 Chapter 1 전체. "본 파트" = 화자가 속한 Part T(자기지칭). "앞 파트" = 화자보다 앞선 Part 0/I — 이미 S-008 정정문(`ch2_appA_traps:51`)이 이 형태를 씀(정합 앵커).
- **최소 diff 원칙**: 산문 논지·수식·자산 무변경, 지칭 계층·격만 교체. 서술형 괄호 라벨 `(eq:xxx)` → live `\eqref{eq:xxx}`.
- **T3 ≠ T2 경고**: T3(§11~17)는 대상이 신 Ch2 로 이동해 방향이 T2 와 반대. 문면이 비슷해도 §번호(11~17 = T3 / 1~9 = T2)로 판별 — 기계 치환 금지.

## 1. T1 전환표 (20건 — Part I/Part 0/부록 → Part T)

대상 라벨은 전부 `_sections/ch2_sec*.tex`(Part T)에서 실확인: `sec:partition`·`ssec:site`·`sec:vibel`·`sec:mixing`·`ssec:overlap`·`ssec:weff`·`sec:synthesis`·`ssec:qrevtab`·`sec:method` · `eq:Z1`·`eq:Svib_mode`·`eq:muV`·`eq:implicit`·`eq:Vxi`·`eq:logistic`.

| 파일:행 | 분류 | 현행(해당 부분) | 개정안(LaTeX) | 비고 |
|---|---|---|---|---|
| `ch1_appB_codemap:132` | T1 | `\code{solve\_U\_oc}(Chapter 2 전하 보존 음함수의 유일근 솔버)` | `\code{solve\_U\_oc}(Part T 전하 보존 음함수~\eqref{eq:implicit} 의 유일근 솔버)` | `eq:implicit`=`ch2_sec05:18` 실존 |
| `ch1_appB_codemap:135` | T1 | `요구명세는 Chapter 2 부록 B) \\` | `요구명세는 열특성 코드 구현 요구명세 부록(부록 B) \\` | **판단 보류** — `ch2_appB` 에 section `\label` 없음 → live `\S\ref` 불가. MISC 코드맵 제목 분업(부록 D 개명+라벨 신설) 확정 후 확정. 그때까지 서술형 |
| `ch1_sec01_n0n1:214` | T1 | `LCO 질서화(\S\ref{sec:lco-hys-od}) 구분과 Chapter 2 의 SOC 부호 교대가` | `LCO 질서화(\S\ref{sec:lco-hys-od}) 구분과 Part T 의 SOC 부호 교대(\S\ref{ssec:qrevtab})가` | `ssec:qrevtab`=`ch2_sec08:110`. (기존 `sec:lco-hys-od` 전방 xr 은 무변경) |
| `ch1_sec01_n0n1:216` | T1 | `그 계산 절차와 실측 대응은 Chapter 2 의 방법론 절이 담당한다.` | `그 계산 절차와 실측 대응은 Part T 의 방법론 절(\S\ref{sec:method})이 담당한다.` | `sec:method`=`ch2_sec09:4` |
| `ch1_sec02a_part0:9` | T1 | `양자 통계가 필요한 항(점유 자리의 진동 자유도, Chapter 2 의 포논$\cdot$전자 분포)은` | `양자 통계가 필요한 항(점유 자리의 진동 자유도, Part T 의 포논$\cdot$전자 분포, \S\ref{sec:vibel})은` | `sec:vibel`=`ch2_sec03:4` |
| `ch1_sec02a_part0:202` | T1 | `진짜 양자 통계가 일하는 곳은 Chapter 2 다 --- 격자 진동의 양자(포논)는` | `진짜 양자 통계가 일하는 곳은 Part T(\S\ref{sec:vibel})다 --- 격자 진동의 양자(포논)는` | `sec:vibel` |
| `ch1_sec02a_part0:233` | T1 | `Chapter 2 의 단일 자리 분배함수(그 문건 식 (eq:Z1))도 같은 기호 $\Xi_1$ 로 통일한다.` | `Part T 의 단일 자리 분배함수(\S\ref{ssec:site} 식~\eqref{eq:Z1})도 같은 기호 $\Xi_1$ 로 통일한다.` | 서술형→`\eqref`; `eq:Z1`=`ch2_sec01:23`, `ssec:site`=`ch2_sec01:16` |
| `ch1_sec02a_part0:300` | T1 | `이것이 Chapter 2 의 vibrational 엔트로피 사슬의 단일 자리 원형이다` | `이것이 Part T 의 vibrational 엔트로피 사슬(\S\ref{sec:vibel})의 단일 자리 원형이다` | `sec:vibel` |
| `ch1_sec02a_part0:302` | T1 | `식~\eqref{eq:sm-sint} 에 넣으면 그 문건의 모드당 엔트로피 $s_k=k_B[…]$가 그대로 나온다` | `식~\eqref{eq:sm-sint} 에 넣으면 Part T 의 모드당 엔트로피~\eqref{eq:Svib_mode}가 그대로 나온다` | `eq:Svib_mode`=`ch2_sec03:25` (동일 $k_B[(1{+}n)\ln(1{+}n)-n\ln n]$ 꼴 실확인) |
| `ch1_sec02b_part0:183` | T1 | `Chapter 2 의 식 (eq:muV)도 같은 관계다.` | `Part T 의 식~\eqref{eq:muV}도 같은 관계다.` | 서술형→`\eqref`; `eq:muV`=`ch2_sec01:55` |
| `ch1_sec02b_part0:284` | T1 | `본론과 Chapter 2 가 중심식으로 쓰는 전하 보존 음함수가 이 대정준 구조의` | `본론과 Part T 가 중심식으로 쓰는 전하 보존 음함수가 이 대정준 구조의` | 호칭만(구체 라벨은 345행에서 명시) |
| `ch1_sec02b_part0:345` | T1 | `이 식은 Chapter 2 가 겹침 가중의 출발점으로 세우는 전하 보존 음함수(그 문건 식 (eq:implicit))와 글자까지` | `이 식은 Part T 가 겹침 가중의 출발점으로 세우는 전하 보존 음함수(\S\ref{ssec:overlap} 식~\eqref{eq:implicit})와 글자까지` | 서술형→`\eqref`; `eq:implicit`=`ch2_sec05:18`, `ssec:overlap`=`ch2_sec05:12` |
| `ch1_sec02b_part0:367` | T1 | `이 한 줄이 Chapter 2 의 계산(그 문건의 유일근 서술)의 통계역학 증명이고` | `이 한 줄이 Part T 의 계산(그 파트의 유일근 서술, \S\ref{ssec:overlap})의 통계역학 증명이고` | `ssec:overlap` (Part T 유일근 서술 위치) |
| `ch1_sec02b_part0:370` | T1 | `본론과 Chapter 2 가 반전에 실제로 쓰는 전이별 logistic 서식(폭 $w_j$ 의 이중지위는 \S\ref{sec:width})` | `본론과 Part T 가 반전에 실제로 쓰는 전이별 logistic 서식(폭 $w_j$ 의 이중지위는 \S\ref{sec:width})` | 호칭만; 기존 `\S\ref{sec:width}` 무변경 |
| `ch1_sec02b_part0:383` | T1 | `본론 \S\ref{sec:eqpeak} 과 Chapter 2 의 겹침 가중·계산용 종합식이 이 계단을` | `본론 \S\ref{sec:eqpeak} 과 Part T 의 겹침 가중·계산용 종합식(\S\ref{ssec:overlap}$\cdot$\S\ref{sec:synthesis})이 이 계단을` | `sec:synthesis`=`ch2_sec08:4` |
| `ch1_sec02b_part0:424` | T1 | `배치 셈법에서 온다(Chapter 2 의 식 (eq:Vxi)가 같은 결론을 발열 관점에서 재사용한다).` | `배치 셈법에서 온다(Part T 의 식~\eqref{eq:Vxi}가 같은 결론을 발열 관점에서 재사용한다).` | 서술형→`\eqref`; `eq:Vxi`=`ch2_sec01:97` |
| `ch1_sec05_width:238` | T1 | `가역 발열 config 항에 자기정합 전파된다(Chapter 2 겹침 가중 파생 A 에서 유도, 발열 종합식이 받음;` | `가역 발열 config 항에 자기정합 전파된다(Part T 겹침 가중 파생 A(\S\ref{ssec:overlap})에서 유도, 발열 종합식(\S\ref{sec:synthesis})이 받음;` | `ssec:overlap`·`sec:synthesis` |
| `ch1_sec05_width:269` | T1 | `첫째 지위(평형 예측)라는 성격은 변하지 않는다(Chapter 2 파생 C 와 동일 취지).` | `첫째 지위(평형 예측)라는 성격은 변하지 않는다(Part T 파생 C(\S\ref{ssec:weff})와 동일 취지).` | `ssec:weff`=`ch2_sec05:161` |
| `ch1_sec05_width:360` | T1 | `\eqref{eq:logisticsolve}$\cdot$\eqref{eq:xieq} 와 일치한다(Chapter 2 의 식 (eq:logistic)과 부호까지 동일).` | `\eqref{eq:logisticsolve}$\cdot$\eqref{eq:xieq} 와 일치한다(Part T 의 식~\eqref{eq:logistic}과 부호까지 동일).` | 서술형→`\eqref`; `eq:logistic`=`ch2_sec01:72` |
| `ch1_sec07_broadening:26` | T1 | `(\S\ref{sec:width-w} 의 지위 구분$\cdot$Chapter 2 파생 C 각주와 같은 한정).` | `(\S\ref{sec:width-w} 의 지위 구분$\cdot$Part T 파생 C(\S\ref{ssec:weff}) 각주와 같은 한정).` | `ssec:weff` |

## 2. T2 전환표 (53건 — Part T·부록 → Part 0/I, 같은 문서)

대상 라벨은 전부 `_sections/ch1_sec*.tex`(Part 0/I)에서 실확인: 절 = `sec:sm-found`·`sec:sm-site`·`sec:sm-mf`·`sec:sm-lattice`·`sec:sm-mc`·`sec:center`·`sec:hys`·`sec:width`·`sec:broadening`·`sec:lag`·`sec:tail`·`sec:notation`·`sec:n0map`·`sec:pol`·`sec:signcheck` / 식·표 = `eq:sm-mc-balance`·`eq:sm-Smix`·`eq:sm-sint`·`eq:Ubranch`·`eq:Uj`·`eq:vn`·`tab:staging`. **`eq:logistic` 은 Part T 자체 라벨**(ch2_sec01) — 서술형 "Chapter 1 의 …~\eqref{eq:logistic}" 는 호칭만 바꾸고 `\eqref` 는 무변경.

| 파일:행 | 분류 | 현행(해당 부분) | 개정안(LaTeX) | 비고 |
|---|---|---|---|---|
| `ch2_appA_traps:9` | T2 | `Chapter 1 부록의 부호 사슬 검산표와 같은 용도다.` | `본 장 부호 사슬 검산표(\S\ref{sec:signcheck})와 같은 용도다.` | `sec:signcheck`=`ch1_appA:5` 실존 |
| `ch2_appB_codemap:13` | T2 | `와 Chapter 1 의 $\xi_j(V,T)$~\eqref{eq:logistic} 를 받아, 전하 보존` | `와 Part I 의 $\xi_j(V,T)$~\eqref{eq:logistic} 를 받아, 전하 보존` | 호칭만; `eq:logistic`(Part T 자체) 무변경 |
| `ch2_appB_codemap:25` | T2 | `증명은 Chapter 1 Part 0 의 다클래스 소절(그 문건 식 (eq:sm-mc-balance))이 상술한다.` | `증명은 Part 0 의 다클래스 소절(\S\ref{sec:sm-mc} 식~\eqref{eq:sm-mc-balance})이 상술한다.` | 서술형→`\eqref`; `eq:sm-mc-balance`=`ch1_sec02b:343`, `sec:sm-mc`=`ch1_sec02b:280` |
| `ch2_appB_codemap:27` | T2 | `구현이 재현해야 한다(298.15 K, Chapter 1 4-전이 staging, $w_j{=}RT/F$).` | `구현이 재현해야 한다(298.15 K, Part I 4-전이 staging[표~\ref{tab:staging}], $w_j{=}RT/F$).` | `tab:staging`=`ch1_sec10:31` |
| `ch2_sec00_intro:7` | T2 | `Chapter 1 은 흑연 음극의 한 $\dd Q/\dd V$ 곡선을,` | `Part I 는 흑연 음극의 한 $\dd Q/\dd V$ 곡선을,` | → `ch2_sec00_intro_partT.tex` 초안 반영 |
| `ch2_sec00_intro:8` | T2 | `$U_j(T)=…$(Chapter 1 §3 의 평형 중심 전위) 위에 세운` | `$U_j(T)=…$(\S\ref{sec:center} 의 평형 중심 전위) 위에 세운` | `sec:center`=`ch1_sec03:4`; 초안 반영 |
| `ch2_sec00_intro:33` | T2 | `이것이 바로 Chapter 1 의 logistic 평형 점유의 통계역학적 기원임을 보인다` | `이것이 바로 Part I \S\ref{sec:width} 의 logistic 평형 점유의 통계역학적 기원임을 보인다` | `sec:width`=`ch1_sec05:4`; 초안 반영 |
| `ch2_sec01_partition:10` | T2 | `그것이 Chapter 1 이 \emph{이미 쓰고 있던} logistic 평형 점유의 기원임을` | `그것이 Part I 가 \emph{이미 쓰고 있던} logistic 평형 점유의 기원임을` | 호칭만(구체 §은 77행) |
| `ch2_sec01_partition:13` | T2 | `배경(…)은 Chapter 1 §2(Part 0, 통계역학 기초)가 처음부터 자세히 세웠다` | `배경(…)은 Part 0(통계역학 기초, \S\ref{sec:sm-found})가 처음부터 자세히 세웠다` | `sec:sm-found`=`ch1_sec02a:4` |
| `ch2_sec01_partition:39` | T2 | `$\Xi_1$ 은 자리 1개의 \emph{대정준} 분배함수이며 Chapter 1 §2 Part 0 의 단일 자리 대정준 분배함수와 통일한 표기다` | `$\Xi_1$ 은 자리 1개의 \emph{대정준} 분배함수이며 Part 0 의 단일 자리 대정준 분배함수(\S\ref{sec:sm-site})와 통일한 표기다` | `sec:sm-site`=`ch1_sec02a:106` |
| `ch2_sec01_partition:42` | T2 | `Chapter 1 §2 Part 0 의 유효 자리 자유에너지 유도가 닫았다` | `Part 0 의 유효 자리 자유에너지 유도(\S\ref{sec:sm-site})가 닫았다` | `sec:sm-site` (`eq:sm-epstilde` 소재 절) |
| `ch2_sec01_partition:47` | T2 | `vibrational 엔트로피 몫의 단일 자리 원형이다(Chapter 1 §2 Part 0 의 같은 자리당 엔트로피).` | `vibrational 엔트로피 몫의 단일 자리 원형이다(Part 0 의 같은 자리당 엔트로피, \S\ref{sec:sm-site} 식~\eqref{eq:sm-sint}).` | `eq:sm-sint`=`ch1_sec02a:298` |
| `ch2_sec01_partition:51` | T2 | `\subsection{전기화학 퍼텐셜과 Chapter 1 logistic 의 기원}\label{ssec:logistic}` | `\subsection{전기화학 퍼텐셜과 Part I logistic 의 기원}\label{ssec:logistic}` | **소절 제목 → TOC 연동 주의**; 라벨 무변경 |
| `ch2_sec01_partition:58` | T2 | `$s(=+1)$ 는 Chapter 1 의 \emph{유도 전용 고정 부호}다.` | `$s(=+1)$ 는 본 장의 \emph{유도 전용 고정 부호}다.` | 장 전역 부호 규약(Part 0 `sec:sm-electro`서 확립) |
| `ch2_sec01_partition:59` | T2 | `$\sigma_d$(Chapter 1 §1 --- 분극$\cdot$분기$\cdot$꼬리 세 작용처 전용, $\pm1$)와는` | `$\sigma_d$(\S\ref{sec:notation} --- 분극$\cdot$분기$\cdot$꼬리 세 작용처 전용, $\pm1$)와는` | `sec:notation`=`ch1_sec01:4` (§1 각주) |
| `ch2_sec01_partition:77` | T2 | `후자가 정확히 Chapter 1 §5 의 전이별 \emph{logistic 평형 종}(그 절의 평형 진행률 $\xi_\eq$)이다` | `후자가 정확히 \S\ref{sec:width} 의 전이별 \emph{logistic 평형 종}(그 절의 평형 진행률 $\xi_\eq$)이다` | `sec:width` |
| `ch2_sec01_partition:81` | T2 | `Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라` | `Part I 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라` | keybox; 호칭 |
| `ch2_sec01_partition:113` | T2 | `혼합(섞임) 엔트로피(곧 \S\ref{sec:config}; Chapter 1 §2 Part 0 의 섞임 엔트로피와` | `혼합(섞임) 엔트로피(곧 \S\ref{sec:config}; Part 0 의 섞임 엔트로피와, \S\ref{sec:sm-lattice} 식~\eqref{eq:sm-Smix})` | `eq:sm-Smix`=`ch1_sec02a:337`, `sec:sm-lattice`=`ch1_sec02a:316` |
| `ch2_sec01_partition:133` | T2 | `이 임계 $\Omega=2RT$ 는 Chapter 1 §4(히스테리시스)의 spinodal 조건과 같은 열역학이며` | `이 임계 $\Omega=2RT$ 는 \S\ref{sec:hys}(히스테리시스)의 spinodal 조건과 같은 열역학이며` | `sec:hys`=`ch1_sec04:4` |
| `ch2_sec02_config:6` | T2 | `그 여집합 $\xi=1-\theta$ 가 Chapter 1 의 평형 종임을 보였다.` | `그 여집합 $\xi=1-\theta$ 가 Part I 의 평형 종임을 보였다.` | 호칭 |
| `ch2_sec02_config:50` | T2 | `\textbf{Chapter 1 의 logistic 폭 $w=RT/F$ 가 이미 부분몰 configurational 엔트로피를 담고 있었다}` | `\textbf{Part I 의 logistic 폭 $w=RT/F$ 가 이미 부분몰 configurational 엔트로피를 담고 있었다}` | 호칭 |
| `ch2_sec02_config:101` | T2 | `\caption{… Fermi--Dirac 와 동형이며 Chapter 1 logistic 평형 점유의 기원.` | `\caption{… Fermi--Dirac 와 동형이며 Part I logistic 평형 점유(\S\ref{sec:width})의 기원.` | **캡션 → LoF**. (같은 그림 tikz 노드 83행 "= Ch1 logistic" 도 "= Part I logistic" 로 정합 권고 — 추가 후보, 스윕 밖) |
| `ch2_sec02_config:134` | T2 | `\subsection{문헌 검증 --- Chapter 1 staging 엔트로피와의 정합}\label{ssec:litverif}` | `\subsection{문헌 검증 --- Part I staging 엔트로피와의 정합}\label{ssec:litverif}` | **소절 제목 → TOC 연동 주의**; 라벨 무변경 |
| `ch2_sec02_config:143` | T2 | `표~\ref{tab:ds} 는 Chapter 1 의 전이별 중심 표준값 $\Delta S^0_j=…$ 가` | `표~\ref{tab:ds} 는 Part I 의 전이별 중심 표준값 $\Delta S^0_j=…$ 가` | 호칭 |
| `ch2_sec02_config:168` | T2 | `$\dagger$ Chapter 1 의 4 주요 plateau 전이와 Allart 등 \cite{allart2018} 의 세분 region…` | `$\dagger$ Part I 의 4 주요 plateau 전이와 Allart 등 \cite{allart2018} 의 세분 region…` | 표 각주; 호칭 |
| `ch2_sec02_config:175` | T2 | `Chapter 1 의 $\Delta H_{\rxn,j}$ 는 \emph{전이별}(differential) 반응 엔탈피이고` | `Part I 의 $\Delta H_{\rxn,j}$ 는 \emph{전이별}(differential) 반응 엔탈피이고` | 호칭 |
| `ch2_sec03_vibel:9` | T2 | `양자 배경은 Chapter 1 §2 의 배경 박스(페르미온$\cdot$보손과 양자 통계)가 한자리에 정리했다.` | `양자 배경은 Part 0 의 배경 박스(페르미온$\cdot$보손과 양자 통계, \S\ref{sec:sm-site})가 한자리에 정리했다.` | `sec:sm-site` (bgbox 소재 절) |
| `ch2_sec03_vibel:40` | T2 | `electronic($\propto T$, \S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(Chapter 1 의 대응 한정과 동급).` | `electronic($\propto T$, \S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(Part I 의 대응 한정과 동급).` | 호칭(일반 대응) |
| `ch2_sec03_vibel:68` | T2 | `$N_A\kB=R$ 로 환산해 넣는다(Chapter 1 의 단위 환산).` | `$N_A\kB=R$ 로 환산해 넣는다(Part 0 의 단위 환산, \S\ref{sec:sm-lattice}).` | `sec:sm-lattice`(몰 환산 $R=N_Ak_B$) |
| `ch2_sec03_vibel:69` | T2 | `Chapter 1 의 규약대로, 삽입(리튬화)은 일반적으로 $\Delta S_e<0$ 이다` | `본 장의 규약대로, 삽입(리튬화)은 일반적으로 $\Delta S_e<0$ 이다` | 장 전역 방향 규약 |
| `ch2_sec03_vibel:82` | T2 | `Li 배열(Chapter 1 의 ``배치'')의 \emph{격자기체}(config),` | `Li 배열(Part 0 의 ``배치'')의 \emph{격자기체}(config),` | 호칭(배치=Part 0 격자기체 언어) |
| `ch2_sec03_vibel:90` | T2 | `이는 Chapter 1 §8$\cdot$§9 동역학 꼬리의 \emph{활성화 엔트로피} $\Delta S_{a,j}$` | `이는 \S\ref{sec:lag}$\cdot$\S\ref{sec:tail} 동역학 꼬리의 \emph{활성화 엔트로피} $\Delta S_{a,j}$` | `sec:lag`=`ch1_sec08:4`, `sec:tail`=`ch1_sec09:4` |
| `ch2_sec04_einstein:21` | T2 | `이 $u_j$ 는 Chapter 1 \S4 spinodal 근의 $u_j=\sqrt{1-2RT/\Omega_j}$ 와도 동명 별개의` | `이 $u_j$ 는 앞 파트 \S\ref{sec:hys} spinodal 근의 $u_j=\sqrt{1-2RT/\Omega_j}$ 와도 동명 별개의` | 각주; `sec:hys`. (S-008 정정문 `ch2_appA:51` 의 "앞 파트 \S\ref{sec:hys}" 표현과 정합) |
| `ch2_sec05_mixing:23` | T2 | `요동 증명(…)은 Chapter 1 Part 0 의 다클래스 소절(그 문건 식 (eq:sm-mc-balance))이 닫는다.` | `요동 증명(…)은 Part 0 의 다클래스 소절(\S\ref{sec:sm-mc} 식~\eqref{eq:sm-mc-balance})이 닫는다.` | 서술형→`\eqref`; `eq:sm-mc-balance`·`sec:sm-mc` |
| `ch2_sec05_mixing:37` | T2 | `국소 \emph{$dQ/dV$ 봉우리(Chapter 1 의 peak) 모양}이다:` | `국소 \emph{$dQ/dV$ 봉우리(Part I 의 peak) 모양}이다:` | 호칭(peak=`sec:eqpeak`) |
| `ch2_sec05_mixing:42` | T2 | `Chapter 1 §2 의 조성 자유에너지 $g_j(\xi)$$\cdot$본 장의 BW 자유에너지 $g(\theta)$` | `Part 0 의 조성 자유에너지 $g_j(\xi)$(\S\ref{sec:sm-mf})$\cdot$본 파트의 BW 자유에너지 $g(\theta)$` | 2건: `sec:sm-mf`=`ch1_sec02b:5`(g(ξ)) + 자기지칭 본장→본파트 |
| `ch2_sec05_mixing:91` | T2 | `★\textbf{수치 검증(파생 A).} Chapter 1 의 4-전이 흑연 staging 파라미터로,` | `★\textbf{수치 검증(파생 A).} Part I 의 4-전이 흑연 staging 파라미터로,` | 호칭(`tab:staging`) |
| `ch2_sec05_mixing:169` | T2 | `$\Omega>2RT$ 문턱 자체가 가르지 않는다 --- Chapter 1 의 초기값 $\Omega$ 는 네 전이가 모두` | `$\Omega>2RT$ 문턱 자체가 가르지 않는다 --- Part I 의 초기값 $\Omega$ 는 네 전이가 모두` | 각주; 호칭 |
| `ch2_sec05_mixing:172` | T2 | `\cite{dahn1991,ohzuku1993}(Chapter 1 의 staging 초기값$\cdot$post-fit 기준).` | `\cite{dahn1991,ohzuku1993}(Part I 의 staging 초기값$\cdot$post-fit 기준).` | 각주; 호칭 |
| `ch2_sec05_mixing:180` | T2 | `는 Chapter 1 §7 의 broadening 절에서 전개하며, 본 장은 그 결과만 받아` | `는 \S\ref{sec:broadening} 의 broadening 절에서 전개하며, 본 파트는 그 결과만 받아` | 2건: `sec:broadening`=`ch1_sec07:4` + 자기지칭 본장→본파트 |
| `ch2_sec05_mixing:183` | T2 | `따라서 Chapter 2 종합식(\S\ref{sec:synthesis})에 들어가는 $w_j$ 는,` | `따라서 본 파트 종합식(\S\ref{sec:synthesis})에 들어가는 $w_j$ 는,` | **자기 구지칭** → 본 파트; `\S\ref{sec:synthesis}` 무변경 |
| `ch2_sec05_mixing:199` | T2 | `$\sigma_d$ 는 탈리튬화 부호(Chapter 1 §4 의 분기 중심식에서 $\gamma_jh_{\eta,j}{=}1$ 로 둔 특수형)라` | `$\sigma_d$ 는 탈리튬화 부호(\S\ref{sec:hys} 의 분기 중심식~\eqref{eq:Ubranch} 에서 $\gamma_jh_{\eta,j}{=}1$ 로 둔 특수형)라` | `sec:hys`·`eq:Ubranch`=`ch1_sec04:240` (자산 C-88 = Ch1 eq:Ubranch 특수형) |
| `ch2_sec07_revheat:21` | T2 | `과전압 소산(2법칙상 항상 발열, Chapter 1 의 동역학 꼬리$\cdot$분극이 만드는 소산)이고` | `과전압 소산(2법칙상 항상 발열, Part I 의 동역학 꼬리$\cdot$분극이 만드는 소산)이고` | 호칭(꼬리=§8/9, 분극=§1) |
| `ch2_sec07_revheat:29` | T2 | `Chapter 1 의 방향 라벨(흑연 하프셀 방전 $=$ 탈리튬화, $\sigma_d{=}+1$)과 \emph{같은 단어}가` | `본 장의 방향 라벨(흑연 하프셀 방전 $=$ 탈리튬화, $\sigma_d{=}+1$)과 \emph{같은 단어}가` | 장 전역 방향 규약(§1). (트랩표 `ch2_appA:55` 의 축약 "Ch1" 도 정합 권고 — 추가 후보) |
| `ch2_sec08_synthesis:23` | T2 | `Chapter 1 의 $\xi_j(V,T)$(본 장 식~\eqref{eq:logistic} --- Chapter 1 §5 의 평형 진행률에서` | `Part I 의 $\xi_j(V,T)$(본 파트 식~\eqref{eq:logistic} --- \S\ref{sec:width} 의 평형 진행률에서` | 3건: 호칭 Part I + 자기지칭 본장→본파트 + `sec:width`; `eq:logistic`(Part T) 무변경 |
| `ch2_sec08_synthesis:38` | T2 | `나머지는 Chapter 1 모수이며, 단일 전이 지배 영역에서` | `나머지는 Part I 모수이며, 단일 전이 지배 영역에서` | 호칭 |
| `ch2_sec08_synthesis:42` | T2 | `과정을 Chapter 1 의 4-전이 staging 파라미터(중심 $U_j$$\cdot$용량 $Q_j$$\cdot$중심` | `과정을 Part I 의 4-전이 staging 파라미터(중심 $U_j$$\cdot$용량 $Q_j$$\cdot$중심` | 호칭 |
| `ch2_sec08_synthesis:47` | T2 | `여기서 중심 $U_j$ 는 Chapter 1 §3 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F$ 로 평가한` | `여기서 중심 $U_j$ 는 \S\ref{sec:center} 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F$~\eqref{eq:Uj} 로 평가한` | `sec:center`·`eq:Uj`=`ch1_sec03:54` |
| `ch2_sec08_synthesis:114` | T2 | `\caption{… (완전식, 298.15 K; Chapter 1 4-전이 staging, $w_j{=}RT/F$).` | `\caption{… (완전식, 298.15 K; Part I 4-전이 staging, $w_j{=}RT/F$).` | **캡션 → LoT**; 호칭 |
| `ch2_sec09_method:16` | T2 | `분극을 먼저 분리한다 --- Chapter 1 §1 의 $V_n=V_\mathrm{app}-\sigma_d\|I\|R_n$ 로` | `분극을 먼저 분리한다 --- \S\ref{sec:pol} 의 $V_n=V_\mathrm{app}-\sigma_d|I|R_n$~\eqref{eq:vn} 로` | `sec:pol`=`ch1_sec01:159`, `eq:vn`=`ch1_sec01:180` |
| `ch2_sec09_method:18` | T2 | `Chapter 1 의 logistic 전이 모델~\eqref{eq:logistic} 을 \emph{동시} 피팅하며` | `Part I 의 logistic 전이 모델~\eqref{eq:logistic} 을 \emph{동시} 피팅하며` | 호칭; `eq:logistic`(Part T) 무변경 |
| `ch2_sec10_closing:8` | T2 | `그것이 Chapter 1 logistic 의 기원임을 보였고($w=RT/F$ 가 분포 폭)` | `그것이 Part I logistic(\S\ref{sec:width})의 기원임을 보였고($w=RT/F$ 가 분포 폭)` | → `ch2_sec10_closing_partT.tex` 초안 반영 |
| `ch2_sec10_closing:13` | T2 | `broadening 기원은 Chapter 1 §7)로 두-상 폭의 지위를,` | `broadening 기원은 Part I \S\ref{sec:broadening})로 두-상 폭의 지위를,` | `sec:broadening`; 초안 반영 |

## 3. T3 전환표 (5건 — Part T → 신 Chapter 2 LCO, xr 장 간)

**주의 — T2 와 방향 반대.** 현행 문면의 "Chapter 1 §13/§14/§15/§17" 은 **구 Ch1 의 LCO 절**(§11~17)로, 신 구조에서 **신 Chapter 2 로 이동**. 대상 라벨은 `ch2_lco_v1.0.22.tex` 가 조립하는 `_sections/ch1_sec13~17.tex` 에서 실확인: `sec:lco-hys`(§13)·`sec:lco-decomp`(§14)·`sec:lco-electronic`(§15, 하위 `sec:lco-Se`)·`sec:lco-code`(§17). `ch1_graphite` 마스터 8행 `\externaldocument{ch2_lco_v1.0.22}` 가 이들을 "2.x" 번호로 해소.

| 파일:행 | 분류 | 현행(해당 부분) | 개정안(LaTeX) | 비고 |
|---|---|---|---|---|
| `ch2_sec00_intro:62` | T3 | `분포 언어의 한 사례로만 포함한다(그 상세 전개는 Chapter 1 §15).` | `분포 언어의 한 사례로만 포함한다(그 상세 전개는 Chapter 2 \S\ref{sec:lco-electronic}).` | §15=`sec:lco-electronic`=`ch1_sec15:4`(신Ch2). xr. 초안 반영 |
| `ch2_sec02_config:128` | T3 | `이 분해는 Chapter 1 §14 의 반응 엔트로피 삼분해$\cdot$슬롯 규칙과,` | `이 분해는 Chapter 2 \S\ref{sec:lco-decomp} 의 반응 엔트로피 삼분해$\cdot$슬롯 규칙과,` | §14=`sec:lco-decomp`=`ch1_sec14:4`(신Ch2). xr |
| `ch2_sec03_vibel:65` | T3 | `는 Chapter 1 §15(LCO 전자 엔트로피)의 전자 엔트로피 유도가 상술했고,` | `는 Chapter 2 \S\ref{sec:lco-electronic}(LCO 전자 엔트로피)의 전자 엔트로피 유도가 상술했고,` | §15=`sec:lco-electronic`; 하위 유도 절 `sec:lco-Se`=`ch1_sec15:72` 도 실존(더 좁게 잡을 옵션) |
| `ch2_sec03_vibel:77` | T3 | `그 전개는 Chapter 1 §13$\cdot$§15 가 상술한다.` | `그 전개는 Chapter 2 \S\ref{sec:lco-hys}$\cdot$\S\ref{sec:lco-electronic} 가 상술한다.` | §13=`sec:lco-hys`=`ch1_sec13:4`, §15=`sec:lco-electronic`(신Ch2). xr |
| `ch2_sec09_method:20` | T3 | `MSMR (Multi-Species, Multi-Reaction) 절차(Chapter 1 §17)와 직접 대응한다` | `MSMR (Multi-Species, Multi-Reaction) 절차(Chapter 2 \S\ref{sec:lco-code})와 직접 대응한다` | §17=`sec:lco-code`=`ch1_sec17:4`(신Ch2). xr |

## 4. 통계 요약

| 분류 | 건수 | 라벨 실확인 | 서술형 `(eq:…)`→`\eqref` | 판단 보류 |
|---|---|---|---|---|
| T1 | 20 | 19/20 live | 5건(`eq:Z1`·`eq:muV`·`eq:implicit`·`eq:Vxi`·`eq:logistic`) | 1건(`ch1_appB:135` — `ch2_appB` 무라벨) |
| T2 | 53 | 53/53 live | 2건(`ch2_appB:25`·`ch2_sec05:23` = `eq:sm-mc-balance`) | 0 |
| T3 | 5 | 5/5 live(xr) | 0 | 0 |
| **계** | **78** | **77/78** | **7** | **1** |

- **live `\S\ref`/`\eqref` 실확인 = 77/78.** 유일 예외 = `ch1_appB:135`(T1-02): 대상 `ch2_appB_codemap` 이 section `\label` 을 갖지 않아 live 참조 불가 → 서술형 개정안 제시 + MISC 코드맵 제목·라벨 신설 확정에 의존(§판단 보류).
- 개정안에 새로 등장하는 라벨 전량이 원문 실존(추측 0). Part T 라벨 vs Part 0/I 라벨 vs LCO 라벨을 파일 단위로 교차 확인.
- 소절/절 제목 변경 2곳(`ch2_sec01:51`·`ch2_sec02:134`)·캡션 3곳(`ch2_sec02:101`·`ch2_sec08:114`, T1 없음)은 TOC/LoF/LoT 연동 → 집행 후 재빌드 3-pass 로 목차 갱신 확인 필요(표기).

## 5. 판단 보류 항목

1. **`ch1_appB:135` "Chapter 2 부록 B" (T1-02)** — `ch2_appB_codemap.tex` 는 `\section*{부록 B --- …}`(비번호·무라벨)이라 live `\S\ref` 대상이 없음. 두 경로:
   (a) 서술형 유지 = 개정안 "열특성 코드 구현 요구명세 부록(부록 B)";
   (b) MISC 코드맵 제목 분업에서 `ch2_appB` 에 `\label{sec:appendix-code-thermal}`(가칭) 신설 + 부록 D 개명 → `요구명세는 부록~\ref{sec:appendix-code-thermal}` 로 live 전환.
   **권고 = (b)**(4부록 letter 충돌도 함께 해소). 라벨 신설은 마스터 집행 사항이므로 O-A 는 (a)를 초안으로 두고 (b)를 MISC 에 제안.
2. **`ch2_sec01:58` s 부호 호칭** — "Chapter 1 의 유도 전용 고정 부호" 를 "본 장의"(장 전역 규약)로 뒀으나, 더 좁히면 `Part 0(\S\ref{sec:sm-electro})`. 규약이 장 전역이라 "본 장" 이 자연스러우나 마스터 재량. (동종: `ch2_sec03:69`·`ch2_sec07:29` 방향 규약 = "본 장의")
3. **정합 추가 후보(스윕 밖 — 실행 아님, 보고만)** — 스윕 패턴이 "Chapter [12]" 라 축약형 "Ch1"·tikz 노드가 미검출: `ch2_sec02:83` tikz 노드 "= Ch1 logistic", `ch2_appA:55` 표셀 "Ch1 ``방전=탈리튬화'' 라벨". 위 T2 개정과 문면 정합을 위해 각각 "Part I logistic"·"본 장 ``방전=탈리튬화''" 로 함께 손보길 권고(추가 후보).

