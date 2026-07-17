# A13_REVIEW — §2.4 Einstein 진동 보정 · §2.5 섞임과 겹침 심층 검토 (FR-A13)

> 대상(전문 정독 완료):
> - `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch2_sec04_einstein.tex` (이하 **sec04**)
> - `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch2_sec05_mixing.tex` (이하 **sec05**)
> - 소속: **ch1_graphite_v1.0.22.tex 빌드 Part T(열특성부)** — 파일명 `ch2_` 는 역사적 명칭(LCO 챕터 문서와 별개). 부록 문자: A=ch1_appA, B=ch1_appB, C=ch2_appA(함정표), D=ch2_appB(코드맵) — 마스터 입력 순서로 확인.
> 참조 원문 대조 완료(read-only): ch2_sec01(eq:logistic·eq:Vxi·eq:BW·eq:Veq_BW), ch2_sec02(eq:Sconfig·eq:dSconfig·eq:dVdT_config·tab:ds·ssec:decomp), ch2_sec03(eq:Svib_mode·eq:Se-ch2·ssec:vib·ssec:elec), ch2_sec06·07·08·09, ch1_sec02b(eq:sm-mc-balance·요동 증명), ch1_sec04(eq:Ubranch·eq:center·fig:hysgap), ch1_sec07(broadening 세 출처), ch2_appA(함정표)·ch2_appB(부록 D.3), ch1v22_bib, results/V1022_REFERENCE_LEDGER.md.
> 규율: 보고 전용 — 소스 무수정·git 무조작·`Codex/` 무접근. 문헌 서치는 haiku 서브에이전트 위임(§서치).

---

## 0. 요약

- **H 3건**: (H1) 흡수 상수를 고전 극한값으로 오인식하는 본문 문장(그림 캡션과 상충 — 캡션이 옳음), (H2) 단일 Einstein 모드 접기의 암묵 전제(알짜 +1 모드·진폭 R 고정) 미명시 → 고전 극한 편차 최대화(§2.3 전제와 역순)·편차 기울기 양수 강직, (H3) vib/electronic 식별 근거로 든 "강제 영점" 은 규약상 두 잔여가 공유 — 식별력은 곡률에만 있음.
- **M 7건**: 식별 곡률 신호의 정량 결여(0.06–0.08 μV/K 급)와 "준양자 창을 걸치는" 문구, "단순 곱" 문장의 불친절, 그림 (a) 파선 마지막 점 수치 오류, eq:hys_branch 의 gap T-동결 전제 미명시(분기 단독 측정 바이어스 ±0.15 mV/K 급), "평균이 ΔS_rxn,j/F 로 떨어지는" 대상 부정확+"config 곡률" 용어, 분기식의 config 항 침묵 탈락, LCO 포논 50–80 meV 무인용(흑연 빌드 맥락).
- **L 8건**: 문체·주석 정합·수식화 제안.
- 수식·수치는 **전부 재계산/재유도로 검증**(§5 재계산 기록). eq:Svib-einstein·eq:dSvib·eq:dUvib·eq:implicit_diff·eq:gj·eq:dxidT·eq:dwdT-nT·eq:weighted·eq:single_config·eq:hys_branch·eq:hys_rev 의 대수 자체는 **전부 옳다**. 그림 (b) 3곡선·본문 4수치·그림 (a) 실선 좌표도 전부 일치(파선 마지막 1점만 오류).

---

## 1. 발견 표

표기: 등급 H=논리/물리 오류·오귀속, M=의미·이해 실질 개선, L=문체. 유형=보완/논리/설명/수식화. 행 번호는 현행 파일 기준. **현행 열의 축자 전문은 §2 "기계 매칭용 축자 블록"** 에 개행 보존으로 재수록(마스터 기계 매칭용).

