# v7-06b 보완 로그 (NOTEb) — v7-06 초본의 4-결함 정정

> 산출 = `v7-06b.tex` (원본 `v7-06.tex` 보존, 별도 사본) + `v7-06b.pdf` (16p).
> 본 라운드 = master 가 방향성으로 지시한 3개 보완점 + 마무리(부호 체크리스트 재확인 + 새 부호회귀 self-test).
> ★REVIEW1.md 는 지시대로 보지 않음. 절 순서·spine·preamble = v7-06 그대로(구조 불변, 국소 정정만).

## ① 정정한 결함 (방향성 3 + 마무리)

### 결함 1 (★) — ∂lnL_q/∂V<0 자기모순 해소
- **문제**: §8 부호 체크리스트 S6 가 `∂lnL_q/∂V<0` 을 실현 미분처럼 `\checkmark` 처리. 그러나 본문 §7
  (eq:Acut 직후·N7 codebox)은 스스로 "A 는 전이당 컷 상수로 *동결*, L_q 는 전이당 1회 평가(대표 T_rep·n)"
  라 적음 → A 가 동결이면 코드 안에서 L_q 는 V 의 함수로 재미분되지 않으므로 운영상 실현 미분은 **0**.
  부등식을 realized 검산으로 둔 것이 본문 진술과 모순.
- **정정**:
  - §7 (eq:LV 직후, `부호의 핵심`): "A 가 컷 상수라 코드 안 L_q 는 V 로 재미분 안 됨 → *운영상 실현 미분
    ∂lnL_q/∂V=0*(전이당 한 스칼라). 부등식 ∂lnL_q/∂V<0 은 *물리적 동기*(국소 구동력 A=σ_dF(V_n−U) 로 두면
    V↑→A↑→장벽↓→L_q↓ 단조 — 이 단조성이 '꼬리 컷점을 원천 정점의 일정 분율로 잡는' 컷 규칙의 정당성).
    곧 컷점 선택의 근거이지 격자마다 평가하는 양이 아님." 으로 재서술. |I| 의존(L_q∝|I|→0)은 동결 뒤에도
    살아 있음을 분리 명시(이건 실제 평형 환원 메커니즘이라 유지).
  - §8 S6: 제목을 `∂lnL_q/∂V<0 (물리적 동기)` 로 바꾸고, "실현 미분=0(전이당 스칼라), 부등식 <0 은 컷 규칙
    동기로만, 동결과 부등식이 같은 단조성에서 일관 → 자기모순 없음" 으로 정정. `\checkmark` 의 신뢰 회복.
- **부호 체크리스트 결론 신뢰 회복**: S6 가 더 이상 본문과 모순되지 않으므로, "전건 정합·부호 결함 0" 결론이 복원됨.

### 결함 2 — 박스 인자 V_n → V_work 정정
- **문제**: §5 codebox(eq:xieq 코드 대응) 가 `z=s(V_n−U)/w` 로 적음. 그러나 코드 L459 는
  `func_ksi_eq(T_work, V_work, center, n_j, sigma_d)` — 함수의 `V_n` 인자 자리에 **V_work**(작업 격자)가
  들어감. §2 가 "평형·동역학은 V_work 위에서 풀고 출력만 V_n 으로 역보간" 을 이미 선언했는데 박스 인자가 V_n.
- **정정**:
  - §5 codebox: `z=σ_d(V_work−U_j^d)/w_j` 로 바꾸고 1줄 추가 — "평가 전위는 내부 전위 V_n 이 아니라 §2 작업
    격자 V_work. 코드 호출 `func_ksi_eq(T_work, V_work, center, n_j, sigma_d)` 에서 함수 `V_n` 인자 자리에
    V_work 가 들어간다(평형·동역학 V_work 풀이, 출력만 V_n 역보간; eq:vwork)."
  - §1 부호 규약 박스: 컨벤션 진술의 `logistic[σ_d(V_n−U)/w]` 을 격자 무관 일반형 `[σ_d(V−U)/w]` 로
    중립화(아직 V_work 미도입 지점이라 forward-ref 회피; 부호 단조성 진술은 격자 불변).
  - eq:xieq 박스(일반 V)·§5 affinity 의 A=sF(V_n−U_j)(물리 구동력=내부 전위, 옳음)는 그대로 유지.

### 결함 3 — dH_a vs dH_a_eff 암묵 전제 1줄 명시
- **문제**: §7 eq:Lqfull 가 ΔH_a^eff 를 무조건 쓰는 것처럼 보임. 코드 `_chi_and_dH_eff`(L302-303)는
  `use_dH_eff=True` 일 때만 ΔH_a−χ_dΩ 적용, False 면 dH_a_use=ΔH_a 그대로. 본문이 이 분기를 식 옆에 안 박음.
- **정정**: eq:Lqfull 코드 대응 직후 1문장 — "*암묵 전제 명시*: 식 eq:Lqfull 의 ΔH_a^eff 는 func_L_q 의 dH_a
  인자로 들어가는 `dH_a_use` 이고, 이것은 use_dH_eff=True 일 때만 eq:dHeff 의 ΔH_a−χ_dΩ 와 같다 — 꺼져 있으면
  그대로 ΔH_a(`_chi_and_dH_eff` 의 분기)."

