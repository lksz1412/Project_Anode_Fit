# v7-04b 보완 노트 (graphite_ica_ch1 v7 — v7-04 미세 보완본)

산출물: `v7-04b.tex` (원본 `v7-04.tex` 보존, 별도 사본) + `v7-04b.pdf` (16쪽, xelatex 2-pass, 에러 0).
성격: v7-04 는 거의 무결(부호 8/8)이라 **구조·식·그림은 유지**하고, 유일 약점(w^eff 게이트)을 본문·표·코드박스에 명시하는 **미세 보완**만 가함. 보완이 무결 상태를 깨지 않았음을 ★부호회귀 self-test 로 실증.

## 1. 베이스 입력 정독 (head→tail)
| 문건 | 경로 | 정독 |
|---|---|---|
| 내 초본 v7-04 | `Claude/results/v7-04/v7-04.tex` | 전문 1–627 |
| 정본 코드 | `v7-00_spine/Anode_Fit_v11_final.py` | 전문 1–706 |
| 플로우차트(척추) | `v7-00_spine/v11_flowchart.md` | 전문 1–90 |
| 작가 브리프 | `v7-00_spine/AUTHOR_BRIEF.md` | 전문 1–76 |
| (베이스 자체검수 로그) | `Claude/results/v7-04/NOTE.md` | 전문 |
- ★REVIEW1.md 는 지시대로 보지 않음.

## 2. 유일 약점 보완 — w^eff 게이트 (보완 방향 #1)

**사실(코드 정본 대조).** `_width` [L283-288] 는 w^eff 를
`use_weff and tr.get('Omega') is not None and tr.get('w') is None` 일 때만 적용한다.
세 번째 게이트 `tr.get('w') is None` 때문에, **전이 dict 에 `'w'` 키가 하나라도 있으면 `use_w_eff=True`라도 w^eff 좁힘이 실효 없이 우회**되고 폭은 그대로 `nRT/F` 로 평가된다.
`GRAPHITE_STAGING_LIT` [L535-564] 의 네 전이는 모두 `'w'`(0.020/0.016/0.014/0.012)를 싣고 있어, 배포 데이터셋에서 w^eff 는 무효다. 독자가 좁힘을 켜려면 전이 dict 에서 `'w'` 를 빼고 폭을 Ω·n 으로만 줘야 한다.

이 사실을 **네 곳**에 명시(독자가 어느 경로로 읽어도 걸리도록):
1. **§1.5 본문**(eq:weff 직후) — 게이트 차단키 설명 + Ω·n 으로 줘야 켜짐 + §1.9 staging 함정 지목.
2. **§1.5 코드박스** — `_width` 게이트 3조건 명시, ★`tr.get('w') is None` 우회.
3. **N0 기호표 `w` 행** — "dict 에 `'w'` 키 있으면 w^eff 게이트 차단 — §1.5" 인라인 단서.
4. **§1.9 staging 표 직후** — 기존 `'w'` 폴백 문단에 부수효과(w^eff 게이트 차단) 1문단 추가.
5. **§1.9 G-usable step (3)** — 폭 항을 `w=nRT/F (w^eff 는 'w' 키 없을 때만 발동)` 로 명료화(재현 코드 정확성).

## 3. 그 외 통독 다듬기 (보완 방향 #2)
- 파일 헤더 주석을 v7-04b 로 갱신 + [v7-04→v7-04b 보완] 변경요약 3줄 추가. pdftitle v7-04b.
- N0–N9·G-usable 6step·그림 5종·부호 사슬·환원 검산은 **불변**(식·라벨·번호 그대로). 표층 라운드(조사만 바꿈) 금지 원칙에 따라 추가 손질은 의미 개선이 확실한 위 게이트 명시로 한정.

## 4. §8 부호 체크리스트 — 전건 재확인 (코드 v11 대조, 전건 PASS)
| # | 항목 | 코드 | 결과 |
|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU | func_U_j L68 | ✓ |
| 2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | func_ksi_eq L84 | ✓ |
| 3 | dξ/dV=σ_d ξ(1−ξ)/w, peak 양수(방향 불변) | L468/L370 | ✓ |
| 4 | ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | func_dU_hys L123, func_U_branch L133 | ✓ |
| 5 | χ_d(방전 χ/충전 1−χ), ΔH_a^eff=ΔH_a−χ_d Ω | func_chi_d L155, func_dH_a_eff L149 | ✓ |
| 6 | ∂lnL_q/∂V<0 (V↑→장벽↓→꼬리↓) | func_L_q L90 | ✓ |
| 7 | 충전 격자 역전 ξ[::-1]…[::-1], 충전=방전 거울·양수 | L474-477 | ✓ |
| 8 | V_n=V_app−σ_d|I|R_n | L412 | ✓ |

보완은 **부호 흐름에 손대지 않음**(폭 평가 경로의 게이트 사실만 명시) → 8건 전건 불변.

## 5. ★새 부호회귀 self-test (보완이 무결을 깨지 않았는지 실증)
스크립트: scratchpad `sign_regression_v7-04b.py` — v11 정본을 import 해 직접 검증.
- §8 부호 8건: 1~8 전부 PASS (U(298)~0.085, 방전 V↑→ξ↑, peak 양수, ΔU_hys≥0·Ω≤2RT→0·dis>chg, χ_d split·ΔH_a^eff, 깊은 affinity→짧은 L_q, 충전 꼬리 양수, V_n 식).
- ★새 w^eff 게이트 주장 직접 검증:
  - (a) staging('w' 보유): `use_w_eff` on==off → 폭이 nRT/F 로 동일(게이트 차단) — PASS.
  - (b) `'w'` 제거(Ω·n 만): w^eff 활성·RT/F 미만으로 좁아짐 — PASS.
  - (c) staging 모델 end-to-end 유한 — PASS.
- **RESULT: ALL PASS** (11/11). 보완의 핵심 주장이 코드 사실과 일치(text-only 보완이 무결 상태 불변).

## 6. 빌드 결과
- `xelatex -interaction=nonstopmode -halt-on-error` 2-pass (MiKTeX). pass1·pass2 exit 0.
- v7-04b.pdf 16쪽, 331 KB. **에러 0 · undefined cross-reference 0 · Missing $ 0 · 50pt 초과 overfull 0.**
- 라벨 감사(python): 정의 44 = 참조 44, **orphan ref 0 · 미참조 0** — 내가 추가한 `\S\ref{sec:width}`·`\eqref{eq:weff}` 전부 resolve.
- 잔여 경고 = 폰트 italic shape 대체 3건(UnBatang/D2Coding it 미정의 → upright) — 베이스와 동일 무해 경고.
- PDF 육안 확인: §1.5(p.9)·§1.9 staging('w' 부수효과 문단, p.15)·G-usable step(3)·맺음(p.16) 정상 렌더. 그림 5종·boxed eq·코드박스 깨짐 0.

## 7. Decision Queue
- 헤더 "N/M" 표기(예 16/14)는 `\pageref{LastPage}` 가 2-pass 에서 본문 마지막 전에 평가돼 생기는 베이스 v7-04 의 기존 quirk(내 보완 무관). 추가 손질은 원본 보존·범위 최소 원칙상 보류(원하면 별도 1줄 수정 가능).
- 브리프 §3 권장 절순서(N6→N3) vs 플로우차트(N3→N6) 충돌은 베이스에서 이미 척추(코드 진행) 채택으로 종결 — 재론 안 함.