| ID | 파일:행 | 유형 | 등급 | 현행(축자 — 요지 발췌, 전문은 §2) | 제안(완성 LaTeX — 전문은 §2) | 근거 |
|----|---------|------|------|------------|------------------|------|
| A13-H1 | sec04:43 (캡션 172–173 과 상충) | 논리 | H | `곧 앞 절이 흡수한 ``$T$-무관 상수''는 이 보편식을 $T_\mathrm{ref}$ 에서 한 번 평가해 동결한 고온 코너다.` | 흡수 상수 = 닫힌형 $S_\vib(T_\mathrm{ref};\theta_{E,j})$ 로 정정, 고전 코너는 $\theta_{E,j}\ll T$ 한정의 점근 해석으로 강등 (§2 H1) | 재계산: $\theta_E{=}700$ K·$T_\mathrm{ref}{=}298.15$ K 에서 닫힌형 $0.349R$ vs 고전식 $R[1{+}\ln(T_\mathrm{ref}/\theta_E)]=0.146R$ — 2.4배 차. eq:dSvib 가 실제로 빼는 것은 닫힌형 값. 같은 그림 캡션("이 곡선을 $T_\mathrm{ref}$ 에서 한 번 평가해 동결한 값")은 옳게 서술 — 본문↔캡션 불일치. 구현자가 고전값을 빼도록 오독할 수 있는 자리 |
| A13-H2 | sec04:18–19·27–29·99 (+38–44 연동) | 논리/보완 | H | `준양자 모드 스펙트럼을 대표 진동수 하나로 접는다.` / `전 모드 합을 대표 진동수 하나로 접고, $S_\vib=-\partial f_\vib/\partial T$ 를 1몰당으로 적용한다.` / `크기는 준양자 영역에서만 뜻이 있다.` | 적용 범위 문장 신설(모드 수 셈·부호 스코프) + [추가 후보] 부호 있는 진폭 $m_j$ 일반화 또는 생성/반응 두-$\theta$ 차분형 (§2 H2) | (i) 반응 진동 엔트로피는 생성/반응 측 모드 집합의 **차** — 모드 수 균형이면 고전 극한에서 편차가 정확히 0(§2.3 ssec:vib 의 "고전 극한=상수 흡수" 전제의 근거). 그런데 본 닫힌형의 편차는 $u_j\to0$ 에서 $R\ln(T/T_\mathrm{ref})$ 로 **최대**: $T{=}348.15$ K 에서 $\theta_E{=}900/700/500\to$ 고전 순으로 $7.24/9.14/10.97\to13.36$ μV/K — 잔여가 "준양자 전용" 이라는 §2.3 서사와 **역순**(암묵 전제 = 알짜 +1 모드 생성·진폭 $R$ 고정). (ii) $\partial\Delta S_\vib/\partial T=C_E(u_j)/T\in(0,R/T]$ 로 **항상 양** — 반응 $\Delta C_p<0$(경화형) 잔여 표현 불가. 가상 수치 예: 균형 차분형(생성 $\theta_p{=}700$ K, 반응 $\theta_r{=}340$ K 가정, 모드 3개)이면 348.15 K 편차 $=3R[0.1061-0.1414]=-9.1$ μV/K — 현행 단일모드 $+9.14$ 와 **부호 반전**. "크기는 준양자 영역에서만 뜻이 있다"(99행)도 폼 안에서는 수치상 성립하지 않음(고전 쪽이 더 큼) — "물리적 뜻" 이라는 의도로 한정 필요 |
| A13-H3 | sec04:102–104 (+캡션 177–179) | 논리 | H | `이 강제된 $T_\mathrm{ref}$ 영점과 고온 로그 곡률이 곧 식별의 근거다: electronic 항 (식~\eqref{eq:Se-ch2}, $\propto T$)은 $T$ 에 선형이고 강제 영점이 없어, 다온도 $dQ/dV$ 곡률 피팅이 두 함수형을 갈라 앞 절이 우려한 혼입을 해소한다.` | 식별 근거를 "곡률(함수형)"로 단일화 — 강제 영점은 두 잔여가 공유하는 규약임을 명시 (§2 H3) | §2.2 ssec:decomp warnbox: $\Delta S^0_j$ 는 "vibrational·electronic 의 중심 기여를 이미 흡수한 상수" → 일관 구현에서 electronic 잔여도 $\gamma(T-T_\mathrm{ref})$ 꼴로 **같은 강제 영점**을 가짐. 설령 $\gamma T$ 로 적어도 자유 상수 $\Delta S^0_j$ 재정의로 같은 족 — 선형 성분은 어떤 기준화든 $\{\Delta S^0_j,\gamma\}$ 에 축퇴. 즉 식별력은 **곡률에만** 있고, 영점은 식별 근거가 아님(결론인 "3 온도점 필요·2점 축퇴"는 옳음 — 근거의 절반이 오귀속). 부수: 창 내($u\approx2.0$–$2.5$)의 곡률은 로그 영역($u\lesssim1$)이 아니라 양자 크로스오버 곡률 — "고온 로그 곡률" 표현도 창 밖 성질 |
| A13-M1 | sec04:104–106 (+§2.9:27–28 동일 문구) | 보완/설명 | M | `단 분리에는 준양자 창 $\kB T\!\sim\!\hbar\omega$ 를 걸치는 $T$ 점\n\textbf{셋 이상}이 필요하다 --- 2-온도 유한차분(국소 기울기만 봄)은 곡률과 선형을 합으로만 보아 축퇴하므로,\n``섞일 수 있다''는 것은 저-온도점 진단이지 물리적 비식별성이 아니다.` | 곡률 신호 정량(0.06–0.08 μV/K) + "준양자 영역($u_j\gtrsim1$)에 놓인" 으로 재서술 + "저-온도점"→"온도점 수 부족" (§2 M1) | (i) "$\kB T\sim\hbar\omega$ 를 걸치는" 을 축자로 읽으면 $T\sim\theta_{E}$(580–930 K) 를 걸쳐야 — 전해질 안전 창(≈250–350 K)에서 불가능. 실제 요구는 "준양자 영역 안에서 곡률이 분해되게 벌어진 3점". (ii) 재계산: 본문 4점(−3.74/0/+3.70/+9.14 μV/K)의 양끝 현을 빼면 중간 두 점 이탈 +0.057/+0.081 μV/K — 이것이 elec(선형)과 가르는 **전체 신호**. 편차 자체(±3.7–9.1 μV/K)의 1/50 규모임을 밝혀야 실측 요구 정밀도(≲0.1 μV/K 급)가 정직해짐. (iii) "저-온도점"은 "낮은 온도의 점"으로 오독됨 |
| A13-M2 | sec04:59–60 | 설명 | M | `가산을 엔트로피 항 하나로만 하면 전위 중심과의 정합이 깨진다. 단순 곱 $T\Delta S_\vib/F$ 는 미분 시 여분\n항을 남기기 때문이다.` | 두 소박한 대안과 각각의 실패를 명시: 엔트로피만 가산 시 $\partial U_j/\partial T\ne\Delta S_{\eff,j}/F$, 중심에 $T\Delta S_\vib/F$ 가산 시 여분 항 $=C_E(T;\theta_{E,j})/F$ (§2 M2) | "단순 곱"의 선행사 부재로 독자가 무엇을 곱했는지 막힘. 재계산: $\partial_T[T\Delta S_\vib/F]=\Delta S_\vib/F+(T/F)\,\mathrm d\Delta S_\vib/\mathrm dT$, 둘째 항 $=(T/F)(C_E/T)=C_E/F$ — 여분 항의 정체를 적으면 round-trip 적분(이후 (b)) 도입 동기가 완결 |
| A13-M3 | sec04:122 (그림 (a) 파선 데이터) | 논리 | M | `(1.540,1.4318) (1.600,1.4574)};` | `(1.540,1.4318) (1.600,1.4700)};` | 재계산: 고전 극한 $1+\ln(T/\theta_E)$ 의 $T/\theta_E{=}1.600$ 값은 $1.4700$. 수록값 $1.4574=1+\ln(1.58)$ — 1.58 격자값이 1.60 자리에 들어감. 파선 나머지 23점·실선 33점은 전부 식과 일치 확인. 캡션이 "좌표는 식~\eqref{eq:Svib-einstein}·\eqref{eq:dUvib} 그대로의 수치 평가다" 를 명시하므로 1점 오류도 주장 위반(끝점 꺾임·실선과의 간격 1.8배 과장) |
| A13-M4 | sec05:198–206 (eq:hys_branch 유도) | 논리/보완 | M | `분기별 전이 중심을 $U_j^{(d)}=U_j+\tfrac12\sigma_d\,\Delta U_j^\hys$ 로 두면 --- (중략) --- 각 분기의 엔트로피 계수는 \emph{그 분기의} 봉우리\n모양 $g_j^{(d)}$ 로 가중된 \eqref{eq:weighted} 다:` | gap $T$-동결 전제 명시 + 분기 단독 측정의 $\pm\tfrac12\,\partial\Delta U_j^\hys/\partial T$ 바이어스와 평균의 소거를 문장으로 추가 (§2 M4) | eq:hys_branch 가 성립하려면 $\partial U_j^{(d)}/\partial T=\Delta S_{\rxn,j}/F$, 곧 $\partial\Delta U_j^\hys/\partial T=0$ 이 필요 — 모델 관례(Ch1 eq:center 의 $\Delta U_j^\hys(T_\rep)$ 동결)로는 성립하나 **전제가 본문에 없음**(유도 비약). 물리적으로 gap 은 강한 $T$-의존(fig:hysgap(b): $\Omega{=}10^4$ J/mol 곡선 기울기 $\approx-0.30$ mV/K — 그림 수록 좌표 (280 K, 61.68)→(320 K, 49.51) 에서 재계산). 실측 분기 단독 온도계수는 $\mp0.15$ mV/K 급 홀수 항을 담아 $\Delta S^0_j/F$(±0.3 급)와 같은 자릿수 — 분기 평균이 이 홀수 항을 (선형화 1차에서) 정확히 소거한다는 것이 eq:hys_rev 를 써야 하는 정량적 이유인데 현행 근거는 "한 사이클 돌면 상쇄" 서사뿐 |
| A13-M5 | sec05:214–217 | 논리/설명 | M | `분기 중심이 서로 달라 같은 $x$ 에서 $g_j^{(\mathrm{ch})}\!\ne\!g_j^{(\mathrm{dis})}$ 이면, 겹침\n가중식~\eqref{eq:hys_branch} 의 config 곡률 때문에 평균이 $\Delta S_{\rxn,j}/F$ 로 떨어지는 것은 $\Delta U^\hys$\n의 1차까지이고 유한 $\Delta U^\hys$ 에선 고차 보정이 남는다.` | 평균의 극한 대상을 "$\Delta U^\hys\to0$ 의 겹침 가중값(연속 블렌드)" 으로 정정 + "config 곡률"→"가중(봉우리 형태) 곡률" + 짝수성 논거 1문장 (§2 M5) | (i) 겹침 영역에서 $\Delta U^\hys{=}0$ 극한값은 블렌드 $\sum Q_jg_j\Delta S_{\rxn,j}/\sum Q_jg_j$ 이지 개별 $\Delta S_{\rxn,j}/F$ 가 아님(후자는 단일 전이 지배 한정). (ii) 곡률의 출처는 $g_j^{(d)}$ 봉우리 형태(가중) 차이 — 본 절이 스스로 세운 "g 4종 충돌" 경계에서 config **항**($n_jRz_j/F$)과 다른 물체인데 "config 곡률" 로 명명해 혼동 유발. (iii) 재유도: 분기 교환에서 shift 가 홀($\pm\delta_j$)이라 평균은 $\delta$ 의 짝함수 — 보정이 $O(\Delta U^{\hys\,2})$ 부터임을 한 문장으로 밝히면 "1차까지 정확" 의 근거 완결 |
| A13-M6 | sec05:200–206 | 보완 | M | `각 분기의 엔트로피 계수는 \emph{그 분기의} 봉우리\n모양 $g_j^{(d)}$ 로 가중된 \eqref{eq:weighted} 다:` (+eq:hys_branch 수식) | 분기식이 단순식 수준임을 명시하고 완전식 수준의 config 항 $+n_jRz_j^{(d)}/F$ 가 그대로 붙음(균일 gap 이면 $z_j^{(d)}$ 분기 불변)을 추가 (§2 M6) | 파생 A/B 가 "측정급은 완전식(config 포함)" 을 srcbox 수치로 확립한 직후, 파생 D 가 config 없는 \eqref{eq:weighted} 형으로 복귀 — 독자 질문("config 는 어디로?")에 답 없음. 재유도: 전이 공통 gap 이면 고정 $\bar x$ 에서 $U_\oc^{(d)}-U_j^{(d)}=U_\oc^{(0)}-U_j$(강체 이동)라 $z_j^{(d)}$ 분기 불변 → config 몫은 평균에서 형태 불변으로 살아남고, 전이별 gap 이면 $O(\Delta U^{\hys\,2})$ 보정 — 한 문장이면 닫힘 |
| A13-M7 | sec04:22–25 | 보완 | M | `대표값의 선택 --- 예컨대\nLiCoO$_2$ 광학 포논 $50$--$80$~meV $\to\theta_{E,j}\approx580$--$930$~K --- 은 \emph{단위 환산 예시일 뿐}이며,` | 무인용 수치의 출처 한정 or 흑연 쪽 예시 병기 — 서치 결과(§4) 기반 후보 문헌은 [원장 등재 필요] 절차로 (§2 M7) | 50–80 meV 범위는 무인용 수치(환산 예시라 해도 본서의 서지 규율상 이례). 또한 본 절은 **흑연 빌드(Part T)** 소속인데 예시가 LCO 뿐 — 바로 이어 인용되는 jpcc2021 은 흑연 제일원리 진동·배치 분해 논문이라 흑연 쪽 대표 스케일 병기가 자연스러움. 환산 자체(580–930 K·700 K≈60 meV)는 재계산 정확(1 meV=11.6045 K) |
| A13-L1 | sec04:190 | 문체 | L | `[C-61] 하위호환 θ_E 미지정 두 가산 0(회귀 기준→부록B)` | `[C-61] 하위호환 θ_E 미지정 두 가산 0(회귀 기준→부록 D)` | 본문(96행) "부록 D가 명세한다" 는 병합 빌드 부록 문자(D=ch2_appB) 기준으로 정확 — % 자산 주석만 구 단독-Ch2 문자(B) 잔존. 동일 잔존이 sec08 주석 [C-111] 에도 있으나 본 창 대상 밖(참고만) |
| A13-L2 | sec05:83–85 | 설명 | L | `가중 분모 $\sum Q_jg_j$ 가 정확히 측정\n$dQ/dV$($=Q\,\partial\bar x/\partial U$; $\bar x$ 무차원이라 $Q$ 배)이므로` | 괄호를 유도 한 줄로 교체: 음함수~\eqref{eq:implicit} 양변의 $U$-미분 (§2 L2) | "무차원이라 $Q$ 배" 는 차원 맞춤 설명이 압축돼 독자가 막히는 자리. $\partial_U$[식~\eqref{eq:implicit}]: $\sum_jQ_jg_j=Q\,\partial\bar x/\partial U$ 한 줄이 더 정확·간결 |
| A13-L3 | sec05:97–100 | 설명 | L | `그리드 실측 최대값 $0.18$ 은 극값을 정확히 샘플하지 않은 결과로,\n해석 상한은 $0.21$ 이다.` | "같은 양(완전식−단순식)의 175점 그리드 최대가 0.18, 그리드 점 사이 해석 극값이 0.21" 로 관계 명시 (§2 L3) | 단순식 오차≡config 항(파생 B)이므로 두 수가 같은 양의 두 샘플링임을 명시해야 "왜 0.18≠0.21" 질문이 닫힘. 크기 자체는 재계산 정합($R/F{=}0.0862$ mV/K, $|0.21|$ ⇔ $|\ln$-odds$|{=}2.4$, $\xi{\approx}0.92$ — 그리드 끝에서 자연) |
| A13-L4 | sec05:192–193 | 보완 | L | `(상호작용 엔트로피 $\propto\partial\Omega/\partial T$\n같은 2차 항이 있을 수 있으나, 흑연에서 소수이고 본 장 범위 밖이다.)` | `…있을 수 있으나, 본 장은 소수로 \emph{가정}하며(값 미확보 --- \S\ref{sec:method} 공백 (3)) 범위 밖이다.)` | §2.9 정직한 한계 (3) "상호작용 $\Omega$ 의 온도 의존…값은 아직 확보하지 못했다" 와 단정 어조가 어긋남. 공백을 메우자는 제안이 아니라(GS 규율 준수) 단정→가정으로 어조 정합만 |
| A13-L5 | sec04:50–57 | 문체 | L | `\Delta S_\vib(T) \;\equiv\; S_\vib(T;\theta_{E,j})-S_\vib(T_\mathrm{ref};\theta_{E,j}),` | 정의 직후 "(전이별 양 — $\theta_{E,j}$ 의존; 표기 간결을 위해 $j$ 를 생략한다)" 1구 추가 | $\Delta S_\vib(T)$ 가 $j$-무첨자인데 $\theta_{E,j}$ 의존 — §2.5·§2.8 로 전달될 때 전이별 양임이 기호에서 안 읽힘. 기존 기호 불변(P5), 주석만 |
| A13-L6 | sec05:45–47 | 수식화/문체 | L | `$\xi_j$ 가 logistic 인자 $a_j=(U-U_j(T))/w_j(T)$ 의 함수이고\n$\partial\xi_j/\partial a_j=g_j w_j$, $\partial w_j/\partial T=n_jR/F$ 임을 쓰면($z_j\equiv(U-U_j)/w_j=\ln[\xi_j/\n(1-\xi_j)]$), 연쇄율로` | $a_j$ 를 $z_j$ 로 통일한 한 줄 연쇄율 표시 (§2 L6) | $a_j$ 와 $z_j$ 가 같은 정의(중복 기호)로 한 문장 안에 병존 — "g 4종" 수준의 기호 위생을 스스로 세운 절이라 통일 여지. 유도 자체는 재확인 정확 |
| A13-L7 | sec04:80–88 (eq:dUvib 부근) | 수식화 | L | `\boxed{\;\n\Delta U_\vib(T)=-\frac1F\Bigl[\Delta F_\vib(T)-\Delta F_\vib(T_\mathrm{ref})+S_\vib(T_\mathrm{ref})\,(T-T_\mathrm{ref})\Bigr],` | 박스 직후 완전 전개형 1식 병기(구현·부록 D 대응): $\Delta U_\vib(T)=-\tfrac{R}{F}\bigl[T\ln(1-e^{-\theta_{E,j}/T})-T_\mathrm{ref}\ln(1-e^{-\theta_{E,j}/T_\mathrm{ref}})\bigr]-\tfrac{S_\vib(T_\mathrm{ref};\theta_{E,j})}{F}(T-T_\mathrm{ref})$ (§2 L7) | 현행 박스는 $\Delta F_\vib$ 기호 경유 — 구현자는 한 번 더 조립해야 함. 전개형 재계산 검증: $\theta_E{=}700$ K, $T{=}348.15$ K 에서 $+0.230$ mV (사다리꼴 적분 근사 $\tfrac12(0{+}9.14)\,\mu$V/K$\times50$ K$\approx0.23$ mV 와 정합) |
| A13-L8 | sec05:161–186 (파생 C) | 수식화 | L | `\item \textbf{단상($\Omega\le2RT$, 균질 고용체)}: …` / `\item \textbf{두-상($\Omega>2RT$, 상분리; …)}: …` | 이중지위 요약 소표 병기(불릿 유지·표 추가): 전이 유형/판정 근거/$w_j$ 지위/$T$-의존 서식 4열 (§2 L8) | 파생 C 의 결론이 §2.8 종합식·§2.9 절차·§1.7 broadening 세 곳에서 재인용되는 허브 — 산문 불릿을 4열 표로 병기하면 인용처가 기계적으로 참조 가능. 기존 문장 삭제 없음 |

