# NOTEb — v7-02b 보완 기록

## 보완 항목 (v7-02 → v7-02b)

### 1. 기호 𝒜 이중 의미 해소
- **문제**: v7-02의 기호 사전 행(L157)과 §7 eq:affinity에서 𝒜를 `min(z_cut n_j RT, A_cap RT)` 상수로 정의했으나, §5 eq:stationary(L413)에서 동일 기호 𝒜를 `σ_d F(V_n − U_j^d)` (전위-의존 구동력)로 재사용 — 이중 의미 충돌.
- **수정**:
  - 기호 사전 𝒜 행: "꼬리 컷점 affinity 상수, 전위 V_n 무의존" 명시로 교체.
  - §5 eq:stationary: 𝒜 기호 제거, 전위-구동력을 `σ_d(V_n−U_j^d)/w_j` 풀어쓰기로 직접 표현(eq:stationary 재작성).
  - §7 eq:affinity·eq:bv: 𝒜 = 컷점 상수임을 절 도입부에서 명시, "V_n 무의존 상수, L_q도 V_n에 직접 의존하지 않음" 추가.
  - 부호 규약 요약: `∂ln L_q/∂V < 0` 오류 문장 삭제 → 𝒜 V_n 무의존 명시로 교체.

### 2. verifybox §2 분극 peak 위치 결론 부호 교정
- **문제**: v7-02 L213-215 "방전 ICA peak가 OCV peak보다 **낮은** 전위에 나타나는 이유" — 부호 역전.
- **분석**: 방전 σ_d=+1 → V_n = V_app − |I|R_n < V_app. ICA peak는 V_n = U_j^d에서 발생, 측정축으로 환원하면 V_app = V_n + |I|R_n > V_n. 따라서 방전 ICA peak는 OCV보다 **높은** V_app에 위치.
- **수정**: "높은 전위에 나타난다"로 교정, 논리 전개도 V_app = V_n + |I|R_n 명시.

### 3. §7 verifybox 오류 등식 삭제
- **문제**: v7-02 L564-566: `∂ln L_q/∂V_n` 검산에서 `−χ_d 𝒜/RT = −χ_d σ_d F(V_n−U_j^d)/RT`로 쓰고 기울기 `= −χ_d σ_d F/RT ≤ 0` 도출 — 𝒜가 상수인데 V_n 함수로 잘못 처리한 오류.
- **수정**: 해당 verifybox를 재작성. 𝒜 V_n 무의존 → `∂L_q/∂V_n = 0` 확인, 충전 방향 χ_d 교체 확인으로 대체.

### 4. §9 세 인자 의존성 표 수정
- **문제**: "꼬리 길이 - 전위 V↑" 셀: "감소 (∂lnL/∂V<0)" — 𝒜 상수화로 근거 소실.
- **수정**: "직접 의존 없음(𝒜 고정)" + Peak 높이 행도 "꼬리 단축으로 증가" → "꼬리 길이 불변, peak 이동만"으로 교정.

## §8 부호 체크리스트 전건 재확인 결과

| # | 항목 | 결과 |
|---|------|------|
| 1 | U_j(T)=(−ΔH+TΔS)/F (ΔG=−FU) | PASS — eq:deltaG·eq:Uj 정합 |
| 2 | ξ_eq = logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ | PASS — eq:xieq, σ_d=+1에서 지수 증가 |
| 3 | dξ/dV = σ_d ξ(1−ξ)/w > 0 (방향 불변) | PASS — eq:dxidV, σ_d 제곱 없음 |
| 4 | ΔU_hys ≥ 0, Ω≤2RT→0; 분기중심 ±½σ_d… | PASS — eq:hysdU·eq:hyscenter |
| 5 | χ_d: 방전 χ / 충전 1−χ; ΔH_a^eff=ΔH_a−χ_dΩ | PASS — eq:chid·eq:dHeff |
| 6 | 𝒜 = 컷점 상수, V_n 무의존, ∂L_q/∂V=0 | PASS (b에서 수정) — eq:affinity 명시 |
| 7 | 충전 격자 역전; 충전 dQ/dV = 방전 거울(양수) | PASS — eq:reverse·verifybox §8 |
| 8 | 분극: V_n = V_app − σ_d|I|R_n; 방전 ICA peak > OCV peak | PASS (b에서 수정) — eq:vn·verifybox §2 |

## ★부호회귀 self-test

- eq:stationary에서 𝒜 기호 제거 후 eq:xieq로 이어지는 σ_d 부호 사슬 재추적:
  `z = σ_d(V_n−U_j^d)/w_j` → `ξ_eq = 1/(1+e^{−z})` → 방전 z↑→ξ↑ PASS.
- eq:affinity의 𝒜는 eq:lnLq에서 `-χ_d 𝒜/RT` 항으로 들어감 — 상수이므로 방전/충전 모두 동일 크기(방향 차이는 χ_d가 수용) PASS.
- verifybox §2: V_n < V_app (방전) → peak@V_n=U_j^d → peak@V_app = U_j^d + |I|R_n > U_j^d (OCV) PASS.

## 빌드 결과

- xelatex 2-pass: 에러 0, 경고 없음(undefined ref 1-pass 후 2-pass 해소).
- 출력: `v7-02b.pdf` 14페이지.

## Decision Queue

- 없음.
