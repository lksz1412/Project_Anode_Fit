# docs/ INDEX (MOC) — 구조 A (문건=docs / 코드·빌드·조사=results)

> 문서 탐색 진입점. **docs/ = 문건(최종 .tex/.pdf, 버전별 폴더)만**. 코드·빌드과정·조사는 `../results/`.
> 본문이 진실 — INDEX 와 충돌 시 INDEX 를 고친다. 문서 추가·수정 시 같은 턴에 해당 행 갱신.
> ★2026-06-30 구조 A 재정리: 흩어진 결과물을 docs(문건)/results(코드·빌드·조사)로 통일. 구버전·빌드산물 → `docs/_archive/`.

## 현재 문건 (docs/ 버전 폴더) — ★★release 1.0.10 = Ch1 문건 + 코드 matched
> ★1.0.10 = 코드(`../results/code/Anode_Fit_v1.0.10.py`) 와 **동일 버전·matched**. dQ/dV 정상 종개형 코드 실증 = `../results/code/figs/anode_fit_v1_0_10_dqdv.png`. 검증보고 = `../results/process/GRAPH_VERIFY_RESULT.md`.

| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| **★Ch1_v1.0.10/graphite_ica_ch1_v1.0.10.tex** | ★★★**release 1.0.10**(34p) = Ch1 v10-11 내용 + 버전 1.0.10 라벨 — **코드 Anode_Fit_v1.0.10.py 와 동일 버전·matched**. broadening(집합 통계역학·사이즈 제외)·w 이중지위·w_eff 제거. dQ/dV 정상 종개형 실증 | 1.0.10, release, matched, Ch1, broadening, 코드 동일버전, 종개형 | 2026-07-01 |
| Ch1_v10/graphite_ica_ch1_v10.tex | Ch1 v10(34p, 내부 빌드 계보) — release 1.0.10 의 내용 본체. v9 + broadening 복원·집합 통계역학·사이즈 제외·w_eff 제거 | chapter1, v10, broadening, 집합 통계역학, apparent-U, w_eff 제거 | 2026-07-01 |
| **Ch2_v5/graphite_ica_ch2_v5.tex** | ★★Ch2 v5 **최신**(13p) — v4 + **w_eff(Ω) 절 제거** + w=두-상 현상학적 자유 피팅 + 종 폭 기원은 Ch1 broadening 참조. 통계열역학 본체 보존 | chapter2, v5, w_eff 제거, 자유피팅, 통계열역학, 분포, 섞임 | 2026-07-01 |
| Ch1_v9/graphite_ica_ch1_v9.tex | Ch1 v9(30p) — 흑연+LCO 통합(전자 엔트로피). ⚠️**broadening 누락 → v10 으로 대체됨** | chapter1, v9, LCO, superseded | 2026-06-30 |
| Ch2_v4/graphite_ica_ch2_v4.tex | Ch2 v4(13p) — 통계열역학. ⚠️**§C w_eff 잘못 → v5 로 대체됨** | chapter2, v4, w_eff, superseded | 2026-06-30 |
| Ch1_v8/v8-11.tex | Ch1 v8(21p) — 유도 확장판(흑연). ⚠️broadening 누락 | chapter1, v8, 유도확장, 흑연 | 2026-06-30 |
| Ch1_v7/v7-11.tex | Ch1 v7(17p) — 코드흐름 간결판 | chapter1, v7, 간결, 코드흐름 | 2026-06-30 |
| Ch2_v3/graphite_ica_ch2_v3.tex | Ch2 v3(5p) — 가역 발열 survey 초안 | chapter2, v3, 가역발열, Bernardi, 초안 | 2026-06-30 |
| _archive/ | 구버전(Opus_v4/v5/v6·Fable_v3·원본 ch1/ch2 — ★broadening 설명 원천) + 빌드산물(.aux/.log) + Archive_old/rebuilt | archive, 구버전, broadening 원천, Opus, Fable | 2026-06-30 |
| Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md | Fable 이력 감사 A5 — Ch2(v3→v4→v5→v1.0.10) + 코드(v11_final→v1.0.10) 트랙. w_eff narrowing 오류가 2라운드 적대검수를 통과하고 코드실행 검증(CODE_w_check.md)에서야 발각된 경위·v12 교훈 5건 | Fable, 감사, 이력, w_eff, narrowing, 적대검수, use_w_eff, LCO seam, q_rev, v12 교훈 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md | Fable 이력 감사 A4 — Ch1(v9→v10→v1.0.10→v1.0.11) 트랙. broadening 기작③ ρ(U_j)→ρ(U_app) 재정초(R1 오판#1)·"폭 구조결함" CRIT 오판·철회(R1 오판#2, 인계무결성검수가 반증)·LCO 6절 산문회귀가 v9 시점부터 존재함을 원문대조로 확인·v1.0.11 은 docs 폴더가 v1.0.10 과 byte-identical(Phase 1.1 이후 미착수, 진행중 중단) 확인·v12 교훈 4건 | Fable, 감사, 이력, R1 오판, 철회, ρ(U_j), apparent-U, 폭 구조결함, LCO 산문회귀, v1.0.11 중단, byte-identical, v12 교훈 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md** | ★Fable 내용 감사(v1.0.11 Ch1·Ch2) — 코어 물리 건전(손검산·SymPy·실측), 문제는 주장·귀속층: HIGH 2(Ch2 BW 부호반전·w_j 지위 챕터내 모순)·MED 11(0.18 오귀속·ν=2 23%점프·꼬리수렴 기호오류·코너 과일반화 등)·이전판정 5/5 유지 | Fable, 내용 감사, 물리 타당성, 비약, 왜곡, 코너케이스, BW 부호, w 지위, 문제 리스트 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_03_code_fitness.md** | ★Fable 코드 적합성 감사 — 확정 결함 0(24 boxed 전부 대응·orphan 0·실측 전항 PASS 면적 1.00000·가중식 1e-19), deferred 4(양측 선언)·개선 권고 P1-P4(버전위생·ν 기본값·default 표시·헤더잔재) | Fable, 코드 감사, 양방향 매핑, 실행 실측, deferred, 적합성 | 2026-07-02 |
| **Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md** | ★Fable 이력 전수감사 **종합**(v3→v1.0.11) — 계보·전환별 장단점/문제점 표·관통 패턴 6(설계doc 순응검수 한계·실행기반 검증 결정력 등)·★방향성 유실 표(Eyring 척추 미계승·S0-S5 절삭·§1.18 park)·v12 교훈 9·4-tier | Fable, 감사, 종합, 이력, 계보, Eyring 척추, 방향성 유실, v12 교훈, 관통 패턴 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md | Fable 이력 감사 A2 — v5→v6(흐름도 재조립·97식 보존 손실0)·v6→v7(코드 수식-구동 재편, 전 유도·해석해·S0-S5 식별·KWW 의도적 절삭 = 재-스코핑, 사용자 사후 불만→v8 촉발). 배열↔깊이 독립 축 교훈 | Fable, 감사, v6, v7, 재조립, 재스코핑, S0-S5, KWW, 절삭, 배열과 깊이 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md | Fable 이력 감사 A3 — v7→v8(유도 4단 복원·KNOWN_DEFECTS 6종 정정·D-PEAK "v8서 생김"은 근거미발견)·v8→v9(LCO 통합·흑연 byte 보존·ΔS_e 역부호 5건 적발). broadening 후퇴 정량(v4/v5 ~2771/1883줄→v7 894줄) | Fable, 감사, v8, v9, KNOWN_DEFECTS, D-PEAK, LCO, 유도 복원, broadening 후퇴 | 2026-07-02 |
| Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md | Fable 이력 감사 A1 — Ch1 v3(Fable)→v4(Opus)→v5(Opus) 전환. v3→v4=순수 추가(§1.18 적층, §1.1~1.17 바이트 동일)이나 최초 무계획 배치작성이 σ충돌·B/κ 산수오류 배출 후 V4R redo·Fable_v4→Opus_v4 개명. v4→v5=수식-구동 장르전환(97식 verbatim·산문 32% 압축·keybox 14→1·athermal 훅 소거)+V5.R8 미게이트 회귀·구트랙 버전번호 충돌 경고·v12 교훈 8건 | Fable, 감사, 이력, v3, v4, v5, 적층, stacking, 수식-구동, keybox, verbatim, athermal, V5RR, 장르 전환, park, v12 교훈 | 2026-07-02 |

## ★재작업 진행 중 (2026-06-30, `../plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md`)
- **Ch1 v10**(예정) = v9 정정·통합 — broadening 복원 + w 이중지위 + w_eff 제거 + 기존 LCO/분포 유지.
- **Ch2 v5**(예정) = w_eff 절 제거 + broadening 참조.
- 누락·개선 분석: `../results/MISSING_CONTENT_REVIEW.md`. 조사: `../results/research/radius`(종모양 origin).

## results/ 안내 (문건 아님)
- `results/builds/{v7,v8,v9,ch2_v4}` — 9종 competition 빌드 과정. `results/code/Anode_Fit_v11_final.py` — Ch1 forward 모델(⚠️use_w_eff 버그·v12 정정 대상). `results/research/` — 조사(LCO·통계열역학·radius). `results/process/` — PHASE/LEDGER/HANDOVER.