---

## 2. 기계 매칭용 축자 블록 + 완성 제안 LaTeX

### A13-H1 — 흡수 상수의 오인식 (sec04:38–44)

**현행 축자(sec04:38–44):**
```latex
두 극한이 이 닫힌형을 검산한다. 고전극한 $\kB T\gg\hbar\omega_{E,j}$($u_j\to0$)에서
$-\ln(1-e^{-u_j})\to-\ln u_j+u_j/2$, $u_j/(e^{u_j}-1)\to1-u_j/2$ 가 상쇄해
\[
S_\vib\;\to\;R\bigl[1+\ln(T/\theta_{E,j})\bigr],
\]
곧 앞 절이 흡수한 ``$T$-무관 상수''는 이 보편식을 $T_\mathrm{ref}$ 에서 한 번 평가해 동결한 고온 코너다.
저온 $u_j\to\infty$ 에서는 $S_\vib\to0$(모든 모드가 바닥상태로 얼어붙어 흩어짐이 사라진다).
```

**제안(마지막 두 문장 대체 — 앞의 극한 전개는 그대로):**
```latex
곧 앞 절이 흡수한 ``$T$-무관 상수''는 닫힌형~\eqref{eq:Svib-einstein} 을 $T_\mathrm{ref}$ 에서 한 번 평가해
동결한 값 $S_\vib(T_\mathrm{ref};\theta_{E,j})$ 이며(그림~\ref{fig:svibid}(a) 캡션과 같은 서술), 고전 극한이
유효한 모드($\theta_{E,j}\ll T_\mathrm{ref}$)에서는 그 값이 위 보편식의 고온 코너
$R[1+\ln(T_\mathrm{ref}/\theta_{E,j})]$ 로 줄어든다 --- 단 본 절의 대표 준양자 작동점($\theta_{E,j}{\approx}700$~K,
$u_j{\approx}2.35$)에서는 닫힌형 $0.35R$ 대 고전 코너 $0.15R$ 로 갈리므로, 편차 정의~\eqref{eq:dSvib} 가 빼는
기준값은 언제나 닫힌형 쪽이다. 저온 $u_j\to\infty$ 에서는 $S_\vib\to0$(모든 모드가 바닥상태로 얼어붙어
흩어짐이 사라진다).
```

**근거(재계산):** $u=700/298.15=2.34781$: $-\ln(1-e^{-u})=0.10044$, $u/(e^u-1)=0.24811$ → $S/R=0.34855$. 고전식: $1+\ln(0.42593)=0.14646$. 비 2.38배. eq:dSvib 는 닫힌형 $S_\vib(T_\mathrm{ref};\theta_{E,j})$ 를 뺀다(50–51행) — 본문 43행만이 고전 코너로 오지시. 그림 캡션 172–173행("앞 절이 중심 표준값에 흡수한 ``$T$-무관 상수''는 이 곡선을 $T_\mathrm{ref}$ 에서 한 번 평가해 동결한 값이다" — "이 곡선"=닫힌형)이 정답 서술이므로 본문을 캡션에 정렬.

