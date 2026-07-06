# HANDOVER v1.0.16 — 폭 다중도 n 의 온도 함수 n(T) 피팅 지원 (fit-n·실측 T·config 전파)

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.16/HANDOVER_v1.0.16.md` (v1.0.16 완결)
- 근거 = `docs/v1.0.15/CLOSING_v1.0.15.md` Part 4(확정 w/T 방향) ← `docs/v1.0.15/HANDOVER_v1.0.15.md`(격자 퇴출) ← `docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` ← v1.0.14 ← …
- 계획/레저 = `Claude/results/process/V1016_EXECUTION_LEDGER.md`. 커밋 = 0e50486(P1+P2)·94084e0(P3)·eec87b5(P4)·P5.

## ① 본 세션 지시·작업 요약
**지시**(사용자): CLOSING_v1.0.15 Part 4 확정 방향을 v1.0.16 문건+코드에 반영. **팝업·결정 대기 없이** 자율 진행·매 phase commit+push(회사 실시간 pull). 방법 = v1.0.15 동일.

**확정 방향(CLOSING Part 4)**: 폭은 w 맨값 아닌 **n 으로 fit**(w=n·RT/F 앵커)·**실측 T 투입**·폭 T-의존은 데이터 확정 **4단 사다리**(상수 n → per-T 진단 → 상수 w 전환 → 최소 n(T))·n(T)면 **가역열 config ∂w/∂T=(R/F)(n+T·n′) 동반**.

**완주(P1–P5, 전건 커밋·push)**:
- **P1 증판**: docs/v1.0.15 → docs/v1.0.16(버전태그·이력 보존). baseline green.
- **P2 코드 n(T)**: `_n_factor` 'n' 경로 선형 n(T)=n+n_T1·(T−n_T_ref)(dict 키 `'n_T1'`[1/K]·`'n_T_ref'`[K], 부재=상수 n)·신설 `_dwdT`=∂w/∂T=(R/F)(n(T)+T·n_T1)·`entropy_coefficient` config 항 전파. round-trip 정확·회귀 bit-exact.
- **P3 FITTING_GUIDE**: §1.5 폭 피팅 규약(fit-n·실측 T·4단·n(T)) + v1.0.15 격자 debt 정정(ν·min_lag_grid·23% 점프 → 점별).
- **P4 Ch1/Ch2**: n(T) config 일반화 수식-주도(Ch2 신설 eq:dwdT-nT·Ch1 교차참조).
- **P5 검수·마감**: 2 렌즈 적대검수 → 6결함 수정(배열 T 지원·w>0 가드·n_T1 가드·비유한 가드·FITTING_GUIDE ν 잔여·Ch1/Ch2 정밀). 3대 무결·HANDOVER·INDEX.

## ② 다음 세션 주의
1. **n(T) = additive**: 전이 dict 에 `'n_T1'`(+`'n_T_ref'`) 없으면 상수 n = v1.0.15 완전 bit-exact(골든 불변). `'n_T1'` 은 반드시 `'n'` 과 함께(없으면 ValueError). n(T)≤0 이면 폭≤0 → `_width` 가 fail-fast.
2. **배열 T(V)**: `dqdv`·`entropy_coefficient`·`reversible_heat` 전부 스칼라(등온)/V 길이 배열 T(V)(비등온) 지원. 각 점 실측 온도 반영.
3. **4단 사다리는 실행 대기**: 코드·문건은 n(T) 를 지원할 뿐, **어느 전이를 상수 n/상수 w/n(T) 로 둘지는 다온도 실데이터 per-T 진단이 정한다**(FITTING_GUIDE §1.5). 무단 배정 X.
4. **golden**: 상수 n bit-exact 라 v1.0.15 골든 그대로(재캡처 불요). n(T) 나 코드 알고리즘을 실제 바꾸면 검증 후 재캡처.
5. **staging 'w'/'n'** = v1.0.15 와 동일 의도 설계(폭 폴백·'n':1 실폭 25.7mV; 좁은 폭은 'n' 제거=피팅 선택).

## ③ 미완료/이월 (실데이터 소관)
- 다온도 실측으로 per-T n 상수성 진단 → two-phase 폭 T-의존 확정(4단 사다리 (2)~(4) 실행). LCO Ω/dH_a 실값·다온도 T² 실측·서지 재확인(v1.0.15 이월 유지).
