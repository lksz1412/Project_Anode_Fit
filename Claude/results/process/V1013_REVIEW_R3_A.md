# V1.0.13 P5 검수 라운드 3 — 검수자 A (식·유도 단위 재유도)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L1–L801 (서론·N0 = L1–307, Part 0 `sec:sm-found` = L309–799; Part I 은 L802 `sec:pol` 시작)
- 방식: 담당 구간 전 번호식·boxed 식을 원문에 기대지 않고 독립 재유도 후 원문 대조. TikZ 4종 좌표 수치 재계산. 코드 `Anode_Fit_v1.0.13.py` 교차 대조. refute mandate 하 수행.
- 삼각 대조(범위 밖 정독): §center eq:eqcond (L879–921), §dist C-1 (L1237–1263), §signcheck S1–S8·R1–R5 (L2832–2884).

---

## 지적 사항

### A-1 [MED] L209 (연쇄: L697) — σ_d "작용처는 셋" 열거가 코드의 방향 의존을 undercount (렌즈 ①/⑥)

- **무엇이**: L209 "방향 부호의 작용처는 셋 — 분극 부호($\mathrm N1$), 분기 중심 선택($\mathrm N3$), 꼬리 지지 방향($\mathrm N8$)". 방향별 전달계수 $\chi_d$ 를 통한 **꼬리 길이(N7)** 의존이 셈에서 빠짐.
- **근거(재유도)**: 코드 `func_chi_d`(py L161–166: `chi if sigma_d >= 0 else 1-chi`)가 `_resolve_lag_length(tr, T_rep, I_abs, Q_cell, n_rep, sigma_d)`(py L488–489)로 꼬리 길이 $L_q$·$L_V$ 에 들어간다 — $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ 및 `func_L_q` 의 $-x\mathcal A/RT$ 항(py L109) 둘 다 $\chi_d$ 의존이라 $\chi\ne\tfrac12$ 이면 충·방전 꼬리 **길이**가 갈린다. 코드 자신의 docstring(py L413–414)이 "동역학 꼬리(σ_d 방향 인과기억) **· χ_d/ΔH_eff 방향 의존**"을 별도 항목으로 명기하고, 문건 자신의 기호표(L249 "방향별 전달 계수 — 방전 $\chi$/충전 $1-\chi$")·fig:spine N7 노드(L174, $\chi_d$ 를 N7 에 배치)·§signcheck S5(L2846–2847)도 이 의존을 확인한다. 즉 σ_d 의 물리 작용처는 N1·N3·**N7**·N8 넷인데 L209 는 "(N8)" 로 좁혀 명기해 N7 이 누락.
- **수정안**: "작용처는 셋 — 분극 부호(N1), 분기 중심 선택(N3), 꼬리(N7·N8 — 방향별 $\chi_d$ 가 꼬리 길이를, 격자 역전이 지지 방향을 가른다)" 로 묶거나 넷으로 재열거. (Part II 의 L1889–1890 "분극·분기·꼬리" 광의 표현과 입도 통일.)

### A-2 [MED] L678–680 (Part 0 item (i)) — 한 문장 내 겉보기 모순: "s 자리에 σ_d 를 넣은 것이 코드의 평형 점유" ↔ "σ_d 는 세 작용처로만 들어간다" (렌즈 ②/⑧)

