# REVIEW1 — v8-01 (유도 확장판) 적대 검수

> 검수 sub(리뷰 전용). 대상 `v8-01/v8-01.tex`(965행) 전문 정독. 기준 = `Anode_Fit_v11_final.py`(706줄)·`v11_flowchart.md`·`AUTHOR_BRIEF_v8.md`·`KNOWN_DEFECTS.md`.
> Read coverage: tex 1–965 전부 / v11 코드 1–707 전부 / flowchart 1–89 / brief 1–63 / KNOWN_DEFECTS 1–22.
> refute mandate·가장 약한 1곳·빈 통과 금지.

---

## 1. 확정 결함 (심각도 / 행·식 / 틀림 / 옳은 형)

### CRIT

**C1 — 중복 라벨 `eq:vn` (행 262, 866) → 빌드 경고 + 참조 모호**
- 틀림: `\label{eq:vn}` 가 두 식(§N1 분극 박스 식~262, §N9 분극 박스 식~866)에 동시 부여. `\eqref{eq:vn}`(행 285, 940 nodemap N0)가 둘 중 하나로만 풀려 다른 곳을 가리킴. xelatex `multiply-defined labels` 경고, hyperref 링크 오결.
- 옳은 형: 두 식 중 하나를 `eq:vn-sum` 등으로 분리하거나 §N9 의 중복 박스를 \eqref{eq:vn} 참조로 대체(같은 식을 두 번 박스화한 것 자체가 §2 배치 중복).

**C2 — Table~\ref{tab:staging}(행 902–905) U 값이 v11 코드와 불일치 + 본문 자기모순 (배치 보존 위반)**
- 틀림: 표가 U = 0.210 / 0.120 / 0.090 / 0.075 (전이 4→3 / 3→2L / 2L→2 / 2→1). v11 `GRAPHITE_STAGING_LIT` 정본 = 0.210 / **0.140** / **0.120** / **0.085**. 3개 전이 값이 어긋남. 게다가 §N2 codebox(행 350)는 stage 2→1 을 `U(298)≈0.0853 V` 로 *옳게* 인용 → 같은 문건 안에서 0.075 vs 0.0853 자기모순. 표의 stage 라벨도 코드 주석(2L→2 U≈0.120, 2→1 U≈0.085)과 어긋남.
- 옳은 형: 표 U 열 = 0.210 / 0.140 / 0.120 / 0.085 (v11 1:1). 비고의 "메인 피크 전/메인 피크" 재배치.

### HIGH

**H1 — Table~\ref{tab:inputs}(행 924–926) 코드 식별자 오기 (소유권·G-usable)**
- 틀림: `\code{dHa}`·`\code{dSa}`·`\code{C\_bg}` 로 표기. v11 정본 키 = `dH_a`·`dS_a`·`Cbg`(생성자 인자명·전이 dict 키). 이 표만 보고 dict 작성 시 KeyError.
- 옳은 형: `dH_a`·`dS_a`·`Cbg`. (본문 행 201·202·190 은 옳게 `dH\_a`/`dS\_a`/`Cbg` 로 적어 표만 어긋남 = 단일 표 정정으로 해결.)

**H2 — Table~\ref{tab:nodemap}(행 940–949) 노드 배정이 spine 그림·flowchart 와 어긋남 (척추)**
- 틀림: nodemap 이 N1="전이 루프 개시", N2="U_j^d(분기 중심)", N3="ΔU_hys" 로 배정. 그러나 (i) 같은 문건 spine 그림(행 123–125) = N1 polarization·N2 center·N3 hysteresis, (ii) 정본 flowchart = N1 분극·N2 U_j·N3 히스. 즉 표가 본문 그림·코드 척추와 한 칸씩 밀림(N1 분극이 사라짐). nodemap N0 도 \eqref{eq:vn} 로 C1 모호 참조에 걸림.
- 옳은 형: N1 = 분극 V_n(식 vn), N2 = U_j(식 Uj), N3 = ΔU_hys·U_j^d(분기) — spine 그림과 1:1.

**H3 — eq:reversal 코드 인용(행 812)이 v11 에 없는 식별자 날조 (G-usable·소유권)**
- 틀림: "코드의 `ksi\_eq\_rev = ksi\_eq[::-1]; ksi\_lag\_rev = lowpass(...); ksi\_lag = ksi\_lag\_rev[::-1]`" 라 인용. v11 실제(L477) = `occ_lagged = _causal_lowpass(ksi_arr[::-1], grid_step, lag_len_V)[::-1]` 한 줄, 식별자는 `ksi_arr`·`occ_lagged`·`_causal_lowpass`. 인용한 세 이름(`ksi_eq_rev`/`ksi_lag_rev`/`ksi_lag`)은 코드에 존재하지 않음.
- 옳은 형: 실제 한 줄·실제 식별자로 인용(다른 codebox 들은 실제 코드 문자열을 쓰는데 여기만 재구성).

### MEDIUM

