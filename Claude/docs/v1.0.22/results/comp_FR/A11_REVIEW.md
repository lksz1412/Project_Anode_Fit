# A11_REVIEW — FR-A11 심층 검토 (Part T §0 서 + §2.1 격자기체 분배함수)

- 검토 창: FR-A11 (v1.0.22 대공사, BRIEF_FR_A.md 규율 준수 — 보고 전용·소스 불변·git 불변·`Codex/` 미접근)
- 대상 (전문 정독):
  - `Claude/docs/v1.0.22/_sections/ch2_sec00_intro.tex` (81줄 전문)
  - `Claude/docs/v1.0.22/_sections/ch2_sec01_partition.tex` (145줄 전문)
- 소속 확인: 두 파일은 **ch1_graphite_v1.0.22.tex 빌드의 Part T(흑연 열특성부)** 소속 (마스터 :36–37 input 확인). 파일명 `ch2_` 는 역사적 명칭 — ch2_lco 빌드(LCO 챕터)와 무관.
- 참조 원문 확인(read-only): ch1_sec01_n0n1(§notation) · ch1_sec02a/02b(Part 0: sm-site·sm-lattice·sm-mf·sm-electro·sm-mc) · ch1_sec03_center · ch1_sec04_hys(eq:spinodal) · ch1_sec05_width(eq:logisticsolve·eq:wbase·eq:xieq·이중지위) · ch2_sec02_config · ch2_sec03_vibel · ch2_sec04_einstein(고온 극한) · ch2_sec05_mixing(파생 A–D 전문) · ch2_sec06_limits · ch2_sec07_revheat(전문) · ch1v22_partT_divider · ch1v22_bib · ch2_lco 마스터(input 목록) · V1022_REFERENCE_LEDGER.md · ch1 빌드 log(미해소 참조 0건 — "undefined" 3건은 전부 폰트 셰이프 경고).
- 표기 규약: 총괄표 셀 안의 개행은 `<br>` 로 표시. **기계 매칭용 축자 정본은 §2 등급별 상세의 코드펜스**(개행 원형 보존)이다.

---

