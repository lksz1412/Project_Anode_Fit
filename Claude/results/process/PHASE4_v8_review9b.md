# Phase 4.1 — v8 보완본(9b) 재검토 (검토2) 종합

> 9 Opus 검수(식·유도 단위 청크 = 검토1과 다른 스킴·refute mandate·★D-PEAK 정정의 *수학적 옳음* 직접 검산·신규 회귀). 개별 = 각 `v8-NN/REVIEW2.md`.

## 재점수 + 회귀 매트릭스 (합 /35)

| 버전 | 모델 | 합(b) | Δ | D-PEAK 정정 | 신규 회귀 | 체리픽 |
|---|---|---:|---:|---|---|---|
| **v8-09b** | Codex | **35** | +5 | ✅ 수치검산 통과 | **0** | 청정·강후보 |
| **v8-06b** | Opus | **34** | +3 | ✅ 2곳 정확(캡션+본문) | **0** | ★**1순위 베이스**(전 KNOWN_DEFECTS 해소·9그림) |
| v8-05b | Opus | 33 | +3 | ✅ 수치검산(R5 50-step 해상도 caveat) | 0 | 강후보 |
| v8-04b | Opus | 33 | +7 | ✅ 정확 | 0 | 강후보·fig:overshoot 전면 정정 |
| v8-08b | Codex | 33 | +6 | ✅ 정확 | 0 | 강후보 |
| v8-01b | Sonnet | 28 | +2 | (본문 무보유 유지) | self-test NR-1 산술·NR-2 거짓극한 재유입 | 본문 graft만 |
| v8-03b | Sonnet | 26 | +2 | ✗ **regime 반전 오류**("연속 환원") | D-WEFF ¼ 오기 | 제외 |
| v8-02b | Sonnet | 25 | −1 | 극한(i) 옳음·**(ii) 재유도 오류** | D-WEFF ¼·D-DHEFF 공허 | 제외 |
| v8-07b | Codex | (미완) | — | ✅ 방향 | **D-WEFF eq:weff_bridge 차원오류·s_F orphan** | 제외 |

## ★ 검토2 적발 — 보완-유입 회귀 (v09b 교훈 적중·이식 금지)
1. **D-PEAK 재정정 오류**: v8-03b(regime 반전)·v8-02b(극한 ii ρ/(1−ρ) 재유도)·v8-01b(self-test R6 거짓극한 재유입) — *고치다 다시 틀림*. **D-WEFF "4Fw 다리"가 함정**: v8-02b·03b(¼ 인수)·07b(차원오류·s_F orphan) 3종 botch(박스값은 옳음).
2. **정확 정정 5종**: v8-06b·09b·05b·04b·08b — D-PEAK·D-WEFF 둘 다 수학 검산 통과·회귀 0.
3. ★**D-PEAK2 심화**(v8-07b 자체 적대검수): eq:branch 는 매끈 극한 아닌 *이산 모드 스위치*, 문턱 ν=2 서 진폭 불일치(불연속). 최종 v8-11 정직 기술(KNOWN_DEFECTS D-PEAK2).

## 체리픽 플랜 (Phase 5 — v6 합류)
- **베이스 = v8-06b**(34·전 KNOWN_DEFECTS 해소·D-PEAK 2곳 정확·유도 풍부·그림 9개). master 가 v8-06b·v8-09b·v8-05b·v8-04b 직접 정독해 최종 확정.
- **graft 후보**: v8-09b(35) 청정 유도·v8-04b fig:overshoot 정정본·v8-05b D-PEAK 수치 R5(해상도 명시 보강)·그림 경쟁 풀(v8-06b 9 + v8-04b doublewell 등).
- **★이식 금지**: v8-03b/02b D-PEAK 재정정 오류·v8-02b/03b/07b D-WEFF botch(¼·차원·orphan)·v8-01b self-test 산술오류·v8-01b 표값(이미 01b서 정정했으나 베이스는 06b).
- **v6 합류 용도**: 유도 사슬·부호·spinodal/χ_d 교차검증 + ★D-PEAK2 문턱 불연속 정직 기술 확정.
- **v8-11 잔여 적용**: D-PEAK2 문턱 불연속 1–2문장·D-WEFF 다리 검증본·3-pass 빌드·minor(반복 압축).

## Gate
PASS_REVIEW2 — 9 보완본 재검토·D-PEAK 정정 정확성 직접 검산·보완 회귀 3종 적발(이식 금지)·베이스 v8-06b·D-PEAK2 심화. 다음 = Phase 5.1(체리픽 v8-10, step 26).
