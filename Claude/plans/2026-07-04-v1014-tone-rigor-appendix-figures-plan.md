# v1.0.14 Plan — 어투·물리 엄밀성·Appendix 재배치·코드-문건 연계 방향 정정·이미지 경연

## Summary

v1.0.13(동결, 커밋 5995d64)에 대한 사용자 피드백 8건+총평을 반영하는 개정판 v1.0.14 를 만든다.
목표 서열(불변): **① 물리·화학 논리 무결 ② 논리 비약 제거 ③ 수식-주도** + 이번 신설 축 **④ 논문·교과서급 어투(독자가 불쾌감을 느끼지 않는 정중함·친절한 상세 유도·리뷰논문급 깊이)**.
범위: Ch1·Ch2 tex 개정(절별 루핑, 문건 체리피킹 없음) → Appendix 신설·이동 → 레퍼런스 보강 → 코드-문건 연계 방향 정정 → 축소 검수 → **이미지·그래프 9종 체리피킹 경연**(문건 확정 후, 유일한 경연 대상) → 마감.
토큰 정책: **고등 사고 불필요 작업(전수 스캔·문헌 서치·기계 치환·초벌 어투 재작성)은 Sonnet 서브세션에 위임, 판단·물리 유도·체리픽은 master(Fable)**.

## Current Ground Truth

- 원천(동결): `docs/v1.0.13/` — ch1 2,934줄(50p)·ch2 776줄(14p)·py 899줄·가이드·스크립트·golden. 최종 게이트 전건 green(0-err·ref 0·overfull>10pt 0·회귀 bit-exact 13/13).
- 사용자 피드백 8건(2026-07-04):
  - **F-A(어투)**: "양자역학은 필요하지 않다"(L314) 류 멘트는 교과서·메이저 저널급 문건에 부적합. 어투·멘트 전수 재판정. 한글이 어려우면 영문 작성 후 번역 또는 영문 유지.
  - **F-B(eq 1.8 논리 오류)**: "canonical Z 와 엄밀히 다르지만 같은 글자로 적는다"는 다른 것을 같다고 하는 논리 오류 — 엄밀 유도로 대체. 아울러 왜 적분이 아닌 n∈{0,1} 단순 합인지 무설명 — 연속 자유도 적분→지수 앞 계수→평균의 분자·분모 상쇄 전개(또는 그에 상응하는 가정 명시)가 필요.
  - **F-C(spinodal)**: binodal/spinodal 이 사전지식 설명 없이 등장 — **별도 appendix 문건**으로 먼저 작성, 편입 여부는 사용자가 보고 판단.
  - **F-D(§1.7 줄글)**: 평형 peak·broadening 절 상세설명이 줄글 과다 — 물리식·이미지 보완.
  - **F-E(PSD 배척)**: PSD 를 대놓고 배제 선언 — 일반(보편) 식을 먼저 도입하고 실조건에서 영향이 작아짐을 **유도로** 보인 뒤 배제해야.
  - **F-F(코드 연계 방향)**: 연계 = **코드가 문건 eq 번호를 참조**하는 방향. 문건이 코드 변수명을 가리키며 언급하는 것은 아님 — 문건 내 코드 식별자 언급 정리.
  - **F-G(레퍼런스)**: 출발 피팅값(문헌 초기값)의 출처 문헌 인용 병기.
  - **F-H(§1.13 검산)**: 본문에 있을 필요 없음(작업용 체크) — appendix 성격의 표(Table)로만 기재.
  - **총평**: 통계역학 기반 논리는 매우 탄탄·신규 이미지 만족. **기존(v7-11 유래) 이미지 불만족** → 경연으로 추가/개선.