## 1. 발견 총괄표

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|---|---|---|---|---|---|---|
| A11-05 | ch2_sec01_partition.tex:34–36 | 논리(수식↔산문 불일치) | **H** | 식~\eqref{eq:occ} 는 구조상 \emph{Fermi--Dirac<br>함수}와 동형이다 --- 자리당 2-상태(채움/빔)가 전자 준위의 점유/공위와 같은 대수 구조를 낳으며, 다른 점은<br>``입자''가 페르미온 전자가 아니라 Li 이온이고 단일 준위 에너지가 $\varepsilon_0-\mu$ 라는 것뿐이다. | §2-H1 참조 | FD 는 $f(E)=1/(e^{\beta(E-\mu)}+1)$ — 대응은 $E\leftrightarrow\varepsilon_0$ 이지 "준위 에너지 $=\varepsilon_0-\mu$" 가 아님($\varepsilon_0-\mu$ 는 준위 에너지가 아니라 지수 인자). Part 0 은 옳게 서술: ch1_sec02a:158–159 "$f(E)=\dots$ 에서 $E$ 자리에 $\varepsilon_0$ 이 앉은 것과 동형". 동형 문장은 §vibel 수용의 근거 문장이라 하중 있음 |
| A11-01 | ch2_sec00_intro.tex:19–21 | 논리(전제 불명시·타 절 문면 충돌) | M | 이 비선형 모양은 ``전이마다 상수 $\Delta S_{\rxn,j}$ 를 가정''하는 것만으로는 재현되지<br>않는다 --- 상수 값만으로는 SOC 축 위에서 봉우리$\cdot$골(경계의 발산형 구조)을 만들 자유도가 없고,<br>부호 교차도 매끄러운 블렌드가 아니라 계단으로만 나오기 때문이다. | §2-M1 참조 | ch2_sec05:80–83(eq:weighted): **상수** $\Delta S_{\rxn,j}$ 를 가중해도 "계단이 아니라 연속 블렌드"; ch2_sec06 keybox: "전이당 상수 표준값 $+$ 분포만으로 측정급 곡선이 나온다". 즉 매끄러운 부호 교차는 상수+겹침가중으로 이미 나오고, 상수가 못 만드는 것은 발산형 구조다. 현행 둘째 논거는 '겹침 무시' 전제를 숨긴 채 §2.5·§2.6 headline 과 표면 모순 |
| A11-02 | ch2_sec00_intro.tex:25–28 | 보완(부호 규약 미명시) | M | \[<br>\dot Q_\rev=-I\,T\,\frac{\partial U_\oc}{\partial T}=-\frac{I\,T}{F}\,\Delta S(x)<br>\]<br>은 한 충전상태에서 다른 충전상태로 넘어갈 때 \emph{이 분포를 재배열하면서 주고받는 열}이다. | §2-M2 참조 | $I$ 부호 규약은 ch2_sec07:21 "($I>0$ 방전, …)" 에서야 등장하고, 같은 절 :48–53 은 이 "방전" 라벨이 Part I 라벨(방전=탈리튬화, $\sigma_d{=}+1$)과 **반대 화학 방향**임을 CRITICAL 로 경고. 첫 노출인 서두가 규약 없이 부호식을 내보내면 그 경고 이전까지 오독 창이 열림 |
| A11-07 | ch2_sec01_partition.tex:52–56(·63) | 보완(중심식 앵커 부재·용어 동요) | M | 이제 화학을 넣는다. Li 가 자리에 들어가는 전기화학 반응의 전기화학 퍼텐셜은 셀 전위에 선형으로 묶인다:<br>\begin{equation}<br>\mu \;=\; \mu^0 \;-\; s\,F\,(V-U_j),<br>\label{eq:muV}<br>\end{equation} | §2-M3 참조 | 동일 관계가 이미 두 곳에서 확립됨: ch1_sec03_center eq:eqcond "$\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$", ch1_sec02b:139 소절 제목 "$\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 와 평형 점유 logistic". §2.1 은 자기완결 재놓기 선언(:12–14)에도 이 식만 무앵커. 또 :52 "전기화학 퍼텐셜" ↔ :63 "몰 화학퍼텐셜" 로 같은 $\mu$ 의 호칭 동요(중성 삽입종이라 값은 일치하나 sec:center (b) 의 $\tilde\mu$/$\mu$ 구분 정밀도와 어긋남) |
| A11-08 | ch2_sec01_partition.tex:58–61(각주) | 논리(열거 누락→표면 모순) | M | \footnote{★부호 각주(오독방지). 이 $s{=}+1$ 은 방향 부호<br>$\sigma_d$(\S\ref{sec:notation} --- 분극$\cdot$분기$\cdot$꼬리 세 작용처 전용, $\pm1$)와는 \emph{별개}다. 평형 관계에는<br>항상 $s{=}+1$ 이 들어가며, $\sigma_d{=}-1$ 을 이 식에 기계적으로 대입하면 점유와 진행률이 뒤바뀌는<br>\emph{여집합 오류}가 생긴다(종은 좌우 대칭이라 봉우리 자체는 멀쩡해 보여 오류가 잠복한다).} | §2-M4 참조 | "세 작용처 전용"이 사실과 어긋남: $\sigma_d$ 는 **평형 진행률 logistic 인자에도** 들어감 — ch1_sec01:29 "$\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$", ch1_sec05 eq:xieq "$\xi_{\eq,j}=1/(1+\exp[-\sigma_d(V-U_j^{\,d})/w_j])$". 또 "평형 관계에는 항상 $s{=}+1$" 은 평형식 eq:xieq 의 $\sigma_d$ 와 표면 충돌 — 그 $\sigma_d$ 가 부호 변경이 아니라 여집합 좌표 교환(ch1_sec05:276–277 "$s\to\sigma_d$ 치환은 여집합 교환과 동치")임을 밝혀야 각주의 경고가 완결됨 |
| A11-09 | ch2_sec01_partition.tex:63–76 | 수식화(산문→식·중복 정리) | M | 식~\eqref{eq:muV} 의 $\mu$ 는 몰 화학퍼텐셜이고 식~\eqref{eq:occ} 의 지수<br>$\beta(\varepsilon_0-\mu)$ 는 자리당이므로, 후자의 분자$\cdot$분모를 $N_A$ 배 해 몰 척도로 맞춘다: 분자는<br>$N_A\varepsilon_0-N_A\mu$ 인데 $N_A\varepsilon_0\equiv\mu^0$(…)이고 $N_A\mu$ 가 식~\eqref{eq:muV} 의 몰 $\mu$ 이므로 $\mu^0-\mu=sF(V-U_j)$(기준 $\mu^0$ 가<br>상쇄된다), 분모는 $N_A\kB T=RT$ 다. (+ :74–76 의 동일 환산 재설명) | §2-M5 참조 | 한 환산을 산문 두 벌(:63–67, :74–76)로 반복 — 핵심 사슬 $\beta(\varepsilon_0-\mu)=(\mu^0-\mu)/RT=sF(V-U_j)/RT=(V-U_j)/w$ 를 한 줄 display 로 세우면 눈으로 검산 가능해지고 두 산문이 각주 수준으로 준다. 재유도 통과(§3-체크 5) — 내용 자체는 옳음 |
| A11-10 | ch2_sec01_partition.tex:85–86(keybox) | 보완(오귀속 경계 — 분류 근거) | M | \emph{두-상 전이}($\Omega_j>2RT$ --- 흑연 staging 의 $2\mathrm L\!\to\!2\cdot<br>2\!\to\!1$)에는 이 유도가 닿지 않아 폭은 현상학적 자유 피팅 파라미터가 된다. | §2-M6 참조 | 문턱 부등식이 두 전이를 지목하는 듯 읽히나, 같은 빌드 두 곳이 명시 반박: ch1_sec05:307–308 "네 전이는 초기값 $\Omega_j$ 가 **모두** $2RT$ 보다 커", ch2_sec05 각주(:169–173) "지목하는 근거는 문턱 부등식이 아니라 실측 plateau$\cdot$staging 문헌의 상평형 \cite{dahn1991,ohzuku1993}". §2.1 keybox 만 이 한정 없이 병치 — 여기만 읽는 독자에게 오귀속 위험(문면 대조 확정) |
| A11-11 | ch2_sec01_partition.tex:100–101 | 설명(재편 후 명칭 정합) | M | 엔트로피에서 온다는 것이 이 장의 첫 매듭이며, 그 매듭을 다음 절이 명시적으로 푼다. | §2-M7 참조 | v1.0.22 재편으로 구 Ch2 전량이 Ch1 의 Part T 로 편입(마스터 :34 주석). 병합 빌드에서 "이 장"=Chapter 1 로 읽히면 "첫 매듭" 주장은 거짓(Part I 의 매듭들이 선행). Part T 한정 주장이므로 "본 파트" 로 좁혀야 정확. 참고: :57–58 의 "본 장의 유도 전용 고정 부호 $s$" 는 장 전체($U_j$ 정의 관례 — sec:center·sec:hys)에서 실제로 쓰이므로 그대로 두는 것이 옳음(일괄 치환 금지) |
| A11-13 | ch2_sec01_partition.tex:115–120 | 논리(유도 비약 — $U_j$ 출처) | M | 평형 전위는 $\theta$<br>1몰 삽입당 자유에너지 변화 $\partial g/\partial\theta$ 를 전위로 환산한 것이므로, 식~\eqref{eq:BW} 를 미분하면 | §2-M8 참조 | 재유도하면 식~\eqref{eq:BW} 문면에는 $\theta$-선형 자리에너지 항이 없어 $\partial g/\partial\theta=RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)$ — 여기서 eq:Veq_BW 의 $U_j$ 는 나올 수 없음. $\mu(\theta)=\mu^0+\partial g/\partial\theta$ 로 두고 식~\eqref{eq:muV} 와 등치해야 닫힘(그러면 정확히 eq:Veq_BW — §3-체크 8 재유도 통과). 다리 한 문장 부재 |
| A11-03 | ch2_sec00_intro.tex:32–33 | 설명($\theta$/$\xi$ 규약 정합) | L | 거기서 점유 분포 $\avg{n}$ 을 얻는데 이것이 바로 Part I<br>\S\ref{sec:width} 의 logistic 평형 점유의 통계역학적 기원임을 보인다. | §2-L1 참조 | Part I §width 의 대상은 평형 **진행률** $\xi_\eq$(점유의 여집합 — ch1_sec05:375 소절 제목). "평형 점유" 호칭은 §2.1 keybox·§config(:66–68 "두 이름을 끝까지 구분해야 한다")가 경계하는 $\theta$/$\xi$ 혼용의 첫 노출 |
| A11-04 | ch2_sec00_intro.tex:53–54 | 설명(양화 과대) | L | 이 사슬이 본 파트 전체의 목차 설계 앵커다 --- 이후 모든 절은<br>이 다섯 마디 중 하나를 여는 일이며, | §2-L2 참조 | §method(방법론 출구)·§closing 은 다섯 마디 밖(입력 조달·맺음). "모든 절" 은 과대 양화 |
| A11-06 | ch2_sec01_partition.tex:25–26 | 설명(주장 미전시) | L | 자리의 평균 점유는 정의상 두 상태의 확률 가중 평균, 곧 분배함수에 대한 로그 미분이다. | §2-L3 참조 | "로그 미분" 은 변수 명시 없이는 검증 불가 — $\avg{n}=\kB T\,\partial\ln\Xi_1/\partial\mu$ (Part 0 식 eq:sm-gc 셋째 식, ch1_sec02a:146–147 교차검증 경로와 동일). 한 줄 명시로 닫힘 |
| A11-12 | ch2_sec01_partition.tex:105–106 | 보완(Part 0 앵커 누락) | L | 이 상호작용을 평균장으로 다루는 것이 Bragg--Williams 근사다 \cite{huggins2009,<br>bazant2013}. | §2-L4 참조 | 같은 모형이 Part 0 \S sm-mf(ch1_sec02b:5 "평균장 상호작용 --- 정규용액 $\mu(\theta)$·$g(\xi)$ 와 이중웰 문턱")에 이미 있음. §2.1 은 sm-site(2회)·sm-lattice 는 앵커하면서 sm-mf 만 무앵커 — 재놓기 관행 비대칭 |
| A11-14 | ch2_sec01_partition.tex:123·131 | 설명(논거 반 문장 생략) | L | 임계 조건은 등온선 기울기가 처음 $0$ 이 되는 곳, 곧 … 이 중앙 $\theta=\tfrac12$ 에서 $0$ 이 되는 $\Omega=2RT$ 다. | §2-L5 참조 | 왜 "처음"이 중앙인지는 $1/[\theta(1-\theta)]$ 의 최소($=4$, $\theta=\tfrac12$) 때문 — eq:slope_BW 에 이미 들어 있으나 산문 반 문장이 비어 있음. $T_c=\Omega/2R$ 온도 독법도 공짜 보강 |
| A11-15 | ch2_sec01_partition.tex:6–7 | 보완(원전 서지) | L | 흑연 격자에 Li 이온이 삽입되는 문제는<br>\emph{격자기체}(lattice gas)로 모형화된다 \cite{newman,huggins2009}: | §2-L6 참조 | Part 0(ch1_sec02a:156–158·srcbox)은 삽입 전극 격자기체의 **적용 원형**을 mckinnon1983 으로 못박음 — §2.1 로 직행하는 독자를 위해 같은 키(기존 bib 등재분) 병기가 정합. 신규 문헌 아님 |
| A11-16 | ch2_sec01_partition.tex:8–10 | 보완(독자 질문 선제) | L | 자리들은 전해질을 통해 Li<br>저장조(상대극 Li 금속)와 평형을 이루므로, 전기화학 퍼텐셜 $\mu$ 가 고정된 \emph{대정준}(grand-canonical)<br>문제다. | §2-L7 참조 | "실제 운용은 정전류(전하 고정)인데 왜 $\mu$-고정인가" 는 표준 독자 질문 — 답(전하 보존의 대정준 반전·유일근)은 Part 0 sm-mc(eq:sm-mc-balance)와 §2.5 eq:implicit 에 있음. 반 문장 포인터로 선제 가능(P3-2 정합: 전하 보존이 중심식임을 이 지점에서 상기) |

