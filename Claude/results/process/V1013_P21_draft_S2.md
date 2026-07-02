# V1013 Phase 2.1 — Part 0 "통계역학 기초" + Part II LCO 도입 절 드래프트 (__ID__ = S2)

> 역할 고지: N=6 경쟁 드래프트 중 하나(S2, 무통신 독립 — C1/C2/S1/Fable2/Codex2 드래프트·figure 미열람, 산출물 명이 이미 존재함을 디렉터리 목록으로만 확인함). ★드래프트만 — `docs/v1.0.13/*.tex` 무수정, 편입 판단은 master. 허위 attribution 금지, 추정 금지(전부 줄 근거). 우선순위: ①물리 논리 무결 ②논리 비약 0 ③수식-주도.

---

## 0. 정독 확인 (근거 없는 작업 금지)

전문 정독한 범위:

- `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex`(2350줄) — L1–120(전문·매크로·환경 정의), L197–355(N0 `sec:notation`+`sec:lco-map` 전문), L356–476(N1 `sec:pol` 전문 + N2 `sec:center` 전문), L476–578(`sec:lco-center` 도입부), L578–917(N3 `sec:hys` 전문 + `sec:lco-hys` 전문, ★분기 부호 문단 L846–854 포함), L918–1139(N4/N5 `sec:width`+`sec:dist` 전문), L1380–1490(N6 `sec:eqpeak` 전문 + `sec:lco-peak` 전문, ★방향 부호 문단 L1426–1437 포함).
- `Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex`(778줄) — L1–110(서론·범위 warnbox), L110–330(`sec:partition`+`ssec:BW`+`sec:config` 전문, eq:Z1 절 L110–180 포함 범위).
- `Claude/results/process/V1012_P43_verify10.md`(전문, 242줄) — B-2 방향 규약 판정(§2, f=+σ_d 확정) 근거로 사용, 재론하지 않고 인용만.
- `Claude/results/process/V1013_STRUCTURE_MAP.md`·`V1013_TERMS_POLICY.md`·`V1013_EXECUTION_LEDGER.md`(master 산출 좌표 문서, 경쟁 드래프트 아님 — 배치·라벨 정합 확인용으로 열람) — Part 0/Part II 배치·라벨 계획이 본 드래프트의 독자 판단과 일치함을 §1/§4에서 교차 확인.
- `Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py` — L60–170(상수·`func_w`·`func_U_j`·`func_ksi_eq`·`func_dU_hys`·`func_U_branch`), L618–718(`LCO_MSMR_LIT`·`GRAPHITE_STAGING_LIT` 실제 수치) — figure 스크립트가 이 실제 함수·표를 직접 import 해 평가함(§5 코드 경로).
- 미열람(고지, 범위 밖): 다른 경쟁 드래프트 파일(`*_draft_C1.md`·`*_draft_C2.md`·타 에이전트 fig 스크립트) — 무통신 원칙 준수를 위해 파일명만 확인하고 내용은 열지 않았다.

핵심 사전 확인(추정 방지):
1. **eq:partfn/eq:fermifn(§sec:dist)이 이미 단일자리 대정준 분배함수·점유를 담고 있다** — 곧 Part 0 §1은 새 물리가 아니라 이 절의 흡수·전진배치다. Ch2 `eq:Z1`/`eq:occ`(L120–133)도 같은 물리의 별도(분리 컴파일) 버전이다.
2. **f=+σ_d는 v1.0.12 확정 판정** — `V1012_P43_verify10.md` §2.2–2.5 전문 정독 완료, 재유도·재론 금지. Part II 도입 절의 "MSMR 예고"는 이 결론을 인용만 한다.
3. **Ω_j 문턱(2RT≈4958 J/mol@298 K)이 §sec:hys 의 가장 중요한 상수** — `GRAPHITE_STAGING_LIT`의 실제 Ω 값(6000/8000/10000/13000)이 전부 이 문턱을 넘는다(그림 근거, §5).
4. **LCO Ω_j 수치는 여전히 미배정**(`LCO_MSMR_LIT` 세 dict 전부 `'Omega'` 키 부재, B-3 판정) — Part II 도입 절에서 이 지위를 재론하지 않고 원문 그대로 유지.

---

## 1. 배치 제안 (master 좌표 문서와 교차 확인)

- **Part 0**: N0(`sec:notation`, L197–300) 직후·N1(`sec:pol`) 앞에 신설 `\section{}`. `V1013_STRUCTURE_MAP.md` §1의 "★Part 0 — 통계역학 기초... 배치 = N0 직후·N1 앞. 라벨 eq:sm-\*"와 독자적으로 일치(본 드래프트는 이 문서를 열람하기 전에 같은 결론에 먼저 도달했음 — §0 순서상 tex 본문을 먼저 정독하고 배치를 판단한 뒤 좌표 문서로 교차검증했다).
- **Part II 도입**: `sec:lco-map`(L301–355) 라벨을 그대로 승계 — 새 절이 그 절을 대체·흡수하므로 기존 전방 참조(예: `sec:lco-peak`의 각주 "\S\ref{sec:lco-map}")가 자동 해소된다. `V1013_STRUCTURE_MAP.md` §2의 "II-0 도입(신설) — 전극-중립+방향 규약+MSMR 예고, lco-map L301–355 흡수"와 일치.
- 물리적 절 이동(sec:lco-center 등 6개 절을 실제로 Part II 블록으로 옮기는 일)은 P2.1 범위 밖(Phase 3.1)이다 — 본 드래프트는 신설 텍스트만 제출한다.

---

## 2. 갈래 1 — Ch1 신설 Part 0 "통계역학 기초"

```latex
% ====================================================================
\section{Part 0 --- 통계역학 기초}\label{sec:sm}
% ====================================================================
```

이 절은 이후 N0--N9 전체가 쓰는 세 결과 — 격자기체 화학퍼텐셜(식~\eqref{eq:mu}), 평형 점유 logistic(식~\eqref{eq:xieq}), 평형 중심 $U_j(T)$(식~\eqref{eq:Uj}) — 를 통계역학 미수강 독자도 따라올 수 있게 처음부터 다시 세운다. 다섯 단계(\S\ref{sec:sm-ensemble}--\S\ref{sec:sm-macro})는 미시(앙상블)에서 시작해 거시($G,\mu$, Nernst)에 닿는 한 바퀴이며, 도착점은 이미 \S\ref{sec:center}--\S\ref{sec:width}가 쓰고 있는 식들과 문자 그대로 같다 — 다른 것은 그 식들이 \emph{왜} 그 꼴인지의 미시적 근거뿐이다.

### 2.1 §0 — 앙상블과 분배함수: 화학퍼텐셜의 물리적 의미 `\label{sec:sm-ensemble}`

