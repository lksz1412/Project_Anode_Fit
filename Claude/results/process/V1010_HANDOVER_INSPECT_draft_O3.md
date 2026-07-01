# V1.0.10 인계 무결성 대검수 — 검수자 O3 (초점: Ch2 통계열역학 인계)

> __ID__=O3 · __ROLE__=Ch2 통계열역학 인계 · v1.0.10 동결(수정 0, 진단만) · 결과는 v1.0.11 핸드오버 갱신용.
> 방법: 기록(SPEC)을 기준 명세로 대조 — AUTHOR_BRIEF·FIX_LIST_v411·review1(R1–R5)·review2(A1–A3) 전문 정독 → v4-11(=SPEC 최종)·v5-draft·v1.0.10 tex head→tail 정독 + Compare-Object 라인 diff + Ch1 v1.0.10 broadening 절 교차확인 + v3 skeleton baseline 확인. refute·가장약한1곳·빈통과금지.

---

## 0. 검수 대상·SPEC 대조 좌표 (실측 근거)

| 산출물 | 경로 | 줄수 | SHA(앞12) | 지위 |
|---|---|---|---|---|
| v4-11 (SPEC 최종) | `results/builds/ch2_v4/v4-11/v4-11.tex` | 713 | 7A8ED5F471B6 | v4 체리픽 최종본 |
| v4-11 사본 | `old/Ch2_v4/graphite_ica_ch2_v4.tex` | 713 | 7A8ED5F471B6 | **byte-identical** = v4 최종이 old/ 로 그대로 이동 |
| v3 skeleton | `old/Ch2_v3/graphite_ica_ch2_v3.tex` | 243 | 6123E9E327A4 | v4 base(얇은 Bernardi survey) |
| v5-draft | `results/builds/ch2v5/v5-draft.tex` | 705 | 2FDDE8E043A4 | w_eff 제거 정정본 |
| **v1.0.10 현행** | `docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` | 705 | E7D3B6919F7F | 동결 대상 |

핵심 사실: **v5-draft → v1.0.10 은 같은 705줄이나 SHA 상이** → 변경 존재. Compare-Object 로 전수 diff 한 결과 변경은 **10줄 미만·전부 개선/정합 방향**(§3-A). **v4-11 → v5 는 131줄 차이이며 그 대부분이 파생 C(w_eff) 절의 의도된 교체**(§2-핵심쟁점).

SPEC 이 확정한 v4 최종의 정답값(R1/R2/A1/A2 삼각):
- config 부분몰 = `+R ln[ξ/(1-ξ)]` (ξ→1 희박 +∞, ξ→0 만충 −∞, ξ=½ 0). ★스파인 doc `41` L27 의 역수 오기 미상속.
- w_eff = `w(1−Ω/2RT)` (V-폭, Ω→2RT⁻ → 0, 역수 아님) — v4 는 v4-05 체리픽으로 이 정답형 채택.
- 이중계산 B: ΔS⁰_j≡[ΔS]_{ξ=½}(config=0)·config 는 분포 w 가 줌·별개 항.
- exo/endo: Q̇_rev=−(IT/F)ΔS, ΔS>0→흡열·ΔS<0→발열 (v4-04 역매핑 교정 완료).
- q_rev = Bernardi Q̇=I(U_oc−V)−IT∂U/∂T.

---

## 1. G-derive (분배함수 → S=−R∑p ln p 점프0) — 인계 무결 [PASS·정독 근거]

**[무결·G-derive/축1] · 위치: v1.0.10 L119–175, L210–256, L363–399 ↔ SPEC R1 L20·A1 표적1·AUTHOR_BRIEF 항2–4**
분포 유도 사슬이 v4-07(R1 이 G-derive 점프0 로 체리픽 base 지정한 빌드)의 무결성 그대로 v1.0.10 에 살아 있다:
- `eq:Z1`(L123) 단일 자리 대정준 분배함수 Z₁=1+e^{−β(ε₀−μ)} → `eq:occ`(L129–131) ⟨n⟩ 각 등식 명시(점프0) → Fermi–Dirac 동형 지적(L134–137).
- `eq:muV`(L142) 전기화학 퍼텐셜 → `eq:logistic`(L151–152) Ch1 logistic 의 기원. **단위 다리 N_A 명시**(L155–156: R=N_A kB, F=N_A e, βF=1/w) — A1 위험5·R1 위험5 정답 충족.
- `eq:Sconfig`(L213) S_config=−R∑p ln p=−R[θ ln θ+(1−θ)ln(1−θ)] → `eq:dSconfig`(L225–227) 부분몰 −R ln[θ/(1−θ)] → `eq:dVdT_config`(L232–237) +R/F ln[ξ/(1−ξ)]. config 사슬 완전 전개.

