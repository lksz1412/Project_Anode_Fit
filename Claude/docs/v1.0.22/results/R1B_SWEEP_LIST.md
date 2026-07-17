# R1B_SWEEP_LIST — 구획 전환(R1) 후 장 지칭 전수 스윕·분류표 (2026-07-17)

> 지위: `AUDIT_LINEAGE_v19_v22.md` §R1b 가 선언한 상세 목록(본 표가 유일 정본). 스윕 패턴 =
> `Chapter[~\s]*[12]|그 문건|별도 컴파일|본 문건|이 문건` (본문 행만 — 주석 행 제외), 파일군 = 신 3장 마스터의 \input 전량.
> 재현: 패턴·파일군 고정이므로 스크립트 재실행으로 그대로 재산출 가능.

## 집계·조정

| 시점 | 신Ch1 | 신Ch2 | 신Ch3 | 계 |
|---|---|---|---|---|
| 검출(정정 전 = R1 직후 HEAD) | 101 | 14 | 2 | **117** |
| S-008 정정 후(현행 — 본 표) | 102 | 14 | 2 | **118** |

117→118 조정 내역(전건 S-008 정정 산물): 이탈 2 = ch2_appA:51(③ “별도 컴파일”→“같은 문서 내”)·ch1_sec10_sum:162(⑦ “Chapter 2”→“Part T”+live ref) / 진입 3 = ch1_sec00_intro:27(①)·ch1_sec10_sum:168(②)·ch1_sec18_inputs:65(⑥) — 정정 문장이 신설한 **정당** 지칭(OK-S8). 나머지 정정 2곳(④ ch2_appA:67·⑤ ch1_sec14:57)은 정정 후에도 패턴에 걸리나 정당 지칭으로 잔존(OK-S8).

| 분류 | 건수 | 처분 |
|---|---|---|
| T1 | 20 | R2 이음매 본안 |
| T2 | 53 | R2 이음매 본안 |
| T3 | 5 | R2 이음매 본안(xr — 기계 치환 금지) |
| L1 | 1 | R3 본안 |
| W | 29 | R2/R3 어휘 일괄 판단 |
| OK-S8 | 5 | 유지(정정 결과) |
| OK-NEW | 5 | 유지(설계 의도) |
| **계** | **118** | R2/R3 인계 = T1+T2+T3+L1 = **79** + W 29 |

## 분류 정의

- **T1** — Part I/부록(구 Ch1 계열) 파일의 구 “Chapter 2”(열특성)·“그 문건” 지칭 — 이제 같은 문서 Part T. → R2: live 참조(\S\ref·\eqref)·“Part T” 호칭 전환
- **T2** — Part T(구 Ch2 계열) 파일의 구 “Chapter 1”·“그 문건” 지칭(자기 구지칭 “Chapter 2 종합식” 포함) — 대상이 같은 문서 Part 0/I/부록에 잔류. → R2: live 참조 전환
- **T3** — Part T 파일의 구 Ch1 §11~17(LCO) 지칭 — 대상이 신 Chapter 2 로 이동. → R2: xr 장 간 참조로 전환(방향이 T2 와 반대이므로 기계 치환 금지)
- **L1** — 신Ch2(LCO) 파일의 구 “Chapter 2”(열특성) 지칭 — 신 구조에서 자기 장 이름과 충돌. → R3: “Chapter 1 Part T” xr 전환(S-008 ⑤ 동종 잔여)
- **W** — “본 문건/이 문건” 어휘 — 장 단독 PDF 로는 유효하나 병합(단일 문건) 대비 “본 장/본서” 정합 검토 대상. → R2(신Ch1분)·R3(신Ch2분) 일괄 판단
- **OK-S8** — S-008 오문 정정의 결과 문장 — 신 구조 정합(정당 지칭). 유지
- **OK-NEW** — R1 신설 파일(장 서두·기호표)의 의도된 장 간 지칭 — 설계 그대로. 유지

## R2/R3 집행 지침(요지)

