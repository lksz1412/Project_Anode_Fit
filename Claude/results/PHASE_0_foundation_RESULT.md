# Phase 0 — Foundation Result (step 1–16)

## Summary
RB 재구성의 토대 3종 확정: cross-chapter 규약 동결(0.1), 참고문헌 grounding+DOI 검증(0.2), 통합 AL 체계+notation+가독gate 골격(0.3). 5-30 사용자 경고("무근거 무리한 가정")가 실제로 적중 — stretched-tail 핵심 물리 근거가 오귀속(macdonald2000)임을 적발·교체.

## Step Range
1–16 (Phase 0.1: 1–5 / 0.2: 6–12 / 0.3: 13–16).

## Inputs (Read 실제 범위)
- `PHASE_A/B_*_RESULT.md` (결함 입력, 전문)
- `RB_CHARTER.md` 작성 입력 = Phase A/B 교차결함
- `Claude/_local_only/jcp_extract.txt` (사용자 PhD JCP2017 원문 추출, 1–120행 직접 read + Eq.32~39 closure 영역 288–340행)
- `PHASE_DIAG_REFS67_DOSSIER.md` (전문)
- DOI 검증 워크플로 wf_d5ee0a03-49d 결과 30종 (전문 read)

## Files Created
- `Claude/results/RB_CHARTER.md` — cross-chapter 규약 5종 동결
- `Claude/results/RB_REFERENCES_DOSSIER.md` — 참고문헌 grounding+DOI (30종+johnston2006 보강)
- `Claude/results/RB_AL_MASTER.md` — 통합 AL ledger 골격(AL-1~63 기등재) + notation bible + 가독 gate
- `Claude/results/PHASE_0_foundation_RESULT.md` — 본 문건

## Files Updated
- `Claude/results/RB_EXECUTION_LEDGER.md` — Phase 0.1/0.2/0.3 PASS 반영, 다음 step 17

## Read Coverage
- jcp_extract.txt: 1–120행(서론·이론 도입) + 288–340행(Eq.32~39 closure) 직접 read. 나머지(Results/Discussion)는 closure 무관으로 부분 검독.
- DOI 워크플로 결과: 30종 전건 read(JSON 전문).
- consolidated_ch1~6 서두: 각 55–85행 read(의존구조 확인, Phase 직전).

## Execution Evidence
- DOI 워크플로 wf_d5ee0a03-49d: 5배치 병렬, 30종, 257 tool_uses, web 실측(Crossref/IOPscience/AIP/APS/ACS/Wiley/RSC/ACM/SIAM).
- 문제 3건 집중 재검증: macdonald2000(WebFetch Crossref 10.1103/PhysRevB.61.228 → 실제 "Comparison of methods for estimating continuous distributions of relaxation times", 제목 불일치 확정), johnston2006(WebFetch Crossref 10.1103/PhysRevB.74.184430 → "Stretched exponential relaxation arising from a continuous sum of exponential decays" verbatim 일치), funabiki(WebFetch Crossref 10.1016/S0013-4686(99)00262-4 → "Stage transformation of lithium-graphite intercalation compounds...", Electrochim. Acta 45(3) 365–377 1999 확정).
- jcp2017 DOI 10.1063/1.5000882 원문 직접 확인.

## Validation (gate 별)
- **PASS_CHARTER (0.1)**: 규약 5종 전부 "확인 가능한 조건" 1행씩 기술. G-cross 판정 기준 확정.
- **PASS_DOSSIER (0.2)**: 30종 DOI web 실측. CONFIRMED 19+ / CORRECTED 4(doyle·reynier·ohzuku·funabiki) / BOOK 4 / REPLACED 1(macdonald→johnston). 환각 cite 0(전건 web 근거).
- **PASS_AL_SKELETON (0.3)**: AL-1~63 기등재(established 가정 + 검증 DOI), notation bible 매핑 누락 0, 가독 gate 10종 정의.

## Gate
**PASS** (Phase 0 종합). Foundation 확정 — Ch1~6 재유도가 상속할 규약·근거·체계 완비.

## Confirmed Non-Changes
- 폰 원본·통합본 미수정(재구성은 Phase 1~ `_rebuilt` 신규).
- macdonald2000 은 \emph{제거 결정만}; 실제 tex 수정은 재구성 시.
- Codex 산출물 미read.

## Open Issues / Decision Queue
- **★ stretched-tail grounding 정밀도**: johnston2006(연속 합 → stretched) + lindsey1980(KWW)이 "고정 barrier 분포 → T-의존 stretched exponent"를 \emph{완전히} 닫는지는 Ch1 S2(grounding 감사)에서 재유도로 확정. 못 닫으면 FLAGGED(방향-3). 이것이 문서 핵심 물리라 Ch1 의 최우선 검증점.
- plonka(논문 10.1021/jp9831808 vs 책 ISBN) 분리: refs 문건(Phase 7.1)서 확정.
- D2~D6 권고값 진행 중(이의 없음).

## Next
**Phase 1.1 — Ch1 골격추출 (cumulative step 17).** Ch1 = 최대한 심플(열역학 무대 + 극판전위 배리어 낮춤). consolidated_ch1 + _body_ch1 전수 정독 → 핵심식 흐름·가정 전수 목록 + 본 장 입력 결함(closure 동결, AL-14 stretched grounding).