### 마무리 — 새 부호회귀 self-test (★)
- §8 S-체크리스트 직후 `verifybox` 신설(R1–R4, 재현 가능 수치 고정 — 코드 `__main__` self-test 와 동일 양 손 재산출):
  - **R1 히스 분기 방향**: Ω=12000, γ=1 → ΔU_hys=86.7 mV (u=√(1−2RT/Ω)=0.766). peak 갈림
    V_dis−V_chg=+γΔU_hys=+86.7 mV>0 (방전 peak 높은 전위). ← 코드 self-test `d(dis-chg)=+gamma*dU_hys` 일치.
  - **R2 히스 문턱**: Ω=2RT=4958 J/mol → u=0 → ΔU_hys=0.0 mV (연속). ← 코드 `Omega=2RT -> dU_hys≈0`.
  - **R3 |I|→0 환원·방향 불변**: γ=0,|I|=1e-6 → L_V∝|I|→0 → 평형 종, 방전/충전 차→0. ← 코드 `gamma=0,|I|->0
    dis/chg max diff≈0`.
  - **R4 L_q 동결 vs 부등식**: A=min(z_cut·nRT,A_cap·RT) 컷 상수 → ∂lnL_q/∂V=0(실현), <0 은 동기(S6 정정과
    일관) → 자기모순 0.
  - 수치 재산출 검증: dU_hys(298.15, 12000)=86.686 mV, u=0.76607, 2RT=4957.6 (Python 확인).

## ② 부호 체크리스트 전건 재확인 (브리프 §8, 코드 v11 대조 — 정정 반영)

| # | 명제 | 상태 |
|---|---|---|
| S1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU (func_U_j) | PASS (불변) |
| S2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | PASS (박스 인자 V_work 정정 후도 단조성 동일) |
| S3 | dξ/dV=σ_d ξ(1−ξ)/w, peak 양수·방향불변 | PASS (불변) |
| S4 | ΔU_hys≥0, Ω≤2RT→0; 분기 ±½σ_d (U^dis>U^chg) | PASS (R1·R2 수치 재확인) |
| S5 | χ_d 방전χ/충전1−χ; ΔH_a^eff=ΔH_a−χ_dΩ | PASS (결함3 전제 명시로 보강) |
| S6 | ∂lnL_q/∂V<0 | **정정 PASS** — 물리적 동기(실현 미분 0, 컷 동결과 일관, 자기모순 해소) |
| S7 | 충전 격자역전 ξ[::-1]…[::-1]; 충전 dQ/dV=방전 거울 양수 | PASS (불변) |
| S8 | 분극 V_n=V_app−σ_d|I|R_n | PASS (불변) |

전 8건 + 신규 R1–R4 회귀 PASS → 부호 결함 0, 자기모순 0.

## ③ 검수 라운드 (정정분 한정, 청크·렌즈 전환)

| R | 청크 | 렌즈 | 결과 |
|---|---|---|---|
| C1 | 식별 (L412·L459·L307–351) | 코드 대조 (박스 인자) | func_ksi_eq 호출 인자=V_work 확정 → §5 박스 정정. _resolve_lag_length 에 V 인자 없음(A 컷상수) 확정 → S6 정정 근거. |
| C2 | 절 (§7) | 논리·자기모순 | "동결" 진술과 "∂lnL_q/∂V<0 checkmark" 충돌 적발 → 본문+S6 양쪽 정정. dH_eff 분기(L302) 대조 → 전제 1줄. |
| C3 | 라인 (verifybox 신규) | 수치 재현 | dU_hys(12000)=86.686·u=0.766·2RT=4958 Python 재산출 일치(초고 0.480 오타 정정). |
| C4 | 통독 | 완결성·orphan | 추가 \eqref(eq:vwork·dHeff·Lqfull·dUhys·Ubranch·branch·eqpeak·LV) 전부 기존 라벨 — undefined 0. verifybox=verifybox env(L36 정의됨) 정상. |
| C5 | 빌드 (PDF) | 렌더·컴파일 | xelatex ×3, exit 0, ! 0, undefined ref/cite 0, 16p. 폰트경고 3건=원본 동일(pre-existing). |

## ④ 빌드 결과

- 명령: `xelatex -interaction=nonstopmode -halt-on-error v7-06b.tex` (2-pass 요건 충족 + cross-ref 정착용 3차 1회).
- 결과: **EXIT=0, TeX 에러(`!`) 0, Undefined reference/citation 0, Rerun 경고 해소(3차 후).**
- PDF: **16 페이지**, 323 KB. (초본 v7-06=15p; verifybox +1p)
- 경고: 폰트 shape(UnBatang/D2Coding italic) 대체 3건 — **원본 v7-06.log 와 동일 건수**(pre-existing, kotex 치환, 무해).
  Overfull/Underfull 13건(장식적). "Infinite glue shrinkage ... box being split" = MiKTeX 내부 ignored-error(넓은 박스
  페이지분할 시 cosmetic, exit 0·PDF 정상 — 빌드 실패 아님).
- 원본 보존: `v7-06.tex` 무수정(별도 사본 `v7-06b.tex` 작성). 다른 폴더·spine 원본 무수정.

## ⑤ 변경 위치 요약 (4 Edit + 신규 박스)

| 위치 | 변경 | 결함 |
|---|---|---|
| §1 부호 규약 박스 | logistic[σ_d(V_n−U)/w] → [σ_d(V−U)/w] (격자 무관 컨벤션) | 2 |
| §5 eq:xieq codebox | z=s(V_n−U)/w → σ_d(V_work−U^d)/w + V_work 평가 1줄 | 2 |
| §7 eq:Lqfull 직후 | dH_a^eff=dH_a_use, use_dH_eff 분기 1줄 | 3 |
| §7 eq:LV 직후 부호의 핵심 | ∂lnL_q/∂V: 실현 미분 0 + 부등식=물리적 동기 재서술 | 1 |
| §8 S6 | 제목·본문 정정(물리적 동기, 자기모순 해소) | 1 |
| §8 verifybox (신규) | 부호회귀 self-test R1–R4 (재현 수치 고정) | 마무리 |