1. **T1·T2 는 같은 문서 내 전환**(“Chapter N”→“Part 0/I/T”+\S\ref, 서술형 “(eq:xxx)”→\eqref) — 산문 논지는 무변경(자산 보존), 지칭 계층만 교체.
2. **T3 는 장 간(xr) 전환** — T2 와 문면이 같아 보여도 대상 절이 신Ch2 로 이동했으므로 **행별 대조 필수**. 본 표의 5행이 전수.
3. **W 는 일괄 규칙으로**: 장 단독 배포 유지 + 병합 대비 → 권고 “본 장”(장 스코프 서술)·“본서”(작업 전체 선언 — 예: doc-leads 선언 ch2_appB:7). §제목·캡션 5곳(비고 표시)은 표기 변경 시 TOC·목록 연동 확인.
4. 본 표 밖 신규 발생 방지: R2/R3 완료 시 같은 패턴 재스윕 → 잔존 = OK 류만이어야 gate PASS.

## 전수 표 — 신 Chapter 1 (흑연+열특성) — 102건

| 파일:행 | 분류 | 발췌 | 비고 |
|---|---|---|---|
| `ch1_appA_signcheck.tex:6` | W | 본 문건 부호 사슬의 전건 검산을 표로 정리한다. 기준 명제는 \emph{방전 시 $V\!\uparrow\Rightarrow$ |  |
| `ch1_appB_codemap.tex:5` | W | 문건과 구현의 연계는 단방향이다 --- 구현(\code{Anode\_Fit\_v1.0.19.py})의 주석$\cdot$docstring 이 본 문건의 |  |
| `ch1_appB_codemap.tex:7` | W | 대응하는가''를 표로 제공하여, 본문을 코드 언급 없이 물리로만 읽을 수 있게 하면서 재현 가능성(이 문건과 |  |
| `ch1_appB_codemap.tex:132` | T1 | $\bar x$ 진입점 & \code{solve\_U\_oc}(Chapter 2 전하 보존 음함수의 유일근 솔버)$\cdot$ |  |
| `ch1_appB_codemap.tex:135` | T1 | additive --- 기존 $V_n$ 경로 무섭동; 요구명세는 Chapter 2 부록 B) \\ |  |
| `ch1_sec00_intro.tex:4` | W | \section*{서론 --- 이 문건이 따라가는 것} | §제목 |
| `ch1_sec00_intro.tex:14` | W | 본 문건은 이 곡선을 \emph{한 번 그리는 계산}을 처음부터 끝까지 그대로 따라간다. 계산은 전이 루프에 들어가기 전에 |  |
| `ch1_sec00_intro.tex:19` | W | 도착점은 한 줄 합산식과, ``이 문건만 보고 같은 곡선을 재현하는 코드를 짤 수 있다''는 실행 가능성이다. | 재현 선언 문구 — “이 장” 전환 시 의미 유지 주의 |
| `ch1_sec00_intro.tex:27` | OK-S8 | Chapter 2 가, 실리콘계$\cdot$혼합 음극은 Chapter 3 가 다룬다. 아래 관측이 이 모든 계산이 설명하려는 대상이다. |  |
| `ch1_sec00_intro.tex:38` | W | 속도가 같아지는 정지점)을, 다른 한편으로는 유한 전류의 지연(꼬리)을 낳는다 --- 본 문건의 유도는 줄곧 이 한 식의 가지를 |  |
| `ch1_sec01_n0n1.tex:152` | W | 선형 정렬되지 않는다)이라, 둘은 전이명(예 $2\to1$)으로만 대응시킨다. 본 문건 방향은 방전(탈리튬화)이다.} |  |
| `ch1_sec01_n0n1.tex:214` | T1 | broadening(\S\ref{sec:broadening})$\cdot$LCO 질서화(\S\ref{sec:lco-hys-od}) 구분과 Chapter 2 의 SOC 부호 |  |
| `ch1_sec01_n0n1.tex:216` | T1 | 열량 측정으로 독립 검증되는 양이고, 그 계산 절차와 실측 대응은 Chapter 2 의 방법론 절이 담당한다. |  |
| `ch1_sec02a_part0.tex:9` | T1 | 필요한 항(점유 자리의 진동 자유도, Chapter 2 의 포논$\cdot$전자 분포)은 해당 자리에서 명시적으로 도입한다. |  |
| `ch1_sec02a_part0.tex:202` | T1 | Chapter 2 다 --- 격자 진동의 양자(포논)는 보손이라 진동 엔트로피가 식~\eqref{eq:sm-fdbe} 의 $\bar n$ |  |
| `ch1_sec02a_part0.tex:233` | T1 | 자유도까지 포함한 완전한 단일 자리 대정준 분배함수이고, Chapter 2 의 단일 자리 분배함수(그 문건 식 |  |
| `ch1_sec02a_part0.tex:300` | T1 | 를 주는데, 이것이 Chapter 2 의 vibrational 엔트로피 사슬의 단일 자리 원형이다 --- 여기 자리 하나의 |  |
| `ch1_sec02a_part0.tex:302` | T1 | $q_k=[1-e^{-\beta\hbar\omega_k}]^{-1}$ 를 식~\eqref{eq:sm-sint} 에 넣으면 그 문건의 모드당 엔트로피 |  |
| `ch1_sec02b_part0.tex:183` | T1 | \Leftrightarrow\Delta G_j<0$, 곧 그 전이가 자발일 전위 창이 양수라는 부호 읽기도 동일). Chapter 2 의 식 |  |
| `ch1_sec02b_part0.tex:284` | T1 | 여럿으로 한 줄 넓혀, 본론과 Chapter 2 가 중심식으로 쓰는 전하 보존 음함수가 이 대정준 구조의 |  |
| `ch1_sec02b_part0.tex:345` | T1 | 이 식은 Chapter 2 가 겹침 가중의 출발점으로 세우는 전하 보존 음함수(그 문건 식 (eq:implicit))와 글자까지 | 서술형 “(eq:implicit)” → \eqref 전환 대상 |
| `ch1_sec02b_part0.tex:367` | T1 | 입자수 요동의 양성이 유일근을 보증한다는 이 한 줄이 Chapter 2 의 계산(그 문건의 유일근 서술)의 통계역학 |  |
| `ch1_sec02b_part0.tex:370` | T1 | \S\ref{sec:hys} 소관이며, 본론과 Chapter 2 가 반전에 실제로 쓰는 전이별 logistic 서식(폭 $w_j$ 의 이중지위는 |  |
| `ch1_sec02b_part0.tex:383` | T1 | \S\ref{sec:eqpeak} 과 Chapter 2 의 겹침 가중·계산용 종합식이 이 계단을 결과 사슬에서 그대로 되밟는다. 남은 |  |
| `ch1_sec02b_part0.tex:424` | T1 | 곡선맞춤이 아니라 배치 셈법에서 온다(Chapter 2 의 식 (eq:Vxi)가 같은 결론을 발열 관점에서 재사용한다). | 서술형 “(eq:Vxi)” → \eqref 전환 대상 |
| `ch1_sec04_hys.tex:6` | W | (그렇지 않으면 $U_j$ 그대로). 본 문건의 주 전개는 방전이며, 히스테리시스는 그 위의 \emph{구조적 분기}로 선언된다 --- 방전과 충전이 |  |
| `ch1_sec05_width.tex:238` | T1 | 얹으며, 그 $\partial w_j/\partial T=(R/F)(n_j(T)+T\,\dd n_j/\dd T)$ 가 가역 발열 config 항에 자기정합 전파된다(… |  |
| `ch1_sec05_width.tex:269` | T1 | 값 역시 평형이 결정하므로 첫째 지위(평형 예측)라는 성격은 변하지 않는다(Chapter 2 파생 C 와 동일 취지). |  |
| `ch1_sec05_width.tex:360` | T1 | 식~\eqref{eq:logisticsolve}$\cdot$\eqref{eq:xieq} 와 일치한다(Chapter 2 의 식 (eq:logistic)과 부호까지 동일). | 서술형 “(eq:logistic)” → \eqref 전환 대상 |
| `ch1_sec07_broadening.tex:26` | T1 | (\S\ref{sec:width-w} 의 지위 구분$\cdot$Chapter 2 파생 C 각주와 같은 한정). |  |
| `ch1_sec07_broadening.tex:40` | W | \emph{① 유한율속 비대칭 꼬리(동역학 몫).} 첫째는 이 문건이 이미 모델로 담은 출처로, \emph{전류가 켜야} 생긴다 --- 유한 |  |
| `ch1_sec07_broadening.tex:65` | W | 무관 OCP(open circuit potential --- 본 문건의 OCV 와 같은 반쪽전지 준평형 전위, 문헌 표기 따름)를 |  |
| `ch1_sec07_broadening.tex:100` | W | $\approx0$($\eta$ 지배)에 묻는 것이 위 가정의 보수적 읽기이며, forward-only 처방에서 안전하다. \emph{단, 본 문건은 식~\eqref… |  |
| `ch1_sec10_sum.tex:18` | W | override 하는 것이 전제) --- 이 표가 있어 ``이 문건만으로 곡선 재현 코드를 짤 수 있다''. |  |
| `ch1_sec10_sum.tex:126` | W | ``이 문건만 보고 같은 곡선을 재현한다''는 선언을 한 점에서 실증한다. 설정은 초기 상태 그대로다: | 재현 선언 문구 — 동상 |
| `ch1_sec10_sum.tex:168` | OK-S8 | 대신 열(엔트로피 분해와 가역 발열)을 뽑고, 이 골격을 두 번째 전극 LCO 양극에 거는 일은 Chapter 2 가 맡는다. |  |
| `ch1_sec18_inputs.tex:8` | W | 피팅할지는 사용자가 데이터로 정한다(본 문건은 스코프를 정하지 않는다). |  |
| `ch1_sec18_inputs.tex:16` | W | \textbf{이 문건만으로 한 곡선 재현(6단계).} | 재현 선언 문구 — 동상 |
| `ch1_sec18_inputs.tex:35` | W | \caption{노드 $\leftrightarrow$ 식 매핑(전체 진행). 본 문건 절 순서 $=$ 이 노드 순서. | 캡션 |
| `ch1_sec18_inputs.tex:40` | W | 노드 & 물리식 & 본 문건 식 \\ |  |
| `ch1_sec18_inputs.tex:65` | OK-S8 | 여기까지가 본 장(흑연)의 결과 사슬이다 --- 표의 LCO 행(N$'$ 계열)은 Chapter 2 가 같은 forward 골격을 |  |
| `ch2_appA_traps.tex:9` | T2 | Chapter 1 부록의 부호 사슬 검산표와 같은 용도다. | “Chapter 1 부록”=같은 문서 앞 부록 |
| `ch2_appA_traps.tex:67` | OK-S8 | LCO 장(Chapter 2)의 동명 식 \code{eq:Se}(별개 장 객체)와 이름 혼동 & |  |
| `ch2_appB_codemap.tex:7` | W | ★\textbf{doc-leads.} 이 문건이 권위이며, 코드(\code{Anode\_Fit})는 이후 이 문건에 맞춰 개정된다. 따라서 이 | doc-leads 선언 — “본서” 권고 |
| `ch2_appB_codemap.tex:13` | T2 | $\{\Delta S^0_j,\,Q_j,\,U_j,\,w_j\}$ 와 Chapter 1 의 $\xi_j(V,T)$~\eqref{eq:logistic} 를 받아, 전하 보존 |  |
| `ch2_appB_codemap.tex:25` | T2 | 단조를 만든다는 증명은 Chapter 1 Part 0 의 다클래스 소절(그 문건 식 (eq:sm-mc-balance))이 상술한다. | 서술형 “(eq:sm-mc-balance)” → \eqref 전환 대상 |
| `ch2_appB_codemap.tex:27` | T2 | \textbf{B.2 회귀 기준값.} 아래 값을 구현이 재현해야 한다(298.15 K, Chapter 1 4-전이 staging, $w_j{=}RT/F$). |  |
| `ch2_sec00_intro.tex:7` | T2 | Chapter 1 은 흑연 음극의 한 $\dd Q/\dd V$ 곡선을, 전이별 평형 중심 전위 |  |
| `ch2_sec00_intro.tex:8` | T2 | $U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F$(Chapter 1 §3 의 평형 중심 전위) 위에 세운 평형 종과 그 위에 |  |
| `ch2_sec00_intro.tex:33` | T2 | 분배함수 $Z$ 이고(\S\ref{sec:partition}), 거기서 점유 분포 $\avg{n}$ 을 얻는데 이것이 바로 Chapter 1 |  |
| `ch2_sec00_intro.tex:62` | T3 | ($\mathrm{LiCoO_2}$)의 전자 엔트로피 항은 분포 언어의 한 사례로만 포함한다(그 상세 전개는 Chapter 1 §15). |  |
| `ch2_sec01_partition.tex:10` | T2 | 문제다. 이 절은 그 분배함수를 세우고, 거기서 점유 분포 $\avg{n}$ 을 끌어낸 뒤, 그것이 Chapter 1 이 \emph{이미 |  |
| `ch2_sec01_partition.tex:13` | T2 | 의미)은 Chapter 1 §2(Part 0, 통계역학 기초)가 처음부터 자세히 세웠다 --- 여기서는 발열 논의에 필요한 최소 |  |
| `ch2_sec01_partition.tex:39` | T2 | 기호와 엄밀성에 관한 두 가지를 밝혀 둔다. 첫째, $\Xi_1$ 은 자리 1개의 \emph{대정준} 분배함수이며 Chapter 1 §2 |  |
| `ch2_sec01_partition.tex:42` | T2 | Chapter 1 §2 Part 0 의 유효 자리 자유에너지 유도가 닫았다 --- 그 결과는 $\varepsilon_0$ 을 유효 자리 자유에너지 |  |
| `ch2_sec01_partition.tex:47` | T2 | 몫의 단일 자리 원형이다(Chapter 1 §2 Part 0 의 같은 자리당 엔트로피). 온도가 오르면 이 엔트로피가 커지는 방향 |  |
| `ch2_sec01_partition.tex:51` | T2 | \subsection{전기화학 퍼텐셜과 Chapter 1 logistic 의 기원}\label{ssec:logistic} | 소절 제목 |
| `ch2_sec01_partition.tex:58` | T2 | Chapter 1 의 \emph{유도 전용 고정 부호}다.\footnote{★부호 각주(오독방지). 이 $s{=}+1$ 은 방향 부호 |  |
| `ch2_sec01_partition.tex:59` | T2 | $\sigma_d$(Chapter 1 §1 --- 분극$\cdot$분기$\cdot$꼬리 세 작용처 전용, $\pm1$)와는 \emph{별개}다. 평형 관계에는 |  |
| `ch2_sec01_partition.tex:77` | T2 | 진행률} $\xi=1-\theta$ 는 $V$ 에 증가하는 logistic이며, 후자가 정확히 Chapter 1 §5 의 전이별 \emph{logistic |  |
| `ch2_sec01_partition.tex:81` | T2 | Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화 |  |
| `ch2_sec01_partition.tex:113` | T2 | 이고, 우변 둘째 항이 \emph{혼합(섞임) 엔트로피}(곧 \S\ref{sec:config}; Chapter 1 §2 Part 0 의 섞임 엔트로피와 |  |
| `ch2_sec01_partition.tex:133` | T2 | $\Omega=2RT$ 는 Chapter 1 §4(히스테리시스)의 spinodal 조건과 같은 열역학이며, |  |
| `ch2_sec02_config.tex:6` | T2 | 앞 절은 점유 분포 $\avg{n}=\theta$ 를 세우고 그 여집합 $\xi=1-\theta$ 가 Chapter 1 의 평형 종임을 보였다. 이제 |  |
| `ch2_sec02_config.tex:50` | T2 | (후술 \S\ref{ssec:overlap} 식~\eqref{eq:dxidT}). 곧 \textbf{Chapter 1 의 logistic 폭 $w=RT/F$ 가 이미… |  |
| `ch2_sec02_config.tex:101` | T2 | \caption{(a) 단일 자리 점유 분포 $\langle n\rangle$~\eqref{eq:occ} --- Fermi--Dirac 와 동형이며 Chapter 1 | 캡션 |
| `ch2_sec02_config.tex:128` | T3 | Chapter 1 §14 의 반응 엔트로피 삼분해$\cdot$슬롯 규칙과, \emph{중심 표준값과 봉우리 내부 config 분포를 별개 |  |
| `ch2_sec02_config.tex:134` | T2 | \subsection{문헌 검증 --- Chapter 1 staging 엔트로피와의 정합}\label{ssec:litverif} |  |
| `ch2_sec02_config.tex:143` | T2 | 표~\ref{tab:ds} 는 Chapter 1 의 전이별 중심 표준값 $\Delta S^0_j=+29\to0\to-5\to-16$ J\,mol$^{-1}$K$^{-… |  |
| `ch2_sec02_config.tex:168` | T2 | {\footnotesize $\dagger$ Chapter 1 의 4 주요 plateau 전이와 Allart 등 \cite{allart2018} 의 세분 region… |  |
| `ch2_sec02_config.tex:175` | T2 | 엔탈피 쪽 표준값 $\Delta H^0_j$ 는 \emph{기준 차이}에 주의해야 한다: Chapter 1 의 $\Delta H_{\rxn,j}$ 는 |  |
| `ch2_sec03_vibel.tex:9` | T2 | 스핀--통계 --- 의 양자 배경은 Chapter 1 §2 의 배경 박스(페르미온$\cdot$보손과 양자 통계)가 한자리에 정리했다. |  |
| `ch2_sec03_vibel.tex:40` | T2 | \S\ref{ssec:elec}) 신호에 소량 섞일 수 있다(Chapter 1 의 대응 한정과 동급). 이 잔여를 명시적으로 닫아 |  |
| `ch2_sec03_vibel.tex:65` | T3 | 유도의 전 단계 --- 정보 엔트로피 합에서 비열을 거쳐 $S_e$ 까지 --- 는 Chapter 1 §15(LCO 전자 엔트로피)의 전자 |  |
| `ch2_sec03_vibel.tex:68` | T2 | $N_A\kB=R$ 로 환산해 넣는다(Chapter 1 의 단위 환산). 부분몰 전자 엔트로피 $\Delta S_e=\partial S_e/\partial x$ |  |
| `ch2_sec03_vibel.tex:69` | T2 | 는 삽입이 $g(E_F)$ 와 $E_F$ 를 바꾸는 방식에 달려 있다. Chapter 1 의 규약대로, 삽입(리튬화)은 일반적으로 |  |
| `ch2_sec03_vibel.tex:77` | T3 | Chapter 1 §13$\cdot$§15 가 상술한다. |  |
| `ch2_sec03_vibel.tex:82` | T2 | 세 분포가 한 전극의 엔트로피를 이룬다: Li 배열(Chapter 1 의 ``배치'')의 \emph{격자기체}(config), 격자 진동의 |  |
| `ch2_sec03_vibel.tex:90` | T2 | $\Delta S(x)$ 뿐이다. 이는 Chapter 1 §8$\cdot$§9 동역학 꼬리의 \emph{활성화 엔트로피} $\Delta S_{a,j}$(Eyring |  |
| `ch2_sec04_einstein.tex:21` | T2 | Chapter 1 \S4 spinodal 근의 $u_j=\sqrt{1-2RT/\Omega_j}$ 와도 동명 별개의 절-국소 기호다 --- 본 장 |  |
| `ch2_sec05_mixing.tex:23` | T2 | Chapter 1 Part 0 의 다클래스 소절(그 문건 식 (eq:sm-mc-balance))이 닫는다. 양변을 고정 $\bar x$ 에서 $T$ 로 음함수 미분하면 | 서술형 “(eq:sm-mc-balance)” → \eqref 전환 대상 |
| `ch2_sec05_mixing.tex:37` | T2 | $dQ/dV$ 봉우리(Chapter 1 의 peak) 모양}이다: |  |
| `ch2_sec05_mixing.tex:42` | T2 | ★기호 주의 --- 이 $g_j(x)$ 는 봉우리 가중[1/V]으로, Chapter 1 §2 의 조성 자유에너지 $g_j(\xi)$$\cdot$본 장의 |  |
| `ch2_sec05_mixing.tex:68` | W | 데이터가 정한다(본 문건은 스코프를 정하지 않는다). |  |
| `ch2_sec05_mixing.tex:91` | T2 | ★\textbf{수치 검증(파생 A).} Chapter 1 의 4-전이 흑연 staging 파라미터로, 유한차분(finite difference) |  |
| `ch2_sec05_mixing.tex:169` | T2 | 속함)}:\footnote{어느 전이를 두-상으로 특정하는지는 $\Omega>2RT$ 문턱 자체가 가르지 않는다 --- Chapter 1 의 |  |
| `ch2_sec05_mixing.tex:172` | T2 | \cite{dahn1991,ohzuku1993}(Chapter 1 의 staging 초기값$\cdot$post-fit 기준). 문턱은 ``상분리가 가능한가''를, 문… |  |
| `ch2_sec05_mixing.tex:180` | T2 | 출처의 분해$\cdot$앙상블 forward 통계평균$\cdot$역산 금지$\cdot$입자 크기 효과 배제)는 Chapter 1 §7 의 |  |
| `ch2_sec05_mixing.tex:183` | T2 | 따라서 Chapter 2 종합식(\S\ref{sec:synthesis})에 들어가는 $w_j$ 는, 흑연 두-상 전이에 대해 평형 예측 | 자기 구지칭(“Chapter 2 종합식”=본 파트) |
| `ch2_sec05_mixing.tex:199` | T2 | 는 탈리튬화 부호(Chapter 1 §4 의 분기 중심식에서 $\gamma_jh_{\eta,j}{=}1$ 로 둔 특수형)라 흑연 라벨에서 \emph{dis 가 |  |
| `ch2_sec07_revheat.tex:21` | T2 | 이다($I>0$ 방전, $V$ 단자 전압, $U_\oc$ 평형 전위). 첫 항은 과전압 소산(2법칙상 항상 발열, Chapter 1 의 |  |
| `ch2_sec07_revheat.tex:29` | T2 | $V<U_\oc$, $\dot Q_\irr\ge0$ 이 강제), 곧 흑연 하프셀에선 작동전극의 \emph{리튬화}다. Chapter 1 의 방향 |  |
| `ch2_sec08_synthesis.tex:23` | T2 | $\{\Delta S^0_j,\,Q_j,\,U_j,\,w_j\}$ 와 Chapter 1 의 $\xi_j(V,T)$(본 장 식~\eqref{eq:logistic} --… |  |
| `ch2_sec08_synthesis.tex:38` | T2 | $U_\oc$ 를 $\xi_j(V,T)$ 에 되먹인다. $\Delta S^0_j$ 는 다온도 $dQ/dV$ 동시 피팅으로 얻고 나머지는 Chapter 1 |  |
| `ch2_sec08_synthesis.tex:42` | T2 | 종합식이 실제로 한 수를 내는 과정을 Chapter 1 의 4-전이 staging 파라미터(중심 $U_j$$\cdot$용량 $Q_j$$\cdot$중심 |  |
| `ch2_sec08_synthesis.tex:47` | T2 | 여기서 중심 $U_j$ 는 Chapter 1 §3 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F$ 로 평가한 |  |
| `ch2_sec08_synthesis.tex:114` | T2 | \caption{탈리튬화 진행에 따른 가역 발열의 부호 교대(완전식, 298.15 K; Chapter 1 4-전이 staging, $w_j{=}RT/F$). | 캡션 |
| `ch2_sec09_method.tex:16` | T2 | \item 측정 전위에서 분극을 먼저 분리한다 --- Chapter 1 §1 의 $V_n=V_\mathrm{app}-\sigma_d\|I\|R_n$ 로 |  |
| `ch2_sec09_method.tex:18` | T2 | \item 같은 $Q_j$ 구조를 공유하되 각 온도의 중심 $U_j(T_k)$ 와 폭 $w_j(T_k)$ 를 허용해 Chapter 1 의 logistic |  |
| `ch2_sec09_method.tex:20` | T3 | (Multi-Species, Multi-Reaction) 절차(Chapter 1 §17)와 직접 대응한다 \cite{msmr_partI,msmr_partII}. |  |
| `ch2_sec10_closing.tex:8` | T2 | $\avg{n}$ 을 끌어내 그것이 Chapter 1 logistic 의 기원임을 보였고($w=RT/F$ 가 분포 폭), 점유 분포에서 |  |
| `ch2_sec10_closing.tex:13` | T2 | 이중지위(파생 C --- 단상은 평형 예측, 흑연 두-상은 현상학적 자유 피팅 폭, broadening 기원은 Chapter 1 §7)로 |  |

## 전수 표 — 신 Chapter 2 (LCO) — 14건

| 파일:행 | 분류 | 발췌 | 비고 |
|---|---|---|---|
| `ch1_sec11_lcointro.tex:27` | W | 두 번째 전극으로 들어온다. 본 문건이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 --- 전셀 합성 |  |
| `ch1_sec11_lcointro.tex:37` | W | 흑연에서 $\xi_j$ 가 탈리튬화 진행이었듯, LCO 양극에서 충전(탈리튬화)이 $\xi:0\!\to\!1$ 의 주 진행 방향이다 --- 본 문건의 |  |
| `ch1_sec11_lcointro.tex:45` | W | 등급 표기(본 문건 전역): tier A $=$ 1차 문헌의 정량 확정값, tier B $=$ 대표/부분 스케일 anchor 또는 |  |
| `ch1_sec12_lcocenter.tex:93` | W | \textbf{★단전극 대 전셀 혼동 금지} --- 이 $+0.83$ mV/K 는 \emph{LCO 단일전극}(vs Li) 값이고 본 문건(하프셀 |  |
| `ch1_sec14_lcodecomp.tex:57` | OK-S8 | 파트(Chapter 1 Part T)가 같은 기호 $\Delta S^0_j$ 로 부르는 것은 그 \emph{전이 전체 상수}(성분 미분해) |  |
| `ch1_sec14_lcodecomp.tex:90` | W | 본 문건이 추적하는 1차 문헌 공백은 셋이다(G$n$ 은 그 일련번호): G1 $=$ 연속 $\Delta S(x)$, G2 $=$ 연속 $g(E_F,x)$ |  |
| `ch1_sec15_lcoelec.tex:37` | W | 자리마다 하나씩 국소화되어 절연한다(여기의 $U$ 와 $t$ 는 본 문건의 전극 전위 $U_j$ 와 별개인 상관 물리의 |  |
| `ch1_sec15_lcoelec.tex:125` | W | MIT 를 가로지르는 \emph{연속 곡선} $g(E_F,x)$ 는 1차 문헌에 \emph{부재}하여(갭 G2 --- 본 문건이 추적하는 |  |
| `ch1_sec15_lcoelec.tex:164` | W | 탈리튬화($x\!\downarrow$, 본 문건 LCO 충전 주 진행) 시 전자 엔트로피가 방출되며, 그 방출량은 게이트가 스스로 |  |
| `ch1_sec15_lcoelec.tex:319` | L1 | Chapter 2 의 완전식과 같은 구조)으로 $\partial U_\mathrm{oc}/\partial T$ 를 평가하면: | S-008 ⑤ 동종 — 완전식 지칭, xr 전환 |
| `ch1_sec17_msmr.tex:19` | W | $f=F/RT$(항상 양)$\cdot$무차원 폭 $\omega_j$ 를 본 문건은 $F/RT$ 를 폭에 흡수($\omega_j\mapsto\omega_jRT/F$, |  |
| `ch2v22_notation.tex:6` | OK-NEW | 본 장의 기호는 두 단으로 관리한다. \textbf{계승}(Chapter 1 정의 그대로 --- 재정의 없음): |  |
| `ch2v22_sec00_intro.tex:4` | OK-NEW | 본 장은 Chapter 1 이 흑연에서 세운 골격을 두 번째 활물질 LCO(Li$_x$CoO$_2$ 양극)에 건다. 서술 |  |
| `ch2v22_sec00_intro.tex:6` | OK-NEW | 추가되는 텀만 적는다.} 곡선 골격(전하 보존 반전$\cdot$평형 종$\cdot$히스테리시스$\cdot$폭)은 Chapter 1 |  |

## 전수 표 — 신 Chapter 3 (Si·혼합) — 2건

| 파일:행 | 분류 | 발췌 | 비고 |
|---|---|---|---|
| `ch3v22_sec00_intro.tex:6` | OK-NEW | Chapter 1 골격의 노드별 생존 지도를 놓고(무엇이 그대로 살고, 무엇이 재해석되고, 무엇이 골격 밖 새 |  |
| `ch3v22_notation.tex:5` | OK-NEW | \textbf{계승}(Chapter 1$\cdot$2 정의 그대로 --- 재정의 없음): 전하 보존 반전~\eqref{eq:sm-mc-balance} |  |