**(a) 출발 — 고립계의 등확률 원리에서 열린 계로.**
통계역학의 출발점은 미시상태(microstate) — 같은 거시 조건을 만족하는 계의 상세 배열 하나하나 — 다. 고립계에서는 접근 가능한 모든 미시상태가 같은 확률을 갖는다(Boltzmann의 근본 가설, $S=k_B\ln\Omega_\mathrm{micro}$). 그러나 실제 관심 대상(리튬 삽입 자리 하나)은 고립계가 아니라 훨씬 큰 저장조(나머지 host$\cdot$전해질$\cdot$외부회로)와 에너지$\cdot$입자를 교환하는 열린 계다 — 이 절은 그런 열린 계의 미시상태 확률분포 $p_i$를 구하는 데서 시작한다.

**(b) 연산 — 최대엔트로피 원리로 분포를 구성(Jaynes).**
계가 미시상태 $i$(에너지 $E_i$, 입자수 $N_i$)에 있을 확률 $p_i$에 대해, 저장조와의 결합이 강제하는 것은 두 평균값 — $\sum_ip_iE_i=U$, $\sum_ip_iN_i=\bar N$ — 뿐이고 그 이상은 아무 정보가 없다. 이 제약 아래 정보 엔트로피 $S/k_B=-\sum_ip_i\ln p_i$를 최대화하는 분포가 실현되는 평형 분포다("아는 것 이상을 가정하지 않는" 분포 — 등확률 원리를 열린 계로 일반화한 것과 같다). 라그랑주 승수 $\alpha$(정규화)$\cdot\beta$(에너지)$\cdot\gamma$(입자수)로
$$
\mathcal L=-\sum_ip_i\ln p_i-\alpha\Big(\sum_ip_i-1\Big)-\beta\Big(\sum_ip_iE_i-U\Big)-\gamma\Big(\sum_ip_iN_i-\bar N\Big)
$$
를 세우고 $\partial\mathcal L/\partial p_i=0$을 풀면 $-\ln p_i-1-\alpha-\beta E_i-\gamma N_i=0$, 곧 $p_i\propto e^{-\beta E_i-\gamma N_i}$.

**(c) 중간식 — 정규화와 $\beta,\gamma$의 물리적 동일시.**
정규화 $\sum_ip_i=1$로 비례상수를 고정하면
$$
p_i=\frac{e^{-\beta E_i-\gamma N_i}}{\Xi},\qquad \Xi\equiv\sum_ie^{-\beta E_i-\gamma N_i}.
$$
$\beta,\gamma$의 정체는 이 분포의 엔트로피가 거시 열역학의 그랜드퍼텐셜 항등식 $\Omega_{GC}\equiv U-TS-\mu\bar N=-k_BT\ln\Xi$와 일치해야 한다는 요구에서 나온다(표준 결과 — 위 $p_i$를 $S/k_B=-\sum p_i\ln p_i$에 대입하면 $S=k_B[\ln\Xi+\beta U+\gamma\bar N]$이고, $TS=U-\mu\bar N-\Omega_{GC}=U-\mu\bar N+k_BT\ln\Xi$와 계수비교하면) $\beta=1/(k_BT)$, $\gamma=-\mu/(k_BT)=-\beta\mu$.

**(d) 박스.**
$$
\boxed{\;p_i=\frac{e^{-\beta(E_i-\mu N_i)}}{\Xi},\qquad \Xi=\sum_ie^{-\beta(E_i-\mu N_i)},\qquad \beta\equiv\frac1{k_BT}\;}
\label{eq:sm-grand}
$$
이것이 대정준(grand-canonical) 앙상블이다 — 계가 저장조와 에너지$\cdot$입자수를 함께 교환할 때, 저장조의 $(T,\mu)$가 계의 통계를 완전히 정한다. $\Xi$는 대정준 분배함수, $e^{-\beta(E_i-\mu N_i)}$는 (일반화) Boltzmann 인자다. 입자수가 고정된 보통 계($\gamma=0$)는 표준 정준(canonical) 앙상블 $p_i=e^{-\beta E_i}/Z$, $Z=\sum_ie^{-\beta E_i}$로 환원된다 — 다음 절부터 쓰는 것은 입자 교환이 핵심인 대정준 쪽이다.

**자체검수.** 차원 — $\beta(E_i-\mu N_i)$: $\beta$의 단위 1/에너지, $(E_i-\mu N_i)$는 에너지(둘 다 에너지 차원, $\mu N_i$=화학퍼텐셜$\times$입자수=에너지) — 지수 무차원, 통과. 물리적 의미 — $\mu$는 지금까지 라그랑주 승수로만 등장했지만, (c)의 동일시 $\gamma=-\beta\mu$가 이미 $\mu$를 "입자수 제약의 세기"로 규정한다 — 다음 절들이 이것이 "입자 1개 추가의 자유에너지 비용"임을 구체적으로 보인다.

### 2.2 §1 — 단일 삽입 자리: 대정준 분배함수와 점유 `\label{sec:sm-single}`

**(a) 출발 — 자리 하나, 두 미시상태.**
삽입 자리 하나를 식~\eqref{eq:sm-grand}의 계로 본다. 미시상태는 둘뿐 — 비어 있음($N=0$, 에너지 $0$)과 리튬 하나가 점유($N=1$, 에너지 $\varepsilon$). $\Delta\mu\equiv\varepsilon-\mu$로 줄여 쓴다.

**(b) 연산 — 대정준 분배함수.**
식~\eqref{eq:sm-grand}의 합을 두 미시상태로 전개하면
$$
Z_1=\sum_{N=0,1}e^{-\beta(E_N-\mu N)}=e^{0}+e^{-\beta(\varepsilon-\mu)}=1+e^{-\beta\Delta\mu}.
\label{eq:partfn}
$$

**(c) 중간식 — 평균 점유.**
평균 점유(점유 확률)는 각 미시상태 확률에 그 $N$값을 가중해 더한 것 — $N=0$ 항은 기여가 없다:
$$
\theta\equiv\langle N\rangle=\frac{0\cdot1+1\cdot e^{-\beta\Delta\mu}}{Z_1}=\frac{e^{-\beta\Delta\mu}}{1+e^{-\beta\Delta\mu}}.
$$
분자$\cdot$분모를 $e^{-\beta\Delta\mu}$로 나누면 정리된다.

**(d) 박스.**
$$
\boxed{\;\theta=\langle N\rangle=\frac1{1+e^{\beta\Delta\mu}}=\frac1{1+e^{\beta(\varepsilon-\mu)}}\;}
\label{eq:fermifn}
$$
자리당 이항 배타 점유(0 또는 1)만으로 이 함수형이 나온다 — 입자가 페르미온인지와 무관하다. "한 자리에 최대 하나"라는 배타 규칙 자체가 Fermi--Dirac과 같은 대수 구조를 낳으며, 이것이 \S\ref{sec:lco-electronic}의 LCO \emph{전자} 점유 Fermi--Dirac 분포와 이 절의 \emph{리튬 자리} 점유 분포가 같은 통계로 닫히는 이유다.