- 방법론: 기존 지침·플랜(`2026-07-02-v1013-restructure-master-plan.md` rev.4·4-세션 분업·단위 구성 루프·N회 가변-청크·GO 후 무중단) 동일. 차이: 문건 체리피킹 X·이미지만 9종 체리픽·Sonnet 적극 활용.
- 미확인: 문헌 초기값의 원 출처 일부(ΔH/ΔS/Ω/ΔH_a per 전이)는 서치 필요 [미검독]. Appendix 편입 여부(F-C)는 사용자 후결정.

## Phase Range

| Phase | 이름 | Steps | 주 실행 |
|---|---|---|---|
| 1.1 | 증판 준비 + 전수 감사(어투·코드 언급·구어체) | 1–4 | Sonnet 스캔 / Fable 판정 |
| 2.1 | 물리 엄밀성 3건(eq 1.8 유도·PSD 유도-배제·spinodal appendix 초안) | 5–9 | Fable 직접 |
| 2.2 | 구조 재배치(§1.13→Appendix 표·코드 대응 재배치·§1.7 식·그림 보강) | 10–14 | Fable + Sonnet |
| 3.1 | 어투 절별 루핑 재작성(Ch1 13절+Ch2 8구획) | 15–19 | Sonnet 초벌 / Fable 정본화 |
| 3.2 | 레퍼런스 보강(문헌 초기값 출처·DOI) | 20–22 | Sonnet 서치 / Fable 검증 |
| 4.1 | 축소 검수 5회(가변-청크·수정분 중심) | 23–28 | R1·R2·R5=Fable, R3·R4=Sonnet |
| 5.1 | 이미지·그래프 경연(9종 체리픽) + 편입 검수 | 29–34 | S3·O3·C3 제작 / Fable 체리픽 |
| 6.1 | 마감(게이트·result·ledger·INDEX·HANDOVER·커밋) | 35–37 | Fable |

## Non-goals

- v1.0.13 원본 폴더·golden·이전 result/ledger 문건 수정 금지(증판 = `docs/v1.0.14/` 신규).
- 문건 전면 재작성 금지 — 지적 지점 중심의 절별 루핑(총평 "그 외 매우 흡족" 존중).
- 코드 물리 로직 변경 금지(주석·docstring 의 eq 참조 보강만). 회귀 bit-exact 유지.
- 문건 체리피킹 경쟁 없음. 이미지·그래프만 9종 경연.
- 실데이터 round-trip(다온도 T² 등 이월 4건)은 이번 범위 밖.

## Implementation Changes

- 신규: `docs/v1.0.14/`(tex 2·py 사본·가이드·스크립트·figs — 버전 문자열 계보 연장), `docs/v1.0.14/appendix_phase_separation.tex`(F-C 별도 문건, 편입 보류), `plans/`(본 문건), `results/process/V1014_EXECUTION_LEDGER.md`·`V1014_TONE_AUDIT.md`·`V1014_REF_SOURCES.md`·검수 R 보고서·경연 산출(`V1014_FIG_CONTEST_*`), `results/V1014_RESULT.md`, `docs/v1.0.14/HANDOVER_v1.0.14.md`.
- 수정: `docs/INDEX.md`(신 블록), 코드 주석(eq 참조 보강).

## Phase 1.1 — 증판 준비 + 전수 감사 (Steps 1–4)

