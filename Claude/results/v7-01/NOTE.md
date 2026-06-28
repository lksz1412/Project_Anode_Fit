# NOTE.md — v7-01 자체 검수 기록

## 1. Read Coverage

| 문서 | 범위 | 방법 |
|------|------|------|
| AUTHOR_BRIEF.md | 전문 (§0–§9) | 순차 정독 |
| v11_flowchart.md | 전문 (N0–N9 + baseline) | 순차 정독 |
| Anode_Fit_v11_final.py | 전문 (L1–L706) | 순차 정독 (5-청크) |
| graphite_ica_ch1_Opus_v5.tex | 전문 (L1–L1883) | 순차 정독 (5-청크) |

Python 코드 주요 라인 커버:
- L64 func_w, L68 func_U_j, L84 func_ksi_eq, L90 func_L_q, L100 _causal_lowpass
- L123 func_dU_hys, L133 func_U_branch, L141 func_w_eff, L149 func_dH_a_eff, L155 func_chi_d
- L283 _width, L291 _chi_d, L307 _resolve_lag_length, L335 A_cap, L346 L_q, L351 L_V
- L354 equilibrium, L412 V_n, L419 V_work, L438 U_j, L451–L452 hys/center
- L459 ksi_eq, L463–L468 lag/eq 분기, L474–L479 충전 역전+peak_shape
- L481 dqdv_work, L483 interp, L535–L564 GRAPHITE_STAGING_LIT

---

## 2. 10-라운드 검수 결함 추이

| R# | 청크 스킴 | 렌즈 | 결함 수 | 결함 내용 |
|----|----------|------|--------|----------|
| R1 | 통독 | 구조/완결성 | 0 | 절 순서 코드 진행 정합 (N3→N4+N5 이 코드 L451→L459 와 일치) |
| R2 | 수식별 8항 | 부호 사슬 전건 | 0 | σ_d·χ_d·ΔU_hys·IIR·역전 전건 8항 모두 정합 |
| R3 | 함수/라인별 | 코드 식별자 | 0 | 모든 함수·라인 번호 v11_final 1:1 대응 확인 |
| R4 | 절별 도입/마무리 | G-follow | 1 | N4+N5 절 도입 문장 없음 → 추가 |
| R5 | 식별 사슬 전체 | G-usable | 1 | z_cut=4.357, A_cap=4.0 RT 기본값 미명시 → 추가 |
| R6 | 핵심 수식 물리 | 적대 검산 | 0 | L_q 유도 코드 지수 대조 정합 |
| R7 | TikZ 라인별 | 언어/표기 | 1 | figure 내부 한글 4곳 → 영어 ASCII 변환 |
| R8 | 정규용액·spinodal | 도메인 물리 | 1 | "방전은 ξ_{s}^- 까지" 오류 → ξ_{s}^+(대값)로 정정 |
| R9 | 직전 수정 재점검 | 새 결함 탐지 | 0 | \left.\right|_{\max} 패턴 빌드 통과, 기능 정합 |
| R10 | 완결성 전수 | orphan/ref | 1 | figure 4종 본문 \ref 없음 → 추가 |

누적 결함: R1–R3 = 0, R4 = +1, R5 = +1, R6 = 0, R7 = +1, R8 = +1, R9 = 0, R10 = +1 → 총 5건 수정

수렴 판정: R8 이후 추가 라운드(R9, R10)에서 직전 수정 연관 결함 없음.
R9=0, R10=1(ref orphan) → R10 수정 후 재검(연속 2R = 0 달성 확인 필요).

추가 R11 (R10 수정 반영 후):
- figure \ref 추가 후 orphan 없음 ✓
- z_cut/A_cap 문구 추가 문법 이상 없음 ✓
- spinodal 방향 수정 물리 재검: 방전(탈리튬화, ξ↑)은 ξ_{s}^+ = 1/2 + u/2 (대값)까지 과주행 ✓
→ R11 = 0

추가 R12:
- 전체 수식 번호 1.1–1.28 단조 누락 없음 ✓
- \label 중복 없음 ✓
- thebibliography 인용 순서 ✓
→ R12 = 0

연속 2R (R11, R12) = 0결함 → **수렴 달성**

---

## 3. 부호 사슬 체크리스트 (AUTHOR_BRIEF §8)

| 항목 | 검산 결과 |
|------|----------|
| (1) U_j = (-ΔH + TΔS)/F, ΔH<0 → U_j>0 | 식 (1.3) + 수치 예 (stage 2→1, 0.085V) ✓ |
| (2) ξ_eq = logistic[σ_d(V_n−U^d)/w], 방전 V_n↑ → ξ_eq↑ | 식 (1.11), 부호 검산 소절 ✓ |
| (3) dξ_eq/dV_n = σ_d·ξ(1−ξ)/w, 방향 불변 양수 | 식 (1.10) + 서론 핵심 부호 사슬 ✓ |
| (4) ΔU_hys ≥ 0, Ω ≤ 2RT → 0 | 식 (1.7), 코드 func_dU_hys ✓ |
| (5) χ_d: 방전 χ / 충전 1−χ; ΔH_a^eff = ΔH_a − χ_d·Ω | 식 (1.16), (1.18) ✓ |
| (6) ∂ln L_q/∂V_n < 0 (구동 깊을수록 꼬리 감소) | 식 (1.21) ✓ |
| (7) 충전 격자역전 후 dQ/dV 양수 유지 | 식 (1.26) + 코드 verbatim ✓ |
| (8) 분극: V_n = V_app − σ_d|I|R_n | 식 (1.2) ✓ |

전건 8항 모두 문건 내 명시적 수식으로 충족.

---

## 4. 그림 목록

| 레이블 | 위치 | 이유 |
|--------|------|------|
| fig:flowchart | 서론 | N0→N9 계산 진행 전체를 한 눈에 보여줘야 독자가 절 순서를 맥락화할 수 있음 |
| fig:polshift | N1 분극 보정 | 분극이 peak를 이동시키는 방향·크기를 시각적으로 확인, σ_d 부호 직관 |
| fig:logistic | N4+N5 점유율 | logistic 형태와 미분(bell curve)이 dQ/dV peak 의 원형임을 보여줌 |
| fig:tail | N8 인과 기억 꼬리 | 평형 기준선 vs 동역학 꼬리의 형태 차이, L_V 크기의 시각적 의미 |

---

## 5. 빌드 결과

- 컴파일러: xelatex (MiKTeX)
- 패스 수: 3회 (1회째 상호참조 미완, 2회째 안정, 3회째 수정 후 2회)
- LaTeX `!` 오류 수: **0**
- 경고: Underfull \hbox (참고문헌 일부), MiKTeX 업데이트 경고 (기능 무관)
- PDF: v7-01.pdf, **15페이지**, 동일 폴더

---

## 6. 특이사항

- fig:flowchart 노드 내 한글이 R7 에서 발견되어 영어 ASCII로 전환.
- R8 에서 spinodal 과주행 방향 오류 발견: 방전은 ξ_{s}^- (소값)이 아니라 ξ_{s}^+ (대값)까지 과주행함 → 물리 정정.
- BRIEF §3의 명목 순서(N4+N5→N6→N3)와 코드 실행 순서(N3→N4+N5)가 다름. 코드 L451(hys_shift) → L459(ksi_eq) 순서에 따라 현 문건 순서(N3 먼저)가 더 옳다고 판단 — 유지.
- `\left.\frac{...}\right|_{\max}^\mathrm{net}` 수식 수정으로 align 환경 내 결함 해소.