### A13-H2 — 단일 모드 접기의 암묵 전제(모드 수·부호) 미명시 (sec04:18–29·99)

**현행 축자(sec04:18–19):**
```latex
준양자 모드 스펙트럼을 대표 진동수 하나로 접는다. 전이 $j$ 의 Einstein 온도를 $\theta_{E,j}\equiv\hbar
\omega_{E,j}/\kB$ 로 정의하면($\kB\theta_{E,j}\equiv\hbar\omega_{E,j}$), 무차원 비 $u_j\equiv\theta_{E,j}/T$ 로
```

**현행 축자(sec04:27–29):**
```latex
\textbf{(a) 출발 --- Einstein 단일 모드.} 식~\eqref{eq:Svib_mode} 유도의 모드 자유에너지
$f_k=\kB T\ln(1-e^{-\beta\hbar\omega_k})$ 에서 전 모드 합을 대표 진동수 하나로 접고, $S_\vib=-\partial
f_\vib/\partial T$ 를 1몰당으로 적용한다.
```

**현행 축자(sec04:99):**
```latex
크기는 준양자 영역에서만 뜻이 있다. 대표값 $\theta_{E,j}=700$~K($\approx60$~meV)$\cdot$$T_\mathrm{ref}=298.15$~K
```

**제안(ssec:einstein-closed 말미 — 44행 뒤 — 에 적용 범위 문단 신설; 기존 문장 삭제 없음):**
```latex
★\textbf{적용 범위 --- 모드 수 셈과 부호.} 위 닫힌형은 전이당 \emph{알짜 한 모드}(진폭 $R$ 고정)가 반응에서
생성되는 셈법이다. 실제 반응 진동 엔트로피는 생성/반응 측 모드 집합의 \emph{차}이므로 모드 수가 균형이면
고전 극한에서 $T$-편차가 정확히 $0$ 으로 상쇄되는데(\S\ref{ssec:vib} 의 ``고전 극한 $=$ 상수 흡수'' 전제의
근거가 이 상쇄다), 단일모드 셈법의 편차~\eqref{eq:dSvib} 는 반대로 $u_j\to0$ 에서 $R\ln(T/T_\mathrm{ref})$ 로
가장 크고 기울기 $\partial\Delta S_\vib/\partial T=C_E(u_j)/T$($C_E$ 는 Einstein 비열, $0<C_E\le R$)가 항상
양이다. 곧 $\theta_{E,j}$ 지정은 ``알짜 연화형($\partial\Delta S_{\rxn,j}/\partial T>0$) 잔여를 갖는 준양자
전이''에 한해 물리적 뜻이 있으며, 경화형($\Delta C_p<0$) 잔여까지 담으려면 [추가 후보 --- 본 절은 제안만
둔다] 부호 있는 진폭 $m_j$ 의 일반화
\[
\Delta S_\vib(T)\;\to\;m_j\bigl[S_\vib(T;\theta_{E,j})-S_\vib(T_\mathrm{ref};\theta_{E,j})\bigr],\qquad
\Delta U_\vib(T)\;\to\;m_j\,\Delta U_\vib(T)\quad(m_j{=}1\text{ 이 현행 서식})
\]
또는 생성/반응 두 대표 모드의 차분형 $S_\vib(T;\theta_{E,j}^{\,p})-S_\vib(T;\theta_{E,j}^{\,r})$(고전 극한
편차 자동 $0$)이 필요하다 --- 두 경우 모두 편차가 선형으로 들어가므로 round-trip 박스~\eqref{eq:dUvib} 는
같은 인자만 곱해 그대로 성립하고, $\theta_{E,j}$ 미지정 하위호환(부록 D)도 불변이다.
```

**근거(재계산):** (i) 고전 극한 균형 상쇄: 모드당 고전 $S=R[1+\ln(T/\theta)]$ — 모드 수 같으면 차에서 $\ln T$ 소거, $T$-무관 $R\ln(\theta_r/\theta_p)$ 만 잔존 → 편차 0 (§2.3 전제의 수학적 내용). (ii) 단일모드 편차의 $\theta_E$-순서(348.15 K): $900\to7.24$, $700\to9.14$, $500\to10.97$, $\theta_E\to0\to R\ln(348.15/298.15)/F=13.36$ μV/K — 고전에 가까울수록 커짐(그림 (b) 세 곡선 값은 전부 재계산 일치 — 폼 자체가 그러함). (iii) 부호 강직: $\mathrm d\Delta S_\vib/\mathrm dT=C_E(u)/T>0$ 항상. (iv) 가상 균형 차분 예(문헌 주장 아님 — 형태 시연): $\theta_p{=}700$·$\theta_r{=}340$ K·3모드 가정 시 348.15 K 편차 $3R(0.10606-0.14136)=-0.881\times\ldots=-9.1$ μV/K — 현행 $+9.14$ 와 부호 반전. §2.6 극한표(6코너)·부록 D 어디에도 이 스코프가 없음을 확인.

### A13-H3 — "강제 영점" 식별 근거 오귀속 (sec04:102–104 + 캡션 177–179)

**현행 축자(sec04:101–104):**
```latex
차가 커질수록 자란다. 이 강제된 $T_\mathrm{ref}$ 영점과 고온 로그 곡률이 곧 식별의 근거다: electronic 항
(식~\eqref{eq:Se-ch2}, $\propto T$)은 $T$ 에 선형이고 강제 영점이 없어, 다온도 $dQ/dV$ 곡률 피팅이 두 함수형을
갈라 앞 절이 우려한 혼입을 해소한다.
```

**현행 축자(캡션 sec04:177–179):**
```latex
의 수치($\theta_E{=}700$ K 에서 $-3.74/0/+3.70/+9.14\ \mu$V/K)다. electronic 항($\propto T$)은 이
강제 영점이 없어 두 함수형이 다온도 곡률 피팅에서 갈리고, 분리에는 준양자 창을 걸치는 온도점 셋
이상이 필요하다.
```

**제안(본문 대체):**
```latex
차가 커질수록 자란다. 식별의 근거는 함수형의 \emph{곡률}이다: $\Delta S_\vib(T;\theta_{E,j})$ 는 기울기와
곡률이 $\theta_{E,j}$ 하나에 묶인 비선형 1-모수족인 반면, electronic 잔여(식~\eqref{eq:Se-ch2}, $\propto T$)는
$T$ 에 선형이라 곡률이 $0$ 이다 --- 다온도 $dQ/dV$ 곡률 피팅이 두 함수형을 갈라 앞 절이 우려한 혼입을
해소한다. ($T_\mathrm{ref}$ 강제 영점 자체는 식별 근거가 아니다 --- \S\ref{ssec:decomp} 의 흡수 규약대로면
electronic 잔여도 $T_\mathrm{ref}$ 기준화되어 같은 영점을 공유하고, 기준화 여부와 무관하게 선형 성분은 자유
상수 $\Delta S^0_j$ 와 섞여 재정의될 뿐이다.)
```

**제안(캡션 대체 — 해당 두 문장만):**
```latex
의 수치($\theta_E{=}700$ K 에서 $-3.74/0/+3.70/+9.14\ \mu$V/K)다. electronic 항($\propto T$)은 곡률이 $0$
이라 두 함수형이 다온도 곡률 피팅에서 갈리고, 분리에는 준양자 영역에 놓인 온도점 셋 이상이 필요하다.
```

**근거:** §2.2 ssec:decomp warnbox 축자 — "첫 항 $\Delta S^0_j$ 는 중심 표준값으로 vibrational$\cdot$electronic 의 중심 기여를 이미 흡수한 상수다" — 이 규약이면 $T\ne T_\mathrm{ref}$ 에서 미흡수 electronic 잔여는 $\gamma(T-T_\mathrm{ref})$ 로 강제 영점 동반. $\gamma T$ 로 쓰더라도 $(\Delta S^0_j+\gamma T_\mathrm{ref})+\gamma(T-T_\mathrm{ref})$ 재매개로 동일 족 — 영점 유무는 식별 불변량이 아님. 3점 필요 결론은 유지(모수 $\{\Delta S^0_j,\gamma,\theta_{E,j}\}$ 3개 = 최소 3온도점 — 현행 "셋 이상" 정확).

### A13-M1 — 식별 곡률 신호 정량 + "준양자 창을 걸치는" (sec04:104–106)