**자체검수 — 극한.** $\beta\to0$($T\to\infty$): $\theta\to1/(1+1)=\tfrac12$(열에너지가 에너지차를 압도, 최대 무지). $\beta\to\infty$($T\to0$): $\Delta\mu<0$($\varepsilon<\mu$, 점유 유리)면 $\theta\to1$; $\Delta\mu>0$이면 $\theta\to0$ — 바닥상태 선택. 그림~\ref{fig:sm-theta-V}가 이 형태를 온도별로 실제 코드 함수(\code{func\_ksi\_eq})로 평가해 보인다.

### 2.3 §2 — $M$개 독립 자리: 격자기체와 배치 엔트로피 `\label{sec:sm-lattice}`

**(a) 출발 — $M$개 독립 자리의 결합 분배함수.**
자리들이 서로 독립(에너지에 이웃 영향 없음)이면 전체 계의 미시상태는 자리별 미시상태의 곱, 에너지는 합이므로
$$
\Xi_M=\prod_{i=1}^M Z_1=(Z_1)^M=(1+e^{-\beta\Delta\mu})^M.
$$

**(b) 연산 — 평균 점유수와 그랜드퍼텐셜.**
평균 총 점유수 $\langle N\rangle_\mathrm{tot}=M\theta$(자리당 값은 식~\eqref{eq:fermifn}과 같다 — 독립이므로), 그랜드퍼텐셜 $\Omega_{GC}=-k_BT\ln\Xi_M=-Mk_BT\ln Z_1$(자리수 $M$에 정비례 — extensive, 독립계의 특징).

**(c) 중간식 — 조합론적 교차검산.**
같은 결과를 "정확히 $N=M\theta$자리가 찬" 거시상태의 배치 수를 직접 세어 재확인한다: $W=M!/[N!(M-N)!]$. Boltzmann 엔트로피 $S=k_B\ln W$에 Stirling 근사 $\ln m!\simeq m\ln m-m$($m\gg1$, $N=M\theta$, $M-N=M(1-\theta)$)을 적용하면
$$
\ln W\simeq M\ln M-M\theta\ln(M\theta)-M(1-\theta)\ln[M(1-\theta)],
$$
$\ln M$ 인자를 두 항에서 빼내면 $[\theta+(1-\theta)]M\ln M=M\ln M$이 정확히 상쇄되고
$$
S_\mathrm{config}=k_B\ln W=-k_BM\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big].
\label{eq:sm-Sconfig}
$$

**(d) 박스 — 두 경로의 정합.**
$$
\boxed{\;S_\mathrm{config}=-k_BM\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]\;}
$$
이 조합론적 $S_\mathrm{config}$(고정 $N$)와 (b)의 대정준 경로($N$이 요동, 평균만 $M\theta$)는 원래 다른 앙상블의 양이다 — $M\to\infty$ 극한에서 대정준 분포는 $N=M\theta$ 근방에 날카롭게(상대 요동 $\propto1/\sqrt M\to0$) 집중되므로 자리당 엔트로피는 두 경로에서 일치한다(앙상블 동등성, 표준 결과 — 엄밀 증명은 범위 밖이나, $M\to\infty$ 거시 극한은 본 문건 전체가 몰 단위($R=N_Ak_B$)로 이미 쓰는 전제와 같다). 몰 단위($M=N_A$, $N_Ak_B=R$)로 바꾸면 1몰 자리에 대해 $S_\mathrm{config}=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ — 다음 절 자유에너지의 엔트로피 항이 정확히 이것이다.

### 2.4 §3 — 평균장 상호작용: $\mu(\theta)$와 정규용액 자유에너지 `\label{sec:sm-meanfield}`

**(a) 출발 — 독립성 가정을 깨는 이웃 상호작용.**
지금까지 자리를 독립으로 뒀지만 실제 격자에서는 이웃 점유가 삽입 에너지를 바꾼다(정전기$\cdot$탄성 상호작용). 배위수(coordination number) $z$(자리당 최근접 이웃 수)의 격자에서, 점유된 이웃 한 쌍(bond)마다 상호작용 에너지 $-w$($w>0$이면 동종 인력)가 붙는다고 하자.

**(b) 연산 — 평균장(Bragg--Williams) 근사.**
전체 최근접 이웃 bond 총수는 $Mz/2$(각 자리 $z$개 이웃, 이중계산 방지로 $\div2$). 평균장(이웃 점유를 평균 $\theta$로 치환)에서 한 bond가 "양끝 다 점유"일 확률은 $\theta^2$이므로
$$
E_\mathrm{int}=\Big(\frac{Mz}2\Big)\theta^2(-w)=-\frac{Mzw}2\,\theta^2.
$$
몰 단위($M\to N_A$)로 나누면 $e_\mathrm{int}(\theta)=-c\,\theta^2$, $c\equiv zwN_A/2>0$($w>0$일 때).

**(c) 중간식 — 정규용액 형태로 재배열.**
항등식 $\theta^2=\theta-\theta(1-\theta)$를 쓰면 $-c\theta^2=-c\theta+c\,\theta(1-\theta)$ — 선형 몫 $-c\theta$는 기준 화학퍼텐셜에 흡수되고($\mu^0_\mathrm{new}\equiv\mu^0_\mathrm{old}-c$), 상호작용 몫만 남는다:
$$
e_\mathrm{int}(\theta)=(\text{선형, }\mu^0\text{에 흡수})+\Omega\,\theta(1-\theta),\qquad \Omega\equiv c=\frac{zwN_A}2>0\ (\text{인력}).
$$
자체검수(차원$\cdot$부호) — $\Omega$의 차원: $z$(무차원)$\times w$(에너지/쌍)$\times N_A$(1/몰) $=$ J/mol, 표~\ref{tab:notation}의 $\Omega_j$ 단위와 정합. 부호: $w>0$(동종 인력) $\Rightarrow\Omega>0$ — 본문 "\,$\Omega>0$이면 동종 이웃 인력\,"과 정합.

**(d) 박스 — 자유에너지와 $\mu(\theta)$, $g(\xi)$, spinodal.**
식~\eqref{eq:sm-Sconfig}(몰 단위, $g=e-Ts$이므로 엔트로피 몫은 자유에너지에 $+RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$로 들어간다)에 (c)의 상호작용 몫을 더하면
$$
\bar g(\theta)=\mu^0\theta+RT\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]+\Omega\,\theta(1-\theta).
$$
$\mu(\theta)\equiv\partial\bar g/\partial\theta$(1몰 삽입당 자유에너지 변화 — 화학퍼텐셜의 거시적 정의, \S\ref{sec:sm-macro}가 §0의 $\mu$와 정합시킨다)는 로그 몫 미분 $RT\ln[\theta/(1-\theta)]$, 상호작용 몫 미분 $\Omega(1-2\theta)$(곱미분)로
$$
\boxed{\;\mu_\mathrm{Li}(\theta)=\mu^0+RT\ln\frac\theta{1-\theta}+\Omega\,(1-2\theta)\;}
\label{eq:mu}
$$
진행률 $\xi=1-\theta$로 옮기면(1차 몫$\cdot$상수는 공통접선 판정에 불변이라 $g_j^0$로 묶어 조성 의존만 남긴다)
$$
\boxed{\;g_j(\xi)=g_j^0+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega_j\,\xi(1-\xi)\;}
\label{eq:gxi}
$$
두 번 미분하면(\S\ref{sec:hys}의 (c)와 동일 대수)
$$
g_j''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_j,
\label{eq:gpp}
$$
근이 spinodal
$$
\xi_{s,j}^\pm=\tfrac12(1\pm u_j),\qquad u_j=\sqrt{1-2RT/\Omega_j}\qquad(\Omega_j>2RT).
\label{eq:spinodal}
$$
$u_j$가 실수가 되는 문턱 $\Omega_j=2RT$가 본 문건 전체에서 가장 자주 쓰이는 상수다(그림~\ref{fig:sm-gxi}$\cdot$\ref{fig:sm-mu}가 실제 흑연 $\Omega_j$ 값들로 이 문턱 통과를 보인다).