이유(왜 무결이 중요): 두 축 중 축1(전개 비약0)·G-derive 가 이 챕터의 존재 이유(v3 skeleton 탈피). SPEC A1 이 "config 는 Z→⟨n⟩→S 완전전개"라 확인한 상태가 v10→v1.0.10 두 세대를 건너 보존됨. **정독 확인: L119–256 전 등식 각 화살표 명시, 근거 없는 점프 0.**

---

## 2. ★섞임항 C = w_eff — **의도된 supersession(인계 결함 아님)** [PASS·오적발 방지 핵심]

**[개선·G-usable·물리정합/축1·2] · 위치: v1.0.10 L539–568(파생 C 재정의) ↔ v4-11 L516–568(구 파생 C w_eff) ↔ v5 헤더 L8–13 ↔ 계획서 L9·L10 ↔ Ch1 v1.0.10 L1275–1352**

이것이 본 초점의 최대 쟁점이며, **base 프롬프트가 경고한 "bell/w_eff 오적발 함정"의 정확한 대상**이다. 결론: **인계 결함 아님 — v10-era 의 의도된 물리 정정(supersession)이 v5 에서 실행되고 v1.0.10 에 온전히 보존**됐다.

사실관계(라인 대조):
- **v4-11(SPEC 최종)**: 파생 C = `\subsection{파생 C — 상호작용에 의한 유효 폭 w_eff(Ω)}`(L516). 유도 dV_eq/dθ|½=(4RT−2Ω)/F=4(RT−Ω/2)/F → **boxed `w_eff(Ω)=w(1−Ω/2RT)`**(정답형), "Ω>0 → w_eff<w 봉우리 좁아진다", "Ω→2RT⁻ w_eff→0 delta형 plateau" + 전용 TikZ `fig:weff`. 이 형태 자체는 R2/A1/A2 가 "정답·견고"로 판정한 것.
- **v5·v1.0.10**: 파생 C = `\subsection{파생 C — 폭 w 의 지위: 단상 평형 예측 vs. 두-상 현상학적 피팅 폭}`(v1.0.10 L539). **w_eff 공식·fig:weff 완전 제거**. 대체: (단상 Ω<2RT=평형 예측 w=RT/F / 두-상 Ω>2RT=현상학적 자유 피팅 폭) 이중지위 + 세 broadening 출처(i 유한율속 비대칭꼬리 ii 내재 RT/F iii 집합 다입자 apparent-U=U_j+η 앙상블), 상세는 Ch1 broadening 절로 이관(L553–555).

정정 근거(v5 헤더 L8–9 verbatim): "★v5 정정(v4 대비): 파생 C(w_eff(Ω)=w(1-Ω/2RT) '상호작용이 종을 좁힘') 절 완전 제거 — two-phase 실측은 *종*이지 델타가 아니라 narrowing 그림이 틀림." 이는 계획서 SPEC(L9 "w 이중지위… w_eff 완전제거", L10 "C=w_eff… 섞임항")·AUTHOR_BRIEF 궤적과 정확히 일치.

**Ch1 w_eff 제거와 Ch2 섞임항 C 의 관계·정합(base 명시 질의):** 완전 정합·coordinated.
- Ch1 v1.0.10 헤더 L20: "w_eff 제거(eq:weff·func_w_eff·use_w_eff·w_eff_floor_frac 자취 0; two-phase 실측은 종이지 델타 아님 — narrowing 반대방향)" — **Ch1 도 동일 근거로 w_eff 삭제**.
- Ch1 broadening 절(L1267–1352)이 Ch2 파생 C 가 이관한 세 출처를 실제 전개: ①=Ch2(i) 유한율속 L_V 꼬리, ②=Ch2(ii) 내재 RT/F, ③=Ch2(iii) Dreyer plateau(iii-a)+apparent-U=U_j+η 앙상블 forward 평균 `eq:ensavg`(iii-b) + 역산 금지(forward-only, ill-posed)+입자 크기 전면 배제. **Ch2 의 이관 선언(L553–555)이 Ch1 실체와 1:1 대응** — dangling 아님.
- 곧 Ch1·Ch2 는 **같은 물리(평형 델타를 종으로 펴는 것은 narrowing 이 아니라 η-broadening)를 공유**하며 역할만 분담(Ch1=broadening 상세 전개, Ch2=w_j 의 지위 못박기). 두 장이 상충하는 w-서술을 남기지 않음.