**현행 축자(sec04:104–106):**
```latex
갈라 앞 절이 우려한 혼입을 해소한다. 단 분리에는 준양자 창 $\kB T\!\sim\!\hbar\omega$ 를 걸치는 $T$ 점
\textbf{셋 이상}이 필요하다 --- 2-온도 유한차분(국소 기울기만 봄)은 곡률과 선형을 합으로만 보아 축퇴하므로,
``섞일 수 있다''는 것은 저-온도점 진단이지 물리적 비식별성이 아니다.
```

**제안(대체):**
```latex
갈라 앞 절이 우려한 혼입을 해소한다. 단 분리에는 준양자 영역($u_j\gtrsim1$)에 놓인, 서로 충분히 벌어진
$T$ 점 \textbf{셋 이상}이 필요하다 --- 2-온도 유한차분(국소 기울기만 봄)은 곡률과 선형을 합으로만 보아
축퇴한다. 크기도 밝혀 둔다: 위 4 온도점($\theta_{E,j}{=}700$~K)에서 양끝을 잇는 직선을 빼면 중간 두 점의
곡률 이탈은 $+0.06/+0.08\ \mu$V/K --- 편차 자체($\pm3.7$–$9.1\ \mu$V/K)의 약 $1/50$ 이므로, 실측 분리는
이 급($\lesssim0.1\ \mu$V/K)의 엔트로피 계수 정밀도를 요구한다. ``섞일 수 있다''는 것은 온도점 수 부족의
진단이지 물리적 비식별성이 아니다.
```

**근거(재계산):** 현(278.15→348.15) 기울기 $12.875/70=0.1839$ μV/K/K; 현 위 값 298.15 K: $-0.057$(실제 0 → 이탈 $+0.057$), 318.15 K: $+3.621$(실제 $+3.702$ → 이탈 $+0.081$). "$\kB T\sim\hbar\omega$ 를 걸치는" 은 $T\sim580$–$930$ K 를 요구하는 것으로 축자 독해됨 — 전지 실험 창에서 불가능(의도는 "준양자 영역 안의 점들"). §2.9:27–28 동일 문구는 본 창 대상 밖이나 동일 수정 권고(참고).

### A13-M2 — "단순 곱" 문장 (sec04:59–60)

**현행 축자(sec04:59–60):**
```latex
가산을 엔트로피 항 하나로만 하면 전위 중심과의 정합이 깨진다. 단순 곱 $T\Delta S_\vib/F$ 는 미분 시 여분
항을 남기기 때문이다. 대신 모드 자유에너지 편차에서 출발해 중심 이동을 닫는다.
```

**제안(대체):**
```latex
가산을 엔트로피 항 하나로만 하면 --- 곧 $\Delta S^0_j$ 에만 $\Delta S_\vib(T)$ 를 더하고 중심 $U_j$ 를 그대로
두면 --- $\partial U_j/\partial T=\Delta S_{\eff,j}(T)/F$ 가 깨진다. 반대로 중심에 소박한 곱
$\Delta U_\vib\overset{?}{=}T\Delta S_\vib(T)/F$ 를 더하면 미분에서 여분 항이 남는다:
$\partial_T[T\Delta S_\vib/F]=\Delta S_\vib/F+(T/F)\,\partial_T\Delta S_\vib=\Delta S_\vib/F+C_E(T;\theta_{E,j})/F$.
대신 모드 자유에너지 편차에서 출발해 중심 이동을 닫는다.
```

**근거(재계산):** $\partial_T\Delta S_\vib=\partial_TS_\vib=C_E/T$ (Einstein 비열) — 여분 항 $=C_E/F$ 명시로 (b)–(d) 적분 유도의 필요성이 자명해짐. 어조는 기존 본문과 동일(설명 강화만).

### A13-M3 — 그림 (a) 파선 마지막 점 (sec04:122)

**현행 축자(sec04:122, 파선 좌표 말미):**
```latex
(1.300,1.2624) (1.380,1.3221) (1.460,1.3784) (1.540,1.4318) (1.600,1.4574)};
```

**제안(대체):**
```latex
(1.300,1.2624) (1.380,1.3221) (1.460,1.3784) (1.540,1.4318) (1.600,1.4700)};
```

**근거(재계산):** $1+\ln(1.600)=1.47000$. 수록값 $1.4574=1+\ln(1.58)$ (1.58 격자의 값이 1.60 에 이식된 형태). 파선 나머지 전 점(0.380→1.540)·실선 전 점(0.040→1.600) 재계산 일치 — 이 1점만 어긋남. 캡션 주장("좌표는 식 그대로의 수치 평가") 준수 복원 + 우단 실선-파선 간격(참: 0.016, 현: 0.029)의 과장 제거.

### A13-M4 — eq:hys_branch 의 gap $T$-동결 전제 (sec05:198–206)

**현행 축자(sec05:196–206):**
```latex
흑연 OCV(open circuit voltage)는 충방전 사이 경로의존이다(준안정 stacking, stage II 무질서)
\cite{hysteresis2018}. 분기별 전이 중심을 $U_j^{(d)}=U_j+\tfrac12\sigma_d\,\Delta U_j^\hys$ 로 두면 --- $\sigma_d$
는 탈리튬화 부호(\S\ref{sec:hys} 의 분기 중심식~\eqref{eq:Ubranch} 에서 $\gamma_jh_{\eta,j}{=}1$ 로 둔 특수형)라 흑연 라벨에서 \emph{dis 가
$+\tfrac12$(위 가지), ch 가 $-\tfrac12$(아래 가지)}다 --- 각 분기의 엔트로피 계수는 \emph{그 분기의} 봉우리
모양 $g_j^{(d)}$ 로 가중된 \eqref{eq:weighted} 다:
```

**제안(eq:hys_branch 직후 --- 207행 "가역 발열에…" 앞 --- 문장 추가; 기존 문장 무변경):**
```latex
이 분기식은 gap 을 온도 상수로 둔 모델 관례 --- \S\ref{sec:hys} 의 중심 조립~\eqref{eq:center} 이
$\Delta U_j^\hys(T_\rep)$ 로 동결하는 그 관례 --- 아래에서 성립한다. gap 을 온도에 살리면
(\S\ref{sec:hys} 의 닫힌 꼴은 $T\to T_{c,j}$ 에서 소멸하는 강한 $T$-의존을 갖는다) 각 분기에
$\pm\tfrac12\,\partial\Delta U_j^\hys/\partial T$ 의 홀수 항이 가중되어 들어오는데, staging 초기값 스케일로
$\mp0.15$ mV/K 급 --- $\Delta S^0_j/F$ 와 같은 자릿수 --- 라 \emph{한 분기만의} 온도계수는 열역학
엔트로피의 추정치가 되지 못한다. 아래 분기 평균이 이 홀수 항을 (선형화 1차에서) 정확히 소거한다는 것이
평균을 써야 하는 정량적 이유다.
```

**근거(재계산·원문 대조):** eq:hys_branch 의 유도(음함수 미분)는 분자에 $\sum Q_jg_j^{(d)}\,\partial U_j^{(d)}/\partial T$ 를 요구 — $\partial U_j^{(d)}/\partial T=\Delta S_{\rxn,j}/F\pm\tfrac12\partial_T\Delta U_j^\hys$. 현행 식은 둘째 항 부재 = $\partial_T\Delta U_j^\hys{=}0$ 암묵 전제. Ch1 eq:center 가 $\Delta U_j^\hys(T_\rep)$ 동결이므로 모델 내부 일관 — 전제만 미명시(유도 비약). $T$-의존 크기: fig:hysgap(b) 수록 좌표($\Omega{=}10^4$ J/mol) (280, 61.683)→(320, 49.505) → 기울기 $-0.3045$ mV/K → 반값 $0.15$ mV/K. tab:ds 의 $\Delta S^0_j/F$: $+0.301/0/-0.052/-0.166$ mV/K — 같은 자릿수 확인.

### A13-M5 — "평균이 $\Delta S_{\rxn,j}/F$ 로" + "config 곡률" (sec05:214–217)

**현행 축자(sec05:214–217):**
```latex
이 상쇄는 두 분기의 봉우리 형태 $g_j^{(d)}$ 가 같다고 본 \emph{선형화 근사}($\Delta U_j^\hys\!\ll\!w_j$)에서
정확하다. 분기 중심이 서로 달라 같은 $x$ 에서 $g_j^{(\mathrm{ch})}\!\ne\!g_j^{(\mathrm{dis})}$ 이면, 겹침
가중식~\eqref{eq:hys_branch} 의 config 곡률 때문에 평균이 $\Delta S_{\rxn,j}/F$ 로 떨어지는 것은 $\Delta U^\hys$
의 1차까지이고 유한 $\Delta U^\hys$ 에선 고차 보정이 남는다.
```