- **무엇이**: "고정 부호 $s$ 자리에 방향 부호 $\sigma_d$, … 를 넣은 것이 코드의 평형 점유다 --- $\sigma_d$ 는 평형이 아니라 방향 라벨의 몫이라 \S\ref{sec:notation} 의 세 작용처로만 들어간다." 앞절은 σ_d 가 평형 점유 식 **안에** 있다고 말하고 뒷절은 (평형 점유가 아닌) 세 작용처로**만** 들어간다고 말한다.
- **근거(재유도)**: 코드 실상은 `ksi_eq = func_ksi_eq(T_work, V_work, center, n_j, sigma_d)`(py L484), 즉 σ_d 가 지수에 실재. 화해 고리는 $\mathrm{logistic}[-x]=1-\mathrm{logistic}[x]$ 라 σ_d 반전은 $\xi\leftrightarrow1-\xi$ **여집합 relabel** 이고 종 $\xi(1-\xi)$ 는 불변이라는 사실(N0 L210 "평형 종 자체는 방향 불변"이 이것) — 이 한 단계가 item (i)에서 압축·생략되어 문장이 자기모순처럼 읽힌다. Part 0 은 "통계역학 미수강자도 닫히도록" 을 표방(L311–313)하므로 이 생략은 대상 독자에게 실질 장애.
- **수정안**: "…를 넣은 것이 코드의 평형 점유다 — 단 지수의 $\sigma_d$ 는 $\xi\leftrightarrow1-\xi$ 여집합 relabel 일 뿐 종 $\xi(1-\xi)$ 은 불변이라(§\ref{sec:notation}), 물리 작용처로는 세지 않는다" 류 1구 삽입.

### A-3 [MED] L226 (기호표 s 행) — "boxed 식에서 $s{=}1$ 대입돼 소멸" 이 Part 0 신설(v1.0.13) 이후 거짓 (렌즈 ⑤/⑧)

- **무엇이**: s 행 마지막 구 "boxed 식에서 $s{=}1$ 대입돼 소멸".
- **근거(원문 인용)**: Part 0 의 boxed 식 셋이 $s$ 를 명시 유지 — eq:sm-eqcond(L655 "$\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$"), eq:sm-logistic(L667 "$\theta_\eq=1/(1+e^{+sF(V-U)/RT})$"), eq:sm-nernst(L782 "$V_\eq(\xi)=U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}$", 주석 "(… $s=+1$)"). 결과-사슬 박스(eq:Uj L906)에서만 실제 소멸. v1.0.10 계열 서술이 Part 0 편입으로 낡음.
- **수정안**: "본론 결과-사슬 boxed 식에서는 $s{=}1$ 대입돼 소멸(Part 0 의 박스는 $s$ 를 명시 유지 — 전 구간 $s{=}+1$ 고정)".

### A-4 [MED] L413·L416·L424·L455 — 기호 Z 충돌: canonical 분배함수로 정의된 Z 를 단일 자리 대정준 합에 재사용 (렌즈 ⑤)

- **무엇이**: L367–368 "그 규격화 합이 canonical 분배함수 $Z=\sum_ie^{-\beta E_i}$" 로 Z 를 정의한 직후, L411–414 에서 "식~\eqref{eq:sm-gc} 의 합"(= 대정준 $\Xi$ 의 단일 자리 특수화)을 $Z=1+e^{-\beta\Delta\mu}$ 로 명명. L424 는 이 Z 에 eq:sm-gc(Ξ용) 셋째 식을 적용하고, L456 은 $\Xi_M=Z^M$ 으로 두 기호를 한 식에 병치.
- **근거(재유도)**: $\sum_{n=0,1}e^{-\beta(\varepsilon-\mu)n}$ 은 µ 를 포함하므로 문건 자신의 정의 체계에서 앙상블상 $\Xi$(자리 1개)다. Ch2 의 (eq:Z1) 표기 정합 의도로 보이나(L416) 문건 내 그 사정 무주석 — "통계역학 미수강" 독자에게 방금 가른 canonical/grand canonical 구분을 도로 흐림.
- **수정안**: eq:partfn 직후 반 문장 "(자리 하나의 대정준 합 $\Xi_1$ 을 Ch2 표기에 맞춰 $Z$ 로 적는다)" 삽입, 또는 $\Xi_1$ 로 개명하고 L456 을 $\Xi_M=\Xi_1^M$ 로.

### A-5 [LOW] L291 fig:staging — stage 1 기둥이 갤러리 6개 중 5개만 채움 (렌즈 ⑦)