이유(왜 개선): 축1(이론 무결) — v4 의 w_eff=w(1−Ω/2RT) "상호작용이 봉우리를 좁혀 델타로"는 실측(두-상 peak=유한 폭 종)과 방향이 반대. R2/A1/A2 가 "수식으로는 정답"이라 판정했으나 그 수식이 서술하는 물리 그림 자체가 실데이터와 어긋난다는 상위 판단이 v10 에서 내려졌고, v5 가 이를 반영. **v1.0.10 은 이 정정을 축소·훼손 없이 계승**(파생 C 절 전문·warnbox "w 는 종의 폭이지 '상호작용이 좁힌 델타'가 아니다" L561–568 보존).

★**오적발 자기표시**: base 는 "bell/w_eff 은 결함 아님"을 경고했다. 만약 현행 문건만 보고 "파생 C 에 w_eff 유도식이 사라졌다 = v4 의 우수 유도 손실"이라 등급 매기면 **오적발**이다. 이력 대조 결과 이는 손실이 아니라 상위 supersession 이므로 **결함 0** 으로 판정한다.

---

## 3. 나머지 통계열역학 본체(config/vib/elec·A/B/D·극한 I·q_rev) 인계

### 3-A. v5 → v1.0.10 변경 전수(Compare-Object 실측) — 전부 개선/정합 [PASS]

**[개선·정합/축1·2] · 위치: 아래 라인** — v5→v1.0.10 변경은 총 <10줄이며 손실 0:
1. `Chapter 1 v9` → `Chapter 1`(L395·L399·L400): v9 이 통합 Ch1 이 됐으므로 버전 라벨 정리(정당).
2. `Anode_Fit_v11` → `Anode_Fit_v1.0.10`(srcbox L485·bib L747): 코드 참조 갱신(정당·코드 회귀 아님, 파일명만).
3. **A2-D3(HIGH) 정정 반영**: 파생 A 정규화 `가중 분모 ΣQ_jg_j 가 정확히 측정 dQ/dV(=∂x/∂U)`(v5) → `(=Q ∂x/∂U; x 무차원이라 Q 배)`(v1.0.10 L479). A2 가 "정확히"는 Q_tot 배 누락이라 지적(D3)한 것을 **v1.0.10 이 정확히 정정** — 인계 개선.
4. q_rev 유도(L652): v5 의 중간단계 `T ΔS/T` 축약 → 직접 대입 서술. 물리 무변, 간결화.
5. **범위 가드 강화**: srcbox 부호규약에 `전셀 조립 시 음극 몫은 부호 반전 +IT∂U_an/∂T 로 들어가나 본 장 범위 밖`(L653) 추가 — 범위 명시 강화.
6. **broadening 이관 명문화**: keybox 폭 이중지위에 `w_j=n_jRT/F 는 §revheat·코드 func_w`(L162)·occupation2019 인용에 `방법 수준·dilute 한정`(L251) 단서 추가 — 정직성 강화(v10 의 전이별 n-factor broadening 복원과 정합).

→ v5→v1.0.10 은 **degradation 0, 개선 6건**. FIX_LIST(A2-D3)·정직 단서가 실제 반영됨.

### 3-B. 이중계산 B — 인계 무결 [PASS·정독 근거]
**[무결·G-follow/축1] · 위치: v1.0.10 L293–309(warnbox)·L524–537(파생 B 절)·L668–685(use-this) ↔ v4-11 L287–306·L516–537 ↔ R2 정답·A1 표적4-2부**
ΔS⁰_j≡ΔS_rxn,j≡[ΔS(x)]_{ξ=½}(config=0) 정의(L294–296) → 분해 `ΔS(x)=ΔS⁰_j + R ln[ξ/(1−ξ)] + δS_vib/e`(L301–305, boxed) → "config 를 ΔS⁰_j 에 또 더하면 이중계산"(L299·L535). 중심 config=0 이라 두 정의 모순 없이 맞물림. v4-11 의 파생 B warnbox 와 **내용 byte-동일**(config 제거 편집이 B 를 건드리지 않음 확인). 이중가산 0.

### 3-C. vib(BE)·elec(Sommerfeld) — 인계 무결 + FIX_LIST 이행 [PASS]
**[무결·G-derive/축1] · 위치: v1.0.10 L359–409 ↔ A1-H1(HIGH)·FIX_LIST_v411 §1**
- `eq:Svib_mode`(L365) S_vib,k=kB[(1+n_k)ln(1+n_k)−n_k ln n_k] — 보손 (1+n) 인자·부호 정확.
- `eq:Se`(L391) S_e=(π²/3)kB²T g(E_F), T-선형. **A1-H1/FIX_LIST 이 지적한 "Sommerfeld 중간대수 생략"이 정정됨**: L386–389 에 Sommerfeld 적분 ∫(−∂f/∂E)(E−E_F)²dE=(π²/3)(kBT)²·전자비열 C_e·S_e=∫(C_e/T′)dT′ 중간단계가 실려 있어 A1-H1 의 "인용 점프" HIGH 가 해소. → FIX_LIST_v411 §1(A1-H1) 이행 확인.
- ΔS_e<0(리튬화, L401)·MIT 예외(x-의존 유지, L406–408) 보존 — Ch1 v9 전자엔트로피 규약 정합.