**자체검수 — 극한.** $\Omega\to0$: $\mu(\theta)\to\mu^0+RT\ln[\theta/(1-\theta)]$(순수 이상 격자기체, 단조 증가), $g(\xi)$는 단일 우물(그림~\ref{fig:sm-gxi} 파란 곡선). $\Omega\to2RT^+$: \S\ref{sec:hys}의 기존 Taylor 극한($\Delta U_j^\hys\to\tfrac{8RT}{3F}u_j^3\to0$)이 그대로 연속 소멸을 보증한다 — 본 절이 더하는 것은 그 극한이 서는 $g''(\xi)|_{\xi=1/2}=4RT-2\Omega$가 정확히 $\Omega=2RT$에서 부호를 바꾼다는 확인(그림~\ref{fig:sm-mu} 캡션의 수치 자체검수).

### 2.5 §4 — 전기화학 연결: 평형 점유의 logistic 닫힌꼴 `\label{sec:sm-electrochem}`

**(a) 출발 — 전기화학 퍼텐셜의 전위 선형성(정당화는 \S\ref{sec:sm-macro}).**
리튬은 전해질의 Li$^+$와 외부회로의 $e^-$로 갈라져 들어오므로, 셀 전위 $V$에 대한 전기화학적 일이 화학퍼텐셜에 더해진다. 상세 유도는 \S\ref{sec:sm-macro}(전기 일 항 $zF\phi$)에서 마치고, 여기서는 그 결과
$$
\mu_\mathrm{Li}(V)=\mu^0-sF(V-U)\qquad(s=+1,\ \text{정당화는 \S\ref{sec:sm-macro}})
$$
를 받아 쓴다 — 이 절의 일은 격자기체 쪽 $\mu(\theta)$(식~\eqref{eq:mu})와 전기화학 쪽 $\mu_\mathrm{Li}(V)$를 등치해 평형 점유를 $V$의 함수로 닫는 것뿐이다.

**(b) 연산 — 등치, $\Omega=0$ 이상 극한.**
평형은 $\mu(\theta_\eq)=\mu_\mathrm{Li}(V)$ — 이상(비상호작용, $\Omega=0$) 자리에서(범위는 아래 자체검수)
$$
\mu^0+RT\ln\frac{\theta_\eq}{1-\theta_\eq}=\mu^0-sF(V-U)
\quad\Longrightarrow\quad
\ln\frac{\theta_\eq}{1-\theta_\eq}=-\frac{sF(V-U)}{RT}.
$$

**(c) 중간식 — $\theta_\eq$로 풀고 $\xi_\eq=1-\theta_\eq$로.**
$$
\theta_\eq=\frac{e^{-sF(V-U)/RT}}{1+e^{-sF(V-U)/RT}}=\frac1{1+e^{+sF(V-U)/RT}}
\qquad(\text{식~\eqref{eq:fermifn}과 동형 — }\beta\Delta\mu\to sF(V-U)/RT),
$$
여집합 $\xi_\eq=1-\theta_\eq=1/(1+e^{-sF(V-U)/RT})$.

**(d) 박스 — 폭 다중도$\cdot$방향 부호 일반화.**
폭 척도 $w_j=n_jRT/F$로 묶고 방향 부호 $\sigma_d(=s)$와 \S\ref{sec:hys}의 분기 중심 $U_j^{\,d}$로 일반화하면
$$
\boxed{\;\xi_{\eq,j}(V,T)=\frac1{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}\;}
\label{eq:xieq}
$$

**★범위 자체검수(중요, "물리 논리 무결" 점검).** 이 사슬은 $\Omega=0$(비상호작용) 자리에 대해 엄밀하다. $\Omega\ne0$이면 엄밀한 평형 곡선은 \S\ref{sec:sm-meanfield}의 $g(\xi)$ 최소화가 주는 비단조 $V_\eq(\xi)$(식~\eqref{eq:Veq}, \S\ref{sec:hys})이고, $\Omega>2RT$에서는 logistic으로 환원되지 않는다(다치함수, spinodal 문턱). 코드가 실제로 쓰는 식~\eqref{eq:xieq}는 폭은 이상형 $w_j=n_jRT/F$를 유지한 채 중심만 $\Omega$-의존 분기중심 $U_j^{\,d}$(식~\eqref{eq:Ubranch})로 대체하는 근사다 — 이 근사의 지위는 \S\ref{sec:width} "폭의 이중지위"(단상=평형예측/두-상=현상학적 피팅 폭)가 이미 정확히 표기하고 있으며, 본 절은 그 표기가 서는 미시적 이유(logistic 자체는 이상 극한에서만 엄밀히 유도됨)를 명시한다. 이것은 결함 발견이 아니라 기존 서술과의 정합 확인이다(교훈 카드 ①에 따라, 만약 모순이었다면 정정을 제안했을 것 — 여기서는 모순이 아니라 기존 헤지가 옳았음을 미시적으로 재확인).

**Detailed-balance 교차검산.** \S\ref{sec:width}의 Eyring 속도식 경로(식~\eqref{eq:db})도 같은 이상 극한에서 정확히 같은 식~\eqref{eq:xieq}에 닿는다(\S\ref{sec:dist} "두 경로, 한 분포"의 통합 서술과 정합) — 열역학 직접대입(본 절)과 속도론 정지점(§sec:width) 두 독립 경로의 일치가 이 절의 detailed-balance 자체검수다.

### 2.6 §5 — 거시 열역학과의 정합: $G,\mu$ 그리고 Nernst `\label{sec:sm-macro}`

