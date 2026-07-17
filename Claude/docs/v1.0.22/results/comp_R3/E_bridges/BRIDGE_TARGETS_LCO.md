# BRIDGE_TARGETS_LCO — 인용 다리(LCO분) 대상 선별표 (v1.0.22 R3 · O-E)

> 산출: 초안 전용. 마스터 `.tex`·기존 문서 무수정. 산출물은 `comp_R3/E_bridges/` 신규 파일만. `Codex/` 무접근.
> 대상 문서 = **신 Chapter 2 (LCO)** = `ch2_lco_v1.0.22.tex` 조립분. **★명칭 주의(P7)**: Ch2 를 조립하는 절 파일은 역사적 이름 `_sections/ch1_sec11~17`(구 Ch1 Part II)이나 현 구조에선 **Chapter 2** 다. 파일명(ch1_secNN)과 챕터(Ch2)를 혼동하지 말 것.
> 서지 규칙: `results/V1022_REFERENCE_LEDGER.md`(v1.0.21→v1.0.20 승계) **V1 키만**. 아래 전건 V1(= `ch2v22_bib.tex` 14종) 확인. 기억 서지 0.
> 스코프: **흑연분(R2 완료)·Si분(R5 소관) 침범 금지.** 본 표 전 대상은 LCO 절(sec11~17)·ch2_lco 마스터 소관.

## 1. 본문 \cite 전수 스캔 — LCO 절(sec11~17, 전부 Ch2 조립) 소재별 대조

| 키 | 본문 cite 실위치(파일:행) | tier/성격 | load-bearing 판정·사유 | 다리 |
|---|---|---|---|---|
| **marianetti2004** | sec13:137 · sec15:55,59 | 이론(DFT) | **상** — 우리 MIT 게이트 `g(E_F,x)`(eq:ggate)의 중심·폭이 이 논문의 불순물-Mott 조성경계(x≲0.75 metal·x≳0.95 insulator)를 직접 읽음 | **○ br_marianetti2004** |
| **vanderven1998** | sec13:33,109,160 | 이론(클러스터전개) | **상** — 우리 유효 인력 `Ω_j^cat`(eq:lco-gxi)·spinodal 문턱의 미시 근거(제일원리 상도표·x=½ 질서상) | **○ br_vanderven1998** |
| **msmr_origin2017** | sec11:165 · sec17:8 | 이론(원전) | **상** — 우리 `eq:msmr`/`eq:lco-msmrmap` 의 종별 logistic 원전 | **○ br_msmr_lineage** |
| **bakerverbrugge2018** | sec17:9 | 이론(명명) | **상** — "multi-species multi-reaction(MSMR)" 명명 원전; 위와 한 다리로 묶음 | **○ br_msmr_lineage** |
| **reynier2004** | sec11:48 · sec14:70 · sec15:166,249,251,258 · sec16:53 | 실측+계산 | **상(추가 후보 판정 = YES)** — 우리 삼분해(eq:lco-decomp: config/vib/elec)가 이 논문의 실측 3기여 분해와 동형; config 지배·MIT electronic≈config 주장의 앵커(6곳 인용) | **○ br_reynier2004** |
| motohashi2009 | sec11:48 · sec13:33,126,136 · sec14:99 · sec15:20,26,55,124,198,230 · sec16:53 | 실측(자기상도표) | **중(값 앵커)** — `g_max=13` anchor·전자 상도표. **측정값 인용**이지 유도식 다리 대상 아님. **★L5 대상**(0.47/1.49 값 원전) | ✗(값 앵커) · L5 |
| reimers1992 | sec13:33,108,135,160 · sec15:26,55,232 | 실측(in situ XRD) | **중(값 앵커)** — T1/T2 전이·2상 공존 실측. 측정 관측 인용, 유도 비의존 | ✗(값 앵커) · **L2 후보** |
| menetrier1999 | sec15:20,26,51,55,232 | 실측(NMR/전기) | **중(값 앵커)** — MIT 2상역 x≈0.75–0.94 실측. 측정 관측 인용 | ✗(값 앵커) · **L2 후보** |
| xia2007 | sec11:42,48 · sec16:53 | 실측(dQ/dV) | **중(값 앵커)** — LCO 세 전이 OCV. 전이 초기값 출발점 인용 | ✗(값 앵커) · L2 참조 |
| swiderska2019 | sec12:89,94 | 실측(∂φ/∂T) | **중(값 앵커)** — LCO 단전극 엔트로피계수 +0.83 mV/K 부호검산. 측정값 인용(tier B), 유도 비관여(R2 판정 승계) | ✗(값 앵커) |
| ml2024 | sec13:111 · sec15:252 | 이론(ML statmech) | **중~하(보조)** — order–disorder 연속축 재확인·config 전용 계산. vanderven 다리 문맥에 병기, 별도 다리 불요 | ✗(보조) |
| mott1968 | sec15:48 | 교과서 | **하(교과서 앵커)** — Mott 판별식 `eq:lco-mottcrit` 는 본문 bgbox 가 이미 자족 유도(다리 내장) | ✗(교과서) |
| imada1998 | sec15:48,50 | 교과서(리뷰) | **하(교과서 앵커)** — MIT 분류·상관물리 리뷰. bgbox 내 다리 완비 | ✗(교과서) |
| msmr2024 | sec11:165 · sec17:10 | 이론(후속) | **하(계보 후속)** — 엔트로피·온도의존 MSMR 파라미터화. msmr_lineage 다리 문맥에 계보 후속으로 병기 | ✗(계보 후속) |

**스캔 총계**: LCO 절 \cite = **14 키**(= ch2v22_bib.tex 14종, 전건 V1). 누락 0.

## 2. 소관 경계 확인 (월권 0)

- 본 표 14 키는 전부 `ch2_lco_v1.0.22.tex` 조립분(sec11~17)에서만 등장 — graphite master(ch1) 및 Si 부록(ch1_appD_si)에 걸친 키는 대상 밖.
- R2(흑연) 소관 키(dreyer·mckinnon1983·bazant2013·weppner_huggins1977·baek_pilon2022·bernardi1985·allart2018·reynier2003) 는 본 스캔에 **미등장**(LCO 절엔 cite 없음) → 침범 0.
- R5(Si) 소관 키(sethuraman·larchecahn1973·verbrugge_lisi2016·koebbing2024 등) 도 LCO 절 **미등장** → 침범 0.
- ★주의: `reynier2004`(LCO 엔트로피, Phys Rev B 70, 174304)는 R2 의 `reynier2003`(흑연 엔트로피, J Power Sources)과 **별개 논문** — 혼동 금지.

## 3. 요약

- **다리 = 4건**(마스터 지목 3 = marianetti2004·vanderven1998·msmr[origin2017+bakerverbrugge2018] + load-bearing 추가 후보 판정 YES = reynier2004).
- 값 앵커·교과서·보조(다리 불요) = 10 키 — 사유 표 명기(측정값 인용/교과서 자족유도/계보 병기).
- 초안·삽입위치·3요소 요지 = `BRIDGE_DRAFTS_LCO.md`. 다리별 스니펫 = `br_<키>.tex`(srcbox).