- **무엇이**: `\foreach \k in {1,2,3,4,5}` — 갤러리 k=6 미채움. 각 기둥은 선 7개(y=0 + 0.6k, k=1..6) = 갤러리 6개.
- **근거(재계산)**: stage 4 = {1,5}(주기 4 ✓), stage 3 = {1,4}(주기 3 ✓), stage 2L·2 = {1,3,5}(주기 2 ✓) 로 전 기둥 주기 일관인데, "완전 채움"(캡션 L296 "stage 1($\mathrm{LiC_6}$, 완전 채움)")이어야 할 stage 1 만 최상단 갤러리가 빈다.
- **수정안**: `{1,...,6}`.

### A-6 [LOW] L762–763 eq:sm-mubridge — F 이중 의미 병존 + "$RT\ll FV$" 과장 (렌즈 ⑤/①)

- **무엇이**: 한 display 안에서 $\partial F/\partial n$ 의 F(Helmholtz, L367–368 정의)와 "$P\Delta v\ll RT\ll F\,V$" 의 F(Faraday)가 병존. 기호표(L260)엔 Faraday 만 등재. 또 흑연 창 하한 $V\!\approx\!0.085$ V 에서 $FV/RT=96485\times0.085/2479\approx3.3$ 이라 "$\ll$" 은 과장 — 다리(eq:sm-mubridge)에 필요한 부등식은 $P\Delta v\ll RT$ 뿐(이는 ~10³ 배로 성립).
- **수정안**: Helmholtz F 첫 등장(L368)에 "(Faraday 상수 $F$ 와 문맥으로 구분)" 각주 1줄 + 괄호를 "$P\Delta v\ll RT,\,FV$" 로.

### A-7 [LOW] L748–750 fig:sm-occ 캡션 (a) — 괄호 오배치 (렌즈 ⑦/⑤)

- **무엇이**: "낮은 $T$ 일수록 계단($\beta\to\infty$), 높은 $T$ 일수록 완만($T\to0$ 극한이 계단 함수다)" — 계단 함수 괄호가 '높은 T·완만' 절에 붙음.
- **수정안**: 둘째 괄호를 첫 절로 이동("낮은 $T$ 일수록 계단($\beta\to\infty$ — $T\to0$ 극한이 계단 함수다)") 또는 삭제.

### A-8 [NOTE] L444 — "(둘째 식은 식~\eqref{eq:fermifn} 의 $\mu$ 미분)" gloss 정밀도

- 식 자체(L441 $\partial\theta/\partial(\beta\mu)=\theta(1-\theta)$)는 재유도 일치(✓). 다만 문자 그대로의 µ 미분은 $\partial\theta/\partial\mu=\beta\theta(1-\theta)$ 라 gloss 는 "$\beta\mu$ 미분"이 정확.

### A-9 [NOTE] L476–478 — "앙상블 동등성 = §dist 명제의 '평형 쪽 절반'" 범주 미끄러짐

- §dist 의 두 경로는 kinetic vs thermo(L1238–1239)인데, 여기 두 경로(대정준 vs 셈법)는 둘 다 thermo 내부 동등성. '평형 쪽 절반'의 정확한 담당은 Part 0 사슬 전체이고 그 서술은 item (ii)(L681–684)가 이미 정확히 한다. 실害 없는 수사적 확대 — 관찰.

### A-10 [NOTE] L540–547 eq:sm-thresh — "이중웰" 은 대칭 섞임 몫 기준의 진술

- $\Omega_j>2RT\Leftrightarrow$ 이중웰은 fig:sm-gxi 가 그리는 대칭 몫 $f(\xi)$ 기준 정확(재유도 ✓). $g_j(\xi)$ 전체에는 $g_j^0$ 의 $\xi$-직선 tilt 가 들어 tilt 크기에 따라 극소 개수가 달라질 수 있고, tilt-불변 진술은 볼록성 상실(박스 첫 줄) 쪽. 본문 L547 이 그림(섞임 몫)에 묶어 서술하므로 실害 없음 — 관찰.

