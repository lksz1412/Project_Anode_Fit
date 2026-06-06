# 작업 계획서(개정) — Chapter 1: 흑연 음극 dQ/dV 피크의 물리 도출 (밀도·$V_n$·$\xi_j$ 보강)

**Date**: 2026-06-03 · **Author**: Claude · **상태**: 작업 계획(설계도). **GO 대기 — 본 turn 에 tex 작성 X.**
**트랙**: 완전 새 트랙. 기존 RB 인프라·문건 미계승(rebuilt 는 `docs/Archive_rebuilt/`, 구track results/work 는 `*/Archive_oldtrack/` 로 정리 완료). \*rebuilt 는 \emph{밀도·설계 참조용}\*(내용 옮겨심기 X, 메인=현재 버전).
**개정 근거**: 현재 `graphite_ica_ch1.tex` 줄별 감사(비약 9·근거부족 7·과단축 8·$\xi_j$ 누락 9·컨벤션 4) + rebuilt 이론부 밀도 비교(개념=절 입도·좌표변환 3단계·$V_n$ 전하보존) + 사용자 지적 3건.

---

## §0. 절대 기준 — 사용자 요청·관측 (verbatim; 변경 없음)

(이전 판 §0 유지) **관측** = dQ/dV 상전이 피크의 \*위치·너비·높이\*가 \*온도·C-rate·극판 전위\* 3인자에 반응(저온→긴 꼬리, 전위→배리어 낮춤). **요청** = 유효 배리어 논리 + \*실무 피팅 근사식 첫째\*, 논문/특허급 둘째, \*학부 무비약·생략 없음\*(P4), solver 코드 X(P1), step-function 금지·activation barrier 유지, 모든 가정·변환은 \*교과서/논문 근거 있을 때만\*, 한글 prose+영어 용어. **범위** = Ch1 단독·최대한 심플(열역학 무대 + 전위 배리어 낮춤). "5단계"=챕터 arc(절 규약 아님).

---

## §0bis. 이번 개정의 진단 (사용자 지적 + 비교 분석)

**사용자 평가**: "전체 구성은 현재 버전이 rebuilt보다 낫다. \*그러나 디테일과 과정이 심각하게 부족\*하고 비약이 심하다(변수 동기 설명은 개선됨)." → \*구조 유지 + 밀도·과정 대폭 보강\*이 본 개정의 핵심.

**rebuilt 가 치밀했던 본질(밀도 패턴 — 캐치해 올 것)**:
1. **개념 1개 = 절 1개 입도.** 한 물리 개념마다 전용 절, 그 안에서 다시 단계 라벨((i)(ii)(iii)·단계1/2/3).
2. **좌표변환을 본문 3단계로 명시**(예: 배리어→길이 = 자코비안 밀도보존 → 지지범위 → 용량가중). 현재는 rigorbox 로 "줄기 밖" 격리 → \*본문 단계로 승격\*.
3. **검산(verifybox)·무결성 극한 복귀를 빈번히** 배치.
4. **매 식 전 물리 동기 문단**(이건 현재가 이미 계승 — 유지).

**현재 버전의 ★필수 물리 누락(import)**: 아래 §2 표.

## Summary

현재 `graphite_ica_ch1.tex` 의 \*우수한 구조(L1~L6 동기 우선)\*는 보존하되, (1) **유도 밀도를 rebuilt 수준으로 대폭 상향**(모든 대수 단계 명시·좌표변환 본문 승격·검산 빈도↑), (2) **★필수 물리 $V_n$ 전하보존 무대 import**(+$Q_\bg/C_\bg$, 다중 전이 $N_p$), (3) **진행률에 전이 인덱스 $\xi\to\xi_j$ 전면 적용**, (4) **서두 \emph{Notation \& Conventions} 절 신설**(리뷰·시뮬 논문 관행), (5) 논리순서 역전(detailed balance)·$s_I$ 미정의 등 횡단 결함 수정. 자기참조 Volterra·closure·$k_\lim$ 은 \*과축조·비약 주범이자 부록/Ch1 심플 경계 밖\*이라 \*스킵\*. 결과 = 같은 식이라도 \*과정이 보이는\* 학부 무비약 본문 + 실무 근사식.

