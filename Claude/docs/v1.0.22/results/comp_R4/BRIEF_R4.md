# BRIEF R4 — Si·블렌드 조사 + L2 등재 준비·L5 재소싱 (v1.0.22 — 저비용 1창, D22-4)

## 규칙 (위반 시 기각)
1. 산출물은 본 폴더(`comp_R4/`) 신규 파일만. 기존 파일 수정·git 조작·`Codex/` 접근 금지.
2. **기억 서지 절대 금지** — 웹(doi/arXiv/출판사)에서 실검증한 문헌만 기록. 검증 실패는 목록에도 올리지 않는다. 원장 등재는 마스터 소관(후보 표까지만).
3. 조기 저장(완성분 즉시 파일).

## 맥락·원전 (정독)
- `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md` — §6 Si 서지 17건(14건 기등재)·Si 확장 설계.
- `/home/user/Project_Anode_Fit/Claude/plans/2026-07-17-v1022-master-plan.md` §7 — R5 블렌드 이론 핵심(공통-μ 대정준·f_Si=Q_Si/Q 0~30%·케이스 Si/SiOₓ/Si–C)·R6 코드 설계. **조사는 R5 저작과 R6 코드가 소비할 초기값·문헌 기반을 만든다.**
- `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_appD_si.tex` — 현행 Ch3 골격(생존 지도·tab:simap·GS-1)과 `results/V1022_REFERENCE_LEDGER.md`(V1 원장)·`comp_R3/E_bridges/L2_TIER_CANDIDATES.md`·`L5_CHARGEORDER_CHECK.md`.

## 작업 (산출 5본)
1. `SI_CASES.md` — 케이스별(원소 Si / SiOₓ / Si–C 복합) 문헌 조사: 전위 곡선 개형·평균 전위·히스테리시스 크기·1차 리튬화 vs 순환 안정 곡선 차이·용량. 각 항목 [검증 문헌·doi·tier 제안·대표 수치(원문 확인분만)].
2. `SI_ENTROPY.md` — Si 엔트로피(∂U/∂T) 실측 문헌 — 흑연 대비 차이·부호.
3. `BLEND_ALIGN.md` — 흑연+Si 블렌드 전위 정렬·용량 배분 문헌(f_Si 0~30% 급 실측 dQ/dV 있으면 표기) — R5 공통-μ 대정준·R6 BlendedAnodeDQDV 가 쓸 초기값 후보.
4. `L2_REGISTER_PREP.md` — comp_R3 의 L2 후보 3건(reynier2004 승급·menetrier1999·EES-entropymetry 2020)의 서지 완전 정보(저자·저널·권호·doi — 원장 등재 양식) 재검증 확정.
5. `L5_RESOURCE.md` — charge-order ΔS(0.47/1.49 J/mol·K) 재소싱: motohashi2009 대체 1차 원전 탐색(열역학/엔트로피 실측 계열) — 성공 시 서지+값+조성, 실패 시 "재소싱 실패·tier-C 유지" 판정.

## 완료 보고
케이스별 검증 문헌 수·신규 후보 수(전건 검증분)·L2 확정 3건 여부·L5 재소싱 성패.