### A-11 [NOTE·미검증] fig:sm-mu L602·L607 — "Ω=4RT" 라벨과 $\theta_s^-$ 마커 라벨의 수직 여백 빠듯

- 좌표 산술(scriptsize ≈0.25 cm, y=0.60 cm/단위 가정): $\theta_s^-$ above-라벨 상단 ≈ y 1.49, "Ω=4RT"(중심 1.75) 하단 ≈ 1.54 — 여백 ≈0.3 mm, 수평 구간은 겹침(θ∈0.126–0.147). 겹침 아님으로 계산되나 여유가 얇아 렌더 확인 권장. **컴파일 렌더 없이 수기 산술 — 오적발 가능성 가장 높은 항목.**

---

## 가장 약한 1곳

**σ_d 작용처 doctrine (A-1 L209 + A-2 L678–680, 한 뿌리)** — 코드 실상(σ_d 가 N1·N3·N7·N8 물리 작용 + ξ_eq 지수 relabel 로 다섯 자리 등장)과 문건의 "셋 + 평형 불변" 요약 사이의 화해 고리($\chi_d$ 꼬리 길이, 여집합 relabel)가 정확히 ★최우선 부호 결함 클래스(L216) 자리에서 생략돼 있다. 부호값 자체는 전부 옳으나, 이 구간만 문건을 "그대로 믿고 코드를 짜면" 작용처 수를 틀리게 세게 되는 유일한 지점.

## 물리 불변 확인 — **PASS**

부호 사슬 $s{=}+1$: $V\!\uparrow\Rightarrow\mu_\mathrm{Li}\!\downarrow$(eq:sm-muV $=-FV$ ✓)$\Rightarrow\theta\!\downarrow,\xi\!\uparrow$ ✓ / $\Delta\mu=+sF(V-U)$ 4중 정합(eq:sm-eqcond L655 ↔ L672–674 지수 ↔ §dist L1249 [C-1] ↔ N0 L226 s 정의) ✓ / $w=RT/F$(23.1/25.7/28.3 mV @268/298/328 K) ✓ / $\Omega\equiv-\tfrac z2N_Au$: 인력 $u<0\Rightarrow\Omega>0$ 상분리 ✓ / 문턱 $g''=RT/[\xi(1-\xi)]-2\Omega$, 최소 $4RT$ @ $\xi{=}\tfrac12$ ⇒ $\Omega\le2RT$ 볼록·등호 한 점, $T_c=\Omega/2R$ ✓ / $\mathrm{var}(n)=\theta(1-\theta)=\partial\theta/\partial(\beta\mu)$ ✓ / $U_j(T)=(-\Delta H+T\Delta S)/F$·$\partial U/\partial T=\Delta S/F$ ✓ / Nernst 로그 = 섞임 엔트로피 부분몰 몫 ✓. 계수·부호 불일치 0.

## Coverage 선언