---

## 2. 등급별 상세 (축자 정본 + 완성 LaTeX 제안)

### H (1건)

#### §2-H1 = A11-05 — FD 동형 문장의 "준위 에너지 $\varepsilon_0-\mu$" 오서술

현행 축자 (ch2_sec01_partition.tex:33–37):
```latex
가 되는데, 마지막 등식은 분자$\cdot$분모를 $e^{-\beta(\varepsilon_0-\mu)}$ 로 나눈 것이다. 이 $\avg{n}$ 은 자리가
채워질 확률 $p_1$ 그 자체이고, 빌 확률은 $p_0=1-\avg{n}$ 이다. 식~\eqref{eq:occ} 는 구조상 \emph{Fermi--Dirac
함수}와 동형이다 --- 자리당 2-상태(채움/빔)가 전자 준위의 점유/공위와 같은 대수 구조를 낳으며, 다른 점은
``입자''가 페르미온 전자가 아니라 Li 이온이고 단일 준위 에너지가 $\varepsilon_0-\mu$ 라는 것뿐이다. 이 동형이
뒤에서 electronic 엔트로피(\S\ref{sec:vibel})를 같은 분포 언어로 받는 근거가 된다.
```

제안 (문장 대체 — 3·4행만):
```latex
함수}와 동형이다 --- 자리당 2-상태(채움/빔)가 전자 준위의 점유/공위와 같은 대수 구조를 낳으며, 다른 점은
``입자''가 페르미온 전자가 아니라 Li 이온이고, 준위 스펙트럼 $E$ 자리에 단일 준위 $\varepsilon_0$ 하나가
앉아 지수가 $\beta(\varepsilon_0-\mu)$ 로 닫힌다는 것뿐이다(Part 0 \S\ref{sec:sm-site} 의 같은 대응). 이 동형이
```

근거(재유도): FD $f(E)=1/(e^{\beta(E-\mu)}+1)$ 에 대해 식 eq:occ 는 $E\mapsto\varepsilon_0$ 대입과 동형. "단일 준위 에너지가 $\varepsilon_0-\mu$" 로 읽으면 $f=1/(e^{\beta(\varepsilon_0-\mu-\mu)}+1)$ 꼴의 이중 감산이 함의되어 물리 오서술($\varepsilon_0-\mu$ 는 준위 에너지가 아니라 대정준 지수 인자). Part 0 의 올바른 문장(ch1_sec02a:158–159)과도 불일치. 이 문장은 §vibel(electronic FD)을 "같은 분포 언어로 받는 근거"로 선언된 하중 문장이므로 H. 수식 자체(eq:occ)는 무결 — 산문만 수리.

### M (8건)

#### §2-M1 = A11-01 — "상수 가정 → 계단" 논거의 전제 불명시

현행 축자 (ch2_sec00_intro.tex:19–21):
```latex
치솟는다. 이 비선형 모양은 ``전이마다 상수 $\Delta S_{\rxn,j}$ 를 가정''하는 것만으로는 재현되지
않는다 --- 상수 값만으로는 SOC 축 위에서 봉우리$\cdot$골(경계의 발산형 구조)을 만들 자유도가 없고,
부호 교차도 매끄러운 블렌드가 아니라 계단으로만 나오기 때문이다.
```

제안 (둘째 논거를 전제 명시형으로 대체 + §limits 판정 선제):
```latex
치솟는다. 이 비선형 모양은 ``전이마다 상수 $\Delta S_{\rxn,j}$ 를 가정''하는 것만으로는 재현되지
않는다 --- 상수 값만으로는 SOC 축 위에서 봉우리$\cdot$골(경계의 발산형 구조)을 만들 자유도가 없고,
부호 교차도 전이 종의 겹침 가중(그 가중 자체가 점유 분포의 산물이다 --- \S\ref{ssec:overlap})을 빌리지
않는 한 매끄러운 블렌드가 아니라 계단으로만 나오기 때문이다. 뒤에서 보듯 전이당 상수 \emph{자체}는 분포
위에 얹으면 유효한 근사로 판정된다(\S\ref{sec:limits}) --- 부족한 것은 상수가 아니라 그 밑의 분포다.
```

