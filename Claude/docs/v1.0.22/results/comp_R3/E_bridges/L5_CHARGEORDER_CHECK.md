# L5_CHARGEORDER_CHECK — charge-order ΔS(0.47/1.49) 1차 원전 재확인 (v1.0.22 R3 · O-E)

> 스펙 원전 = `docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md` §5 L5 행: "charge-order ΔS 값(T2/T3) 0.47/1.49 J/(mol·K)@x=½,⅔ 슬롯 배정 tier C(조성창 불일치) → 1차 원전 재확인 후 tier 권고."
> 규칙: 확인 성공 시 [원전 서지·정확한 조성·본문 슬롯 배정과의 일치 여부·tier 권고], 실패 시 "확인 불가 — tier-C 유지".

## 1. 대상 값과 현행 본문 귀속

- 값: **ΔS_charge-order ≈ 0.47 J/(mol·K) @ x=½** · **≈ 1.49 J/(mol·K) @ x=⅔** (T2/T3 config 슬롯 초기값).
- 본문 인용 위치·귀속: **Motohashi\cite{motohashi2009}** 로 귀속됨 —
  - `sec13:125-127`: "정렬의 charge-order 엔트로피 변화(≈0.47 J/(mol K)@x=½, ≈1.49 J/(mol K)@x=⅔ [값은 tier A, Motohashi; 단 두 anchor 조성(x=½,⅔)이 모두 T2/T3 조성 창(x≈0.55/0.48)과 정확히 일치하지 않아 **슬롯 배정은 양쪽 다 tier C**])".
  - `sec14:99`: "ΔS_j^0(Motohashi ≈0.47/1.49 J/(mol K), T2/T3 — 배정 양쪽 tier C)".
  - `sec11` 표 `tab:lco-staging`: T2 config ≈0.47(배정 tier C)·T3 config ≈1.49(배정 tier C).

## 2. 원전 재확인 시도 (본 세션 WebSearch/WebFetch)

| 시도 | 소스 | 결과 |
|---|---|---|
| 1 | WebSearch "Motohashi Electronic phase diagram LixCoO2 PRB 80 165114" | **motohashi2009 는 자기(magnetic)·전자 상도표 논문** 확인 — dc-자화율 + $^{59}$Co NMR/NQR 기반; 자기 임계점 x=0.35–0.40(Pauli-paramagnetic ↔ Curie–Weiss metal), Curie–Weiss 영역(x≥0.40)에 상전이들. **config charge-order 엔트로피 측정 논문 아님.** |
| 2 | WebFetch arXiv:0909.3556 (PRB 80,165114 프리프린트) | PDF 스트림 바이너리 손상 → 신뢰 추출 실패. 추출 가능분에서 **0.47/1.49 J/(mol·K)·g(E_F)=13 값 미표출**(단, 손상으로 부재 단정 불가). |
| 3 | WebFetch Aalto 기관 리포지터리 PDF | HTTP 403(접근 실패). |

## 3. 판정 — **확인 불가 (원전 직접 대조 실패) → tier-C 유지**

**근거:**
1. **귀속 의심**: motohashi2009 의 판독 가능 메타/초록은 이 논문이 **자기 상도표(자화율+NMR/NQR)** 연구임을 보임 — x=½,⅔ 의 **configurational charge-order 엔트로피(J/mol·K)** 를 주는 1차 원전으로는 부정합. 0.47/1.49 값이 이 논문의 **자기(스핀) 엔트로피**일 가능성마저 있으며, 그렇다면 config 슬롯에 넣는 것은 **물리 범주 오류**(스핀 엔트로피≠charge-order config 엔트로피)로, 별도 진단 필요.
2. **직접 대조 불능**: 권위 프리프린트(arXiv:0909.3556)가 본 도구로 기계 판독 불가 포맷이고 유료/기관본이 403 — 0.47/1.49 값의 **존재 여부·정확한 조성을 직접 확인/반증 모두 실패**. 기억 서지 금지 원칙상 미확인 값 재현·tier 승급 불가.
3. **조성 불일치 보강**: 본 세션 검증된 유일한 LCO 엔트로피 실측 1차 문헌 **reynier2004**(ASU pure 초록)는 Li·빈자리 **질서상을 x=½ 와 x=5/6(≈0.83)** 에 둔다 — 본문 슬롯의 **x=⅔(≈0.67) anchor 와도 불일치**. 곧 x=⅔ 배정은 motohashi 뿐 아니라 최근접 검증 실측 문헌과도 어긋난다.

**즉 현행 본문의 "tier A(값)·tier C(슬롯 배정)" 표기 중 "tier A(값)" 의 원전 귀속이 재확인되지 않았다.** 조성창 불일치(x=½,⅔ vs T2/T3 x≈0.55,0.48)는 본문이 이미 tier C 로 정직 표기 중이며, 본 재확인은 그 **tier-C 유지를 지지**한다(오히려 값 자체의 원전도 재확인 필요로 격상).

## 4. 마스터 권고 (실집행 소관)

1. **tier-C 유지** — T2/T3 config ΔS(0.47/1.49) 슬롯 배정은 현행대로 tier C 유지.
2. **원전 직접 대조**: motohashi2009 전문(PhysRevB 80,165114 — 유료; arXiv:0909.3556 은 본 도구 판독 불가)을 사람이 직접 열어 (a) 0.47/1.49 J/(mol·K) 값의 실재·정확 조성·**엔트로피 종류(config vs 자기)** 를 확인. 확인 실패 시 값의 tier 도 A→C 강등 검토.
3. **재소싱 대안**(값이 motohashi 원전에서 확인 안 될 경우): charge-order config ΔS 를 검증된 config-엔트로피 원전으로 재귀속 —
   - **reynier2004**(실측 ΔS, x=½·5/6 질서상; L2 후보 C1), 또는
   - **EES-entropymetry2020**(monoclinic order–disorder ΔS 실측 서명; L2 후보 C3), 또는
   - **ml2024/vanderven1998**(제일원리 order–disorder config 엔트로피) —
   조성을 실측 질서상(x=½, x=5/6 등)에 맞춰 재배정.
4. **자산 표기**: 본 재확인 결과를 L5 자산 노트로 원장/각주에 반영(값 원전 미확인·tier-C 유지·재소싱 후보 제시).