- **정독 줄 범위**: L1–879 전량 축차 정독(담당 L1–801 전부 + 경계 맥락 L802–879). 삼각 대조 부분 정독: L879–923(eq:eqcond·eq:Uj), L1237–1311(§dist C-1·fig:logistic), L2832–2884(§signcheck). 코드: `Anode_Fit_v1.0.13.py` L75–131, 301–319, 352–360, 399–542, 609–628, 705–740.
- **재유도 식 전수(28)**: eq:sm-S·sm-fund·sm-resv·sm-taylor·sm-gibbsfactor·sm-gc(셋째 식 $\partial\ln\Xi/\partial\mu$ 포함)·partfn·sm-occmid·fermifn(극한 3종)·sm-flucres(분산·$\beta\mu$ 미분 양쪽)·sm-factor·sm-Smix(Stirling 전개)·sm-mucount(양 경로: 셈법 + fermifn 역전)·sm-muideal·sm-mf·sm-omega($\theta^2=\theta-\theta(1-\theta)$ 항등)·sm-gtheta·**mu(계수 2 확인: $\Omega(1-2\theta)$; ξ-좌표 등치 $RT\ln\frac{\xi}{1-\xi}+\Omega(1-2\xi)=sF(V-U)$ L687 재유도 일치)**·gxi($f'(1-\xi)=-f'(\xi)$ 포함)·sm-thresh(등호 위치 $\xi{=}\tfrac12$)·sm-emu·sm-workbal·sm-refbal·sm-muV(2-평형 차감·전자 몫 각주 검토)·sm-eqcond·sm-logistic($w=RT/F$·σ_d 삽입 위치=코드 L484 확인)·sm-mubridge·sm-nernst + N0 의 eq:n0map. 잔여 번호식 없음(eq:vapppol 이후는 Part I).
- **TikZ 검산**: fig:sm-gxi 8점+spinodal $\xi_s=0.2113/0.7887$ 폐형 재유도 일치 · fig:sm-mu 6점+spinodal $\theta_s=(1\pm\sqrt{1/2})/2=0.1464/0.8536$, 값 $\pm1.0657$ 일치, **R2 이동 라벨 (0.99,1.97) right: 곡선이 θ=0.98 에서 끝나 관통 없음 ✓** · fig:sm-occ (a) 3곡선 9점·(b) 4곡선 8점 일치, 범례-선종 대응 ✓ · fig:sm-reservoir 구조 ✓ · fig:staging 주기 재계산(A-5 발견) · fig:spine 노드식 8건 코드 대조 ✓.
- **R1·R2 직전 수정 재검(렌즈 ⑧)**: $g_j^0$ 문장(L527–530) — 공통접선·곡률 불변 논거 재유도 정확 ✓ / fig:sm-mu 라벨 ✓(위) / eq:sm-thresh aligned 분할 — 구문·내용 ✓ / eq:n0map 프로즈 분리(L208–210) ✓ / Q_cell 행 $ 밸런스(L228) — 5쌍 균형 ✓. 이동 편입 라벨 4종(eq:partfn/fermifn/mu/gxi) 중복 정의 0(grep 전수) ✓.
- **코드 충실도(⑥)**: func_w·func_U_j·func_ksi_eq·func_U_branch·func_chi_d·`_n_factor`($w\to n=wF/RT$ 역산 L305–306)·`_direction_to_sigma`·z_cut 4.357·A_cap_RT 4.0·GRAPHITE_STAGING_LIT 4건(U≈0.210/0.140/0.120/0.085) — 전부 문건 기술과 일치 ✓.

## 5줄 요약

1. 담당 28개 번호식 전수 독립 재유도 — 계수·부호 결함 **0**, 물리 불변 PASS; C-1($\Delta\mu=+sF(V-U)$) 4중 삼각 정합 확인.
2. MED 4건: σ_d 작용처 "셋" 이 $\chi_d$ 꼬리-길이(N7) 의존을 누락(A-1), Part 0 item (i) 한 문장 내 relabel 화해 고리 생략(A-2), s 행 "boxed 소멸" 이 Part 0 박스 3개로 반증(A-3), Z 기호 canonical/대정준 충돌(A-4).
3. LOW 3건: fig:staging stage 1 갤러리 6번 미채움(A-5), eq:sm-mubridge F 이중의미+"$RT\ll FV$" 3.3배 과장(A-6), fig:sm-occ 캡션 괄호 오배치(A-7).
4. TikZ 4종 좌표 수치 전 검산 일치(spinodal 폐형 포함), R1·R2 수정 5건 전부 유효 — 새 결함 미유발.
5. 오적발 자기표시: A-11(라벨 여백)은 렌더 미검증 수기 산술로 가장 불확실, A-10 은 본문이 이미 그림 기준으로 방어된 관찰, A-4 는 Ch2 표기 정합의 의도 가능성(다만 문건 내 무주석은 사실).
