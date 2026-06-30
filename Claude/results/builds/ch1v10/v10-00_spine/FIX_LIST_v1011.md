# Ch1 v10-11 — adversarial fix-list (v10-10 → v10-11)

> A1/A2/A3 결함 누적. master 삼각검증 후 v10-11. 핵심 = 기작③(집합 통계역학) 재정초.

## A1 broadening 물리 ✅ — 기작③ CRIT/HIGH (재정초 필요)
### ★CRIT D1 — ρ 의 정체: 평형 U_j 분포 아님, **apparent-U(η) 분포**
- 문제: ρ(U_j)를 "입자마다 *전이전위* 분포"로 도입 ↔ 같은 절 "평형 중심 Ū_j=입자 무관 *상수*" → 자기모순(+ORIGIN "평형 U_j 분포≈0").
- ★정정(물리 재정초):
  1. **Dreyer 다입자 통계역학** = two-phase *plateau 구조* 설명(앙상블이 비단조 단일입자 자유에너지 하 **순차 전환**·공통 전위 → 평탄역). 이게 "집합 통계역학" 내용(사용자 요구) — *평형 통계역학*.
  2. **plateau→실측 종 broadening** = 앙상블의 **apparent-U = U_j + η 분포**: ★**U_j(평형 중심)=입자 무관 상수**(분포 ≈0), **분포하는 건 η**(과전압·국소환경·접촉 = 비-크기·비-사이즈). forward 통계평균 $\langle\dd Q/\dd V\rangle=\int \rho(U_\mathrm{app})(\dd Q/\dd V)^\mathrm{single}\,\dd U_\mathrm{app}$, $U_\mathrm{app}=U_j+\eta$. 적분변수 = **apparent-U(η)**, 평형 U_j 아님.
  3. 구조 무질서(Dahn turbostratic) 는 평형 중심에 **작은** 잔여만(tier 정직), 주broadening 은 η.
  → 중심 상수 ↔ 폭(η) 분포 = 모순 해소·ORIGIN 정합.

### HIGH D2 — Dahn x_max=1−P 인용 정정
- x_max=1−P 는 **intra-particle 용량/site-blocking**(sloping) 식 — *inter-particle ρ* 1차근거로 과대인용. inter-particle 정량은 카드43 tier C(근거미발견) → ★tier 병기·"용량한계 예시일 뿐 inter-particle 분포 직접근거 아님" 명시.

### HIGH D3 — LCO 무차별 적용 정정
- 집합 통계역학③(흑연 turbostratic 기반)을 LCO 3전이에 무차별 적용 X. ★기작③은 **흑연 two-phase(LiC₁₂·LiC₆)에 scope**; LCO 는 별도(또는 일반 η 분포로만, 구조무질서 흑연-특정 근거 빼고).

### MED D4/D5
- D4: eq:ensavg 가 전류의존 ①(L_V kernel)을 평형 ρ 적분에 혼입 → ①(kinetic)과 ③(앙상블 통계평균) *분리* 서술(η 분포 평균 vs 단일입자 율속 꼬리).
- D5: 폭폴백↔전이 매핑 G-follow 보강.

## A2 w_eff·보존 ✅ (CRIT/HIGH 0 — 견고, 유지)
- w_eff 잔존 0·★전자엔트로피 byte-identical(SHA-256 일치·184줄)·흑연 4전이/부호 사슬/N7-9 byte 보존·w 이중지위 2개·undefined 0·0-err. ΔS_e<0 보존·apparent-U=U_j+η(중심 불변) 정합.
- NOTE: dreyer2010 = base 기존 bibitem 재사용(주석 표기만 경미).
## A3 인용·빌드 ✅
- fabrication 0·DOI/권 정확·★**사이즈 인용 잔존 0**(yang2023/cogswell \cite 0). 빌드 0-error·문체·TikZ 한글 0.
- ★**D9 CRIT**: `fig:broadening` 선언됐으나 본문 `\ref{fig:broadening}` 0 = orphan → 참조 추가.
- **D1 HIGH**: fly2020 = Fly·Schaltz·**Stroe** 3인인데 bibitem 2인 → Stroe 추가.
- **D2 MED**: rsc2021 bibitem 저자·제목 없음 → 서지 완성. **D3 MED**: dahn1995 제목 한국어·공저자 누락 → 표준화.

## 정정 원칙
base=v10-10 복사→v10-11, ★기작③ 재정초(D1: apparent-U/η 분포·Dreyer plateau·중심 상수)·D2/D3 정정, 사이즈 제외·Ω 2개·w_eff 제거·전자엔트로피 byte 보존 유지, 정식 10회·xelatex 0-err.
