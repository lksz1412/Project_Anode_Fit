# A06_REVIEW — v1.0.22 심층 검토 FR-A06 (§5 폭 절 ch1_sec05_width.tex)

- 대상: `Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex` (전문 정독, 411행 — §5.1 logistic 유도 + TST bgbox + Bazant srcbox + §5.2 폭 이중지위 + §5.3 분포 관점 + 그림 3종)
- 검토 창: FR-A06 (보고 전용 — 본문 무수정·git 무조작·`Codex/` 무접근). 4관점(보완/논리/설명/수식화) 전부 적용.
- 검증 방법: 참조 라벨 전수 역추적(sec01·02a·02b·03·04·06·07·08·10·11·15 + ch2 sec01·05·08 원문 대조) · 전 수식 재유도/전 수치 재계산(§검증 로그) · 서지는 bib·V1 원장 대조 + 하이쿠 서브에이전트 Crossref 왕복 검증(§서치).
- 상태: **본판 (서치 절 통합 완료)**.

---

## 0. 발견 색인 (등급순)

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A06-H1 | ch1_sec05_width.tex:111–113 (+97, 113–114 연동) | 논리 | H | TST verifybox (ii) 고온 극한 검산 자체가 불성립 — 표준 모드 부기(q_R=반응물 전 모드)에서 $q^{\ddagger}/q_R\propto1/T\to0$ 이라 "진동수 비의 고전값으로 수렴·$\Delta S_a$ 유한"이 성립하지 않음. 유한 수렴하는 것은 전치인자 $(k_BT/h)(q^{\ddagger}/q_R)\to\prod\nu^R/\prod\nu^{\ddagger}$(고전 시도빈도). (d)의 "반응물의 (반응좌표를 뺀) reduced" 서술이 같은 부기 혼선의 뿌리 |
| A06-M1 | ch1_sec05_width.tex:101–104 | 논리(정밀)/보완 | M | Part 0 접속 — "같은 연산 $k_B\partial(T\ln q)/\partial T$ 을 비에 건다"는 서술과 박스 식별 $\Delta S_a=R\ln(q^{\ddagger}/q_R)$ 는 $RT\,\partial_T\ln(\cdot)$ 만큼 다른 두 정의. "잔여 $T$-의존은 $\Delta H_a$ 쪽" 가드의 성립 조건(Gibbs–Helmholtz 읽기) 미명시 |
| A06-M2 | ch1_sec05_width.tex:199, 207–208 | 보완/설명 | M | fig:barrier 캡션·패널(b) 주석의 $\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$·$L_q$ — §8(sec:lag) 결과의 선행 사용에 포인터 부재 + 그림이 그린 기작($\mathcal A$ 기울임)과 별개 기작($\Omega$ 흡수)임을 미구분 |
| A06-M3 | ch1_sec05_width.tex:299–301 | 보완 | M | $(1-\Omega_j/2RT)$ 유효 폭 문장 — 수학은 정확(재유도 일치)하나 Part T 파생 C warnbox 가 "재도입 금지"로 명명한 $w_\eff(\Omega)$ 류와 동일 인자라 외견 충돌. "해석적 성질 서술 ≠ 모델 폭 항" 가드 half-clause 필요 |
| A06-M4 | ch1_sec05_width.tex:28–30 | 설명 | M | "정방향이 찬 자리($1-\xi$)에서" — 정/역방향의 물리 실명(탈리튬화/리튬화)과 $\xi$=빈 자리 분율 명시가 없어 부호 사슬의 관문 문장이 압축됨 |
| A06-M5 | ch1_sec05_width.tex:30 | 수식화 | M | 운동방정식 $\dd\xi/\dd t=r^+(1-\xi)-r^-\xi=k_j(\xi_\eq-\xi)$ 가 무번호 인라인 — §8 이 "\S\ref{sec:width} 의 운동방정식"으로 절 단위 참조 중. 번호식 승격(eq:relax 제안) |
| A06-M6 | ch1_sec05_width.tex:311–313 | 설명 | M | "같은 지위의 초기값" — 문단 주제어 "지위"(폭의 이중지위)와 동음 충돌로 "둘째(두-상) 지위와 같은 지위"로 오독 가능. 재서술안 |
| A06-M7 | ch1_sec05_width.tex:296–305 | 수식화 | M | ★이중지위 문단(산문 전개) — 2행 소표 보강으로 기계적 대조 가능(문단 대체 아님·보강) |
| A06-M8 | ch1_sec05_width.tex:15–16 | 보완 | M | $\mathcal A_j=sF(V_n-U_j)$ 가 이상 몫 한정( $r^\pm$ 이 $\xi$-무관 상수가 되는 전제)임이 §5.1 시점에 미명시 — 독자 질문("상호작용 $\Omega$ 는?")의 선제 half-clause |
| A06-L1 | ch1_sec05_width.tex:113–115 | 문체 | L | verifybox (iii) "순수 Arrhenius 형" — 전치인자 $k_BT/h$ 의 $T$-선형 의존이 남으므로 표현 정밀화 |
| A06-L2 | ch1_sec05_width.tex:366–367 | 문체 | L | fig:logistic 캡션 "$\dd\xi_\eq/\dd V=\xi_\eq(1-\xi_\eq)/w$(식 eq:belliden)" — eq:belliden 은 $z$-미분 항등식·$V$-미분엔 $\sigma_d/w$ 연쇄율. $\sigma_d{=}+1$/절댓값 명시 |
| A06-L3 | ch1_sec05_width.tex:404–408 | 문체 | L | keybox "같은 통계로 닫혀" — Part 0 eq:fermifn 검산 박스의 ★함수형 가드(동형이되 배타 근거는 기하 vs Pauli)와 표현 정렬 |
| A06-L4 | ch1_sec05_width.tex:204–206 | 문체 | L | fig:barrier "정점을 $\chi\mathcal A{=}0.25$ 낮추면" — 기울임에 의한 안장점 위치 이동 보정 $O(\mathcal A^2)$(수치 0.007) 각주 여지 |
| A06-L5 | ch1_sec05_width.tex:385–390 | 수식화/문체 | L | §dist (c) 몰 환산 사슬의 한 줄 displayed 수식화 + 국소 "$w_j\equiv RT/F$" 재정의가 eq:wbase 의 $w_j=n_jRT/F$ 와 기호 충돌(첨자 없는 $w$ 제안) |

