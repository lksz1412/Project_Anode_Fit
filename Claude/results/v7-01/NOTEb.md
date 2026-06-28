# NOTEb.md — v7-01b 보완 내역 (2026-06-29)

## 보완 항목

### 1. N7 동역학 절: A_j 재정의 (주요 수정)

**원본 v7-01 오류**: `§6.5 전위 의존` 소절에서 A = sF(V_n − U_j) 로 서술, ∂lnL_q/∂V < 0 을 코드 구현으로 주장.

**실제 코드 (L335)**:
```python
A = float(min(z_cut * n_safe * R * T, A_cap * R * T))
```
A_j 는 전이당 상수(z_cut·n·RT 와 A_cap·RT 중 소값). 전위 V_n에 의존하지 않음.
또한 L_q는 전이당 1회 평가(L463: `T_rep` 스칼라로 호출). 전위 격자별 L_V 아님.

**v7-01b 수정**:
- `§7.2 컷 affinity: 전이당 상수 A_j` 소절 신설, 식 (eq:Aj) 박스형으로 명시.
- `∂lnL_q/∂V < 0` 를 `§7.6 물리적 동기 단락`으로 격하, 코드 구현이 아닌 BV 동기임을 명시.
- 검증절 §9.1 항목 6 재정의: "A_j = 전이당 상수; L_q 는 전위 독립 스칼라"로 교체.

### 2. 닫힌형 L_q 식에 −TΔS_a 항 추가 (eq:Lq)

**원본 v7-01 오류**: eq:Lq 에서 지수 인수를 `(ΔH_a^eff − χ_d A_j)/RT` 로만 씀.

**실제 코드 (L95-96)**:
```python
dG_a = dH_a - T * dS_a
ln_Lq = ... + dG_a / (R * T) - x * A / (R * T)
```
`dG_a = dH_a - T·dS_a` = ΔG_a^eff = ΔH_a^eff − T·ΔS_a 가 지수에 들어감.

**v7-01b 수정**:
- 기호표에 ΔG_{a,j} = ΔH_{a,j} − TΔS_{a,j} 및 ΔG_{a,j}^eff = ΔH_{a,j}^eff − TΔS_{a,j} 행 추가.
- `§7.4 유효 활성화 엔탈피와 자유에너지` 소절로 분리, eq:dGeff 신설.
- eq:kuniv: 지수 인수를 ΔG_{a,j}^eff − χ_d A_j 로 교체.
- eq:Lq (닫힌형): 지수 인수를 (ΔG_{a,j}^eff − χ_d A_j)/RT 로 수정. 코드 구현 명시.
- eq:lnLq (로그형): ΔH_a^eff/RT − ΔS_a/R 두 항으로 명시 분리(절편 b_j 정의와 정합).

### 3. S3 피팅 식별 경로 수정

**원본 v7-01 오류**: S3 에서 `∂lnL_q/∂V_n ≈ −χ_d F/RT` 기울기로 χ 식별. A 가 전위의존이 없으므로 이 식 성립 안 함.

**v7-01b 수정**: S3 를 전이 간 비교법으로 교체 — eq:S3chi: 두 전이 j, j'의 lnL_V 차에서 χ_d(A_j − A_j') 의 기여를 분리.

## 부호 사슬 체크리스트 전건 재확인 (브리프 §8)

| # | 체크 항목 | 상태 |
|---|-----------|------|
| 1 | U_j = (−ΔH + TΔS)/F; ΔH<0 → U_j>0 | PASS — eq:Uj 정합 |
| 2 | ξ_eq = logistic[σ_d(V_n−U)/w]; 방전 V↑→ξ↑ | PASS — eq:ksi_eq 정합 |
| 3 | dξ/dV = σ_d ξ(1−ξ)/w — 방향 불변 양수 | PASS — eq:dxidV 정합 |
| 4 | ΔU_hys ≥ 0; Ω≤2RT → 0. 분기중심 ±½σ_d… | PASS — eq:dUhys, eq:Ubranch 정합 |
| 5 | χ_d: 방전 χ / 충전 1−χ. ΔH_a^eff = ΔH_a − χ_dΩ | PASS — eq:chid, eq:dHeff 정합 |
| 6 | A_j 전이당 상수 (z_cut·n·RT 컷); L_q 전위 독립 | PASS — eq:Aj 신설로 코드 정합 |
| 7 | 충전 격자역전; 충전 dQ/dV 양수 유지 | PASS — eq:reverse 정합 |
| 8 | 분극: V_n = V_app − σ_d|I|R_n | PASS — eq:vn 정합 |

**새 회귀 없음**: 보완 수정(A_j 재정의 + ΔS_a 추가)이 다른 절·식에 부호 결함 유입하는지 검토.
- eq:Lq 지수 변경 → eq:lnLq 절편 b_j 재정의와 정합 확인: `b_j = −ΔS_a/R − ln(1+e^{−A/RT})` (두 항 모두 온도 약의존) → OK.
- S4 arrhenius 식 eq:arrhenius: y(T) 의 보정 항을 −(−χ_d A_j)/RT + ln(1+e^{−A/RT}) 로 명시 → 기울기 = −ΔH_a^eff/R 정합.
- ΔG_{a,j}^eff 도입이 eq:chid, eq:dHeff 에 영향 없음(ΔS_a 는 별도 항).

## 빌드 결과

- xelatex 2-pass: **에러 0** (Warning만 — 1차 pass undefined ref 정상, 2차 pass 해소)
- PDF: `v7-01b.pdf` 293 kB, 2026-06-29 생성
- 원본 v7-01.tex: 비파괴 보존(미수정)

## 그림 목록

| 그림 | 위치(절) | 이유 |
|------|----------|------|
| fig:flowchart | 서론 | N0→N9 진행 전체 조감 |
| fig:polshift | N1 (§2) | 분극 이동 직관 |
| fig:logistic | N4/N5 (§5) | logistic + dξ/dV bell 시각화 |
| fig:tail | N8 (§8) | 동역학 꼬리 발생 시각화 |
