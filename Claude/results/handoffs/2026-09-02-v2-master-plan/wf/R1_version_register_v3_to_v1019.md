# R1 — 버전별 변경점 등록부 전반 (v3 → v1.0.19) 초안

> 작성 = 판독·등록부 초안 에이전트 [hist_early], 2026-09-03. 상위 = `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`(작업 챕터 1 · Phase 1.2 시드). 이 문건은 **초안**이며 master 가 후반 등록부(v1.0.20 → v1.0.26)와 통합한다.
> 경로 표기: 별도 언급이 없으면 `D:\Projects\Project_Anode_Fit\Claude\` 기준 상대 경로다. 행 번호는 `path:L<n>` 로 적는다.
> 4-tier: **[확정]** = 배정 원천에 path+line 근거 · **[근거 미발견]** = 배정 원천에서 찾지 못함 · **[추정]** = 본 에이전트의 해석 · **[미검증]** = 원천이 스스로 미검증이라 표기했거나 실물(tex·코드) 대조가 필요한 사항.

---

## 0. 요지

이 구간의 이력은 **"축소 → 재확장 왕복"**(`docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md:L6`)과 그 뒤의 **"증판(增版) 누적"**으로 요약된다. 2026-06-11 Fable v2 가 사용자 지시("모든 것이 Eyring 식에서 뻗어야")를 유일하게 완전 구현했고, v3(6-12) 이 그 위에서 무결 수렴, v4(Opus) 가 §1.18 적층 준안정을 순수 추가, v5 가 수식-구동 장르로 전환(97식 verbatim·산문 32% 소거), v6 이 코드 흐름도 순으로 손실 0 재조립했다. 그러나 6-29 v7 이 코드 플로우차트(N0→N9)를 척추로 "곡선에 필요한 식만" 남기며 **의도적으로 절삭**(894줄·17p)했고, 사용자가 사후 "중간 도출을 완전히 날렸다"고 판정해 v8(유도 4단 복원)·v9(LCO 통합)·v10(broadening 복원·w_eff 제거)·v1.0.10(코드-문건 동기)으로 선별 재확장됐다. 7-02 Fable 이력 감사가 이 왕복에서 **미계승된 사용자 방향(Eyring 척추·S0–S5 역방향 식별·§1.18 적층)**을 확정한 뒤, v1.0.12(N=10 경쟁·체리픽)부터 v1.0.19(Fable 전면 재작성) 까지는 사용자 피드백을 집행하는 증판이 이어졌다. 이 구간의 결정적 규범 문건은 `docs/v1.0.15/CLOSING_v1.0.15.md`(헌법 3종)이며, 그 이후 버전(v1.0.16~v1.0.19)은 헌법 3종 아래에서 물리(n(T)·vib Einstein)·register·서지·구조를 개별적으로 다듬었다.

구간 말(v1.0.19)의 상태: Ch1 61p + Ch2 24p + appendix 8p, 자산 336(Ch1)·133(Ch2) 전건 보존, 코드 `Anode_Fit_v1.0.19.py` doc-leads 정합·회귀 골든 bit-exact(`docs/v1.0.19/HANDOVER_v1.0.19.md:L14–24, L27`).

---

## 1. 범위·행 구성 원칙

- **범위**: brief §4.3 계보 중 `Fable v2/v3 → … → v1.0.19`. 단 계보의 출발점인 구트랙 RB(5-28)와 v3 직전의 신규 트랙(6-07 Ch2~5 야간 초안·6-10 TBR 50p·6-11 v2 백지)도 **선행 행**으로 넣었다 — 방향성 유실 항목(Eyring 척추·원구상 Chapter 2~5)의 원 지시 시점이 거기에 있기 때문이다.
- **행 단위**: Ch1 계보를 주 축으로 하고, 버전이 아닌 **결정 원천 사건**(6-30 radius 조사·7-02 Fable 이력 감사·7-04 v1.0.15 KICKOFF)도 별도 행으로 둔다(사용자 결정이 그 시점에 고정됐기 때문). Ch2 트랙(v3→v4→v5)과 코드 트랙(v11_final→v1.0.10)은 v1.0.10 에서 합류하기 전까지 §3 의 보조 표로 분리했다.
- **버전 번호 동명이물 경고 [확정]**: `old/Archive_oldtrack/` 의 `COMPARISON_CLAUDE_v4/v5/v5.2_*`·`REVIEW_LEDGER_v3/v4_*` 는 **구트랙(5-28~29, `chapter1.tex` canonical) 기록**이며 본 계보의 v3/v4/v5(6-12~6-17 tex) 와 번호만 같은 별개 산출물이다(`docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md:L36–39`). 통합 초안에서 버전 언급 시 파일 경로 병기가 필요하다.
- **brief §4.3 대조**: 계보 목록의 항목(RB·Fable v2/v3·Opus v4/v5/v6·v7/v8/v9/v10·v1.0.10·Fable 이력감사·v1.0.12·v1.0.13·v1.0.14·v1.0.15·v1.0.16·v1.0.17·v1.0.18.1/.2·v1.0.19)은 전부 §2 표에 행이 있다. 계보 목록에 **없으나 원천에 실재하는 v1.0.11**(byte-identical 중단판)은 추가했다(Decision Queue DQ-3).

---

## 2. 주 등록부 — Ch1 계보 (선행 행 → v1.0.19)

각 행의 9 항목: 버전 | 날짜 | 구조 변경 | 물리·식 변경 | 코드 | 게이트·빌드(페이지 포함) | 사용자 결정(verbatim 은 「 」) | 유실·park 발생 | 근거 path. 표 아래 §2-보충에서 행별 4-tier 보충 서술을 단다.

| # | 버전 | 날짜 | 구조 변경 | 물리·식 변경 | 코드 | 게이트·빌드 | 사용자 결정(verbatim 있으면) | 유실·park 발생 | 근거 path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | 구트랙 RB(rb-rebuild) | 2026-05-28 ~ 06-02 | `chapter1.tex` canonical → Ch1~6 학부-재유도 재구축 → Ch1~5 통합 107p; Ch6(피팅 실무) 해체해 Ch1 부록 B 흡수 | 논문수준 논리를 학부생 무생략으로 재유도; 품질 기준 G-follow·G-usable·챕터 자기완결 확립 | (해당 없음) | 107p·~110 결함 절별 검수 | 「논문 수준 논리를 학부생도 이해하게 재구성. 수식 흐름 보존, 물리 타당성 검증하며 재유도. 모든 가정식 논문/교과서 근거. 계산편의 비약 배제.」(HANDOVER_RB 2026-05-31 L17, A2 인용) | 이후 트랙과 계보 단절(동명이물 v3/v4/v5) | `FABLE_AUDIT_01:L10, L21` · `note_A2:L25–34` · `note_A1:L36–39` |
| S2 | Ch2~5 야간 초안(신규 트랙) | 06-07 | 원구상 P1 = Ch2 발열·Ch3 반응속도론·Ch4 통합 상태방정식·Ch5 히스테리시스 4장 초안(589/762/841/838줄). Ch1 확정본 952줄·20p 기준 | 𝒜_j 일반형 = s·n_eff·F(V_drive−U_j) cross-chapter 통일(28220f5); Ch5 충전 logistic 부호·두 평형·η 부호 등 HIGH 미반영 | (해당 없음) | 4장 독립 빌드 GREEN; Ch3~5 deep 검수 미실시 | 「지금 작업한 내용과, 형식 그리고 작업방법을 그대로 따와서 챕터2~5를 밤새 진행한다 … 챕터 2부터는 이전 챕터까지도 함께 검토를 진행해야한다.」 | ★원구상 4장 구조가 이후 supersede(6-08 재편 → Ch1 흡수) — Ch4 통합 상태방정식·전기-열 coupling 은 계승 근거 미발견 | `results/process/HANDOVER_2026-06-07_ch2-5-overnight.md:L8, L12–21, L29, L75, L92–94` · `note_A5:L18` · `plans/INDEX.md:L57` |
| S3 | TBR — Ch1 교과서 재작업(`graphite_ica_ch1_Fable.tex`, 사실상 v1) | 06-10 | 절별 재작성 18단위 + R1~R17; 50p/2428행·그림 9·연습문제 7·모듈 스켈레톤 | 번호식 55 불변(ch3·ch4 인계 13종 포함); §1.5 eq:Lq 원천항 포함 보편형 일반화; 일반해-먼저 재구성(§1.5·§1.6); 피팅 알고리즘 소절 §1.16 | R17 round-trip 실증(U/w/Q ±0.1mV, Ω 4.07 vs 4.00 RT₀) | 빌드 0/0·R15 텍스트 수렴 0·R16 PDF 시각 무결 | 지시 요지: 리뷰 논문급 깊이·10회 하한·「이 문건만 보고 dQ/dV 피팅 코드를 짤 수 있는 수준」·50p 이상·괄호 구어체 금지·보편식→코너 순서 | Ω=8RT₀ 퇴화 round-trip·결과 수치 부록화 = 사용자 결정 대기(후속 근거 미발견) | `results/process/HANDOVER_2026-06-10_ch1-textbook-rewrite.md:L9–10, L15, L21` |
| S4 | Fable v2 백지 재작성(`graphite_ica_ch1_Fable_v2.tex`) | 06-11 | 17단위 새 구성: Eyring=(1.1) 근본식 → 열역학 다리 → 정·역 균형 정지점으로 logistic 회수 → binodal/spinodal → 관측축 → 기준선 → C-rate/전위/온도 세 가지 → 합성 → [확장] 분기·gap → 통합식+알고리즘 → 검증·반증; 연습문제 0; Addendum §1.17 예시 구현 | ★**Eyring 근본식 척추** 최초·유일 완전 구현; (1−r_a) 보존 인자; eq:LqV 재구성; S3 꼬리-우세 전제; Ω 흡수+S5 후 복원식; 충전 가지 χ_d=1−χ 정정 | §1.17 M1–M6 직역 파이썬(식 번호 1:1)·round-trip PASS(ΔU^hys 54.8mV) | 35p → 39p; err0/of0/undef0; V.R 14 + E.R 10 = 24회 검수 | 「(1.21) Eyring 식에서 시작해 풀어나가는 문건일 줄 알았다 — 사실상 모든 열역학의 근본이고 전위/주변온도/C-rate 영향이 전부 그 식에서 뻗어야 하는데 이 문건은 그 식이 들러리」 + 「검토를 grep 으로 하지 말 것」·「같은 전문을 렌즈별로 따로 N회 돌지 말 것」 | v1(50p) 지위·아카이브 여부 사용자 결정 대기; ch3/ch4 (1.x) 하드코딩 재매핑 별도 phase 필요(→ 구 Ch3/4 supersede 로 소멸, 추정) | `results/process/HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md:L7, L11–13, L18–19, L33, L36–38` · `FABLE_AUDIT_01:L11, L47` |
| V3 | Fable v3(`old/_archive/graphite_ica_ch1_Fable_v3.tex`) | 06-12 (W4·X-pass ~06-13) | v2 사본에서 "수식 자기완결" pass; 2758줄·48p·번호식 97·figure 16·keybox 14·verifybox 9·울타리 ①~⑯·§1.17 코드 절 | 차원 97/97·극한 32식×119칸 비물리 0·도출 그래프 38노드 순환 0·후보 5건 refute 기각; 산문 다리 3곳(1.95·1.75·1.83)이 식 사슬 밖에 잔존 | §1.17 round-trip 코드 절 | V3-RR 10회 수렴 → W4 → X-pass → 674ac82 "publication level"(내부 감사 기준) | 사용자 6차 피드백 「수식만 따라가도 이해 — 교과서처럼」(A1 §1.4 인용) | (유실 없음) 단 "publication level" 외부 타당성은 추정 | `note_A1:L21, L41–44, L122` · `FABLE_AUDIT_01:L11, L23, L70` |
| V4 | Opus v4(`…_Opus_v4.tex`) | 06-13 (V4R 계획서 일자, 추정) | +158/−4줄: §1.18 적층 준안정 신설(eq:gcoupled~gapsplit 6식·fig:stackloop·문헌 6편)·§1.1 기호표 6행·§1.16 athermal 훅 2줄; §1.1~§1.17 바이트 동일 | 둘째 order parameter ψ 로 방향별 임계 조성 ξ_open≠ξ_close 유도; gap 절편 = configurational((T_c−T)^{3/2}) + stacking(athermal) 분리; 가설 tier 자기 격리 | (무변경) | 2912줄·50p·번호식 103; V4R 수렴 c06fb81 gates 0/0/0; v3 하위호환 0/0/0 병행 | (사용자 지적으로 V4.1 방법론 위반 적발 → V4R redo) | ★V4.1 통째 배치 작성 사고(σ 3중 충돌 29개소·B/κ 산수오류) · 파일명 Fable_v4 오명명→Opus_v4 개명 | `note_A1:L13, L50–56, L67–71, L79–81` |
| V5 | Opus v5(`…_Opus_v5.tex`) | 06-17 (V5RR 재검 06-22) | 수식-구동 장르 전환: 2912→1883줄(산문 ~32% 압축)·40p; keybox 15→1·stagebox 소거; §1.18·기호표 6행·athermal 훅 배제; 승격 무번호식 +5 | 번호식 97 **문자 단위 verbatim**; V5RR R2 97식 4축(물리·화학·수리·선행식) 적대 재유도 오류 0 + SymPy | 코드 절 문자 일치 | V5 R1~R7 수렴 + V5RR 4-Phase; ★V5.R8 미게이트 회귀(overfull 2 + 커밋 메시지 허위) · Codex 교차 미가동(샌드박스 740) · 실독자 reading-test 미수행 | 사용자 장르 전환 요청(v5 계획서 L7 인용: 「산문 설명을 배제하고 물리·수식으로만 논리를 잇는 '수식 연속' 버전」) + §1.18 배제 지시 | ★**§1.18 적층·athermal 훅 = park**(배제 결정 기록에 손실 명시 없음 = 근거 미발견) · keybox 13·동기 산문 소거(이후 계보의 유일 baseline 이 됨) | `note_A1:L14, L87–92, L95, L103–104, L114–120, L126–127` · `FABLE_AUDIT_01:L25, L51` |
| V6 | Opus v6(`…_Opus_v6.tex`) | 06-22 | 흐름도(구 BD 코드 파이프라인) 순 재조립: §hys 를 §regsol 직후로, §master 를 §hyspol 앞으로; sec:inputs "실험 기반 시작값" 신설 | 물리·식 무변경(97=97·figure 16=16·boxed 13=13); forward-ref 재봉합 4건 | 임베디드 listing 하드코딩 식번호 14건 동기화 | 1758줄·41p·0/0/0; git diff v3·v4·v5 무손상 | (v6 계획 4원칙: "재조립이지 요약 아님·완성도 ≥ 현재") | (손실 0) — 배열과 깊이의 분리 실증 | `note_A2:L16, L46–58, L67` · `FABLE_AUDIT_01:L12, L26` |
| V7 | v7-11(`results/builds/v7/v7-11/v7-11.tex`) | 06-29 | ★코드 `Anode_Fit_v11_final.py` 진행 N0→N9 를 절 순서로: 서론+9절+부호검산; 894줄·17p; 9+9+1+1 경쟁→체리픽 최초 실증; v5/v6 그림 전량 폐기·신규 5 | 곡선식 11노드만; 통계역학 전 유도(Stirling→S_mix→μ)·꼬리 memory convolution 해석해·KWW/입자분포·lever/common-tangent·Marcus λ·S0–S5·16-울타리·falsify·round-trip **의도적 절삭**; 신규 = V_work 작업 격자·컷 affinity 𝒜=min(z_cut·nRT, A_cap·RT)·이산 저역통과 eq:lowpass·충전 격자 역전 eq:reversal; 부호 사슬 S1–S8 전수검산 + self-test R1–R4 | 코드 1:1 노드맵(tab:nodemap) | 3-pass 0-error 17p; 부호 8/8 | 「실제 표현에 필요한 수식만」(6-29) → 사후 「식 배치·간결화는 잘됐다. 그러나 유도 과정까지 있는 교과서적 문건을 원했는데 중간 도출을 완전히 날렸다」·「너무 과한 확장이었다」 | ★**Eyring 척추 미계승**(코드 플로우차트 척추, Eyring 은 L_q 절 내부) · ★S0–S5 역방향 식별·16-울타리 절삭 · KWW/장벽분포 절삭 · 배제 물리의 피팅 무관성 독립검증 없음(v5 §1.15 반대 경고) · "모델=구현" 동일시(이산형이 종으로 안 환원됨을 설계로 서술) | `note_A2:L17, L76–78, L86–96, L113` · `note_A3:L27–33, L67–81` · `FABLE_AUDIT_01:L13, L27, L47, L50, L54` |
| V8 | v8-11(`old/Ch1_v8/v8-11.tex`) | 06-29 | v7 배치·결과 박스·부호 보존 + (a)출발식→(b)연산→(c)중간식→(d)박스 4단 유도 복원(G-derive); 그림 +4(barrier·flux·doublewell·relaxode)=9; 1209줄·21p | 11식 유도 사슬 닫힘(eq:Uj·eq:xieq detailed balance·eq:dUhys artanh 등); KNOWN_DEFECTS 6종(D-PEAK·D-PEAK2·D-WEFF·D-VEQ·D-DHEFF·D-UBR) 전파추적·정정; self-test R1–R5(R5 falsifiable 회귀 가드 신설); D-PEAK2 = 문턱 ν=2 진폭 점프 정직 기술 | (코드 무변경) | REVIEW_A(SymPy/NumPy)·REVIEW_B(PDF) CRITICAL/HIGH 0; 잔존 = eq:weff 1줄 압축·z_cut=4.357 출처 부재 | 「곡선에 필요한 11식의 유도만 … 과확장 분노 전례」(v8 plan Non-goals) | broadening/분포/KWW/mosaic/Marcus/lever 미복원(v8 Non-goals 로 재유입 금지 명문) · "실측 폭은 broadening 지배" 경고 문장 부재(정직성 공백) | `note_A3:L16, L37–63, L79–92` · `FABLE_AUDIT_01:L28` · `docs/INDEX.md:L177` |
| V9 | v9(`old/Ch1_v9/graphite_ica_ch1_v9.tex`) | 06-30 | 흑연부 v8-11 byte-보존 + LCO 신규 절(sec:dist·sec:lco-electronic·sec:lco-code 등); 1544줄·30p | ξ_eq 분포 프레이밍(Z=1+e^{−βΔμ}, Fermi 함수형 — 단일 자리 점유 분포, 다입자 broadening 아님); LCO 전자 엔트로피(Fermi–Dirac→Sommerfeld→ΔS_e→MIT 게이트 eq:dSegate, tier 3분리); MSMR eq:msmr ↔ eq:xieq 동형(f=−σ_d) | 코드 일반화 명세(구조 변경 0+파라미터 교체+전자항 plug-in) | xelatex 0-err·30p; ★9종 중 5종 ΔS_e 역부호 주입 → 삽입 기준 ΔS_e<0 확정; 인용 fabrication("R. Aronson")·+0.83 mV/K 6종 오귀인 적발·정정 | (사용자 지시: 가역 발열 전셀 = 양극−음극이라 LCO 정량 선행) | ★LCO 6절 산문 회귀("같은 틀 그대로 적용")가 **v9 시점에 기원**(v1.0.10 STYLE audit 에서 진단·v1.0.12 해소) · broadening 후퇴 미회복 | `note_A3:L17, L99–137` · `note_A4:L76–80` · `FABLE_AUDIT_01:L29` |
| E1 | radius 조사 트랙(결정 원천, 버전 아님) | 06-30 | `research/radius/` 3라운드 verdict + 문서 대조 + 코드 실측; 원본 무수정 | (A) 반경→평형 U_j 분포 가설 무효(Gibbs–Thomson ~0.01–0.05mV·양자가둠 sub-meV·역변환 ill-posed) (B) 종모양 = apparent-U=U_j+η 분포(율속 꼬리·크기 kinetic 분산 τ∝r²·RT/F floor)·GITT 잔여 = 미평형/metastable stacking (C) v3/v4/v5 는 두-broadening·ρ_G·현상학적 w 를 이미 설명, v8 이 제거 | ★`v11_final.py` `use_w_eff` = 면적보존 위반 버그(FWHM 90.6mV·면적 9.29 vs 0.5) 실측 | (fig_bell_vs_spike.png) | 사용자 발화 7건 verbatim(등록부 §2-보충 E1 참조) — 요지 「그냥 쌩으로 피팅할 파라미터로 봐야 하는 거 아니냐」·「나한테 이미지를 보여줘야 내가 확인하지」 | [과제 MODEL-1] ρ_G 분포 항 복원 = 선택·범위 결정 필요(→ 이후 scope-out 으로 확정) · [과제 보강] 403 강등 1차문헌 승격 미수행 | `results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md:L10–16, L22–48, L53–56` |
| V10 | Ch1 v10(`old/Ch1_v10/graphite_ica_ch1_v10.tex`) | 06-30 ~ 07-01 | v9 +227/−19줄; 신규 sec:broadening(~170줄); w_eff 3곳 제거·tab:inputs w_eff 컬럼 삭제; 1739줄·34p | broadening 3기작(①유한율속 비대칭 꼬리 ②내재 RT/F ③집합 다입자 통계역학 비-크기) 설명으로 복원(모델 확장 0); **w 이중지위**(단상 Ω≤2RT=평형 예측 폭 / 두-상 Ω>2RT=현상학적 자유 피팅 폭); ★기작③ ρ(U_j) 자기모순 CRIT(A1 adversarial) → ρ(U_app), U_app=U_j+η 로 재정초 | (문건만; 코드는 v1.0.10 에서) | 9종 경쟁→R1/R2/R3→체리픽 v10-10→A1/A2/A3→v10-11; xelatex 0-err 34p; 전자엔트로피 절 byte-identical(SHA 687ba7e6) | 사용자 결정(설계서 baked): 다입자/PSD 모델 X(D3)·w_eff 제거(D2)·v9→v10 통합(D1) + 2차 명확화 "size 배제·집합 통계역학 반영" | R1 오판 #1(설계서 자체 모순 미검) — 설계서 `broadening_w_design.md` 는 사후에도 ρ(U_j) 표기 잔존(ground truth 재사용 위험) | `note_A4:L9, L23–47` · `FABLE_AUDIT_01:L13, L30` · `docs/INDEX.md:L173` |
| V1010 | release 1.0.10(`docs/v1.0.10/`, Ch1+Ch2+코드 동일 버전 matched) | 07-01 | Ch1 v10 +102/−17줄(1821줄); LCO_STAGING_LIT→LCO_MSMR_LIT 식별자 통일·가독성 4-다리(Maxwell/Dreyer 화해 등); Ch2 = v5 동결 편입(+4 국소); 구조 A 정리(docs=문건/results=코드·빌드·조사) | 추가만: 직접엔트로피 교차검증 eq:Sedirect·eV→J 단위환산 eq:gunit(실제 단위버그 가드)·T² 적분계수 eq:U1T2; 물리 결과식·부호 변경 없음 | ★코드 v11_final(흑연 전용) → v1.0.10(742줄): LCO seam(`_effective_dS_rxn` 3경로 공유)·`LCOCathodeDQDV`·`func_dSe_molar`·`entropy_coefficient`·`reversible_heat`·**use_w_eff 제거**; factor-2 전자엔트로피 적발 → T_ref=298.15K 동결 상수 근사(다온도 T² 곡률 P5 이월) | P1~P5 완료; 흑연 회귀 13/13 bit-exact; V2 parity 4.66e-12; Ch1 34p(INDEX)/35p(ledger)·Ch2 13p 0-error | (계획서 순서 결정: 코드 검증→Ch1·Ch2 정련→코드 개정→최종 점검) | ★R1 오판 #2("폭 모델 구조결함" CRIT → 코드 실행+SPEC 대조로 철회, rev.2) · LCO 6절 산문 회귀 진단(수식화 = v1.0.11 과제) · 다온도 T² 동결 해제 이월 | `note_A4:L10, L54–74` · `note_A5:L84, L101–105, L113` · `docs/INDEX.md:L5, L167–172` · `docs/v1.0.10/HANDOVER_v1.0.11.md:L7, L11, L77` |
| V1011 | v1.0.11(`docs/v1.0.11/` — **byte-identical 사본, 중단**) | 07-02 (07-07 계획서) | 폴더 증판만; Phase 0.1 ✅·1.1 🔄(supplement `V1011_P11_map_v10.md` 320줄 작성, tex 미편입)·1.2~4.1 ⬜ | (반영 0) 계획 = LCO 6절 (a)→(d) 수식화(물리 불변)·인계 minor·default n=1 사용성 | (0 byte 차이) | fc /N 0 byte 차이(Ch1·Ch2·코드·가이드·스크립트 전부); 중단 사유 ledger 미기록 | Non-goals 명문(rev.2): broadening 재설계 금지·near-delta 강제 금지·use_w_eff 부활 금지·ρ_G 기계장치 도입 금지(6-30 MODEL-1 scope-out 유지) | supplement 편입 대기 상태로 남음(→ v1.0.12 가 LCO 수식화를 수행해 supersede) · Phase 2.2 ρ_G 진단 예고 prose 미착수 | `note_A4:L9–16, L88–113, L127` · `docs/v1.0.10/HANDOVER_v1.0.11.md:L16–32, L56` |
| E2 | Fable 이력 전수감사(결정 원천) | 07-02 | `docs/Fable_점검/` 8본: 01 종합·02 내용 감사·03 코드 적합성·note A1~A5 | 방향성 유실 표 §4(Eyring 척추 미계승·S0–S5 절삭·§1.18 park·KWW scope-out·자기완결 vs 필요식만 긴장); 관통 패턴 6(설계 doc 순응 검수 한계·실행 기반 검증 결정력·통째 배치 사고·수렴 후 게이트 재실행·다중 모델 마찰·문서-코드 이중 진실); v12 교훈 9 | (코드 감사 03: 확정 결함 0·deferred 4) | (감사 문건) | (Fable 5대 지시의 첫 단계 = 감사) | ★Phase 4.1 명시 결정 항목으로 **이관만** 되고 본 구간 원천에서 결정 기록 근거 미발견: Eyring 척추 회복·§1.18/athermal 재개방·S0–S5 복원 범위·KWW 진단 prose·자기완결 vs 필요식만 조율 | `FABLE_AUDIT_01:L3, L36–42, L44–54, L56–65` · `docs/INDEX.md:L181–188` |
| V1012 | release 1.0.12(`docs/v1.0.12/`) | 07-02 | Ch1 41p·Ch2 14p 한 폴더 증판; N=10 경쟁 작성·체리픽·검수 union·verify10 → finalizer 3커밋 | LCO 6절 줄글→(a)-(d) 수식사슬(신설 eq:lco-* 26); ★방향규약 원자정정(f=+σ_d pairing·F-2 전극중립 한정·세 작용처); F-1 config +R ln[ξ/(1−ξ)]; B-3 Ω 지위; H-1 BW V_eq 부호 정정(Ch2); H-2 w_j 지위 일원화 | 코드 v1.0.12: 흑연+LCO(MSMR)+가역열·주석 f=+σ_d 동기화·σ_d 한정 보강; 회귀 13/13·demo IDENTICAL | 0-err; FITTING_GUIDE §0 방향규약·**S0–S5 비순환 식별사슬·울타리 16·잔차 진단표(D3 선별 복원)**·ν≈8–10 권고(D5) | (Fable 5대 지시) | S0–S5·울타리는 **가이드에 복원**(tex 본문 복원 여부 = 근거 미발견) · Ω 미배정 | `docs/INDEX.md:L156–165` · `docs/v1.0.13/HANDOVER_v1.0.13.md:L3` |
| V1013 | v1.0.13(`docs/v1.0.13/`) | 07-02 야간 GO → 07-03/04 | ★Part 0 통계역학 기초 신설(eq:sm-* 24·TikZ 3) + Part I 순수 흑연 + Part II LCO 단일 우산(전부 후방); 산문 압축(LCO≥35%); 용어 = 한글 서술+영어 원어; Ch1 50p·Ch2 14p | C-1 Δμ=+sF(V−U) 정정; 물리 실결함 3건(config n_jR/F·스칼라 침묵 오차·'w'-단독 config 오가산) 수치 실증 후 정정; eq:lco-sigmaslot·fig:lco-dirmap | 코드 v1.0.13: `curve()` 전극 인지 σ_d 환산(`_delith_is_discharge`)·LCO 전자항 T1(x_MIT 0.85) 재정렬·스칼라 평형 강제·'w'-단독 config 게이트; 회귀 13/13(golden 프로젝트 내) | Fable 3기×10라운드(정정 ≈260곳)·0-err·ref 0·overfull>10pt 0·bit-exact 13/13 | 사용자 지적 7건 요지(①LCO 후방 몰기 ②산문 과다 — v6 원칙「모든 내용을 거의 수식만 읽더라도 대부분 이해 가능한 수준」회복 ③1.85/1.86 overfull ④약자 원어 병기·일본식 번역체 대신 영문 용어 ⑤통계역학에서 시작 ⑥코드에 없어도 필요한 개념 서술 ⑦문건-코드 상호 유기 루프) + GO 「물리·화학 이론 전개 시 문제 발견되면 수정하면서 가는 것 필수. 최우선 = 물리 논리 결함 제거, 다음 논리 비약, 다음 수식 위주 구성. 끝까지 쭉 다 마쳐놔.」 | 이월(실데이터): 다온도 T² 동결 해제·LCO Ω^cat/dH_a 배정·ν≳10 재베이스라인·x-매핑 순환 수치 확인; 부호 함정 3종 가드(σ_d 슬롯·Bernardi 방전·MSMR f=+σ_d) | `docs/v1.0.13/HANDOVER_v1.0.13.md:L6–8, L12–13, L18, L21` · `docs/INDEX.md:L143–154` |
| V1014 | v1.0.14(`docs/v1.0.14/`) | 07-04 | 부록 A(부호 검산표)/B(구현 대응표) 신설·§1.7 폭 예산·§1.13→appendix 표; ★spinodal 독립 부록(8p) 신설 — 별도 문건 유지 확정; 그림 경연 72안→8승자; Ch1 57p·Ch2 14p | eq 1.8 Hill 면밀 유도(Ξ₁·q(T)·ε̃); PSD 보편식 도입 후 수치 유도로 배제; 레퍼런스 DOI 병기(신규 bibitem 5·park2021 정정, Crossref 전건); Ch2 Ξ₁ 통일·Bernardi 전제 명시 | 코드 v1.0.14: docstring eq 참조 16곳(원형 보존 구역 불변)·회귀 13/13; py L74 "1바이트도 변조 X" 구역 침범→원복 이력 | 검수 R1~R7 누적 ~98건·물리 실결함 0 수렴; 0-err/ref 0/of 0 | 피드백 8건 F-A~F-H(어투 교과서·메이저 저널급/eq1.8 엄밀 유도 「간결보다 면밀」/spinodal 부록/§1.7 보강/PSD 배제/코드 연계 단방향·문건 내 변수명 금지/DOI/§1.13 표) + GO 「물리·화학 이론 전개 시 문제 발견되면 수정하면서 가는 것 필수(최우선 물리>비약>수식-주도). 반영해서 작업 진행하자.」 + 검토 후 「spinodal 부록은 별도 문건으로 그냥 놔두자. 나머지는 거의 대부분 마음에 든다.」 | Ch2 그림 과소(2장/14p) → v1.0.15 P5.1 선택 제안; Motohashi g_max=13·ml2024·[A2]–[A5] 원문 재확인 이월 | `docs/v1.0.14/HANDOVER_v1.0.14.md:L6–8, L11, L15–18, L22` · `docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md:L6, L12–14` · `docs/INDEX.md:L129–141` |
| E3 | v1.0.15 KICKOFF(결정 원천) | 07-04 | 코드 업데이트 계획서 3단 진화(rev.1 전자항 정밀형 → rev.2 점별 경로 병행 → **rev.3 이산 격자 완전 퇴출·점별 단일 아키텍처**) | 진단: 격자는 `lfilter` 벡터화 구현 편의였고 ν 스위치·23% 점프·재보간은 파생물; 연속 메모리 적분은 L_V→0 에서 평형 종으로 해석적 매끈 환원(스위치 불요) | (실행은 차기 세션) | fig15(fig:reversal) yshift −3.9cm 정정·57p | 「이산전압 격자를 꼭 적용해야돼? … 이전 세션 어느 버전인가부터 묻지도 않고 그냥 도입했던건데 … 굳이....?」 → 「이산 전압 격자는 완전 퇴출 시킨다. 어차피 이전 버전에 이력이 남아있으니 참고하려면 찾아보면 될 일이고, 이번 버전은 싹 들어낸 버전으로 만든다.」 + Fable 한도 소진 고지 | 원형 보존 구역(`_causal_lowpass`·`func_L_q`) 불가침 주의 → (v1.0.15 에서 사용자 「죽는 부분은 지워야지」로 dead 삭제로 전환) · FITTING_GUIDE 문턱 70–74 kJ/mol 재산출 필요 | `docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md:L8–9, L15–16, L19, L23–25` · `CLOSING_v1.0.15.md:L77` |
| V1015 | v1.0.15(`docs/v1.0.15/`) + ★CLOSING | 07-05 GO → 07-06 | ★이산 전압 격자 아키텍처 퇴출 → 점별 연속 인과 기억 적분; Ch1 §1.9 재작성(신설 eq:memory/lag/tail-limit/reversal·제거 eq:branch/vwork/lowpass); Ch2 worked example 신설; Ch1 58p·Ch2 16p·appendix 8p(승계) | Fable 물리 6종 검토: 확정 CRIT/HIGH 0·물리오류 1(P2-1 Sommerfeld Mott 오귀속)·완결성 갭 3; ★staging 'w'+'n' = 의도 설계('n':1 우선 → 실폭 RT/F=25.7mV·FWHM 90.5mV; 'w' 는 폴백) — 워크드 예제 코드 정합 정정(U_oc 74.4mV·∂U/∂T −0.204·q_rev +60.8) | 코드 v1.0.15: dqdv 점별 재아키텍처(V_work·역보간·`_causal_lowpass`·ν 제거)·`_causal_memory_pointwise` 신설·dead 삭제(`func_U_j_hys`·`_causal_lowpass`)·격자 param 5종 제거; 골든 6종 게이트 검증 후 재캡처; `_LAG_RESOLVE_DECAY_CAP=40` | P1~P7 전건 커밋; 0-err/ref 0/of>10 0; 회귀 13/13 | ★**헌법 3종** 「이 문건의 제일 중요한 두가지는 교과서 수준의 문건, 논문의 깊이의 전문성이고, 세번째가 수식 주도의 문건이다. 수식만 쭉 따라가도 제대로 된 물리, 화학적 논리를 대부분 이해할 수 있는 수준의 문건.」 + D1~D6 + 프로세스 규율(「내 지침이랑 과거 이력좀 제대로 확인좀해라」·「하다못해 1.0.14 본 문건을 제대로 파악했으면 이런짓을 했을까?」·「죽는 부분은 지워야지」·「그런식으로 땜질하지마 문건이 누더기가 되잖아」·「무슨 검사를 안하고 그대로 가져가려고 골든이라고 처리하려고하냐」) + Part 4 w/T 확정(n 으로 fit·실측 T·4단 사다리·n(T)→config 동반) | staging 'w'/'n' 중복 키 정리 = 사용자 판단 대기 · v1.0.14 폴백 · 이월 = 다온도 T² 곡률·two-phase 폭 T-의존·LCO Ω^cat/ΔH_a·ν≳10 실측·서지 재확인 · ★「자기완결 교과서 vs 필요한 식만」 긴장은 헌법 3종으로 조율 완료(추정) | `docs/v1.0.15/HANDOVER_v1.0.15.md:L10–19, L22–29` · `docs/v1.0.15/CLOSING_v1.0.15.md:L9–32, L38–60, L69–81, L86–94` · `docs/INDEX.md:L116–127` |
| V1016 | v1.0.16(`docs/v1.0.16/`) | 07-06 | Ch2 eq:dxidT 뒤 신설 eq:dwdT-nT·Ch1 eq:wbase 교차참조; FITTING_GUIDE §1.5(fit-n·4단 사다리)+격자 debt 정정; Ch1 58p·Ch2 16p | 폭 n(T)=n+n_T1(T−n_T_ref) 선형 일반화; ∂w/∂T=(R/F)(n+T·n′) config 전파 | 코드 v1.0.16: `_n_factor` n(T)·`_dwdT` 신설·`entropy_coefficient` config 전파·배열 T(V)·n(T)≤0 fail-fast; 상수 n = v1.0.15 bit-exact | P1~P5 커밋·push; 2렌즈 적대검수 6결함 수정; 회귀 bit-exact | 지시 요지: CLOSING Part 4 반영·팝업·결정 대기 없이 자율·매 phase commit+push | 4단 사다리 (ii)~(iv) 실행 대기(다온도 실데이터) · 무단 배정 금지 | `docs/v1.0.16/HANDOVER_v1.0.16.md:L9–18, L21–28` · `docs/INDEX.md:L105–114` |
| V1017 | v1.0.17(`docs/v1.0.17/`) | 07-07 | register 정련(★제목/헤더/pdftitle 「코드 진행→계산 진행」·본문 코드/구현/dict/진입점→물리·모델·내부라벨 삭제)·tab:notation caption/label; Ch2 keybox→warnbox·derbox 삭제; Ch1 58p·Ch2 16p·appendix 8p | 물리·수식 무변경; eq:lco-mit underbrace 명료화·(d)박스 라벨·기호 T_{c,j}·ŝ(ζ)·q_int; ★Ch2 참고문헌 7 저자 보충(CrossRef)+DOI 2 정정(occupation2019 134774·hysteresis2018 05.052); appendix κ[J/m]·M 단위(Cahn-Hilliard 차원정합) | 코드 v1.0.17 = matched bump(v1.0.16 bit-identical·회귀 13/13) | P1~P6 커밋; 9종 체리피킹(sonnet 9+CrossRef 1); 3-tex GREEN·undef0·overfull0 | 지시 요지: 외부 리뷰 S6 타당한 것만 반영·9종 체리피킹·팝업 없이 자율; ★사용자 지적으로 추출 오류(Ch2·Appendix 통째 누락·"미포착" 거짓) 정정 → 원본 사진 4장 재추출 | 이월 [선택] = verifybox 활성·longtable·signcheck ✓·N3 재배열·z 각주·ω 다리·N/n 통일·appendix N_A 각주 등(→ v1.0.18.1); standardised2024 저자 2인 이례적(원문 재확인 권장) | `docs/v1.0.17/HANDOVER_v1.0.17.md:L9–20, L23–32` · `docs/INDEX.md:L93–103` |
| V10181 | v1.0.18.1(`docs/v1.0.18.1/`, 2-버전 중 이월판·안전 폴백) | 07-08 | v1.0.17 이월 [선택] 완결: Ch1 8건(verifybox 활성 5·longtable·signcheck ✓·tab:staging 서식·z 각주·ω 다리 2·N/n 통일·(b)(c) 병합)+tab:notation \endfirsthead; Appendix 4건; Ch1 59p·Ch2 16p·appendix 8p | 물리 무변경 | 코드 bit-identical(matched) | GREEN·undef0/multiply0/of>10 0/err0·회귀 0-DIFF | 사용자 결정 = **2-버전 제작**(18.1 이월 완결만 / 18.2 = 18.1 + 제안1 + 로드맵) | 의도적 보류: tab:notation N3 그룹 재배열(#5) | `docs/v1.0.18.1/HANDOVER_v1.0.18.1.md:L9–14, L17–23` · `docs/INDEX.md:L78–85` |
| V10182 | v1.0.18.2(`docs/v1.0.18.2/`, 물리판·18.1 superset) | 07-08 | Ch2 §sec:vibel vib Einstein (a-d) 수식주도(eq:Svib-einstein·eq:dSvib·eq:dUvib)·Ch1 eq:lco-slots 노트·FITTING_GUIDE §1.6; ★`ROADMAP_future_physics.md`(제안2 Ω(ξ)·3 Cahn-Hilliard γ_j·4 Butler-Volmer 농도분극·5 PSD 나노 = 외부 위임); Ch1 59p·Ch2 17p | 제안1: 동결 ΔS_vib → S_vib(T;θ_E)=R[−ln(1−e^{−u})+u/(e^u−1)] Einstein 양자보정·고온극한 R[1+ln(T/θ_E)]·ΔC_p 상쇄 round-trip; 식별 조건 = 준양자 창 걸치는 T 점 ≥3 | 코드 v1.0.18.2: `_vib_theta`·`_S_vib`·`_vib_dU`·`_vib_dS` additive(θ_E 부재 = bit-exact); round-trip 0.000000 µV/K | P4~P8 커밋; 회귀 0-DIFF; 9종 체리피킹(비-Fable) | (2-버전 결정 동일) 「9종 체리피킹은 비-Fable. 최종 Fable 검수 best-effort」 | 제안 2~5 외부 위임(차기 후보 = 제안 2) · Fable 최종검수 2% 잔량 미완 가능 · v1.0.16 물리-데이터 이월(제안1 θ_E 와 같은 다온도 데이터로 동시 식별) | `docs/v1.0.18.2/HANDOVER_v1.0.18.2.md:L12–17, L20–29` · `docs/INDEX.md:L86–91` |
| V1019 | v1.0.19(`docs/v1.0.19/`, Ch1+Ch2 전면 재작성·doc-leads) | 07-08 ~ 07-13 | ★Fable 한 세션 재작성(기존 틀 폐기·새 framework): Ch1 `_sections/ch1_secNN.tex` 24파일 \input 조립·61p / Ch2 15파일·24p; 구조 재설계 5건 = Part II 단일→§11–17 7분할·삼분해(§14)를 전자항(§15) 앞으로·broadening §7 독립절 승격("N6 확장")·§5 유도선행(logistic→폭 모수화)·N0+N1→§1 통합; Ch2 = vib Einstein §2.4 전용절 승격·§2.7/2.8/2.9 3분할·부록 A 함정표·부록 B doc-leads 요구명세; 라벨 키 전부 보존 | ★2대 무결: 물리·화학·수학 골격 오류 0(CENTRAL 12·비자명 11 독립 재유도) / 자산 회귀 0(Ch1 336·Ch2 133 전건 보존); 결함 24(Ch1)·CU-1~11(Ch2) = 구조 재배치·doc↔code·계승(물리 무관); ★CU-1 §2.1 vib 엔트로피 부호 정정(s_int=k_B ∂(T ln q)/∂T); eq:Se→eq:Se-ch2 분리 | ★doc-leads: 코드 K-P1 개정 = `Anode_Fit_v1.0.19.py`(additive: x̄→U_oc 솔버 `solve_U_oc`·`entropy_coefficient_x`·`reversible_heat_x`·`return_terms`), 회귀 골든 13/13 bit-exact; 가이드 §3 dVdq_qa·§6 잔차 정규화·§7 스크립트 세트 | P1~P5·C-P1~C-P5·K-P1·R-P1; xelatex 3-pass Ch1 61p·Ch2 24p·appendix 8p 전 undef0/err0/multiply0; 10종 검수(9 비-Fable+1 Fable) | 「페이블 → 10종 → 페이블 3단계」·「챕터2도 같은 방식」; 자료 = 계획서 1.0.10~1.0.18 + 이력 1.0.18 + 작업물 1.0.18; 문건만·코드 제외(→ 이후 doc-leads 로 코드 개정) · brief §4.3 인용 사용자 평 "v1.0.19 = 구문 최고"(A12 미배정 — DQ-5) | 이월 = 다온도 LCO 전자항 T-복원(현 T_ref 동결)·total heat q_irr 3분해·LCO tier-2/3 실측 초기값·U-24 N6a/N6b 서브라벨·W2-2 orphan 라벨·appendix 편입 여부 사용자 결정 대기·제안 2~5·v1.0.16 물리-데이터 | `docs/v1.0.19/HANDOVER_v1.0.19.md:L10–24, L27–38` · `docs/INDEX.md:L66–76` |

### §2-보충 — 행별 4-tier 보충 서술

**S1~S4 (선행 행).** S1 의 세 기준(G-follow·G-usable·챕터 자기완결)은 이후 v7 감사의 잣대가 됐다 **[확정, `note_A2:L29–34`]**. S2 의 원구상 4장(발열·반응속도론·통합 상태방정식·히스테리시스)은 CLAUDE.md P1 의 "Chapter 2~5" 원형이며, 6-08 장 의존 트리 재편(new Ch2=반속·Ch3=발열) 뒤 "6-07~6-09 작업은 반응속도론·히스테리시스로 재편되어 전부 Ch1(v8-11)에 흡수됐다" **[확정, `note_A5:L18`; `HANDOVER_2026-06-10:L5`]**. 통합 상태방정식(Ch4, 전기-열 coupling·implicit DAE, `HANDOVER_2026-06-07:L61`)이 어디에 흡수됐는지는 본 구간 원천에서 **[근거 미발견]** — §5 유실 후보 L-07. S3 의 "이 문건만 보고 dQ/dV 피팅 코드를 짤 수 있는 수준" 요구는 v3 §1.17·v7 노드맵·v1.0.14 부록 B·v1.0.19 doc-leads 로 형태를 바꿔 계승됐다 **[추정]**. S4 의 Eyring 척추 verbatim 은 `HANDOVER_2026-06-11:L7` 에 "전문 요지, 왜곡 없이"로 기록돼 있어 문자 그대로의 verbatim 은 아닐 수 있다 **[미검증]**.

**V3~V6.** v3 의 "publication level" 은 내부 감사 기준이며 외부 타당성은 감사 문건 자체가 추정으로 분류했다(`FABLE_AUDIT_01:L70`). v4 의 §1.18 은 코드 절 뒤에 붙는 부록성 확장으로 코드 실증이 없었다(`note_A1:L80`). v5 의 §1.18 배제 결정 기록에 athermal 훅 소실의 명시 언급이 없다는 점은 감사 노트가 **[근거 미발견]** 으로 분류했다(`note_A1:L126`). v6 은 손실 0 이 정량 검증됐고(`note_A2:L56`), hyspol 을 master 뒤로 옮긴 논리-순 역전의 실독자 영향은 **[추정]** 이다(`note_A2:L141`).

**V7~V9.** v7 의 절삭은 사용자 당대 승인("실제 표현에 필요한 수식만")이었으나 사후 과도 판정으로 v8 을 촉발했다 **[확정, `note_A2:L96`; `note_A3:L33`]**. 배제 물리의 피팅 무관성은 독립 검증이 없어 **[근거 미발견]** 으로 남았다(`note_A2:L140`). "D-PEAK 오류가 v8 에서 처음 생겼다"는 서술은 v7-11 최종본이 이미 정확해 **[근거 미발견]** 이다(`note_A3:L54`). v9 의 ΔS_e 역부호 5건·인용 fabrication 은 경쟁+적대검수가 적발했다 **[확정, `note_A3:L120–121`]**.

**E1·V10·V1010·V1011.** 6-30 조사의 사용자 발화 7건은 `HANDOVER_2026-06-30:L10–16` 에 번호 순으로 실려 있다(예: 「그 코드로 그림을 그리면 뾰족이만 나오냐? 종모양은 안 나오고?」·「앞선 문건이 이미 w를 피팅의 영역으로 보는데 코드에서 w/w_eff 산출이 의미 없는 거 아니냐? 그냥 쌩으로 피팅할 파라미터로 봐야 하는 거 아니냐.」). v10 의 R1 오판 #1 과 v1.0.10 의 R1 오판 #2 는 공통적으로 "1차 검수가 설계서 순응도·기본값 출력만 채점하고 SPEC·코드 실행을 대조하지 않은" 패턴이었고, 방치 시 "이미 옳게 고친 것을 되돌리는" 방향의 피해였다 **[확정, `note_A4:L117–126`]**. v1.0.10 페이지 수는 `docs/INDEX.md:L172` 가 34p, `FABLE_AUDIT_01:L13`·`note_A4:L61` 이 35p 로 어긋난다(DQ-2). v1.0.11 은 `fc /N` 0 byte 차이로 중단이 확정됐고 중단 사유는 ledger 에 없다 **[확정, `note_A4:L11–16, L100`]**.

**E2·V1012·V1013.** 감사가 "Phase 4.1 명시 결정 항목"으로 넘긴 5건(Eyring 척추 회복·§1.18/athermal 재개방·S0–S5 복원 범위·KWW 진단 prose·자기완결 vs 필요식만)에 대해 본 구간 배정 원천에는 **명시 결정 기록이 없다 [근거 미발견]** — 다만 S0–S5·울타리 16 은 v1.0.12 FITTING_GUIDE 에 "D3 선별 복원"으로 들어갔고(`docs/INDEX.md:L164`), "자기완결 vs 필요식만"은 CLOSING 헌법 3종이 "교과서 register + 논문 깊이 + 수식-주도"로 사실상 조율했다 **[추정]**. v1.0.13 의 사용자 지적 ②가 인용한 "v6 원칙"은 6-22 Opus v6 이 아니라 사용자 발화 속 원칙 표현이다 — 어느 v6 을 가리키는지 원문 대조가 필요하다 **[미검증]**.

**V1014·E3·V1015.** v1.0.14 의 spinodal 부록은 binodal·spinodal·Maxwell·핵생성/Cahn-Hilliard 자족 유도를 담아(`docs/INDEX.md:L136`) v7 이 절삭한 lever/common-tangent 상평형 일반론을 **별도 문건 형태로 부분 회복**했다 **[추정 — 부록 본문 미정독]**. KICKOFF 의 격자 퇴출 결정은 사용자 verbatim 이 가장 길게 남은 결정이며(`HANDOVER_v1.0.15_KICKOFF:L8–9`), CLOSING Part 3-1 은 그 세션에서 staging 'w'/'n' 확정 설계를 새 발견처럼 플래그한 실수를 "[최악]"으로 기록했다(`CLOSING:L68–71`).

**V1016~V1019.** 이 네 버전은 물리 골격 변경이 작고(v1.0.16 n(T)·v1.0.18.2 vib Einstein, 둘 다 additive·bit-exact) 나머지는 register·서지·구조·재작성이다. v1.0.19 의 "2대 무결"과 자산 336/133 보존은 인계 문건의 자기 서술이며 실물 대조는 작업 챕터 2 소관이다 **[미검증]**. brief §4.3 의 사용자 평("v1.0.19 = 구문 최고·v1.0.23 = 논리 최고")은 A12 `results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md` 근거인데 본 에이전트 배정 밖이라 인용만 한다(DQ-5).

---

## 3. 보조 등록부 — Ch2 트랙·코드 트랙 (v1.0.10 합류 전)

### 3.1 Ch2 트랙

| 버전 | 날짜 | 구조·물리 변경 | 게이트 | 유실·park | 근거 |
|---|---|---|---|---|---|
| Ch2 v3(`old/Ch2_v3/…v3.tex`, 266행·5p) | 06-30 | 백지 조사·초안: 다온도 dQ/dV → U_j(T) → ∂U_j/∂T=ΔS_rxn,j/F → Q̇_rev=−IT∂U/∂T(Bernardi) 사슬; 부호 규약 Bernardi·Newman·MSMR 삼각; ΔS_rxn +29→0→−5→−16 J/mol/K 가 Allart 2018 과 양 끝 일치 | 0-err·cite 11/11 | "다온도 dQ/dV 직접 추출" 실증 없음(Open Issue #4) → v1.0.10 까지 이월; staging 4전이 vs Allart region x-경계 불일치를 "해상도 차이" 각주로 처리 → 4개 판 상속 | `note_A5:L18–27` |
| Ch2 v4(`old/Ch2_v4/…v4.tex`, 760행·13p) | 06-30 | 통계열역학 챕터화(9종 competition-cherrypick): 분배함수 Z₁ → 점유 ⟨n⟩ → S_config → 부분몰 발산항 → vib Bose-Einstein·electronic Fermi-Dirac/Sommerfeld; 파생 B 이중계산 경고 신설; ★파생 C w_eff=w(1−Ω/2RT) narrowing — 마스터 설계 doc 오류(역수형) 9작가 상속 → 체리픽서 "정정형"으로 바꿨으나 그 정정형도 물리적으로 거꾸로; exo/endo 역매핑 4종 CRITICAL 적발·정정 | review1 R1–R5 + review2 A1–A3 통과(내적 정합만 검증) | ★w_eff 물리 오류가 적대 2라운드를 통과 — 설계 doc 순응 검수의 한계 실증 | `note_A5:L33–53` · `FABLE_AUDIT_01:L33` |
| Ch2 v5(`results/builds/ch2v5/v5-draft.tex`, 751행) | 07-01 | 파생 C 절 완전 제거; w = 두-상 현상학적 자유 피팅 파라미터·폭 기원은 Ch1 broadening 참조(coordinated); 파생 A·B·D·I 보존; 극한표 Ω→2RT⁻ 행 서술만 정정 | Opus 단일 build — 별도 review 파일 부재(절차 비대칭) | 교정 자체의 재검수 생략 | `note_A5:L59–74` · `docs/INDEX.md:L174` |
| Ch2 v1.0.10(13p) | 07-01 | v5 동결 편입(+4 국소: func_w 교차참조·dilute 한정·Q∂x/∂U 정규화·전셀 부호 각주) | 0-error | P3 "Ch2↔코드/Ch1 정합 매트릭스"의 tex 내 소재 근거 미발견(`V1010_P3_ch2_RESULT.md` 미정독) | `note_A5:L84–90, L130` |

이후 Ch2 는 주 등록부 행(V1012 H-1/H-2 → V1013 → V1014 Ξ₁ → V1015 worked example → V1016 eq:dwdT-nT → V1017 서지 → V1018.2 vib Einstein → V1019 재작성 24p)을 따른다.

### 3.2 코드 트랙

| 코드 | 날짜 | 변경 | 검증 | 근거 |
|---|---|---|---|---|
| `results/code/Anode_Fit_v11_final.py`(617행 또는 706줄 — 원천 불일치, DQ-2) | 06-29 | 흑연 음극 전용 forward dQ/dV; v7 문건의 척추; `use_w_eff` 경로 버그 내재 | v7 부호 8/8 | `note_A5:L9, L96` · `FABLE_AUDIT_01:L16` · `note_A2:L76` |
| `results/code/Anode_Fit_v12.py`(607행, 실험적 청소본) | 07-01 | `func_w_eff`·`use_w_eff` 완전 삭제 실험본; v11 대비 equilibrium/dqdv 0.00e+00 동일 | `v12_roundtrip_check.md` | `note_A5:L11, L113` · `FABLE_AUDIT_01:L65` |
| `docs/v1.0.10/Anode_Fit_v1.0.10.py`(742행) | 07-01 | LCO seam·`LCOCathodeDQDV`·`func_dSe_molar`·`entropy_coefficient`·`reversible_heat`·`irreversible_heat`·use_w_eff 제거; 원형 보존 구역(`func_w`·`func_U_j`·`func_ksi_eq`·`func_L_q`·`_causal_lowpass`·`GRAPHITE_STAGING_LIT`) 1바이트 불변; factor-2 전자엔트로피 → T_ref 동결 근사 | 흑연 13/13 bit·면적 0.936308·전자엔트로피 −45.68 | `note_A5:L101–109` |
| v1.0.11 | 07-02 | 0 byte 차이 | — | `note_A4:L13` |
| v1.0.12 → v1.0.19 | 07-02 ~ 07-13 | 주 등록부 "코드" 열 참조. 요지: v1.0.13 전극 인지 σ_d·T1 0.85 → v1.0.14 docstring eq 참조 → v1.0.15 점별 재아키텍처·dead 삭제·골든 재캡처 → v1.0.16 n(T)·`_dwdT` → v1.0.17/18.1 matched bump → v1.0.18.2 vib Einstein 4헬퍼 → v1.0.19 doc-leads `solve_U_oc`·x̄ 진입점 | 각 버전 회귀 13/13 bit-exact(골든 재정초 = v1.0.15 1회) | 주 등록부 각 행 |

### 3.3 부록(spinodal) 트랙

v1.0.14 신설(8p, 별도 문건 유지 확정) → v1.0.15/v1.0.16 승계(격자 무관·무변경) → v1.0.17(κ[J/m]·M[m⁵/(J·s)] 단위·f 부피밀도 기준) → v1.0.18.1(N_A 각주·γ 단위·분류표 라벨·§app:kinetics note) → v1.0.19 승계(절번호 참조 갱신, 편입은 사용자 결정 대기) **[확정, `docs/INDEX.md:L76, L84, L100, L125, L136`; `HANDOVER_v1.0.19:L35`]**.

---

## 4. 구간 관통 규범·결정의 성립 시점 (통합 초안이 등록부 1.3 과 연결할 지점)

| 규범·결정 | 성립 시점·원천 | 본 구간 말 상태 |
|---|---|---|
| G-follow·G-usable·챕터 자기완결 | RB(5-31~6-02) `note_A2:L29–34` | 존속(헌법 ②③ 에 흡수) |
| Eyring 근본식 척추 | 6-11 사용자 `HANDOVER_2026-06-11:L7` | ★미계승(§5 L-01) |
| (a)→(b)→(c)→(d) 4단 유도·"대입하면 [박스]" 점프 금지 | v8 AUTHOR_BRIEF(6-29) `note_A3:L39` → CLOSING 헌법 ③ [D3] `CLOSING:L25` | 존속 |
| 부호 함정 3종 가드(σ_d 슬롯=탈리튬화·Bernardi 방전=흑연 리튬화·MSMR f=+σ_d) | v1.0.12/13 `HANDOVER_v1.0.13:L21` | 존속(문서·코드·가이드에 가드 문구) |
| w 이중지위(단상 평형 폭 / 두-상 현상학적 자유 폭)·use_w_eff 제거·forward-only·ρ_G 역산 금지 | 6-30 조사 → v10 → v1.0.10 → v1.0.11 Non-goals `HANDOVER_v1.0.11:L27–29` | 존속(불가침) |
| staging 'w'+'n' = 의도 설계('n':1 우선·실폭 25.7mV) | 7-05 O2-B 코드검증·Ch1 L1272–1274 `HANDOVER_v1.0.15:L22` | 존속·중복 키 정리 사용자 판단 대기 |
| 이산 전압 격자 완전 퇴출·점별 연속 아키텍처 | 7-04 사용자 `HANDOVER_v1.0.15_KICKOFF:L9` | 존속(D4 격자 잔재 0) |
| 헌법 3종(①교과서 register ②논문 깊이 ③수식-주도)·D1~D6 | 7-06 `CLOSING:L7–32` | 존속(상위 근거) |
| 제안 전 과거 이력 확인·base 전문 정독·팝업 금지·명시 선택 대체 금지·검증 없이 골든 금지 | 7-06 `CLOSING:L38–60` | 존속(프로세스) |
| w/T 피팅 = n 으로 fit·실측 T·4단 사다리·n(T)→config 동반 | 7-06 `CLOSING:L86–94` → v1.0.16 구현 | 존속·사다리 (ii)~(iv) 실행 대기 |
| 코드 연계 단방향(문건 내 변수명 금지, F-F) → register "코드 진행→계산 진행" → doc-leads | v1.0.14 `HANDOVER_v1.0.14:L6` → v1.0.17 `HANDOVER_v1.0.17:L23` → v1.0.19 `HANDOVER_v1.0.19:L27` | 존속(→ CLAUDE.md P3 #8 코드=부록 전용의 전사) |
| 한글 서술 + 영어 원어·약자 원어 병기 | v1.0.13 사용자 지적 ④ `HANDOVER_v1.0.13:L6` | 존속(→ F-10 의 전사) |
| 2-버전(안전 폴백판/물리판) 분기 관례 | v1.0.18 `HANDOVER_v1.0.18.1:L9` | 선례(v1.0.24.1·v1.0.25.1 폴더명 관례의 원형 — INDEX L19 "선례 v1.0.18.1/.2") |
| 자산 체크리스트(336/133)·CRITICAL 오독방지 앵커·`% 자산:` 절 말미 주석 | v1.0.19 `HANDOVER_v1.0.19:L13, L29` | 존속(→ v1.0.22 계보 감사 ③=0건 기준의 원형) |

---

## 5. 이 구간에서 남은 방향성 유실·park 항목

각 항목 = 원 지시 시점 · 유실/park 발생 시점 · 본 구간 말(v1.0.19) 상태 · 근거 · 재개방 후보 여부(본 에이전트 판단 — 결정 아님). brief §4.5 시드 중 본 구간 소관인 것과 정독 중 발견분을 합쳤다. v1.0.20 이후 산출(SM2·IMPROVEMENT·LIT_ADVANCE·SURV·anodefit 캠페인)은 후반 등록부 소관이라 여기 넣지 않았다(DQ-4).

| ID | 항목 | 원 지시 시점 | 유실·park 시점 | v1.0.19 시점 상태 | 근거 | 재개방 후보 |
|---|---|---|---|---|---|---|
| L-01 | ★**Eyring 근본식 척추**("모든 것이 Eyring 식에서 뻗어야") | 6-11 사용자 | v7(6-29) 코드 플로우차트 척추로 교체 — Eyring 은 L_q 절 내부 | **미계승 [확정]**. v1.0.19 도 N0–N9 코드-정합 스파인 보존(`HANDOVER_v1.0.19:L28`). 감사가 "v12 척추 결정 필요(F-1)"로 넘겼으나 본 구간 결정 기록 근거 미발견 | `FABLE_AUDIT_01:L47, L64` · `HANDOVER_2026-06-11:L7, L11` | 예 — 작업 챕터 3.1 동역학 축(TST/Eyring)의 직접 입력. 후반 등록부가 v1.0.21 TST bgbox(`docs/INDEX.md:L43`)와의 관계를 판정해야 함 |
| L-02 | ★**역방향 식별 사슬 S0–S5·16-울타리**(비순환 파라미터 추출) | v3 §1.15(6-12)·v5/v6 | v7 절삭("Optuna 로 알아서") | tex 본문 = **미복원 [근거 미발견]** / FITTING_GUIDE = v1.0.12 "D3 선별 복원"·v1.0.13 "S0-S5 승계" **[확정]** | `note_A2:L94, L106, L125` · `docs/INDEX.md:L151, L164` | 예 — 기준 5)(일반→특수 가정 사다리)와 G-usable 역방향의 본문 편입 여부(DQ-7) |
| L-03 | ★**§1.18 적층 준안정·athermal 절편 바닥 훅** | v4(6-13, Opus) | v5(6-17) 배제 → park | **park 지속 [확정]**. v1.0.18.2 로드맵(제안 2~5)에도 적층 항목 없음. 6-30 조사가 metastable AAAA stacking(Mercer 2021)을 GITT 잔여 원인으로 인용해 물리적 연관은 살아 있음 | `note_A1:L118–120, L181` · `FABLE_AUDIT_01:L51` · `HANDOVER_2026-06-30:L35` · `HANDOVER_v1.0.18.2:L16` | 예 — 히스테리시스 축(spinodal·CNT·Preisach)에서 "재개방/영구 배제/부록화" 명시 결정 필요(감사 교훈 5) |
| L-04 | **KWW/장벽분포 꼬리 일반형·ρ_G 배리어 분포 적분**(β(T) falsifiable 진단) | v3/v4/v5 §1.10 | v7 절삭 → v10 apparent-U/η 로 부분 대체 → 6-30 [MODEL-1] 선택 → v1.0.11 Non-goals "ρ_G 기계장치 도입 금지·진단 prose 예고만 허용" | 의도적 scope-out **[확정]**. "실측 폭은 broadening 지배" 경고 문장·KWW 진단 prose 의 v1.0.19 잔존 여부 **[미검증]**(v1.0.19 broadening §7 독립절은 확인되나 내용은 미정독) | `note_A3:L69–72, L83–86, L143` · `HANDOVER_v1.0.11:L28–29, L56` · `HANDOVER_v1.0.19:L28` | 조건부 — 동역학 축(master equation/Fokker-Planck·KWW/장벽분포)에서 "일반형 도입 후 forward-only 로 간소화" 사다리 설계 시 참조 |
| L-05 | **lever/chord/cotangent binodal 공통접선·Maxwell 2상 일반론** | v3/v4/v5 §1.5 | v7 절삭·v8 Non-goals 재유입 금지 | v1.0.14 spinodal 독립 부록(binodal·spinodal·Maxwell·핵생성/CH)으로 **별도 문건 형태 부분 회복 [추정 — 부록 미정독]**; 사용자 결정 = 별도 유지·편입 안 함 | `note_A3:L73` · `docs/INDEX.md:L136` · `HANDOVER_v1.0.14:L15` | 예 — 열역학 축(정칙용액·상분리) 본문 편입 여부 = 3.3 구조 결정 항목 |
| L-06 | **다입자 mosaic(Dreyer)·Marcus λ 2차항** | v4/v5 | v7 절삭 | mosaic: v1.0.10 "Maxwell/Dreyer 화해" 다리·v1.0.19 CRITICAL 앵커 A-132 로 **선언 수준 계승 [확정]**; Marcus λ: 본 구간 **[근거 미발견]** | `note_A3:L74–75` · `note_A4:L62` · `HANDOVER_v1.0.19:L29` | Marcus 는 3.1 동역학 축(BV·Marcus) 후보 카탈로그 입력 |
| L-07 | ★**원구상 Chapter 2~5**(발열·반응속도론·통합 상태방정식·히스테리시스) — 특히 **Ch4 통합 상태방정식·전기-열 coupling(implicit DAE)** | 6-07(사용자 야간 지시) | 6-08 재편 → Ch1(v8-11) 흡수; Ch2 가역발열은 6-30 백지 재출발 | 발열 = Ch2 로 계승·반응속도론·히스 = Ch1 §lag/§hys 흡수 **[확정]**; **통합 상태방정식·전기-열 coupling 은 계승 근거 미발견** | `HANDOVER_2026-06-07:L12–21, L61` · `note_A5:L18` · `plans/INDEX.md:L57` | 예 — CLAUDE.md P1 "Chapter 4 통합 상태방정식" 과 열 축(entropy production·Bernardi) 설계 시 원구상 대조 필요(DQ-6) |
| L-08 | 𝒜_j 일반형 = s·n_eff·F(V_drive−U_j), n_eff=RT/(Fw_j)(Ch1 sF 는 이상 특수형) | 6-07 §𝒜 cross-chapter 해법 | 구 Ch3/4/5 supersede | v3 이후 본문에서 어떤 형으로 계승됐는지 **[미검증]** | `HANDOVER_2026-06-07:L75` | 조건부 — 2.3 가정 사다리 감사에서 확인 |
| L-09 | v3 산문 다리 3곳((1.95) dHeff χ_d 정의·(1.75) xidecomp·(1.83) Ifuse L_V 환산)의 식 사슬 완결 | v3(원천 설계) → V5RR 노출 | 완화(cross-ref)만, 종결 아님 | v1.0.19 재작성 후 상태 **[미검증]** | `note_A1:L122, L182` | 2.2 유도 완결성 감사 체크 항목 |
| L-10 | eq:weff 1줄 압축(11식 중 유일)·z_cut=4.357 닫힌 출처 부재 | v8 | — | weff 는 v10 제거로 소멸 **[확정]**; z_cut 출처는 v1.0.11 "오적발(E2/E3/z_cut) 재개정 금지" 이후 **[미검증]**(v1.0.14 가이드에 코드 기본값으로 존속) | `note_A3:L91, L149` · `HANDOVER_v1.0.11:L7, L32` · `HANDOVER_v1.0.14:L25` | 2.3 가정 사다리(컷 상수의 레퍼런스) |
| L-11 | Ch2 "다온도 dQ/dV 직접 추출" 실증 갭·staging 4전이 vs Allart region x-경계 불일치 각주 | Ch2 v3(6-30) | 4개 판 상속 | v1.0.19 Ch2 재작성 후 상태 **[미검증]** | `note_A5:L26–27` | 2.4 서지·2.2 완결성 감사 |
| L-12 | 실데이터 이월 묶음: 다온도 T² 동결 해제(eq:U1T2 ½ 적분)·LCO Ω^cat/ΔH_a 배정·x-매핑 순환 수치·Motohashi g_max=13·ml2024 tier A·[A2]–[A5] 원문·다온도 per-T n 진단(4단 사다리 ii~iv)·θ_E 다온도 식별·LCO 전자항 T-복원·q_irr 3분해·LCO tier-2/3 초기값 | v1.0.10~v1.0.19 각 인계 | 실데이터 필요로 지속 이월 | **전건 이월 상태 [확정]** | `HANDOVER_v1.0.13:L18` · `HANDOVER_v1.0.14:L18` · `HANDOVER_v1.0.15:L28` · `HANDOVER_v1.0.16:L28` · `HANDOVER_v1.0.18.2:L28` · `HANDOVER_v1.0.19:L35` | 아니오(Non-goal 회사 데이터 의존 정량) — 단 warnbox·tier 정직 표기 대상 |
| L-13 | 제안 2~5(Ω(ξ)·Cahn-Hilliard γ_j·Butler-Volmer 농도분극·PSD 나노) 외부 위임 | v1.0.18.2(7-08) | 로드맵 park | park **[확정]**(brief B1 원문은 후반 담당) | `HANDOVER_v1.0.18.2:L16, L27` | 예 — 3.1 후보 카탈로그 시드(brief §4.5 와 동일) |
| L-14 | staging 'w'+'n' 중복 키 정리 | v1.0.15 | 사용자 판단 대기 | 대기 지속 **[확정]** | `HANDOVER_v1.0.15:L29` · `docs/INDEX.md:L117` | 코드 Non-goal 이나 문건 서술(폭 폴백 지위)은 2.5 register 감사 대상 |
| L-15 | tab:notation N3 그룹 재배열(#5) | v1.0.17 이월 | v1.0.18.1 의도적 보류 | 보류 **[확정]** | `HANDOVER_v1.0.18.1:L22` | 낮음 |
| L-16 | Ch2 그림 과소(2장/14p) | v1.0.14 검토 | v1.0.15 P5.1 선택 제안 | v1.0.15 P6 는 좌표 재검산만·신규 4매 여부 **[근거 미발견]** | `HANDOVER_v1.0.15_KICKOFF:L14` · `HANDOVER_v1.0.15:L18` | 후반(v1.0.20 그림 경쟁·v1.0.21 A급 5본) 소관 |
| L-17 | appendix(spinodal) 본문 편입 여부 | v1.0.14 별도 유지 확정 | v1.0.19 "편입은 사용자 결정 대기" | 대기 **[확정]** | `HANDOVER_v1.0.19:L35` | 예 — 3.3 구조 결정과 연동(L-05) |
| L-18 | U-24 broadening "N6 확장 절" N6a/N6b 서브라벨·W2-2 orphan 라벨(sec:center-eqcond/Uj) | v1.0.19 | — | 여지로 기록 **[확정]** | `HANDOVER_v1.0.19:L36–37` | 낮음 |
| L-19 | TBR R17 선택 과제(Ω=8RT₀ 퇴화 round-trip·결과 수치 부록화)·v1(50p 교과서판) 지위·아카이브 | 6-10/6-11 | 사용자 결정 대기 | 후속 기록 **[근거 미발견]**(INDEX `_archive/` 목록에 Fable v1/v2 명시 없음) | `HANDOVER_2026-06-10:L21` · `HANDOVER_2026-06-11:L19` · `docs/INDEX.md:L180` | 낮음(이력 정리) |
| L-20 | 6-30 [과제 보강] 403 강등 1차문헌 본문 승격 | 6-30 | 미수행 | **[근거 미발견]** | `HANDOVER_2026-06-30:L56` | 2.4 서지 감사 |
| L-21 | 설계서 `research/broadening_w_design.md` 의 ρ(U_j) 표기 잔존(ground truth 재사용 위험) | v10 | 소급 미수정 | 잔존 **[확정, 감사 시점]** | `note_A4:L47` | 작업 챕터 1 정독 시 주의 표기 |
| L-22 | v1.0.11 P1.1 supplement(`V1011_P11_map_v10.md`)의 편입 여부 | v1.0.11 | 중단 | v1.0.12 가 LCO 수식화를 수행(eq:lco-* 26)해 **supersede [추정]** — supplement 자체 흡수 여부는 근거 미발견 | `note_A4:L96` · `docs/INDEX.md:L161` · `FABLE_AUDIT_01:L63` | 낮음 |
| L-23 | "자기완결 교과서 vs 실제 표현에 필요한 수식만" 두 지시의 긴장 | 6-10 / 6-29 | 감사가 v12 조율 필요로 이관 | CLOSING 헌법 3종으로 조율 **[추정]** — 명시 조율 문장은 근거 미발견 | `FABLE_AUDIT_01:L54, L64` · `CLOSING:L7–26` | 통합 초안 등록부 1.3 에 "헌법 3종이 조율" 로 기재 권고 |

---

## 6. Decision Queue

- **DQ-1 (범위)**: 본 등록부는 brief §4.3 계보의 "v3 이전" 항목(RB·6-07 Ch2~5·6-10 TBR·6-11 v2)을 선행 행 S1~S4 로 넣었다. 근거 = L-01·L-07 의 원 지시 시점이 거기 있음. 통합 시 유지 여부는 master 판단.
- **DQ-2 (수치 불일치)**: ① v1.0.10 Ch1 페이지 34p(`docs/INDEX.md:L172`) vs 35p(`FABLE_AUDIT_01:L13`·`note_A4:L61`) ② `Anode_Fit_v11_final.py` 617행(`note_A5:L9`) vs 706줄(`FABLE_AUDIT_01:L16`·`note_A2:L76`) ③ v3 줄수 2758(`note_A1:L21`) vs 2759(`note_A1:L88` 인용) ④ v4 줄수 2912(`note_A1:L22`) vs 2735(`note_A2:L14`) vs ~2771(`note_A3:L13`). 통합 초안은 실물 `wc -l`/PDF 페이지로 확정하거나 양측 병기.
- **DQ-3 (계보 누락)**: brief §4.3 계보 문장에 v1.0.11(byte-identical 중단판)이 없다. 등록부에는 포함했고, 통합 초안 Current Ground Truth 계보 문장에 "v1.0.11(byte-identical·중단)" 삽입을 권고.
- **DQ-4 (시드 분할)**: brief §4.5 시드 중 SM2-A/B/C·IMPROVEMENT #3/#4·LIT_ADVANCE ◐선검증군·SURV Tier2/기각군·anodefit 캠페인 B/C/E 는 v1.0.20 이후 산출(B1~B7)이라 본 등록부 §5 에서 제외했다. 후반 등록부가 담당하되, L-01(Eyring)·L-03(적층)·L-13(제안 2~5)은 양쪽에 걸치므로 통합 시 ID 를 하나로 합칠 것.
- **DQ-5 (사용자 평 출처)**: "v1.0.19 = 구문 최고·v1.0.23 = 논리 최고" 는 brief §4.3 이 A12 를 근거로 적었으나 A12 는 본 에이전트 배정 밖. 본 등록부는 brief 인용으로만 표기 — 통합 시 A12 원문 대조 필요.
- **DQ-6 (유실 후보 신규)**: 원구상 Ch4 "통합 상태방정식·전기-열 coupling(DAE)" 의 계승 근거를 본 구간 원천에서 찾지 못했다(L-07). brief §4.5 는 "원구상 Chapter 2~5" 로 묶어 두었는데, 통합 초안 1.4 등록부에서 Ch4 를 별도 항목으로 쪼개고 v1.0.20 이후(Part T·Bernardi) 와 대조하도록 권고.
- **DQ-7 (본문 vs 가이드)**: S0–S5·16-울타리는 FITTING_GUIDE 에만 복원됐고 tex 본문에는 없다(L-02, 본문 복원 = 근거 미발견). v2.0.0 이 "일반→특수 가정 사다리"(기준 5)와 G-usable 역방향을 본문에 넣을지는 작업 챕터 3.3/3.4 결정 후보로 올릴 것을 권고.
- **DQ-8 (날짜 추정)**: v4(6-13)·v5(6-17)·Ch2 v5(7-01)·v10(6-30~7-01) 날짜는 계획서 파일명·INDEX 갱신일 기반 추정. 통합 시 `git log` 대조 권고(본 에이전트는 git 명령 금지).
- **DQ-9 (이음매)**: brief Phase 1.2 명칭은 "v3→v1.0.26" 이나 본 과제는 v3→v1.0.19 분할. 후반 등록부는 §5 L-12·L-13·L-17·L-18 을 v1.0.19 인계 이월 목록의 시작점으로 받아야 한다(HANDOVER_v1.0.19:L35–38 이 정본).
- **DQ-10 (verbatim 등급)**: 6-10·6-11·v1.0.13·v1.0.14 의 사용자 지시는 인계 문건이 "전문 요지, 왜곡 없이"/"요지" 로 표기한 것이라 문자 그대로의 verbatim 보증이 없다. 등록부에서는 「 」로 인용하되 통합 초안이 "사용자 결정(verbatim)" 으로 격상할 때는 인계 문건의 요지 표기를 각주로 남길 것을 권고. 문자 그대로 verbatim 이 확실한 것 = 6-07(`HANDOVER_2026-06-07:L8` "전문, 생략 없이")·6-30 7건·KICKOFF 4건·CLOSING 인용문·v1.0.13 GO 문장.

---

## 7. Read Coverage (파일·행 범위 전건)

모든 파일은 Read 도구로 head→tail 전 영역을 한 번에 반환받아 정독했다(부분 read 없음).

| # | 파일(`D:\Projects\Project_Anode_Fit\Claude\` 기준) | 행 범위 | 비고 |
|---|---|---|---|
| 1 | `results/handoffs/2026-09-02-v2-master-plan/brief.md` | L1–219 (전문) | 지시·골격 |
| 2 | `docs/INDEX.md` | L1–197 (전문) | 계보 1차 정본 |
| 3 | `docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | L1–73 (전문) | 이력 감사 종합 |
| 4 | `docs/Fable_점검/FABLE_AUDIT_note_A1_v3-v5.md` | L1–188 (전문) | |
| 5 | `docs/Fable_점검/FABLE_AUDIT_note_A2_v5-v7.md` | L1–143 (전문) | |
| 6 | `docs/Fable_점검/FABLE_AUDIT_note_A3_v7-v9.md` | L1–160 (전문) | |
| 7 | `docs/Fable_점검/FABLE_AUDIT_note_A4_v9-v1011.md` | L1–128 (전문) | |
| 8 | `docs/Fable_점검/FABLE_AUDIT_note_A5_ch2-code.md` | L1–133 (전문) | |
| 9 | `docs/v1.0.15/CLOSING_v1.0.15.md` | L1–106 (전문) | 헌법 3종 |
| 10 | `docs/v1.0.10/HANDOVER_v1.0.11.md` | L1–79 (전문) | |
| 11 | `docs/v1.0.13/HANDOVER_v1.0.13.md` | L1–25 (전문) | |
| 12 | `docs/v1.0.14/HANDOVER_v1.0.14.md` | L1–27 (전문) | |
| 13 | `docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` | L1–30 (전문) | |
| 14 | `docs/v1.0.15/HANDOVER_v1.0.15.md` | L1–30 (전문) | |
| 15 | `docs/v1.0.16/HANDOVER_v1.0.16.md` | L1–29 (전문) | |
| 16 | `docs/v1.0.17/HANDOVER_v1.0.17.md` | L1–33 (전문) | |
| 17 | `docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` | L1–24 (전문) | |
| 18 | `docs/v1.0.18.2/HANDOVER_v1.0.18.2.md` | L1–30 (전문) | |
| 19 | `docs/v1.0.19/HANDOVER_v1.0.19.md` | L1–39 (전문) | |
| 20 | `results/process/HANDOVER_2026-06-07_ch2-5-overnight.md` | L1–95 (전문) | |
| 21 | `results/process/HANDOVER_2026-06-10_ch1-textbook-rewrite.md` | L1–30 (전문) | |
| 22 | `results/process/HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md` | L1–44 (전문) | |
| 23 | `results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md` | L1–76 (전문) | |
| 24 | `plans/INDEX.md` | L1–65 (전문) | |

미정독(배정 밖·인용만): `FABLE_AUDIT_02_ch1ch2_content.md`·`FABLE_AUDIT_03_code_fitness.md`(INDEX 요약으로만 참조), 각 버전 tex·코드 실물, 계획서 본문, brief 3-B 의 B1~B7, A12 `VERSION_COMPARISON_v19_v23_v24.md`. 등록부의 "[미검증]" 표시는 이 미정독 실물과의 대조가 필요한 항목이다.