집계: **H 1건 · M 8건 · L 5건**.

---

## 1. H 등급 (논리/물리 오류)

### A06-H1 — TST verifybox (ii) 고온 극한 검산 불성립 (+모드 부기 혼선)

- 파일:행 = `ch1_sec05_width.tex:111–113` (연동: 97행 (d) 첫 문장, 113–114행 (iii) 첫 구) · 유형 = 논리 · 등급 = **H**

현행(축자 — verifybox (ii)):
```latex
(ii) 고온 극한: 진동 모드의
$q\to k_BT/\hbar\omega$ 라 $q^{\ddagger}/q_R$ 가 진동수(곡률) 비의 고전값으로 수렴, $\Delta S_a\to
R\ln(\text{고전 비})$ 로 유한하다.
```
현행(축자 — 연동 (d) 첫 문장, 97행):
```latex
활성화 엔트로피는 활성복합체와 반응물의 (반응좌표를 뺀) reduced 분배함수 비의 로그다
```

근거(재유도 — 두 부기 어느 쪽으로도 현행이 닫히지 않음):
1. **본문 자신의 정의로는 $q_R$ = 반응물 전 모드다.** (b) "반응좌표 모드를 뗀 활성복합체 분배함수를 $q^{\ddagger}$, 반응물의 것을 $q_R$", (c) 인구비 논증과 식 eq:tst-rate $k=(k_BT/h)(q^{\ddagger}/q_R)e^{-\Delta E_0/RT}$ 는 표준 Eyring 형 — 이 형이 옳으려면 $q_R$ 는 반응물의 **전(全)** 분배함수여야 한다(반응좌표 모드는 복합체 쪽에서만 떼어 $k_BT/h$ 로 이미 흡수됨).
2. 그러면 반응물은 $N$ 개, 복합체(뗀 뒤)는 $N-1$ 개 진동 모드다. 고전 극한 $q_\mathrm{vib}\to k_BT/\hbar\omega$ 를 넣으면
   $\dfrac{q^{\ddagger}}{q_R}\to\dfrac{(k_BT/\hbar)^{N-1}\big/\prod_{i=1}^{N-1}\omega_i^{\ddagger}}{(k_BT/\hbar)^{N}\big/\prod_{i=1}^{N}\omega_i^{R}}=\dfrac{\hbar}{k_BT}\cdot\dfrac{\prod_{i=1}^{N}\omega_i^{R}}{\prod_{i=1}^{N-1}\omega_i^{\ddagger}}\;\propto\;\frac1T\;\to\;0$,
   곧 비는 유한 상수로 **수렴하지 않고** $1/T$ 로 소멸하며, $\Delta S_a=R\ln(q^{\ddagger}/q_R)$ 는 $-R\ln T$ 로 **발산**(느린 로그)한다. "진동수(곡률) 비의 고전값으로 수렴·유한"은 성립하지 않는다.
3. 유한·$T$-무관으로 수렴하는 것은 **$k_BT/h$ 와 묶인 전치인자**다:
   $(k_BT/h)\,(q^{\ddagger}/q_R)\to\prod_{i=1}^{N}\nu_i^{R}\big/\prod_{i=1}^{N-1}\nu_i^{\ddagger}$ — 고전 조화 고체의 시도빈도(Vineyard 형; §서치 후보 표). 이것이 "실제 Arrhenius 전치인자가 $k_BT/h$ 자체가 아니라 $\sim10^{12\text{--}13}$/s 의 시도빈도인 까닭"이라 본문 (b) 의 $k_0$ 이야기와도 자연 접속된다.
4. 현행 (ii) 가 성립하는 유일한 읽기는 "반응물 쪽도 반응좌표 대응 모드를 뗀 **동수 모드 비교**"(97행 (d) 의 "(반응좌표를 뺀) reduced ... 비" 표기, 113행 (iii) "자유도가 변치 않아 $q^{\ddagger}=q_R$" 도 이 읽기에서 자연스러움)다. 그러나 그 부기에서는 식 eq:tst-rate 가 반응물 반응좌표-모드 인자(고전 $k_BT/h\nu_R$)를 잃어 표준 Eyring 식이 아니게 된다 — 곧 **박스 본문(전-모드 부기)과 verifybox(동수-모드 부기)가 서로 다른 부기를 쓰는 내부 불일치**다.

제안(완성 LaTeX — (ii) 대체):
```latex
(ii) 고온 극한: 진동 모드의
$q\to k_BT/\hbar\omega$ 라 Eyring 전치인자가
$(k_BT/h)\,(q^{\ddagger}/q_R)\to\prod_{i=1}^{N}\nu_i^{R}\big/\prod_{i=1}^{N-1}\nu_i^{\ddagger}$
--- 온도$\cdot$유효질량에 무관한 \emph{고전 시도빈도}(진동수$\cdot$곡률 비) --- 로 유한 수렴한다
($q_R$ 는 반응물 전 모드$\cdot$$q^{\ddagger}$ 는 반응좌표를 뺀 모드라 비 자체는 $\propto1/T$;
유한 수렴의 주체는 비가 아니라 $k_BT/h$ 와 묶인 전치인자다).
```
제안(완성 LaTeX — 97행 (d) 첫 문장 대체):
```latex
활성화 엔트로피는 (반응좌표를 뗀) 활성복합체 분배함수 $q^{\ddagger}$ 와 반응물 분배함수 $q_R$ 의 비의 로그다
```
(선택 — (iii) 첫 구 "활성화로 자유도가 변치 않아" 는 "활성화가 (반응좌표를 뺀 비교에서) 자유도를 조이지도 풀지도 않아 $q^{\ddagger}/q_R=1$ 이면" 으로 함께 정렬하면 부기 혼선이 완전히 걷힌다 — A06-L1 과 같은 자리.)

