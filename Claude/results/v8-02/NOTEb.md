# NOTEb — v8-02b 증분 보완 기록

## 베이스
- v8-02.tex (1068행) → v8-02b.tex (증분 수정)

## 보완 4건

### D-PEAK (sec:tail — peak 모양 절)
- **삭제**: "L_V 작으면 ξ_lag→한 칸 뒤처진 ξ_eq→종 환원" 서술 (틀림: ρ→0이면 ξ_lag→ξ_eq 즉시, peak→0)
- **추가**: 두 극한 전개
  - 극한 (i) L_V→0: ρ=e^{−Δgrid/L_V}→0 ⇒ ξ_lag→ξ_eq 즉시 추종 ⇒ peak→0. 코드 eq:branch 스위치(L_V<ν·Δgrid)가 0/0 우회해 평형 종 반환.
  - 극한 (ii) L_V≫Δgrid: ρ→1, (1−ρ)≈Δgrid/L_V, 연속 전개로 (ξ_eq−ξ_lag)/L_V→dξ_eq/dV. 매끄러운 종 환원.
- **업데이트**: eq:branch 케이스 박스에 "eq:branch 스위치" 명칭 및 두 극한 참조 추가
- **업데이트**: 부호 검산 R3 self-test — ρ→0 경로 명시

### D-DHEFF (sec:lag — 방향별 전달 계수 절)
- **보강**: forward rate의 −χ_dΩ 경유 중간식
  - ΔG_a^eff ≡ ΔG_a − χ_d·Ω 경로 명시
  - 깊은 꼬리 ξ→1(방전)에서 상수 기여 +Ω가 순방향 장벽에 흡수되는 물리 경로 서술
  - ΔH_a^eff = ΔH_a − χ_d·Ω 결론식 inline 중간식으로 연결

### D-WEFF (sec:width — 폭 절)
- **추가**: w_eff 중심기울기 다리
  - g_j''(ξ)|_{ξ=1/2} = 4RT − 2Ω 평가
  - sF·dξ/dV|_{1/2} = sF/[g_j''|_{1/2}] 연쇄율
  - 유효 폭 w_eff = RT/F·(1 − Ω/2RT) 도출 경로 완성

### D-VEQ (sec:hys — 히스테리시스 분기 중심 절)
- **추가**: eq:Veq 앞에 sF(V_eq−U)=g'(ξ) 평형 조건 다리 inline
  - "평형 조건 sF(V_eq−U)=g_j'(ξ)에서 나온다" + g_j' 대입 명시
  - forward-defer 없이 직접 연결

## 부호 8항 재확인
S1~S8 전건 v8-02 상태와 동일하게 PASS. 변경사항은 R3 설명 보강뿐 (로직 변경 없음).

## 새 회귀 self-test (D-PEAK 대응)
- R3 업데이트: "ρ=e^{−Δgrid/L_V}→0 → ξ_lag→ξ_eq 즉시" 경로 명시
- L_V≫Δgrid 극한은 문중 서술로 커버 (별도 R 항목 대신 inline)

## 빌드
- xelatex 3-pass, 에러(!) 0건
- 출력: v8-02b.pdf, 19페이지
- 경고: MiKTeX 업데이트 권고(무해), font substitution(무해), Labels changed→3pass로 안정

## 산출물
- `v8-02b.tex` — 증분 수정 완결 문건 (v8-02.tex 원본 보존)
- `v8-02b.pdf` — xelatex 3-pass 빌드 결과
- `NOTEb.md` — 이 파일
