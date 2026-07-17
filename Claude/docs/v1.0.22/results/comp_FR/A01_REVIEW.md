# A01_REVIEW — FR-A01 심층 검토 (ch1_sec00_intro.tex · ch1_sec01_n0n1.tex)

- 검토 창: FR-A01 (v1.0.22 대공사, BRIEF_FR_A.md 준수 — **보고 전용**, 소스 무수정·git 무조작·`Codex/` 무접근)
- 대상(전문 정독): `Claude/docs/v1.0.22/_sections/ch1_sec00_intro.tex`(93행 전문) · `ch1_sec01_n0n1.tex`(253행 전문)
- 참조 원문 확인(read-only): ch1 마스터·common_preamble·sec02a/b(Part 0)·sec03(N2)·sec04(N3)·sec05(N4/N5)·sec06(N6)·sec07(broadening)·sec08(N7)·sec09(N8)·sec10(N9·tab:staging)·sec18(nodemap)·appA(signcheck)·appB(codemap)·ch1v22_bib·sec11(lco-intro)·ch2_sec07(revheat)·`Anode_Fit_v1.0.22.py`(dqdv/curve 경로)·`results/V1022_REFERENCE_LEDGER.md`·`v1.0.21/results/V1021_REFERENCE_LEDGER.md`(승계 키)
- 4관점 전부 적용: ①내용 보완(빡세게) ②논리 오류(재계산·재유도) ③더 쉬운 설명 ④산문→수식 간결화
- 상태: **완료** (2026-07-17)

## 양식 주기 (축자성 보존)

BRIEF 의 7열 표 규격(`| ID | 파일:행 | 유형 | 등급 | 현행 | 제안 | 근거 |`)을 따르되, **현행(축자)·제안(완성 LaTeX) 열은 md 표 셀에서 축자 보존이 불가능**하다(원문에 `$|I|$` 등 파이프·개행 다수 → 표 파손 또는 이스케이프로 축자성 훼손). 따라서 **색인 표(7열 중 현행·제안은 요지로 축약) + 발견별 상세 블록(현행 축자 = fenced block 정본, 개행 포함 그대로)** 의 2단 구성으로 준수한다. 기계 매칭은 상세 블록의 fenced `현행` 을 정본으로 쓸 것.

## 색인 표

| ID | 파일:행 | 유형 | 등급 | 현행(요지 — 축자는 상세 블록) | 제안(요지 — 완성 LaTeX 는 상세 블록) | 근거(요지) |
|----|---------|------|------|------|------|------|
| A01-H1 | ch1_sec01_n0n1.tex:92-94, 145-146, 149-150 | 논리(그림↔타 절 사실 불일치·오귀속) | H | fig:staging 아래축 = "초기값 수치 평가"·"네 초기값 전이의 실제 peak"·"표 tab:staging 의 U_j,Q_j,w_j" | 폭 = §sum "폭 폴백" 값임을 명시 + 실제 초기 상태(n=1 우선, 균일 w=RT/F)와의 구분 각주 | tab:staging 에 w_j 열 없음; sec10:44-46 "n 이 우선 … 실제 초기 폭은 네 전이 균일 25.7 mV"; fig:sumcurve(2→1 peak 4.865)와 fig:staging(10.4) 상충 — 수치 전수 재계산으로 확인 |
| A01-H2 | ch1_sec01_n0n1.tex:52 | 논리(오귀속) | H | tab:notation T_rep 행 "N1·N3·N7 대표조건 평가" | "N3·N7 대표조건 평가"로 정정(+대상 명시) | N1(eq:vn)은 T 무관(본문·코드 전수 추적: T_rep 실사용 = N3 분기 gap·N7 지연 길이뿐 — 코드 527/556/566행) |
| A01-M1 | ch1_sec00_intro.tex:16 | 논리(산문↔그림 불일치) | M | "전이 j 마다 반복하는 전이 루프 N2--N9 로 진행한다" | 루프 = N2–N8, 합산 N9 는 루프 뒤 1회로 정정 | fig:spine 파선 상자 fit=(n2)…(n78), N9 는 "post-loop: sum … once"·캡션 "모든 전이가 이 loop 를 마치면 N9 가 … 합산한다" |
| A01-M2 | ch1_sec00_intro.tex:21-23 | 논리+보완 | M | "본론 N1--N9 가 결과로만 받아 쓰는 평형식들(점유 통계·logistic·평균장 상호작용·Nernst 식)을, 본론에 앞선 Part 0 …" | "본론의 전이 사슬 N2–N9"+"그 사슬에 앞선"으로 정정, 목록에 "다클래스 전하 보존식" 추가, N0·N1 의 위치 주기 | 지면 순서 = §1.1(N0·N1)→§1.2(Part 0)→§1.3(N2) (toc 확인); N1 은 평형식 미사용; 전하 보존식(1.2.6)은 N6·N9 출발식(P3-2 중심식) |
| A01-M3 | ch1_sec00_intro.tex:80-81 | 논리(캡션 입출력 도치) | M | "외부 실험조건 $(\sigma_d,\|I\|,T,Q_\cell)$ 이 N0 에서 모델 입력으로 환산되고" | 외부조건 (V_app, direction, c_rate, Q_cell, T) → 모델 입력 (σ_d, \|I\|) 로 재서술 | σ_d·\|I\| 는 eq:n0map 환산의 **출력**(sec01:10-18); 그림 io 노드 자체와도 불일치 |
| A01-M4 | ch1_sec01_n0n1.tex:31-32 | 논리(과대 주장) | M | "이 규약은 §…--§… 과 Chapter 2(LCO) 전건에서 유지되며" | Ch2 는 전극-중립형(탈리튬화=+1, 셀 라벨 환산 eq:lco-sigmaslot)으로 잇는다는 한정 추가 | Ch2 규약: "LCO 충전 ↦ σ_d=+1"(sec11:35, eq:lco-sigmaslot; 코드 `_delith_is_discharge` 부호 반전) — '방전 +1' 라벨 규약·흑연 반쪽전지 전위는 Ch2 전건 유지가 아님 |
| A01-M5 | ch1_sec01_n0n1.tex:33-34, 48 | 논리(계보 서술 부정확) | M | "s 는 … 본론의 결과-사슬 boxed 식에서 s{=}1 로 대입돼 소멸한다"(본문+표 s 행) | "중심식은 s=1 대입, 진행률식 방향 자리는 s→σ_d 일반화(여집합 교환 동치)로 소멸" 2경로 명시 | sec02b:200 "고정 부호 s 자리에 방향 부호 σ_d"; sec05:276-277 "s→σ_d 치환은 여집합 교환과 동치" — eq:xieq 에서 s 는 1 이 아니라 σ_d 로 감 |
| A01-M6 | ch1_sec01_n0n1.tex:193-194 | 설명+수식화 | M | "온도가 배열 T(V) 이면 각 V_n 점의 값을 그대로 취해 전이당 상수 평가용 대표 온도 T_rep=T̄ 를 얻고" | 점별 양(각 점 T(V_n))과 전이당 상수(전 구간 평균 T_rep) 2규칙 분리 재서술(+선택: eq:trep 수식화) | 현행 구문은 "각 점 값을 취해 T_rep 를 얻는다"로 오독됨 — 표(52행) "전 구간 평균"·코드 `T_rep=mean(T_prog)` 와 정합하게 분리 필요 |
| A01-M7 | ch1_sec01_n0n1.tex:183-184 뒤 | 보완(빠진 논증) | M | (부재 — R_n·꼬리·η 산포의 분담 경계 서술 없음) | §pol 말미에 R_n(평행이동)/L_V(비대칭 꼬리)/③ η 산포(대칭 퍼짐) 3분담·무이중계산 1문장 추가 | 전문 독자 1순위 질문(분극 저항과 동역학 지연의 이중계산 여부)에 본 장 어디에도 답 없음(R_n 전수 grep — sec07 ③ 는 η 산포만, R_n 무언급) |
| A01-M8 | ch1_sec01_n0n1.tex:24 | 보완 | M | "진행률 ξ_j(방전 시 0→1 로 증가, 곧 탈리튬화 진행)" — 충전 시 의미 미정의 | "충전의 진행률은 같은 분포의 여집합 좌표 θ=1−ξ"(sec05 표현) 선행 고지 추가 | ξ 의 방향 의존 의미는 sec05:276-277 에서야 나옴 — 독자가 §1~§4 동안 충전 ξ 를 오독할 여지 |
| A01-M9 | ch1_sec01_n0n1.tex:61 근방 | 보완(마스터표 누락 행) | M | tab:notation 에 ξ_j(실제 진행률)·θ_j·r_j·N_p·q 행 부재 | 5개 행 추가(제안 LaTeX) | ξ_j 는 보존식·eq:sum 의 중심 변수(sec06:7, sec09:96 "ξ_j=ξ_eq,j−r_j"), q 는 인과 순서 기준축(sec09) — 마스터 조회표 취지상 필수 |
| A01-L1 | ch1_sec00_intro.tex:31-32 | 설명 | L | 관측 (b) "극판 전위" — (a)(c)는 실험 손잡이, (b)만 곡선 좌표 | "(b) 그 전이가 앉은 극판 전위(곧 국소 구동력)" 재서술 | 독자 걸림 — 뒤 문장("전위는 장벽 ΔG_a 자체")과의 연결 조기화 |
| A01-L2 | ch1_sec01_n0n1.tex:215-216 | 보완(기호 미정의) | L | bgbox (iii) "$-IT\,\partial U_\mathrm{oc}/\partial T$" — 부호 있는 I 는 본 장 표기(\|I\|·σ_d)에 없음 | "(부호 있는 I 의 층위·규약은 Part T §revheat 소관)" 괄호 추가 | Part T ch2_sec07 이 부호·라벨 층위 전담(ssec:signlabel) — 곡선부 첫 등장에서 전방 지시 필요 |
| A01-L3 | ch1_sec01_n0n1.tex:199 | 설명 | L | keybox "다음 절부터 전이 루프의 모든 물리량 …" — 다음 절은 Part 0(루프 아님) | "전이 루프(§sec:center 이후)의 모든 물리량" 으로 정정 | 지면 순서상 다음 절 = §1.2 Part 0 (toc 확인) |
| A01-L4 | ch1_sec01_n0n1.tex:16 | 보완 | L | "(또는 I_abs 직접 지정)" — 둘 다 줄 때 우선순위 미기재 | "(직접 지정 시 c_rate 무시 — I_abs 우선)" 보강 | 코드 curve(): "주면 c_rate 무시(우선)" — 문서만으로 재현 시 모호 |
| A01-L5 | ch1_sec00_intro.tex:7-8 | 보완 | L | ICA 정의 문장 \cite{bloom2005,dubarry2012} — bloom2005 는 DVA 원전, DVA 무언급 | DVA=같은 곡선의 역수 시선 1구 추가(본 장은 dQ/dV 통일) | P1 프로젝트 목표는 ICA·DVA 병기 — 본 장 전체에 dV/dQ 언급 0(전수 grep) |
| A01-L6 | ch1_sec01_n0n1.tex:90-92 | 설명 | L | "각 stage 전이가 한 peak 를 남기고, … 초기값 … 이 이 네 전이에 대응한다" — 술어 중복·어색 | 재서술안 제시 | 문장 성분 정리(내용 불변) |
| A01-L7 | ch1_sec00_intro.tex:33 | 보완 | L | 관측 인용구 "전류를 0 으로 줄여도 사라지지 않는 성분" — 무인용 | \cite{dreyer2010} 조기 병기(선택) | 해당 실측 주장 첫 인용이 §1.4 — 원장 V1 키 기존 사용분이라 안전 |
| A01-L8 | ch1_sec01_n0n1.tex:78 | 보완 | L | ΔH_a^eff 행 "유효 장벽 $=\Delta H_a-\chi_d\Omega$" — 무조건부 | "(보강 적용 시; 미적용이면 ΔH_a)" 조건 병기 | sec08:106-107·eq:Lqfull 암묵 전제 명시와 정합 |
| A01-L9 | ch1_sec01_n0n1.tex:20-22 | 수식화 | L | σ_d 작용처 셋 서술(산문) | 3행 미니표 대체안(조회 편의) | 산문→표 간결화 후보(내용 동일) |
| A01-L10 | ch1_sec01_n0n1.tex:187-188 | 설명 | L | "그 점 하나만으로 완결되는 값이고" — 직후 기억 적분(과거 필요)과 표면 긴장 | "그 점 자신의 과거에 대한 적분 하나로 점별 완결" 재서술 | eq:lag 는 과거 적분 — '점 하나' 표현이 순간적 자기모순으로 읽힘(뒤 문장이 해소하나 첫 문장에서 선제 해소 가능) |