**제안(대체):**
```latex
이 상쇄는 두 분기의 봉우리 형태 $g_j^{(d)}$ 가 같다고 본 \emph{선형화 근사}($\Delta U_j^\hys\!\ll\!w_j$)에서
정확하다. 분기 중심이 서로 달라 같은 $x$ 에서 $g_j^{(\mathrm{ch})}\!\ne\!g_j^{(\mathrm{dis})}$ 이면, 겹침
가중식~\eqref{eq:hys_branch} 의 가중(봉우리 형태) 곡률 때문에 평균이 $\Delta U^\hys\!\to\!0$ 의 겹침
가중값(단일 전이 지배 영역에서는 $\Delta S_{\rxn,j}/F$)으로 떨어지는 것은 $\Delta U^\hys$ 의 1차까지이고
유한 $\Delta U^\hys$ 에선 고차 보정이 남는다 --- 분기 교환이 중심 이동 $\pm\tfrac12\Delta U_j^\hys$ 의 부호를
일제히 뒤집는 홀 변환이라 평균은 이동의 짝함수이고, 따라서 남는 보정은 $O(\Delta U^{\hys\,2})$ 부터다.
```

**근거(재유도):** (i) 겹침 영역의 $\Delta U^\hys{\to}0$ 극한값은 블렌드 $\sum Q_jg_j\Delta S_{\rxn,j}/\sum Q_jg_j$ — 개별 $\Delta S_{\rxn,j}/F$ 는 단일 전이 지배 한정(eq:single_config 의 조건과 동일). (ii) "config 곡률"의 실체는 $g_j^{(d)}$(가중) 차이 — sec05:42–44 가 세운 "$g$ 4종 충돌" 위생상 config 항($n_jRz_j/F$)과 구분 필요. (iii) 짝수성: 분기값을 이동 $\{\pm\delta_j\}$ 의 함수 $F(\{\pm\delta_j\})$ 로 두면 평균 $\tfrac12[F(\{\delta\})+F(\{-\delta\})]$ 는 짝부 — 홀수(1차) 항 전멸, 보정 $O(\delta^2)$ — "1차까지 정확" 의 수학적 근거.

### A13-M6 — 분기식의 config 항 침묵 탈락 (sec05:200–206)

**현행 축자(sec05:200–206):**
```latex
각 분기의 엔트로피 계수는 \emph{그 분기의} 봉우리
모양 $g_j^{(d)}$ 로 가중된 \eqref{eq:weighted} 다:
\begin{equation}
\frac{\partial U_\oc^{(d)}}{\partial T}
\;=\;\frac1F\,\frac{\sum_j Q_j\,g_j^{(d)}(x)\,\Delta S_{\rxn,j}}{\sum_j Q_j\,g_j^{(d)}(x)}.
\label{eq:hys_branch}
\end{equation}
```

**제안(eq:hys_branch 직후 괄호 문장 추가; 식 자체 무변경):**
```latex
(중심값 수준 --- 단순식~\eqref{eq:weighted} 의 분기판 --- 으로 적었다. 완전식 수준에서는 각 분기에 봉우리
내부 config 항 $+n_jR\,z_j^{(d)}/F$($z_j^{(d)}\equiv(U_\oc^{(d)}-U_j^{(d)})/w_j$)가 같은 자리에서 더해지며,
gap 이 전이 공통이면 고정 $\bar x$ 에서 분기 전위와 분기 중심이 같은 양만큼 이동해
$z_j^{(d)}=z_j$ --- config 몫은 분기 무관으로 평균~\eqref{eq:hys_rev} 에서 형태 불변으로 살아남는다.
전이별 gap 이면 그 차이도 위 고차 보정과 같은 $O(\Delta U^{\hys\,2})$ 다.)
```

**근거(재유도):** 파생 A srcbox 가 "단순식은 최대 0.18 mV/K 빗나감(측정급은 완전식)" 을 확립한 직후, 파생 D 가 config 없는 형으로 복귀하면서 아무 한정이 없음 — 독자 질문 방치. 균일 gap 강체 이동: $U_\oc^{(d)}(\bar x)=U_\oc^{(0)}(\bar x)\pm\tfrac12\Delta U^\hys$ (모든 중심이 같은 이동이면 음함수 해도 같은 이동) → $U_\oc^{(d)}-U_j^{(d)}=U_\oc^{(0)}-U_j$ 정확히 → $z_j^{(d)}$ 불변.

### A13-M7 — LCO 포논 50–80 meV 무인용 + 흑연 빌드 맥락 (sec04:22–25)

**현행 축자(sec04:22–25):**
```latex
안에서 $u_j$ 는 오직 $\theta_{E,j}/T$ 를 뜻한다(부록 C 함정표 참조).} 대표값의 선택 --- 예컨대
LiCoO$_2$ 광학 포논 $50$--$80$~meV $\to\theta_{E,j}\approx580$--$930$~K --- 은 \emph{단위 환산 예시일 뿐}이며,
실제로는 대상 호스트의 실측 포논$\cdot$제일원리 포논 DOS \cite{jpcc2021} 로 교체하거나 다온도 곡률에서 직접
회귀한다[데이터-주도 1순위].
```

**제안(대체 — 서치 §4 의 검증 후보가 원장 등재되기 전에는 인용 없이 한정 표현만):**
```latex
안에서 $u_j$ 는 오직 $\theta_{E,j}/T$ 를 뜻한다(부록 C 함정표 참조).} 대표값의 선택 --- 예컨대 산화물
양극류의 광학 포논 대역 $50$--$80$~meV $\to\theta_{E,j}\approx580$--$930$~K(자릿수 예시 --- 본 파트가
값으로 쓰지 않는 무인용 환산 연습) --- 은 \emph{단위 환산 예시일 뿐}이며, 실제로는 대상 호스트(본 장은
흑연)의 실측 포논$\cdot$제일원리 포논 DOS \cite{jpcc2021} 로 교체하거나 다온도 곡률에서 직접
회귀한다[데이터-주도 1순위].
```
(서치 §4 의 후보 중 사용자가 채택·원장 등재하는 문헌이 생기면 "산화물 양극류" 대신 구체 호스트+\cite 로 승급 — V1 키 전용 규칙(D22) 준수.)

**근거:** 본서 서지 규율(원장 V1 키 전용·수치 주장에 근거 병기)에 비해 50–80 meV 는 무인용 수치 — "예시일 뿐" 이라도 특정 물질(LiCoO$_2$)+정량 범위를 단정. 그리고 이 절은 흑연 81p 빌드 Part T 소속 — 이어지는 \cite{jpcc2021}(Haruyama 등, JPCC 125, 27891, 2021 — 흑연 제일원리 진동·배치 분해, 원장 [abstract tier])이 흑연 쪽이므로 "대상 호스트(본 장은 흑연)" 명시가 정합. 검증 후보 문헌은 §4 서치 절.

### A13-L2 — "$\bar x$ 무차원이라 $Q$ 배" (sec05:83–85)

**현행 축자(sec05:83–85):**
```latex
\textbf{계단이 아니라 연속 블렌드}다(그림~\ref{fig:blend}). 가중 분모 $\sum Q_jg_j$ 가 정확히 측정
$dQ/dV$($=Q\,\partial\bar x/\partial U$; $\bar x$ 무차원이라 $Q$ 배)이므로, 비중은 ``그 SOC 에서 어느 봉우리가
활성인가''를 그대로 읽는다.
```

**제안(괄호부 대체):**
```latex
\textbf{계단이 아니라 연속 블렌드}다(그림~\ref{fig:blend}). 가중 분모 $\sum Q_jg_j$ 가 정확히 측정
$dQ/dV$ 다 --- 음함수~\eqref{eq:implicit} 양변을 $U$ 로 미분하면 $\sum_jQ_j\,\partial\xi_j/\partial U
=Q\,\partial\bar x/\partial U$, 좌변이 $\sum_jQ_jg_j$ 그대로다. 따라서 비중은 ``그 SOC 에서 어느 봉우리가
활성인가''를 그대로 읽는다.
```

### A13-L3 — 0.18(그리드) vs 0.21(해석) 관계 (sec05:97–100)

**현행 축자(sec05:97–100):**
```latex
config 항만큼 체계적으로 빗나간다(단순식 절대오차 최대 $0.18$ mV/K). 그 config 항 자체의 부호 있는 크기는
구간에 따라 $[-0.21,+0.14]$ mV/K 범위다. 그리드 실측 최대값 $0.18$ 은 극값을 정확히 샘플하지 않은 결과로,
해석 상한은 $0.21$ 이다.
```

**제안(마지막 문장 대체):**
```latex
config 항만큼 체계적으로 빗나간다(단순식 절대오차 최대 $0.18$ mV/K). 그 config 항 자체의 부호 있는 크기는
구간에 따라 $[-0.21,+0.14]$ mV/K 범위다. 두 수는 \emph{같은 양}(완전식$-$단순식 $=$ 가중 config 항)의 두
샘플링이다 --- $0.18$ 은 175 점 그리드 위의 최대, $0.21$ 은 그리드 점 \emph{사이}의 해석 극값이라 그리드가
극값을 정확히 샘플하지 않은 만큼 작게 읽힌 것이다.
```

