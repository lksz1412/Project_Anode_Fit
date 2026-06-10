# HANDOVER — Ch1 교과서 수준 전면 재작업 (2026-06-10, Fable)

## Chain 헤더 (거슬러 올라갈 위치, 최상단 리스트만으로 추적 가능)
- 본 handover ← `Claude/results/HANDOVER_2026-06-07_ch2-5-overnight.md`(구 ch2~5 야간 초안) ← `Claude/results/Archive_oldtrack/HANDOVER_RB_2026-06-02b.md`(구-track rb-rebuild)
- 6-08(장 의존 트리 재편: new Ch2=반속(ch4 파일)·Ch3=발열)·6-09(병합·보강)·6-10 주간(FRR 13라운드, `PHASE_FRR_*`) 세션들은 별도 handover 없이 result/ledger 로 기록 — `PHASE_FRR_EXECUTION_LEDGER.md`·`PHASE_FRR_ROUNDS_RESULT.md` 참조.

## 1. 본 세션 지시 (전문 요지, 왜곡 없이)
모델 교체(Opus→Fable) 후 두 단계 지시.
(A) 주간: "작업 방식 그대로 처음부터 전면 재검토(절별 재작업 수준), 복붙-완료 금지, 절 시작 전 CLAUDE.md·메모리 확인, 전문 정독, 물리 결함 수정+교과서 해설 타당성, 10회 재검토(매회 커밋·푸쉬), 계획서 승인 후 무중단 자율, .tex/pdf 덮어쓰기 금지 — `_Fable` 접미 사본에서 작업" + /goal 보강("리뷰 논문급 깊이, 10회=하한, 완결성까지 루프").
(B) 야간 /goal(본 작업): "동일 계획서·동일 지시. 직전 결과 일부 개선됐으나 불만 — ①조사만 바꾸는 토큰 낭비 금지 ②'V_n 이 아니다(분극이 섞여있다)' 류 괄호 구어체 금지 ③§1.9 이후 절간 단절 ④보편식→코너 케이스 순서 위반(꼬리 극한의 전 구간 확장) ⑤피팅 지시 불명료 ⑥분량 36p(50p 넘어야) — Ch1 한정, 방전 메인·히스 덤, 절마다 [위치 파악→계획→계획 검수→작업→작업 검수→커밋→푸쉬], 병렬 최소화·순차, 이 문건만 보고 dQ/dV 피팅 코드를 짤 수 있는 수준, 보완 10회+, 컴팩션 시 계획서+본문 전문 재독."

## 2. 수행 결과
- 계획: `Claude/plans/2026-06-10-ch1-textbook-rewrite-plan.md`(11-section). Ledger: `PHASE_TBR_EXECUTION_LEDGER.md`. 라운드: `PHASE_TBR_ROUNDS_RESULT.md`. Result: `PHASE_TBR_ch1_RESULT.md`. 검수 보조: `TBR_BEFORE_AFTER_REVIEW_AID.md`.
- 본작업 T.1 = 절별 재작성 18단위(절당 커밋) + T.2 게이트. 보완 T.R = **R1~R17**(R17=실행 실증: 문건 사양 그대로의 피팅 코드 round-trip PASS)(문체 전수/흐름 통독/★코드 작성 시뮬/★신규 물리 적대 검산/분량/해설 비약/그림/검증/실용/진단표/그림2/확인/50p 돌파/검증/확인/★PDF 시각 판독).
- 최종: `Claude/docs/graphite_ica_ch1_Fable.tex|pdf` = **50p/2428행/그림 9/연습문제 7/참조표·진단표·모듈 스켈레톤**, 빌드 0/0, 번호식 55 불변(ch3·ch4 인계 13종 포함), 원본 불가침. R15 텍스트 수렴 0건 + R16 시각 판독 무결. 커밋 `d7d6c4d`→`5f35297`(약 50커밋, 전부 push, branch rb-rebuild-2026-05-30).
- 사용자 4클래스: 인용 문구 3건 grep 0건 실증, 일반해-먼저 재구성(§1.5·§1.6), 본론 종결/확장 선언(§1.11/§1.12), 피팅 알고리즘 소절(§1.16) — 상세는 `TBR_BEFORE_AFTER_REVIEW_AID.md`.

## 3. 미완료 항목
- **사용자 본인 검수**만 남음(Stop hook 의 "완벽한 교과서" 판정은 사용자 주관 — 부재로 미확인). 추가 지적 시 같은 절 단위 루프로 재개.
- ch3(발열)·ch4(반속, 표제 Chapter 2)는 본 세션 범위 외(Ch1 한정 지시) — Ch1 의 §1.5 eq:Lq 가 원천항 포함 보편형으로 일반화됐으나 L_q 정의 보존이라 ch3 (1.23) 인용 정합 확인 완료. 단 ch3·ch4 를 다음에 열 때 Ch1 신판 기준 재검토 권장(특히 eq:Lq 인용 문맥).
- (R17 완료) 합성 round-trip 실증 — `results/TBR_R17_roundtrip/`(코드+로그, PASS: U/w/Q ±0.1mV/±0.001, Ω 4.07 vs 4.00 RT₀, γ 0.573 vs 0.600). 잔여 선택 과제(사용자 결정 대기): Ω=8RT₀ 퇴화 시나리오의 별도 round-trip(조건 명시됨), 결과 수치의 본문 부록화 여부.

## 4. 다음 세션 주의
- 작업본은 `_Fable` 접미 파일이 정본 작업 트랙. 원본 `graphite_ica_ch1.tex` 절대 불가침 유지.
- 번호식 게이트: 신규 식은 무번호(equation*/align*/gather*)만 — .aux 라벨→번호 55개 diff(`/tmp/tbr_baseline_eq.txt` 는 세션 휘발 — 재생성: aux 에서 grep) 불변 확인 후 커밋.
- 본문 수정은 Temp python 스크립트(UTF-8, assert count==1) 패턴 — bash heredoc/인라인은 이스케이프 사고 多(`\f` 폼피드 등). 체인은 전부 `&&`(no-op 커밋 방지).
- xelatex 는 반드시 `Claude/docs` 에서 2-pass. Overfull 게이트는 광역 grep('Overfull') 기준.
- 절 작업 = 절 단위 루프(통째 배치 금지), 절당 커밋+푸쉬, 병렬은 검수 Agent 1개씩.
- PDF 시각 검증 도구: pdftoppm(MiKTeX 내장) — 그림 페이지는 aux 의 newlabel{fig:..} 에서 추출.
