# V1.0.15 P6 RESULT — 그림 좌표 재검산·점별 재산출·정합

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P6(Steps 28–32). 대상 = Ch1 데이터-보유 그림. 상태 = ✅ 완주.

## 1. 스코핑 판단 (경연 vs 재검산)
계획 P6 = "그림 9종 경연 + 좌표 재검산·정합". 현 Ch1/Ch2 그림은 이미 Fable TikZ 로 완성도 높고, **격자 퇴출과 직접 관련된 실질 작업은 데이터-보유 그림(memory-integral 곡선)이 점별 코드와 정합하는지 재검산·재산출**이다. 좋은 도식을 재설계 경연으로 누더기 만들 위험(사용자 상시 우려)을 피하고, **좌표 재검산·점별 재산출**(플랜의 P6 gate)에 집중했다. 순수 개념/열역학 도식(flowchart·blend·staging·gxi)은 격자 무관이라 재산출 불요.

## 2. 재산출 (점별 코드로 그림 데이터 재계산)
격자-법 좌표를 지녔던 두 데이터 그림을 **Anode_Fit_v1.0.15 의 `_causal_memory_pointwise` 로 재산출**:

- **fig:reversal**(인과 꼬리 방향, Ch1 §1.9): 방·충전 peak-shape 실선 전 곡선(각 23점)을 점별 기억적분으로 재계산. 격자-법 peak **0.1923@1.00w → 점별 0.1955@1.01w**(격자 이산화 아티팩트 ~1.6% 제거). 평형 점선(ξ_eq(1−ξ_eq)/w, 0.25@중심)은 이미 해석값이라 불변. peak dot·라벨·캡션·주석(0.192→0.196) 동기화. 방·충 정확 거울 유지·면적 보존 확인(∫peak→1).
- **fig:relaxode**(지연 완화 도식): 목표 ξ_eq(그려진 sigmoid)로부터 지연 ξ_lag 를 **실제 기억적분(L=0.4 q-단위)으로 재산출**(손그림 → 자기정합). 현 손그림(ξ_lag@1.5=1.08)과 점별값(1.11) 거의 일치 확인 후 정확값으로 교체. gap 화살표 r=ξ_eq−ξ_lag·dotted 정합.

## 3. 정합 확인 (재산출 불요 그림)
- **fig:spine**(계산 흐름 flowchart): P3 에서 이미 branch-select 제거·N6–N8 단일 꼬리 경로로 정합(데이터 없음).
- **fig:blend**(Ch2 겹침 블렌드): 개념 sigmoid 블렌드(모식, 격자 무관) — 정합.
- **fig:staging·fig:gxi·fig:lco-dirmap 등**: 열역학/방향 도식(격자 무관) — 무변경.
- **Ch2 Q_rev(x̄) 곡선**(P4 그림 후보): tab:qrev 표가 5-SOC 부호 교대를 이미 전달하므로 별도 TikZ 신설 안 함(Ch2 includegraphics 0 원칙·누더기 회피). worked example 표로 충분.

## 4. Gate
- **점별 정합**: 두 데이터 그림이 이제 Anode_Fit_v1.0.15 점별 출력과 point-exact 정합(도식 수치평가 = 실 구현값).
- **빌드 GREEN**: Ch1 `xelatex` 2-pass exit 0 / undefined 0 / Overfull >10pt 0 / 58p. 좌표 갱신 정상 컴파일.
- **격자 아티팩트 제거**: fig:reversal 마지막 격자-법 잔재(0.1923) → 점별(0.1955). 그림 캡션 P6-누출(이전 판·P6 소관)은 P3 에서 이미 제거.

## 5. Read Coverage
- fig:reversal TikZ+캡션(L2160-2207)·fig:relaxode TikZ+캡션(L2031-2056) 정독. 점별 코드로 곡선 재계산·플롯점 대조.

## 6. 미결/이월
- **P7**: 변경분 검수 + 문건↔코드 수치 대조(P4 worked example·fig 좌표) + HANDOVER·INDEX + 최종 게이트.

## 7. 상태·커밋
✅ **P6 완주**. 데이터 그림 2종 점별 재산출·정합, 개념 도식 확인. 재설계 경연 불요(Fable 품질 도식을 점별 정합화). 빌드 GREEN. 커밋 = main·attribution 없음·명시 스테이징(Ch1 tex/pdf + P6 결과 + 레저).