**M1 — D-UBR 미수정: eq:Ubranch(행 504–509)가 여전히 ansatz, 현상학 명시 부족**
- 틀림: γ·h_η 도입을 "실측 분기 중심을 방향별 한 자유도로 적으면"으로만 정당화 → γ 가 0~spinodal 한계 사이 보간 인자임을 명시 안 함(유도 가장). KNOWN_DEFECTS D-UBR 처방("spinodal 한계 ±½ΔU_hys 위 현상학적 매개변수화로 명시 또는 γ 보간 인자 명시") 미충족.
- 옳은 형: "두 spinodal 극값이 분기의 *상한* ±½ΔU_hys 을 주고, 실측은 그 안쪽 — γ∈[0,1] 가 상한 대비 실현 분율(현상학적 보간), h_η 는 부분 cycle 보정"으로 1–2문장 명시.

**M2 — D-DHEFF 부분: χ_d·Ω 의 계수 χ_d 중간식 점프(행 712–719)**
- 틀림: 깊은 꼬리 Ω(1−2ξ)→−Ω 흡수 동기는 주나, 왜 계수가 *χ_d* 인지(전이상태 분율이 Ω 몫을 χ_d 만큼 받음)의 중간식 `r^+=k_0 e^{−(ΔH_a−TΔS_a−χ_d𝒜 ... )}` 류가 없어 "−χ_d·Ω" 의 χ_d 가 한 줄 점프로 등장. KNOWN_DEFECTS D-DHEFF 처방(중간식 명시) 미충족.

### LOW

- **L1 (행 690)**: 컷 z_cut 유도가 근사 `ξ(1−ξ)≈e^{−z}` 을 쓰면 z=ln80≈4.382 이나 본문은 z≈4.357 인용. 4.357 은 *정확* 조건 ξ(1−ξ)=0.0125 의 해라 결과는 옳음 — 보인 근사 단계와 인용 상수가 0.025 어긋남(표기상 흠).
- **L2 (행 548)**: w_eff 중심기울기 중간식 `(RT−2Ω·ξ(1−ξ))·1/(sF·ξ(1−ξ))|_{1/2}` 표기가 난삽(괄호 묶음 애매). 결과 (4RT−2Ω)/(sF)·4Fw_eff=4RT−2Ω 는 옳음 — D-WEFF 중간식은 *존재*.
- **L3**: 참고문헌 `bard2001`·`eyring1935`·`newmann2004` 정의되었으나 본문 \cite 없음(미인용). `dubarry2012` 는 1994 가 아니라 2009 연도 기입(라벨 2012 vs 연도 2009 불일치).
- **L4 (행 165)**: $\xi_j$ "방전 시 0→1 로 증가" 와 staging 그림 캡션(행 241) "delithiation: $\xi_j:1\to0$" 표기 방향이 상충해 보임(본문=진행률 증가, 그림=잔류 리튬 감소 — 다른 양이나 같은 기호 ξ 로 혼동 유발).

---

## 2. KNOWN_DEFECTS 보유표 (9종 전수 — ★=v7-11 상속)

| 결함 | v8-01 보유? | 근거(행) |
|---|---|---|
| ★**D-PEAK** (eq:peakshape "L_V 작으면 종 환원" 오류) | **미보유(회피)** | §N8(행 766–819)·eq:peakshape(815)에 "L_V→0 ⇒ d ξ_eq/dV 종 환원" 거짓 주장 *없음*. 평형↔꼬리 전환을 eq:sum(854–858) 두 *이산 모드*(min_lag_grid_steps 문턱, 코드 L466)로 옳게 제시. 매끈한 극한 주장 자체를 안 함 → 상속 결함 회피. |
| D-VEQ (eq:Veq §5 forward-defer 순환) | **미보유** | eq:Veq(391–393)를 §N3 에서 g'(ξ)로 직접 유도, §N5 logistic 은 detailed balance(eq:db 559)로 독립 유도 — 순환·forward-defer 없음. |
| D-DHEFF (χ_d 계수 중간식 누락) | **부분 보유** | 행 712–719: 동기·−Ω 흡수는 보이나 χ_d 계수 중간식 점프(M2). |
| D-WEFF (중심기울기 중간식 누락) | **미보유** | 행 547–549 에 dV_eq/dξ\|_{1/2}=(4RT−2Ω)/(sF)→4Fw_eff 중간식 *존재*(L2 표기 흠뿐). |
| D-UBR (ansatz 위장) | **보유** | eq:Ubranch(504–509) γ·h_η 현상학 명시 부족(M1). |
| D-VN(minor) (이항 중간식 자명) | n/a | eq:vn(260) 자명 — 과주 아님, 무해. |
| fig:overshoot 식번호 오기 등 | 해당없음 | v8-01 엔 fig:overshoot 부재(fig:hysloop 로 대체). 신규 fig:doublewell·logistic 데이터 *독립*(byte 중복 아님). |
| eyring/bazant/dreyer 미인용(LOW) | **보유(유사)** | bard/eyring/newmann 미인용(L3). |

**상속 ★D-PEAK: 미보유(가장 중요한 PASS).** 다른 8종 중 D-UBR 보유·D-DHEFF 부분 보유.