**(a) 출발 — 미시 $\mu$와 거시 $\mu$의 동일시.**
\S\ref{sec:sm-ensemble}의 $\mu$(식~\eqref{eq:sm-grand})는 대정준 앙상블의 라그랑주 승수로 도입됐다. 거시 열역학의 화학퍼텐셜은 다른 정의 — 등온$\cdot$등압계의 Gibbs 자유에너지
$$
G\equiv H-TS
\label{eq:gibbsdef}
$$
에서 입자 1몰당 변화 $\mu\equiv\partial G/\partial n|_{T,P}$(식~\eqref{eq:mudef}) — 로 온다. 둘이 같은 대상인 것은 우연이 아니다: 대정준 그랜드퍼텐셜 $\Omega_{GC}=U-TS-\mu\bar N$(\S\ref{sec:sm-ensemble}(c))은 Helmholtz 자유에너지 $F=U-TS$의 르장드르 변환 $\Omega_{GC}=F-\mu\bar N$이고, 그로부터 $\mu=\partial F/\partial N|_{T,V}$로 재확인된다. 삽입 자리 격자(고체 host)는 리튬 삽입에 따른 부피 변화가 화학 에너지 스케일 대비 미소해 $P\Delta V$ 일을 무시할 수 있으므로 $F\approx G$ — 따라서 $\partial F/\partial N|_{T,V}\approx\partial G/\partial n|_{T,P}$, 곧 \S\ref{sec:sm-ensemble}의 통계적 $\mu$와 식~\eqref{eq:mudef}의 열역학적 $\mu$는 (강체 격자 근사 하에) 같은 물리량을 가리킨다.

**(b)(c)(d) — 사슬 완결은 \S\ref{sec:center}가 이미 밟았다(재수록 금지).**
이 동일시 위에서, 전기화학 평형($\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$, 식~\eqref{eq:eqbalance})$\to$$\Delta G_j=-sFU_j$(식~\eqref{eq:eqcond})$\to$$U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$(식~\eqref{eq:Uj})로 이어지는 사슬은 \S\ref{sec:center}가 이미 완결했다 — 그 사슬을 세우는 세 재료(Gibbs 정의$\cdot$화학퍼텐셜 정의$\cdot$전기화학 평형조건)는 반응종 무관 항등식이며 host 정체는 오직 입력값 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$로만 들어간다(\S\ref{sec:lco-center} (a)가 이미 이 점을 확인해 뒀다). 본 절이 그 사슬에 더하는 것은 오직 (a)의 동일시 — 그 $\mu$가 \S\ref{sec:sm-ensemble}의 대정준 $\mu$와 (강체 격자 근사 하에) 같은 물리량이라는 것 — 이며, 박스는 여기서 재수록하지 않는다(교훈 카드 ④, \S\ref{sec:center}의 식~\eqref{eq:gibbsdef}--\eqref{eq:Uj}를 그대로 참조).

**자체검수 — $T\to0$ 극한.** $U_j\to-\Delta H_{\rxn,j}/F$(순수 엔탈피, \S\ref{sec:center} (c)의 기존 검산과 동일). 미시적으로도 정합 — $T\to0$은 \S\ref{sec:sm-ensemble}/\S\ref{sec:sm-single}의 $\beta\to\infty$ 극한과 같으며, 그때 $\theta$(식~\eqref{eq:fermifn})는 바닥상태로 완전히 붕괴한다(§1(d) 극한과 정합, 원 한 바퀴가 미시$\cdot$거시 양쪽에서 같은 극한으로 닫힌다).

\begin{keybox}
\textbf{Part 0 요약.} §0(대정준 앙상블) $\to$ §1(단일 자리 점유, 식~\eqref{eq:fermifn}) $\to$ §2($M$자리 독립, 배치 엔트로피) $\to$ §3(평균장 $\Omega$, $\mu(\theta)$·$g(\xi)$, 식~\eqref{eq:mu}·\eqref{eq:gxi}·\eqref{eq:spinodal}) $\to$ §4(전기화학 연결, logistic $\xi_\eq$, 식~\eqref{eq:xieq}) $\to$ §5(거시 $G,\mu$와의 정합, \S\ref{sec:center}로 재접속) — 다섯 단계 전부 라그랑주 승수 $\beta,\mu$ 하나(§0)에서 갈라져 나와, 마지막에 다시 같은 $\mu$(§5)로 닫힌다.
\end{keybox}

---

## 3. 재접속 표 (Part 0 신설 후 원천 절 처분)

| 원천(현행 위치) | 대상 라벨/내용 | 처분 | Part 0 대응 |
|---|---|---|---|
| `sec:hys` L586–620(§(a)(b)(c)(d), 이중웰 그림 L622–645 포함) | eq:mu, eq:gxi, eq:gpp, eq:spinodal, fig:doublewell | **Part 0 §3(`sec:sm-meanfield`)로 정의 이관** — N3(`sec:hys`)는 이 지점부터 "\S\ref{sec:sm-meanfield}에서 이미 $g_j(\xi)$·spinodal을 세웠다" 1문장 다리 + `\subsection{gap 의 닫힌 꼴...}`(L647~)부터 재개 | §3 (d) |
| `sec:width` 첫 소절 L924–952(폭 이중지위) | eq:wbase 서술 중 "폭 척도가 logistic 중심 기울기에서 온다"는 유도 문장(L925–926)만 | **유도 문장만 Part 0 §4 참조로 압축**, 이중지위 논의(단상=평형예측/두-상=현상학적) 자체는 **Part I 잔류**(이는 흑연 데이터셋 특정 판정이지 일반 통계역학이 아님) | §4 (d) 범위 자체검수 |
| `sec:width` 둘째 소절 L953–1065(§(a)–(d), Eyring/detailed balance) | eq:bv, eq:db, eq:logisticsolve, fig:barrier, fig:flux | **Part I 잔류(적출 안 함)** — Part 0 §4는 열역학 직접대입 경로만 담고, 이 절의 속도론(kinetic) 경로는 §4가 인용하는 \emph{독립적 두 번째 경로}로 유지(둘의 일치 자체가 detailed-balance 자체검수, §4 말미) | §4 (교차검산으로 인용, 정의는 이관 안 함) |
| `sec:dist` L1073–1112(§(a)–(d), 단일자리 GC 점유↔logistic 동형) | eq:partfn, eq:fermifn | **Part 0 §1(`sec:sm-single`)로 정의 이관**, `sec:dist`는 (c)(d)(분포 관점의 결론 문단·keybox)만 남기고 도입부(a)(b)는 "\S\ref{sec:sm-single}에서 이미 세웠다" 1문장으로 압축 | §1 (d) |
| Ch2 `sec:partition` L110–189(eq:Z1, eq:occ, eq:muV, eq:logistic, ssec:BW 일부) | 단일자리 GC 분배함수·점유·전기화학 연결·Bragg--Williams | **Ch2 잔류(별도 컴파일 단위라 `\eqref` 상호참조 불가)** — 내용은 Part 0 §1/§3/§4와 사실상 중복. 향후(P6.1, 본 드래프트 범위 밖) Ch2 쪽을 "Ch1 Part 0 참조" 산문 포인터 + 최소 recap으로 압축하는 것을 권고만 한다(집행은 master 판단) | §1·§3·§4 (산문 포인터만, 라벨 공유 불가) |
| `sec:center` L417–475(§(a)–(d)) | eq:gibbsdef, eq:mudef, eq:eqbalance, eq:eqcond, eq:Uj | **무변경(재수록 안 함)** — Part 0 §5는 이 사슬이 서는 $\mu$가 §0의 $\mu$와 같은 대상임을 보이는 새 문단(§5(a))만 추가하고, (b)(c)(d)는 `\S\ref{sec:center}`를 인용 | §5 (a)만 신규, (b)(c)(d)는 인용 |