---

## 2. M 등급 (의미·이해 실질 개선)

### A06-M1 — eq:tst-box 식별 vs Part 0 접속 "같은 연산"의 정합 조건 미명시

- 파일:행 = `ch1_sec05_width.tex:101–104` · 유형 = 논리(정밀)/보완 · 등급 = M

현행(축자):
```latex
\textbf{Part 0 접속.} 이 ``로그-분배함수 $=$ 엔트로피'' 대응은 Part 0 의 내부 자유도 언어와 같다 --- Part 0 은
단일 자리 내부 분배함수 $q(T)$(식~\eqref{eq:partfn})에 연산 $s_\mathrm{int}=k_B\,\partial(T\ln q)/\partial T$
(식~\eqref{eq:sm-sint})를 걸어 자리 엔트로피를 읽었고, 여기서는 같은 연산을 활성화의 비 $q^{\ddagger}/q_R$ 에
걸어 활성화 엔트로피를 읽는다(비의 잔여 $T$-의존은 $\Delta H_a$ 쪽으로 넘기는 표준 읽기).
```

근거(재계산): "같은 연산"을 비에 걸면 $R\,\partial[T\ln(q^{\ddagger}/q_R)]/\partial T=R\ln(q^{\ddagger}/q_R)+RT\,\partial_T\ln(q^{\ddagger}/q_R)$ — 박스 값 $R\ln(q^{\ddagger}/q_R)$ 와 둘째 항만큼 다르다. 두 읽기의 정리: (i) **식별 읽기**(박스): $\Delta S_a\equiv R\ln(q^{\ddagger}/q_R)$ 로 두면 eq:tst-dG 에서 $\Delta H_a=\Delta E_0$ 이 **정확**해 "$\Delta H_a$ 쪽으로 넘길" 잔여가 없다(잔여 $T$-의존은 $\Delta S_a(T)$ 의 인자 안에 그대로 남는다). (ii) **Gibbs–Helmholtz 읽기**: $\Delta S_a=-\partial\Delta G_a/\partial T=R\ln(\cdot)+RT\,\partial_T\ln(\cdot)$, $\Delta H_a=\Delta E_0+RT^2\,\partial_T\ln(\cdot)$ — 미분 몫이 $\Delta H_a$ 에 나타나는 것은 **이쪽** 읽기다. 현행 괄호는 (ii) 의 서술을 (i) 의 박스에 붙여 두 정의를 섞는다. 비가 $T$-무관이면 두 읽기가 일치하므로, 그 정합 조건을 명시하면 닫힌다.

제안(완성 LaTeX — 괄호부 대체):
```latex
(같은 연산을 그대로 걸면 $R\ln(q^{\ddagger}/q_R)+RT\,\partial_T\ln(q^{\ddagger}/q_R)$ 라, 박스~\eqref{eq:tst-box} 의
식별 $\Delta S_a=R\ln(q^{\ddagger}/q_R)$ 는 비가 $T$-무관일 때 그와 일치한다; 비가 $T$-의존이면
Gibbs--Helmholtz 읽기에서 미분 몫 $RT^2\,\partial_T\ln(q^{\ddagger}/q_R)$ 가 $\Delta H_a=\Delta E_0+RT^2\,\partial_T\ln(q^{\ddagger}/q_R)$
쪽에 나타나며, Eyring 플롯이 상수 $(\Delta H_a,\Delta S_a)$ 로 피팅하는 표준 읽기가 그 잔여를 흡수한다)
```

### A06-M2 — fig:barrier 의 $\Delta H_a^\eff$·$L_q$ 선행 사용 — §8 포인터·기작 구분

- 파일:행 = `ch1_sec05_width.tex:199, 207–208` · 유형 = 보완/설명 · 등급 = M

현행(축자 — 패널(b) 주석 node, 199행):
```latex
\node[font=\scriptsize,anchor=south west] at (-0.2,-0.48) {$\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$};
```
현행(축자 — 캡션 말미, 207–208행):
```latex
$\chi\!\cdot\!(1{-}\chi)$ 분할이 detailed balance(식~\eqref{eq:db})를 강제하고, 유효 장벽은 $\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$
다. 이 그림이 logistic(식~\eqref{eq:xieq})과 $L_q$ 의 공통 출발점이다.}
```

근거: $\chi_d$(식 eq:chid)·$\Delta H_a^\eff$(식 eq:dHeff)·$L_q$(식 eq:Lq)는 전부 §8(sec:lag) 결과다(§1 표기표 선언만 선행). 그림이 실제로 그린 것은 이상 구동력 $\mathcal A$ 의 $\chi:(1-\chi)$ 기울임이고, $\Delta H_a^\eff$ 는 **구동력의 상호작용 상수 몫 $\Omega$ 를 장벽으로 흡수**한 별개 단계(§8 (d))다 — 포인터 없는 단언이라 §5 독자가 "이 그림 어디서 $\Omega$ 가 나왔나"를 물을 자리다. 대응 표기는 부록 A S5 행과 정합(오귀속은 아님).