---

## 발견 상세 (현행 = 축자 정본)

### A01-H1 — fig:staging 폭 귀속: "초기값·실제 peak" 이 §10 의 실제 초기 상태와 상충 [논리 H]

**현행 ①** (`ch1_sec01_n0n1.tex:92-94`):
```latex
\S\ref{sec:sum} 표~\ref{tab:staging} 소관)이 이 네 전이에 대응한다. 이 그림이 서론에서
말한 ``상전이 하나 $=$ peak 하나''의 실제 모양이며, 아래 $\dd Q/\dd V$ 축은 평형 종 식~\eqref{eq:eqpeak}(\S\ref{sec:eqpeak})의
초기값 수치 평가다.
```
**현행 ②** (`ch1_sec01_n0n1.tex:145-146`, 캡션 서두):
```latex
\caption{흑연 staging 의 갤러리 채움 도식(위)과 대응 $\dd Q/\dd V$ peak(아래, 식~\eqref{eq:eqpeak} 의
초기값 수치 평가 --- $\dd Q/\dd V=Q_j\xi_\eq(1-\xi_\eq)/w_j$, 표~\ref{tab:staging} 의 $U_j,Q_j,w_j$).
```
**현행 ③** (`ch1_sec01_n0n1.tex:149-150`, 캡션 중):
```latex
아래: 네 초기값 전이의 실제 peak --- 높이 $Q_j/(4w_j)$ 는 전이마다 크게 다르다
($2\to1$ 이 가장 큼, $10.4\,Q_\cell/$V).
```