### A13-L6 — $a_j$/$z_j$ 기호 중복 (sec05:45–47)

**현행 축자(sec05:44–47):**
```latex
폭 $w_j(T)=n_jRT/F$ 의 명시적 온도 의존이다. $\xi_j$ 가 logistic 인자 $a_j=(U-U_j(T))/w_j(T)$ 의 함수이고
$\partial\xi_j/\partial a_j=g_j w_j$, $\partial w_j/\partial T=n_jR/F$ 임을 쓰면($z_j\equiv(U-U_j)/w_j=\ln[\xi_j/
(1-\xi_j)]$), 연쇄율로
```

**제안(대체 — 기호 하나로):**
```latex
폭 $w_j(T)=n_jRT/F$ 의 명시적 온도 의존이다. $\xi_j$ 가 logistic 인자 $z_j\equiv(U-U_j(T))/w_j(T)
=\ln[\xi_j/(1-\xi_j)]$ 하나의 함수이고 $\partial\xi_j/\partial z_j=g_jw_j$,
$\partial z_j/\partial T\big|_U=-\bigl[\partial U_j/\partial T+z_j\,\partial w_j/\partial T\bigr]/w_j$,
$\partial w_j/\partial T=n_jR/F$ 임을 쓰면, 연쇄율로
```

### A13-L7 — $\Delta U_\vib$ 완전 전개형 병기 (sec04:82–88 직후)

**현행 축자(sec04:82–88):**
```latex
\begin{equation}
\boxed{\;
\Delta U_\vib(T)=-\frac1F\Bigl[\Delta F_\vib(T)-\Delta F_\vib(T_\mathrm{ref})+S_\vib(T_\mathrm{ref})\,(T-T_\mathrm{ref})\Bigr],
\qquad
\frac{\partial\,\Delta U_\vib}{\partial T}=\frac{\Delta S_\vib(T)}{F}\;}
\label{eq:dUvib}
\end{equation}
```

**제안(박스 유지 + 직후 전개형 1식 병기, 제안 라벨 `eq:dUvib-explicit`):**
```latex
구현용으로 전부 풀어 쓰면(부록 D 의 회귀 기준 평가식)
\begin{equation}
\Delta U_\vib(T)=-\frac{R}{F}\Bigl[T\ln\bigl(1-e^{-\theta_{E,j}/T}\bigr)
-T_\mathrm{ref}\ln\bigl(1-e^{-\theta_{E,j}/T_\mathrm{ref}}\bigr)\Bigr]
-\frac{S_\vib(T_\mathrm{ref};\theta_{E,j})}{F}\,(T-T_\mathrm{ref})
\tag{제안 eq:dUvib-explicit}
\end{equation}
이다($S_\vib$ 는 닫힌형~\eqref{eq:Svib-einstein}).
```

**근거(재계산):** $\theta_E{=}700$ K·$T{=}348.15$ K: $-\tfrac RF[348.15\ln(0.866095)-298.15\ln(0.904423)]-\tfrac{0.348548R}{F}\cdot50=+0.230$ mV — 적분 사다리꼴 근사($\tfrac12(0+9.14)\,\mu$V/K$\times50$ K$=0.229$ mV)와 정합.

### A13-L8 — 파생 C 이중지위 요약표 병기 (sec05:161–186)

**현행 축자(sec05:163–164 — 도입부):**
```latex
것은 전이 종류이며, 이 \emph{이중지위}가 본 절의 전부다.
```

**제안(불릿 뒤 요약표 추가 — 불릿 무삭제; 제안 라벨 `tab:wstatus`):**
```latex
\begin{table}[t]
\centering\small
\caption{폭 $w_j$ 의 이중지위 요약(파생 C). 판정 근거·상세는 본문 불릿과 \S\ref{sec:broadening}.}
\label{tab:wstatus}
\begin{tabular}{l l l l}
\toprule
전이 유형 & 판정 근거 & $w_j$ 의 지위 & $T$-의존 서식 \\
\midrule
단상($\Omega\le2RT$) & 평형 등온선 단조 & 평형이 \emph{예측}(검증 가능) & $n_jRT/F$(이상 극한 $RT/F$) \\
두-상($\Omega>2RT$) & 실측 plateau$\cdot$상평형 \cite{dahn1991,ohzuku1993} & broadening 이 정하는 \emph{자유 피팅 폭} & 다온도 round-trip 확정 대상(\S\ref{sec:method}) \\
\bottomrule
\end{tabular}
\end{table}
```

---

## 3. 등급별 정리

### H (3건) — 논리/물리 오류·오귀속
| ID | 한 줄 |
|----|-------|
| A13-H1 | 흡수 상수를 고전 코너값으로 오지시(닫힌형이 정답 — 자체 캡션과 상충, 2.4배 차) |
| A13-H2 | 단일모드 접기의 암묵 전제(알짜 +1 모드·진폭 R) 미명시 → 고전 극한 편차 최대화(§2.3 전제와 역순)·$\partial_T\Delta S_\vib>0$ 부호 강직(경화형 잔여 표현 불가) |
| A13-H3 | vib/electronic 식별 근거의 절반("강제 영점")이 오귀속 — 규약상 두 잔여 공유, 식별력은 곡률뿐(3점 결론 자체는 옳음) |

### M (7건) — 의미·이해 실질 개선
| ID | 한 줄 |
|----|-------|
| A13-M1 | 곡률 신호 0.06–0.08 μV/K 정량 부재 + "준양자 창($T\sim\theta_E$) 걸치는" 문구 실현 불가 독해 |
| A13-M2 | "단순 곱" 선행사 부재 — 여분 항($C_E/F$) 명시로 round-trip 동기 완결 |
| A13-M3 | 그림 (a) 파선 (1.600, 1.4574) → 1.4700 (캡션의 "식 그대로 수치" 주장 위반 1점) |
| A13-M4 | eq:hys_branch 의 $\partial_T\Delta U^\hys{=}0$ 전제 미명시 + 분기 단독 측정 바이어스 $\mp0.15$ mV/K 급과 평균의 소거 |
| A13-M5 | "평균이 $\Delta S_{\rxn,j}/F$ 로" 대상 부정확(블렌드가 정답) + "config 곡률" 명명 혼동 + 짝수성 근거 부재 |
| A13-M6 | 분기식에서 config 항 침묵 탈락 — 균일 gap 시 $z_j^{(d)}$ 불변 한 문장으로 닫힘 |
| A13-M7 | LCO 50–80 meV 무인용 + 흑연 빌드 맥락 부정합(jpcc2021 은 흑연 논문) |

### L (8건) — 문체·수식화
A13-L1(자산 주석 부록B→D 잔존) · A13-L2($Q$ 배 괄호 재서술) · A13-L3(0.18/0.21 관계 명시) · A13-L4($\partial\Omega/\partial T$ "소수" 단정→가정, §2.9 공백(3) 어조 정합) · A13-L5($\Delta S_\vib$ $j$-의존 주석) · A13-L6($a_j$/$z_j$ 중복 기호 통일) · A13-L7($\Delta U_\vib$ 전개형 병기) · A13-L8(파생 C 요약표 병기)

---

## 4. §서치 — 문헌 후보 (haiku 서브에이전트 위임)

- 위임 범위: (1) LiCoO$_2$ 광학 포논 50–80 meV 지지 1차 문헌, (2) Li-graphite(LiC$_6$/LiC$_{12}$) 진동/포논 에너지 스케일 1차 문헌, (3) 삽입 엔트로피의 진동 기여를 Einstein/포논 계산으로 다룬 선행(존재 확인·DOI 실검증분만).
- 규율: 기억 서지 금지·Crossref/출판사 실조회 검증분만 후보 표로. **상태: 서브에이전트 실행 중 — 결과 도착 시 본 절 갱신.**
- 용도: A13-M7 제안의 승급 경로(후보 → 사용자 검토 → 원장 V1 등재 → 그때 \cite). 후보가 확보되지 않으면 A13-M7 의 무인용-한정 표현안이 그대로 유효.

---

## 5. 재계산 기록 (검증 완료분 — 무발견 축의 근거)

