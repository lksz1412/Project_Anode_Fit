# P5 Step2 — 검토1 (별도 세션 Opus, 9감사 통합·적대적 교차검증) 결과

> 9 감사(S1-3·O1-3·C1-3) + 코드 850줄 + Ch1/Ch2 tex 직접 대조(드래프트 인용 무승계·재검증). ★검토자 자체 grep 함정(`\_` 이스케이프) 정정 후 확정.

## ① 명명 갭 정정방향 — **코드 불변, Ch1 4곳 → `LCO_MSMR_LIT`** [확정]
- Ch1 `\code{LCO\_STAGING\_LIT}` 4곳: **L312·L322(tab:lco-staging cap)·L1750(sec:lco-code)·L1844(tab:nodemap)**.
- 코드 `LCO_MSMR_LIT`(L621 정의) + demo_lco_heat.py L27/28/31 + P4 RESULT — **코드 생태계 전체 MSMR self-consistent**. 코드 L615-618 헤더 "MSMR 동형"이 명명 뒷받침.
- 판정: (a) 코드 변경 0=흑연 0-diff·식별자 보존 절대부합 (b) demo까지 MSMR라 코드측 파급 큼 (c) MSMR 물리명명 정당 → **Ch1 4곳 `LCO_STAGING_LIT`→`LCO_MSMR_LIT` 치환**. **Sonnet 3종 전원 이 최중대 갭 놓침**(A조 code↔Ch1인데 식별자 대조 누락); O1·O3·C1·C3 적발.

## ② x_MIT/전위/전이 — **코드 tier-C 값 유지 + Ch1 분리 라벨** [확정]
Ch1 tab:lco-staging(L326-337)·eq:ggate(L1069-70) 실제값 vs 코드:
| | Ch1 | 코드 LCO_MSMR_LIT |
|---|---|---|
| T1 | ~3.90V·x0.94-0.75·**MIT 전자항 ON** | 3.930V·전자항 없음 |
| T2 | ~4.05V·x≈0.55·off | 3.880V·**electronic=True**·x_center0.50 |
| T3 | ~4.17-4.20V·x≈0.48 | 4.050V·off |
| x_MIT | **≈0.85** | 0.50 |
- **3중 불일치**: 전자항 배정 위치(Ch1 T1 최저전위↔코드 중간)·x_MIT 값·T3 부재. **단순 T3 누락보다 깊음.**
- 정정: 코드 데모값 **tier-C라 지금 코드 수치 안 고침**(round-trip 이월, P4 결정 계승). Ch1 tab:lco-staging에 "코드 LCO_MSMR_LIT 시연값(3.930/3.880/4.050·x_MIT0.50)=tier-C placeholder, 물리 anchor(T1 MIT 3.90·x_MIT≈0.85·T3 4.17)와 별개·round-trip 정합" 각주.
- **흑연 0-diff 무영향**(LCO 데이터만, 흑연 클래스·GRAPHITE_STAGING_LIT 미접촉) [확정].

## ③ 확정 갭 (문서측·코드값 불변) · 기각 갭
| ID | 위치 | 정정 | 등급 |
|---|---|---|---|
| 명명 | Ch1 L312·322·1750·1844 | `LCO\_STAGING\_LIT`→`LCO\_MSMR\_LIT`(4곳) | HIGH |
| x_MIT/전이표 | Ch1 tab:lco-staging·eq:ggate | tier-C vs anchor 분리 각주 | MED |
| 파일명 | Ch1 **L133 본문** + 헤더 L46 `Anode\_Fit\_v11\_final.py` | →`v1.0.10.py`(L3는 이미 1.0.10, 내부충돌) | LOW |
| nodemap | Ch1 L1832 `dqdv L408` | 실제 분극줄=**L430** | LOW |
| x↔ξ 라벨 | Ch1 sec:lco-decomp | "P4=x_center 상수동결(단일-기준), x↔ξ 매핑=다온도 round-trip" 1줄(현재 코드 docstring L659-664에만) | LOW·defer |
| eq:hys_rev 라벨 | 코드 entropy_coefficient docstring / Ch2 | "히스 분기평균=평형중심 자동근사(γ대칭)·비대칭 미구현" 1줄 | LOW |