근거: eq:weighted(ch2_sec05:74–83)는 **상수** $\Delta S_{\rxn,j}$ 만으로 "계단이 아니라 연속 블렌드"를 이미 만들고(수치 검증: 내부 경계 3곳 연속), §limits keybox 는 "상수 표준값 + 분포로 측정급"이라 판정. 현행 문장의 둘째 논거는 '겹침 가중 없음' 전제를 숨겨 §2.5 그림 fig:blend 캡션("계단(빨간 점선)이 아니다")·§2.6 keybox headline 과 표면 모순을 만든다. 첫 논거(발산형 자유도 없음)는 재계산으로도 참(상수의 가중 평균은 $[\min_j,\max_j]$ 를 못 벗어남 — 발산 불가). 제안은 논거를 참으로 만들면서 서두의 수사 구조(분포 필요성)를 강화한다.

#### §2-M2 = A11-02 — 서두 $\dot Q_\rev$ 식의 $I$ 규약 미명시

현행 축자 (ch2_sec00_intro.tex:24–28):
```latex
이 미시상태 분포의 흩어짐 척도이고, 가역 발열
\[
\dot Q_\rev=-I\,T\,\frac{\partial U_\oc}{\partial T}=-\frac{I\,T}{F}\,\Delta S(x)
\]
은 한 충전상태에서 다른 충전상태로 넘어갈 때 \emph{이 분포를 재배열하면서 주고받는 열}이다.
```

제안 (display 에 규약 괄호 부기):
```latex
이 미시상태 분포의 흩어짐 척도이고, 가역 발열
\[
\dot Q_\rev=-I\,T\,\frac{\partial U_\oc}{\partial T}=-\frac{I\,T}{F}\,\Delta S(x)
\qquad(I>0\ \text{방전 --- 이 라벨의 층위와 부호 유도는 \S\ref{sec:revheat}})
\]
은 한 충전상태에서 다른 충전상태로 넘어갈 때 \emph{이 분포를 재배열하면서 주고받는 열}이다.
```

근거: eq:qrev(ch2_sec07:15–21)와 동일식이나 규약 "($I>0$ 방전)"은 그 절에서야 나오고, :48–53 ★라벨 층위(Bernardi "방전"=흑연 리튬화 vs Part I "방전"=탈리튬화, "본 장에서 부호가 가장 크게 어긋날 수 있는 자리")가 CRITICAL 로 지정된 사안. 부호 있는 식의 첫 노출에 규약 부재는 그 위험을 서두에서 방치하는 것.

#### §2-M3 = A11-07 — eq:muV 무앵커 + $\mu$ 호칭 동요

현행 축자 (ch2_sec01_partition.tex:52–56):
```latex
이제 화학을 넣는다. Li 가 자리에 들어가는 전기화학 반응의 전기화학 퍼텐셜은 셀 전위에 선형으로 묶인다:
\begin{equation}
\mu \;=\; \mu^0 \;-\; s\,F\,(V-U_j),
\label{eq:muV}
\end{equation}
```

제안 (도입문 대체 — 식·라벨 불변):
```latex
이제 화학을 넣는다. Li 가 자리에 들어가는 삽입종의 화학퍼텐셜(중성 삽입 Li 라 전기화학 퍼텐셜과 일치 ---
\S\ref{sec:center} (b))은 셀 전위에 선형으로 묶인다(\S\ref{sec:center} 식~\eqref{eq:eqcond}$\cdot$Part 0
\S\ref{sec:sm-electro} 의 전기화학 결선과 동일한 관계):
\begin{equation}
\mu \;=\; \mu^0 \;-\; s\,F\,(V-U_j),
\label{eq:muV}
\end{equation}
```

근거: (i) 앵커 — 동일 관계가 eq:eqcond(ch1_sec03:33–37)·Part 0 sm-electro(ch1_sec02b:139)에 선행 확립. §2.1 은 sm-site 앵커를 2회 두면서(:40, :42) 중심 관계식인 eq:muV 만 무앵커 — 새로 상정한 식으로 오독될 여지. (ii) 용어 — :52 "전기화학 퍼텐셜" 과 :63 "몰 화학퍼텐셜" 이 같은 $\mu$ 를 가리킴. sec:center (b) 는 $\tilde\mu=\mu+zF\phi$ 를 구분 정의했으므로, 중성 삽입종($z{=}0$)에서 둘이 일치함을 한 번 밝히면 동요가 해소된다.

#### §2-M4 = A11-08 — ★부호 각주의 $\sigma_d$ 작용처 열거 누락

현행 축자 (ch2_sec01_partition.tex:58–61, 각주 전문):
```latex
\footnote{★부호 각주(오독방지). 이 $s{=}+1$ 은 방향 부호
$\sigma_d$(\S\ref{sec:notation} --- 분극$\cdot$분기$\cdot$꼬리 세 작용처 전용, $\pm1$)와는 \emph{별개}다. 평형 관계에는
항상 $s{=}+1$ 이 들어가며, $\sigma_d{=}-1$ 을 이 식에 기계적으로 대입하면 점유와 진행률이 뒤바뀌는
\emph{여집합 오류}가 생긴다(종은 좌우 대칭이라 봉우리 자체는 멀쩡해 보여 오류가 잠복한다).}
```

제안 (각주 대체):
```latex
\footnote{★부호 각주(오독방지). 이 $s{=}+1$ 은 방향 부호 $\sigma_d$(\S\ref{sec:notation} ---
분극$\cdot$분기$\cdot$꼬리 세 작용처와, 충전 진행률을 여집합 좌표로 읽는 평형 종 식~\eqref{eq:xieq} 의
logistic 인자에 쓰는 $\pm1$)와는 \emph{별개}다. 열역학 평형 관계식~\eqref{eq:muV} 에는 항상 $s{=}+1$ 이
들어간다 --- 식~\eqref{eq:xieq} 의 $\sigma_d$ 는 좌표 교환($s\to\sigma_d$ 치환 $=$ 여집합 교환,
\S\ref{sec:dist})이지 이 평형 관계의 부호 변경이 아니며, $\sigma_d{=}-1$ 을 식~\eqref{eq:muV} 에 기계적으로
대입하면 점유와 진행률이 뒤바뀌는 \emph{여집합 오류}가 생긴다(종은 좌우 대칭이라 봉우리 자체는 멀쩡해
보여 오류가 잠복한다).}
```

근거: notation(ch1_sec01:28–31)은 $\sigma_d$ 의 등장처로 평형 진행률 logistic 인자를 **첫째로** 열거하고, eq:xieq(ch1_sec05:279–282)가 그 평형식이다. 현행 "세 작용처 전용" + "평형 관계에는 항상 $s{=}+1$" 은 이 두 원문과 표면 모순 — 각주의 목적(오독 방지)에 정확히 반대로 작동할 수 있는 자리. 여집합 교환 동치(ch1_sec05:276–277)를 인용해 닫으면 경고가 완결된다.