### 3-D. 극한·코너 I — 인계 무결 [PASS·정독 근거]
**[무결·G-usable/축1·2] · 위치: v1.0.10 L596–634(tab:limits 6코너+keybox) ↔ A2 표적I·AUTHOR_BRIEF 항6**
6 코너(ξ→1 config+∞ / ξ→0 config−∞ / ξ=½ 표준값 config=0 / **Ω→2RT plateau** / 단일봉우리 환원 / 고온 Sommerfeld S_e∝T) 전부 A2 가 확인한 정답 극한 보존. **Ω→2RT 행은 w_eff 제거와 정합되게 재서술**: "실측 두-상 폭은 현상학적 피팅(§weff)"(L613)·keybox (iii)(L623–624). "ΔS_rxn,j 전이당 상수" 근사 타당성 판정(비선형=겹침+분포 config 자동생성)·MIT 예외(L631–632) 보존.

### 3-E. 가역열 q_rev·exo/endo·Bernardi — 인계 무결 [PASS]
**[무결·축1] · 위치: v1.0.10 L636–666 ↔ R3 정답·A1 표적3**
- `eq:qrev`(L643–645) Q̇=I(U_oc−V)−IT∂U/∂T, Q̇_rev=−IT∂U/∂T=−(IT/F)ΔS — Bernardi 골격·가역/비가역 분리 보존.
- srcbox 부호규약 ΔS=−∂(ΔG)/∂T=+F∂U_oc/∂T(L651–653) 자기일관.
- **exo/endo 6매핑 정답 보존**(R3 이 v4-04 등 역매핑 CRITICAL 로 기각한 함정을 회피): ΔS>0→방전 흡열, ΔS<0→발열, 저-x config양 발산→방전 흡열, stage2→1 큰 음 ΔS→방전 발열(L658–664). **역매핑 잔존 0**.
- 파생 D 히스(L570–593): 분기별 g_j^(d) 가중·가역=분기평균 `eq:hys_rev`·비가역=히스 gap 소산 분리 — A2 표적D 정답 보존.

### 3-F. 파생 A 수치검증·"선두차수" 오칭 정정 [PASS·FIX_LIST 이행]
**[개선/축1] · 위치: v1.0.10 srcbox L484–495·한계갭 L687–692 ↔ A1-L1/A2-D1·FIX_LIST_v411 §2**
175점 검증(완전식 abs-err≈0 / 단순식 max 0.18 mV/K / config 잔차 [−0.21,+0.14] mV/K)·연속 블렌드(계단 아님) 서술이 A2 독립재현 수치와 일치. **A2-D1/A1-L1 이 지적한 "선두차수까지다" 오귀속이 v1.0.10 에서 부재**: 한계갭(1)(L687–692)이 남는 공백을 "고차 보정"이 아니라 "logistic 형·파라미터 집합의 실데이터 round-trip 피팅"으로 정확히 프레이밍. → FIX_LIST_v411 §2 이행 확인.

---

## 4. v3 → v4 전환 확인 (skeleton 탈피) [PASS]

**[개선/축1·2] · 위치: v3 L2–7·L53 ↔ v4-11 전체 ↔ AUTHOR_BRIEF L3·L6**
v3(243줄)는 헤더·본문에서 스스로 "이 장은 **새 물리를 더하지 않는다**"(L53)라 명시 — Ch1 의 ∂U_j/∂T 추출 + Bernardi 수지 + MSMR-template 추정만 담은 얇은 초안(분배함수→점유분포→S=−R∑p ln p **부재**). AUTHOR_BRIEF 가 "Ch1+ΔS 한 절 수준 탈피" 를 v4 목표로 못박은 그 baseline 그대로. v4-11(713줄)이 통계열역학 본체(분배함수·점유분포·config/vib/elec·섞임 A/B/C/D·극한 I)를 신규 구축 → **v3→v4 는 진성 챕터급 상향**(축2 교과서성 확보). 이 본체가 v5·v1.0.10 까지 보존됨은 §1·§3 에서 확인.

---

## 5. 가장 약한 1곳 (refute 집중)