**기각(refute — 결함 아님)**: config 부호(Ch1 L1698 S_config 미분형↔코드 L571 ∂U/∂T 기여형, Ch2 L488과 삼자일치·부호 맞물림) · 비가역 3분해(Ch2 boxed 부재 확정, 코드 lumped 정합) · FD 175점(numverif2026 내부검증 인용, 허위 아님) · LCO Ω/γ 미지정(tier-C 선택, ② 묶음).

## ④ 코드없는내용 = 0 — **PASS(조건부→라벨 승격 시 무조건)** [확정]
x↔ξ 매핑·T² 곡률 모두 Ch1/코드 docstring/P4 §11 self-label → 허위 아님. 단 x↔ξ·hys_rev defer 라벨이 **코드 docstring에만 강하고 본문엔 약함** → 본문 승격(③ 라벨)하면 오독 0·무조건 PASS. C3 "조건부 FAIL"은 과함 = 실제 PASS + 라벨 6건.

## ⑤ 피팅 문건 목차 + 그래프 suite (통합)
**피팅 문건**: (1) 파라미터 tier 표(scope·initial·bounds·constraint·required-data·release-status: Tier-1 peak골격 U_j/ΔH/ΔS·n>0·Q·Cbg / Tier-2 히스 Ω>2RT·γ·χ·Rn / Tier-3 꼬리 dH_a·dVdq_qa(누락=silent off) / Tier-4 다온도 ΔS·dS_a / LCO 전자항 g_max·x_MIT(0.50/anchor0.85)·dx) (2) round-trip 5-Phase(A 저율 peak→B 충방전 Ω·γ→C rate 꼬리→D 다온도 ΔS·전자항→E holdout) — L_V직접 vs 물리fit tier분리(과식별 금지) (3) 초기값·bounds+가드 미커버 bound wrapper강제 (4) 수렴판정 잔차<1e-4·ΣQ∈[0.95,1.05]·U_j 순서·**흑연 0-diff assert**.
**그래프 suite V1-V9**: V1 흑연+LCO 나란히·**V2 round-trip 복원 parity(핵심 신뢰 가드)**·V3 q_rev 흡발열 교대·V4 ∂U/∂T 완전식vs단순식vs FD·V5 온도의존 peak이동·V6 전자항 골 x_MIT 0.50vs0.85 오버레이·**V7 다온도 T² 곡률(선형기준선+예상곡률, 현 동결근사=선형 주의라벨)**·V8 히스분기 split·V9 면적보존 회귀. (기존 plot_dqdv·demo_lco_heat = PASS 분류.)

## ⑥ 가장 약한 1곳
**전자항 dict 배정 구조 불일치**(9 드래프트 정면 미짚음): Ch1은 전자항을 T1(3.90V·최고x·MIT)에, 코드는 중간(3.880V·x_center0.50)에. x_MIT 값만의 문제 아니라 "어느 전이가 MIT인가" 재배정. → **round-trip 청사진에 "전자항 dict를 Ch1 T1(최고x·최저V) 기준 재정렬" 단계 명시**(나중 조용히 틀림 방지).

## ⑦ master 마감 주의 5줄
1. **흑연 0-diff 절대 유지** — 정정 전부 Ch1/Ch2 tex 문자열·라벨 + LCO docstring 한정. GraphiteAnodeDischargeDQDV·func_*·GRAPHITE_STAGING_LIT·seam base 1바이트도 X(정정 후 13/13 재확인).
2. **코드값 안 고침** — 명명=Ch1 4곳 치환(코드/demo 불변), x_MIT·전위=tier-C 분리 라벨. LCO 물리값 정정=round-trip 이월.
3. **덮어쓰기 금지** — P4 RESULT·9드래프트·이월 문건 불가침. tex in-place 최소편집만.
4. **defer 라벨 본문 승격** — x↔ξ·hys_rev·T² "미구현·다온도 과제" 코드 docstring→Ch1/Ch2 본문 1줄씩 → 코드없는내용 0 무조건 PASS.
5. **기각 갭 재소환 금지** — config 부호·3분해·FD·Ω/γ 확정 갭 아님. P4 gate(CRIT/HIGH 0) 승계 유효·확정 갭 전건 LOW~MED(명명만 HIGH·문서 4곳 즉시해소). **3대 무결(물리·코드·의도) 최종 확정.**