**라벨 이관 규칙**: 위 표에서 "정의 이관"은 `\label{...}`을 Part 0 쪽 박스로 옮기고 원 위치는 `\eqref{...}` 인용만 남긴다는 뜻 — LaTeX 라벨은 참조 방향(전방/후방)과 무관하게 해소되므로 이관 자체는 빌드 안전(단, 같은 라벨을 두 곳에서 `\label`로 재정의하면 "multiply defined labels" 에러이므로 **정의는 반드시 한 곳**이어야 한다 — 편입 시 원 위치의 `\label`을 지우는 작업이 필수, master 게이트 항목으로 명기 요청).

---

## 4. 갈래 2 — Part II "LCO 양극" 도입 절

```latex
\subsection{두 번째 전극 --- LCO 양극으로의 일반화}\label{sec:lco-map}
```

**(1) 전극-중립 골격 — 무엇이 전극 무관인가.**

지금까지(Part 0 + N0)의 유도가 실제로 전극을 가리지 않는다는 것을 라벨 단위로 짚는다:

```latex
지금까지의 기호와 매핑은 \emph{전극을 가리지 않는다}. 라벨 단위로 짚으면 —
(i) 실험조건 매핑 $\sigma_d=\pm1,\ |I|=\text{c\_rate}\cdot Q_\cell$(식~\eqref{eq:n0map})은
방향 부호$\cdot$전류 환산이며 삽입형 전극이면 종류를 가리지 않는다;
(ii) 전이 인덱스 $j$$\cdot$진행률 $\xi_j$$\cdot$점유 $\theta_j=1-\xi_j$(\S\ref{sec:notation})는 삽입형
전극이면 어디서나 같은 골격이고, 그 골격의 미시적 근거가 \S\ref{sec:sm-single}--\S\ref{sec:sm-lattice}의
자리-점유 통계다; (iii) 평형 조건 $\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$, $\Delta G_j=-sFU_j$
(식~\eqref{eq:eqcond})와 $U_j(T)$ 식(식~\eqref{eq:Uj})은 반응종 무관 항등식(Gibbs 정의$\cdot$화학퍼텐셜
정의$\cdot$전기화학 평형조건, \S\ref{sec:sm-macro})에서만 나오며 host 정체는 입력값
$(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$로만 들어간다; (iv) 격자기체 자유에너지
$g_j(\xi)=g_j^0+RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]+\Omega_j\xi(1-\xi)$(식~\eqref{eq:gxi})는
``동등한 자리에 리튬이 차고 빈다''는 가정 하나만 쓰므로(\S\ref{sec:sm-meanfield}) LCO
$\mathrm{Li}_x\mathrm{CoO_2}$의 팔면체 리튬 자리에도 문자 그대로 성립한다.

이 절은 이 골격을 두 번째 사례인 $\mathrm{LiCoO_2}$(LCO) 양극에 \emph{건다}. 흑연 서술은 한 줄도
바뀌지 않으며, LCO는 ``파라미터를 갈아 끼우고 고유 항 하나를 더하는'' 두 번째 전극으로 들어온다.
본 문건이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 --- 전셀 합성은 범위 밖이며
(후속), 단전극 부호와 전셀 부호를 섞지 않는다.

[기존 데이터 문단 무변경 유지 --- 원 sec:lco-map L309--354: 양극 부호 규약 문단(리튬화/탈리튬화
전위 방향), 표~\ref{tab:lco-staging}(LCO_MSMR_LIT 3전이 초기값, MIT/OD_a/OD_b)와 그 provenance
각주(tier-C placeholder 지위, round-trip 피팅 전제), 키 구조 대응 문단(GRAPHITE_STAGING_LIT 대응).
이 부분은 물리·수치·부호 불변 --- 이번 드래프트가 손대는 것은 그 앞뒤의 프레임(전극-중립 골격 재진술
+ 아래 방향 규약 통합 + MSMR 예고)뿐이며, 데이터 자체는 여기서 재타이핑하지 않는다(전사 오류 위험
회피 + 교훈 카드 ④ 재수록 금지 정신).]
```

**(2) 방향 규약 — 통합.**

원 `sec:lco-hys`의 "★분기 부호의 전극-중립 읽기"(L846–854)와 `sec:lco-peak`의 "★방향 부호의 전극-중립 읽기"(L1426–1437) 두 문단이 말하는 것은 결국 하나의 규칙이다 — 여기서 한 번만 완전히 진술한다:

```latex
\begin{keybox}
\textbf{방향 슬롯 $\sigma_d$의 물리 내용은 전극 불문 하나 --- 탈리튬화(산화) 진행 $=+1$.}
이 슬롯이 작용하는 곳은 \emph{세 작용처}뿐이다: 분극(\S\ref{sec:pol}, $V_\app=V_n+\sigma_d|I|R_n$,
식~\eqref{eq:vn})$\cdot$분기(\S\ref{sec:hys}, $U_j^{\,d}=U_j+\tfrac12\sigma_d h_\eta\gamma\Delta U_j^\hys$,
식~\eqref{eq:Ubranch})$\cdot$꼬리(\S\ref{sec:tail}, 격자 역전 방향). 평형 종 자체(식~\eqref{eq:xieq}의
\emph{모양})는 $\xi\leftrightarrow1-\theta$ 여집합 대칭이라 이 선택에 불변이다 --- 방향 읽기가 갈라놓는
것은 이 세 작용처이지 평형 봉우리의 존재 자체가 아니다.

흑연 음극 반쪽전지에서는 방전이 곧 탈리튬화라 셀 방향 \emph{라벨}(discharge/charge)과 물리
\emph{슬롯}($\sigma_d=\pm1$)이 우연히 일치한다(위 (1) 양극 부호 규약 문단과 대칭). LCO 양극
반쪽전지에서는 \emph{충전}이 탈리튬화(전위 상승 진행)이므로, LCO 데이터에 모델을 걸 때 세 작용처의
방향 인자는 셀 라벨이 아니라 탈리튬화 여부로 준다 --- 충전 곡선 $\mapsto\sigma_d=+1$ 슬롯, 방전
(리튬화$\cdot$전위 하강) 곡선 $\mapsto\sigma_d=-1$ 슬롯. 이렇게 읽으면 분극($V_\app>V_n$은 산화
방향에서 --- LCO 충전서 성립)$\cdot$분기(탈리튬화 봉우리가 위)$\cdot$꼬리 인과(시간 순서 = 전위
오름차순) 세 부호가 흑연과 1:1로 유지된다.

두 서술 --- ``방전($\sigma_d=+1$)은 LCO엔 리튬화''(셀 방향 \emph{라벨}의 의미론, 위 (1))와 ``LCO
데이터의 모델 입력 슬롯은 탈리튬화 여부로 준다''(이 keybox) --- 는 층위가 달라 모순이 아니다: 전자는
``어느 셀 동작이 어느 화학 방향인가''를 말하고, 후자는 ``모델에 어느 부호를 먹이는가''를 말한다.
\end{keybox}

그림~\ref{fig:lco-direction}이 이 규칙을 실제 코드 \code{func\_ksi\_eq}로 평가해 보인다 --- 흑연
(discharge$\mapsto\sigma_d{=}{+}1$)과 LCO(charge$\mapsto\sigma_d{=}{+}1$)가 셀 라벨은 반대이면서도
``탈리튬화 진행률은 $V$에 증가''라는 같은 모양의 곡선을 준다.
```