**파생 C 이관의 단방향 의존성 — Ch2 L553–555 가 "Chapter 1 broadening 절"에 전적으로 의존.** 이것이 인계 결함은 아니나(Ch1 v1.0.10 L1267–1352 에 실체 존재 확인 완료), **가장 취약한 연결점**이다. 근거·리스크:
- Ch2 파생 C 는 w_eff 유도(자기완결 수식)를 버리고 broadening 물리를 **전부 Ch1 에 위임**했다. 현재 Ch1 broadening 절이 세 출처·apparent-U·forward-only·크기배제를 온전히 담아 정합하나, **두 장이 별도 파일·별도 버전 관리**되므로 향후 Ch1 broadening 절이 개정되면 Ch2 파생 C 의 이관 선언이 stale 될 구조적 위험이 있다. 현재 시점 판정은 **정합(결함 0)**이되, v1.0.11 핸드오버에 "Ch1 §broadening ↔ Ch2 파생 C 는 동반 개정" 제약을 명기 권고.
- 부차: v1.0.10 파생 C 는 정성 서술(이중지위·세 출처)만 있고 수식이 0 이다. 축1(전개과정까지 식) 관점에서 이 절만은 "식이 아니라 말"이나, broadening 의 정량 물리는 Ch1 소관이므로 Ch2 에 수식 요구는 범위 밖 — **정당한 서술절**로 판단(오적발 방지).

(빈 통과 금지 준수: PASS 판정 영역도 §1·§3-B~F 에서 현행 줄번호·SPEC 줄번호·정답값으로 적대 대조함.)

---

## 6. 버전 전환별 인계 판정 (Ch2 통계열역학 초점)

| 전환 | 판정 | 근거 |
|---|---|---|
| **v3 → v4** | **개선(챕터급 상향)** | 얇은 skeleton(243줄, "새 물리 X")→통계열역학 본체 신규(713줄). AUTHOR_BRIEF 목표 달성. §4 |
| **v4 → v5** | **개선(의도된 정정)** | 파생 C w_eff=w(1−Ω/2RT) "narrowing" 제거(실측=broadened 종이지 delta 아님)→폭 이중지위+broadening 이관. 통계열역학 본체(A/B/D·config/vib/elec·극한·q_rev) 보존. §2 |
| **v5 → v1.0.10** | **보존+개선** | Compare-Object 실측 변경 <10줄, degradation 0. A2-D3 정규화 정정·A1-H1 Sommerfeld 중간대수·"선두차수" 오칭 제거 등 FIX_LIST 이행. 버전 라벨·코드 참조 갱신. §3-A·3-C·3-F |
| **종합(v4→v1.0.10)** | **인계 무결 + 개선** | G-derive 점프0·config 부호·이중계산 B·극한 6코너·exo/endo·Bernardi 전부 보존. w_eff 는 의도된 supersession. **인계 결함 0.** |

---

## 7. 5줄 요약

1. **초점**: Ch2 통계열역학 인계(분배함수→점유분포→config/vib/elec·섞임 A/C/D/I·극한 I·가역열·이중계산 B·G-derive) 의 v3→v4→v5→v1.0.10 보존.
2. **인계 결함 수 = 0**(강등·손실 0). 검출된 것은 전부 **개선/정합**(FIX_LIST A1-H1·A2-D1·A2-D3 이행, 범위 가드·정직 단서 강화) + 의도된 supersession(파생 C w_eff 제거).
3. **최중대(가장 약한 곳)**: 결함 아닌 구조적 리스크 — 파생 C 가 broadening 물리를 Ch1 §broadening 에 단방향 위임(현재 정합, 향후 동반 개정 제약 필요). v1.0.11 핸드오버에 명기 권고.
4. **두 축 유지 판정**: 축1(전개 비약0·G-derive) **유지**(config 사슬 Z→⟨n⟩→S 완전전개·N_A 단위다리·Sommerfeld 중간대수 정정 반영) · 축2(교과서 follow·G-usable) **유지**(v3 skeleton 탈피 후 챕터급 본체 보존, use-this 종합식·6코너 극한·절도입/마무리 다리).
5. **★오적발 자기표시**: 파생 C 에서 v4 의 w_eff=w(1−Ω/2RT) 유도식이 사라진 것을 "우수 유도 손실"로 등급 매기면 **오적발**임 — 이력 대조 결과 v10-era 의 의도된 물리 정정(narrowing 그림이 실측 방향과 반대)이며 Ch1 w_eff 제거와 coordinated. base 의 "bell/w_eff 은 결함 아님" 경고에 부합, 결함 0 으로 확정.