제안(완성 LaTeX — node 대체):
```latex
\node[font=\scriptsize,anchor=south west] at (-0.2,-0.48) {$\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$ (\S\ref{sec:lag})};
```
제안(완성 LaTeX — 캡션 말미 대체):
```latex
$\chi\!\cdot\!(1{-}\chi)$ 분할이 detailed balance(식~\eqref{eq:db})를 강제하고, 구동력의 상호작용 상수 몫을
장벽으로 흡수하면 유효 장벽 $\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$ 가 된다(\S\ref{sec:lag}
식~\eqref{eq:dHeff} --- 이 그림의 기울임은 이상 몫 $\mathcal A$ 만; 기본값 $\chi{=}0.5$).
이 그림이 logistic(식~\eqref{eq:xieq})과 \S\ref{sec:lag} 지연 길이 $L_q$ 의 공통 출발점이다.}
```

### A06-M3 — $(1-\Omega_j/2RT)$ 유효 폭 문장과 Part T "재도입 금지" warnbox 의 외견 충돌

- 파일:행 = `ch1_sec05_width.tex:299–301` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
엄밀히 이 닫힌 폭은 이상 극한($\Omega_j=0$) 기준이고,
$0<\Omega_j<2RT$ 에서는 평형 등온선의 중심 기울기가 $(1-\Omega_j/2RT)$ 배 좁아진 유효 폭을 주되 그
값 역시 평형이 결정하므로 첫째 지위(평형 예측)라는 성격은 변하지 않는다(Part T 파생 C(\S\ref{ssec:weff})와 동일 취지).
```

근거(재유도 + 원문 대조): 수학은 정확 — eq:Veq 미분으로 $sF\,\dd V_\eq/\dd\xi|_{1/2}=4RT-2\Omega_j$, 곧 중심 기울기 정의 폭 $w_\eff=w\,(1-\Omega_j/2RT)$ (재유도 일치·단상에서만 양수). 그러나 Part T 파생 C warnbox(`ch2_sec05_mixing.tex:187–193`)는 "본 장은 그런 유효-폭 축소식($w_\eff(\Omega)=w(1-\Omega/2RT)$ 류)을 쓰지 않는다(재도입 금지)" 를 명시하고 자산 [C-2] 가 "구 $w_\eff(\Omega)$ narrowing 식 완전 제거(재도입 금지)" 를 기록한다 — 금지 표적은 **두-상 폭의 모델 항**이고 §5 는 **단상 등온선의 해석적 성질** 서술이라 실충돌은 아니나, 금지된 것과 같은 인자가 문언으로 재등장해 두 문서를 다 읽는 독자가 저촉 여부를 물을 자리다. §5 자신의 "폭은 항상 이 한 식(eq:wbase)" 선언(272–273행)과의 관계를 그 자리에서 명시하면 닫힌다.

제안(완성 LaTeX — 말미 괄호 확장 대체):
```latex
엄밀히 이 닫힌 폭은 이상 극한($\Omega_j=0$) 기준이고,
$0<\Omega_j<2RT$ 에서는 평형 등온선의 중심 기울기가 $(1-\Omega_j/2RT)$ 배 좁아진 유효 폭을 주되 그
값 역시 평형이 결정하므로 첫째 지위(평형 예측)라는 성격은 변하지 않는다(단상 등온선의 \emph{해석적 성질}
서술이다 --- 모델 폭 항은 여전히 식~\eqref{eq:wbase} 하나이고, 두-상 폭을 이 인자로 좁히는 유효-폭
축소식을 쓰지 않는다는 Part T 파생 C(\S\ref{ssec:weff}) warnbox 의 금지와 무모순$\cdot$동일 취지).
```

### A06-M4 — 정·역방향의 물리 실명과 $\xi$=빈 자리 분율 명시

- 파일:행 = `ch1_sec05_width.tex:28–30` · 유형 = 설명 · 등급 = M

현행(축자):
```latex
운동
방정식은 정방향이 찬 자리($1-\xi$)에서, 역방향이 빈 자리($\xi$)에서 출발하므로
$\dd\xi/\dd t=r^+(1-\xi)-r^-\xi=k_j(\xi_\eq-\xi)$($k_j\equiv r^++r^-$).
```

근거: 이 문장이 §5 부호 사슬 전체의 관문인데(이후 §dist 의 $\xi=1-\theta$ 여집합 명제·signbox·eq:xieq 가 전부 여기 걸림), "정방향"의 물리(탈리튬화 — $s{=}+1$ 유도 기준)와 "$\xi$ 가 빈 자리 분율"이라는 두 사실이 괄호 속 암시로만 있다. 독자가 $\xi$ 를 관례적 점유율 $\theta$ 로 순간 오독하면 $r^+(1-\xi)$ 의 부호 구조가 뒤집혀 보인다.

제안(완성 LaTeX):
```latex
운동
방정식은 정방향(탈리튬화 --- 자리를 비우는 쪽)이 찬 자리 분율 $1-\xi$ 에서, 역방향(리튬화)이 빈 자리 분율
$\xi$ 에서 출발하므로 --- 진행률 $\xi$ 는 곧 빈 자리 분율이다(\S\ref{sec:dist} 의 $\xi=1-\theta$) ---
$\dd\xi/\dd t=r^+(1-\xi)-r^-\xi=k_j(\xi_\eq-\xi)$($k_j\equiv r^++r^-$).
```

### A06-M5 — 운동방정식의 번호식 승격 (eq:relax 제안)

- 파일:행 = `ch1_sec05_width.tex:30` · 유형 = 수식화 · 등급 = M

현행(축자): A06-M4 와 동일 행 — 인라인 `$\dd\xi/\dd t=r^+(1-\xi)-r^-\xi=k_j(\xi_\eq-\xi)$($k_j\equiv r^++r^-$)`.

근거: §8 이 이 식을 절 단위로 참조한다(`ch1_sec08_lag.tex:10` — "\S\ref{sec:width} 의 운동방정식 $\dd\xi_j/\dd t=k_j(\xi_{\eq,j}-\xi_j)$"), §9 의 결핍 변수 $r_j=\xi_{\eq,j}-\xi_j$ 도 같은 구조를 쓴다. N7 사슬의 출발식이 무번호 인라인인 것은 참조 정밀도 손실 — 번호식으로 승격하면 §8 (a) 를 "식~\eqref{eq:relax}" 로 잇는다(마스터 재량의 후속 1치환).

제안(완성 LaTeX — 인라인을 다음으로 대체; 신규 라벨은 제안 표기):
```latex
\begin{equation}
\frac{\dd\xi_j}{\dd t}=r_j^+(1-\xi_j)-r_j^-\,\xi_j=k_j\,(\xi_{\eq,j}-\xi_j),
\qquad k_j\equiv r_j^++r_j^-
\label{eq:relax}
\end{equation}
```

### A06-M6 — "같은 지위의 초기값" 동음 충돌 재서술

- 파일:행 = `ch1_sec05_width.tex:311–313` · 유형 = 설명 · 등급 = M

현행(축자):
```latex
폭 쪽으로는, 네 전이의 폭 출발값(0.020/0.016/0.014/0.012 V)이
같은 지위의 초기값이고($w$ 폴백 --- $n_j$ 입력을
배제해야 활성화되며 현재 출발은 $n_j{=}1$: \S\ref{sec:broadening} ②), 단상의 $w$ 는 평형이
정하고 두-상의 $w$ 는 피팅이 정한다.
```

근거: 이 문단의 주제어 "지위"는 폭의 **이중지위**(평형 예측 vs 현상학 폭)다. "같은 지위의 초기값"의 의도는 "표의 $\Omega_j$ 와 같은 자격 — 피팅이 override 하는 거친 초기값"이지만, 직전 문장들 뒤에서는 "둘째(두-상) 지위와 같은 지위"로 오독될 수 있다(폭 폴백 규정 자체는 sec10:45–48·§7 ② 와 정합 — 값 대조 완료).

제안(완성 LaTeX):
```latex
폭 쪽으로는, 네 전이의 폭 출발값(0.020/0.016/0.014/0.012 V)도 위 $\Omega_j$ 와 같은 자격 --- 피팅이
override 하는 거친 초기값 --- 이고($w$ 폴백 --- $n_j$ 입력을
배제해야 활성화되며 현재 출발은 $n_j{=}1$: \S\ref{sec:broadening} ②), 단상의 $w$ 는 평형이
정하고 두-상의 $w$ 는 피팅이 정한다.
```

### A06-M7 — ★이중지위 문단의 소표 보강 (대체 아님)

- 파일:행 = `ch1_sec05_width.tex:296–305` · 유형 = 수식화 · 등급 = M

현행(축자 — 문단 도입부; 문단 전체가 대상이며 산문 유지 전제):
```latex
\textbf{★폭 $w_j$ 의 이중지위 --- 같은 식, 다른 지위.} 식~\eqref{eq:wbase} 의 \emph{값}은 한 줄이지만, 그것이
\emph{무엇을 뜻하는지}는 전이의 상분리 여부로 갈린다.
```

근거: 이 절의 핵심 자산이 10행 산문으로만 전개된다. 갈림 기준($\Omega_j$)·평형이 예측하는 것·$w_j$ 지위·폭 결정자의 4열 대조는 표가 기계적으로 명확하며, §7·Part T 파생 C 와의 대응 확인도 빨라진다. 문단 뒤에 보강 삽입(산문 삭제 없음).

제안(완성 LaTeX — 문단 직후 삽입):
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}llll@{}}
\hline
전이 부류 & 평형이 예측하는 것 & $w_j$ 의 지위 & 폭을 정하는 것 \\
\hline
단상 $\Omega_j\le2RT$ & 유한 폭 등온선(중심 기울기 폭 $n_j\frac{RT}{F}(1-\frac{\Omega_j}{2RT})$) & 검증 가능한 평형 예측 & 평형(식~\eqref{eq:wbase}) \\
두-상 $\Omega_j>2RT$ & 날카로운 선(델타$\cdot$plateau) & 현상학적 자유 피팅 폭 & broadening(\S\ref{sec:broadening} ①②③) \\
\hline
\end{tabular}
\end{center}
```

