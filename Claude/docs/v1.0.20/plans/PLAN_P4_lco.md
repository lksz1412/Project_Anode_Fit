# Phase P4 세부 계획서 — Ch1 LCO Part II §11–§17: 수식사슬·중간다리 대보강 (Steps 45–62)

## Summary
F-4(LCO — 신규 내용 과다·설명 부족·수식 전개 띄엄띄엄) 해소. 핵심 = §15 전자 엔트로피(최밀집 최첨단부)에 Mott/MIT 배경 bgbox + FD→Sommerfeld 유도 완결성 점검(D7), §13 order–disorder/MIT 문헌 다리(vanderven1998·marianetti2004 등), §17 MSMR 원 논문 정확 대응(msmr_origin2017·bakerverbrugge2018), U5~U8·U11 해소. 대형 신규 콘텐츠 유닛은 경쟁 저작(N=4), 국소 인용·다리는 master 직접.

## Current Ground Truth
sec11 전문 정독(기획 세션). sec12~17 미정독 → Steps 46–48 에서 전문 정독 후 경쟁 유닛 범위 확정(정독 전 확정 금지 — P3 의 KWW 기각 교훈). 원장 V1 대기: imada1998·mott1968·marianetti2004·vanderven1998·msmr_origin2017·bakerverbrugge2018·(ashcroftmermin1976 = ch1_bib 등재 완료).

## Phase Range
P4 단독(Steps 45–62).

## Non-goals
물리 모델·수치·기존 라벨 변경 X. 이월 3건(LCO tier-2/3 실측·다온도 T-복원·q_irr)은 범위 밖 유지. 자산(물리 내용·수치·경고·Gn 선언) 유실 0 — 산문 압축은 중복·수사에 한정.

## Phase P4 Steps
| Step | 내용 | Gate |
|---|---|---|
| 45 | 본 계획서 저장 | 파일 |
| 46–48 | sec12·13 / sec14·15 / sec16·17 전문 정독 + 보강 지도 작성(다리 필요처·D3 점프·압축 후보·경쟁 유닛 확정) | Read Coverage·보강 지도 |
| 49 | CHANGE_LOG 사전 등재(보강 B-00x·서지추가 C-01x) + 경쟁 브리프(확정 유닛) | 등재·브리프 |
| 50–52 | ★경쟁 초안 4본(Opus×3+Fable×1, 병렬) — 유닛별 | 4본 존재 |
| 53–55 | master 교차검토·체리픽 통합(유닛별) + PICK_JUDGMENT | 기록 |
| 56–58 | master 직접분: U5~U8·U11 인용 부여·§13/§17 다리·bib 등재·산문 압축(자산 보존) | 편집 완료 |
| 59 | 빌드 3-pass + 구조 + diff(변경 ↔ CHANGE_LOG 1:1) | GREEN |
| 60 | 후방 정합: Part I(전극-중립 골격·§10 접속)·§18/부록 접합·용어 rubric | 대조 기록 |
| 61 | baseline 처리 기입·기록(STEP_LOG·RESULT·ledger) | 기록 |
| 62 | 커밋+푸시 | 해시 |

## Implementation Interfaces
경쟁 프로토콜 = 마스터플랜 공통 절(comp_P4_<unit>/ 폴더). D8 다리 양식·D7 2단 양식 = rubric. 신규 자산 태그 [V20-0xx].

## Test Plan
빌드 err0/undef0·cite↔bib 정합·자산 앵커 336 보존·diff↔CHANGE_LOG 1:1·U5~U8·U11 전건 처리.

## Assumptions
정독 결과에 따라 경쟁 유닛 수(1~2)와 범위를 Step 48 에서 확정(Correction History 에 기록). 압축은 물리 내용 무손실 원칙이 분량 감소보다 우선.

## Correction History
(초판 — 유닛 확정은 Step 48 후 추기)