#### §2-M5 = A11-09 — 몰 환산 산문 2벌 → display 1줄

현행 축자 (ch2_sec01_partition.tex:63–76):
```latex
\emph{감소}한다. 식~\eqref{eq:muV} 의 $\mu$ 는 몰 화학퍼텐셜이고 식~\eqref{eq:occ} 의 지수
$\beta(\varepsilon_0-\mu)$ 는 자리당이므로, 후자의 분자$\cdot$분모를 $N_A$ 배 해 몰 척도로 맞춘다: 분자는
$N_A\varepsilon_0-N_A\mu$ 인데 $N_A\varepsilon_0\equiv\mu^0$(자리 에너지의 몰 환산이 기준 화학퍼텐셜과 일치하는
전이 중심 기준)이고 $N_A\mu$ 가 식~\eqref{eq:muV} 의 몰 $\mu$ 이므로 $\mu^0-\mu=sF(V-U_j)$(기준 $\mu^0$ 가
상쇄된다), 분모는 $N_A\kB T=RT$ 다. 따라서 지수가 $\beta(\varepsilon_0-\mu)=sF(V-U_j)/RT=(V-U_j)/w$ 로 닫혀,
평형 점유와 그 여집합(탈리튬화 진행률 $\xi\equiv1-\theta$)은
```
(및 :74–76)
```latex
이고 여기서 $w\equiv RT/F$ 다. 몰 단위 환산은 $R=N_A\kB$, $F=N_Ae$ 로 닫힌다 --- $\beta(\varepsilon_0-\mu)$ 의
분자를 몰 에너지로 쓰면 지수는 $(V-U_j)/(RT/F)=(V-U_j)/w$, 곧 몰 척도에서 $F/RT=1/w$ 이고, 자리당
$\beta=1/\kB T$ 그대로는 $\beta F=N_A/w$ 다.
```

제안 (:63–67 을 display 사슬로 대체, :74–76 을 한 문장으로 압축 — 정보 전량 보존):
```latex
\emph{감소}한다. 식~\eqref{eq:muV} 의 $\mu$ 는 몰 화학퍼텐셜이고 식~\eqref{eq:occ} 의 지수
$\beta(\varepsilon_0-\mu)$ 는 자리당이므로, 분자$\cdot$분모를 $N_A$ 배 해 몰 척도로 맞추면 지수가 한 줄로 닫힌다:
\begin{equation*}
\beta(\varepsilon_0-\mu)\;=\;\frac{N_A\varepsilon_0-N_A\mu}{N_A\kB T}
\;=\;\frac{\mu^0-\mu}{RT}
\;=\;\frac{sF\,(V-U_j)}{RT}
\;=\;\frac{V-U_j}{w},\qquad w\equiv\frac{RT}{F}
\end{equation*}
--- 첫 등식이 $N_A$ 배, 둘째가 $N_A\varepsilon_0\equiv\mu^0$(자리 에너지의 몰 환산을 전이 중심의 기준
화학퍼텐셜과 일치시키는 규약)과 $N_A\kB=R$, 셋째가 식~\eqref{eq:muV}(기준 $\mu^0$ 상쇄)다. 따라서
평형 점유와 그 여집합(탈리튬화 진행률 $\xi\equiv1-\theta$)은
```
그리고 eq:logistic 직후 문장:
```latex
이고 여기서 $w\equiv RT/F$ 다($R=N_A\kB$, $F=N_Ae$ --- 몰 척도에서 $F/RT=1/w$, 자리당 $\beta$ 그대로는
$\beta F=N_A/w$).
```

근거: 같은 환산의 산문 2벌(:63–67 과 :74–76)이 연달아 나와 독자가 두 번 검산하게 됨. display 사슬은 각 등식을 눈으로 대조 가능(재유도 통과: $\beta F=F/\kB T=N_A F/RT=N_A/w$ 포함 — §3-체크 5). 기존 사실 항목($N_A\varepsilon_0\equiv\mu^0$ 규약·$\mu^0$ 상쇄·$R=N_A\kB$·$F=N_Ae$·$F/RT=1/w$·$\beta F=N_A/w$) 전량 보존 — 삭제 없음, 재배치·압축만.

#### §2-M6 = A11-10 — keybox 두-상 지목의 근거 한정 누락

현행 축자 (ch2_sec01_partition.tex:84–86, keybox 내):
```latex
분배함수~\eqref{eq:Z1} 의 $RT/F$, 상호작용이 있으면 $\Omega$ 가 폭을 바꾸되 그 값 역시 평형 등온선이
결정한다 --- \S\ref{ssec:BW}), \emph{두-상 전이}($\Omega_j>2RT$ --- 흑연 staging 의 $2\mathrm L\!\to\!2\cdot
2\!\to\!1$)에는 이 유도가 닿지 않아 폭은 현상학적 자유 피팅 파라미터가 된다.
```

제안 (괄호부 대체):
```latex
분배함수~\eqref{eq:Z1} 의 $RT/F$, 상호작용이 있으면 $\Omega$ 가 폭을 바꾸되 그 값 역시 평형 등온선이
결정한다 --- \S\ref{ssec:BW}), \emph{두-상 전이}($\Omega_j>2RT$; 흑연 staging 에서 실측 plateau$\cdot$상평형
문헌이 두-상으로 지목하는 $2\mathrm L\!\to\!2\cdot2\!\to\!1$ \cite{dahn1991,ohzuku1993} --- 문턱 부등식
자체는 전이 실명을 가르지 않는다, \S\ref{ssec:weff} 각주)에는 이 유도가 닿지 않아 폭은 현상학적 자유 피팅
파라미터가 된다.
```

근거: §2-M6 총괄표 행 참조. `dahn1991`·`ohzuku1993` 은 ch1v22_bib.tex:6–7 기등재 키(신규 문헌 아님 — V1 원장 승계분). 이 한정은 ssec:weff 각주(ch2_sec05:169–173)의 문장을 압축 인용한 것.

#### §2-M7 = A11-11 — "이 장의 첫 매듭" → "본 파트의 첫 매듭"

현행 축자 (ch2_sec01_partition.tex:99–101):
```latex
이 되는데, 이 \emph{Nernst 형 로그항}이 뒤에서 configurational 엔트로피의 부분몰 형태로 다시 나타난다
(\S\ref{sec:config}). 식~\eqref{eq:Vxi} 의 $\ln[\xi/(1-\xi)]$ 가 단순한 곡선맞춤이 아니라 점유 분포의
엔트로피에서 온다는 것이 이 장의 첫 매듭이며, 그 매듭을 다음 절이 명시적으로 푼다.
```

