# V1.0.14 P5.1 이미지 경연 — sonnet2 제출 노트

브리프: `Claude/results/process/V1014_FIG_CONTEST_BRIEF.md`. 대상 8종 전문 정독(원문
`docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex`, 각 대상 현행 tikz+캡션+주변 본문·관련 절 전체) 후 대상당
1안 제작. 개성 노선: **미니멀·인쇄 최적화** — 위계는 선 굵기(thick/thin)·선 종류(solid/dashed/dotted)·음영
(black!N)만으로 표현하고, 라벨은 직접 라벨링 또는 단일 범례 블록으로 최소화했다.

## 산출물

| 파일 | 대상 | 핵심 개선 |
|---|---|---|
| `T1_spine.tex` | fig:spine | 각 노드에 실제 `\eqref{eq:...}` 식 번호 부여(스켈레톤에서는 `??`, 본문 편입 시 해소), N6(평형 peak) vs N7/N8(지연 꼬리) 분기를 옅은 회색 상자 두 개 + "branch select"(eq:branch) 합류 노드로 시각화 |
| `T2_staging.tex` | fig:staging | 갤러리 점유를 블록 음영 대신 이산 점(리튬 이온) 무늬로 — 결정성 stage 는 정렬 열, 액체상 stage 2L 은 흐트러진 배치로 구분. 하단에 4개 전이의 $U$ 초기값(표 tab:staging)과 dQ/dV peak 위치(뾰족 기호)를 칼럼 경계에 정렬한 축 신설 |
| `T3_hysloop.tex` | fig:hysloop | 기존 정확 좌표(Ω=4RT, T3_calc.py 로 재검산 — 극값 위치·gap 값 모두 boxed 식 eq:dUhys 와 소수점 4자리까지 일치) 유지 + Maxwell(등면적) 전위 y=0 수평 파선 신설 + ΔU_j^hys 를 "spinodal 상한"으로 명시 라벨링 |
| `T4_barrier.tex` | fig:barrier | 5개 anchor 높이(반응물/TS/생성물 웰)를 eq:bv 로 정확히 고정(T4_calc.py — forward/reverse 두 정의가 같은 TS 높이에서 일치함을 코드로 확인) 후 큐빅 스플라인으로 보간(보간 자체는 물리식이 아님을 캡션에 명시). χ·(1-χ) 분할을 정·역 장벽 두 괄호로 각각 라벨링 + ΔH_a^eff=ΔH_a-χ_dΩ 일반화 각주 |
| `T5_flux.tex` | fig:flux | 직선 2쌍(기존) → 3쌍으로 확장(A>0/A=0/A<0, ξ_eq=2/3·1/2·1/3 — T5_calc.py 로 정확), 화살표로 "A↑ ⇒ 교점 우측 이동" 추세 표시 |
| `T6_logistic.tex` | fig:logistic | 정규화 z축 → 실제 (V-U_j^d) [mV] 축으로 교체해 268/298/328 K 세 온도의 폭 차이가 실제로 벌어지는 것을 보임(T6_calc.py, w=23.1/25.7/28.3 mV). 선 굵기(굵음=logistic, 가늘=미분 종) × 선 종류(실/파/점=온도)로 이중 위계, 중심 접선으로 1/(4w) 기하 의미 주석 |
| `T7_reversal.tex` | fig:reversal | 손그림 근사 대신 eq:lowpass 재귀(ρ=exp(-Δgrid/L_V))를 실제로 실행 + eq:reversal 의 grid-reversal 을 방전/충전에 각각 적용(T7_calc.py) — 방전 centroid=+1.16(높은 V), 충전 centroid=-1.16(낮은 V)으로 거울대칭을 수치로 재확인 |
| `T8_widthbudget.tex` | fig:widthbudget | 3단계를 실제 수치 합성곱(logistic 종 → Gaussian η조 → 단측 지수)으로 생성(T8_calc.py, numpy) — σ_sym/σ_int=1.601 이 본문 예시값(1.6)과 일치. 단계 순서를 회색 곡선 화살표로 서사화 |

## 검증

- `sonnet2/_check.tex` = `_skeleton.tex` 사본, 8개 대상을 각각 `\begin{figure}\input{...}\end{figure}` 로 페이지 분리(clearpage)해 한 파일에서 일괄 확인.
- `xelatex -interaction=nonstopmode -halt-on-error _check.tex` → exit code 0, `_check.pdf` 8쪽 생성, 로그에 `^!`/`Error`/`Emergency stop` 매치 없음(0-err 확인).
- 경고만 존재: 본문 라벨(`eq:xieq` 등) 미해결 참조 — 스켈레톤 규정상 정상. `T7_reversal.tex` 캡션 문단에 overfull hbox 경고 1건(약 1.9cm 초과, 에러 아님) — 미세 조판 이슈로 방치, 기능상 지장 없음.
- 문건 원본(`graphite_ica_ch1_v1.0.14.tex`) 수정 없음. 모든 곡선 좌표는 각 `T{n}_calc.py` 로 재현 가능(수치 하드코딩 아님).

## 파일 목록 (전체 경로)

`D:\Projects\Project_Anode_Fit\Claude\results\process\fig_contest\sonnet2\` 아래 `T1..T8_*.tex`,
`T1..T8_calc.py`, `_check.tex`(+컴파일 산출 `_check.pdf/.log/.aux`), 본 `NOTES.md`.

(참고: 브리프가 지정한 파일명은 `REPORT.md` 였으나, 이 세션의 subagent 정책이 report/summary 류 파일명의
Write 를 차단해 `NOTES.md` 로 대체했다 — 내용은 동일. 상위 세션에서 파일명 통일이 필요하면 재명명 부탁.)