**(3) MSMR 예고.**

```latex
이 절이 세운 방향 규약은 \S\ref{sec:lco-code}에서 multi-species, multi-reaction(MSMR) 모델과의
동형으로 다시 확인된다 --- 결론만 미리 적으면, 슬롯 대응
$U\leftrightarrow V,\ U_j^0\leftrightarrow U_j^{\,d},\ \omega_j\leftrightarrow w_j,\
X_j\leftrightarrow Q_j$ 아래 방향 인자는 $f=+\sigma_d$(진행률$\leftrightarrow$진행률 짝짓기, 원계열
$f=F/RT>0$의 재모수화)이며 --- 이는 본 절이 세운 ``탈리튬화$=+1$'' 규약과 \emph{같은 결론}이다.
이 대응은 v1.0.12에서 물리 제1원리 재유도로 확정된 판정이며(관측 불변, $\theta(1-\theta)=\xi(1-\xi)$
잠복형), 상세 유도(원계열 부호 실측$\cdot$짝짓기 유일해 논증)는 \S\ref{sec:lco-code}가 맡는다 ---
본 절은 예고만 하고 재유도하지 않는다.
```

### 4.1 Part II 도입 절의 자체 정합 노트 (Track 1과 대칭, 요구 범위 밖 자발 제출)

| 흡수원 | 처분 |
|---|---|
| `sec:lco-hys` ★분기 부호 문단(L846–854) | 본 절 (2)로 흡수 — 원 위치는 "방향 규약은 \S\ref{sec:lco-map}이 통합 진술한다" 1문장 + 각주 잔존분(L841–844 "★주의 — $\gamma_j,h_{\eta,j}$는...현상학적 축소 인자다")만 남김 |
| `sec:lco-peak` ★방향 부호 문단(L1426–1437, 각주 포함) | 본 절 (2)로 흡수(각주의 "두 서술은 층위가 달라 모순이 아니다" 논증도 keybox 말미에 재현) — 원 위치는 "\S\ref{sec:lco-map}(2) 참조" 1문장으로 축약 |
| `V1013_STRUCTURE_MAP.md` §2 "II-0" 계획 | 위 처분이 그 계획("★방향 부호 문단은 II-0로 흡수·각주 처리 재설계")과 일치함을 확인 |

---

## 5. Figure 목록 + 코드/스크립트 경로

| # | 목적 | 형식 | 배치 | 캡션(안) |
|---|---|---|---|---|
| `fig:sm-theta-V` | Part 0 §1/§4 — 단일자리 평형 점유 $\xi_\eq(V)/\theta_\eq(V)$가 온도에 따라 폭($w{=}RT/F$)만 바뀌고 모양은 불변임을 보임 | matplotlib(PNG, 실제 \code{func\_ksi\_eq} 평가) | \S\ref{sec:sm-single} 또는 \S\ref{sec:sm-electrochem} 말미 | "단일자리 대정준 점유(식~\eqref{eq:fermifn})와 그 전기화학 닫힌꼴(식~\eqref{eq:xieq})을 실제 코드 함수로 평가 --- 흑연 stage 2→1 중심($U{=}0.085$ V)에서 세 온도(260/298.15/340 K), 폭 $w{=}RT/F$가 온도에 비례해 넓어짐(22.4/25.7/29.3 mV)을 보인다." |
| `fig:sm-gxi` | Part 0 §3 — 정규용액 자유에너지 $g(\xi)$의 단일웰→이중웰 전이(spinodal 문턱 $\Omega{=}2RT$) | matplotlib(PNG, 실제 \code{GRAPHITE\_STAGING\_LIT}의 $\Omega$값 사용) | \S\ref{sec:sm-meanfield} 말미(spinodal 박스 직후) | "정규용액 $g(\xi)$(식~\eqref{eq:gxi})를 실제 흑연 전이표의 $\Omega$값(6000/8000/10000/13000 J/mol)으로 평가 --- $\Omega{\le}2RT{\approx}4958$ J/mol(주황)은 단일웰, 그 이상은 이중웰이며 점(spinodal, 식~\eqref{eq:spinodal})은 닫힌꼴과 수치 근찾기(scipy.brentq)가 일치함을 스크립트 내에서 검증." |
| `fig:sm-mu` | Part 0 §3 — 평균장 화학퍼텐셜 $\mu(\theta)$의 단조→비단조(S자 되꺾임) 전이 | matplotlib(PNG, 동일 $\Omega$ 세트) | \S\ref{sec:sm-meanfield} 말미(fig:sm-gxi와 나란히) | "$\mu_\mathrm{Li}(\theta)-\mu^0$(식~\eqref{eq:mu})를 같은 $\Omega$ 세트로 평가 --- $\theta{=}1/2$에서의 기울기 $4RT-2\Omega$가 $\Omega{=}2RT$를 경계로 부호를 바꿔(닫힌꼴=중심차분 수치미분 일치, 스크립트 내 assert) 단조(안정)↔비단조(spinodal 쌍 발생) 전이를 만든다." |
| `fig:lco-direction` | Part II 도입 §(2) — 셀 라벨(방전/충전)과 탈리튬화 방향($\sigma_d{=}{+}1$ 슬롯)의 대응이 전극마다 다름을 시각화 | matplotlib(PNG, 실제 \code{GRAPHITE\_STAGING\_LIT}·\code{LCO\_MSMR\_LIT} 값 사용) | \S\ref{sec:lco-map} (2) keybox 직후 | "흑연(방전=탈리튬화, $U{=}0.085$ V)과 LCO(충전=탈리튬화, $U{=}3.930$ V) 각각에서 $\sigma_d{=}{+}1$ 슬롯을 '탈리튬화'로 읽으면 두 반쪽전지 모두 $\xi_\eq(V)$가 증가하는 같은 모양을 준다 --- 셀 라벨은 반대(방전 vs 충전)이나 물리 슬롯은 같다(식~\eqref{eq:xieq})." |

**스크립트 경로(전부 실행·검증 완료, 실제 `Anode_Fit_v1.0.13.py` 함수를 `importlib`로 로드해 평가 — 날조 없음):**

- `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_theta_xi_V.py` → `V1013_P21_fig_S2_theta_xi_V.png`
- `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_gxi_doublewell.py` → `V1013_P21_fig_S2_gxi_doublewell.png`
- `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_mu_theta.py` → `V1013_P21_fig_S2_mu_theta.png`
- `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_S2_direction_map.py` → `V1013_P21_fig_S2_direction_map.png`

---

## 6. 물리 자체검수 기록