## Current Ground Truth

- **현재 버전 강점(보존)**: 동기 우선(공식 앞 물리 말)·절 전이 bridge·반증/비유일성/경쟁원 분리·grounding 16 DOI 검증·step-function 0. 사용자 "구조 우수" 확인.
- **현재 버전 약점(개정 대상)**: 밀도 절반 이하(개념 압축)·$V_n$ 무대 누락·$\xi_j$ 누락·서두 컨벤션 절 없음·핵심 유도 5곳 압축(아래 §3 fix-list)·detailed balance 논리 역전.
- **rebuilt(참고)**: `docs/Archive_rebuilt/graphite_ica_ch1_rebuilt.tex` 이론부 — 밀도·$V_n$·좌표변환 패턴만 캐치(내용 미계승).

## §1. 개정 구조 — 도출 논리 (L0 신설 + $V_n$ 무대 + $\xi_j$; 절은 도출서 도출)

> 도구(열역학·동역학·전기화학·통계)는 절 기준이 아니라 각 단계 inline. \*개념 1개=절 1개\* 입도로 밀도 확보. 모든 진행률은 $\xi_j$.

| 단계 | 절(담당) | 핵심 — \*밀도 요구\* | import/신규 |
|---|---|---|---|
| **L0** | \textbf{Notation \& Conventions}(신설) | 기호·단위·\*부호 규약\*($s,s_I$)·$j$-인덱스 규약 표. 리뷰 논문식 서두 정리 | ★신설 |
| **L1** | 무대: 전하보존이 $V_n$ 을 정한다 | $Q_\cell q=Q_\bg(V_n,T)+\sum_j Q_j\xi_j$ → $V_n$=보존식 해(외부 lookup 아님), OCV=평형 특수해, $V_\app=V_n+s_I|I|R_n$. $C_\bg=\partial Q_\bg/\partial V_n>0$ 1줄 | ★import(필수) |
| **L2** | 평형 peak (전이 $j$) | $\xi_{\eq,j}(V_n)$ logistic \*무비약\*(평형조건 \emph{유도} 포함), 위치 $U_j(T)$·너비 $w_j$·높이 \*각각 개별 유도\*, ∂U_j/∂T | 밀도↑·$\xi_j$ |
| **L3** | 동역학 지연 | $\dd\xi_j/\dd t=k_j(\xi_{\eq,j}-\xi_j)$, Eyring, ODE \*해 명시\* → 꼬리, 시간→용량→전압 좌표변환 \*단계 분리\*, 저온/C-rate | 밀도↑·$\xi_j$ |
| **L4** | 유효 배리어(전위) | BV 방향성 $r_j^\pm$, detailed balance \*여기서 평형 재생\*(L3 전방참조 정리), $k_j\simeq r_j^+$ 근사 부등식 명시 | 밀도↑·논리순서 |
| **L5** | 입자 분포·중첩 | 입자→$\rho_G$→$L_{q,j}(G)$→중첩 적분 \*본문 4칸\*, 좌표변환 \*본문 승격\*(rigorbox→단계) | 밀도↑ |
| **L6** | 종합: 3×3 + 근사식 | 닫힌식($\ast$ \emph{정의 명시}), 3×3, 단일 집단 극한 \*sifting 명시\*, 식별 S1~S4 \*각 step 3요소·arrhenius 대수 유도\* | 밀도↑ |
| **L7** | 검증·반증 | falsification·경쟁원 분리(현재 충분 — 유지) | 유지 |

## §2. rebuilt import 판정 (메인=현재; 과도 import 경계)