- **Step 1** 증판: v1.0.13 → `docs/v1.0.14/` 복사, 버전 문자열 정밀 패치, 빌드·회귀 기준선 확인. gate: 0-err·13/13.
- **Step 2** [Sonnet] **어투 전수 감사**: 두 tex 전문에서 ①메타·자기지시 멘트("양자역학은 필요하지 않다"·"이 문건이 하지 않는 것"류 선언·"못박는다"·"걷어낸다" 등) ②구어·은유("전기화학 옷"·"환율"·"값어치"·"먹인다"·"산다/죽는다"·"~다(전보체)" 등) ③단정·훈계조("금한다"·"주의한다"의 과잉) 전 출현을 [위치|원문|위반 유형|초벌 대체문] 표로 산출 → `V1014_TONE_AUDIT.md`. **판정 기준(Fable 이 머리에 고지)**: 메이저 저널·표준 교과서(예: Newman, Bard&Faulkner 급)의 서술 관례 — 1인칭 최소·명령문 대신 서술문·은유 대신 물리 용어·독자 지시 대신 내용 전달. 필요 시 영문 초안→한역 병행.
- **Step 3** [Sonnet] **코드 식별자 언급 전수 감사**: 문건 내 \code{}·codebox·코드 서술("코드는 ~한다") 전 출현 목록화 + 처분 초안(삭제/물리 서술화/Appendix 이동) → 같은 문건에 병기.
- **Step 4** [Fable] 두 감사의 전 항목 판정(채택/수정/기각) — 절별 적용 명세 확정. gate: 감사 coverage = 전문(missing 0), 판정 100%.

## Phase 2.1 — 물리 엄밀성 3건 (Steps 5–9, Fable 직접 — 물리 1급)

- **Step 5** **eq 1.8 엄밀 재유도**(F-B): 현행 "같은 글자 Z" 서술 폐기. **[GO 확정: 간결판이 아니라 면밀·완결판 — Hill Ch.7 Langmuir 유도를 삽입 전극 언어로 전개, 논리적 납득이 우선]** 확정 4개 항 = ①hard-core 배타(가정 1)·자리 독립(가정 2, Ω 로 완화 예고) 명시 → $\xi_1=1+q(T)e^{-\beta(\varepsilon_0-\mu)}$ (점유 상태의 연속 위상공간 적분 $q(T)$ 를 유도로 도입) → 분자·분모 상쇄·$\tilde\varepsilon=\varepsilon_0-k_BT\ln q$ 흡수 → logistic ②기호 = 교과서 표기($\xi$ 또는 $\Xi_1$·$q(T)$), canonical $Z$ 와 글자부터 분리·Ch2 $Z_1$ 동일 기호 통일 ③$q(T)\to U_j$ 흡수 경로 + Ch2 vib 엔트로피($-k_B\partial(T\ln q)/\partial T$)와의 연결 1문단 ④참고문헌: Hill(1960) Ch.7·McQuarrie(1976)·Fowler \& Guggenheim(1939)·McKinnon \& Haering(1983). 유도 골격 —
  (i) 자리 하나의 일반 대정준 분배함수를 **점유수 합 × 점유 상태의 내부(연속) 자유도 적분**으로 출발: $\Xi_1=\sum_{n\in\{0,1\}} e^{\beta\mu n}\, z_\mathrm{int}(T)^{\,n} e^{-\beta\varepsilon n}$, 여기서 $z_\mathrm{int}(T)=\int e^{-\beta H_\mathrm{int}}\,d\Gamma$ 는 점유 시 이온의 진동·국소 자유도 적분(지수 앞 계수의 정체).
  (ii) 평균 점유 $\langle n\rangle$ 계산에서 이 계수가 **분자·분모에 공통으로 등장** — 로그를 취하면 유효 자리 에너지 $\tilde\varepsilon\equiv\varepsilon-k_BT\ln z_\mathrm{int}$ 로 흡수되어 logistic 형이 보존됨을 명시(사용자 지적의 "계수 상쇄" 전개 그대로).
  (iii) $n\in\{0,1\}$ 합의 근거 = **hard-core 배타(자리당 이온 1)** 를 가정으로 명시 — "가정 없이 자명" 처리 금지.
  (iv) 기호 정리: canonical $Z$ 와 구분되는 **독립 기호(예: $\Xi_1$ 또는 $\zeta$)** 를 정의하고 Ch2 의 $Z_1$ 표기와 한 기호로 통일(Ch2 동시 수정) — "다르지만 같은 글자" 류 서술 전면 제거. 하류(eq:sm-factor $\Xi_M$·eq:fermifn 유도문·Ch1↔Ch2 교차참조) 연쇄 갱신.
