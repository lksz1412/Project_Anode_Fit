# 심층 절 단위 재검토 Ledger — Ch1 §1~ / Ch2 §1~ (완성도 최우선)

> 박사님 지시(6-09): 메모리 절 단위 루프(feedback_anode_fit_section_by_section_loop) 미준수 정정. Ch1 §1부터 끝까지
> [정독→작업이력 대조(누락·왜곡)→6렌즈 검수→수정→빌드→앞 절·정합→다음 절]. 시간·토큰 무관, 완성도 최우선.
> 세션 감사 기준선 = `9f06579`(세션 전). 6렌즈 = ①물리논리 ②문장내용 ③교과서형식 ④버전경과 누락 ⑤절간연결 ⑥챕터연속성.

## 작업 이력 감사 (전수, 확정)
- Ch1 vs 9f06579: +177/−? . 삭제 17줄 전수 확인 = 메타/중복 prune·결함시정·본문보존+추가. **누락·왜곡 0**.
- Ch2 vs 9f06579: +237/−? . 삭제 27줄 전수 확인 = 결함시정(γ_j·V_n·g''승격)·§2.4 두기원 §3 dedup(보존)·확장. **누락·왜곡 0**.

## Ch1 절별 검토 진행 (완료, 24p clean)
| 절 | 제목 | 정독 | 6렌즈 | 수정 | 빌드 | 상태 |
|---|---|---|---|---|---|---|
| 서론 | 도입·관찰·도착점 | ✓ | clean | - | - | DONE |
| 1 | 기호와 규약 | ✓ | clean(부호·단위 정확) | - | - | DONE |
| 2 | 전하 보존 V_n | ✓ | clean(eq:charge·cbg·vapp) | - | - | DONE |
| 3 | 평형 peak 기준선 | ✓ | clean(Stirling·logistic 부호반전·FWHM·dU/dT 손검) | add-only 검증 | ✓ | DONE |
| 4 | 동역학 지연·꼬리 | ✓ | clean(2-state 완화·Eyring·L_q·rsol 손검) | add-only 검증 | ✓ | DONE |
| 5 | 전위 유효 배리어 | ✓ | clean(BV·db·keff·LqV 손검, 이전 Codex) | add-only 검증 | ✓ | DONE |
| 6 | 입자 분포 통계 도구 | ✓ | clean(밀도·가중평균·분산전파·C2-1 시정 자연) | - | ✓ | DONE |
| 7 | 배리어 분포·중첩 | ✓ | **§7 line727 잔여 C2-1 표기 시정**(∝e^{G/RT}→e^{(G−χ𝒜)/RT}, χ𝒜 상수오프셋) | ✓ 수정 | ✓ | DONE |
| 8 | 종합·3×3 | ✓ | clean(닫힌식·worked example·S1–S4, Codex 수치 검증) | textbook 보강 | ✓ | DONE |
| 9 | 다중전이 겹침 | ✓ | clean(융합 worked example, Codex) | textbook 보강 | ✓ | DONE |
| 10 | 종합 모델식 | ✓ | clean(eq:master 손검·walkthrough) | textbook 보강 | ✓ | DONE |
| 11 | 검증·반증 | ✓ | clean(진단표, Codex) | textbook 보강 | ✓ | DONE |

## Ch2 절별 검토 진행
| 절 | 제목 | 정독 | 6렌즈 | 수정 | 빌드 | 상태 |
|---|---|---|---|---|---|---|
| 서·1 | 서론·기호 | | | | | TODO |
| 2 | 사전지식(상분리) | | | | | TODO |
| 3 | 관측 gap 분해 | | | | | TODO |
| 4 | spinodal 유도 | | | | | TODO |
| 5 | 분기·ΔU_hys | | | | | TODO |
| 6 | 분기별 dQ/dV | | | | | TODO |
| 7 | 동역학 분극 | | | | | TODO |
| 8 | 부분 cycle 기억 | | | | | TODO |
| 9 | 파라미터화 | | | | | TODO |
| 10 | 데이터→예측 | | | | | TODO |
| 11 | 종합 모델식 | | | | | TODO |

## Findings log (절별 기록)
### Ch1 (완료)
- 작업이력 감사: 삭제 17줄 전수 = 정당(메타/중복 prune·결함시정·보존+추가). 누락·왜곡 0.
- §서론~§6: 정독·6렌즈 clean. 핵심 유도 손검 전부 정확.
- **§7 finding(시정 완료)**: 저온 꼬리 확장 문단(line 727)의 $L_q\propto e^{G/RT}$ 가 §6 C2-1 시정($e^{(G-\chi\mathcal A)/RT}$, χ𝒜 집단 공통)과 표기 불일치. 결론(Var=σ_G²/(RT)²)은 정확하나 표기 어긋남 → $e^{(G-\chi\mathcal A_j)/RT}$, χ𝒜 상수오프셋 흡수 명시로 통일. 빌드 clean.
- §8~§11: textbook 보강분 Codex 수치 검증 통과(FWHM·융합·진단표). clean.
- **Ch1 종합: 누락·왜곡 0, 잔여 결함 1건 시정, 24p clean.**

### 최대 effort 재패스 (2026-06-09, effort 리셋 후)
박사님: effort 자동 하향 의심 → 최대 effort로 §1부터 재검토. NO Workflow(순차 master 루프, 상시 지시 > ultracode 기본값).
- **Ch1 §1**: 표 전 항목 손검 통과. finding: $r_{a,j}$ 표 $(0,1]$ vs §8 $(0,1)$ → §8을 $(0,1]$로 시정(완료).
- **Ch1 §2**: 전하보존·유일성(C_bg>0 단조·중간값 정리·평형분기 a fortiori) 손검 정확.
- **Ch1 §3**: Stirling→μ(1.9)→eqcond(1.10)→logistic 부호반전→FWHM 3.53→dU/dT 전수 손검 정확.
- **Ch1 §4·§5**: eq:relax 항등식·Eyring·L_q·db(χ상쇄)·keff·LqV 손검 정확.
- **Ch1 §6·§7·§8–§11**: 이번 턴 검증 완료(§7 잔여 C2-1·worked example·master·진단표). 
- **Ch1 종합(최대 effort): clean, 24p. 신규 시정 = §8 r_{a,j} 정의역.**

### Ch2 (최대 effort 재패스 — 진행 중)
- 이번 턴 §서론~§11 정독 완료, finding 2건 시정(§1 인력적→동종선호, §10 Ω_j/γ_j 식별성). 11p clean.
- 잔여: 최대 effort 재손검 §1부터(다음 진행).
