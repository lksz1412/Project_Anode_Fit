# V1.0.16 EXECUTION LEDGER — 폭 다중도 n 의 온도 함수 n(T) 피팅 지원 (fit-n·실측 T·config 전파)

> 근거 = `../../docs/v1.0.15/CLOSING_v1.0.15.md` Part 4(확정 w/T 방향). 방법 = v1.0.15 동일(증판·phase·검수·verify·phase별 commit+push). 상태 ⬜/🔄/✅.

## 방향 (CLOSING Part 4)
폭은 w 맨값이 아니라 **n으로 fit**(w=n·RT/F, RT/F 앵커). **실측 T 투입**. 폭 T-의존은 가정 아닌 데이터 확정 **4단 사다리**(상수 n → per-T 진단 → 상수 w 전환 → 최소 n(T)). **n(T)로 가면 가역열 config 항 ∂w/∂T=(R/F)(n+T·n′) 동반**. v1.0.16 = 이 방향을 문건+코드에 반영(코드 = n(T) 선형 지원 additive).

| Phase | 이름 | 산출 | Gate | 상태 |
|---|---|---|---|---|
| P1 | 증판(v1.0.15→v1.0.16) | docs/v1.0.16 | 빌드·회귀 bit-exact | ✅ |
| P2 | 코드 n(T) 선형 지원 + config 전파 | _n_factor·_dwdT·entropy_coefficient | round-trip·bit-exact·golden | ✅ |
| P3 | FITTING_GUIDE(fit-n·실측 T·4단·n(T)) | guide | 명문화·정합 | ⬜ |
| P4 | Ch1/Ch2(fit-n·T-진단·n(T) config 수식주도) | ch1/ch2 | 빌드·헌법 3종·D1-6 | ⬜ |
| P5 | 적대검수 + 3대 무결 + HANDOVER·INDEX | 마감 | 3대 무결·최종 | ⬜ |

## 진행 로그 (append-only)
- **2026-07-06 P1 증판**: docs/v1.0.15 소스 → docs/v1.0.16 복제(tex 3·py 6·guide·golden·figs). 버전 태그 rename(파일명·현행 선언·코드 참조 → 1.0.16, 이력·temporal 보존). baseline gate green: Ch1 58p·Ch2 16p·appendix 8p 전부 exit0/undefined0/of>10 0, 회귀 GRAPHITE 0-DIFF PASS(코드 bit-identical).
- **2026-07-06 P2 코드 n(T)**: 3개 변경 — ①`_n_factor` 'n' 경로에 선형 n(T)=n+n_T1·(T−n_T_ref) 지원(dict 키 'n_T1'[1/K]·'n_T_ref'[K], 부재=상수 n) ②신설 `_dwdT`=∂w/∂T=(R/F)(n(T)+T·n_T1)(상수 n → n·R/F bit-exact, 'w'-단독·기본 → 0) ③`entropy_coefficient` config 항 = _dwdT·ln[ξ/(1−ξ)](n_j·R/F 대체, n(T) 정합). **검증**: import OK·회귀 bit-exact(상수 n, 골든 불변→재캡처 불요)·**config 전파 round-trip 정확**(해석 entropy_coefficient = U_oc(T) 유한차분: 단일 전이 0.0000 μV/K·다전이[2→1 n_T1=0.004] 0.0003 μV/K)·다운스트림 demo/sample/suite/plot 전부 exit0. additive(n_T1 부재 시 v1.0.15 완전 동일).