- **Step 6** **PSD 유도-기반 배제**(F-E): §1.7(c)(i) 재작성 — ①일반식 먼저: 입자 반경 분포 $p(r)$ 위 dQ/dV 합성곱의 보편형과, 반경이 평형 전위를 옮기는 두 채널(Gibbs–Thomson $\Delta U\sim 2\gamma V_m/(rF)$ 스케일·율속 $\tau\propto r^2$ 분산)을 식으로 도입 ②실조건 대입: 마이크론 흑연 $r\sim\mu$m 에서 $\Delta U(r)$ 수치 추정 ≪ 실측 폭 → 항이 작음을 **수치 유도로** 보이고 ③그 결과로서 비-크기 η 산포만 잔존함을 결론(현행 "다루지 않는다" 선언은 이 유도의 따름 문장으로 강등). 필요한 문헌 상수(γ·V_m)는 Phase 3.2 서치와 연동, tier 병기.
- **Step 7** **spinodal/binodal Appendix 초안**(F-C): 별도 파일 `appendix_phase_separation.tex` — 혼합 자유에너지 곡선에서 공통접선(binodal)·곡률 반전(spinodal)·준안정/불안정 영역·Maxwell construction·핵생성 vs spinodal 분해 구분까지, 사전지식 0 독자용 완결 유도 + 그림 1–2매. 본문(§1.2·§1.5)에는 "부록 X 참조" 연결만 임시 삽입. **편입/폐기는 사용자 검토 후 결정** — 초안 완성 시점에 별도 보고.
- **Step 8** §1.13 물리 재분류(F-H 선행 판단): 검산 항목 중 본문 유지 가치가 있는 것(0)과 표 이동분 분류.
- **Step 9** gate: 신설 유도 전건 Fable 독립 재검산(부호·차원·극한)·빌드 0-err.

## Phase 2.2 — 구조 재배치 (Steps 10–14)

- **Step 10** **§1.13 → Appendix 표화**(F-H): 부호 사슬 S1–S8·R1–R5 를 appendix 의 검산표(항목|명제|근거 식|판정) 1–2개로 압축, 본문 §1.13 제거. LCO verifybox 검산도 같은 표에 통합.
- **Step 11** **코드 대응 재배치**(F-F): Phase 1.1 판정 명세대로 — 본문 프로즈의 \code{} 인라인·"코드는 ~" 서술을 물리 서술로 재작성 or 삭제, codebox 2개·tab:nodemap·tab:inputs 는 **Appendix "구현 대응표"** 로 이동(재현 가능성 목표는 appendix 가 담당). fig:spine 의 코드 함수명 병기 정리.
- **Step 12** [코드 측] py 주석·docstring 의 eq 번호 참조를 전 함수로 보강(이미 다수 존재 — 누락분 채움, 코드→문건 단방향 완성). 회귀 bit-exact 확인.
- **Step 13** **§1.7 식·그림 보강**(F-D): broadening (b)①②③·(c) 의 줄글을 — ① $L_V$ 소멸·② $\sim RT/F$ 잔여·③ eq:ensavg 합성곱 — 각 몫의 **정량 스케일 식+개형 그림(신규 1–2매, 경연 대상에도 등재)** 으로 재구성, 산문은 다리 1–2문장 원칙.
- **Step 14** gate: 이동·삭제 후 참조 무결(ref 0)·orphan 0·빌드.

## Phase 3.1 — 어투 절별 루핑 (Steps 15–19)

- **Step 15–18** Ch1 13절+서론, Ch2 8구획을 **절 단위 루프**로: [Sonnet 초벌 재작성(Phase 1.1 판정 명세 적용) → Fable 정본화(물리 표현 무손실 검증·리뷰논문급 문장) → 앞 절과의 다리 정합 → 빌드]. 물리 유도 신설부(Phase 2.1 산출)는 Fable 이 직접 문장까지 마감.
- **Step 19** gate: TONE_AUDIT 전 항목 처분 완료·구어/은유/메타 멘트 재스캔 0·수식·수치 diff 0(어투 패스는 물리 비접촉 증명 — 수식 토큰 해시 대조).