**§2.4 수치 — 전부 재계산으로 확인:**
- θ_E 환산: 1 meV = 11.6045 K → 50–80 meV = 580.2–928.4 K ("580–930 K" ✓), 700 K = 60.3 meV ("≈60 meV" ✓)
- (c) 대수 항등식: $(1+n)\ln(1+n)-n\ln n = -\ln(1-e^{-u})+u/(e^u-1)$ — $n=1/(e^u-1)$ 대입 전개로 항등 확인 ✓ ("새 근사가 아니다" ✓)
- 고전극한 전개: $-\ln(1-e^{-u})=-\ln u+u/2-u^2/24+\cdots$, $u/(e^u-1)=1-u/2+u^2/12-\cdots$ → $u/2$ 상쇄 ✓ → $R[1+\ln(T/\theta_E)]$ ✓; 저온 $S\to0$ ✓
- $S_\vib/R(700,298.15)=0.34855$ → 그림 (a) 작동점 (0.426, 0.3486)·라벨 0.35 ✓
- $\partial\Delta U_\vib/\partial T$: 278.15/298.15/318.15/348.15 K → $-3.736/0/+3.702/+9.139$ μV/K = 본문 "−3.74/0/+3.70/+9.14" ✓
- 그림 (b) 스팟체크 6점: θ500@258.15→−9.531(수록 −9.530✓)·θ500@303.15→+1.144✓·θ500@348.15→+10.966(수록 10.967✓)·θ700@303.15→+0.931(수록 0.930✓)·θ900@278.15→−2.808✓·θ900@358.15→+8.693(수록 8.694✓)
- 그림 (a) 실선 스팟체크 10점(0.080/0.120/0.160/0.200/0.240/0.400/0.440/0.840/1.000/1.560/1.600) 전부 ✓; 파선 전점 ✓ — 유일 예외 (1.600,1.4574) [A13-M3]
- eq:dUvib 유도: $S=-\partial_T\Delta F_\vib$ 성립(직접 미분 ✓)·정적분 닫힘 ✓·$\partial_T\Delta U_\vib=\Delta S_\vib/F$ ✓·$\Delta F_\vib(T{\to}0){\to}0$ ✓
- Gibbs–Helmholtz 정확성: $\mathrm d\Delta G/\mathrm dT=\Delta C_p-\Delta S-T(\Delta C_p/T)=-\Delta S$ — Kirchhoff 상쇄 근사 없음 ✓ (Bernardi 관계 서술 ✓)
- 하위호환 서술 ↔ 부록 D.3(ch2_appB:61–64) 축자 정합 ✓; "부록 C 함정표" ↔ ch2_appA(θ/θ_E·u_j/x·u_j/Ch1 u_j·F_vib/F·ΔS_vib(T)/∂S_vib/∂x 5항목 존재) ✓; sec:hys spinodal $u_j=\sqrt{1-2RT/\Omega_j}$ ↔ fig:hysgap 캡션 ✓

**§2.5 수식 — 전부 재유도로 확인:**
- eq:implicit ↔ Part 0 eq:sm-mc-balance **글자까지 동일** ✓; 유일근 요동 증명 $\partial\langle N\rangle/\partial\mu=\beta\,\mathrm{var}(N)>0$ = eq:sm-mc-fluc ✓ (평균장 이중웰 가드는 Part 0 verifybox 소관 — 인용 구조 정합)
- eq:implicit_diff 음함수 미분 ✓; eq:gj: logistic $\mathrm d\xi/\mathrm da=\xi(1-\xi)$·$\partial a/\partial U=1/w$ ✓ (ξ 는 $U$ 에 증가 — §2.1 eq:logistic 정합 ✓)
- eq:dxidT: $\partial a/\partial T=-[\partial_TU_j+z\,\partial_Tw]/w$, $\partial_Tw=n_jR/F$ → 두 조각 ✓; $z=a=\ln[\xi/(1-\xi)]$ ✓
- eq:dwdT-nT 곱미분 ✓ ($n_j$ 상수 환원 ✓); eq:weighted 첫 조각 대입 ✓; 완전식 = 가중평균 내부 $+n_jRz_j/F$ ✓ = §2.8 eq:complete ✓
- eq:single_config 부호: $V=U_j+(RT/F)\ln[\xi/(1-\xi)]$ (eq:Vxi) → $\partial_TV|_\xi=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$ = §2.2 eq:dVdT_config ✓; $\partial S_\config/\partial\theta|_{\theta=1-\xi}=+R\ln[\xi/(1-\xi)]$ ✓
- config 스케일: $R/F=0.08617$ mV/K; $|0.21|$ mV/K ⇔ $\xi\approx0.92$(그리드 끝) 자연 ✓; "양끝 폭 0.35"=0.21+0.14 ✓; "~0.3 mV/K 급" 대표 규모 ✓
- $2RT$@298.15 K $=4957.6$ J/mol ("≈4957" ✓); 네 전이 $\Omega$ 초기값(6000–13000) 모두 초과 — §1.7 동일 한정 ✓
- tab:ds $+29/0/-5/-16$ (리튬화 방향 라벨) → 탈리튬화 진행 순 $-16\to-5\to0\to+29$ "상승" — fig:blend 캡션 ✓
- 파생 C 세 출처 ↔ §1.7 broadening ①②③(유한율속 꼬리·내재 $RT/F$·비-크기 앙상블 $\rho(U_\app)$)·역산 금지 ✓; $w_{\eff}(\Omega)$ 재도입 금지 ↔ [C-2] ✓
- 파생 D 부호: eq:Ubranch($\sigma_d{=}+1$ 방전=탈리튬화 가지 위) ↔ "dis 가 $+\tfrac12$(위 가지)" ✓; $\gamma_jh_{\eta,j}{=}1$ 특수형 명시 ✓; 평균의 짝수성 → 보정 $O(\delta^2)$ — "1차까지" 서술과 정합 ✓
- 인용 키 8종(numverif2026·dahn1991·ohzuku1993·hysteresis2018·jpcc2021 등) 전부 ch1v22_bib 존재 ✓ (원장 승계 구조 확인)

---

## 6. 말미 4-tier + 무발견 축

**[확정] (재계산·원문 축자 대조로 확정)**
- A13-H1 의 수치 대비(0.349R vs 0.146R)와 본문↔캡션 불일치; A13-H3 의 근거(§2.2 warnbox 흡수 규약 축자); A13-M3 그림 점 오류(1.4574=1+ln 1.58); A13-M1 의 곡률 이탈 수치(+0.057/+0.081 μV/K); A13-M4 의 유도 전제(식 형태상 $\partial_T\Delta U^\hys=0$ 필요)와 fig:hysgap 좌표 기반 기울기(−0.3045 mV/K); A13-M5 의 블렌드-극한 대상; A13-M6 의 균일 gap $z$-불변; A13-L1 부록 문자(마스터 입력 순서로 D 확정); §5 재계산 기록 전부.

**[추정] (논증은 완결이나 문서 의도 해석 포함)**
- A13-H2 의 물리 프레임(모드 수 균형이 §2.3 "고전=상수 흡수" 의 근거라는 재구성 — 표준 열역학 논증이며 수치 시연은 가상 파라미터 명시): 단일모드 폼의 수학적 성질(고전 극한 편차 최대·기울기 양수)은 [확정], "따라서 스코프 문장이 필요하다" 는 판단은 [추정-강]. A13-M4 의 실측 함의(분기 단독 측정 바이어스)는 gap 의 실제 $T$-의존이 spinodal 닫힌 꼴을 따를 때의 스케일 추정.

**[미검증]**
- LiCoO$_2$ 광학 포논이 실제로 50–80 meV 대역인지(무인용 원문 수치 — §4 서치로 후보 확보 시도 중; 본 검토는 환산 산술만 검증). haiku 서브에이전트 결과 도착 전까지 §4 는 잠정.
- numverif2026 의 175점 수치 자체(내부 자료 — 본 검토는 스케일 정합성만 교차 확인, 원 코드 재실행은 범위 밖).

**[무발견 축] (검토했으나 문제 없음)**
- **수식 대수 전체**: eq:Svib-einstein·eq:dSvib·eq:dUvib·eq:implicit·eq:implicit_diff·eq:gj·eq:dxidT·eq:dwdT-nT·eq:weighted·eq:single_config·eq:hys_branch(동결 전제 하)·eq:hys_rev — 재유도 전부 통과, 부호 오류 없음.
- **수치 전체**(그림 (a) 파선 1점 제외): 본문 4수치·그림 (b) 3곡선·환산·상수(2RT=4957) 전부 일치.
- **교차 정합**: §2.4↔§2.3(편차 vs 부분몰 구분 — 절 전체에서 유지)·§2.4↔부록 C/D·§2.5↔Part 0(음함수 축자 동일·요동 증명)·§2.5↔§2.2(config 부호·이중계산 분리)·§2.5↔§1.7(broadening 세 출처·재도입 금지)·§2.5↔§1.4(분기 부호)·§2.5↔§2.8(완전식 전달)·좌표 규약($\bar x$·$\xi$·$s{=}+1$) — 충돌 없음.
- **P3-7(명칭)**: 두 파일 내 ver.N/Chapter 혼동 없음; P3-2(전하 보존 중심식): §2.5 는 보존식을 중심식으로 유지(OCV 읽기 회귀 없음) ✓; P3-3(순환 의존): 음함수 지위를 Part 0 "정의상 implicit formulation" 으로 명시 — 정합 ✓.
- **GS 공백 존중**: §2.9 공백 (1)–(5)를 메우는 제안 없음(A13-L4 는 어조 정합만); bgbox 증축분(§2.7)의 독립성 건드리는 제안 없음; 기존 자산·수식 삭제 제안 0건(전부 대체·보강·병기).
