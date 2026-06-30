# NOTEb — v8-05b 증분 보완 로그 (원본 v8-05.tex·NOTE.md 보존)

> 작업 sub. 방향성만 받아 자율 구현. `v8-05.tex`(82338 B, 미변경) 보존, `v8-05b.tex`(증분)에만 수정.
> ★REVIEW1.md 미열람(지시). git commit 미수행(master 전담).

## 1. 적용한 증분 4건

### (1) ★D-PEAK 정정 — `\S sec:tail`, 차분식 환원 방향 (구 L889 부근)
- **결함**: "`$L_V$ 가 작으면 $\rho\to0$ 이라 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 가 되어 … 종으로 환원된다" — 틀림.
- **물리 정정**(코드·수치 실증):
  - 점화식~`eq:lowpass` 한 줄 대수: 분자 $\xi_{\eq,i}-\xi_{\mathrm{lag},i}=\rho(\xi_{\eq,i}-\xi_{\mathrm{lag},i-1})$.
  - $L_V\to0 \Rightarrow \rho=e^{-\Delta_\mathrm{grid}/L_V}\to0 \Rightarrow \xi_\mathrm{lag}\to\xi_\eq$(원신호 자체, "한 칸 뒤처진" 아님) ⇒ 분자 지수적 소멸, 분모는 로그 규모로만 감소 ⇒ **peak_shape $\to0$ (종 아님)**.
  - **매끈한 환원은 $L_V\gg\Delta_\mathrm{grid}$**($\rho\to1$, $1-\rho\simeq\Delta_\mathrm{grid}/L_V$): 충실한 이산화 ⇒ $r_j/L_V=\dd\xi/\dd V$ 종 수렴.
  - **작은 $L_V$ 평형회복은 `eq:branch` 스위치 담당**(코드 v11_final.py L466–468: `lag_len_V < min_lag_grid_steps*grid_step` 이면 해석 종 `ksi_eq*(1-ksi_eq)/w`).
- **모순 해소**: `eq:branch`(이미 옳음)와 본문 prose 가 이제 일치 — "두 진술은 모순 아니라 역할 분담(매끈=큰 $L_V$, 작은 $L_V$=스위치)" 명문화.

### (2) D-VEQ 다리 마무리 — `\S sec:hys`, 신규 식 `eq:gveqbridge`
- 잔존 부분(평형 조건→$g'(\xi)$ 를 괄호 단정으로만 적음)을 명시 유도로 승급.
- `eq:eqcond` 의 $\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V_\eq-U_j)$ + $\mu_\mathrm{Li}=\partial g/\partial\theta$, $\xi=1-\theta\Rightarrow\partial/\partial\theta=-\partial/\partial\xi$ ⇒ $\mu_\mathrm{Li}-\mu^0=-g'(\xi)$ ⇒ **$g_j'(\xi)=sF(V_{\eq,j}-U_j)$**(식 `eq:gveqbridge`). 이어 `eq:gprime`→`eq:Veq` 흐름이 다리 좌변 대입으로 자연 연결.

### (3) orphan bib 인용 3건
- `dreyer2010` (히스테리시스 열역학 기원) → `\S sec:hys` 도입(L389).
- `bazant2013` (비평형 열역학 Butler–Volmer) → `eq:bv` 도입(L598).
- `eyring1935` (활성 착물 $k_0=k_BT/h$) → `eq:kuniv` 직후(L782).
- 빌드 후 undefined citation = 0. 인용 총 7건(기존 4 + 신규 3).

### (4) ★새 회귀 self-test R5 — verifybox
- 차분식 환원 방향을 falsifiable 수치로 못박음(코드 `_causal_lowpass`+차분식 직접 구동, $w=RT/F$, 해석 종 정점 $1/(4w)=9.730$):
  - $L_V=50\Delta_\mathrm{grid}$($\rho=0.980$): 정점 **9.61** (종의 98.8%).
  - $L_V\to0$($\rho\to0$): 정점 **→0** (종의 0%) — 거짓 진술 falsify.
  - 스위치 문턱 $L_V=2\Delta_\mathrm{grid}$($\rho=0.607$): 정점 **7.50** (종의 77%) — 코드가 이 아래로 해석 종 갈아타는 까닭 수치 확인.

## 2. 부호 8항 재확인 (전건 PASS — 정정이 부호 사슬 미훼손)
1. $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-sFU$ ✔
2. $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$, 방전 $V\uparrow\Rightarrow\xi\uparrow$ ✔
3. $d\xi/dV$ peak $=|\cdot|\ge0$ 방향 불변 ✔ (R5 가 차분식 정점 거동으로 보강)
4. $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$, 분기 $\pm\tfrac12\sigma_d$ ✔ (R1·R2 수치 86.7/0.0 mV 재확인)
5. $\chi_d$ 충전 $1-\chi$, $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ ✔
6. $\partial\ln L_q/\partial V$: 컷 상수라 운영 0, 부등식은 동기 ✔ (R4)
7. 꼬리 충전 격자 역전, 충전 $dQ/dV$ 방전 거울(양수) ✔
8. 분극 $V_n=V_\app-\sigma_d|I|R_n$, 방전 측정$>$내부 ✔

## 3. 빌드 결과
- `xelatex -interaction=nonstopmode -halt-on-error` **2-pass, exit 0 / exit 0**.
- **에러 0, undefined ref/citation 0**, LaTeX Warning(비-rerun) 0.
- Overfull hbox 2건뿐(2.15pt·22.55pt, 표/식 행 — 무해, 기존 유래).
- 산출 **`v8-05b.pdf` (21 pages, 397821 B)**.

## 4. 변경 안 한 것 (보존 확인)
- `v8-05.tex` 원본 미수정(타임스탬프·크기 불변), `NOTE.md` 미수정.
- 결과 박스 식·코드 식별자·부호·절 순서·표·그림 전부 보존 — 추가는 prose 정정 + 다리 식 1개 + R5 1항 + 인용 3건뿐.
- 신규 그림 없음(이번 증분은 텍스트·식·인용·self-test 보완 범위).