## Phase 3.2 — 레퍼런스 보강 (Steps 20–22)

- **Step 20** [Sonnet] 문헌 초기값 전수 목록(흑연 4전이 U/ΔH/ΔS/Ω/ΔH_a·LCO 3전이 anchor·g_max·x_MIT·γ·V_m 등)별 원 출처 서치(기준 시점=현재, DOI 포함) → `V1014_REF_SOURCES.md`(값|후보 문헌|정합 근거|tier).
- **Step 21** [Fable] 출처 검증·채택 판정(추정 금지 — 못 찾은 값은 [근거 미발견]+tier C 유지 명시), tab:staging·tab:lco-staging·본문에 \cite 병기, bibitem 에 DOI 병기.
- **Step 22** gate: 표의 모든 수치가 인용 또는 [근거 미발견] 명시 중 하나를 보유.

## Phase 4.1 — 축소 검수 5회 (Steps 23–28)

- 가변-청크·렌즈 로테이션 유지, 라운드 축소(토큰 정책·수정 국소성 반영 — **기본값 5회, 수렴=연속 2R 확정결함 0 시 조기 종료**):
  - R1 통독(수정분+전체 정합) — Fable×3
  - R2 신설 유도 재유도(eq 1.8 사슬·PSD 스케일·spinodal appendix·§1.7 신설식) — Fable×3
  - R3 어투·용어·레퍼런스 정합 — Sonnet×3, Fable 삼각검증
  - R4 참조·그림·경계(재배치 여파) — Sonnet×3, Fable 삼각검증
  - R5 자유 사냥+flag 처분 — Fable×3
- **Step 23–27** 라운드 실행(각: 3기 병렬→master 삼각검증→정정→게이트→커밋). **Step 28** 수렴 판정.

## Phase 5.1 — 이미지·그래프 경연 (Steps 29–34)

- **Step 29** [Fable] 대상 선정: ①기존 v7-11 유래 7종(spine·staging·hysloop·barrier·flux·logistic·reversal) 개선본 ②§1.7 등 신규 필요 위치(Phase 2.2 에서 등재된 것 포함) — 대상별 "위치·전달할 물리·현행 불만점" 브리프 작성(문건 재작성 없음, 위치·내용 선정만).
- **Step 30–32** 경연: 대상마다 **9안 = Sonnet 3 + Opus 3 + Codex 3**(Codex 는 스텝별 지시+폴링 감시), 전 안 TikZ 소스+렌더 확인 제출. 제작 머리에 좌표=식 수치 평가 원칙·라벨 무교차·본문 용어 정합 고지.
- **Step 33** [Fable] 체리픽: 안별 [물리 정확(좌표 검산)|전달력|문건 정합] 3축 채점→선정·필요 시 합성, 편입.
- **Step 34** gate: 편입 그림 전수 좌표 재검산·캡션-본문 정합·빌드. 경연 기록 `V1014_FIG_CONTEST_MAP.md`.

## Phase 6.1 — 마감 (Steps 35–37)

- **Step 35** 최종 게이트(두 tex 빌드·회귀·demo/sample 재실행·appendix 포함 참조 무결). **Step 36** `V1014_RESULT.md`(11항목)·ledger 마감·INDEX. **Step 37** HANDOVER(Chain: …→v1.0.13→본)·최종 커밋+푸쉬.

## Implementation Interfaces

