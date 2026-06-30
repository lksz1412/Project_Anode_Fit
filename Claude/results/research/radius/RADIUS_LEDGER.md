# RADIUS_LEDGER — 조사 트랙 실행 원장 (12-col)

| Step | Phase | 작업 | 주체 | 입력 | 산출 | 도구 | 검증/Gate | tier 분포 | 결함/수정 | 출처폐쇄 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | v8-11.tex·v11_final.py 정독·전제 grounding | master | tex 1209행·py | 모델구조 확인(weff·peak·꼬리) | Read/Grep | func_w_eff floor 코드 확인 | 확정 | — | 코드:line | done |
| 2 | 0 | 연구질문6·검색전략·전제 1차판정 | master | 모델 | 00_scope.md | Write | Ω>2RT→δ Maxwell 논리 | 확정(논리) | — | 자체식 | done |
| 3 | 1 | 축A 단일입자+ensemble 조사 | 서브A | scope | 10_*.md | Agent+web | 4카드 출처/tier | 확정·추정·미검증 | autocat/avalanche 반례 포착 | DOI | done |
| 4 | 1 | 축B 반경→U_j 결합·정량 | 서브B | scope | 11_*.md | Agent+web | ΔV 계산·22nm 임계 | 추정(값)·확정(1/r) | ★마이크론 1000배 갭 | DOI+계산 | done |
| 5 | 1 | 축C 역문제·PSD·DOS | 서브C | scope | 12_*.md | Agent+web | Fredholm/DRT 동형 | 확정(ill-posed)·추정 | dQ/dV→PSD 선례 부재 | DOI | done |
| 6 | 1 | 축D 경쟁 broadening·흑연 정량 | 서브D | scope | 13_*.md | Agent+web | 70mV·C-rate 분리신호 | 확정·추정·근거미발견 | 반경 평형mV 미발견 | DOI | done |
| 7 | 2 | 4카드 master 전수 정독·삼각검증 | master | 4카드 | (검증 노트) | Read | ≥2 독립·sub요약 비신뢰 | — | sub 주장 직접확인 | — | done |
| 8 | 2 | 종합·사슬 커버맵·경쟁 매트릭스 | master | 4카드 | 20_synthesis.md | Write | 5고리 충족판정·갭 정직 | 4-tier | — | DOI | done |
| 9 | 3 | verdict 작성 | master | 종합 | RADIUS_VERDICT.md | Write | 판정·조건·한계·권고 | 4-tier | — | DOI | done |
| 10 | 3 | RESULT·ledger·report | master | 전체 | RESULT·ledger·50_report | Write | 11항목·12col | — | — | — | done |

## Round 2 — "종모양의 진짜 원인" (apparent-U 분포 기원)
| Step | Phase | 작업 | 주체 | 산출 | 검증/Gate | tier | 핵심 결과 | 상태 |
|---|---|---|---|---|---|---|---|---|
| 11 | R2-0 | 재구성·scope(true-U vs apparent-U) | master | 30_scope_origin.md | 3계층 분리 논리 | 확정(논리) | 분포 비필수·η 분포 재정식 | done |
| 12 | R2-1 | 축E 분포없는 종모양 | 서브E | 31_*.md | 전이별 1차/연속 | 확정·추정 | U_j분포 필수 반박; LiC12/LiC6만 강1차 | done |
| 13 | R2-1 | 축F 크기 kinetic 분산(신가설) | 서브F | 32_*.md | τ∝r²·C-rate | 확정(기작)·추정(mV) | ★신가설 강지지; Yang2023 operando | done |
| 14 | R2-1 | 축G apparent-U 원인 순위·분해법 | 서브G | 33_*.md | 8원인 순위·lever | 확정·추정 | 지배=율속꼬리+PSD분산; 참U≈0 | done |
| 15 | R2-2 | 3카드 master 정독·삼각검증 | master | (노트) | ≥2 독립 | — | sub 주장 직접확인 | done |
| 16 | R2-3 | 종합 verdict | master | ORIGIN_VERDICT.md | 3줄답·계층·분해·모델 | 4-tier | 종모양=율속+PSD분산+RT/F | done |

## Round 3 — GITT 비-델타 + 밴드/DOS 채널
| Step | Phase | 작업 | 주체 | 산출 | tier | 핵심 결과 | 상태 |
|---|---|---|---|---|---|---|---|
| 17 | R3-0 | 재구성·scope(GITT 평형성·양자가둠 1차계산) | master | 40_scope_band.md | 확정(논리·계산) | 양자가둠 µm=15 neV·과교정 선언 | done |
| 18 | R3-1 | 축H GITT 잔여폭 기원 | 서브H | 41_*.md | 확정·추정 | 주범=미평형/히스(Mercer·Dreyer)≠U분포 | done |
| 19 | R3-1 | 축I 밴드/DOS·크기 스케일 | 서브I | 42_*.md | 확정·추정+계산 | dQ/dV=DOS 옳음; µm 양자효과 sub-meV | done |
| 20 | R3-1 | 축J 구조무질서 이질성 | 서브J | 43_*.md | 확정(기작)·미검증(정량) | 평형 U분포 후보 O, 반경 독립 | done |
| 21 | R3-2 | 3카드 master 정독·삼각검증 | master | (노트) | — | 42 전문정독·41/43 검증 | done |
| 22 | R3-3 | 종합 verdict | master | BAND_VERDICT.md | 4-tier | 반경=평형 핸들 무효(전 채널)·동역학만 | done |

## Next Step
- (실측·교수님 검토 후) C-rate 사다리+GITT 분리 실험 설계 / 독립 PSD 상관 검정 / 단일입자 dQ/dV 상한.
- (공백 보강) ScienceDirect 본문 정식 접근으로 snippet 출처(est.2019·Maire·Senyshyn·Farkhondeh) tier 승격. 흑연 평형 입경의존·흑연 γ 실측 추가 조사.
- (모델, 범위 외) 분포 항 도입 시 일반 U_j 이질성 + C-rate 식별구속.
