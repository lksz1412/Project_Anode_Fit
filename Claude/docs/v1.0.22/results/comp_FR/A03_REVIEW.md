# A03_REVIEW — §2 Part 0 후반부 (`ch1_sec02b_part0.tex`) 심층 검토 (FR-A03)

> 대상: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex` (전문 정독 — §2.4 평균장 / §2.5 전기화학 결선 / §2.5′ 다클래스 대정준 반전(bgbox V22-SM2-B 포함) / §2.6 거시 마감)
> 참조 원문 확인(read-only): `ch1_sec02a_part0.tex`(eq:sm-S·sm-gc·fermifn·sm-flucres·sm-Smix·sm-mucount·sm-muideal·sm-factor·sm-epstilde·partfn), `ch1_sec01_n0n1.tex`(sec:notation — s·σ_d 작용처 3곳·N_p·tab:notation), `ch1_sec03_center.tex`(eq:eqcond·eq:Uj·fig:UjT), `ch1_sec04_hys.tex`(eq:gpp·spinodal·Veq·dUhys·fig:hysloop ±1.066), `ch1_sec05_width.tex`(eq:db·wbase·xieq·sec:width-w 이중지위·sec:dist), `ch1_sec06_eqpeak.tex`(N6 보존식), `ch1_sec10_sum.tex`(tab:staging Ω열·U=0.085), `ch2_sec01_partition.tex`(eq:Z1·muV·Vxi·ssec:site), `ch2_sec05_mixing.tex`(ssec:overlap·eq:implicit), `ch2_sec08_synthesis.tex`(sec:synthesis 라벨), `ch1_sec13_lcohys.tex`(Ω_j^cat 표 밖 확인), `ch1_sec17_msmr.tex`(sec:lco-code-msmr — ch2 빌드 포함 확인), `ch1_graphite_v1.0.22.tex`·`ch2_lco_v1.0.22.tex`(빌드·xr), `ch1v22_bib.tex`, `results/V1022_REFERENCE_LEDGER.md`(V1 원장).
> 규율: 보고 전용 — 소스 무수정·git 무조작·`Codex/` 미접근. bgbox[V22-SM2-B]는 제거 용이 독립 블록 — 아래 제안 중 bgbox 관련(M6)은 **박스 내부 문장 대체만**이며 본문→박스 의존을 만들지 않는다(L5 는 그 의존을 일부러 피해 설계). GS-1/GS-2(Ch3 Si 정직 공백)는 본 절 무접점 — 메움 제안 없음.
> 상태: **최종본** (조기 저장 후 검증·서치 완료 통합, 2026-07-17)

---

## 발견 표 (BRIEF 양식 — 요약; 현행 열은 축자 앵커, 여러 행짜리는 아래 상세 절에 개행 포함 전문 축자)

| ID | 파일:행 | 유형 | 등급 | 현행(축자 앵커) | 제안(요지 — 완성 LaTeX 는 상세 절) | 근거 |
|---|---|---|---|---|---|---|
| A03-M1 | ch1_sec02b_part0.tex:163–166 | 논리/수식화 | M | `그 결과 측정 전위` `$V\equiv\phi_M-\phi_\mathrm{ref}$(vs Li/Li$^+$)만 남는다:` | 접촉 전위차를 "흡수"한다면서 $V$ 를 Galvani 차 $\phi_M-\phi_\mathrm{ref}$ 로 `\equiv` 정의하는 자기긴장 해소 — 조작적 정의 $-FV\equiv\tilde\mu_{e^-}^{M}-\tilde\mu_{e^-}^{\mathrm{ref}}$ 명시 | 재유도: 동일단자 전위차 = $-(\tilde\mu_{e^-}^M-\tilde\mu_{e^-}^\mathrm{ref})/F$; 앞 문장(표준 처리)과 `\equiv` 가 충돌 |
| A03-M2 | ch1_sec02b_part0.tex:162–163 | 보완 | M | `빼면 전해질 몫($\mu_{\mathrm{Li}^+}+F\phi_S$)이` `상쇄된다.` | 상쇄의 숨은 전제(무전류 평형 → 전해질 내 $\tilde\mu_{\mathrm{Li}^+}$ 균일; 유한 전류 구배는 §1 분극 몫) 한 절 명시 | 전자 몫엔 숨은 단계를 명시하면서 전해질 몫은 무전제 상쇄로 적음 — 대칭 보강 |
| A03-M3 | ch1_sec02b_part0.tex:147–149 | 보완 | M | `host 안의 Li 는 중성이라` `$\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$ 다:` | 반응식의 빈자리 $[\,]$ 몫이 어디 갔는지 한 절 — $\mu_\mathrm{Li}(\theta)=\partial F/\partial N$ 이 점유·공위 교환을 함께 셈($\ln[\theta/(1-\theta)]$ 분모가 공위 몫) | 독자 표준 질문(반응식 좌변 $[\,]$ 의 $\mu$ 항 부재) 선제 답변 |
| A03-M4 | ch1_sec02b_part0.tex:307–311 | 논리 | M | `자기무모순 평균장으로만 들어가므로 $\Xi_{1,j}$ 는 그 평균장 속의 단일 자리 분배함수이고` | (i)의 "Ω_j 가 든다" 서술 ↔ 전시식의 θ-독립 $\tilde\varepsilon_j(T)$ 불일치를 명시화 — 자기무모순이면 지수가 $[sF(V{-}U_j)+\Omega_j(1{-}2\theta_j)]/RT$ 로 되먹임(정의상 implicit), 전시식 \eqref{eq:sm-mc-occ}–\eqref{eq:sm-mc-fluc} 는 되먹임 동결 서식 | 재유도(아래 §V-9); P3-3·4 (순환 의존 위치·분류 명시) 정합 |
| A03-M5 | ch1_sec02b_part0.tex:368–371 | 보완 | M | `가드 --- 평균장 이중웰($\Omega_j>2RT$,` | 중간 창 $0<\Omega_j\le2RT$ 의 지위 추가 — 자기무모순 응답 $[1-2\Omega_j\theta_j(1-\theta_j)/RT]^{-1}$ 배(양성 유지 → 유일근 결론 불변), 단 \eqref{eq:sm-mc-fluc} 가운데 등식은 $\Omega_j{=}0$ 서식에서만 축자 성립 | 재유도(§V-9): $\partial\theta/\partial\mu$ 분모 최솟값 $1-\Omega_j/2RT$ |
| A03-M6 | ch1_sec02b_part0.tex:396–398 | 보완 | M | `$\sqrt{\mathrm{var}(N)}/\langle N\rangle$ 이 곧 $U_\mathrm{oc}$ 를` `흐리는 함량 폭인데` | (bgbox 내부만) $U_\mathrm{oc}$ 흐림에 실제로 곱해지는 것은 조성 폭 $\sigma_{\bar x}=\sqrt{\mathrm{var}}/M\le1/(2\sqrt M)$(균일 상계) — 상대 요동은 내부 조성 동등 척도로 병기 | 재유도(§V-10): $\sigma_{\bar x}^2\le1/(4M)$ 균일; $\sqrt{\mathrm{var}}/\langle N\rangle$ 는 $\theta\to0$ 끝에서 발산 |
| A03-M7 | ch1_sec02b_part0.tex:417–424 | 보완/설명 | M | `\qquad(\text{삽입 고체: }P\Delta v\ll RT,\;F\,V)` | 한 식 안 4중 기호 충돌($F$=Helmholtz/Faraday·$V$=부피/전위) 해소 — 괄호에서 `F\,V` 제거(산문이 이미 전기 일 스케일 서술), ≃ 가 근사하는 실제 자리(강체 격자 모형 $F$ 의 $P\Delta v$ 탈락, $\sim1$ J/mol ≪ $RT$) 명시 | ∂G/∂n|_{T,P}=∂F/∂n|_{T,V} 는 완전 $F$ 에선 항등(연쇄율, §V-11); sec02a 의 "문맥으로 갈린다" 방침이 한 줄 안에서 무력화되는 유일 지점 |
| A03-M8 | ch1_sec02b_part0.tex:44–47 | 설명/수식화 | M | `$g_j^0$ 는 상수 몫과 $\xi$-직선 몫을 묶은 것이고, 미분에는 그중 상수 기여만 남는다:` | 오독 유발 문장 재서술 — $g_j^0(\xi)\equiv\mu^0(1-\xi)$(아핀) 명시, "미분하면 상수 $-\mu^0$ 로 줄고 두 번 미분에 소멸" | "상수 기여만 남는다"는 '상수항이 살아남는다'로 오독 가능(상수항은 미분에서 죽음) — P5: 기호 유지·인수 표기만 개정 제안 |
| A03-M9 | ch1_sec02b_part0.tex:67–72 | 보완 | M | `극한 검산 --- $\Omega_j\to0$: $g''\ge4RT>0$ 로 항상 한 웰` | 문턱 verifybox 에 평균장 지위 가드 1문장 — BW 는 상관 무시로 같은 $u$ 대비 $T_c$ 과대평가 쪽 치우침(\cite{mcquarrie1976}); 본론 사용처는 문턱의 존재·스케일이고 $\Omega_j$ 는 피팅 슬롯이라 치우침 흡수 | 표준 결과(정확 2D 해 대비 MF $T_c$ 과대 — §S 후보 onsager1944 검증됨); tab:staging "Ω 정규용액 추정(피팅 출발점)" 과 정합 |
| A03-M10 | ch1_sec02b_part0.tex:272–277 | 설명 | M | `(b) 식~\eqref{eq:sm-logistic} 의 $\xi_\eq(V)$ ($U=0.085$ V, stage` | 캡션에 동결 명시 — 두 패널 모두 $\tilde\varepsilon$·$U$ 를 온도 상수로 동결해 폭의 $T$-의존만 분리; 중심의 온도 이동은 §3 그림 fig:UjT 소관 | Part 0 자체가 $\tilde\varepsilon(T)$·$U_j(T)$ 온도 의존을 강조(2→1 은 $-0.166$ mV/K → 60 K 창 $-10$ mV) — 독자가 그림과 §3 을 잇다 혼동할 지점 |
| A03-L1 | ch1_sec02b_part0.tex:171 | 문체 | L | `화학퍼텐셜이 정확히 $-FV$ 만큼 낮아진다` | 이중 부정 해소: "기준 금속 대비 정확히 $FV$ 만큼 낮아진다" | $\mu_\mathrm{Li}-\mu_\mathrm{Li}^\mathrm{metal}=-FV$: 낮아지는 '양'은 $+FV$ |
| A03-L2 | ch1_sec02b_part0.tex:173–175 | 표기 | L | `전이 중심 $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$ 로 재포장하면` | §2.4 의 "(이하 한 전이의 $\Omega\equiv\Omega_j$)" 장치를 동일 적용: "(이하 한 전이의 $U\equiv U_j$·$\Delta G\equiv\Delta G_j$; …)" | eq:sm-eqcond 한 줄 안에서 무첨자 $U$ 와 첨자 $U_j$ 혼재 — 첨자 도입 근거 부재 |
| A03-L3 | ch1_sec02b_part0.tex:146 | 표기 | L | `($z$ = 전하수, $\phi$ = 그 종이 있는 상의 정전 퍼텐셜)` | "($z$ = 전하수 --- \S\ref{sec:sm-mf} 의 배위수 $z$ 와 별개, …)" | 직전 소절의 $z$(배위수)와 동일 기호 — §5 는 원거리 각주로 처리했으나 국소 병기가 저렴 |
| A03-L4 | ch1_sec02b_part0.tex:64–66 | 보완 | L | `$\Omega_j>2RT$ 면 가운데($g''<0$)가 언덕이 되어 두 골짜기가 생기고` | 수치 눈금 병기: "($298.15$ K 에서 $2RT\approx4.96$ kJ/mol --- 표~\ref{tab:staging} 초기값 $6$–$13$ kJ/mol 이 모두 넘는 문턱)" | 추상 문턱의 실척도 제공; 검산 $2\times8.3145\times298.15=4957.7$ J/mol |
| A03-L5 | ch1_sec02b_part0.tex:351–352 | 표기 | L | `대정준($\mu$ 독립)$\to$정준($\langle N\rangle$` `고정)의 Legendre-켤레 반전이다` | "정준($N$ 고정)" — 정준의 정의는 $N$ 고정(평균 아님) | bgbox 는 "N 을 고정한 정준 기술"로 옳게 적음 — 본문과 박스 사이 표기 불일치(본문 수정으로 정합; bgbox 의존 신설 아님) |
| A03-L6 | ch1_sec02b_part0.tex:27–30 | 보완 | L | `이 한 모수로 혼합 자유에너지를 적는 모형이` `\emph{정규용액}이고` | A–B 정규용액 표기와의 대응 각주: A=점유·B=공위, $u_{AA}=u$·$u_{AB}=u_{BB}=0$ ⇒ $\Omega=-\tfrac z2N_Au$ 회수 | 정규용액 문헌 독자의 표준 환산 질문 선제(검산 §V-1) |
| A03-L7 | ch1_sec02b_part0.tex:283–287 | 보완 | L | `이 소절은 두 결과를 전이` `여럿으로 한 줄 넓혀` | 모형 계보 포인터 1구: "(다클래스 서식의 문헌 계보 --- MSMR --- 대응은 Ch.2 \S\ref{sec:lco-code-msmr})" | sec:lco-code-msmr 는 ch2 빌드 포함 확인 — 기존 xr 관행(sec:lco-hys 참조)과 동일 메커니즘 |
| A03-L8 | ch1_sec02b_part0.tex:348–350 | 수식화 | L | `반전의 지위도 여기서 정확해진다: 대정준에서는` | (선택) 순방향/반전 두 사상의 한 줄 디스플레이 병기 | 산문 3행의 구조를 사상 표기로 압축 — 선택 사항 |

**등급 합계: H 0 / M 10 / L 8.**

---

## H 등급 (논리/물리 오류·오귀속)

**무발견.** 본 절의 전 수식(eq:sm-mf/omega/gtheta/mu/gxi/sm-thresh/sm-emu/workbal/refbal/muV/eqcond/logistic/mc-factor/mc-occ/mc-balance/mc-fluc/mubridge/nernst)과 세 그림의 전 좌표를 재계산·재유도로 검증했으며(§V), 부호 사슬(s=+1·∓ 짝·거울 ±1.066·V↑⇒ξ↑)과 "글자까지 같다" 주장 2건(eq:eqcond·eq:implicit) 및 인접 장 전달식 전부가 원문과 일치함을 확인했다. H 등급에 해당하는 논리·물리 오류·오귀속은 없다.

---

## M 등급 상세 (의미·이해 실질 개선)

### A03-M1 — 접촉 전위차 "흡수" 선언과 $V\equiv\phi_M-\phi_\mathrm{ref}$ 정의의 자기긴장
- 파일:행 = `ch1_sec02b_part0.tex:162–166` (유형 논리/수식화)
- 현행(축자):
```latex
\eqref{eq:sm-workbal} 에서 \eqref{eq:sm-refbal} 을 빼면 전해질 몫($\mu_{\mathrm{Li}^+}+F\phi_S$)이
상쇄된다. 전자의 화학 몫도 상쇄되는데, 여기에는 한 단계가 숨어 있다 --- 두 전극의 전자 화학퍼텐셜은
엄밀히는 재질에 따라 다르며, 그 차이(접촉 전위차)는 두 전극을 같은 재질의 도선 단자 사이에서 읽는 측정
전위의 조작적 정의에 흡수되어 별도 항으로 남지 않는다(전기화학의 표준 처리). 그 결과 측정 전위
$V\equiv\phi_M-\phi_\mathrm{ref}$(vs Li/Li$^+$)만 남는다:
```
- 문제: 직전 문장이 옳게 말한 대로 두 전극의 $\mu_{e^-}$ 는 재질에 따라 다르고, 그 차이를 **흡수하는** 양은 동일 재질 단자 사이에서 읽는 조작적 측정 전위 $-FV\equiv\tilde\mu_{e^-}^{M}-\tilde\mu_{e^-}^{\mathrm{ref}}$ 다. 그런데 결론 문장은 $V$ 를 Galvani 전위차 $\phi_M-\phi_\mathrm{ref}$ 로 `\equiv` 정의한다 — 이는 접촉 전위차가 **흡수되지 않는** 바로 그 양이라, 두 문장이 기호 수준에서 충돌한다(두 전극 재질이 같아야 두 정의가 일치; 여기서는 흑연 vs Li 금속이라 다름). 결과식 \eqref{eq:sm-muV} 자체는 조작적 $V$ 로 읽으면 정확하다.
- 제안(대체 LaTeX — 마지막 문장만):
```latex
그 결과 남는 것이 측정 전위 $V$(vs Li/Li$^+$)다 --- 같은 재질 단자 사이 전위차라는 조작적 정의가
$-FV\equiv\tilde\mu_{e^-}^{M}-\tilde\mu_{e^-}^{\mathrm{ref}}$ 로 좌변 전자 몫 전체와 정확히 일치하며,
두 전극의 전자 화학 몫이 같은 이상화에서는 $V=\phi_M-\phi_\mathrm{ref}$ 로 환원된다:
```
- 근거: 재유도 — 단자(동일 재질, 전자 평형 $\tilde\mu_{e^-}$ 연속)로 읽는 전위차는 $-F\,V_{\rm meas}=\tilde\mu_{e^-}^{M}-\tilde\mu_{e^-}^{\mathrm{ref}}=(\mu_{e^-}^{M}-\mu_{e^-}^{\mathrm{ref}})-F(\phi_M-\phi_\mathrm{ref})$. 이 정의를 쓰면 \eqref{eq:sm-workbal}$-$\eqref{eq:sm-refbal} 이 항등적으로 \eqref{eq:sm-muV} 가 된다(전자 화학 몫이 정확히 흡수). 원문 \eqref{eq:sm-workbal}·\eqref{eq:sm-refbal} 이 공통 기호 $\mu_{e^-}$ 를 쓰는 것(= 이상화 선취)은 유지 가능 — 위 대체문이 그 이상화의 지위를 명시한다.

### A03-M2 — 전해질 몫 상쇄의 숨은 전제(무전류 평형) 미명시
- 파일:행 = `ch1_sec02b_part0.tex:162–163` (유형 보완)
- 현행(축자): `\eqref{eq:sm-workbal} 에서 \eqref{eq:sm-refbal} 을 빼면 전해질 몫($\mu_{\mathrm{Li}^+}+F\phi_S$)이` + 개행 + `상쇄된다.`
- 문제: 상쇄는 두 전극 표면 위치의 $\mu_{\mathrm{Li}^+}+F\phi_S$(= $\tilde\mu_{\mathrm{Li}^+}$)가 같을 때 성립 — 무전류 평형에서 전해질 전체에 $\tilde\mu_{\mathrm{Li}^+}$ 가 균일하다는 전제다. 전자 몫의 숨은 단계는 정성껏 명시했으면서 전해질 몫은 무전제로 상쇄해, 유한 전류의 농도·액간 전위 구배를 아는 독자가 "왜 자동인가"를 묻게 된다(답: 본 절은 평형·무전류; 유한 전류 몫은 §1 분극).
- 제안(대체 LaTeX):
```latex
\eqref{eq:sm-workbal} 에서 \eqref{eq:sm-refbal} 을 빼면 전해질 몫($\mu_{\mathrm{Li}^+}+F\phi_S$)이
상쇄된다(무전류 평형이라 $\tilde\mu_{\mathrm{Li}^+}$ 가 전해질 전체에 균일해 두 전극 위치에서 같은 값 ---
유한 전류의 전해질 구배는 평형 밖 몫으로 \S\ref{sec:pol} 의 분극에 든다).
```
- 근거: \S\ref{sec:sm-ensemble} 의 평형 조건($\mu$ 일치) 논리의 전해질판; `ch1_sec01_n0n1.tex` \S\ref{sec:pol}(lumped $R_n$)과 역할 분담 명시.

### A03-M3 — 반응식 좌변 빈자리 $[\,]$ 의 $\mu$ 항이 어디 갔는가 (독자 질문 선제)
- 파일:행 = `ch1_sec02b_part0.tex:147–149` (유형 보완)
- 현행(축자):
```latex
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\mathrm{host})}$ 의 평형은 양변 $\tilde\mu$ 합의 일치이고
(\S\ref{sec:center} 가 결과 사슬에서 같은 균형으로 진입한다), host 안의 Li 는 중성이라
$\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$ 다:
```
- 문제: 반응식에 $[\,]$(빈자리)를 명시해 놓고 평형식 \eqref{eq:sm-workbal} 우변에는 그 몫이 따로 없다. 격자기체에 익숙지 않은 독자의 표준 질문("빈자리의 화학퍼텐셜 항은?")에 답이 없다 — 실제 답은 $\mu_\mathrm{Li}(\theta)=\partial F/\partial N$ 이 '점유 하나 증가 = 공위 하나 감소' 교환을 이미 함께 세는 양이라는 것(그래서 $\ln[\theta/(1-\theta)]$ 에 공위 몫이 분모로 들어 있음)이며, 이 사슬은 \eqref{eq:sm-mucount} 로 이미 닫혀 있으나 연결 문장이 없다.
- 제안(대체 LaTeX — 해당 구절만):
```latex
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\mathrm{host})}$ 의 평형은 양변 $\tilde\mu$ 합의 일치이고
(\S\ref{sec:center} 가 결과 사슬에서 같은 균형으로 진입한다), host 안의 Li 는 중성이라
$\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$ 다(빈자리 $[\,]$ 의 몫을 따로 적지 않는 것은 격자기체
$\mu_\mathrm{Li}(\theta)=\partial F/\partial N$~\eqref{eq:sm-mucount} 이 점유 하나가 늘며 공위 하나가
줄어드는 교환을 이미 함께 세기 때문이다 --- $\ln[\theta/(1-\theta)]$ 의 분모가 그 공위 몫이다):
```
- 근거: \eqref{eq:sm-mucount} 재유도로 확인 — $\partial S_\mathrm{mix}/\partial N$ 이 $-k_B\ln[\theta/(1-\theta)]$ 를 주는 계산에 공위 감소가 포함되어 있음.

### A03-M4 — (b)(i) "Ω_j 가 자기무모순 평균장으로 들어간다" ↔ 전시식의 θ-독립 $\tilde\varepsilon_j(T)$ 불일치
- 파일:행 = `ch1_sec02b_part0.tex:307–311` (유형 논리 — 수식↔산문 불일치)
- 현행(축자):
```latex
--- 독립 부분계 분배함수의 표준 인수분해다 \cite{hill1960,mcquarrie1976}. 근사 경계는 두 겹이다: (i) 클래스
\emph{안}의 이웃 상호작용 $\Omega_j$(\S\ref{sec:sm-mf})는 각 자리가 자기 클래스의 평균 점유만 느끼는
자기무모순 평균장으로만 들어가므로 $\Xi_{1,j}$ 는 그 평균장 속의 단일 자리 분배함수이고, (ii) 클래스
\emph{사이}의 상관 --- 한 갤러리의 채움이 이웃 stage 의 문턱을 옮기는 staging 결합 --- 은 이 곱에서 빠진다.
곧 식~\eqref{eq:sm-mc-factor} 는 평균장 수준에서 정확하다.
```
- 문제: (a)는 $\tilde\varepsilon_j(T)$ 를 \eqref{eq:sm-epstilde} 클래스판(θ-무관)으로 정의했고, \eqref{eq:sm-mc-factor}·\eqref{eq:sm-mc-occ}·\eqref{eq:sm-mc-fluc} 는 전부 그 고정 $\tilde\varepsilon_j$ 로 전시·미분된다. 그런데 (i)는 $\Omega_j$ 가 $\Xi_{1,j}$ 에 "자기무모순 평균장으로" 든다고 말한다 — 액면대로면 지수의 $\tilde\varepsilon_j$ 가 $\theta_j(\mu)$ 를 통해 $\mu$-의존이 되어, (c)의 $\partial\ln\Xi/\partial\mu$ 항별 미분과 검산 (i)의 $\partial\theta_j/\partial\mu=\beta\theta_j(1-\theta_j)$ 가 되먹임 항을 놓친 셈이 된다. 산문(자기무모순)과 수식(동결)이 서로 다른 모형을 가리키는 상태 — 어느 쪽이 전시식의 지위인지 한 문장이 필요하다(P3-3: 순환 의존이 **어느 식·어느 변수**에서 생기는지 명시).
- 제안(대체 LaTeX — (i) 항만; (ii)와 마지막 문장 유지):
```latex
근사 경계는 두 겹이다: (i) 클래스 \emph{안}의 이웃 상호작용 $\Omega_j$(\S\ref{sec:sm-mf})는 각 자리가
자기 클래스의 평균 점유만 느끼는 자기무모순 평균장으로 들어간다 --- 명시하면
\S\ref{sec:sm-electro} (iii) 의 암시 등온선 그대로, \eqref{eq:sm-mc-occ} 의 지수가 몰당
$[sF(V-U_j)+\Omega_j(1-2\theta_j)]/RT$ 로 밀려 $\theta_j$ 자신이 지수에 되먹임되는(정의상 implicit) 서식이고,
아래 \eqref{eq:sm-mc-occ}--\eqref{eq:sm-mc-fluc} 의 \emph{명시 꼴}은 그 되먹임을 끈($\Omega_j{=}0$, 곧
상호작용 몫을 상수로 $U_j$ 에 흡수한) 독립 자리 서식이다;
```
- 근거: 재유도(§V-9) — \eqref{eq:mu} 를 \eqref{eq:sm-eqcond} 에 넣으면 $\theta_j=\{1+\exp[(sF(V{-}U_j)+\Omega_j(1{-}2\theta_j))/RT]\}^{-1}$ (자기무모순). 이 명시화는 검산 (i) 가드(A03-M5)와 한 쌍으로 닫힌다. 기존 자산(수식·라벨) 무삭제.

### A03-M5 — 검산 (i) 가드에 중간 창 $0<\Omega_j\le2RT$ 의 지위 추가
- 파일:행 = `ch1_sec02b_part0.tex:368–371` (유형 보완)
- 현행(축자):
```latex
가드 --- 평균장 이중웰($\Omega_j>2RT$,
식~\eqref{eq:sm-thresh})의 비단조 등온선 가지(그림~\ref{fig:sm-mu})는 이 보증의 밖이고 그 창의 분기 구성은
\S\ref{sec:hys} 소관이며, 본론과 Part T 가 반전에 실제로 쓰는 전이별 logistic 서식(폭 $w_j$ 의 이중지위는
\S\ref{sec:width})은 항마다 강단조라 보증 안이다.
```
- 문제: 가드가 $\Omega_j>2RT$ 만 밖으로 선언해, 독자는 $0<\Omega_j\le2RT$ 에서 \eqref{eq:sm-mc-fluc} 의 **등식까지** 그대로 성립한다고 읽기 쉽다. 실제로는 (자기무모순 평균장에서) 유일근 **결론**은 문턱까지 그대로 살지만, 가운데 등식(독립 자리 분산 가법 $=\beta\sum M_j\theta_j(1-\theta_j)$)은 $\Omega_j=0$ 서식에서만 축자 성립한다 — 응답이 $[1-2\Omega_j\theta_j(1-\theta_j)/RT]^{-1}$ 배로 바뀌기 때문.
- 제안(가드 문장 끝에 이어붙임 — 기존 문장 유지):
```latex
중간 창 $0<\Omega_j\le2RT$ 는 자기무모순 평균장 등온선에서도 응답이
$[\,1-2\Omega_j\theta_j(1-\theta_j)/RT\,]^{-1}$ 배가 될 뿐 양성이 유지되어(분모 최솟값이
$\theta_j{=}\tfrac12$ 에서 $1-\Omega_j/2RT\ge0$; 등호점 $\Omega_j{=}2RT$·$\theta_j{=}\tfrac12$ 는 수직 접선의
고립점이라 순증은 유지) 유일근 결론은 그대로다 --- 단 이 경우 \eqref{eq:sm-mc-fluc} 의 가운데
등식(독립 자리 분산 가법)은 $\Omega_j{=}0$ 서식에서만 문자 그대로다.
```
- 근거: 재유도(§V-9) — $\mu(\theta)=\mu^0+RT\ln[\theta/(1-\theta)]+\Omega_j(1-2\theta)$ 에서 $\dd\mu/\dd\theta=RT/[\theta(1-\theta)]-2\Omega_j$, 역수 취하면 위 인자; $\theta(1-\theta)\le\tfrac14$ 로 $\Omega_j\le2RT$ 면 전역 양성(등호 한 점). \S\ref{sec:width-w}(0<Ω<2RT 유효 폭 $(1-\Omega_j/2RT)$ 배 협착 — 같은 인자의 폭 판) 및 이중지위 서술과 정합.

### A03-M6 — (bgbox 내부) $U_\mathrm{oc}$ 흐림에 곱해지는 폭의 정체: 상대 요동 → 조성 폭
- 파일:행 = `ch1_sec02b_part0.tex:396–398` (유형 보완 — bgbox[V22-SM2-B] 내부 문장 대체만, 독립성 유지)
- 현행(축자):
```latex
$\bar x$)으로 읽어도 되는 근거다 --- $\sqrt{\mathrm{var}(N)}/\langle N\rangle$ 이 곧 $U_\mathrm{oc}$ 를
흐리는 함량 폭인데, 그 폭이 거시 $M$ 에서 소멸하기 때문이다.
```
- 문제: $U_\mathrm{oc}$ 를 흐리는 데 실제로 곱해지는 것은 함량 **좌표**의 폭 $\sigma_{\bar x}=\sqrt{\mathrm{var}(N)}/M$($\delta U_\mathrm{oc}\approx|\partial U_\mathrm{oc}/\partial\bar x|\,\sigma_{\bar x}$)이지 상대 요동 $\sqrt{\mathrm{var}}/\langle N\rangle$ 이 아니다. 내부 조성($\langle N\rangle=O(M)$)에선 둘 다 $1/\sqrt M$ 로 같이 죽어 결론은 불변이나, $\theta_j\to0$ 끝단에선 상대 요동이 발산하는 반면 $\sigma_{\bar x}\le1/(2\sqrt M)$ 는 **균일** 상계라, 지금 문장은 끝단 독자 검산에 취약하다.
- 제안(대체 LaTeX — 해당 문장만; bgbox 안에서 자족, 새 라벨·외부 참조 없음):
```latex
$\bar x$)으로 읽어도 되는 근거다 --- $U_\mathrm{oc}$ 를 흐리는 것은 함량 좌표의 폭
$\sigma_{\bar x}=\sqrt{\mathrm{var}(N)}/M\le1/(2\sqrt M)$($\theta_j(1-\theta_j)\le\tfrac14$ 의 균일 상계)이고
흐림이 $|\partial U_\mathrm{oc}/\partial\bar x|\,\sigma_{\bar x}$ 로 그 폭에 비례하는데, 그 폭이 거시 $M$
에서 소멸하기 때문이다(위 상대 요동 $\sqrt{\mathrm{var}}/\langle N\rangle$ 은 같은 $1/\sqrt M$ 소멸을
내부 조성 $\langle N\rangle=O(M)$ 에서 재는 동등한 척도다).
```
- 근거: 재유도(§V-10) — $\sigma_{\bar x}^2=\mathrm{var}(N)/M^2=\sum_jM_j\theta_j(1-\theta_j)/M^2\le(\tfrac14\sum_jM_j)/M^2=1/(4M)$. 1차 전파로 $\delta U_\mathrm{oc}=|\partial U_\mathrm{oc}/\partial\bar x|\sigma_{\bar x}$. 박스의 기존 전개($\mathrm{var}=O(M)$·$\langle N\rangle=O(M)$)와 기호 전부 공유 — 독립성 훼손 없음.

### A03-M7 — eq:sm-mubridge 한 줄 안의 $F$·$V$ 4중 충돌과 ≃ 의 실제 근사 자리
- 파일:행 = `ch1_sec02b_part0.tex:417–424` (유형 보완/설명)
- 현행(축자):
```latex
\S\ref{sec:sm-ensemble} 의 $\mu=\partial F/\partial N|_{T,V}$ 였다. 둘의 다리는 $G=F+PV$ 다 --- 응축상
격자에 이온 1몰을 넣을 때의 $P\Delta v$ 몫은 $RT$·전기 일($FV$) 스케일에 비해 무시되므로
\begin{equation}
\mu=\frac{\partial G}{\partial n}\Big|_{T,P}\;\simeq\;\frac{\partial F}{\partial n}\Big|_{T,V}
\qquad(\text{삽입 고체: }P\Delta v\ll RT,\;F\,V)
\label{eq:sm-mubridge}
\end{equation}
```
- 문제 두 겹: (1) \eqref{eq:sm-mubridge} 한 줄에서 $F$ 가 분자(Helmholtz)와 괄호(Faraday)로, $V$ 가 아래첨자(부피)와 괄호(전위)로 동시에 두 뜻 — sec02a 가 "문맥으로 갈린다"고 세운 방침이 무력화되는 유일 지점이다. (2) 완전한 $F(T,V,N)$ 라면 $\partial G/\partial n|_{T,P}=\partial F/\partial n|_{T,V}$ 는 근사가 아니라 항등($G=F+PV$ 에 $P=-\partial F/\partial V$ 연쇄율)이라, ≃ 가 실제로 근사하는 곳은 **강체 격자 모형 $F$**(부피·탄성 일 탈락) 쪽임이 드러나지 않는다.
- 제안(대체 LaTeX — 산문+수식 괄호):
```latex
\S\ref{sec:sm-ensemble} 의 $\mu=\partial F/\partial N|_{T,V}$ 였다. 둘의 다리는 $G=F+PV$ 다 --- 완전한
$F$ 라면 두 미분은 항등으로 같고($\partial G/\partial n|_{T,P}=\partial F/\partial n|_{T,V}$: 역학 평형
$P=-\partial F/\partial V$ 의 연쇄율), 근사가 실제로 앉는 곳은 격자를 강체로 두어 부피 일을 떨어뜨린 모형
$F$ 쪽이다. 응축상 격자에 이온 1몰을 넣을 때의 $P\Delta v$ 몫(상압에서 부분몰 부피 수 cm$^3$/mol 기준
$\sim1$ J/mol 미만)은 $RT\sim2.5$ kJ/mol·전기 일 $F\times$수백 mV $\sim10^1$ kJ/mol 에 비해 무시되므로
\begin{equation}
\mu=\frac{\partial G}{\partial n}\Big|_{T,P}\;\simeq\;\frac{\partial F}{\partial n}\Big|_{T,V}
\qquad(\text{삽입 고체: }P\Delta v\ll RT)
\label{eq:sm-mubridge}
\end{equation}
```
  (괄호의 `,\;F\,V` 제거 — 전기 일 스케일은 산문이 담당; 식 안 $V$ 는 부피 하나로 통일. 라벨·자산 불변.)
- 근거: 재유도(§V-11) — $G(T,P,n)=F(T,V^*(T,P,n),n)+PV^*$ 미분에 $\partial F/\partial V=-P$ 대입 시 정확 상쇄. 수치: $\Delta v\approx3$ cm$^3$/mol(흑연 c축 $\sim10\%$ 팽창 규모), $P\Delta v|_{1\,\mathrm{atm}}\approx0.3$ J/mol.

### A03-M8 — $g_j^0$ 문장: "미분에는 그중 상수 기여만 남는다"의 오독 가능성
- 파일:행 = `ch1_sec02b_part0.tex:44–47` (유형 설명/수식화; P5 — 기호 $g_j^0$ 유지, 인수 표기 개정은 제안)
- 현행(축자):
```latex
(그림~\ref{fig:sm-mu} 가 이 함수의 세 얼굴이다.) 진행률 $\xi=1-\theta$ 로 옮기면 섞임 몫과
$\theta(1-\theta)=\xi(1-\xi)$ 몫이 모두 $\xi\leftrightarrow1-\xi$ 자리바꿈에 대칭(우함수)이라 조성 몫의 꼴이
불변이고, 상수$\cdot$직선 몫은 공통 접선$\cdot$곡률 판정에 기여하지 않으므로 이들을 하나의 기호 $g_j^0$ 로 모아 적는다 ---
$g_j^0$ 는 상수 몫과 $\xi$-직선 몫을 묶은 것이고, 미분에는 그중 상수 기여만 남는다:
```
- 문제: "미분에는 그중 상수 기여만 남는다"는 (의도: 미분 결과가 상수 $-\mu^0$ 하나) ↔ (오독: 상수항이 미분에서 살아남는다 — 거짓, 상수항은 미분에서 죽고 살아남는 것은 직선 몫의 계수)의 두 독해가 갈린다. 또 $g_j^0$ 를 "하나의 기호"로 적으면 상수처럼 보이지만 실제로는 $\xi$-아핀이다.
- 제안(대체 LaTeX — 해당 구절만):
```latex
(그림~\ref{fig:sm-mu} 가 이 함수의 세 얼굴이다.) 진행률 $\xi=1-\theta$ 로 옮기면 섞임 몫과
$\theta(1-\theta)=\xi(1-\xi)$ 몫이 모두 $\xi\leftrightarrow1-\xi$ 자리바꿈에 대칭(우함수)이라 조성 몫의 꼴이
불변이고, 남는 것은 $\mu^0\theta=\mu^0(1-\xi)$ 의 상수$+\xi$-직선(아핀) 몫뿐이다. 아핀 몫은 공통
접선$\cdot$곡률 판정에 기여하지 않으므로 하나의 기호 $g_j^0(\xi)\equiv\mu^0(1-\xi)$ 로 모아 적는다 ---
$\xi$ 로 한 번 미분하면 $g_j^0$ 몫은 상수 $-\mu^0$ 하나로 줄고, 두 번 미분하면 완전히 사라진다:
```
- 근거: 재계산 — $g(\theta)=\mu^0\theta+\cdots$ 에서 비대칭 몫은 $\mu^0\theta$ 뿐(섞임·$\Omega$ 몫은 우함수), $\theta=1-\xi$ 대입 시 $g_j^0(\xi)=\mu^0(1-\xi)$, $\dd g_j^0/\dd\xi=-\mu^0$(상수), $\dd^2 g_j^0/\dd\xi^2=0$. \S\ref{sec:hys-gap} 68–73행(선형 몫이 남긴 상수 $\mu^0$ 의 양변 상쇄 서술)과 정합.

### A03-M9 — 문턱 verifybox 에 평균장(BW) 정량 지위 가드 1문장
- 파일:행 = `ch1_sec02b_part0.tex:67–72` (유형 보완)
- 현행(축자):
```latex
\begin{verifybox}
극한 검산 --- $\Omega_j\to0$: $g''\ge4RT>0$ 로 항상 한 웰(\S\ref{sec:sm-lattice} 로 환원);
$\Omega_j\to2RT^-$: $g''(\tfrac12)\to0^+$ 로 바닥이 평탄해지되 아직 한 웰; $\Omega_j\to2RT^+$: 웰이 둘로
갈라지기 시작하고 $T_{c,j}=\Omega_j/2R$ 아래에서만 상분리가 존재한다(안정하다). 이 $\mu(\theta)$ 를 측정 전위에 결선하는
것이 다음 소절이다.
\end{verifybox}
```
- 문제: Part 0 은 문턱 $\Omega_j\le2RT$·$T_{c,j}=\Omega_j/2R$ 를 유도하지만, 이 값이 상관을 버린 평균장(Bragg–Williams)의 값이라 같은 미시 $u$ 에서 정확 해 대비 $T_c$ 를 과대평가하는 쪽으로 치우친다는 **정량 지위**가 어디에도 없다(sec02b 의 근사 경계 서술은 다클래스 곱에 한정). 문헌 $u$ 에서 $\Omega_j$ 를 계산해 쓰려는 독자가 오독할 지점 — 본 모델은 $\Omega_j$ 자체를 피팅 슬롯으로 쓰므로(표~\ref{tab:staging} "정규용액 추정 — 피팅 출발점") 한 문장이면 닫힌다.
- 제안(verifybox 마지막 문장 앞에 삽입):
```latex
지위 가드 --- 이 문턱·$T_{c,j}$ 는 상관을 버린 평균장(Bragg--Williams)의 값이라 같은 $u$ 에서 정확 해보다
$T_c$ 를 과대평가하는 쪽으로 치우친다 \cite{mcquarrie1976}; 본론이 쓰는 것은 문턱의 존재와 스케일이고
$\Omega_j$ 는 피팅 슬롯(표~\ref{tab:staging})이라 그 치우침은 피팅값에 흡수된다.
```
- 근거: 표준 결과(평균장은 요동 무시로 질서를 과안정 — 2D 정확 해 대비 MF $T_c$ 약 1.76배; §S 후보 onsager1944 DOI 검증됨, 등재는 마스터 선택 — 본 제안 자체는 기존 키 \cite{mcquarrie1976} 만 사용). `ch1_sec10_sum.tex:52–53` 의 "Ω 는 정규용액 추정(전이별 문헌 anchor 없음 --- 피팅 출발점)"과 정합.

### A03-M10 — fig:sm-occ 캡션: 온도 가족에서 $\tilde\varepsilon$·$U$ 동결의 명시
- 파일:행 = `ch1_sec02b_part0.tex:272–277` (유형 설명)
- 현행(축자):
```latex
\caption{단일 자리 점유의 전기화학적 재매개변수화(좌표는 식 그대로의 수치 평가). (a) 식~\eqref{eq:fermifn} 의
$\theta$ --- $\varepsilon=\mu$ 에서 $\tfrac12$, 낮은 $T$ 일수록 계단($\beta\to\infty$ --- $T\to0$ 극한이
계단 함수다), 높은 $T$ 일수록 완만. (b) 식~\eqref{eq:sm-logistic} 의 $\xi_\eq(V)$ ($U=0.085$ V, stage
$2\!\to\!1$ 초기값) --- 폭 $w=RT/F$ 가 $23.1/25.7/28.3$ mV($268/298/328$ K)로 $T$ 에 비례해 열리고, 회색
$\theta_\eq=1-\xi_\eq$ 와 중심 $V=U$ 에서 교차한다($\tfrac12$).}
```
- 문제: Part 0 자신이 $\tilde\varepsilon(T)$(내부 자유도 $q(T)$)와 뒤이어 §3 이 $U_j(T)$($\partial U_j/\partial T=\Delta S_{\rxn,j}/F$; $2\!\to\!1$ 은 $-0.166$ mV/K → 60 K 창에 $-10$ mV) 온도 의존을 강조하는데, 이 그림의 온도 가족은 (a) $\varepsilon$·(b) $U$ 를 온도 상수로 동결하고 폭만 변화시킨다. 동결 선언이 없어 fig:UjT 와 잇는 독자가 "왜 중심이 안 움직였나"를 묻게 된다.
- 제안(캡션 끝에 한 문장 추가):
```latex
두 패널 모두 자리·중심 모수($\varepsilon$ 곧 $\tilde\varepsilon$·$U$)는 온도 상수로 동결해 분포 함수형의
폭 $T$-의존만 분리했다 --- 중심 자체의 온도 이동($\partial U_j/\partial T=\Delta S_{\rxn,j}/F$)은
\S\ref{sec:center} 그림~\ref{fig:UjT} 소관이다.
```
- 근거: `ch1_sec03_center.tex` fig:UjT(중심의 온도 지도)와 역할 분담이 실제 설계 의도임을 두 그림 좌표에서 확인(본 그림 U=0.085 고정·좌표 재계산 §V-8 일치).

---

## L 등급 상세 (문체·표시)

### A03-L1 — 이중 부정: "정확히 $-FV$ 만큼 낮아진다"
- 파일:행 = 171. 현행(축자): `전위를 올리면 host 안 Li 의 화학퍼텐셜이 정확히 $-FV$ 만큼 낮아진다 --- ``$V$ 를 올리면 탈리튬화''가 이 한 줄이다.`
- 제안: `전위를 올리면 host 안 Li 의 화학퍼텐셜이 기준 금속 대비 정확히 $FV$ 만큼 낮아진다 --- ``$V$ 를 올리면 탈리튬화''가 이 한 줄이다.`
- 근거: \eqref{eq:sm-muV} 는 $\mu_\mathrm{Li}-\mu_\mathrm{Li}^\mathrm{metal}=-FV$ — "낮아지는 양"은 $+FV$(부호는 '낮아진다'가 이미 담음).

### A03-L2 — 무첨자 $U$ ↔ 첨자 $U_j$ 혼재 (eq:sm-eqcond 한 줄 안)
- 파일:행 = 173–175. 현행(축자): `\textbf{(c) 중간식 --- 상수 덩이를 $U$ 로 묶기.} 식~\eqref{eq:sm-muV} 의 상수 $\mu_\mathrm{Li}^\mathrm{metal}$` + `를 전이 중심 $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$ 로 재포장하면($s=+1$ --- \S\ref{sec:notation}` + `표의 유도 전용 고정 부호, 방향 부호 $\sigma_d$ 와 별개)`
- 제안: 괄호를 `(이하 한 전이의 $U\equiv U_j$·$\Delta G\equiv\Delta G_j$; $s=+1$ --- \S\ref{sec:notation} 표의 유도 전용 고정 부호, 방향 부호 $\sigma_d$ 와 별개)` 로 확장 — \S\ref{sec:sm-mf}(c) 의 "(이하 한 전이의 $\Omega\equiv\Omega_j$)" 장치와 동일 문법.
- 근거: \eqref{eq:sm-eqcond} 첫 식은 $U$, 둘째 식은 $U_j$ — 첨자 $j$ 의 도입 선언이 없다.

### A03-L3 — $z$(전하수) ↔ $z$(배위수) 국소 병기
- 파일:행 = 146. 현행(축자): `($z$ = 전하수, $\phi$ = 그 종이 있는 상의 정전 퍼텐셜)`
- 제안: `($z$ = 전하수 --- \S\ref{sec:sm-mf} 의 배위수 $z$ 와 별개, $\phi$ = 그 종이 있는 상의 정전 퍼텐셜)`
- 근거: 직전 소절이 $z$=배위수로 사용; §5 의 원거리 각주(`ch1_sec05_width.tex:285`)가 이미 3중 충돌을 인지 — 발생 지점 국소 병기가 저렴한 보강.

### A03-L4 — 문턱의 실척도 수치 병기
- 파일:행 = 64–66. 현행(축자): `$\Omega_j>2RT$ 면 가운데($g''<0$)가 언덕이 되어 두 골짜기가 생기고(그림~\ref{fig:sm-gxi}), 그 변곡점` + `(spinodal)의 닫힌 근과 거기서 자라는 히스테리시스 gap 은 \S\ref{sec:hys} 가 닫는다 --- Part 0 은 문턱까지만` + `놓는다.`
- 제안: 첫 구를 `$\Omega_j>2RT$($298.15$ K 에서 $2RT\approx4.96$ kJ/mol --- 표~\ref{tab:staging} 초기값 $6$--$13$ kJ/mol 이 모두 넘는 문턱) 면 가운데($g''<0$)가 언덕이 되어 두 골짜기가 생기고(그림~\ref{fig:sm-gxi}),` 로.
- 근거: $2RT=2\times8.3145\times298.15=4957.7$ J/mol(재계산); `tab:staging` Ω 열 6000–13000 J/mol. \S\ref{sec:width-w} 도 같은 수치 앵커를 씀 — Part 0 독자에게 선제 제공.

### A03-L5 — "정준($\langle N\rangle$ 고정)" → "정준($N$ 고정)"
- 파일:행 = 351–352. 현행(축자): `고정-함량 반전의 \emph{정의상 implicit formulation} 이며, 대정준($\mu$ 독립)$\to$정준($\langle N\rangle$` + `고정)의 Legendre-켤레 반전이다.`
- 제안: `고정-함량 반전의 \emph{정의상 implicit formulation} 이며, 대정준($\mu$ 독립)$\to$정준($N$ 고정)의 Legendre-켤레 반전이다.`
- 근거: 정준 앙상블의 정의는 입자수 $N$ 고정(평균이 아님); bgbox 는 "$N$ 을 고정한 정준 기술"로 옳게 적어 본문과 어긋난다. 본문 쪽을 고치면 bgbox 의존 없이 정합(제거 용이성 무영향).

### A03-L6 — 정규용액 A–B 표기와의 대응 각주
- 파일:행 = 27–30. 현행(축자): `이 한 모수로 혼합 자유에너지를 적는 모형이` + `\emph{정규용액}이고, 본론 표~\ref{tab:staging} 의 $\Omega_j$ 와 Chapter 2 의` + `$\Omega_j^\mathrm{cat}$(표 밖 --- 피팅 배정 전제, \S\ref{sec:lco-hys}) [J/mol]이 정확히 이 슬롯이다.`
- 제안(각주 추가 — "정규용액이고" 직후):
```latex
\emph{정규용액}이고\footnote{A--B 혼합 표기의 정규용액 $\Omega=zN_A[u_{AB}-\tfrac12(u_{AA}+u_{BB})]$ 와의
대응은 A $=$ 점유, B $=$ 공위, $u_{AA}=u$·$u_{AB}=u_{BB}=0$ --- 대입하면 $\Omega=-\tfrac z2N_Au$ 로
식~\eqref{eq:sm-omega} 그대로다.},
```
- 근거: 재계산 — $zN_A[0-\tfrac u2]=-\tfrac z2N_Au$ 일치. 정규용액 문헌에서 온 독자의 표준 환산 질문 선제.

### A03-L7 — MSMR 계보 포인터 (선택)
- 파일:행 = 283–287. 현행(축자): `실제 전극은 전이 하나가 아니라 staging 이 나누는 여러 전이를 동시에 갖는다 --- 이 소절은 두 결과를 전이` + `여럿으로 한 줄 넓혀, 본론과 Part T 가 중심식으로 쓰는 전하 보존 음함수가 이 대정준 구조의` + `\emph{제약 반전}(constrained inversion)임을 보인다.`
- 제안: 문장 뒤에 `(이 다클래스 서식의 문헌 계보 --- MSMR --- 대응은 Ch.2 \S\ref{sec:lco-code-msmr} 이 닫는다.)` 1구 추가.
- 근거: `ch1_sec17_msmr.tex` 의 `sec:lco-code-msmr` 가 ch2 빌드에 포함됨을 확인; sec02b 가 이미 LCO 장 라벨(\S\ref{sec:lco-hys})을 xr 로 참조하는 관행과 동일 메커니즘. 선택 사항(무추가도 결함 아님).

### A03-L8 — 반전 지위 산문의 사상(map) 한 줄 병기 (선택 수식화)
- 파일:행 = 348–350. 현행(축자): `반전의 지위도 여기서 정확해진다: 대정준에서는` + `$\mu$(결선하면 $V$)가 독립변수여서 $\langle N\rangle(\mu)$ 가 결정되는 반면, 측정은 거꾸로 통과 전하($\bar` + `x$)를 고정하고 그에 맞는 전위를 푼다.`
- 제안(산문 유지 + 직후 무번호 디스플레이 병기):
```latex
\[
\underbrace{\mu\ (\text{결선하면 }V)\ \longmapsto\ \langle N\rangle(\mu)}_{\text{대정준(순방향)}}
\qquad\text{vs}\qquad
\underbrace{\bar x\ \longmapsto\ U_\mathrm{oc}(\bar x,T)\ \text{: 식~\eqref{eq:sm-mc-balance} 의 유일근}}_{\text{측정(제약 반전)}}
\]
```
- 근거: 산문 3행의 대구 구조를 시각화 — 선택 사항(문체 취향의 영역).

---

## §V 검증 로그 (재계산·재유도 — 전 항목 독립 수행)

1. **eq:sm-mf/omega**: $M\theta$ 점유 × 평균 $z\theta$ 점유 이웃 × $u$ ÷ 2 = $(Mz/2)u\theta^2$ ✓. 항등 분해 $(z/2)N_Au\theta^2=(z/2)N_Au\theta-\underbrace{(z/2)N_Au}_{=-\Omega}\theta(1-\theta)$ ✓ — $u<0\Leftrightarrow\Omega>0$(상분리 경향) 격자기체 표준 부호와 일치. A–B 환산(§L6)도 일치.
2. **eq:mu/gxi/우함수**: $\dd[\theta\ln\theta+(1-\theta)\ln(1-\theta)]/\dd\theta=\ln[\theta/(1-\theta)]$, $\dd[\theta(1-\theta)]/\dd\theta=1-2\theta$ ✓. $f(\xi)=f(1-\xi)\Rightarrow f'(1-\xi)=-f'(\xi)$ ✓(§hys 68–73행의 사용처와 정합).
3. **eq:sm-thresh**: $g''=RT/[\xi(1-\xi)]-2\Omega_j$; $\min_\xi RT/[\xi(1-\xi)]=4RT$($\xi=\tfrac12$) ⇒ $\Omega_j\le2RT\Leftrightarrow g''\ge0$(등호 한 점), $T_{c,j}=\Omega_j/2R$ ✓.
4. **fig:sm-gxi 좌표**(표본 8점): $\xi{=}0.5$ 값 $-0.6931/-0.4431/-0.1931/-0.0681/+0.0569$($\Omega/RT{=}0,1,2,2.5,3$) ✓; $\Omega{=}3RT$ spinodal $\xi_s=\tfrac12[1\pm1/\sqrt3]=0.21132/0.78868$, $f/RT=-0.0157$ ✓; $\Omega{=}0,3RT$ 의 $\xi{=}0.07$ 값 $-0.2536/-0.0583$ ✓.
5. **fig:sm-mu 좌표**: $\Omega{=}0$, $\theta{=}0.02$: $\ln(0.02/0.98)=-3.892$ ✓; $\Omega{=}2RT$, $\theta{=}0.02$: $-1.972$ ✓; $\Omega{=}4RT$ 극값 $\theta_s=\tfrac12[1\pm1/\sqrt2]=0.1464/0.8536$, 값 $\pm1.0657$ ✓. **거울 관계**: $h(x)=\ln[x/(1-x)]+(\Omega/RT)(1-2x)$ 는 $x{=}\tfrac12$ 홀함수 ⇒ $-h(1-\xi)=h(\xi)$ — "θ=1−ξ·부호 반전 거울, 같은 ±1.066" 주장 ✓ (`fig:hysloop` 좌표 $(0.146,+1.066)/(0.854,-1.066)$ 대조 일치).
6. **전기화학 결선**: \eqref{eq:sm-workbal}$-$\eqref{eq:sm-refbal} ⇒ \eqref{eq:sm-muV} ✓; $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$ 대입 ⇒ \eqref{eq:sm-eqcond}($s{=}+1$)·$\Delta G_j=-sFU_j$·$U_j>0\Leftrightarrow\Delta G_j<0$ ✓; \eqref{eq:sm-muideal} 대입·로그 반전 ⇒ \eqref{eq:sm-logistic} ✓(여집합 대수 $1-\mathrm{logistic}[x]=\mathrm{logistic}[-x]$ ✓); 자리당↔몰당 지수 환산 $\beta\Delta\mu\to(\mu^0-\mu_\mathrm{Li})/RT\to+sF(V-U)/RT$ ✓.
7. **항목 (i)–(iii)**: (i) $\sigma_d$ 지수 반전 = 여집합 relabel(종 $\xi(1-\xi)$ 불변) ✓ — §1 "작용처 셋(분극·분기·꼬리)" 규정과 정합; (ii) 평형비 $\xi/(1-\xi)=e^{sF(V-U)/RT}$ — §5 detailed balance \eqref{eq:db}($r^+/r^-=e^{\mathcal A_j/RT}$, $\mathcal A_j=sF(V-U_j)$) 정지점과 일치 ✓; (iii) $\theta{=}1{-}\xi$ 치환·부호 반전 ⇒ $RT\ln[\xi/(1-\xi)]+\Omega_j(1-2\xi)=sF(V-U)$ ✓, 비단조 ⟺ $\Omega_j>2RT$ ✓, §hys \eqref{eq:Veq} 와 항 배치 일치 ✓.
8. **fig:sm-occ**: $w=RT/F=23.09/25.69/28.28$ mV(268.15/298.15/328.15 K) ✓; (b) $\xi_\eq(0\,\mathrm V)=0.02464/0.03529/0.04716$, $\xi_\eq(0.2\,\mathrm V,298\,\mathrm K)=0.9887$ ✓; (a) $x{=}1$ 에서 $0.1192/0.2689/0.3775$($T_0/2,T_0,2T_0$) ✓. $U=0.085$ V = §3 수치 예시($\Delta H=-13000$·$\Delta S=-16$ ⇒ $U(298)=0.0853$ V)와 정합 ✓.
9. **다클래스·유일근**: \eqref{eq:sm-mc-factor}→\eqref{eq:sm-mc-occ}→$Q\bar x=\sum Q_j\xi_j$ 대수 ✓($e=F/N_A$); \eqref{eq:sm-mc-fluc} 독립 자리 전제로 ✓; 경계 $U_\mathrm{oc}\to\mp\infty$ ⇒ 좌변 $\to0/Q$ ✓(∓ 짝 순서 정확); IVT+순증 ⇒ $\bar x\in(0,1)$ 유일근 ✓. **자기무모순 평균장 확장**(M4·M5 근거): $\dd\mu/\dd\theta=RT/[\theta(1-\theta)]-2\Omega_j$ ⇒ $\partial\theta/\partial\mu$ 가 인자 $[1-2\Omega_j\theta(1-\theta)/RT]^{-1}$ 를 얻고, $\theta(1-\theta)\le\tfrac14$ ⇒ $\Omega_j\le2RT$ 전역 양성(등호 한 점 수직 접선) — 유일근 문턱까지 유지, 분산 가법 등식은 $\Omega_j=0$ 한정.
10. **bgbox 1/√M**: $\mathrm{var}=O(M)$·$\langle N\rangle=O(M)$ ⇒ 상대 요동 $\sim1/\sqrt M$ ✓; $\sigma_{\bar x}^2=\mathrm{var}/M^2\le1/(4M)$ 균일 ✓; $M$ 수치 — LiC$_6$ 자리밀도 $\approx1.9\times10^{22}$ cm$^{-3}$ ⇒ 1 μm$^3$ 에 $\approx1.9\times10^{10}$ 자리 ⇒ "$M\gg10^8$" ✓; 강상관 창(공존 $\mu$)의 쌍봉 분포 ⇒ 상대 요동 $O(1)$ 잔존 ✓.
11. **eq:sm-mubridge**: $G(T,P,n)=F(T,V^*,n)+PV^*$, $\partial G/\partial n|_{T,P}=(\partial F/\partial V+P)\partial V^*/\partial n+\partial F/\partial n|_{T,V}=\partial F/\partial n|_{T,V}$(항등) — ≃ 의 실제 자리는 강체 격자 모형 $F$; $P\Delta v|_{1\,\mathrm{atm}}\approx0.3$ J/mol ≪ $RT=2479$ J/mol ≪ $F\times0.1$ V $=9.6$ kJ/mol ✓.
12. **Nernst·온도 환산**: 로그 반전 ⇒ \eqref{eq:sm-nernst} ✓; $\Delta G=-FU$ 의 Gibbs–Helmholtz ⇒ $\dd U_j/\dd T=\Delta S_{\rxn,j}/F$(정확) — §3 \eqref{eq:Uj} 박스와 일치 ✓.
13. **전달·"글자까지" 주장 대조**: \eqref{eq:sm-eqcond}↔`ch1_sec03_center.tex` \eqref{eq:eqcond} 동일 ✓; \eqref{eq:sm-mc-balance}↔`ch2_sec05_mixing.tex` \eqref{eq:implicit} 동일 ✓(양쪽 ★좌표 $\bar x$ 규약 동일); N6 보존식 문구(`ch1_sec06_eqpeak.tex:8`) 동일 ✓; \eqref{eq:muV}·\eqref{eq:Vxi}·\eqref{eq:Z1}(Part T) 형태 일치 ✓; $\Omega_j^\mathrm{cat}$ "표 밖"(`ch1_sec13_lcohys.tex:35`) ✓; keybox 사다리의 전 라벨 실재 ✓.

---

## §S 문헌 서치 (하이쿠 서브에이전트 위임 — DOI 실검증분만, 기억 서지 없음)

검증 방법: 서브에이전트가 Crossref API 로 DOI 메타데이터를 실조회·대조(2026-07-17). 아래 2건 모두 **검증됨** — V1 원장 등재 여부는 마스터 선택(본 보고의 제안 중 M9 는 기존 키 `mcquarrie1976` 만으로 성립하며, 아래는 정밀 인용을 원할 때의 선택 후보).

| 후보 | DOI | Crossref 확인 필드 | 판정 | 용처(제안) |
|---|---|---|---|---|
| Onsager, "Crystal Statistics. I. A Two-Dimensional Model with an Order-Disorder Transition" | 10.1103/PhysRev.65.117 | Lars Onsager / Physical Review / 65 / 117–149 / 1944 | 검증됨(메타데이터 전체 일치) | A03-M9 의 "정확 해 대비 MF $T_c$ 과대" 정밀 앵커(선택) |
| Bragg & Williams, "The effect of thermal agitation on atomic arrangement in alloys" | 10.1098/rspa.1934.0132 | W. L. Bragg, E. J. Williams / Proc. R. Soc. Lond. A / 145 / 699–730 / 1934 | 검증됨(메타데이터 전체 일치) | \S\ref{sec:sm-mf}(a) "Bragg--Williams" 명명의 원전 병기(선택 — 현재 무인용; 기존 키 hill1960/mcquarrie1976 병기로도 충분) |

---

## 말미 정리

### 4-tier 분류
- **확정(재계산·원문 대조 완료)**: §V 1–13 전 항목(수식·그림 좌표·부호·전달식·"글자까지" 주장); M1(정의 충돌의 존재)·M4(산문↔전시식 불일치의 존재)·M5(응답 인자 유도)·M6(균일 상계 유도)·M7(항등성·기호 충돌)·M8(오독 구조)·L1–L6 의 계산 근거; §S 2건 DOI 검증.
- **추정(물리 관행 기반 판단)**: M2(무전류 균일 전제의 명시 필요성 — 상쇄 자체는 평형에서 정확)·M9 의 "치우침 방향 = 과대평가"의 일반성(격자기체/이징 표준 결과 — 구체 배율은 격자 의존)·M10(독자 혼동 예측)·L7(포인터의 효용).
- **미검증**: 없음(본 절 범위에서 접근 불가한 주장 없음). 단, tab:staging Ω 초기값의 물리적 타당성 자체는 본 절 밖(§10 tier 소관)이라 검토 대상에서 제외.
- **제안 지위**: 전 제안은 대체·보강만(자산·수식·라벨 삭제 없음); P5 에 따라 기호 개정(M8 의 $g_j^0(\xi)$ 인수 표기 등)은 '제안'이며 채택은 마스터 소관; GS-1/GS-2 무접점·bgbox 독립성 유지(M6 는 박스 내부 자족 대체, L5 는 박스 의존을 피한 설계).

### 무발견 축 (검토했으나 문제 없음)
1. **부호 사슬**: $s{=}+1$ 전 경로(muV→eqcond→logistic→mc-balance→nernst), ∓/0/Q 짝, "V↑⇒탈리튬화", 거울 ±1.066 — 전부 재계산 일치, 오류 없음.
2. **그림 수치**: 세 그림(fig:sm-gxi·sm-mu·sm-occ) 좌표 표본 30여 점 재계산 — "식 그대로의 수치 평가" 주장 그대로, 편차 없음.
3. **전달식 정합(P3-6)**: §3(eq:eqcond)·§4(eq:Veq·spinodal)·§5(eq:db·xieq·이중지위·dist)·§6(N6 보존식)·§10(tab:staging)·Part T(eq:Z1·muV·Vxi·implicit·synthesis)와의 결선 전건 일치; "글자까지 같다" 2건 축자 확인.
4. **순환 의존 진단(P3-3·4)**: $U_\mathrm{oc}$ 음함수의 "정의상 implicit formulation" 분류 명시 확인 — 적정(M4 는 이 분류를 평균장 되먹임까지 확장하자는 보강이지 지적 아님).
5. **명칭 규율(P3-7)**: ver.N/Chapter 혼동 없음(본 절은 Part 0·Part T·N-노드 명명만 사용).
6. **라벨 무결성**: 본 절이 참조하는 전 라벨(동일 문서 24종·xr 2종) 실재 확인 — 깨진 참조 없음.
7. **인용 규율**: 본 절 내 \cite 2회(hill1960·mcquarrie1976) 모두 V1 원장 승계 키 — 위반 없음.
8. **bgbox[V22-SM2-B] 독립성**: 본문→박스 의존 없음(박스가 본문 식을 참조하는 단방향) — 제거 용이성 현상 유지 확인.