- 어투 감사 표: `| 줄 | 원문 | 유형(메타/구어/은유/단정) | 초벌 대체문 | Fable 판정 |`
- eq 1.8 목표 형태: $\Xi_1=1+z_\mathrm{int}(T)\,e^{-\beta(\varepsilon-\mu)}$, $\langle n\rangle=\dfrac{z_\mathrm{int}e^{-\beta(\varepsilon-\mu)}}{1+z_\mathrm{int}e^{-\beta(\varepsilon-\mu)}}=\dfrac{1}{1+e^{+\beta(\tilde\varepsilon-\mu)}}$, $\tilde\varepsilon=\varepsilon-k_BT\ln z_\mathrm{int}$ — 가정(hard-core 배타·내부 자유도 인수분해) 명시, Ch1·Ch2 공통 기호 1개.
- 레퍼런스 표: `| 파라미터 | 값 | 출처(저자·연도·DOI) | 정합 근거 | tier |`
- 경연 제출: `V1014_FIG_CONTEST_<대상>_<모델><n>.tex`(standalone 컴파일 가능) + 렌더 png.
- ledger 12-col·Result 11항목·검수 보고 양식 = v1.0.13 과 동일.

## Test Plan

- 매 Phase: xelatex 2-pass 0-err·ref 0·overfull>10pt 0 / `test_regression_graphite.py`(무인자=verify) 13/13 bit-exact.
- 어투 패스 물리 무손실: 수식 환경 토큰 추출 해시 전후 대조(diff 0).
- 신설 유도: Fable 독립 재검산(부호·차원·β→0/∞·Ω 극한·계수 상쇄 확인).
- 레퍼런스: 인용-값 1:1 대조, 미확보 값 [근거 미발견] 표기 잔존 확인.
- 그림: 편입안 좌표 전점 식 재계산·라벨 교차 산술.
- 재배치: appendix 이동 후 본문 잔여 참조 grep 0.

## Assumptions

- 검수 5회 축소·R3/R4 Sonnet 실행이 사용자 토큰 정책 부합(조정 가능).
- 코드 대응표(nodemap·inputs·codebox)는 삭제가 아니라 **Appendix 이동**이 재현성 목표와 양립하는 기본값.
- 이미지 경연 대상 ≈ 기존 7종+신규 ~3종, 대상당 9안. Opus/Codex 가용 전제.
- spinodal appendix 는 초안 완성 후 사용자 판단까지 본문 비편입(포인터만).
- §1.13 의 "table 5 정도" = 검산 내용을 appendix 표 형식으로 기재하라는 취지로 해석.

## Decisions Required (GO 시 기본값으로 진행)

1. **검수 라운드 수**: 기본 5회(위 구성). 10회 유지 원하시면 지정.
2. **코드 대응물 처분**: 기본 = 본문 프로즈 제거+Appendix "구현 대응표" 이동. 전면 삭제(코드 주석만 남김) 원하시면 지정.
3. **이미지 경연 범위**: 기본 = 기존 유래 7종 개선+신규 ~3종, 대상당 9안(S3/O3/C3).
4. **영문 병행 수위**: 기본 = 한글 서술 유지+어투만 논문급 교정(난문만 영문 초안→한역). 특정 절 영문 유지 원하시면 지정.

## Correction History

- **rev.2 (2026-07-04, GO)**: 사용자 승인 — 방향성 전체 동의. eq 1.8 유도는 사전 설명·납득 후 확정: "간결한 것보다 면밀한 것, 논리적으로 납득하는 것이 더 중요" → Step 5 를 면밀·완결판 4개 항으로 확정(위 명시). Decisions Required 4건은 기본값으로 진행(검수 5회·코드 대응물 Appendix 이동·경연 ~10종×9안·한글 유지+논문급 교정).
- 신규 계획(v1.0.13 마스터플랜 rev.4 의 후속). v1.0.13 대비 방법 변경: 문건 체리피킹 폐지(사용자 지시)·검수 10→5 축소(토큰 정책)·Sonnet 실작업 위임 확대·이미지 경연을 문건 확정 후 별도 Phase 로 분리(9종 체리픽은 이미지 한정)·코드-문건 연계 방향을 "코드→문건 참조 단방향"으로 정정.