**문제(재계산으로 확정)**:
1. 캡션이 인용하는 "표~\ref{tab:staging} 의 $U_j,Q_j,w_j$" 중 **$w_j$ 는 tab:staging 에 열이 없다**(sec10 표 열 = stage/U/ΔH_rxn/ΔS_rxn/Q/Ω/ΔH_a/|dV/dq| — w 열 부재). 그림이 실제로 쓴 폭 0.020/0.016/0.014/0.012 V 는 표 아래 산문의 "**폭 w 폴백**" 값이다.
2. sec10(`ch1_sec10_sum.tex:44-46`)은 "폭 서식은 $n$ 이 \emph{우선} 적용되어 **실제 초기 폭은 네 전이 균일하게 $w=RT/F\approx25.7$ mV** 이며, $w$ 폴백 열의 좁은 값은 전이 dict 에서 $n$ 입력을 제거할 때 활성화되는 대안 폭"이라고 규정한다. 따라서 "**초기값 수치 평가**"·"네 초기값 전이의 **실제 peak**"라는 서술은 §10 의 초기 상태 정의와 상충한다.
3. 수치 전수 재계산: fig:staging 좌표는 폴백 폭 기준 eq:eqpeak 의 정확한 평가다(4곡선 × 4–6점 표본 검산 — 예: 2→1 최고점 (5.289, 10.399) = V 0.086, z=0.0833, ξ(1−ξ)=0.24957, ×Q/w=41.667 ✓; 진최고 Q/(4w)=10.417→캡션 "10.4" ✓). 반면 **실제 초기 상태**(n=1 우선)의 최고 높이는 Q_j/(4·RT/F) = 0.973/1.167/2.432/**4.865** 로, sec10 그림 fig:sumcurve 의 좌표열 (0.085, 4.865)와 일치한다. 같은 "초기값" 명칭 아래 두 그림의 2→1 높이가 10.4 vs 4.87 로 갈린다 — 독자·피팅 사용자 오도.

**제안** (① 대체):
```latex
\S\ref{sec:sum} 표~\ref{tab:staging} 소관)이 이 네 전이에 대응한다. 이 그림이 서론에서
말한 ``상전이 하나 $=$ peak 하나''의 실제 모양이며, 아래 $\dd Q/\dd V$ 축은 평형 종 식~\eqref{eq:eqpeak}(\S\ref{sec:eqpeak})을
표~\ref{tab:staging} 의 $U_j,Q_j$ 와 \S\ref{sec:sum} 의 \emph{폭 폴백 값} $w_j$(0.020/0.016/0.014/0.012 V --- $n$ 입력 제거 시 활성화되는 전이별 대안 폭)로
평가한 것이다. 실제 초기 상태는 $n_j{=}1$ 이 우선이라 네 전이 균일 $w=RT/F$ 로 평가되며(\S\ref{sec:sum}, 그림~\ref{fig:sumcurve}),
여기서는 전이별 폭$\cdot$높이 차이를 드러내는 폴백 폭 쪽을 보였다.
```
**제안** (② 대체 — 캡션 서두):
```latex
\caption{흑연 staging 의 갤러리 채움 도식(위)과 대응 $\dd Q/\dd V$ peak(아래, 식~\eqref{eq:eqpeak} 의
수치 평가 --- $\dd Q/\dd V=Q_j\xi_\eq(1-\xi_\eq)/w_j$, 표~\ref{tab:staging} 의 $U_j,Q_j$ 와 \S\ref{sec:sum} 폭 폴백 $w_j$).
```
**제안** (③ 대체 — 캡션 중):
```latex
아래: 폭 폴백 값으로 평가한 네 전이 peak --- 높이 $Q_j/(4w_j)$ 는 전이마다 크게 다르다
($2\to1$ 이 가장 큼, $10.4\,Q_\cell/$V; $n_j{=}1$ 우선의 실제 초기 폭 $w{=}RT/F$ 에서는 $4.87$ --- \S\ref{sec:sum}).
```
**근거**: `ch1_sec10_sum.tex:44-46`(n 우선 규정)·tab:staging 열 구성·fig:sumcurve 좌표열(0.085, 4.865)·전수 재계산. 기존 그림·수치·자산은 그대로 두고 귀속 서술만 정정하는 보강안(P5 준수).

### A01-H2 — tab:notation T_rep 행의 "N1" 오귀속 [논리 H]

**현행** (`ch1_sec01_n0n1.tex:52`):
```latex
$T_\rep$ & K & 비등온 시 전이당 상수 평가에 공통으로 쓰는 \emph{전 구간 평균} $\overline T$(전이 창별 평균이 아니라 진행 구간 전체의 단일 평균) — N1$\cdot$N3$\cdot$N7 대표조건 평가 \\
```
**문제(코드·본문 전수 추적으로 확정)**: N1(분극, eq:vn `V_n=V_app−σ_d|I|R_n`)은 온도를 쓰지 않는다(R_n 은 상수 lumped 저항 — 표 53행·코드 `self.Rn`). T_rep 의 실사용처 전수: 본문 = `ch1_sec04_hys.tex:272` 분기 gap $\Delta U_j^\hys(T_\rep)$(N3)·`ch1_sec08_lag.tex:128` "전이당 상수 하나(대표 $T_\rep\cdot$대표 $n$)"(N7)·`ch1_appB_codemap.tex:154`(N7). 코드 = 527(정의)·556(func_U_branch — N3)·566/568(_n_factor·_resolve_lag_length — N7). **N1 사용처는 어디에도 없다**. 마스터 조회표의 오귀속은 구현 독자를 직접 오도한다.

**제안** (행 대체):
```latex
$T_\rep$ & K & 비등온 시 전이당 상수 평가에 공통으로 쓰는 \emph{전 구간 평균} $\overline T$(전이 창별 평균이 아니라 진행 구간 전체의 단일 평균) — N3(분기 gap $\Delta U_j^\hys$)$\cdot$N7(지연 길이 $L_{V,j}$) 대표조건 평가 \\
```
**근거**: 위 전수 추적. (만약 "N1" 이 다른 의도였다면 그 의도가 본문 어디에도 식·코드로 실현돼 있지 않으므로 어느 쪽이든 정정 필요.)

### A01-M1 — "전이 루프 N2–N9" vs 그림의 루프 N2–N8 + 합산 1회 [논리 M]

**현행** (`ch1_sec00_intro.tex:14-16`):
```latex
본 장은 이 곡선을 \emph{한 번 그리는 계산}을 처음부터 끝까지 그대로 따라간다. 계산은 전이 루프에 들어가기 전에
한 번만 실행되는 두 노드 --- 외부 실험조건을 모델 입력으로 환산하는 $\mathrm N0$ 와 측정 전위에서 분극을 벗기는
$\mathrm N1$ --- 에서 출발해, 전이 $j$ 마다 반복하는 전이 루프 $\mathrm N2$--$\mathrm N9$ 로 진행한다(그림~\ref{fig:spine}). 각 절은 그 한 단계의 물리식을, 그 단계를
```
**문제(그림·코드 대조로 확정)**: fig:spine 의 파선 루프 상자는 `fit=(n2)(n3)(n45)(n78)` = **N2–N8** 이고, N9 는 소스 주석("post-loop: sum over transitions j, once")과 캡션("모든 전이가 이 loop 를 마치면 N9(진한 상자, 식 eq:sum)가 배경 위에 합산한다") 모두에서 루프 밖 1회다. 코드도 `for tr` 루프 밖에서 `bg + acc_prog` 로 곡선을 닫는다. 본문 "전이 루프 N2–N9" 는 자기 그림과 어긋난다.

**제안** (해당 구 대체):
```latex
$\mathrm N1$ --- 에서 출발해, 전이 $j$ 마다 반복하는 전이 루프 $\mathrm N2$--$\mathrm N8$ 로 진행하고,
모든 전이가 루프를 마치면 합산 $\mathrm N9$ 가 배경 위에 한 곡선을 닫는다(그림~\ref{fig:spine}).
```
**근거**: fig:spine 소스(75-78행 fit 범위)·캡션 85행·코드 544-587행.

### A01-M2 — "본론 N1–N9 … 본론에 앞선 Part 0": 순서·귀속 부정확 + 평형식 목록에 전하 보존식 누락 [논리+보완 M]

**현행** (`ch1_sec00_intro.tex:21-24`):
```latex
문서는 세 층으로 짜인다. 본론 $\mathrm N1$--$\mathrm N9$ 가 결과로만 받아 쓰는 평형식들(점유 통계$\cdot$
logistic$\cdot$평균장 상호작용$\cdot$Nernst 식)을, 본론에 앞선 Part 0(\S\ref{sec:sm-found})이 통계역학 첫
원리(분배함수)에서 유도해 둔다. 그 위에서 본론(Part I)이 흑연 곡선 사슬을 닫고, 이어지는 Part T 가 같은
전극$\cdot$같은 입력에서 곡선 대신 \emph{열} --- 반응 엔트로피의 세 분포 분해와 가역 발열 --- 을 닫는다.
```
**문제(toc·원문 대조로 확정)**: (i) 지면 순서는 §1.1(N0·N1) → §1.2(Part 0) → §1.3(N2)… 이므로 "본론 N1–N9" 에 "앞선" Part 0 이라는 서술은 N1 에 대해 거짓이다(Part 0 은 N1 **뒤**에 온다). (ii) N1(eq:vn)은 나열된 평형식을 하나도 받아 쓰지 않는다 — 받아 쓰는 것은 N2 이후 사슬이다. (iii) 나열된 Part 0 산출 목록에 **다클래스 전하 보존식**(§1.2.6 "전하 보존식의 대정준 반전")이 빠져 있다 — 이 식이 N6·N9 의 출발식($Q_\cell q=Q_\bg+\sum_jQ_j\xi_j$, sec06 (a)·sec10)이자 P3-2 의 중심식이므로 목록 누락은 실질 손실이다.

**제안** (두 문장 대체):
```latex
문서는 세 층으로 짜인다. 본론의 전이 사슬 $\mathrm N2$--$\mathrm N9$ 가 결과로만 받아 쓰는 평형식들(점유 통계$\cdot$
logistic$\cdot$평균장 상호작용$\cdot$다클래스 전하 보존식$\cdot$Nernst 식)을, 그 사슬에 앞선 Part 0(\S\ref{sec:sm-found})이 통계역학 첫
원리(분배함수)에서 유도해 둔다(기호$\cdot$규약과 한 번만 실행되는 $\mathrm N0\cdot\mathrm N1$ 은 그보다도 앞서 \S\ref{sec:notation} 이 세운다).
```
**근거**: `ch1_graphite_v1.0.22.toc`(§1.1→§1.2→§1.3)·sec06:7-9(보존식 출발)·sec02b §1.2.6 제목·P3-2(전하 보존 중심식 유지 — 서론 층위 배치에서 강화).

### A01-M3 — fig:spine 캡션의 입·출력 도치 [논리 M]

**현행** (`ch1_sec00_intro.tex:80-82`):
```latex
\caption{한 곡선을 그리는 계산 진행(spine). 외부 실험조건 $(\sigma_d,|I|,T,Q_\cell)$
이 N0 에서 모델 입력으로 환산되고(식~\eqref{eq:n0map}), 분극으로 내부 전위 $V_n$ 을 얻은 뒤(N1,
식~\eqref{eq:vn}), 파선 상자 안(전이별 반복 계산 단위, $j=1..N_p$)에서 전이 $j$ 마다 평형 중심(N2)$\cdot$히스
```
**문제**: $\sigma_d$·$|I|$ 는 N0 환산의 **출력**(모델 입력)이지 외부 실험조건이 아니다 — 외부 실험조건은 본문(sec01:10)·그림 io 노드("input: $V_\app$, direction $\to\sigma_d$, c-rate $\to|I|$, $T$, $Q_\cell$") 대로 $(V_\app,\text{direction},\text{c\_rate},Q_\cell,T)$ 다. 캡션이 자기 그림의 io 노드와 어긋나고 $V_\app$ 도 빠뜨린다.

**제안** (캡션 서두 대체):
```latex
\caption{한 곡선을 그리는 계산 진행(spine). 외부 실험조건 $(V_\app,\text{direction},\text{c\_rate},Q_\cell,T)$
이 N0 에서 모델 입력 $(\sigma_d,|I|)$ 로 환산되고(식~\eqref{eq:n0map}), 분극으로 내부 전위 $V_n$ 을 얻은 뒤(N1,
식~\eqref{eq:vn}), 파선 상자 안(전이별 반복 계산 단위, $j=1..N_p$)에서 전이 $j$ 마다 평형 중심(N2)$\cdot$히스
```
**근거**: sec01:10-18(eq:n0map 정의)·fig:spine io 노드(53행).

### A01-M4 — "이 규약은 … Chapter 2(LCO) 전건에서 유지" 과대 주장 [논리 M]

**현행** (`ch1_sec01_n0n1.tex:28-32`, 부호 규약 문단 중):
```latex
\textbf{부호 규약.} 전위는 흑연 음극 반쪽전지 전위(vs Li/Li$^+$)다. 방향 부호 $\sigma_d=\pm1$
(방전 $+1$/충전 $-1$)이며, 평형 진행률 $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$ 에서 방전
($\sigma_d=+1$)은 $V\!\uparrow\Rightarrow\xi_\eq\!\uparrow$(전위를 올리면 탈리튬화). 분기 중심 $+\tfrac12\sigma_d(\cdots)$
는 $\sigma_d$ 를 따라 방전$\cdot$충전이 반대로 갈리고, 꼬리는 충전에서 적분 방향이 반전된다. 이 규약은 \S\ref{sec:notation}--\S\ref{sec:sum}
과 Chapter 2(LCO) 전건에서 유지되며 \S\ref{sec:signcheck} 가 전수 검산한다.
```
**문제(원문·코드 대조로 확정)**: 이 규약의 두 요소 — "전위 = 흑연 음극 반쪽전지 전위"·"방전 +1/충전 −1"(셀 라벨 매핑) — 는 Chapter 2 에서 문자 그대로 유지되지 **않는다**. Ch2 의 유지 대상은 전극-중립 불변량 "σ_d 슬롯의 물리 = 탈리튬화 = +1" 이고, LCO 는 **충전**이 탈리튬화라 셀 라벨이 반전 환산된다(`ch1_sec11_lcointro.tex:35` "LCO \emph{충전}$\mapsto\sigma_d{=}+1$", eq:lco-sigmaslot; 코드 `if not self._delith_is_discharge: sigma_d = -sigma_d`). '전건 유지' 를 그대로 믿고 Ch2 로 간 독자는 LCO 방향을 거울로 오독한다.

**제안** (마지막 문장 대체):
```latex
이 규약은 \S\ref{sec:notation}--\S\ref{sec:sum} 전건에서 유지되고 \S\ref{sec:signcheck} 가 전수 검산하며,
Chapter 2(LCO)는 같은 규약을 전극-중립형으로 잇는다 --- $\sigma_d$ 슬롯의 물리는 ``탈리튬화 $=+1$''
그대로이고, 양극에서는 셀 라벨(충$\cdot$방전)이 식~\eqref{eq:lco-sigmaslot} 로 환산되어 들어온다(\S\ref{sec:lco-intro}).
```
**근거**: sec11:35·86-95(방향 규약 절)·sec18 facade("LCO 전극은 셀 라벨을 탈리튬화 부호로 자동 환산")·코드 curve(). xr 전방 참조는 기존 관행(sec18 이 이미 \eqref{eq:lco-sigmaslot} 사용) — 빌드 안전.

### A01-M5 — s 의 소멸 경로: "s=1 대입" 단일 서술이 eq:xieq 계보와 불일치 [논리 M]

**현행 ①** (`ch1_sec01_n0n1.tex:32-34`):
```latex
유도 편의를 위해 \S\ref{sec:center}$\cdot$\S\ref{sec:hys}
의 $U_j$ 정의 관례에는 \emph{항상 $+1$ 인 고정 부호} $s$ 를 따로 두는데, 이는 방향에 따라 $\pm1$ 로 바뀌는 $\sigma_d$ 와
별개다 --- $s$ 는 Part 0 의 박스에서 명시적으로 유지되다가 본론의 결과-사슬 boxed 식에서 $s{=}1$ 로 대입돼 소멸한다.
```
**현행 ②** (`ch1_sec01_n0n1.tex:48`, 표 s 행):
```latex
$s$ & --- & 유도 전용 고정 부호 — 항상 $+1$(\S\ref{sec:center}$\cdot$\S\ref{sec:hys} 의 $U_j$ 정의 관례); 방향에 따라 $\pm1$ 로 바뀌는 $\sigma_d$ 와 별개, 본론 결과-사슬 boxed 식에서 $s{=}1$ 대입돼 소멸(Part 0 의 박스는 $s$ 를 명시 유지) \\
```
**문제(원문 재추적으로 확정)**: s 의 실제 소멸 경로는 두 갈래다 — (i) 중심식 계열: $\Delta G_j=-sFU_j$ 에 $s{=}1$ 대입(`ch1_sec02b_part0.tex:433`, `ch1_sec03_center.tex` eq:Ujmid) ✓ 현행 서술과 일치; (ii) 진행률식 계열: eq:logisticsolve 의 s 자리는 $s{=}1$ 이 아니라 **$s\to\sigma_d$ 치환**으로 일반화된다(`ch1_sec02b_part0.tex:200` "고정 부호 $s$ 자리에 방향 부호 $\sigma_d$", `ch1_sec05_width.tex:276-277` "$s\to\sigma_d$ 치환은 여집합 교환과 동치"). s 를 추적하는 독자가 eq:xieq 에서 1 이 아닌 σ_d 를 만나면 현행 서술과 모순으로 읽는다 — s/σ_d 구분 문단의 취지(부호 혼동 방지)에 반한다.

**제안 ①** (해당 구 대체):
```latex
별개다 --- $s$ 는 Part 0 의 박스에서 명시적으로 유지되다가 본론의 결과-사슬 boxed 식에서 소멸한다:
중심식 계열(식~\eqref{eq:Uj})에서는 $s{=}1$ 대입으로, 진행률식의 방향 자리(식~\eqref{eq:xieq})에서는
$s\to\sigma_d$ 일반화(여집합 교환과 동치 --- \S\ref{sec:width})로.
```
**제안 ②** (표 행 대체):
```latex
$s$ & --- & 유도 전용 고정 부호 — 항상 $+1$(\S\ref{sec:center}$\cdot$\S\ref{sec:hys} 의 $U_j$ 정의 관례); 방향에 따라 $\pm1$ 로 바뀌는 $\sigma_d$ 와 별개. 본론 boxed 식에서 소멸 — 중심식은 $s{=}1$ 대입, 진행률식 방향 자리는 $s\to\sigma_d$ 일반화(\S\ref{sec:width}; Part 0 의 박스는 $s$ 를 명시 유지) \\
```
**근거**: sec02b:189-200·433·sec05:276-281 원문.

### A01-M6 — §pointwise 의 T_rep 문장: 점별 사용과 평균 정의의 혼선 [설명+수식화 M]

**현행** (`ch1_sec01_n0n1.tex:193-194`):
```latex
온도가 배열 $T(V)$ 이면 각 $V_n$ 점의 값을 그대로 취해 전이당 상수
평가용 대표 온도 $T_\rep=\overline{T}$ 를 얻고, 스칼라면 $T$ 를 공통으로 쓴다.
```
**문제**: "각 $V_n$ 점의 값을 그대로 취해 … $T_\rep=\overline T$ 를 얻고" 는 (a) 점별 양은 각 점의 $T(V_n)$ 을 그대로 쓴다, (b) 전이당 상수는 전 구간 **평균** $T_\rep$ 한 값으로 평가한다 — 서로 다른 두 규칙을 한 구문에 눌러 담아, "점 값을 취하는 것"이 곧 $T_\rep$ 획득으로 읽힌다(평균 단계가 문면에서 증발). 표 52행("전 구간 평균 … 단일 평균")·코드(`T_rep=float(np.mean(T_prog))`; U_j·w·ξ_eq 는 `T_prog` 점별)와 정합하도록 분리 필요.

**제안** (문장 대체):
```latex
온도가 배열 $T(V)$(비등온)이면 \emph{점별 양}($U_j\cdot w_j\cdot\xi_\eq$)은 각 $V_n$ 점의 $T(V_n)$ 값을
그대로 쓰고, \emph{전이당 상수}(분기 gap$\cdot$지연 길이 --- N3$\cdot$N7)는 진행 구간 전체의 단일 평균
$T_\rep=\overline{T}$ 한 값으로 평가한다; 스칼라면 둘 다 $T$ 를 공통으로 쓴다.
```
**(선택) 수식화 — 관점④** (신규 라벨 제안 `eq:trep`, 같은 자리 삽입):
```latex
\begin{equation}
T_\rep\;\equiv\;\overline{T(V_n)}\;=\;\frac1N\sum_{i=1}^{N}T(V_{n,i})
\qquad(\text{스칼라 }T\text{ 면 }T_\rep=T),
\label{eq:trep}
\end{equation}
```
**근거**: 표 52행·코드 527행·sec08:128("전이당 상수 하나(대표 $T_\rep\cdot$대표 $n$)").

### A01-M7 — R_n(N1) ↔ L_V(N7) ↔ η 산포(③) 분담 경계 미서술 [보완 M]

**현행** (`ch1_sec01_n0n1.tex:160-161` — 보완 앵커; 이 소절 어디에도 분담 서술 없음):
```latex
계산의 첫 물리식은 분극을 벗기는 환산이다. 관측은 유한 전류에서 이루어지므로 측정 전위 $V_\app$ 에는 셀의
직렬 저항을 통과한 IR 분극이 실려 있고, 평형 열역학이 사는 전위는 그 분극을 벗긴 내부 전위 $V_n$ 이다.
```
**문제(전수 grep 으로 확정)**: 전류 효과가 세 자리(N1 의 $R_n$, N7–N8 의 $L_V$ 꼬리, §7 ③ 의 국소 과전압 $\eta$ 산포)에 나뉘어 들어가는데, 셋의 분담 경계·무이중계산 근거를 문서 어디에서도 말하지 않는다($R_n$ 등장처 전수: sec00 그림·sec10($R_n{=}0$)·sec18·appA S8·appB — 분담 서술 0건; sec07 ③ 은 $\eta$ 산포와 ① 꼬리의 경계만 논함). "분극 저항으로 벗겼는데 왜 또 동역학 지연이 남는가 — 같은 과전압의 이중계산 아닌가"는 전문 독자가 §1 에서 바로 던질 질문이다.

**제안** (식~eq:vn 검산 문장 뒤, `:184` "…두 전위가 일치한다." 다음에 추가):
```latex
이 보정의 담당 범위를 분명히 하면 --- $R_n$ 은 전이 \emph{바깥}의 직렬(lumped) 성분으로 곡선 전체를
전위축에서 $\sigma_d|I|R_n$ 만큼 평행이동시킬 뿐이고, 전이 \emph{안}의 유한 완화가 만드는 모양 변형
(비대칭 꼬리)은 지연 길이 $L_{V,j}$(\S\ref{sec:lag}--\S\ref{sec:tail})가, 입자마다 다른 국소 과전압의
\emph{산포}는 두-상 broadening 층(\S\ref{sec:broadening})이 따로 담당한다 --- 세 몫은 관측 효과
(평행이동$\cdot$비대칭 꼬리$\cdot$대칭 퍼짐)가 서로 달라 서로를 다시 세지 않는다.
```
**근거**: sec07:118-123(①/③ 경계·"이중계산" 어휘)·eq:vn 의 상수-이동 구조(재유도: $R_n\cdot|I|$ 상수 ⇒ 전 곡선 균일 이동). 기존 문장 삭제 없음 — 순수 추가.

### A01-M8 — ξ_j 의 충전 방향 의미 미정의 [보완 M]

**현행** (`ch1_sec01_n0n1.tex:24-26`):
```latex
\textbf{전이 인덱스.} $j=1,\dots,N_p$($N_p\approx3$--$4$). 전이 $j$ 의 진행률 $\xi_j$(방전 시 $0\to1$ 로 증가, 곧 탈리튬화 진행),
용량 가중 $Q_j$. 박스 결과식은 $j$ 첨자를 단다. 점유율과 진행률은 $\theta_j=1-\xi_j$ 로 묶이며(점유 $\theta$ 가 $1\to0$
줄어드는 것이 진행 $\xi$ 가 $0\to1$ 느는 것), 유도에서 둘은 부호 한 번 차이로 오간다.
```
**문제**: 진행률의 의미가 방전에 대해서만 정의된다. 충전에서 ξ 가 무엇인지(eq:xieq 의 $\sigma_d{=}-1$ 이면 전위 하강 방향으로 $0\to1$ — 곧 리튬화 진행 = 여집합 좌표)는 sec05:276-277 에서야 나온다. §1–§4 를 읽는 동안 충전 ξ 를 '탈리튬화 진행'으로 오독할 여지.

**제안** (첫 문장 보강 — 괄호 확장):
```latex
\textbf{전이 인덱스.} $j=1,\dots,N_p$($N_p\approx3$--$4$). 전이 $j$ 의 진행률 $\xi_j$(방전 시 $0\to1$ 로 증가, 곧 탈리튬화 진행;
충전의 진행률은 같은 분포의 여집합 좌표 $\theta=1-\xi$ 가 맡는다 --- \S\ref{sec:width} 가 식으로 회수),
용량 가중 $Q_j$.
```
**근거**: sec05:276-277 원문 표현 차용(어조 동일).

### A01-M9 — 기호 마스터표 누락 행: ξ_j·θ_j·r_j·N_p·q [보완 M]

**현행** (`ch1_sec01_n0n1.tex:61` — 삽입 위치 앵커):
```latex
$\xi_{\eq,j}$ & --- & 평형 진행률(logistic) \\
```
**문제**: 마스터표(참조용 조회표 — 39-40행 자기 선언)에 본론 중심 변수가 빠져 있다: 실제 진행률 $\xi_j$(보존식 $Q_\cell q=Q_\bg+\sum_jQ_j\xi_j$ 와 eq:sum 의 변수; sec09 "$\xi_j=\xi_{\eq,j}-r_j$"), 점유율 $\theta_j$, 지연 $r_j$, 전이 개수 $N_p$, 용량 좌표 $q$(인과 순서의 기준축 — sec09 (a)). 독자가 sec06 의 보존식에서 $\xi_j$ 를 만나 표를 찾으면 $\xi_{\eq,j}\cdot\xi_{\mathrm{lag},j}$ 만 있다.

**제안** (위 행 직후에 4행, — 실험조건 구획에 $N_p\cdot q$ 1–2행 추가; 예시):
```latex
$\xi_j$ & --- & 전이 $j$ 실제 진행률 $=\xi_{\eq,j}-r_j$(지연 포함 — \S\ref{sec:tail}); 보존식$\cdot$식~\eqref{eq:sum} 의 변수 \\
$\theta_j$ & --- & 점유율 $=1-\xi_j$ \\
$r_j$ & --- & 지연 $=\xi_{\eq,j}-\xi_j$(\S\ref{sec:lag}) \\
$N_p$ & --- & 전이 개수($\approx3$--$4$; 표~\ref{tab:staging} 는 $4$) \\
$q$ & --- & 무차원 용량 좌표 $=Q/Q_\cell$ — 항상 진행 방향으로 증가(인과 순서의 기준축, \S\ref{sec:tail}) \\
```
**근거**: sec06:7·sec09:96·sec09 (a)(q 정의)·표의 자기 선언("마스터 대응").

### A01-L1 — 관측 (b) "극판 전위" 의 층위 [설명 L]

**현행** (`ch1_sec00_intro.tex:31-33`, 인용 블록):
```latex
$\dd Q/\dd V$ 상전이 peak 의 위치$\cdot$너비$\cdot$높이는 (a) 온도 $T$, (b) 극판 전위, (c) C-rate(전류)
세 가지에 따라 변한다.
```
**문제**: (a)·(c)는 실험자가 잡는 손잡이, (b)는 곡선의 가로축 좌표라 층위가 섞여 독자가 걸린다(바로 뒤 문단이 "전위는 장벽 $\Delta G_a$ 자체"로 해소하지만 인용 블록 안에서는 미해소).

**제안** (해당 구 대체):
```latex
$\dd Q/\dd V$ 상전이 peak 의 위치$\cdot$너비$\cdot$높이는 (a) 온도 $T$, (b) 그 전이가 앉은 극판 전위(곧 국소 구동력의 크기), (c) C-rate(전류)
세 가지에 따라 변한다.
```
**근거**: 뒤 문단(36-39행)의 세 갈래 설명과 층위 일치.

### A01-L2 — bgbox (iii) 의 부호 있는 전류 $I$ 미정의 [보완 L]

**현행** (`ch1_sec01_n0n1.tex:215-216`):
```latex
(iii) \emph{가역 발열}: $-IT\,\partial U_\mathrm{oc}/\partial T$ 는 등온
열량 측정으로 독립 검증되는 양이고, 그 계산 절차와 실측 대응은 Part T 의 방법론 절(\S\ref{sec:method})이 담당한다.
```
**문제**: 본 장 곡선부 표기는 $|I|$·$\sigma_d$ 뿐(표~tab:notation)이라 부호 있는 $I$ 는 여기서 처음이자 무정의로 등장한다. 부호·라벨 층위는 Part T(\S revheat, eq:qrev·ssec:signlabel)가 전담하므로 전방 지시 한 구가 필요하다.

**제안** (해당 구 대체):
```latex
(iii) \emph{가역 발열}: $-IT\,\partial U_\mathrm{oc}/\partial T$(부호 있는 $I$ 의 층위$\cdot$규약은 Part T \S\ref{sec:revheat} 소관 — 본 절 곡선부 표기는 $|I|\cdot\sigma_d$ 뿐)는 등온
열량 측정으로 독립 검증되는 양이고, 그 계산 절차와 실측 대응은 Part T 의 방법론 절(\S\ref{sec:method})이 담당한다.
```
**근거**: ch2_sec07(동일 빌드 Part T):7·37·76(부호·라벨 층위 절과 $\dot Q_\rev=-IT\partial U_\oc/\partial T$).

### A01-L3 — keybox "다음 절부터" [설명 L]

**현행** (`ch1_sec01_n0n1.tex:199-201`, keybox):
```latex
\textbf{두 전위.} $V_\app$(측정)$\cdot$$V_n$(내부, 식~\eqref{eq:vn})만 남는다. 다음 절부터 전이 루프의 모든
물리량 --- 평형 중심$\cdot$분기$\cdot$폭$\cdot$평형 진행률$\cdot$지연 꼬리 --- 는 이 $V_n$ 위에서 바로
평가되고, 그 값이 곧 출력이다.
```
**문제**: 지면상 다음 절은 Part 0(§1.2, 전이 루프 아님)이고 전이 루프는 §1.3(N2)부터다.

**제안** (해당 구 대체):
```latex
\textbf{두 전위.} $V_\app$(측정)$\cdot$$V_n$(내부, 식~\eqref{eq:vn})만 남는다. Part 0 를 지나 전이 루프(\S\ref{sec:center} 이후)의 모든
물리량 --- 평형 중심$\cdot$분기$\cdot$폭$\cdot$평형 진행률$\cdot$지연 꼬리 --- 는 이 $V_n$ 위에서 바로
평가되고, 그 값이 곧 출력이다.
```
**근거**: toc 순서(§1.2 Part 0 → §1.3 N2).

### A01-L4 — I_abs 우선순위 미기재 [보완 L]

**현행** (`ch1_sec01_n0n1.tex:16`, 식 eq:n0map 내):
```latex
|I|=\text{c\_rate}\cdot Q_\cell\quad(\text{또는 }I_\mathrm{abs}\text{ 직접 지정}).
```
**문제**: c_rate 와 $I_\mathrm{abs}$ 를 함께 주면 어느 쪽이 이기는지 문서만으로 모른다(코드 curve(): "주면 c\_rate 무시(우선)").

**제안** (괄호 보강):
```latex
|I|=\text{c\_rate}\cdot Q_\cell\quad(\text{또는 }I_\mathrm{abs}\text{ 직접 지정 — 지정 시 c\_rate 무시}).
```
**근거**: `Anode_Fit_v1.0.22.py` curve() docstring·구현("I_abs … 주면 c_rate 무시(우선)"); "본 장만으로 재현 코드" 목표(서론 19행)와 정합.

### A01-L5 — DVA 무언급 + bloom2005 의 성격 [보완 L]

**현행** (`ch1_sec00_intro.tex:7-8`):
```latex
리튬이온전지 흑연 음극의 incremental capacity analysis(ICA)는 충방전 곡선 $Q(V)$ 의 미분
$\dd Q/\dd V$ 를 관측 대상으로 삼는다 \cite{bloom2005,dubarry2012}.
```
**문제**: 프로젝트 목표(P1)는 ICA(dQ/dV)·DVA(dV/dQ) 병기인데 Ch1 빌드 전체에 dV/dQ 언급이 0건이고(전수 grep), 인용 중 bloom2005 는 DVA(differential voltage) 원전이다. "DVA 는 어디서 다루나"는 자연스러운 독자 질문.

**제안** (문장 뒤 1문 추가 — 기존 인용 삭제 없음):
```latex
짝 미분 $\dd V/\dd Q$ 를 읽는 differential voltage analysis(DVA)\cite{bloom2005} 는 같은 곡선의 역수
시선이며, 본 장은 $\dd Q/\dd V$ 로 통일해 적는다.
```
**근거**: P1(ICA·DVA)·bib 19행(bloom2005 = "Differential voltage analyses…")·본 장 dV/dQ 부재(grep 0건). 원장 V1 기존 키만 사용 — 신규 서지 없음.

### A01-L6 — fig:staging 도입 문장 성분 정리 [설명 L]

**현행** (`ch1_sec01_n0n1.tex:90-92`):
```latex
흑연 staging 의 갤러리 채움을 그림~\ref{fig:staging} 에 둔다 --- 각 stage 전이가 한 peak 를 남기고,
흑연 staging 네 전이의 초기값(문헌 기반\cite{dahn1991,ohzuku1993} --- 값의 확정과 tier 는
\S\ref{sec:sum} 표~\ref{tab:staging} 소관)이 이 네 전이에 대응한다.
```
**문제**: "초기값이 … 전이에 대응한다"는 술어가 헛돌고 "흑연 staging" 이 두 번 반복된다.

**제안** (대체 — A01-H1 제안 ① 과 이어짐):
```latex
흑연 staging 의 갤러리 채움을 그림~\ref{fig:staging} 에 둔다 --- 각 stage 전이가 한 peak 를 남기며,
네 전이 각각의 초기값(문헌 기반\cite{dahn1991,ohzuku1993} --- 값의 확정과 tier 는
\S\ref{sec:sum} 표~\ref{tab:staging} 소관)을 아래 축 평가에 썼다.
```
**근거**: 내용 불변 문장 정리(어조 유지).

### A01-L7 — 영전류 잔존 히스 주장의 조기 인용(선택) [보완 L]

**현행** (`ch1_sec00_intro.tex:32-33`, 인용 블록 말미):
```latex
서로 다른 전위에 peak 를 남기며(충방전 히스테리시스 --- 이하 `히스'로도 축약), 이 갈림에는 전류를 $0$ 으로 줄여도 사라지지 않는 성분이 있다.
```
**제안** (선택 — 말미에 기존 원장 키 병기):
```latex
서로 다른 전위에 peak 를 남기며(충방전 히스테리시스 --- 이하 `히스'로도 축약), 이 갈림에는 전류를 $0$ 으로 줄여도 사라지지 않는 성분이 있다\cite{dreyer2010}.
```
**근거**: 실측 주장 첫 인용이 §1.4(eq:Ubranch 부호 문단)라 서론 관측 블록은 무근거 상태 — dreyer2010 은 원장 V1 기존 키(신규 아님). 관측 블록을 인용 없이 순수 현상 기술로 두는 현행 방침도 일관적이므로 '선택' 등급.

### A01-L8 — ΔH_a^eff 행의 무조건부 등식 [보완 L]

**현행** (`ch1_sec01_n0n1.tex:78`):
```latex
$\Delta H_{a,j}^\eff$ & J/mol & 유효 장벽 $=\Delta H_a-\chi_d\Omega$ \\
```
**제안**:
```latex
$\Delta H_{a,j}^\eff$ & J/mol & 유효 장벽 $=\Delta H_a-\chi_d\Omega$(장벽 보강 적용 시; 미적용이면 $\Delta H_a$ 그대로 — \S\ref{sec:lag}) \\
```
**근거**: sec08:106-107 "유효 장벽 보강이 켜져 있을 때만 … 꺼져 있으면 그대로 $\Delta H_a$"(암묵 전제 명시)와 표의 정합.

### A01-L9 — σ_d 작용처 셋: 산문→미니표(선택) [수식화 L]

**현행** (`ch1_sec01_n0n1.tex:20-22`):
```latex
방향 부호가 실제로 작용하는 자리는 셋뿐이다 --- 분극 부호($\mathrm N1$)$\cdot$분기 중심 선택($\mathrm N3$)$\cdot$꼬리($\mathrm N7\cdot\mathrm N8$:
방향별 전달계수 $\chi_d$ 가 꼬리 \emph{길이}를, 적분 방향(식~\eqref{eq:reversal})이 인과 기억의 진행 \emph{방향}을 가른다).
```
**제안** (선택 — 산문 유지 + 직후 조회용 미니표 추가):
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}lll@{}}
\toprule
$\sigma_d$ 작용처 & 노드 & 식 \\
\midrule
분극 부호 & N1 & \eqref{eq:vn} \\
분기 중심 선택 & N3 & \eqref{eq:Ubranch} \\
꼬리 --- 전달계수$\cdot$적분 방향 & N7$\cdot$N8 & \eqref{eq:chid}$\cdot$\eqref{eq:reversal} \\
\bottomrule
\end{tabular}
\end{center}
```
**근거**: 조회 편의(내용 동일). 산문 자체는 정확함을 재검증했으므로(아래 무발견 축) 표는 순수 보강.

### A01-L10 — §pointwise 첫 문장의 표면 긴장 [설명 L]

**현행** (`ch1_sec01_n0n1.tex:187-188`):
```latex
이후 모든 전이 계산은 내부 전위 $V_n$ 이 주어지는 낱낱의 점에서 직접 닫힌다 --- 전이 $j$ 의 기여
$[\text{peak shape}]_j(V_n)$ 은 그 점 하나만으로 완결되는 값이고, 공유된 보조 좌표를 거치지 않는다.
```
**문제**: 직후 문장이 말하는 인과 기억은 과거 전 구간의 적분이라 "그 점 하나만으로"와 순간적으로 충돌해 읽힌다(문단 후반이 해소하지만 첫 문장에서 선제 가능).

**제안** (대체):
```latex
이후 모든 전이 계산은 내부 전위 $V_n$ 이 주어지는 낱낱의 점에서 직접 닫힌다 --- 전이 $j$ 의 기여
$[\text{peak shape}]_j(V_n)$ 은 그 점 자신(과 그 점의 과거에 대한 적분 하나)으로 완결되는 값이고, 여러
전이$\cdot$여러 평가점이 공유하는 보조 좌표나 패딩 격자를 거치지 않는다.
```
**근거**: eq:lag 의 점별 적분 구조(sec09:57-63 "임의의 평가점 $V$ 마다 그 점 하나의 적분으로 닫힌다")와 동일 논지로 정렬.

---

## 등급별 정리

- **H (2건)** — A01-H1(fig:staging '초기값·실제 peak' 폭 귀속이 §10 의 n-우선 초기 상태·fig:sumcurve 와 상충 + 표에 없는 w_j 열 인용), A01-H2(마스터표 T_rep 행의 N1 오귀속). 두 건 모두 수치 재계산·코드 추적으로 확정. 물리식 자체의 오류는 아니며 **귀속·상호 정합** 결함.
- **M (9건)** — 구조 서술 불일치(M1 루프 범위, M2 본론/Part 0 순서+전하 보존식 누락, M3 캡션 입출력 도치), 과대 주장(M4 Ch2 전건 유지), 계보 부정확(M5 s 소멸 경로), 설명 혼선(M6 T_rep 문장), 빠진 논증(M7 R_n/L_V/η 분담), 정의 공백(M8 충전 ξ), 마스터표 누락(M9).
- **L (10건)** — 문체·조회 편의·선택적 보강(L1–L10).

## §서치 (문헌 서치 위임 기록)

**하이쿠 서브에이전트 미가동 — 사유**: 본 두 절의 \cite 8종(bloom2005·dubarry2012·dahn1991·ohzuku1993·weppner_huggins1977·reynier2003·swiderska2019·baek_pilon2022)은 전부 `V1022_REFERENCE_LEDGER.md` 가 승계한 v1.0.21 원장 V1 키로 확인했고(ch1v22_bib.tex 의 DOI 표기 존재 병행 확인), 본 검토의 모든 제안은 **신규 문헌을 요구하지 않는다**(L5·L7 제안도 기존 원장 키 재배치·병기뿐). 기억 서지 신규 도입 0건.

## 무발견 축 (검토했으나 문제 없음)

1. **eq:vapppol→eq:vnmid→eq:vn 유도·부호**: 방전(산화, η>0 ⇒ $V_\app>V_n$)·충전 양방향 재유도 — 부호 사슬 정확. appA S8 과 정합.
2. **eq:n0map 차원**: [1/h]·[A h]→[A]·정규화 규약 — 정합.
3. **fig:staging 수치 전수**: 4곡선 × 4–6점 표본 재계산(로지스틱 종 $Q_j\xi(1-\xi)/w_j$, x↔V 사상 $x=6.45(0.25-V)/0.20$) — 좌표열 전부 식의 정확 평가(±0.003). 눈금 사상·범례 배치·갤러리 채움 주기(1:4/1:3/2L/1:2/1:1, stage 1=LiC$_6$ 완채움)·위/아래 축 비선형 대응 경고 — 모두 정확.
4. **spine 노드 요약식 ↔ boxed 원식 전 항목 대조**: eq:Uj·eq:Ubranch·eq:wbase·eq:xieq·eq:LV·eq:peakshape·eq:eqpeak·eq:tail-limit·eq:sum — 그림 축약이 원식과 전부 일치(라벨 해소도 전건 확인).
5. **"방향 부호 작용처 셋뿐" 주장**: 코드에서 σ_d 등장 5곳(V_n·branch·logistic·χ_d·정렬) 중 logistic 몫은 $\xi\to1-\xi$ 대칭으로 평형 종에 관측 효과 없음을 재유도($\xi(1-\xi)$ 불변; 충전 꼬리도 거울 대칭 확인) — 주장 성립. sec02b:221·appA S2·S3 과 정합.
6. **부호 규약 문단의 흑연 물리**: 방전=탈리튬화=$V\uparrow\Rightarrow\xi_\eq\uparrow$·$U^{\dis}>U^{\chg}$(dreyer2010 부호) — 정확.
7. **수치 상수**: $w=RT/F=25.69$ mV(298.15 K)·$T_c=\Omega/2R$(eq:sm-thresh)·appA R1(ΔU^hys=86.7 mV — 독립 재계산 일치)·캡션 높이 $Q_j/(4w_j)$ 산술(폴백 폭 기준 10.417→"10.4") — 전부 재현.
8. **서지 대응**: GITT=Weppner–Huggins 1977(√t·확산계수 서술 포함)·엔트로피법=reynier2003/swiderska2019·해석 지도=baek_pilon2022(tier B, 1차 병기 규약 준수)·$\partial U_\oc/\partial T=\Delta S/F$ 의 부호·귀속(삽입 반응 기준, eq:Uj 와 정합) — 문제 없음.
9. **P3 규약 관점**: V 위계(본 장은 $V_\app$/$V_n$ 2전위 체계로 일관 — keybox 명시)·순환 의존(본 장 사슬은 feed-forward 로 설계되어 self-consistent 루프 자체가 없음 — 위반 아님)·ver.N↔Chapter 명칭 혼동(두 절 내 없음) — 결함 없음.
10. **bgbox·srcbox(측정 원리·다리)**: GITT↔eq:vn 대응표·가정 차(상수-저항 근사) 서술 — 정확·스코프 가드 적절. (L2 의 $I$ 표기만 예외.)

## 범위 밖 참고 (타 절 소관 — 본 절을 참조하는 곳의 오귀속)

- `ch1_sec09_tail.tex:40`: "하한 $-\infty$ 가 곧 \S\ref{sec:pol} 이 말한 ``자연 경계''다" — '자연 경계'는 \S\ref{sec:pol}(분극)이 아니라 **\S\ref{sec:pointwise}**(점별 평가 원칙, 제목 자체가 "자연 경계가 여는 여유")의 것. A09 창 소관이나 본 절 참조라 기록해 둔다.

## 말미 4-tier

- **확정(재계산·코드/원문 대조 완료)**: A01-H1, A01-H2, A01-M1, A01-M2, A01-M3, A01-M4, A01-M5, A01-M6, A01-L3, A01-L4, A01-L8 + 무발견 축 1–10 + 범위 밖 참고 1건.
- **추정(개선 이득 판단 — 채택은 사용자 결정)**: A01-M7, A01-M8, A01-M9, A01-L1, A01-L2, A01-L5, A01-L6, A01-L7, A01-L9, A01-L10 (사실관계 근거는 전건 원문 확인 완료; '보완이 이득'이라는 판단만 추정).
- **미검증**: 없음(신규 서지 도입 0건 — 검증 대상 부재; 제안 LaTeX 는 문법 검토만 했고 컴파일은 미실시 — 보고 전용 규율상 빌드 실행 안 함).
- **무발견 축**: 위 절에 10항 명시.

*본 문서는 제안만 담는다 — 소스 무수정(P5·BRIEF 규율). 제안 중 기존 자산·수식 삭제는 0건(전부 대체·보강).*