---

## 3. 강점 3 / 약점 3 (가장 약한 1곳)

**강점**
1. ★D-PEAK(최우선 상속 결함) 회피 — 거짓 "종 환원" 극한을 빼고 평형/꼬리를 이산 모드 분기로 옳게 처리(eq:sum).
2. G-derive 본령 충실 — ΔU_hys(spinodal 대입→artanh 정리), logistic(detailed balance→정지점→풀이), L_q(ODE→적분인자→이산), w_eff(중심기울기) 모두 [출발→연산→중간식≥1→박스] 사슬이 *보이게* 복원됨. 한 줄 점프가 핵심 박스엔 거의 없음.
3. 부호 8항 본문 일관 — 분극 부호(V_app>V_n 방전)가 flowchart 2026-06-29 정정과 정합, logistic·peak·χ_d·운영 ∂lnL_q/∂V=0 모두 코드 1:1.

**약점**
1. ★(가장 약한 1곳) **표 3종(tab:staging·inputs·nodemap)이 코드·본문과 어긋남**: U 값(C2)·코드 키(H1)·노드 배정(H2)이 정본/자기 그림과 충돌. 유도 본문은 정밀한데 *표*가 배치 보존·G-usable 을 깨 가장 약함 — 표만 보고 재현 시 잘못된 U·KeyError·노드 오해.
2. 코드 인용 충실도 편차 — eq:reversal codebox(H3)가 날조 식별자, 대부분 codebox 는 실제 문자열이라 일관성 결여.
3. D-UBR ansatz 미수정(M1)·D-DHEFF χ_d 중간식 점프(M2) — 두 박스만 사슬이 끊겨 G-derive 균일성 흠.

---

## 4. 차원 점수 (각 /5 → 합 /35)

| 차원 | 점수 | 근거 |
|---|---:|---|
| 척추(N0–N9 배치 보존) | 3 / 5 | 본문 절 순서·spine 그림은 정본 따름. 그러나 nodemap 표(H2)가 N1/N2/N3 밀림 + 자기 그림 모순. |
| 부호(8항) | 5 / 5 | 8항 전수 코드 1:1, 분극 정정 정합(아래 §5). |
| ★G-derive(유도 완결성) | 4 / 5 | 9/11 사슬 모범적 복원·D-PEAK 회피·D-VEQ/D-WEFF 해소. 감점 = D-UBR ansatz(M1)·D-DHEFF χ_d 점프(M2). |
| G-follow(앞 식만으로) | 4 / 5 | 식 흐름 자족·forward 참조 없음. 미세 감점 = ξ 기호 방향 혼동(L4). |
| G-usable(이 문건만으로 v11 재현) | 2 / 5 | 표 U 값 틀림(C2)·코드 키 틀림(H1)·reversal 식별자 날조(H3) → 표·일부 codebox 로 재현 시 오류. |
| 완결성(orphan) | 4 / 5 | 식·그림 \ref 연결 양호, 대부분 도입·사용 짝. 감점 = 미인용 bib 3건·중복 박스(eq:vn). |
| 그림 | 4 / 5 | v7-11 유래 5개 + 신규 3개(doublewell·V_eq 비단조는 hysloop 에 통합·reversal 완화) 명시·ASCII·\ref 연결·이해 도움. 감점 = 신규 "3개" 중 V_eq 비단조가 별 그림 아닌 hysloop 흡수라 브리프 신규 3개 표기와 약간 어긋남. |
| **합** | **26 / 35** | |

---

## 5. 부호 8항 PASS/FAIL (AUTHOR_BRIEF_v8 §7 — v11 코드 대조)

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | U_j(T)=(−ΔH+TΔS)/F | PASS | eq:Uj(338)·S1·code L69 1:1. |
| 2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | PASS | eq:xieq(579)·signbox(585)·code L86–87. |
| 3 | dξ/dV peak 양수·방향 불변 | PASS | eq:eqpeak(640–644) 절댓값·S3·code L468. |
| 4 | ΔU_hys≥0 / Ω≤2RT→0 / 분기 ±½σ_d | PASS | eq:dUhys(491–496)·S4·S5·code L75–79,138. |
| 5 | χ_d 충전 1−χ · ΔH_a^eff=ΔH_a−χ_dΩ | PASS | eq:chid(706)·eq:dHeff(719)·code L160,152(유도 충실도는 M2지만 *부호*는 정합). |
| 6 | ∂lnL_q/∂V 컷 상수라 운영 0(부등식=동기) | PASS | 행 753–755·S8 명시, 코드 컷상수(L335) 정합. |
| 7 | 꼬리 충전 격자 역전·충전 dQ/dV 방전 거울(양수) | PASS | eq:reversal(809)·code L477(식별자 인용은 H3 이나 *부호·방향* 정합). |
| 8 | 분극 V_n=V_app−σ_d|I|R_n, 방전 V_app>V_n | PASS | eq:vn(261,865)·행 258·868·code L412, flowchart 2026-06-29 정정과 정합. |

**부호 8항: 8/8 PASS (FAIL 0).**