### A06-M8 — §5.1 구동력의 이상 몫 한정 half-clause

- 파일:행 = `ch1_sec05_width.tex:15–16` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
구동력 $\mathcal A_j=sF(V_n-U_j)$ 가 정$\cdot$역 장벽을
비대칭 이동시켜(분율 위치 $\chi$ --- 비평형 열역학 기반 전하전달 동역학의 표준 분해\cite{bazant2013}), 자리당 정$\cdot$역 속도가
```

근거: 식 eq:bv 의 $r_j^\pm$ 이 $\xi$-무관 상수(그래서 정지점이 **닫힌** logistic)가 되는 것은 $\mathcal A_j$ 를 이상 몫 $sF(V_n-U_j)$ 로 한정한 결과다. 상호작용 몫 $-\Omega_j(1-2\xi_j)$ 를 얹는 일반화는 §8(eq:dHeff 유도부)과 §dist (d) 가 하지만, §5.1 시점에는 그 한정이 선언되지 않아 "격자기체 상호작용은 어디 갔나"라는 독자 질문이 남는다(§5.2 의 "이상 극한 기준" 명시는 폭 값에 대해서만).

제안(완성 LaTeX):
```latex
구동력 $\mathcal A_j=sF(V_n-U_j)$ --- 이상 몫만이다: 자리 상호작용 $\Omega_j$ 의 구동력 몫은
\S\ref{sec:lag}$\cdot$\S\ref{sec:dist}(d) 가 얹고, 그 덕에 $r_j^\pm$ 은 $\xi$-무관 상수다 --- 가 정$\cdot$역 장벽을
비대칭 이동시켜(분율 위치 $\chi$ --- 비평형 열역학 기반 전하전달 동역학의 표준 분해\cite{bazant2013}), 자리당 정$\cdot$역 속도가
```

---

## 3. L 등급 (문체·정밀)

### A06-L1 — verifybox (iii) "순수 Arrhenius 형"

- 파일:행 = `ch1_sec05_width.tex:113–115` · 유형 = 문체 · 등급 = L

현행(축자):
```latex
(iii) 원형 회수: 활성화로 자유도가 변치 않아 $q^{\ddagger}=q_R$ 이면
$\Delta S_a=0$ 이라 식~\eqref{eq:tst-box} 가 $k=(k_BT/h)e^{-\Delta H_a/RT}$ 의 순수 Arrhenius 형으로 환원된다
--- \S\ref{sec:sum} 의 기본값 $\Delta S_a{=}0$ 이 이 극한이다.
```

제안(완성 LaTeX):
```latex
(iii) 원형 회수: 활성화로 자유도가 변치 않아 $q^{\ddagger}=q_R$ 이면
$\Delta S_a=0$ 이라 식~\eqref{eq:tst-box} 가 $k=(k_BT/h)e^{-\Delta H_a/RT}$ --- $\Delta S_a{=}0$ 의 Eyring 형
(전치인자의 $T$-선형 의존만 남는 Arrhenius 꼴) --- 으로 환원된다
--- \S\ref{sec:sum} 의 기본값 $\Delta S_a{=}0$ 이 이 극한이다.
```

근거: $k_BT/h$ 는 $T$-선형이라 "순수 Arrhenius"(T-무관 전치인자)와 다르다. Eyring 플롯($\ln(k/T)$ vs $1/T$)에선 직선인 형이므로 표현만 정밀화. (A06-H1 채택 시 "자유도가 변치 않아" 구도 함께 정렬 — H1 말미 선택안 참조.)

### A06-L2 — fig:logistic 캡션의 eq:belliden 귀속 표기

- 파일:행 = `ch1_sec05_width.tex:366–367` · 유형 = 문체 · 등급 = L

현행(축자):
```latex
수치 평가). 오른축 종(bell)이 $\dd\xi_\eq/\dd V=\xi_\eq(1-\xi_\eq)/w$(식~\eqref{eq:belliden})로 세 온도
```

제안(완성 LaTeX):
```latex
수치 평가). 오른축 종(bell)이 $|\dd\xi_\eq/\dd V|=\xi_\eq(1-\xi_\eq)/w$(식~\eqref{eq:belliden} 의
$z$-항등식에 연쇄율 $\sigma_d/w$ 를 곱한 꼴 --- 그림은 $\sigma_d{=}+1$)로 세 온도
```

근거(원문 대조): eq:belliden(`ch1_sec06_eqpeak.tex:13–18`)은 $\dd\xi_\eq/\dd z=\xi_\eq(1-\xi_\eq)$ 의 $z$-미분 항등식이고 $V$-미분은 $\sigma_d\,\xi(1-\xi)/w_j$(§6 (c))다. 캡션 말미 "종은 방향 불변(양수)" 문장과도 절댓값 표기가 정합.

### A06-L3 — keybox "같은 통계로 닫혀" 의 가드 정렬

- 파일:행 = `ch1_sec05_width.tex:404–408` · 유형 = 문체 · 등급 = L

현행(축자):
```latex
\textbf{분포 다리.} $\xi_\eq$ 가 평형 점유 확률 분포(식~\eqref{eq:fermifn})라는 것이 \S\ref{sec:lco-electronic}
의 LCO \emph{전자} 엔트로피(전도 전자 Fermi--Dirac 분포 $f(E)=1/(1+e^{\beta(E-E_F)})$)와 \emph{동형}이다 ---
흑연의 \emph{리튬 자리} 점유와 LCO 의 \emph{전자 준위} 점유가 같은 통계로 닫혀, 이 다리가 LCO 전자 엔트로피
절을 흑연 forward 틀 안으로 끌어들인다.
```

제안(완성 LaTeX — 셋째 행 대체):
```latex
흑연의 \emph{리튬 자리} 점유와 LCO 의 \emph{전자 준위} 점유가 같은 두-상태 배타 점유 통계로 닫혀(동형일 뿐
배타의 근거는 기하 vs Pauli 로 다르다 --- 식~\eqref{eq:fermifn} 검산 박스의 ★함수형 가드), 이 다리가 LCO 전자 엔트로피
절을 흑연 forward 틀 안으로 끌어들인다.
```

근거: Part 0 eq:fermifn verifybox(★함수형 가드)가 "공유하는 것은 배타 점유의 대수 구조뿐"이라 못박았는데, 여기 "같은 통계"가 양자 통계 동일로 읽힐 여지가 있다. 가드 한 줄 재인용으로 정렬.

### A06-L4 — fig:barrier 정점 강하의 $O(\mathcal A^2)$ 각주

- 파일:행 = `ch1_sec05_width.tex:204–206` · 유형 = 문체 · 등급 = L

현행(축자):
```latex
(a) 평형($\mathcal A{=}0$) --- 두 골 같은 높이, 장벽 $\Delta G_a{=}0.90$. (b) 구동력 $\mathcal A_j{=}sF(V_n{-}U_j){>}0$
($\chi{=}\tfrac12$)가 도착 골을 $\mathcal A{=}0.50$ 내려 정점을 $\chi\mathcal A{=}0.25$ 낮추면, 정방향 장벽
$\Delta G_a{-}\chi\mathcal A{=}0.65$ 로 하강$\cdot$역방향 $\Delta G_a{+}(1{-}\chi)\mathcal A{=}1.15$ 로 상승(점선 $=$(a)).
```

제안(완성 LaTeX — 둘째 문장에 괄호 추가):
```latex
($\chi{=}\tfrac12$)가 도착 골을 $\mathcal A{=}0.50$ 내려 정점을 $\chi\mathcal A{=}0.25$ 낮추면(기울임에 따른
안장점 \emph{위치} 이동의 보정은 $O(\mathcal A^2)$ --- 표준 선형화), 정방향 장벽
```

근거(재계산): 기울인 곡선 $G_\mathrm{base}-\mathcal A\phi$ 의 실제 최대는 $x\approx2.887$ 에서 $0.7571$ — $x{=}3$ 값 $0.75$ 와의 차 $0.007=\mathcal A^2\phi'^2/(2|G''|)=0.25\times0.0625/(2\times1.110)$ 로 정확히 2차 보정. eq:bv 는 $\chi\mathcal A$ 이동을 **정의**로 쓰므로 물리 오류는 아니며, 정밀 독자용 반 괄호면 족하다.

### A06-L5 — §dist (c) 몰 환산 사슬의 displayed 한 줄 + 국소 $w_j$ 재정의 충돌

- 파일:행 = `ch1_sec05_width.tex:385–390` · 유형 = 수식화/문체 · 등급 = L

현행(축자):
```latex
전기화학 구동력이 자리 점유 비용을 정한다 --- 전이 중심 기준(자리 자유에너지의 몰 환산 $N_A\tilde\varepsilon=\mu^0$)과
식~\eqref{eq:eqcond} 의 $\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 를 정의에 넣으면 1몰 기준으로
$\Delta\mu=+sF(V-U_j)$, 곧 지수는 몰당 형태로
$\Delta\mu/(RT)=+s(V-U_j)/w_j$($w_j\equiv RT/F$, 이상 극한)다($\beta$ 의 자리당 $k_BT$ 가 몰당 $RT$ 로,
자리당 전하 $e$ 가 몰당 $F$ 로 한꺼번에 환산 --- 비는 불변).
```

제안(완성 LaTeX — 산문 유지 + 사슬을 한 줄 수식으로; "$w_j\equiv RT/F$" 국소 재정의는 첨자 없는 $w$ 로):
```latex
전기화학 구동력이 자리 점유 비용을 정한다 --- 전이 중심 기준(자리 자유에너지의 몰 환산 $N_A\tilde\varepsilon=\mu^0$)과
식~\eqref{eq:eqcond} 의 $\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 를 정의에 넣으면 1몰 기준으로
\[
N_A\Delta\mu=\mu^0-\big[\mu^0-sF(V-U_j)\big]=+sF(V-U_j)
\quad\Longrightarrow\quad
\frac{\Delta\mu}{k_BT}=\frac{s(V-U_j)}{w}\qquad(w\equiv RT/F\text{ --- 이상 극한}\cdot n_j{=}1;\ \text{일반 폭은 식~\eqref{eq:wbase}})
\]
($\beta$ 의 자리당 $k_BT$ 가 몰당 $RT$ 로, 자리당 전하 $e$ 가 몰당 $F$ 로 한꺼번에 환산 --- 비는 불변).
```

근거: (i) 사슬 자체는 재유도로 정확(무발견) — 다만 4중 괄호 산문이라 displayed 한 줄이 더 간결·정확. (ii) 현행 "$w_j\equiv RT/F$" 는 eq:wbase 의 전역 정의 $w_j=n_jRT/F$ 와 같은 기호의 국소 재정의(사실상 $n_j{=}1$ 특수화) — 첨자 없는 $w$ 로 두면 충돌이 사라진다(후속 두 곳의 $w_j$ 도 동반 치환 필요: 390–392행).

---

## 4. 서치 절 (하이쿠 서브에이전트 위임 — Crossref 왕복 검증분만)

A06-H1 제안의 "고전 시도빈도(Vineyard 형)" 서술에 문헌 anchor 를 달 경우의 검증 후보(등재는 마스터 재량 — 기존 키 mcquarrie1976·glasstone1941 로도 서술 자체는 지지 가능하므로 신규 등재는 선택):

| key(제안) | 저자 | 제목 | 저널 | 권 | 쪽 | 연도 | DOI | 검증 방법 |
|---|---|---|---|---|---|---|---|---|
| vineyard1957 | George H. Vineyard | Frequency factors and isotope effects in solid state rate processes | Journal of Physics and Chemistry of Solids | 3 | 121–127 | 1957 | 10.1016/0022-3697(57)90059-8 | 하이쿠 서브 Crossref 왕복 검증(query 검색 → DOI 재조회 동일 확인) 성공 |

기존 인용 5키(bazant2013·eyring1935·glasstone1941·laidlerking1983·mcquarrie1976)는 `ch1v22_bib.tex` 실재 + V1 원장 승계 확인(v1.0.21 원장: glasstone1941·laidlerking1983 = v1.0.20 P7 검증 승계 명시, mcquarrie1976 = 기존 V1 키) — 신규 검증 불요.

---

## 5. 무발견 축 (검토했으나 문제 없음 — 재계산·재유도·원문 대조 완료분)

1. **부호 사슬 전건**: eq:bv→eq:db($\chi$ 상쇄)→eq:logisticsolve(분모·분자 나누기 주석 포함)→eq:xieq($s\to\sigma_d$·여집합 동치)→signbox(방전 $V\!\uparrow\Rightarrow\xi_\eq\!\uparrow$ — sec03 (d)·sm-electro signbox 와 일치)→§dist($\theta_\eq$·$\xi_\eq$ 부호, Part T eq:logistic 과 "부호까지 동일" 주장 원문 대조 일치) — 전 단계 재유도 일치.
2. **TST 유도 본체**: $q_\mathrm{rc}$(eq:tst-qrc)·반쪽 Maxwell 평균 $\langle v\rangle=(k_BT/2\pi m^*)^{1/2}$(적분 재수행)·$(\langle v\rangle/\delta)q_\mathrm{rc}=k_BT/h$($m^*,\delta$ 상쇄 재계산)·$k_BT/h@298\,\mathrm K=6.209\times10^{12}$/s·eq:tst-rate 인구비 논증·eq:tst-dG 식별·eq:tst-box 대수 — 모두 정확(문제는 verifybox (ii)·접속 괄호에 국한 = H1·M1).
3. **수치 전건**: fig:barrier 전 좌표점($G_\mathrm{base}$ 수치·정 0.65/역 1.15/정점 0.25/도착골 −0.4) · fig:flux($\xi_\eq=\tfrac12,\tfrac23,\tfrac45$) · fig:logistic($w=23.094/25.680/28.265$ mV, 정점 $1/(4w)=10.825/9.735/8.845$/V, FWHM $=2\ln(3{+}2\sqrt2)w=3.5255w=81.4/90.5/99.7$ mV, 곡선 표본점·접선 기울기·면적 보존) · $2RT@298.15\,\mathrm K=4957.6\approx4958$ J/mol · $RT/F@25^\circ\mathrm C=25.69$ mV — 전부 재계산 일치.
4. **폭 문단의 대수**: $n_j=w_jF/RT$ 역산 · $\partial w_j/\partial T=(R/F)(n_j+T\,\dd n_j/\dd T)$(ch2 eq:dwdT-nT 와 축자 수준 일치·종합식 sec08:34–35 수신 확인) · 단상 유효 폭 인자(eq:Veq 재미분) — 일치.
5. **§dist 통합의 정량 검증**: $\Xi_1$ 흡수형·eq:fermifn·$N_A\tilde\varepsilon=\mu^0$(sec02a:317–319 원문 확인)·$\Delta\mu=+sF(V-U_j)$ 대입 사슬 · (d) 의 "$\Delta\mu$ 에 $-\Omega(1-2\xi)$ 가 더해진 자기무모순 분포" — eq:mu 를 $\theta=1-\xi$ 로 변환해 재유도하면 $RT\,\mathrm{logit}(\xi)=sF(V-U)-\Omega(1-2\xi)$ 로 eq:Veq 와 **정확히 동치** 확인 · spinodal 접힘 지목(eq:spinodal) — 일치.
6. **참조 라벨 전수 실재**: sec:pol(eq:vn 의 $V_n$)·eq:center(분기 중심 조건식)·eq:eqcond·eq:Veq·eq:mu·eq:spinodal·eq:partfn·eq:fermifn·eq:sm-sint·eq:belliden·eq:logistic(ch2)·ssec:overlap·ssec:weff·sec:synthesis·sec:lco-direction·sec:lco-electronic($f(E)$ 형 일치)·sec:broadening(-class)·sec:eqpeak·sec:hys·sec:sum·tab:staging — 전부 실재·내용 정합.
7. **폭 폴백·초기값 정합**: 0.020/0.016/0.014/0.012 V(sec10:45·§7 ②와 삼중 일치) · "$n$ 우선·$w$ 폴백은 $n$ 입력 배제 시 활성" 규정 삼중 일치 · $\Omega_j$ 초기값 6000/8000/10000/13000 J/mol 전부 $>2RT$ — "네 전이 모두 출발점에선 두-상 쪽" 주장 성립 · 두-상 실명 회피와 §broadening-class 위임 — §7·파생 C 각주와 정합.
8. **srcbox(Bazant 다리)**: 지수 등치 eq:br-bazant2013-1($F=N_Ae$·$R=N_A\kB$) 재유도 일치 · $\eta$ 기호 충돌 가드(§broadening 의 $U_\app=U_j+\eta$ 와 별개 선언) 원문 대조 일치 · "이상 교환속도 vs 조성 의존 $I_0$" 가정 차 서술 — P3-5 취지의 4항목(서지·구조·매핑·가정 차) 충족.
9. **P3 관련**: V 위계(평가 전위 $=V_n$ 명시, P3-1) · ver.N/Chapter 명칭 혼동 없음(P3-7) · 전달식 충돌 없음(Part T eq:dwdT-nT·ssec:weff·synthesis 대조, P3-6). bgbox 독립성("본문 흐름은 이 박스 없이도 읽히고") 유지 — 제거 용이 블록 규약 충족.
10. **문장 검산 소항목**: "열역학은 detailed balance 한 곳으로만" — $\mathcal A$ 정의는 부기(열역학 항등 재사용)로 보면 성립, 과대 주장 아님 판단 · (a) "$\Delta G_a$ 이상을 갖출 확률 $\propto e^{-\Delta G_a/RT}$" — 발견적 서술이며 bgbox 가 엄밀화한다고 자기 선언(42–44행)이 이미 있어 무발견 처리 · $z\ge0/z<0$ 분기 평가(오버플로) — 표준 안정화, 정확.

---

## 6. 보고 신뢰도 4-tier

- **T1 확정(재계산·원문 대조로 결정)**: A06-H1(재유도 2경로 모두 검증)·M1(대수 항등)·M3(재유도 + ch2 warnbox 축자 대조)·M4·M5(참조 구조 원문 확인)·M6(규정 삼중 대조)·L1·L2(eq:belliden 원문 대조)·L4(수치 재계산)·L5(대수) · §5 무발견 축 1–10 전건.
- **T2 추정(정황·판단 포함)**: A06-M2 의 "독자 혼동" 정도 평가(형식 사실 — 포인터 부재·§8 소재 — 은 확정) · M7·M8 의 개선 이득 평가 · L3 의 오독 여지 평가.
- **T3 미검증(본 창 범위 밖 — 판단 보류)**: srcbox 의 Bazant 2013 원문 식번호([7][26][27][29]) 실물 대조(기존 자산 — 선행 라운드 검증 승계 추정, 원문 미접근) · eyring1935 DOI 실물 왕복(원장 승계 신뢰) · 그림 3종의 컴파일 렌더링 배치(좌표 수치는 확정, 겹침 여부는 빌드 확인 필요).
- **T4 제안 채택 조건부**: H1 채택 시 (iii) 표현 정렬(L1 병기)·M5 채택 시 §8 (a) 의 참조 1치환 — 마스터 일괄 적용 시 상호 의존 주의.