| 물리 | 판정 | 처리 |
|---|---|---|
| 전하보존 $V_n$ 결정 | **★필수** | L1 신설(심플: 보존식+OCV 특수해+$V_\app$ 환산; well-posedness 는 1줄 권장) |
| 배경용량 $Q_\bg/C_\bg$ | 권장 | L1 에 $C_\bg=\partial Q_\bg/\partial V_n>0$ 정의 + L6 배경-꼬리 공선형 정량 |
| 다중 전이 $N_p$/staging 융합 | 권장 | L0/L1 에 $j=1..N_p$ 정의(peak 겹침=관측 핵심) |
| 물리병목 $k_\lim$ | 선택 | L4 각주 1줄(강구동 $\Delta G_\eff<0$ 가드 명분)만, 본문 X |
| effective 전자수 $n_j^\eff$ | 스킵 | Ch3·4 전달용, 단일장 경계 밖(ideal $w_j=RT/F$ 유지) |
| 자기참조 Volterra | **스킵** | 과축조·비약 주범; forward-prediction 경계서 불요(사용자 "구조 현재가 낫다"=단순화 긍정) |
| closure Plan A/B(g-grid) | **스킵** | 수치·피팅 실무 = 부록 분리 방침 |

## §3. ★ 밀도·디테일 보강 fix-list (현재 작업물 줄별 감사 → 실행 spec)

\*가장 압축 5곳(최우선)\*:
1. **eq:logistic 평형조건 유도(전 문서 최대 비약)**: 전극 Li 삽입 $\mathrm{Li}^++e^-+\square\to\mathrm{Li}$ 전기화학 평형 → $\mu(\xi_j)=sF(V_n-U_j^0)$ 가 \emph{왜}(전자 일 $-FV$, 부호 $s$). 그 뒤 $U_j$ 흡수·$w_j$ 정의·지수풀이 $\xi/(1-\xi)=E$→$\xi_{\eq,j}=E/(1+E)$ \*각 줄 분리\*.
2. **eq:closed $\ast$ 정의**: 상승부(logistic)와 꼬리(분포중첩 지수)의 결합이 convolution 인지 정점 접합인지 \*수학적으로 정의\* → 학부생이 계산 가능하게. $\rho_G\to\delta$ 무결성 복귀 1~2줄.
3. **eq:smix→mu_mix**: $\ln W=N\ln N-n\ln n-(N-n)\ln(N-n)$ 전개 + $-N+n+(N-n)=0$ 명시 + $n=N\xi_j$ 대입(3줄). 자리당↔몰당 환산 인자 분리.
4. **식별 S1~S4 + arrhenius**: 각 S 에 "고정→분리→공선형 해소 근거" 3요소 문장. $y(T)$ 보정식을 $\ln L_{q,j}=\ln\frac{|I|h}{Q_\cell k_B}-\ln T+\frac{\Delta H_a-T\Delta S_a-\chi\mathcal A}{RT}$ 전개서 \*항 이동 2~3줄\* 로 유도.
5. **eq:tail ODE 해**: $\dd r_j/\dd q=-r_j/L_{q,j}$ 의 해 $r_j=r_j(q_a)e^{-(q-q_a)/L_{q,j}}$ \*명시\* → $\dd\xi_j/\dd q$ 도출 → $V$ 선형 가정으로 $q\to V$ 변수변환 1~2줄.

\*추가 보강(중)\*: eq:dxidV logistic 미분 항등식 2줄 유도 · eq:mu_int 정규용액 평균장 1줄+cite · ∂U/∂T Gibbs–Helmholtz 2줄 · FWHM 이차방정식 풀이 1줄 · eq:bv $\chi$=전이상태 위치 1~2줄 · eq:keff $k_j\simeq r_j^+$ 부등식 1줄 · superpose 신호 선형성 1줄 · arrhenius 분산전파 1줄.

\*$\xi_j$ 누락 9곳 전수 교정\* + L0 에 "$\xi_j,\xi_{\eq,j},k_j,r_j,L_{q,j}$; 단일전이 문맥만 $j$ 생략" 규약.

\*횡단 결함\*: (a) detailed balance 논리 역전 — L3 에서 $\xi_{ss}=\xi_{\eq,j}$ 쓸 때 "L4 BV 에서 $r^+/r^-=e^{\mathcal A/RT}$ 로 검증" 전방참조 명시. (b) $s_I$(전류 부호) L0 정의.

## Phase Range