제안 (:101 만):
```latex
엔트로피에서 온다는 것이 본 파트의 첫 매듭이며, 그 매듭을 다음 절이 명시적으로 푼다.
```

근거: v1.0.22 병합 빌드에서 "이 장"=Chapter 1 로 읽히면 "첫 매듭" 은 거짓(Part I 선행). 주장의 범위가 Part T 이므로 "본 파트"가 정확. 단 :57–58 "본 장의 유도 전용 고정 부호" 는 장 전역 규약($s$ — sec:center·sec:hys·sec:width 공용)이라 그대로 두는 것이 맞음 — 기계적 일괄 치환 금지. (참고 — 범위 밖 잔여: 같은 "본 장" 계열 표현이 Part T 타 절(예: ch2_sec07:22·57)에도 남아 있음. 본 창 대상 밖이라 제안 없이 관찰만 기록.)

#### §2-M8 = A11-13 — eq:BW → eq:Veq_BW 유도의 $U_j$ 다리 부재

현행 축자 (ch2_sec01_partition.tex:113–120):
```latex
이고, 우변 둘째 항이 \emph{혼합(섞임) 엔트로피}(곧 \S\ref{sec:config}; Part 0 의 섞임 엔트로피(\S\ref{sec:sm-lattice} 식~\eqref{eq:sm-Smix})와
같은 양), 셋째 항이 regular-solution 형 \emph{혼합 엔탈피}다 --- 상호작용 모수 $\Omega>0$ 은
같은 종끼리 뭉치려는 인력(상분리 경향), $\Omega<0$ 은 교대 정렬(규칙화) 경향을 뜻한다. 평형 전위는 $\theta$
1몰 삽입당 자유에너지 변화 $\partial g/\partial\theta$ 를 전위로 환산한 것이므로, 식~\eqref{eq:BW} 를 미분하면
```

제안 (:115–116 의 마지막 문장 대체 — eq:BW·eq:Veq_BW 불변):
```latex
같은 종끼리 뭉치려는 인력(상분리 경향), $\Omega<0$ 은 교대 정렬(규칙화) 경향을 뜻한다. 식~\eqref{eq:BW}
의 $g$ 는 섞임$\cdot$상호작용 몫만 적은 것이고 자리 에너지의 $\theta$-선형 몫 $\mu^0\theta$ 는 전이 중심
$U_j$ 로 이미 흡수돼 있으므로($N_A\varepsilon_0\equiv\mu^0$ --- \S\ref{ssec:logistic}), 삽입 1몰당
화학퍼텐셜은 $\mu(\theta)=\mu^0+\partial g/\partial\theta$ 다. 이를 평형 조건~\eqref{eq:muV} 의
$\mu=\mu^0-sF(V-U_j)$ 와 등치해 $V$ 로 풀면
```

근거(재유도): 문면의 eq:BW 만으로는 $\partial g/\partial\theta=RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)$ 이고 "전위로 환산"의 규칙이 정의돼 있지 않아 eq:Veq_BW 의 $U_j$ 항이 유도 불가(비약). 제안의 다리로는 $\mu^0+RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)=\mu^0-sF(V-U_j)$ → $V_\eq=U_j-\frac{RT}{F}\ln\frac{\theta}{1-\theta}-\frac{\Omega}{F}(1-2\theta)$ — eq:Veq_BW 와 정확히 일치(§3-체크 8). Part 0 의 $\mu(\theta)$ 경로(eq:sm-mucount·eq:sm-muideal)와도 정합.

### L (7건)

#### §2-L1 = A11-03 — "logistic 평형 점유" → "logistic 평형 종(진행률)"

현행 축자 (ch2_sec00_intro.tex:31–33):
```latex
이 때문에 본 파트는 분포를 결론으로 인용하는 대신 \emph{본체}로 전개한다. 출발점은 단일 격자 자리의
분배함수 $Z$ 이고(\S\ref{sec:partition}), 거기서 점유 분포 $\avg{n}$ 을 얻는데 이것이 바로 Part I
\S\ref{sec:width} 의 logistic 평형 점유의 통계역학적 기원임을 보인다.
```

제안 (:32–33):
```latex
분배함수 $Z$ 이고(\S\ref{sec:partition}), 거기서 점유 분포 $\avg{n}$ 을 얻는데 이것이 바로 Part I
\S\ref{sec:width} 의 logistic 평형 종(평형 진행률 $\xi_\eq$ --- 점유 분포의 여집합)의 통계역학적 기원임을 보인다.
```

근거: Part I §width 의 확립 대상은 진행률 $\xi_\eq$(ch1_sec05:375 "$\xi_\eq$ 는 평형 점유 분포의 여집합"). §config :66–68 이 $\theta$/$\xi$ 혼용을 명시 금지하는 문서에서, 서두의 "평형 점유" 호칭은 첫 단추의 혼용.

#### §2-L2 = A11-04 — "이후 모든 절" 양화 완화

현행 축자 (ch2_sec00_intro.tex:53–54):
```latex
이고, 각 화살표는 점프 없이 분포에서 유도된다. 이 사슬이 본 파트 전체의 목차 설계 앵커다 --- 이후 모든 절은
이 다섯 마디 중 하나를 여는 일이며, 봉우리 중심에서 발열까지 가는 부호는 한 자리도 라벨이 아니라 식이 정한다.
```

제안:
```latex
이고, 각 화살표는 점프 없이 분포에서 유도된다. 이 사슬이 본 파트 전체의 목차 설계 앵커다 --- 이후 본론 절들은
이 다섯 마디 중 하나를 여는 일이고(방법론 출구 \S\ref{sec:method} 는 그 입력을 조달한다), 봉우리 중심에서
발열까지 가는 부호는 한 자리도 라벨이 아니라 식이 정한다.
```

#### §2-L3 = A11-06 — "로그 미분" 변수 명시

현행 축자 (ch2_sec01_partition.tex:25–26):
```latex
자리의 평균 점유는 정의상 두 상태의 확률 가중 평균, 곧 분배함수에 대한 로그 미분이다. 분자에 점유 상태의
Gibbs 인자를, 분모에 $\Xi_1$ 을 놓아 정리하면
```

제안:
```latex
자리의 평균 점유는 정의상 두 상태의 확률 가중 평균, 곧 분배함수의 로그 미분
$\avg{n}=\kB T\,\partial\ln\Xi_1/\partial\mu$ 이다(Part 0 식~\eqref{eq:sm-gc} 셋째 식의 교차검증 경로).
분자에 점유 상태의 Gibbs 인자를, 분모에 $\Xi_1$ 을 놓아 정리하면
```

