# NOTEb — v8-06b 증분 보완 (v8-06.tex → v8-06b.tex)

원본 `v8-06.tex` 보존, `v8-06b.tex` 로 증분 작성. KNOWN_DEFECTS 5종(VEQ·DHEFF·WEFF·UBR·VN)은 v8-06 에서 이미 해소 — 유지·미수정. 본 라운드 = **D-PEAK** + **orphan bib** 두 결함 마감.

## 1. D-PEAK 정정 (핵심) — 두 곳

오개념: "L_V 작으면 ξ_lag→한 칸 뒤처진 ξ_eq ⇒ peak_shape 가 평형 종으로 매끈히 환원". 틀림.
- ρ=exp(−Δgrid/L_V). **L_V→0 ⇒ ρ→0 ⇒ ξ_lag→ξ_eq(같은 칸, 한 칸 지연 아님)** ⇒ 분자(ξ_eq−ξ_lag)→0 과 분모 L_V→0 이 함께 사라지는 **0/0** — 종으로 매끈히 환원되지 않음.
- 매끈한 차분 (ξ_eq−ξ_lag)/L_V → dξ_eq/dV 수렴은 **반대 극한 L_V≫Δgrid (ρ→1, 커널이 진짜 미분)** 에서 성립.
- 작은 L_V 평형 회복은 식의 극한이 아니라 **코드 분기 스위치(eq:branch, L_V<νΔgrid ⇒ eq:eqpeak 직접)** 가 담당. (코드 L466–479 정합: `if lag_len_V < min_lag_grid_steps*grid_step → ξ_eq(1−ξ_eq)/w`.)

수정 위치:
- **(a) fig:relaxode 캡션** (구 L915–917): 오개념 문장 제거 → 그림이 그리는 영역=L_V≫Δgrid 명시 + 작은 L_V 환원은 분기 스위치 담당으로 정정.
- **(b) §peak_shape 본문** (구 L933–934): ρ 두 극한 대비(L_V≫Δgrid ρ→1 매끈 미분 / L_V→0 ρ→0 같은 칸 0/0)로 재서술, eq:branch 가 작은 L_V 환원을 강제함을 본문에서 닫음.

## 2. Orphan bib 인용 (3건) — 모두 본문 인용처 확보
- `eyring1935` → §width Eyring 속도식 (a) 출발 지점.
- `bazant2013` → §width eq:bv 비대칭 장벽(비평형 열역학 기반 전하전달 동역학) 지점.
- `dreyer2010` → §hys 절 도입(삽입형 전극 히스테리시스의 열역학적 기원).
- 검증: `\cite` 7키 전부 `\bibitem` 존재, orphan 0, 빌드 undefined citation 0.

## 3. 새 회귀 self-test (R5 추가)
verifybox 에 **R5 (D-PEAK 회귀)** 추가: ρ 두 극한의 부호 대비를 반증 가능 항으로 못박음("L_V 작으면 식이 종으로 환원" = 거짓, ρ 부호 뒤집으면 깨짐). 마무리 "네 항"→"다섯 항".

## 4. 부호 8항 재확인 (S1–S8, 변경 없음 — 정합 유지)
U_j=(−ΔH+TΔS)/F·ΔG=−FU ✓ / ξ_eq=logistic[σ_d(V−U)/w] 방전 V↑→ξ↑ ✓ / dξ/dV peak |·|≥0 방향불변 ✓ / ΔU_hys≥0·Ω≤2RT→0·분기 ±½σ_d ✓ / χ_d 충전 1−χ·ΔH_a^eff=ΔH_a−χ_dΩ ✓ / ∂lnL_q/∂V 운영 0(부등식=동기) ✓ / 꼬리 충전 격자역전·충전 거울 양수 ✓ / V_n=V_app−σ_d|I|R_n ✓. → 부호 결함 0.

## 5. Read Coverage
- v8-06.tex 전문(1–1182, 3창) / v11_final.py 관련 심볼(_causal_lowpass·_resolve_lag_length·dqdv L412–481 분기) / v7-11.tex 환원 서술 grep 대조 / AUTHOR_BRIEF_v8.md 전문. (★REVIEW1.md 미열람 — 지시 준수.)

## 6. 빌드
xelatex 2-pass(+교차참조 정착 3rd) `-interaction=nonstopmode` → **exit 0·TeX error 0·undefined ref/citation 0**. `v8-06b.pdf` 21p, 399 KB. 잔여 경고 = 한글 폰트 italic 폴백 3건(UnBatang/D2Coding 무이탤릭, cosmetic, 빌드 무영향).

## 7. 산출물
- `v8-06b.tex` (원본 v8-06.tex 보존·증분)
- `v8-06b.pdf` (21p)
- `NOTEb.md` (본 파일)
