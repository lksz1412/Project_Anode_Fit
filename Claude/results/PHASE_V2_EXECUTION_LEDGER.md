# PHASE_V2 Execution Ledger — Ch1 백지 재작성 v2 (Eyring 척추)

Plan: Claude/plans/2026-06-10-ch1-blank-rewrite-v2-plan.md (/goal GO + 추가 지시: 전수 Fable 작성·검수, 검수 시 Codex 적대 검수 병행).
신규 파일: Claude/docs/graphite_ica_ch1_Fable_v2.tex (직전 판 graphite_ica_ch1_Fable.tex 50p 는 불가침 보존).
게이트: 절당 2-pass 빌드 0/0 + 커밋·푸쉬. 피드백 6항 반영 체크리스트는 V.2 게이트.

| Step | 절 | 작업 | 검수 | Commit |
|---|---|---|---|---|
| 117–118 | V.0 계획·ledger | 본 문건 | — | ecd4e7d |
| 119 | 서론 | 척추 선언+stagebox+두 경로, preamble 재사용 | 빌드 0/0(전방 ref 10 보류)·재정독 | a48b22b |
| 120 | §1 기호 | 척추 순서 사전 표+σ_d 세 작용처 | 0/0·재정독 | de390ce |
| 121 | §2 근본식 | eq:eyring=(1.1)+fig:barrier+세 인자 지도 | 0/0·수치(k₀) 검산 | f6cacd3 |
| 122 | §3 열역학 다리 | G→μ→격자기체(Stirling)→전기화학 (피드백①) | 0/0·부호 물리 검산 | b4b51f3 |
| 123 | §4 정·역과 회수 | BV/BEP 합1 강제→detailed balance→logistic 유도 (피드백④ keystone) | 0/0·극한 검산 | 2f75155 |
| 124 | §5 상분리 | 현 작도→binodal→spinodal 단계 명명 (피드백③), 그림 2 재캡션 | 0/0·binodal 좌표 검산 | cfc3612 |
| 125 | §6 관측축 | 보존식 해 V_n·세 전위·연쇄율·worked example | 0/0·worked 검산 | 68115d5 |
| 126 | §7 기준선 | 종 3량, FWHM 닫힌꼴 없음 (피드백②) | 0/0·면적 보존 검산 | aee7cf6 |
| 127 | §8 C-rate 가지 | 보편 ODE→기억 커널 해→두 극한+fig:kernel | 0/0·L_q 수치 | b97b288 |
| 128 | §9 전위 가지 | ΔG_eff 슬롯·직렬 율속·Marcus 창 | 0/0·전이대 % 검산 | a6455e2 |
| 129 | §10 온도 가지 | Arrhenius 회귀(χ 선행)·분포 1/RT 전파·중첩 | 0/0·σ_lnL 검산 | 2c80394 |
| 130 | §11 합성 | eq:closed·simplefit·3×3 표·비순환 원칙 | 0/0·r_a 보존 검산 | 7a6f44d |
| 131 | §12 합산·겹침 | 보존 vs 독립 층위·융합 두 조건·forward 원칙 | 0/0 | 7b3c4c5 |
| 132 | §13 [확장] 분기 | V_eq loop·eq:hysdU 유도·γ 축소 | 0/0·차원/환원/부호 검산 | ed8f8aa |
| 133 | §14 [확장] 관측 gap | 절편/기울기 분해·gap-T 표+그림·부분 cycle 소절 | 0/0·표 수치 검산 | 73b2a09 |
| 134 | §15 통합·알고리즘 | (1)–(8)+M1–M6+S0–S5+참조표+울타리 (round-trip 사양) | 0/0 (134b: overfull 1 수정) | 0682bb2·aea5362 |
| 135 | §16 검증·반증 | 경쟁 꼬리원 표·히스 세 칼날·마무리 recap | 0/0 | 1987b76 |
| 136a | V.1 완료 게이트 | 잔존 undef(sec:dist→sec:tempbranch) 수정 | **err0/of0/undef0, 32p** | 23f3efe |
| 136b | V.2 챕터 게이트 | 피드백 6항 체크 전부 PASS·전문 통독·수치 검산·orphan 0·RESULT | PHASE_V2_ch1_RESULT.md | 04d56fc |
| 137 | V.R R1 | prose 렌즈(구어체·전보체 4건) + Codex 1차 투입 | 0/0/0 | 56c9b97 |
| 138 | V.R R2 | 코드 시뮬 렌즈 — §15 사양 결정성 3건 | 0/0/0 | f82261f |
| 139 | V.R R3 | PDF 시각 판독 — 그림 10p 결함 0 | 검증 라운드 | ada0210 |
| 140 | V.R R4 | Codex 1차 삼각검증 — 확정 2(ξ_s 반전·r_a 누락)+채택 5 | 0/0/0 | c9d3be8 |
| 141 | V.R R5 | 절별 A(서론·§1·§2) — 반쪽전지 선언·s_I·fig:barrier 파선 χ=½ 재계산 등 16건 | 0/0/0 | 36c0ad1 |
| 142 | V.R R6 | 절별 B(§3·§4) — μ⁰ 기준 몫 신설·쌍 셈 자기일관·골짜기 문장 등 16건 | 재유도 8항 통과 | cba6df7 |
| 143 | V.R R7 | 절별 C(§5·§6) — g′=isotherm 우변 연결·§5 verifybox 등 10건 | 좌표 전수 재계산 통과 | ec88b44 |
| 144 | V.R R8 | 절별 D(§7·§8) — verifybox 곡률 부호 처방 교체 등 5건 | kernel convolution 대조 | fcdf343 |
| 145 | V.R R9 | 절별 E(§9·§10) — LqV 유도 단절·댕글링 예고 2·절편 부호 등 12건 | 재계산 10항 통과 | 8f56f1c |
| 146 | V.R R10 | 절별 F(§11·§12) — ★(1−r_a) 보존 인자 3식+그림 2 재좌표 등 16건 | 좌표 역산 적발 | 4be9623 |
| 147 | V.R R11 | 절별 G(§13·§14) — 거울 쌍 한정·곡률 용어·γ 두 기전 등 10건 | 수치 전수 통과 | fa3b1c9 |
| 148 | V.R R12 | 절별 H(§15·§16) — 실행 순서 2건·Ω 흡수 결정·b_j 행 등 19건 | 코드 시뮬 | 35b00dd |
| 149 | V.R R13 | 꼬리 경로 round-trip 신규 — PASS(χ 0.534, (1−r_a)=ODE 진실) + 사양 발견 2건 반영 | 실행 검증 | 3d3efe2 |
| 150 | V.R R14 | Codex 2차 삼각검증(7건 정상·지적 7건 채택 — w·C_bg/Q_cell 차원·Ω 흡수 조건+복원식·중간 구간 규칙 등) + PDF 시각 스윕 결함 0 | 0/0/0, 35p | 4a2abd6 |
| 151 | V.E E.0 | 예시 구현 절 계획(2026-06-11-ch1-v2-code-example-plan.md) | — | (plan 커밋) |
| 152 | V.E E.1 | graphite_ica_model.py(M1–M6 직역)+run_example 실행 검증 3종 PASS | 54.8mV·면적 0.3998·S1 회복 | (E.1 커밋) |
| 153 | V.E E.2 | §1.17 절 수록(verbatim 분할 diff 게이트) | 0/0/0, 37p | 1cf280f |
| 154–155 | V.E ER1+ER2 | 종단 물리 적대+Codex 코드 절 — 충전 ln_Lq 파손 수렴 적발→방향형 수정+충전 면적 시험 | 0.4000 정확 | ed830f6 |
| 156 | V.E ER3 | 종단 검수 본문 일괄 17건(울타리 ⑪–⑭·plateau 별표·변별 지문 등) | 0/0/0, 38p | 1dd1814 |
| 157–158 | V.E ER4+ER5 | 시각·구조 검증 + 정합 스윕(§14 keybox 옛 강도 동기화) | 0/0/0 | 9b3b118 |
| 159–161 | V.E ER6–ER8 | Codex 3차 투입·prose(전문 정독으로 재수행)·완전성 스윕 | 누락 0 | (기록 커밋) |
| 162–163 | V.E ER9+ER10 | fresh-eyes 전문 통독(확정10·의심6)+Codex 3차(확정1: χ_d) → 일괄 27건+실행·diff 재검증 | 0/0/0, **39p** | 723a85a |
| 164 | V.P P.0 | 교정 pass 계획(2026-06-11-ch1-v2-proofread-pass-plan.md) — GO 후 진행 | — | (plan 커밋) |
| 165–181 | V.P P.1–P.17 | 절별 한큐 루프(정독→인벤토리→refute→수정→재정독→0/0/0→커밋) — 32건 | 절당 커밋 | c5106c7→30f33aa |
| 182–184 | V.P P.R1–R3 | Codex+Fable 전문 통독 병행→삼각검증 21건(현-기준 통일·ICA 부호 규약 등)+overfull 정정 | 0/0/0 | ce3198a·d0cc367 |
| 185–187 | V.P P.R4–R6 | 실무-경로 통독("피팅 착수 가능" 판정)→11건(ΔH^eff 방향성 등)+시각 9p 스윕 | 실행·diff PASS | 9e8b7f1 |
| 188–191 | V.P P.R7–R10 | Codex 최종(A–E 전부 정상)→잔존 3건 수정→종합 게이트 전 항목 PASS | 0/0/0, 39p | (본 커밋) |
| 192 | V.T T.0 | 어조·유도 복원 pass 계획+보강(중간식 번호 부여·코드 주석 T.R5 재매핑·컴팩션 청크 운용) | — | (plan 커밋) |
| 193 | V.T T.2 §1.3 | 어조 제거(도입)+G 축소(2법칙 sketch 제거)+Stirling 전 단계(eq:W/stirlingexp/lnW)+ḡ(eq:gbar)+항별 미분(eq:mixderiv)+전기화학 균형(eq:eqbalance/eqexpand) — 식 번호 재배정 시작(eq:mu=1.10) | 0/0/0, 39p | (본 커밋) |
| 194 | V.T T.3 §1.4 | db 비 3단 등식·k 보편형(eq:kuniv)·정지점(eq:stationary)·logistic 풀이(eq:logisticsolve) 번호 부여·★ξ_ss→ξ_eq 전환 설명 복원 | 0/0/0, 40p | (본 커밋) |
| 195 | V.T T.4 §1.5 | w_eff 매칭 전 단계(eq:isoslope)·g(ξ) 번호화(eq:gxi — eq:gbar 와 연결)·g″(eq:gpp)+이차방정식 풀이 단계 | 0/0/0, 40p | (본 커밋) |
| 196 | V.T T.4보정 | 직전 커밋 overfull 1 잔존 정직 정정(인라인 기울기식→eq:logslope 디스플레이 승격) + ★단정형 build_gate.py 도입(echo 비단정 게이트 사고 재발 방지 — err/of/undef≠0 이면 exit 1) | 0/0/0, 40p | b4f899d |
| 197 | V.T T.5 §1.7 | logistic 미분 단계 전개 — 종 항등식 e^-z/(1+e^-z)²=ξ(1-ξ) 를 underbrace 항별로 보인 eq:belliden + 연쇄율 dz/dV_n=s/w 명시 후 eq:dxidV | 0/0/0, 40p | (T.5 커밋) |
| 198 | V.T T.6 §1.8 | 적분인자 유도 3단 전개 — 곱미분 묶음(eq:intfactor)→정적분(eq:intfacint)→지수 재결합 일반해 번호 부여(eq:memory) | 0/0/0, 40p | 381624c |
| 199 | V.T T.7 §1.10 | Arrhenius 유도 전 단계 — L_q 조립(eq:LqT, k₀=k_BT/h 명시)→로그 분해(eq:lnLq)→이항 2회 y(T) 선형식(eq:ydef)→박스에 기울기+절편(결합값) 병기 | 0/0/0, 40p | (T.7 커밋) |
| 200 | V.T T.8 §1.13 | 히스 gap 유도 전개 — spinodal 대입값(eq:hyssub: 역수 logit·∓u)→극대-극소 차 3줄 align(eq:hysdiff)→artanh 항등식 명시 후 eq:hysdU | 0/0/0, **41p** | 015c21c |
| 201 | V.T T.9 §1.14 | 관측 gap 유도 — 방향별 peak 위치 번호식(eq:hyspeakpos)+차 계산(분극 2|I|R_n 합산·중심차=γΔU^hys) 명시 후 eq:hysobsgap | 0/0/0, 41p | 7c91651 |
| 202 | V.T T.10a | §1.2 "공대 물리 독자 기준으로" 어조 잔여 제거(4차 피드백 명시 건) + 서론·기호 청크 정독 정상 | 0/0/0, 41p | (T.10a 커밋) |
| 203 | V.T T.10b §1.6 | 궤적 연쇄율 전개 — 보존식 q-미분(eq:chargederiv) 번호 부여 후 eq:dQdV | 0/0/0, 41p | (T.10b 커밋) |
| 204 | V.T T.10c §1.9 | eq:LqV 압축 해소 — ∂ln k/∂V(eq:dlnk)→직렬 합성 로그미분(eq:dlnkeff)→부호 반전 3단 | 0/0/0, 41p | 3888fdd |
| 205 | V.T T.10d §1.11 | 닫힌식 조립 전개 — 선형 분해(eq:xidecomp)+꼬리 진폭 미분(eq:taildiff — eq:rsol/eq:tail→eq:simplefit 다리) | 0/0/0, **42p** | 2c7d9c1 |
| 206 | V.T T.10e | §1.13 임계 Taylor 전개 align(eq:hyscrit — artanh 급수·Ω-2RT=Ωu² 재묶음·u²=(T_c-T)/T_c 멱 3/2) + M3 가 eq:lnLq 직접 지칭. §1.12·§1.15·§1.16 정독 정상 | 0/0/0, 42p | a3683b3 |
| 207 | V.T T.10f §1.7 | 측정축 전환 번호식(eq:relaxq)+지연 변화율 대입 명시. eq:dUdT(2단 prose 충분)·eq:superpose(완결) 점검 정상 — T.10 잔여 절 정독 점검 완료 | 0/0/0, 42p | 54dd579 |
| 208–209 | V.T T.R1–R3 | Codex+Fable 전문 통독 병행(대수 전수 CONFIRMED·티배깅 0) → 삼각 수정 5건(step함수 한정·패러데이 완화·U 재정의 명시·r_j 구별·RT/(2Ω)) | 0/0/0, 42p | 8a43c25 |
| 210 | V.T T.R5 | 코드 주석 구번호→신번호 20곳(aux 69개+baseline 38개 전수 대조)·verbatim 재동기·diff True/True·실행 PASS(수치 불변) | 게이트 전부 통과 | 4d981d9 |
| 211 | V.T T.R6 | 42p 전 페이지 시각 스윕(결함 0) + ln_Lq 지칭 eq:lnLq 통일 2곳 | 0/0/0 | (R6 커밋) |
| 212 | V.T T.R4+R7+R8 | 독자 3-페르소나 시뮬+Codex 최종(블로커 0) → 권고 12건 반영(울타리 ⑮⑯ 추가·S4 평가점 명문화·S0 모형식 등), 기각 2건 사유 기록 | 0/0/0, 42p, diff·실행 PASS | b12316d |
| 213–214 | V.T T.R9–R10 | 최종 정독(잔여 4구간 — 결함 0) + 종합 게이트 7항목 전부 PASS, RESULT V.T 섹션 기록 | 종합 게이트 PASS | (본 커밋) |
| 215–218 | V.U U.1–U.4 | §1.8/§1.11/§1.12/§1.13 친절 수식 — kernelint·risefollow·tailrate·★tail 진폭 승격·areacons·kinshift·Ifuse·veqslope·hyssym | 0/0/0, 43p | eb2305c→b48d639 |
| 219–225 | V.U U.5–U.11 | 그림 6개편+1신설(전부 실계산): barrier 2패널·doublewell 띠·kernel 2케이스·anatomy 면적·fusion 꼬리 몫·vdwloop 경로·★staging 도식 | 렌더 검증 각 1회+ | 13ca53d→cd59e18 |
| 226–227 | V.U R1–R3 | Codex+Fable 병행(수식 9·그림 7 전부 CONFIRMED) → 주석 재번호 12곳+tail np.where+★comment_gate.py 신설(20패턴)+5건 | 전 게이트 PASS | 6ff26fd |
| 228–229 | V.U R4–R6 | 독자 시뮬+43p 시각 전수 → 16건(라벨 재배치 7·eq:dHeff 신설·중복 압축 등, hysmaster→1.78 동기) | 0/0/0+comment 20/20 | 840a9aa |
| 230 | V.U R7–R8 | Codex 최종(참조 321/미정의 0) → 미인용 라벨 5개 자연 인용처+fusion 라벨 | 0/0/0 | 0a70575 |
| 231–232 | V.U R9–R10 | 최종 정독(3블록+2렌더)+종합 게이트 7항 전부 PASS, RESULT V.U 섹션 | 종합 PASS | (본 커밋) |
| 233–240 | V3.0–V3.6+V3.14 | v3 분기(수식 자기완결): boltz·smixmol·meanfield·constbundle·chisum·affgen·lever·gprime·unique·dUdT 사슬 + 게이트 인자화 + 코드 주석 v3 재매핑 | v3 0/0/0, 44p | 225d765→75f2e24 |
| 241–242 | V3.R1–R3 | 추적 1차 11/13 + Codex 10/10 → 끊김 12 수선(★eq:emu 신설·다리 출처 전수화), emu +1 이동 게이트 적발→동기 | 전 게이트 PASS | cee3d0d |
| 243–244 | V3.R4–R6 | ★재추적 13/13 PASS + 44p 시각 0결함 + 최약 고리 4 보강 | 0/0/0+20/20 | d4b4fb4 |
| 245–246 | V3.R7–R10 | Codex 최종(물리 드리프트 0, 합본 truncation 은 worker 로그로 대체 — 정직 기록)→gxi 다리 eq:emu 인용, 종합 게이트 8항 PASS, RESULT V3 섹션 | 종합 PASS | 81af579·(본 커밋) |
| 247–248 | V3-RR R1–R2 | 6창(~400행) 전담 병렬 검수 → 삼각 수정 35건(★anatomy V_a 재현불가 정정·S1 공동회귀·hold-out 입력·Ω=0 한정 3곳·dG=−SdT 교정·ill-posed 등) | 0/0/0+20/20, diff·run PASS | 9054d56 |
| 249–250 | V3-RR R3–R5 | Codex 통독(확정 0)+시각 45p(★p.38 고아 제목 — \* 결속 해소, 렌더 재검증) | 0/0/0 45p | f6734d2 |
| 251–252 | V3-RR R6–R8 | 문장 prose + 종단 서사 렌즈 → 22건(전보체 통일·keybox 정렬·약속 문구 쌍) — 사슬·전방참조·코드번호 전수 무결 | 0/0/0+20/20 | fc687dd |
| 253–254 | V3-RR R9–R10 | fresh 수렴 라운드 ★확정 0 — 61건 수정의 새 결함 0, 제안 3 반영, "출판 가능" 판정, 종합 게이트 전 항목 PASS | 수렴 충족 | 674ac82 |
| 255–257 | W4.1–4.4 | 수식 13 display(★chordtest·cotangent·binodal·omegaaxis·conv·twolimits·deltareduce·logslopeT 등)+글 압축, 번호 이동 2회 게이트 적발→재매핑 | 0/0/0+20/20, run PASS | 95c2f21·77b7095 |
| 258 | W4.5–4.9 | ★신규 그림 5(실계산·눈금): mudecomp·fluxcross·chargesolve·arrplot·gapI | 렌더 검증 | 3ead8a2 |
| 259 | W4.P1–P3 | ★물리 정식 감사: 차원 97/97·극한 119칸 0이상·그래프 무순환·에너지 폐합·면적 보존 — 확정 모순 0, 감사 문서 커밋, 후속 3 | V3_W4_PHYSICS_AUDIT.md | 3728983 |
| 260–261 | W4.R | fresh 수렴: 번호 주장 aux 로 기각·그림 라벨 10 재배치·캡션 정직화 2·제안 3(수식 모드 오류 1 즉시 정정) | 0/0/0 47p+20/20 | 532ad09 |