근거: 재유도 — $\partial\ln\Xi_1/\partial\mu=\beta e^{-\beta(\varepsilon_0-\mu)}/(1+e^{-\beta(\varepsilon_0-\mu)})=\beta\avg{n}$ ✓. Part 0(ch1_sec02a:146–147)이 같은 경로를 교차검증으로 전시 — 여기만 변수 무명시.

#### §2-L4 = A11-12 — ssec:BW 에 Part 0 sm-mf 앵커 추가

현행 축자 (ch2_sec01_partition.tex:104–106):
```latex
실제 격자에서는 자리들이 독립이 아니다. 점유된 이웃 자리는 다음 Li 의 삽입 에너지를 바꾼다(정전 반발,
탄성 변형, 전자 구조 변화). 이 상호작용을 평균장으로 다루는 것이 Bragg--Williams 근사다 \cite{huggins2009,
bazant2013}.
```

제안:
```latex
실제 격자에서는 자리들이 독립이 아니다. 점유된 이웃 자리는 다음 Li 의 삽입 에너지를 바꾼다(정전 반발,
탄성 변형, 전자 구조 변화). 이 상호작용을 평균장으로 다루는 것이 Bragg--Williams 근사다 \cite{huggins2009,
bazant2013}(Part 0 \S\ref{sec:sm-mf} 의 정규용액 평균장과 같은 모형 --- 여기서는 $\theta$ 좌표로 다시 적는다).
```

#### §2-L5 = A11-14 — 임계 조건 논거 반 문장 + $T_c$ 독법

현행 축자 (ch2_sec01_partition.tex:131–133):
```latex
이 중앙 $\theta=\tfrac12$ 에서 $0$ 이 되는 $\Omega=2RT$ 다. $\Omega\le2RT$ 면 등온선이 단조(균질 고용체 ---
등호에선 중심 기울기 $0$), $\Omega>2RT$ 면 중앙에서 기울기가 양으로 뒤집혀(불안정) 상분리한다. 이 임계
$\Omega=2RT$ 는 \S\ref{sec:hys}(히스테리시스)의 spinodal 조건과 같은 열역학이며,
```

제안 (첫 문장 뒤 보강):
```latex
이 중앙 $\theta=\tfrac12$ 에서 $0$ 이 되는 $\Omega=2RT$ 다($1/[\theta(1-\theta)]$ 의 최소가
$\theta=\tfrac12$ 의 $4$ 라 기울기가 가장 덜 음인 곳이 중앙이고, 온도로 읽으면 임계온도 $T_c=\Omega/2R$ 다).
$\Omega\le2RT$ 면 등온선이 단조(균질 고용체 ---
등호에선 중심 기울기 $0$), $\Omega>2RT$ 면 중앙에서 기울기가 양으로 뒤집혀(불안정) 상분리한다. 이 임계
$\Omega=2RT$ 는 \S\ref{sec:hys}(히스테리시스)의 spinodal 조건과 같은 열역학이며,
```

#### §2-L6 = A11-15 — 격자기체 서지에 원전 병기

현행 축자 (ch2_sec01_partition.tex:6–7):
```latex
통계역학에서 한 계의 모든 평형 열역학량은 분배함수에서 나온다. 흑연 격자에 Li 이온이 삽입되는 문제는
\emph{격자기체}(lattice gas)로 모형화된다 \cite{newman,huggins2009}: 결정 안에 동등한 삽입 자리들이 있고,
```

제안:
```latex
통계역학에서 한 계의 모든 평형 열역학량은 분배함수에서 나온다. 흑연 격자에 Li 이온이 삽입되는 문제는
\emph{격자기체}(lattice gas)로 모형화된다 \cite{newman,huggins2009,mckinnon1983}: 결정 안에 동등한 삽입 자리들이 있고,
```

근거: mckinnon1983 은 ch1v22_bib.tex:16 기등재("격자기체 삽입 등온선의 원전") — Part 0 이 원전으로 못박은 키의 병기일 뿐, 신규 문헌 아님.

#### §2-L7 = A11-16 — "왜 $\mu$-고정 대정준인가" 선제 포인터

현행 축자 (ch2_sec01_partition.tex:8–10):
```latex
각 자리는 비어 있거나(에너지 $0$) Li 하나가 점유한다(에너지 $\varepsilon_0$). 자리들은 전해질을 통해 Li
저장조(상대극 Li 금속)와 평형을 이루므로, 전기화학 퍼텐셜 $\mu$ 가 고정된 \emph{대정준}(grand-canonical)
문제다.
```

제안:
```latex
각 자리는 비어 있거나(에너지 $0$) Li 하나가 점유한다(에너지 $\varepsilon_0$). 자리들은 전해질을 통해 Li
저장조(상대극 Li 금속)와 평형을 이루므로, 전기화학 퍼텐셜 $\mu$ 가 고정된 \emph{대정준}(grand-canonical)
문제다(정전류 운용처럼 전하가 고정될 때는 전하 보존식을 $\mu$ 에 대해 반전한다 --- Part 0
\S\ref{sec:sm-mc}$\cdot$본 파트 \S\ref{ssec:overlap} 식~\eqref{eq:implicit}).
```

근거: 독자 표준 질문("전지는 전하 제어인데 왜 $\mu$-고정인가")의 답이 같은 빌드(eq:sm-mc-balance 유일근·eq:implicit)에 이미 있음 — 반 문장 포인터로 선제. P3-2(전하 보존식이 내부 전위 결정 중심식)와의 정합 표시를 §2.1 진입점에서 상기하는 효과.

---

## 3. 재계산·재유도 검증 기록 (논리 축 — 통과 항목 포함 전량)

