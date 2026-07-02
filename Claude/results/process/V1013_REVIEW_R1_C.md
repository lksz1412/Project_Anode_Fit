# V1013 REVIEW — Round 1, 검수자 C

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` (Ch1 L1815–말미 = ★Part II 전체 + 전체 입력 인자·facade·signcheck; 맥락상 L1755부터 정독) · `graphite_ica_ch2_v1.0.13.tex` 전문 (L1–779) · 코드 상호충실도 `Anode_Fit_v1.0.13.py` 대조 정독(부분).
- mandate: refute(반증 시도) · 의견만(tex/코드 수정 0건) · 모든 지적에 줄 번호·원문 인용.
- 최중점 판정 선결론: **f=+σ_d · Δμ=+sF(V−U) · H-1 BW 부호 — 3건 모두 무훼손(PASS)**. 상세는 말미 "물리 불변 확인".

---

## 지적 사항 (등급순)

### [HIGH] C-01 — Ch2 L679·L688–694: eq:qrev 의 "방전(I>0)" 라벨이 Ch1 확정 방향 규약(eq:lco-sigmaslot)의 "흑연 하프셀 방전" 라벨과 화학 방향이 반대 — 무표기 충돌
- 무엇이: Ch2 L679 "($I>0$ 방전, $V$ 단자 전압, $U_\oc$ 평형 전위)" 및 L688–692 "방전($I>0$)에서 $\Delta S>0$ 이면 $\dot Q_\rev<0$ 으로 흡열 … 저-$x$ 에서 config 양의 발산이 지배해 $\Delta S>0$ 이므로 방전 시 $\dot Q_\rev<0$(흡열)".
- 근거(재유도): Bernardi 수지의 $\dot Q_\irr=I(U_\oc-V)\ge0$ 조건은 $I>0 \Leftrightarrow V<U_\oc$, 곧 코인 셀(흑연 양단자 vs Li)의 **자발 방향 = 흑연 환원 = 리튬화**를 강제한다. 삽입 기준 ΔS>0(저-x, +29 J/(mol K))에서 리튬화가 TΔS≈+8.6 kJ/mol 흡수 → "방전=리튬화" 로 읽어야만 L688–694 의 흡열/발열 서술과 calorimetry 정합이 전부 성립한다(검산 일치). 그런데 Ch1 L1886–1887(eq:lco-sigmaslot)·fig:lco-dirmap 은 "흑연 하프셀 — 방전↦σ_d=+1(**탈리튬화**)" 로 라벨을 확정했다. 같은 단어 "방전"이 두 챕터에서 반대 화학 방향이다. Ch1 라벨을 들고 Ch2 를 읽으면(방전=탈리튬화, ΔS_실반응=−29) 모든 흡열/발열 판정이 반전된다. Ch1 이 §lco-direction 을 신설한 목적(부호 실수 가드)이 정작 Ch2 대표 산출식 문단에는 미적용.
- 수정안: eq:qrev 직후 1문장 삽입 — "여기서 $I>0$ 방전은 **코인 셀의 전기화학적 방전 = 작동전극(흑연) 리튬화**($V<U_\oc$ 자발 방향)이며, Ch1 흑연 하프셀 라벨 '방전'(탈리튬화, $\sigma_d{=}+1$)과는 반대 방향임에 주의" — 또는 $\dot Q_\rev$ 를 σ_d 언어(탈리튬화 $\sigma_d=+1$ 시 $I=-|I|$ 대입)로 재진술. 식 자체는 표준·무결(방향에 선형이라 charge 는 $I<0$ 으로 자동 처리)이므로 라벨 명시만으로 닫힌다.

### [HIGH] C-02 — Ch1 L1855–1857 (tab:lco-staging 캡션): 코드 현행(루프 B)과 어긋난 구판 서술 — "x_MIT=0.50·전자항 중간 dict" 는 이미 폐기된 상태
- 무엇이: 캡션 "★코드 \code{LCO\_MSMR\_LIT} 시연값($U{=}3.930/3.880/4.050$ V, $x_\mathrm{MIT}{=}0.50$, 전자항을 중간 dict 에 배정)은 tier-C placeholder … (피팅 시 전자항은 T1=MIT dict 로 재정렬)".
- 근거(코드 대조): `Anode_Fit_v1.0.13.py` L640–645 — "[v1.0.13 루프 B] 전자항을 물리 anchor(T1=MIT, x_MIT≈0.85 …) dict 로 재정렬(구판은 중간 dict x_MIT=0.50 tier-C 시연 배정)" + 실제 첫 dict(U=3.930)에 `'electronic': True, 'x_MIT': 0.85, 'g_max_eV': 13.0, 'dx_MIT': 0.05`. 곧 재정렬은 **이미 완료**됐고 x_MIT=0.50·중간 dict 배정은 현존하지 않는다. 같은 Ch1 안에서도 §lco-code (ii) L2667 "T1 전이의 $\Delta S_{\rxn}$ 평가에 몰당 전자항을 더하는 한 줄" 이 현행(T1)을 말해 캡션과 자기모순. (U 시연값 3.930/3.880/4.050 자체와 "동결 상수 오프셋" 서술은 코드와 일치 — 문제는 dict 배정·x_MIT 두 사실만.)
- 수정안: 캡션을 "…시연값($U{=}3.930/3.880/4.050$ V; 전자항은 T1=MIT dict, $x_\mathrm{MIT}{=}0.85$ 물리 anchor 로 배정 — v1.0.13 루프 B 재정렬 완료)…" 로 갱신하고 "(피팅 시 … 재정렬)" 예고문 삭제.

### [HIGH] C-03 — Ch2 L459 (eq:implicit)·L710 vs L78·L345–350(tab:ds)·L690: 기호 $x$ 가 한 챕터 안에서 서로 반대 방향의 두 좌표로 사용
- 무엇이: eq:implicit "$\sum_j Q_j\,\xi_{\eq,j}(U_\oc,T)=Q\,x$" 와 procedurebox L710 "주어진 SOC $x$" 의 $x$ 는 **탈리튬화(추출 전하) 분율**이어야 성립한다 — 만충에서 모든 $\xi_j=0$ 이므로 좌변 0, 우변 $Qx$ 가 0 이려면 만충 $x{=}0$. 반면 서 L78("$x$ 작을 때 양"), tab:ds(4→3 = $x$ 0.08–0.16, 2→1 = $x$ 0.50–1.00), L690("저-$x$ 에서 config 양의 발산") 의 $x$ 는 **Li 함량**(만충 $x{=}1$)이다. 같은 기호, 반대 배향, 변환 각주 없음. fig:blend 축 라벨 "x (delithiation)"(L528)은 전자, tab:ds 는 후자.
- 근거(무해성 한정): eq:implicit_diff 의 비(比)는 $\theta=1-\xi$ 치환에 불변이라($\partial\theta/\partial T=-\partial\xi/\partial T$, $\partial\theta/\partial U=-\partial\xi/\partial U$ — 분자·분모 동시 부호 반전 상쇄) 최종 가중식·종합식 수치는 무영향. 순수 좌표 라벨 충돌이나, 종합식 사용자가 tab:ds(Li 함량)로 anchor 대조하며 eq:implicit(탈리튬화 분율)로 $\xi_j$ 를 풀면 SOC 축이 뒤집힐 실장 위험.
- 수정안: eq:implicit 직전에 "$x$ = Li 함량" 으로 통일하고 식을 $\sum_jQ_j\theta_{\eq,j}=Qx$(또는 $\sum_jQ_j\xi_j=Q(1-x)$)로 적거나, 별도 기호($\bar x\equiv1-x$)를 도입해 fig:blend 축·procedurebox 도 함께 정합.

### [MED] C-04 — Ch1 L2780–2782 (facade)·L2795 (tab:nodemap N0): curve() 의 σ_d 환산 서술이 코드의 전극 인지 변환(루프 B)을 누락
- 무엇이: "상위 \code{curve} 가 실험조건을 받아 $\sigma_d=\code{\_direction\_to\_sigma}$ … 로 환산해 \code{dqdv} 를 재사용한다" — 흑연 base 클래스에만 참인 서술.
- 근거(코드 대조): 코드 L530–535 — `sigma_d = self._direction_to_sigma(direction)` 후 `if not self._delith_is_discharge: sigma_d = -sigma_d`(전극 인지 환산, Ch1 eq:lco-sigmaslot 구현), L682 `LCOCathodeDQDV._delith_is_discharge = False`, L669–672 "LCO 충전 곡선은 direction='charge' 그대로 주면 σ_d=+1 슬롯에 간다". Ch1 전체에 `_delith_is_discharge`/전극 인지 언급 0건(grep). Part II 가 세운 방향 규약이 코드에서 **어떻게** 라벨→물리부호로 구현되는지가 문건에 없어, facade 문장은 LCO 클래스에 대해 사실과 다르다(-σ_d 반전 생략).
- 수정안: facade 문단에 1문장 — "LCO 서브클래스는 전극 인지 플래그(\code{\_delith\_is\_discharge}=False)로 셀 라벨을 탈리튬화 부호로 자동 환산한다('charge'↦$\sigma_d{=}+1$; 저수준 \code{dqdv}(s=…) 는 물리 부호 직접)". tab:nodemap N0′ 행에도 반영 권장.

### [MED] C-05 — Ch1 L2844–2846 vs L2847–2866 vs L2867: 부호 회귀 self-test 항 수 자기모순("네 항" ↔ R1–R5 5항 ↔ "다섯 회귀 항") + 코드 대응 과대 서술
- 무엇이: 도입 "아래 **네 항**은 코드 \code{\_\_main\_\_} 의 self-test 와 같은 양을 손으로 재산출한 것이며", 목록은 R1–R5 **다섯** 항, 마무리 "**다섯** 회귀 항이 모두 통과한다".
- 근거(코드 대조): `__main__`(코드 L743–879)에 직접 대응 존재 = R1(Ω=12000·γ=1 분기, L813–822)·R2(Ω=2RT→0, L835–836)·R3(|I|→0 dis/chg 일치, L838–841). R4($\partial\ln L_q/\partial V$ 동결)·R5(꼬리 두 극한 ρ)는 대응하는 `__main__` 수치 테스트가 없다(가장 근접한 것은 L824–831 꼬리 방향 역전 테스트 — R5 의 극한 검사와 다른 양). 곧 "네 항 … 같은 양" 은 수(4≠5)와 대응(3건만 직접) 양쪽에서 부정확 — 직전 R5 추가(D-PEAK 회귀) 시 도입부 미갱신으로 보임(렌즈 ⑧).
- 수정안: "아래 다섯 항 중 R1–R3 은 \code{\_\_main\_\_} self-test 와 같은 양의 수기 재산출, R4 는 컷 규칙 정의 검사, R5 는 극한 논증(코드 분기 스위치로 회귀)" 식으로 재서술.

### [MED] C-06 — Ch2 L333: "MCMB 흑연 엔트로피 계수가 저-$x$ 에서 $+3\sim4$ mV/K" — 같은 문단 내부 스케일과 10배 이상 모순, 본 문서 모델로 재현 불가능한 값
- 근거(적대 검산): 직전 문장의 anchor ΔS≈+29 J/(mol K) ⇒ $\partial U/\partial T=29/96485=+0.30$ mV/K. +3.5 mV/K 이려면 ΔS≈+338 J/(mol K) 필요. 본 장 자신의 config 발산 항 $R\ln[\xi/(1-\xi)]/F$ 로도 $x{=}10^{-5}$ 에서 ≈0.85 mV/K, $x{=}10^{-9}$ 에서 ≈2.1 mV/K(로그 발산) — 물리적 조성 범위에서 +3~4 mV/K 도달 불가. msmr\_partII 원문 값 재확인 필요(0.3~0.4 mV/K 의 자릿수 오기 가능성). 4-tier: **미검증**(원문 대조 못함) — 단 내부 부정합은 확정.
- 수정안: 원문 재확인 후 수치 정정 또는 "(전셀/타 단위 보고값 — 본 문서 스케일과 상이)" 각주.

### [MED] C-07 — Ch2 L506·L716–718: "완전식은 175 점 전 범위에서 유한차분값과 부동소수점 정밀도로 일치(절대오차 ≈0 mV/K)" — 겹침 구간에서 원리적으로 성립 불가한 과장
- 근거(재유도): $U_\oc(x,T)$ 가 $T$ 에 정확히 affine 인 것은 **단일 전이 지배** 한계뿐이다 — 그때는 전하 보존이 $\xi_j$ 를 고정해 $U_\oc=U_j(T)+w_j(T)z_j$($z_j$ 상수). 겹침 구간에선 $z_j=F(u-U_{j0})/(n_jRT)+\text{const}$ 의 $1/T$ 재배분 때문에 $\partial^2U_\oc/\partial T^2\ne0$ 이고, $\Delta T{=}6$ K 편측 유한차분과 점미분의 차는 $\tfrac12\Delta T\,\partial^2U/\partial T^2$ ~ 수 µV/K 급(추정 0.003–0.012 mV/K)으로 남는다 — 0.18 mV/K(단순식 오차)보다 작지만 부동소수점(10⁻¹⁶ 상대) 급은 아니다. "부동소수점 정밀도" 가 문자 그대로면 비교 프로토콜이 순환(같은 사슬 재평가)이거나 평가 온도가 시컨트-정합이었을 것.
- 수정안: "표시 정밀도(≲10⁻² mV/K)로 일치" 로 완화하거나, numverif2026 의 비교 프로토콜(차분 방식·완전식 평가 온도)을 1문장 명시. (수치 자체 재실행은 본 라운드 범위 밖 — 미검증 표기.)

### [MED] C-08 — Ch1 전방 참조 3계열 (렌즈 ③): 정의 전 수식 라벨 참조
- (a) eq:U1T2(정의 L2345–2348)를 L1859(tab:lco-staging 캡션 "$\Delta S_e{\propto}T$ 의 다온도 $T^2$ 곡률(식~\eqref{eq:U1T2})")와 L2038–2039 에서 선참조.
- (b) eq:lco-decomp(정의 L2564–2569)를 L2027·L2053·L2056·L2062·L2179–2180·L2195 등 §lco-center·§lco-hys 전역에서 선참조.
- (c) 게이트 기호 $g_{\max}$·$\Delta x_\mathrm{MIT}$·$\sigma(1-\sigma)$ 를 정의(eq:ggate, L2360–2362) 전에 닫힌식으로 사용 — L2321–2323("이를 대입한 게이트형 몰당 닫힌식은 $-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_{\max}/\Delta x_\mathrm{MIT})\sigma(1-\sigma)$")·L2340–2343($a_e$ 정의). §lco-Se 독자는 아직 게이트 파라미터를 모른다.
- 수정안: (a)(b)는 절 참조(\S)로 강등하거나 "아래 \S…에서 정의" 병기, (c)는 $a_e$·닫힌식 문장을 §lco-gate 뒤로 이동하거나 기호 예고 1줄 삽입.

### [MED] C-09 — Ch1 L2178–2180 ↔ tab:lco-staging(L1866–1867): Motohashi anchor "$\approx1.49$ J/(mol K)@$x{=}\tfrac23$" 를 T3($x\approx0.48$) config 슬롯에 배정 — 조성 창 불일치 무해명
- 근거: $x=2/3\approx0.667$ 은 T3 창($x\approx0.48$)에도 T2 창($x\approx0.55$)에도 들지 않는다. tier A 는 값 자체의 등급일 뿐, "그 값을 T3 전이에 넣는다"는 배정은 문건 자체 기준(허위 정밀 금지·tier 병기)으로 근거 미제시.
- 수정안: 배정 근거(예: $x{=}\tfrac23$ 질서화가 전위축에서 T3 에 대응한다는 문헌 논거) 각주 추가, 불가하면 해당 슬롯 tier 를 B/C 로 하향하고 "조성 anchor 창 불일치 — 피팅 위임" 명시.

### [MED] C-10 — Ch2 L145–151 (eq:muV + C-2 각주): 평형 관계에 σ_d 기호 사용 + 본문 "충/방전 방향 부호(Chapter 1 규약)" 지칭 — Ch1 가드와 표기 충돌 (확정 판정 자체는 무훼손)
- 근거: Ch1 L1881–1883 은 "σ_d 가 모델에 들어가는 작용처는 셋뿐(분극·분기·꼬리)" 이고 평형 유도는 고정 부호 $s$(eq:eqcond, §sm-electro 표제 "$\mu_\mathrm{Li}=\mu^0-sF(V-U)$")를 쓴다. Ch2 eq:muV 는 같은 자리에 $\sigma_d$ 를 쓰고 본문이 이를 "충/방전 방향 부호"라 부른다 — 각주(C-2)가 "$s(=+1)$ 에 해당·값 동일" 로 정정하지만, 식에 $\sigma_d{=}-1$ 을 기계 대입하면 점유↔진행률이 뒤바뀌는 함정(여집합 교환이라 종형은 불변 — Ch1 이 명시한 바로 그 오독 경로)이 열려 있다. 대수 검증: $\varepsilon_0-\mu=+sF(V-U_j)$ → $\theta=[1+e^{+(V-U)/w}]^{-1}$ ✓ — **확정 판정 C-1(Δμ=+sF(V−U))과 동치, 훼손 없음**. 문제는 기호 선택·본문 지칭뿐.
- 수정안: eq:muV 를 $s$ 로 적고("$\mu=\mu^0-sF(V-U_j)$, $s{=}+1$ — 유도 전용 고정 부호, Ch1 eq:eqcond"), 각주는 "방향 부호 σ_d 와 혼동 금지" 로 역할 반전.

### [LOW] C-11 — Ch2 L644 (tab:limits): "$\Omega\to2RT^-$" 행이 "평형 등온선 비단조화$\to$plateau" 와 짝지어짐 — 접근 방향 표기 오류
- 근거: 비단조화(중앙 기울기 $+$ 반전, L216–219)는 $\Omega>2RT$ 측에서 발생. 아래(−)에서 접근하면 임계 도달까지 단조 유지. "$\Omega\to2RT^+$" 또는 무첨자 "$\Omega\to2RT$(임계)" 가 옳다.

### [LOW] C-12 — Ch1 L2071–2072: 약자 OD 첫 출현(eq:lco-J 의 "$\mathrm{OD}_a$·$\mathrm{OD}_b$")이 병기 지점(L2162 "order--disorder(OD)")보다 앞선다 — 약자 첫 출현 병기 규정 위반. 병기를 L2072 로 당길 것.

### [LOW] C-13 — Ch2 약자 자체 병기 누락: SOC(첫 출현 L78)·OCV(L598)·MCMB(L333) — Ch1 은 SOC 를 L2051 에서 병기하나 Ch2 는 독립 문서라 자체 첫 출현 병기 필요.

### [LOW] C-14 — Ch1 L2796 (tab:nodemap N1): "\code{dqdv} L430" 라인 앵커 부패 — 코드 실제 분극 계산 주석은 L436("# 분극: V_n = V_app − σ_d|I|R_n"). 코드 개정마다 썩는 라인 번호 대신 식별자·주석 앵커 권장.

### [LOW] C-15 — Ch2 L573–574: 파생 C "(상분리; 흑연 staging 전이가 여기 속함)" 무한정 서술 — 같은 문서 keybox L170–171("$2\mathrm L\!\to\!2\cdot2\!\to\!1$ 가 피팅 후에도 여기 남는 전이다")·Ch1 two-phase calibration(L2084–2088: 4건 중 2건만 잔존)과 어긋나는 과일반화. "staging 의 두-상 전이(2L→2·2→1)가 여기 속함" 으로 한정 필요.

### [LOW] C-16 — Ch1 '초기값' 이중 의미: L2093–2095 "Ω 수치 열을 싣지 않으며(초기값 미배정)·Ω=0 폴백" vs L2507–2509 "pure-LCO 초기값에서 세 전이 모두 $\Omega>2RT$ 의 두-상 측" — 전자는 수치 기본값, 후자는 문헌 물리 기대. 같은 단어가 두 층위로 쓰여 "미배정인데 >2RT?" 로 읽힐 수 있음. 후자를 "pure-LCO 문헌 물리에서" 로 어휘 교체 권장.

### [NOTE] C-17 — fig:lco-electronic(L2432–2437) 곡선 좌표는 정성 스케치: eq:ggate 대비 예컨대 xx=0.10($x{=}0.90$, $z{=}+1$)에서 도식 0.55 vs 식 $2.6[1-\sigma(1)]=0.70$ 등 최대 ~0.2 단위 편차. 중심 xx=0.15 에서 1.30=$g_{\max}/2$ 정확 ✓, 파선 봉 대칭 ✓, 축 매핑($x=1-$xx, $x_\mathrm{MIT}$ 점선 위치) ✓ — 결함 아닌 관찰(도식 성격 캡션 유지 시 무해).

### [NOTE] C-18 — fig:lco-electronic 캡션 L2446–2447 "작지만(O3 부분몰 $\approx0.18\,k_B$/atom)" — ★세 양의 구분(L2412–2419)이 "서로 다른 양이므로 한자리에 섞지 않는다·검산으로 쓰지 않는다" 고 못박은 두 척도를 캡션이 다시 병치. 괄호를 "게이트 골 −46 J/(mol K), 총합 대비 국소" 류로 교체 고려.

### [NOTE] C-19 — 기호 $g$ 3중 사용 관찰: Ch2 $g_j(x)$(종형 비중, L471)·$g(E_F)$(DOS, L408)·Ch1 $g(\xi)$(자유에너지). 국소 정의는 각각 명시돼 있어 결함은 아니나 종합식 사용 시 혼동 여지.

---

## 검산 통과 목록 (재계산·재유도로 확인 — 오적발 아님을 함께 보고)
$F\cdot0.83$ mV/K$=+80.1$ J/(mol K) ✓ · 30 K 창 +25 mV ✓ · 게이트 골 $-45.96$(300 K)/$-45.7$(298 K, 코드 주석 일치) ✓ · $S_e$ 끝점 $1.1\,k_B$ 및 게이트 적분과의 항등(몰당 9.19 vs 9.15 J/(mol K)) ✓ · $1/e_V^2\approx3.9\times10^{37}$ ✓ · 되먹임 14 mV$\lesssim w_1{=}30$ mV ✓ · R1: $u{=}0.766$, $\Delta U^\hys{=}86.7$ mV ✓ · $2RT{=}4958$ ✓ · 도핑 Taylor $\tfrac{8RT}{3F}u^3$ ✓ · spinodal $\xi_s^\pm$·$\Delta U^\hys$·대칭 평균 $U_j$ 대수 재유도 ✓ · eq:lco-belliden·peakobs($Q/4w$·면적 $Q$) ✓ · MSMR 사전(진행률 pairing 유일해 $f{=}+\sigma_d$, 직접 등치 시 $f{=}-\sigma_d$) 재유도 ✓ · Ch2 eq:occ→eq:logistic 부호 사슬 ✓ · eq:Veq\_BW↔Ch1 eq:lco-Veq($\theta{=}1{-}\xi$) 동치 = H-1 무훼손 ✓ · eq:slope\_BW·임계 $2RT$ ✓ · eq:dSconfig·dVdT\_config 부호 맞물림 ✓ · eq:dxidT 두 조각·eq:weighted·완전식 재유도 ✓ · $\Delta H^0=-FU+FT\partial_TU=-13.0$ kJ/mol ✓ · 파생 D 1차 상쇄 논리 ✓ · Kirchhoff 잉여항 논증 ✓ · 동결 근사 문건↔코드 일치 ✓ · Ω 미배정 폴백·"실질 활성 분극뿐" 문건↔코드 일치 ✓ · tab:inputs 기본값 전항 코드 일치(z\_cut 4.357·A\_cap 4.0·grid\_pad 0.15·n\_work\_min 2048·min\_lag 2.0·v\_span\_floor 1e-6·seed 298.15/0.1/1.0) ✓ · '천이' 잔재 0건(매치는 "원천이다" 오탐) ✓ · Ch1 라벨 중복 0건·미정의 참조 0건, Ch2 동일 ✓.

---

## 가장 약한 1곳
**C-01** (Ch2 L679·L688–694): 챕터 대표 산출식 $\dot Q_\rev$ 의 "방전(I>0)" 이 Ch1 확정 라벨(흑연 하프셀 방전=탈리튬화)과 반대 화학 방향으로만 물리가 성립하는데 그 사실이 무표기 — Ch1 라벨을 들고 읽으면 문서 전체 흡열/발열 판정이 반전되는 단일 최대 리스크. 1문장으로 닫히는 수정.

## 물리 불변 확인 (확정 판정 훼손 여부 — 최중점)
- **f=+σ_d: PASS.** Ch1 L1964(예고)·L2638–2651(본유도) — 진행률↔진행률 pairing 하 유일해 재유도 일치, 역부호 $f=-\sigma_d$ 는 오pairing 산물로 정확히 기술됨. 코드 주석(L630–631) 동일.
- **C-1 Δμ=+sF(V−U): PASS.** Ch1 L1244 "$\Delta\mu=+sF(V-U_j)$"($\Delta\mu\equiv\varepsilon-\mu_\mathrm{Li}$) 그대로. Ch2 eq:muV 는 $\mu=\mu^0-\sigma_dF(V-U_j)$($\sigma_d\to s{=}+1$ 각주) — $\varepsilon_0-\mu=+sF(V-U)$ 로 대수 동치, 판정 무훼손(표기 리스크만 C-10).
- **H-1 BW 부호: PASS.** eq:Veq\_BW($\theta$ 좌표) ↔ Ch1 eq:lco-Veq($\xi$ 좌표) $\theta=1-\xi$ 로 동치, spinodal·임계 $2RT$ 정합.
- 이중계산 가드(파생 B·eq:lco-slots·eq:lco-mit)·detailed-balance 계열 참조 무결. **박스식 물리 위반 0건** — 상기 HIGH 3건은 라벨/충실도 결함이지 물리식 훼손이 아님.

## Coverage 선언 (정독 줄 범위 — 빠짐 없이)
- Ch1 `graphite_ica_ch1_v1.0.13.tex`: **L1755–2897(EOF)** 연속 전문 정독(할당 L1815–말미 + 경계 맥락 L1755–1814; Part II 도입 3소절 L1803–1971·eq:lco-sigmaslot L1884–1890·이동 6절 L1972–2723·전체 입력 인자 L2725–2778·facade L2780–2814·signcheck L2817–2868·참고문헌 L2871–2896 포함). L1–1754 는 참조 확인용 spot(라벨 전수 grep + eq:sum L1756–1768·tab:staging L1770–1795 등) — 할당 범위 밖.
- Ch2 `graphite_ica_ch2_v1.0.13.tex`: **L1–779(EOF) 전문 정독**(헤더 주석·keybox 2·파생 A–D·limits·revheat·procedurebox·맺음·참고문헌 전부).
- 코드 `Anode_Fit_v1.0.13.py`: 대조 정독 L174–190(func\_dSe\_molar)·L242–290(생성자 기본값)·L352–360(컷)·L425–443(분극 앵커)·L505–610(curve·seam·entropy\_coefficient·q\_rev/q\_irr)·L612–712(방향 환산·LCO\_MSMR\_LIT·LCOCathodeDQDV·GRAPHITE\_STAGING\_LIT 머리)·L743–879(\_\_main\_\_ 전체) + 식별자 전수 grep. 코드 전문 통독은 아님(상호충실도 렌즈 필요 범위 한정).

## 5줄 요약
1. 확정 판정 3건(f=+σ_d·Δμ=+sF(V−U)·H-1) 전부 재유도로 무훼손 확인 — 박스 물리식 위반 0건, 수치 검산 20여 항 전부 통과.
2. HIGH 3건: Ch2 "방전(I>0)" 라벨이 Ch1 확정 라벨과 반대 방향으로만 성립(C-01), tab:lco-staging 캡션이 코드 루프 B 이전 상태 서술(C-02), Ch2 기호 $x$ 의 배향 이중 사용(C-03) — 셋 다 물리식이 아닌 라벨·충실도 결함이라 각 1–2문장 수정으로 닫힘.
3. MED 7건: facade 전극 인지 누락(C-04)·self-test "네 항/다섯 항" 자기모순(C-05)·"+3~4 mV/K" 내부 스케일 모순(C-06)·"부동소수점 정밀도" 과장(C-07)·전방 참조 3계열(C-08)·Motohashi $x{=}\tfrac23$ 배정 불일치(C-09)·eq:muV σ_d 표기(C-10).
4. 오적발 자기표시: C-06·C-07 은 원문헌/내부 수치 미재실행 상태의 내부-정합 논증(미검증 tier — 원자료 대조 시 뒤집힐 수 있음), C-09 는 Motohashi 원문 미확인(배정 근거가 논문에 있으면 철회), C-17 은 도식 성격상 무해 관찰.
5. 가장 약한 1곳 = C-01; 권고 우선순위 C-01→C-02→C-03→C-04/C-05(코드-문건 동기화 계열 일괄).
