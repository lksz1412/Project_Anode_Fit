# Ch1 v9 — 종합·문서 통합 구조 (Phase A.3, master)

> 35_electronic_entropy_design.md(전자 엔트로피·전이표·코드 일반화) 위에서, **v8-11(흑연) → v9(흑연+LCO 통합)** 문서 구조를 확정. 빌드 9종 공통 입력.

## 1. 통합 원칙
- v8-11 의 흑연 9 절(N0–N9 + 부호검산)은 **골격 보존**. LCO 는 *각 절에 양극 대응을 짜 넣되*, 별도 부록이 아니라 같은 프레임의 "두 번째 전극 사례"로 통합.
- 전개 순서: **일반(전극 불문) → 흑연 사례 → LCO 사례**. 곧 forward 모델 식(logistic·$U_j(T)$·∂U/∂T)은 *전극 일반*으로 세우고(이미 v8-11 이 그러함), 파라미터·고유항만 전극별 분기.
- LCO 고유 = **전자 엔트로피 항**(흑연엔 없음) → 새 소절로 도입하되, "왜 흑연엔 없고 LCO엔 있나"(metallic 천이 유무)를 물리로 설명.

## 2. 절별 LCO 통합 지점
| v8-11 절 | LCO 추가 | 깊이 |
|---|---|---|
| N0 기호·매핑 | LCO_STAGING_LIT 전이표(§35-4) 추가, 양극 부호 규약(U 높음) | 표 1행 |
| N2 평형중심 U_j(T) | LCO 전이 U_j(3.9/4.05/4.17V)·∂U_j/∂T=ΔS/F 양극 부호 | 짧은 절 |
| N3 히스/g(ξ) | LCO order–disorder Ω(monoclinic 정렬)·MIT 2상역 = 같은 정규용액 틀 | 짧은 절 |
| **N4/N5 폭·logistic** | ★**ξ_eq 분포 프레이밍 1점 보강**(분포 관점, statmech_review) + LCO 적용 | ★소절 추가 |
| **N(신규) 전자 엔트로피** | ★**LCO 전자 엔트로피 항**($S_e=\frac{\pi^2}{3}k_B^2Tg(E_F)$·MIT 게이트·∝T) — 흑연엔 0, LCO 고유 | ★새 절(핵심) |
| N6 평형 peak | LCO dQ/dV peak(3.9·4.05–4.20V) | 그림+짧은 절 |
| N9 합산·역보간 | LCO ΔS_rxn^cat 분해(config+vib+electronic) | 짧은 절 |
| 코드 일반화 | MSMR↔Ch1 동형(§35-5)·파라미터 교체+전자항 plug-in(H) | 짧은 절 |

## 3. 새 절 "전자 엔트로피" 위치·논리 (★핵심 신규)
- 위치: N5(logistic) 뒤, N6(peak) 앞 — 분포 프레이밍(N4/5 보강) → "흑연은 config+vib 로 닫히나 LCO 는 metallic 천이로 *전자 분포(Fermi–Dirac)* 가 엔트로피에 추가" 자연 연결.
- 논리 사슬: (a) LCO x=1 절연체→x↓ metal(MIT, Ménétrier) (b) Fermi–Dirac 분포→Sommerfeld $S_e=\frac{\pi^2}{3}k_B^2Tg(E_F)$ (c) 부분몰 $\Delta S_e\propto T\,\partial g/\partial x$ (d) g(E_F,x) MIT-logistic 게이트(모델 가정, 초기값 피팅) (e) 작지만(0.18 kB/atom) MIT 게이트로 필수(config 단독 2상역 재현 불가).
- ★흑연과의 대비를 명시: 흑연은 반금속/전도성 변화 미미 → 전자항 무시 가능, LCO 는 MIT 로 필수. *이 대비가 통합 챕터의 교육 가치*.

## 4. 갭 처리 (문서 내 명시)
G1–G5(연속 ΔS(x)·g(E_F)(x)·MSMR LCO 파라미터·도핑 shift·ΔH_f 절대) = **초기값(§35-2,4)+우리 데이터 round-trip 피팅**으로 식별 — 문서에 "문헌 초기값, 데이터 피팅" 명시(Ch1 GRAPHITE_STAGING_LIT 철학 동일). 허위 정밀 금지(tier 표기).

## 5. 범위 가드
- 코인 하프셀(LCO vs Li) 단독 — **전셀 합성(∂U_cell=∂U_cat−∂U_an) 범위 외**(후속 v10/별도). 단전극 +0.83 mV/K 와 전셀 부호전환 혼동 금지(상충3 해소).
- 분량 = 통합의 자연 결과(흑연 골격 + LCO 절 + 전자 엔트로피 새 절). 조사-급 군더더기 금지.

## Gate (A.3 완료)
문서 통합 구조·새 절 논리·갭 처리·범위 가드 확정. → AUTHOR_BRIEF LCO 칸 채움 → Phase B.
