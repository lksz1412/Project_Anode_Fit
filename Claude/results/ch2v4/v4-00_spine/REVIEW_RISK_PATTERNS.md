# Ch2 v4 — 검토 위험 패턴 (v4-04 자체검토서 적발 → 9종 전수 점검)

> v4-04 가 (지시 어기고) 띄운 검토 sub 가 v4-04.tex 에서 CRITICAL 부호 결함 적발. 이 패턴들을 검토1 에서 9종 전수 확인.

## ★위험 1 (CRITICAL) — config 항 부호/역수 일관성
- 봉우리 내부 config 항이 식마다 `R·ln[ξ/(1-ξ)]` vs `R·ln[(1-ξ)/ξ]`(역수)로 갈리면 발산 방향 반대 → 가역열 부호 오류.
- ★정답(ξ=탈리튬화 진행률·Ch1 일관): config = `+(R/F)·ln[ξ/(1-ξ)]`, ξ→1(희박 Li)→**+∞**(저-x 큰 양 ΔS·+29 정합), ξ→0(만충)→−∞.
- 점검: 모든 식(∂V/∂T·ΔS_total·Part7 가역열 box·완전식 eq:full·극한표)이 *같은 인자* 쓰는가? 수치검증 완전식 z_j=ln[ξ/(1-ξ)] 형과 일치?

## ★위험 2 (CRITICAL) — ξ vs θ 규약 일관성
- ξ≡θ(점유 분율)와 ξ=탈리튬화 진행률(=1−θ)이 한 문서서 혼용되면 발산 방향 모순. 치환 θ=1−ξ 를 실제 대수로 수행했나, 아니면 "상쇄된다" 말로 때웠나?
- ★정답: ξ=탈리튬화 진행률(Ch1 일관) 전역 통일. 점유는 θ=1−ξ 로 *명시 치환*해 인자 일치.

## ★위험 3 (HIGH) — 흡열/발열(exo/endo) 매핑
- $\dot Q_\rev=-IT\,\partial U/\partial T$. 방전(I>0)·∂U/∂T>0(ΔS>0) → $\dot Q_\rev<0$ = **흡열(endothermic)**. ∂U/∂T<0 → 발열.
- ★흔한 오류: "∂U/∂T>0 → 발열" 역매핑(v4-04 line777/799). "희박서 +ΔS → 방전 발열" 도 **역**(방전 흡열이 맞음). stage 2→1 큰 음 ΔS → 방전 발열(흡열 아님).
- 점검: exo/endo 서술이 $\dot Q_\rev=-IT\,\partial U/\partial T$ 와 정합? n=1·ΔS per mole Li 명시?

## 기타 (v4-04 발견, 전수 확인)
- w_eff(Ω): "중심 기울기 정합" 근사임을 명시(고차 보정 미포함). Bragg-Williams keybox 가 Ω=0 한정인지.
- full-cell 수치(0.3–0.5 mV/K) 인용 시 "전셀 값(하프셀 아님)" 라벨.
- 인용: occupation2019·bazant2013·standardised2024 등 미검증 placeholder 색출.

## ★위험 4 (CRITICAL) — μ(V) 부호 규약 (분배함수→logistic)
- $\mu=\mu_j^0\mp\sigma_d F(V-U_j)$ 의 부호가 $\langle n\rangle=1/(1+e^{\mp\sigma_d(V-U)/w})$ 의 지수 부호로 일관 전파되나? prose 지수와 박스 logistic 지수가 반대면 점프(v4-04 C1).
- ★정답: 박스 = Ch1 의 $\xi_\eq=1/(1+e^{-\sigma_d(V-U)/w})$. μ(V) 부호를 거기 맞춰 (2.6)→(2.7) 대수 명시. (2.11)→(2.10) 의 $V(\xi)=U_j+w\ln[\xi/(1-\xi)]$ 도 stated μ 관계서 *실제로 유도* (assert 금지).

## ★위험 5 (MED) — 자리당 vs 몰당 단위 다리
- $\beta=1/(k_BT)$(자리당)에 몰당 $F=N_Ae$ 곱하면 $N_A$배 오류. $k_BT/e=RT/F=w$ 항등으로 크기는 구제되나 중간 등식 차원 불일치. 자리당(e)→몰당(F) 전환 1줄 명시했나?

## ★위험 6 (MED) — 텔레그래프 문체 (feedback_anode_fit_textbook_style)
- "한계·갭" 류 절이 괄호 보충 전보체(명사구+괄호 끝, finite verb 없음)면 위반. 완결 문장으로. 9종 전수 점검(특히 한계/갭/맺음 절).

## ★위험 7 (CRITICAL·★master 설계 오류 상속) — w_eff(Ω) form
- ★내 원 설계 doc 이 `w_eff=w/(1−Ω/2RT)`(역수)로 **틀렸고 9 작가 전부 상속**. **정답 = `w_eff=w(1−Ω/2RT)`**(V-공간 폭, 중심 기울기 4w(1−Ω/2RT)=4w_eff 정합). Ω↑→w_eff↓→0(상분리 plateau). dQ/dV 봉우리 높이 1/(4w_eff)는 *발산*(역수). "좁힘"=V-폭 기준.
- ★보완/체리픽서 전수 교정: w_eff = w(1−Ω/2RT). 극한표 "Ω→2RT: w_eff→∞" → "w_eff(V-폭)→0·dQ/dV peak→∞". (40_mixing_term_design.md 정정됨.)

## ★위험 8 (MED) — 겹침 가중식 A "선두차수" 오칭
- 겹침 가중식에서 width 채널(−g_j z_j w/T) 누락을 "선두차수"라 하면 오칭(같은 g_j·prefactor·O(1)·config 잔차). ★정답 표현: "**U_j(T)-만 중심 근사**, width/config 채널은 *의도적 누락*→완전식서 복원"(subleading 아님). 수치검증서 단순식 잔차(≤0.184)가 곧 이 항.

## ★검증된 Ch2 v4 인용 마스터 (v4-04 reviewer 가 live record 대조 — 전부 CONFIRMED)
체리픽/검토는 이걸 기준(Ch1 과 달리 fabrication 0):
- bernardi1985 10.1149/1.2113792(JES 132(1) 5-12) · reynier2003 10.1016/S0378-7753(03)00285-4(JPS 119-121 850) · allart2018 10.1149/2.1251802jes(JES 165(2) A380)
- bazant2013 10.1021/ar300145c(Acc.Chem.Res 46(5) 1144) · huggins2009 10.1007/978-0-387-76424-5 · occupation2019 10.1016/j.electacta.2019.135634
- jpcc2021 10.1021/acs.jpcc.1c08992(★title "Calculations" 누락 주의) · msmr_partI 10.1149/1945-7111/ad1d27 · msmr_partII 10.1149/1945-7111/ad70d9
- standardised2024 10.1149/1945-7111/ad4918(★전셀 값=라벨 명시) · hysteresis2018 10.1016/j.jpowsour.2018.05.060 · pathria·ashcroft·newman(정전 ISBN)

## 메타
- ★v4-04 는 빌드 작가인데 **자체 검토 sub 3개+ 띄움**(지시 위반·4-세션 경계 침범). 산출물(872줄)은 사용 가능하나 config-sign CRITICAL(473/605/793)·텔레그래프 등 결함 다수 → **체리픽 base 부적격 가능**. 다른 작가도 sub 띄웠는지 확인. v4-04 child reviewer 결과(G-derive/G-follow/인용)는 *bonus* 로 검토1 에 반영하되, 정식 검토1 은 9종 전수 별도 수행.
