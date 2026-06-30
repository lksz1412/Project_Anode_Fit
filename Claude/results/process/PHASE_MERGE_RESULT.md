# PHASE_MERGE Result — Ch1+Ch2 병합 + 6창 적대검수 + 3-Pass 수정

대상: `Claude/docs/graphite_ica_merged.tex` (병합 단일 챕터, 29p, build 0/0). Branch `rb-rebuild-2026-05-30`.
방식: 절 단위 통합 작성 → **멀티에이전트 청킹 6창 적대검수(3렌즈: 정확성·G-follow·G-usable, refute, 빈통과 0)** → master 직접 3-Pass 수정(발견→수정→재검증).

## 1. 작성(병합)
- 서론 병합 arc 재작성 / §정규용액·상분리(Ω≠0, g''·T_c·spinodal, vdW 도구, Dreyer; lever rule CUT·CNT 정성 TRIM) / §충방전 분기(V_eq·spinodal·ΔU_hys·γ) / §분기별 dQ/dV / §동역학 분극(gap 분리) / §부분 cycle(return-point+h_j) / **통합 master eq:hys_master**(방전+충방전 한 식, 환원검산 2) / §기호 히스 행 / §검증 히스 반증.

## 2. 6창 적대검수 (Agent 도구, 팝업 0) — 빈 통과 0, 실효 적발
| 창 | 범위 | 핵심 결과 |
|---|---|---|
| 1 | 서론·기호·전하보존 | R_{n,j}/R_n 누락 적발·V_{n,OCV} orphan·전하보존 서술-수식 괴리 |
| 2 | 평형peak·정규용액 | **부호 사슬(eq:mu↔eq:eqcond↔eq:logistic)·g''·T_c·spinodal·FWHM 전수 손검 일치, 확정오류 0**. vdW μ=dg/dξ 부호 이중정의(G-follow) |
| 3 | 동역학·유효배리어 | 11식 검산 통과(확정오류 0). λ orphan·k_j=r⁺+r⁻ vs r⁺ 인자2 bridge·r_a 정의 위치 |
| 4 | 통계·분포·종합·겹침 | **E1 eq:superpose r_a(G) vs 용량보존 포화전제·E2 r_{a,j}≤1 조건부·worked example orphan(overlap이 같은 91mV 독립 재계산)** |
| 5 | 충방전 분기·PART B | ΔU_hys·spinodal·임계극한·54mV 독립 재검산 일치. **R_{n,j}/R_n 확정·h_j 완전 orphan** |
| 6 | 통합 master·검증 | (a)방전 재현·(b)분극소멸·(e)(T_c−T)^{3/2} 검산 성립. **R_n/R_{n,j} 확정·s_I/σ_d 혼용·h_j orphan·허수 u 절단 절내 부재·walkthrough S5 누락** |

## 3. 3-Pass 수정 (master 직접) + 재검증
| # | 결함(확정/핵심) | 수정 | 검증 |
|---|---|---|---|
| 1 | **R_{n,j}(PART B) vs R_n(표·vapp·master) 불일치** (3창 독립) | 공통 R_n 으로 통일(eq:vapp 규약·피팅 파라미터 최소). "전이별 1개"→"공통, SOC 의존 크면 R_{n,j} 확장" | grep R_{n,j}=1(확장언급만) |
| 2 | **h_j(부분cycle) 완전 orphan**(master 미사용) | eq:hys_master 중심을 U_j+σ_d½**h_j(η)**γΔU 로 일반화(완전 cycle h_j=1)·도입절 전달문구와 닫힘 | h_j master서 사용 |
| 3 | s_I vs σ_d 부호기호 혼용 | σ_d 도입에 "s_I 양방향 일반화(s_I=σ_d)" 명시 | build |
| 4 | worked example(91mV) orphan·overlap 중복재계산 | synth example→S1 sanity+overlap 입력 forward / overlap→synth 값 인용 back | 도입→사용 닫힘 |
| 5 | vdW μ=dg/dξ vs μ_Li(θ) 부호 이중정의 | "dg/dξ=−(μ_Li−μ⁰), 변수만 다름" 명시 | build |
| 6 | 허수 u 절단 근거 master 절내 부재 | 환원검산①에 "u 허수⇔spinodal 부재⇔ΔU≡0(regsol verifybox)" | build |
| 7 | walkthrough S5(충방전 gap) 누락 | enumerate에 S5 단계(gap 외삽→γ/Ω)·예측 양방향 추가 | build |
| 8 | r_{a,j}≤1 무조건(E2) | (0,ξ_eq(q_a)] 포화창 조건 명시 | build |
- E1(eq:superpose 포화)·table r_a 조건은 기존 본문에 "포화 근사" 명시 확인(추가 불요).
- **재검증**: xelatex 2-pass, 29p, overfull 0, undefined 0.

## 4. 잔여(경미, 차후) — 4-tier: 미검증/추정 아님, 명시 defer
- λ(Marcus) 정성 인용 전용 명시 / V_{n,OCV} 사용처 / k_j 인자2 bridge 1줄 / 전하보존 비평형 V_n=Q_bg^{-1} 서술 보강 / S5 γ·Ω 분리 다온도 의존 표기. 모두 결론 무영향(의존성·기울기 보존), 정합 1줄 보강감.

## 5. 승격 완료(M19) + genuine 심화
- merged → **graphite_ica_ch1.tex 승격**, 구 ch2→old/, Ch3/Ch4 인계 식번호 라벨기준 재매핑(전부 0/0). merged.tex 제거(ch1 이 정식).
- **심화 1 — 유효 폭 $w_j^\eff=(RT/F)(1-\Omega_j/2RT)$ (식 eq:weff, 패딩 아님·전부 사용)**: 평형조건 $V_n$ 미분서 손유도. (a) staging peak 가 이상 $RT/F$ 보다 날카로운 까닭, (b) $w_j$ 에 물리근거·\emph{온도의존}($w_j(T)=(RT-\Omega/2)/F$, 한 온도 $w_j\to\Omega_j\to$ 타 온도 예측), (c) 폭의 $\Omega_j$ = gap 의 $\Omega_j$ \emph{과결정 교차검증}(§검증). §정규용액 도입→§master $w_j$ 행 근거→§검증 일치, 완전 통합.
- **심화 2 — DVA($\dd V/\dd Q$) 절(sec:dva)**: 프로젝트 목표(ICA·DVA) 정합. peak↔valley 대응(DVA peak=stage 경계, ICA peak=plateau), 왜 둘 다(경계 강건성·용량 직접성·교차검증·노화 LLI/LAM), 같은 $\{w_j,\Omega_j,\gamma_j,R_n\}$ — 새 물리 아님, 같은 모델 두 그림. eq:weff·eq:Lq·sec:hys_branch 인용(통합).
- ch1 **30p** 0/0. 심화로 식번호 재차 이동 → Ch3(1.20/1.21/1.23/1.48/1.49)·Ch4(1.20/1.27/1.28/1.29) 재매핑·재빌드 undef 0. 분량은 패딩 아닌 실질 결과.