| # | 대상 | 방법 | 결과 |
|---|---|---|---|
| 1 | eq:Z1 $\Xi_1=1+e^{-\beta(\varepsilon_0-\mu)}$ | 2-상태 Gibbs 합 직접 전개 | 통과 |
| 2 | eq:occ 3형 등식 + "마지막 등식은 분자·분모 나눔" | 직접 나눗셈·로그미분($\kB T\,\partial\ln\Xi_1/\partial\mu=\avg{n}$) 재유도 | 통과 |
| 3 | FD 동형 대응 | $f(E)$ 와 항별 대조 | **산문 오서술 발견 (A11-05)** — 수식은 무결 |
| 4 | eq:muV 부호 방향($V\uparrow\Rightarrow\mu\downarrow\Rightarrow\theta\downarrow$) | 부호 추적 | 통과 (eq:eqcond·sm-electro 와 동형 확인) |
| 5 | 몰 환산 사슬 $\beta(\varepsilon_0-\mu)=(V-U_j)/w$·$F/RT=1/w$·$\beta F=N_A/w$ | $N_A$ 배·$R=N_A\kB$·$F=N_Ae$ 대입 재계산 | 통과 |
| 6 | eq:logistic 쌍($\theta_\eq$ 감소·$\xi_\eq$ 증가) + 극한($V\gg U_j\Rightarrow\xi\to1$) | 직접 평가 | 통과 — eq:logisticsolve($s{=}+1$)·eq:xieq($\sigma_d{=}+1$)와 일치 |
| 7 | eq:Vxi 반전 및 $\theta=1-\xi$ 대입 | 역함수 재유도 | 통과 — eq:Veq_BW 의 $\Omega=0$ 극한·keybox 서술과 정합 |
| 8 | eq:BW → eq:Veq_BW | $\partial g/\partial\theta$ 직접 미분 후 eq:muV 등치 | **다리 부재 발견 (A11-13)** — 다리 보충 시 정확히 재현 |
| 9 | eq:slope_BW 미분·$\theta{=}\tfrac12$ 값 $(2\Omega-4RT)/F$·임계 $\Omega=2RT$·안정성 부호 | 직접 미분·평가 | 통과 — sec:hys eq:spinodal($u_j$ 실수 조건 $\Omega_j>2RT$)·sec:limits 코너와 동일 열역학 확인 |
| 10 | 서두 $U_j(T)$ 식 | eq:Uj(ch1_sec03:52–55)와 축자 대조·$\partial U_j/\partial T=\Delta S/F$ 재미분 | 통과 |
| 11 | $\dot Q_\rev$ 두 형태 등가·차원 | $\Delta S=+F\,\partial U_\oc/\partial T$(ch2_sec07 srcbox) 대입·W 차원 검산 | 통과 (단 $I$ 규약 미명시 — A11-02) |
| 12 | $\Omega\gtrless0$ 물리 해석(뭉침/규칙화) | $\Omega\theta(1-\theta)$ 부호 논증 | 통과 |
| 13 | $s_\mathrm{int}$ 선도항 $+\kB\ln q$·고온 증가·$S_\vib\to R[1+\ln(T/\theta_{E,j})]$ 합치 | $\kB\partial(T\ln q)/\partial T$ 전개·1D 고전 $q=\kB T/\hbar\omega$ 대입 | 통과 — eq:sm-sint(ch1_sec02a:321–325)·ch2_sec04:41 과 일치 |
| 14 | 전셀 차감식 $\partial U_\cell/\partial T=\partial U_\mathrm{cat}/\partial T-\partial U_\mathrm{an}/\partial T$ | $U_\cell=U_\mathrm{cat}-U_\mathrm{an}$ 미분 | 통과 — ch2_sec07 srcbox(음극 몫 부호 반전)와 정합 |
| 15 | 서두 부호 프로파일(저-$x$ 양·고-$x$ 음) | §config 문헌검증 절(reynier2003·allart2018 서술)과 대조 | 통과(내부 정합 — 외부 재검증은 §config 소관) |
| 16 | 라벨·참조 해소(두 파일의 전체 \S\ref·\eqref·\cite) | grep 정의처 대조 + 빌드 log | 통과 — 전건 해소(sec:lco-electronic 은 xr 로 ch2_lco 빌드에서 해소, input 확인) |

## 4. 서치 절 (문헌 위임 판단)

하이쿠 서브에이전트 위임 **불실행** — 판단 근거: 본 창의 전 제안이 인용하는 키(`dahn1991`·`ohzuku1993`·`mckinnon1983`)는 ch1v22_bib.tex:6·7·16 기등재 + V1022_REFERENCE_LEDGER 의 v1.0.21 원장 전건 승계 범위이며, 두 대상 파일의 어느 주장도 **신규 외부 문헌** 없이는 판정 불가한 것이 없었다(서두의 실측 프로파일 주장은 §config 의 기존 검증 절이 담당 — 그 절 자체는 본 창 범위 밖). 기억 서지 신규 투입 0건.

## 5. 무발견 축 (검토했으나 문제 없음)

- **수식 대수 오류**: 0건 — §3 의 16개 재계산 전 항목에서 두 파일의 display 수식 자체는 전부 무결(발견 H/M 은 산문·전제·앵커 층위).
- **부호 오류**: 0건 — eq:muV·eq:logistic·eq:Vxi·eq:Veq_BW·eq:slope_BW·$\dot Q_\rev$ 의 부호 방향 전부 상류(eq:eqcond·eq:logisticsolve·eq:xieq·eq:qrev)와 정합.
- **라벨·참조 깨짐**: 0건 — 두 파일이 쓰는 \S\ref·\eqref 23종 전부 정의처 확인, 빌드 log 의 undefined 는 폰트 경고 3건뿐.
- **서지 오귀속(두 파일 내 \cite)**: 0건 — newman·huggins2009·bazant2013 사용처 적절(전부 V1 원장 승계 키).
- **P3 항목**: 두 파일 범위에서 $V_n$ 위계 위반·전하 보존 중심식 회귀(OCV 읽기 회귀)·ver.N/Chapter 혼동 없음(§2.1 은 단일 전이 분포 층위이고 전하 보존 반전은 §2.5·Part 0 에 유지 — divider 가 명시 인계).
- **제거 용이 블록(bgbox 증축분) 독립성**: 해당 없음 — 두 파일에 bgbox 없음(warnbox·keybox 는 원 자산).
- **GS-1/GS-2 공백**: 두 파일과 무관(Ch3 Si 소관) — 메우는 제안 없음.

## 6. 말미 4-tier

- **확정** (재계산·문면 대조로 검증 완료): A11-05(FD 산문 오서술 — 재유도), A11-13(eq:BW 문면에 $U_j$ 원천 부재 — 재유도), A11-08("세 작용처 전용" ↔ notation:29·eq:xieq 문면 충돌), A11-10(네 전이 초기값 모두 $\Omega>2RT$ — ch1_sec05:307–308 문면), A11-01(상수+가중=연속 블렌드 — eq:weighted·fig:blend·§limits keybox 문면), A11-02($I$ 규약이 §2.7 에서야 등장 — 문면), §3 의 통과 16항.
- **추정** (합리적이나 저자 의도 확인 필요): A11-11("이 장"이 구 Ch2 잔재라는 해석 — 의도적 장 지칭일 가능성 낮음), A11-07/L4/L6/L7 의 앵커·서지 병기가 재놓기(자기완결) 설계 의도와 충돌하지 않는다는 판단, 각 제안 문구의 표현 선택.
- **미검증**: 제안 LaTeX 의 실제 빌드 렌더(보고 전용 규율상 컴파일 미실행 — 전 제안은 기존 매크로 \rxn·\oc·\rev·\eq·\avg·\kB 범위 내 표준 구문), Part I tab:staging 의 $\Omega_j$ 초기 수치 원표 재대조(본 창은 ch1_sec05 본문 서술을 전거로 사용), Part T 타 절의 "본 장" 잔여 표현 전수(범위 밖 — §2-M7 말미에 관찰만 기록).

— 이상. 발견 총 16건: **H 1 · M 8 · L 7**. 소스 파일·git·`Codex/` 무접촉.