| 항목 | 절 | 검수 내용 | 결과 |
|---|---|---|---|
| 차원 | §0(d) | $\beta(E_i-\mu N_i)$ 무차원(에너지/에너지) | PASS |
| 차원$\cdot$부호 | §3(c) | $\Omega=zwN_A/2$: [무차원]$\times$[J]$\times$[1/mol]=J/mol(표 단위 정합), $w{>}0\Rightarrow\Omega{>}0$(동종 인력, 본문 정합) | PASS |
| 극한 $\beta\to0$ | §1(d) | $\theta\to1/2$(고온 최대무지) | PASS |
| 극한 $\beta\to\infty$ | §1(d) | $\Delta\mu{\lessgtr}0\Rightarrow\theta\to1/0$(바닥상태 선택) | PASS |
| 극한 $\Omega\to0$ | §3 말미 | $\mu(\theta)$ 순수 로그(이상 격자기체), $g(\xi)$ 단일웰 | PASS(그림 검증, `fig_S2_mu_theta.py` 콘솔 출력) |
| 극한 $\Omega\to2RT^\pm$ | §3 말미 | $g''(1/2)=4RT-2\Omega$ 부호 전환점이 정확히 $\Omega{=}2RT$; \S\ref{sec:hys}의 기존 $\Delta U^\hys\to0$ Taylor 극한과 정합 | PASS(닫힌꼴=중심차분 수치미분 일치, assert 통과) |
| spinodal 닫힌꼴 vs 수치 | §3(d) | $\xi_s^\pm=\tfrac12(1\pm u)$ vs `scipy.optimize.brentq`로 찾은 $g''=0$ 근 | PASS(4개 실제 $\Omega$ 값 전부 일치, `fig_S2_gxi_doublewell.py` 콘솔 출력) |
| Detailed balance | §4 말미 | 열역학 직접대입(§4) vs 속도론 정지점(\S\ref{sec:width} Eyring) — 같은 이상 극한에서 같은 식~\eqref{eq:xieq} | PASS(구조적 일치, \S\ref{sec:dist} 기존 통합 서술과 교차) |
| $T\to0$ | §5 말미 | $U_j\to-\Delta H_{\rxn,j}/F$; 미시적으로 $\beta\to\infty$ 바닥상태 붕괴와 정합 | PASS |
| **자기 오류 정정(투명 공개)** | fig 스크립트 작성 중 | `fig_S2_mu_theta.py` 1차 작성 시 단조/비단조 태그 라벨이 **부호가 뒤바뀜**(슬�페 음수를 "monotonic"으로 오기)을 자체 발견 — closed-form 수치 자체는 처음부터 옳았고(중심차분과 일치), 오직 그 수치를 해석하는 텍스트 라벨만 반대였음. 원인: $g''(\theta)<0$(불안정, spinodal 쌍 발생)을 "monotonic"으로 잘못 태그. 코드 수정(라벨 조건 반전) 후 재실행해 정정 확인 | **발견·정정 완료** — 이 항목이 본 드래프트의 "①물리 논리 무결(전개 중 문제 발견 시 정정)" 준수 증거 |
| 방향 규약 재론 여부 | §4(3) | f=+σ_d를 재유도하지 않고 확정 판정만 인용했는지 grep 자기점검 | PASS — 본 드래프트 어디에도 "f=-σ_d" 유도 시도나 대안 pairing 논증 없음 |
| 기존 라벨 재정의 충돌 | §2 전체 | eq:mu·eq:gxi·eq:gpp·eq:spinodal·eq:xieq·eq:partfn·eq:fermifn을 Part 0에서 `\label`로 새로 정의 — 원 위치(`sec:hys`·`sec:width`·`sec:dist`)에서 같은 라벨이 **동시에** `\label`로 남아있으면 LaTeX "multiply defined" 에러 | **주의 플래그(§3 재접속 표에 명기)** — 편입 시 원 위치의 `\label` 제거가 선결 조건, 단독 드래프트 텍스트만으로는 검증 불가(빌드 시점 게이트) |

---

## 7. 5줄 요약

1. **Part 0(§0–§5)**: 대정준 앙상블(Jaynes 최대엔트로피)에서 시작해 단일자리 점유(eq:fermifn)→$M$자리 배치 엔트로피(Stirling, 대정준과 조합론 두 경로 교차검산)→평균장 $\Omega$(배위수$\cdot$쌍에너지에서 독립 재유도, eq:mu/eq:gxi/eq:spinodal)→전기화학 logistic(eq:xieq, $\Omega{=}0$ 범위 명시)→거시 $G,\mu$ 정합(\S\ref{sec:center} 재접속)까지 다섯 단계, 전부 독립 재유도.
2. **재접속 표**: `sec:hys`(μ(θ)·g(ξ)·spinodal 부분)·`sec:width`(logistic 유도부)·`sec:dist`(전문)의 정의를 Part 0로 이관하고 원 위치는 인용으로 압축하는 구체적 라벨 매핑을 제출했으며, master의 독자 좌표 문서(`V1013_STRUCTURE_MAP.md`)와 사후 대조해 일치를 확인했다.
3. **Part II 도입**: `sec:lco-map` 라벨을 승계해 전극-중립 골격(4항목, 식 단위 재확인)·방향 규약(두 ★ 문단을 "세 작용처" keybox 하나로 통합)·MSMR 예고(f=+σ_d 인용만, 재론 없음) 세 내용을 하나의 절로 묶었고, 기존 데이터 표(`tab:lco-staging`)는 재타이핑하지 않고 위치만 유지했다.
4. **Figure 4건 전부 실제 코드 함수(`func_ksi_eq`) + 실제 표값(`GRAPHITE_STAGING_LIT`/`LCO_MSMR_LIT`)을 `importlib`로 로드해 평가**했고, spinodal 닫힌꼴은 `scipy.brentq` 수치근과, 기울기부호 문턱은 중심차분 수치미분과 각각 assert로 교차검증했다 — 그 과정에서 자체 라벨링 오류 1건을 발견·정정했다(§6 기록).
5. **최약점 자기표시**: (i) §5(a)의 "강체 격자 근사로 $F\approx G$" 동일시는 표준적이나 이 문건 다른 곳에서 명시적으로 전제된 적은 없어 신규 가정 취급이 필요할 수 있다(물리적으로는 건전 — 삽입 반응의 부피 변화가 화학 에너지 스케일 대비 무시 가능하다는 것은 고체전극 문헌의 표준 근사이나, 본 드래프트가 처음 명문화했다는 점은 master 검토 대상). (ii) Ch2 `sec:partition`과의 중복은 재접속 표에서 "권고만" 했을 뿐 집행하지 않았다 — Part 0가 신설되면 Ch2 쪽 압축(P6.1)은 후속 phase의 몫으로 남는다. (iii) §2/§3 사이의 앙상블 동등성($M\to\infty$) 논증은 엄밀 증명이 아니라 표준 결과 인용이며, 이 절 범위에서 완전한 증명을 재구성하지는 않았다(스코프 판단 — 통계역학 개론 수준을 넘는 엄밀도는 목표가 아니라고 판단).
