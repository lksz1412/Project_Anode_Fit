# HANDOVER — Ch1 백지 재작성 v2 (Eyring 척추, 2026-06-11, Fable)

## Chain 헤더 (거슬러 올라갈 위치, 최상단 리스트만으로 추적 가능)
- 본 handover ← `Claude/results/HANDOVER_2026-06-10_ch1-textbook-rewrite.md`(TBR 50p 교과서 재작업) ← `Claude/results/HANDOVER_2026-06-07_ch2-5-overnight.md`(구 ch2~5 야간 초안) ← `Claude/results/Archive_oldtrack/HANDOVER_RB_2026-06-02b.md`(구-track rb-rebuild)

## 1. 본 세션 지시 (전문 요지, 왜곡 없이)
2차 /goal: "아래 피드백 기준 전면 재검토 후 **백지에서 재작성**. ① 공대 물리 출신은 화학퍼텐셜=깁스 미분을 모를 수 있는데 (1.9) μ 식이 뜬금없음 ② FWHM 는 꼬리가 주 토픽인 시스템에 유도까지 필요했는지 의문 ③ binodal/spinodal 은 모르는 용어 — 뭔지·왜 나왔고·어떻게 연결되는지 모르겠음 ④ **(1.21) Eyring 식에서 시작해 풀어나가는 문건일 줄 알았다 — 사실상 모든 열역학의 근본이고 전위/주변온도/C-rate 영향이 전부 그 식에서 뻗어야 하는데 이 문건은 그 식이 들러리** ⑤ 그림 일부는 개념 이해에 좋은 도식이 아님 ⑥ 교과서가 아니라 회사 연구원 설득용 — 연습문제 불필요, 50p 는 상징(억지 분량 금지). 작업 방식·주의점은 이전과 동일." + 보충 지시: "논리 재구성, 계획서부터, **전수 Fable 작성·검수**(검수 시만 Codex 플러그인 적대 검수 병행)."

## 2. 수행 결과
- 계획: `Claude/plans/2026-06-10-ch1-blank-rewrite-v2-plan.md`(11-section, 검수 체계 절 포함). Ledger: `PHASE_V2_EXECUTION_LEDGER.md`(steps 117–150). 챕터 게이트: `PHASE_V2_ch1_RESULT.md`. 라운드: `PHASE_V2_ROUNDS_RESULT.md`(R1–R14).
- **산출물: `Claude/docs/graphite_ica_ch1_Fable_v2.tex|pdf` = 35p, 식 (1.1)–(1.34), 그림 10(좌표 전부 실함수 계산값), 빌드 err0/of0/undef0.** 새 구성 17단위: Eyring=(1.1) 근본식 → 열역학 다리(G→μ→격자기체→전기화학) → 정·역 균형의 정지점으로 logistic **회수** → 현 작도→binodal/spinodal 단계 명명 → 관측축 → 기준선(FWHM 닫힌꼴 없음) → C-rate/전위/온도 세 가지 → 합성·합산 → [확장] 분기·관측 gap → 통합식+알고리즘(1)–(8) → 검증·반증. 연습문제 0.
- V.1 절별 작성(절당 커밋) → V.2 게이트(피드백 6항 체크 전부 PASS) → **V.R 14라운드**: R1 prose / R2 사양 결정성 / R3 시각 / R4 Codex 1차(ξ_s 반전·r_a 누락 등 7) / R5–R12 절별 전담 8묶음(3렌즈: G-follow/G-usable/정확성 — 검수 Agent 1창씩 순차, 매 라운드 refute·최약점 의무) / R13 **꼬리 경로 round-trip 신규 PASS**(χ 0.534/참 0.50, (1−r_a) 면적 회계=ODE 진실 정확 일치, 구판 +50.9% 과계상 입증 — `results/V2_R13_roundtrip/`) / R14 Codex 2차+시각 스윕.
- 실질 물리·사양 수정 사례: **(1−r_a) 보존 인자**(simplefit/master/hysmaster — 면적 Q(1−r_a)+Q r_a=Q), fig:barrier 파선 χ=½ 틸트 재계산, eq:LqV 유도 재구성, 거울 쌍 "폭 동일" 한정(중심만이 지문), §8 곡률 부호 처방 교체, S3 꼬리-우세 전제(L_V≳w)·창 배치 규칙(A≳3RT, 합성시험 +0.07→+0.03), Ω 흡수 결정+S5 후 복원식, 실행 순서 위상 정렬(read_Rn·cut_qa), μ⁰ 기준 몫 신설, 반쪽전지 전위 기준 선언.
- 커밋: a48b22b→4a2abd6(전부 push, branch rb-rebuild-2026-05-30). 직전 판 `graphite_ica_ch1_Fable.tex`(50p)·원본 — 불가침 보존 확인.

## 3. 미완료 항목
- **사용자 본인 검수**만 남음. 추가 지적 시 해당 절부터 절 단위 루프 재개.
- **ch3/ch4 의 (1.x) 하드코딩 인용 재매핑** — v2 는 전면 새 번호라 v2 확정 후 별도 phase 필수(plan·V.2 RESULT 에 기록). 이번 작업 중 ch3/ch4 무수정.
- 선택 과제(사용자 결정 대기): v1(50p 교과서판) 의 지위 — v2 확정 시 아카이브 여부. TBR_R17 준평형 round-trip 은 (1−r_a) 와 무관해 그대로 유효(r_a≈0 경로) — 전 경로(S1–S5+꼬리) 통합 round-trip 을 원하면 R13 코드와 R17 코드의 병합 확장 가능.

## 4. 다음 세션 주의
- 정본 작업 트랙 = `graphite_ica_ch1_Fable_v2.tex`. 원본·v1 절대 불가침.
- v2 는 식번호 인계 게이트 **해제** 상태(전면 새 번호) — ch3/ch4 재매핑 전까지 ch3/ch4 와 번호 불일치가 정상.
- 본문 수정 = Temp python 스크립트(UTF-8, assert count==1), 체인 `&&`, xelatex 는 반드시 `Claude/docs` 에서 2-pass(cwd 리셋 주의 — 본 세션 2회 헛빌드), Overfull 광역 grep.
- PDF 시각 검증 = pdftoppm + aux 의 newlabel{fig:..} 페이지 추출. Claude/work 는 gitignore — 실행 증거물은 results/ 하위로.
- 절별 검수 패턴(R5–R12)이 효과 컸음: ~200행 묶음 × 3렌즈(G-follow/G-usable/정확성) × refute·최약점 의무 — 절당 5~19건 적발. Codex 는 검수 의견만(파일 수정 절대 금지, Codex/ 불가침).
