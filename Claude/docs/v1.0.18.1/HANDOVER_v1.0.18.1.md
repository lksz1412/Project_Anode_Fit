# HANDOVER v1.0.18.1 — v1.0.17 register/정합 이월 완결 (물리 무변경)

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` (v1.0.18.1 완결 = 2-버전 중 이월판)
- 근거 = `plans/2026-07-08-v1018-physics-extension-master-plan.md`(§9 Decision Gate 2-버전 결정) ← `docs/v1.0.17/HANDOVER_v1.0.17.md`(register 정련·이월 목록) ← v1.0.16(n(T)) ← v1.0.15(격자 퇴출) ← …
- 레저 = `results/process/V1018_EXECUTION_LEDGER.md`(P1~P3=18.1). 자매판 = **v1.0.18.2**(= 18.1 + 제안1 vib Einstein + 로드맵, 진행).

## ① 본 세션 지시·작업 요약
**지시**(사용자): 신규 발전 제안서 + 이월 + 누적 이력 → v1.0.18 방향 검토. **결정 = 2-버전 제작**: **18.1 = 이월 완결만** / 18.2 = 18.1 + 제안1(vib Einstein) + 제안2~5 로드맵. Opus(master)+Sonnet 로 가능한 모든 건·phase별 commit+push(회사 GitHub 확인). 최종 Fable 검수 1회 best-effort(맨 끝).

**18.1 = v1.0.17 register/정합 이월 [선택] 완결**(doc-only·물리 무변경·matched bit-exact). Sonnet 서브세션 2(Ch1·Appendix, 자체 빌드) → master 적대검증·통합:
- **Ch1 8건**: ① "극한 검산" 5문단 verifybox 감쌈(정의만 됐던 박스 활성) ② tab:inputs·tab:nodecode longtable 전환 ③ tab:signcheck-R 판정열(✓) 추가 ④ tab:staging 서식(footnotesize·arraystretch 1.3) 통일 ⑤ z 각주(logistic 인자 vs 배위수/전하수 구분) ⑥ ω_0→ω_i·ω_i→ω_k 전환 다리 문장 2 ⑦ §sm-lattice n→N 통일(단일자리 n_k∈{0,1} 불변) ⑧ U_j 유도 (b)(c) 병합 라벨. + **tab:notation \endfirsthead 추가**(master — v1.0.17 잔존 "Label multiply defined" 해소).
- **Appendix 4건**: N_A(아보가드로) vs N_A(A종수) 각주·γ 옆 v_m/Δg_v 단위 병기·(c) 분류표 라벨(표 지칭)·§app:kinetics 도입 note((a-d) 축약 명시).
- **빌드 GREEN**: Ch1 59p·Ch2 16p·appendix 8p·전 undef0/multiply0/of>10 0/err0 · **회귀 GRAPHITE 0-DIFF PASS**(코드 bit-identical).

## ② 다음 세션 주의
1. **물리·코드 무변경**: 18.1 은 register/서식/라벨만. 방정식·수치·식별자 불변. 코드 = matched bump(bit-exact). Ch1 58p→59p 는 verifybox 박스·각주·다리·longtable 헤더 오버헤드(콘텐츠 자연 증가, 결함 아님).
2. **N/n 통일 과치환 주의**: §sm-lattice 의 입자수 n→N 만 바꿈. §sm-site 단일자리 이진 n_k∈{0,1} 은 보존. (적대검증에서 과치환 여부 확인.)
3. **자매판 18.2**: 18.1 을 증판 base 로 제안1(vib Einstein) 물리 구현 + 제안2~5 로드맵. 회사는 안전 폴백판(18.1)/물리판(18.2) 선택 가능.

## ③ 미완료/이월
- **의도적 보류(애매·저가치)**: 마스터표(tab:notation) N3 그룹 물리적 재배열(#5) — "평형 중심·폭·진행률(N2·N4·N5)" 그룹을 쪼개 N3 를 N2/N4 사이로 넣어야 하는데, N2·N4·N5 를 하나로 묶은 현 그룹핑(평형 peak 량 묶음 → 히스 → 동역학)도 논리적으로 타당하고 단일 이동으로는 파이프라인 순서(N2→N3→N4)를 못 맞춤. 그룹헤더 분할은 판단 필요 → 현행 유지가 합리적. (원치 않으면 후속 재배열.)
- v1.0.16 물리-데이터 이월(다온도 per-T n 진단 등) = 18.2 로드맵에서 캡처.