| Phase | 이름 | Step | result |
|---|---|---|---|
| **NT.0** | 보강 구조·밀도 spec·게이트 동결 | 1–3 | (본 계획) |
| **NT.1** | L0 Notation 절 + L1 $V_n$ 무대 작성 | 4–7 | tex + result |
| **NT.2** | L2 평형 peak(밀도 보강·$\xi_j$) | 8–11 | tex + result |
| **NT.3** | L3 지연 + L4 유효배리어(밀도·논리순서) | 12–16 | tex + result |
| **NT.4** | L5 분포(좌표변환 본문 승격) + L6 종합($\ast$·S 보강) | 17–21 | tex + result |
| **NT.5** | L7 검증 + 밀도·$\xi_j$·무비약 적대검증 + 빌드 + Decision Gate | 22–26 | 검증 result |

## Non-goals

자기참조 Volterra·closure·수치 solver(부록/Ch3 경계). $n_j^\eff$·강구동 일반화. rebuilt 내용 옮겨심기(밀도 패턴만 캐치). Workflow 등 권한팝업 도구(Agent only). Ch2~5.

## Test Plan (게이트 — verifiable)
- **G-density(★ 신규)**: 가장 압축 5곳 + 추가 보강이 \*각 대수 단계 명시\*로 풀림. 독립 agent 가 "이 식에서 다음 식으로 가는 중간 단계가 본문에 다 있나" Y/N → 전원 Y.
- **G-jindex(신규)**: 모든 진행률·전이별 양에 $j$ 일관($\xi_j,\xi_{\eq,j},k_j,r_j,L_{q,j}$); 무첨자 잔존 0(단일전이 문맥 규약 예외).
- **G-notation(신규)**: 서두 Notation 절에 §3 기호 목록·단위·부호($s,s_I$)·$j$ 규약 전부 등재.
- **G-Vn(신규)**: $V_n$ 이 전하보존식 해로 \*도출\*됨(출처 있음), $V_n/V_\app/V_\drive/V_\OCV$ 구분 일관.
- **G-noleap·G-undergrad·G-usable·G-3x3·G-nostep·G-ground·G-noTransplant·G-spine·G-latex**: 이전 판 유지(특히 G-noTransplant 는 archive rebuilt 와 식·문장 diff 0).

## Assumptions
- A1: 구조는 현재 버전 유지(사용자 확인), 밀도·$V_n$·$\xi_j$·Notation 만 보강.
- A2: $V_n$ import 는 \*심플 수준\*(보존식+OCV+$V_\app$); 자기참조 closure 는 스킵(경계).
- A3: 모든 가정·변환은 교과서/논문 근거 동반(사용자 명시). rebuilt 는 밀도 참조, 내용·식 표현 미계승(diff 0).

## Decisions Required (평문, 무응답 시 권고값)
- **D-Vn 범위**: $V_n$ 무대를 \*심플\*(보존식 해+OCV 특수해+$V_\app$ 환산)로 import, 자기참조 closure 스킵. 권고: 그대로. \*전하보존 well-posedness 까지 원하면 1줄 추가\*.
- **D-밀도 목표**: rebuilt 수준 밀도(개념=절, 좌표변환 본문 단계). 권고: 그대로. 분량은 현재 ~340줄 → ~600줄+ 예상(밀도 보강분).
- **D-구조**: L0~L7(L1 $V_n$ 무대 신설). 권고: 그대로.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-03 (NT v1/v2) | 물리 중심 전환·BV detailed balance·Marcus 유추 강등 등(이전 판). |
| 2026-06-03 (NT v3, 본판) | 사용자 "디테일·과정 심각 부족" + rebuilt 밀도 비교 + 줄별 감사 반영: **밀도 대폭 상향(fix-list 5+9)·$V_n$ 전하보존 무대 import·$\xi_j$ 전면·Notation 절 신설·detailed balance 논리순서·$s_I$ 정의**. 자기참조 Volterra·closure·$k_\lim$ 은 과축조 경계로 \*스킵\*(메인=현재 구조, rebuilt=밀도 참조). |
