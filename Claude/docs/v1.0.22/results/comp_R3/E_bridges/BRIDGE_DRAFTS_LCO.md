# BRIDGE_DRAFTS_LCO — 인용 다리(LCO분) 초안 색인 (v1.0.22 R3 · O-E)

> 초안 전용. 각 다리 = `br_<키>.tex` 스니펫(본문 삽입용 LaTeX, `srcbox` 컨테이너 — 우리 기호 서술, 논문 량은 대응표에서만). 삽입은 마스터가 diff 1:1 로그로 집행.
> 3요소(마스터플랜 §7): ①변수 대응표 + 등치 중간식 1~3개 ②논문 방법 요지 한 문장 ③가정 차 한 문장 — 전건 완비.
> 컨테이너 = `srcbox`(R2 집행례 `comp_R2/B_bridges/br_bazant2013.tex` 양식 모범 승계). 신규 등치식 라벨 = `eq:br-<키>-<n>`(제안).
> 원문 검증 규칙: doi/arXiv 확인분만 수식 사용, 미확인 수식은 재현 금지·"★확인 필요" 표기.

## 다리 4건 색인

| # | 스니펫 | 키 | 삽입 파일:행(앵커) | 우리 식(라벨) | 논문 식/결과 | srcbox 행수 | 원문 검증 |
|---|---|---|---|---|---|---|---|
| 1 | `br_marianetti2004.tex` | marianetti2004 | ch1_sec15_lcoelec.tex : MIT bgbox(30–67) 직후, 69행 앞 | eq:ggate·eq:dSegate·eq:lco-mottcrit | 불순물-Mott 조성경계(결과) | 40 | 기작·경계 **확인** · 원 모델식 **★확인 필요** |
| 2 | `br_vanderven1998.tex` | vanderven1998 | ch1_sec13_lcohys.tex : §13.3 전개블록(115–123) 직후, 124행 앞 | eq:lco-gxi·eq:lco-spinodal | 제일원리 클러스터전개 상도표 | 39 | 방법·x=½ 질서 **확인** · ECI 식 **★확인 필요** |
| 3 | `br_msmr_lineage.tex` | msmr_origin2017 + bakerverbrugge2018 | ch1_sec17_msmr.tex : eq:msmr 재모수화(13–22) 직후, 23행 앞 | eq:msmr·eq:lco-msmrmap | 종별 점유식(형태·정의) | 39 | 식형태·파라미터 정의 **확인**(PyBaMM 대조) · 식번호만 경미 |
| 4 | `br_reynier2004.tex` | reynier2004 | ch1_sec14_lcodecomp.tex : 삼분해 박스+역할(62–87) 직후, 89행 앞 | eq:lco-decomp·eq:lco-Sadd | 실측 3기여 분해·ΔS=F dU/dT | 37 | 측정원리·분해·척도 **확인** · 0.18 kB 값 **★확인 필요** |

총 srcbox 155행(+ 헤더 주석). 삽입 위치 4곳 전건 파일:행·앵커 문장 명기.

## 다리별 3요소 요지(스니펫 상세는 각 .tex)

### 1. marianetti2004 → eq:ggate + eq:lco-mottcrit (§15)
- ① x_MIT≈0.85 ↔ 절연(x≳0.95)–금속(x≲0.75) 2상역 중앙 · Δx_MIT≈0.05 ↔ 유한 조성창 폭 · g(E_F,x):0→g_max ↔ DFT g(E_F) 절연→금속 · "왜 한꺼번에" ↔ 불순물 띠 임계농도 일괄 비국소화. 등치식 eq:br-marianetti2004-1: x_MIT∓2Δx_MIT≈0.75/0.95(게이트 양끝 = 금속/절연 경계).
- ② 대형 초격자 DFT 로 탈리튬화 정공이 host t2g 띠 대신 Li 빈자리 속박 불순물 준위를 이루고, 그 불순물 띠가 임계농도에서 일괄 비국소화(불순물 Mott)해 1차 MIT·2상 공존을 설명(x≳0.95 절연·x≲0.75 금속 재현).
- ③ 원 계산=상관·불순물 미시 / 본문=조성축 logistic 게이트 하나로 현상학화(발현 분산을 Δx_MIT 에 흡수). **eq:lco-mottcrit(U≳2zt)은 교과서 판별식(mott1968·imada1998)이지 Marianetti 정량식 아님 — 오귀속 금지.**
- ★확인 필요: 원 모델 Hamiltonian·정확한 판별식·식번호 미확인(구 Nature PDF 기계 판독 실패). 기작·조성경계는 WebSearch 초록(nmat1178) 확인 → 결과 수준 대응, 논문 식 재현 안 함.

### 2. vanderven1998 → eq:lco-gxi + eq:lco-spinodal (§13)
- ① 유효 인력 Ω_j^cat(평균장 쌍) ↔ 유효 클러스터 상호작용(ECI) 집합 · 볼록성 상실 Ω_j^cat>2RT ↔ 제일원리 2상 안정역 · x≈½ 질서상(T2/T3) ↔ 계산이 재현한 x=½ Li·빈자리 질서상 · 저농도 ↔ 저-x staging. 등치식 eq:br-vanderven1998-1: Ω_j^cat ξ(1−ξ) ↔ [ECI 최근접 쌍]_평균장, Ω_j^cat>2RT ⇔ x≈½ 질서상 안정.
- ② LixCoO2 형성에너지를 제일원리 클러스터 전개로 적고 상평형(자유에너지 최소)으로 풀어 x=½ 질서상·저-x staging 을 재현한 상도표 획득.
- ③ 원 계산=다체 ECI·명시적 질서 바닥상태 전부 / 본문=전이별 단일 평균장 Ω_j^cat 로 축약(정규용액 이중웰) — 미시 구조 아닌 유효 문턱만, 실제 gap 은 피팅된 Ω_j^cat 이 결정.
- ★확인 필요: 정확한 클러스터 전개 에너지식·ECI 값·식번호 미확인(구 APS PDF 기계 판독 실패). 방법·x=½ 질서·저-x staging 은 WebSearch 초록·ADS 확인 → 방법·결과 구조 수준 대응. **등치식은 우리 평균장 축약이지 원 논문 식 아님.**

### 3. msmr_origin2017 + bakerverbrugge2018 → eq:msmr + eq:lco-msmrmap (§17) — [형태 검증완료]
- ① x_j=X_j/(1+e^{f(U−U_j^0)/ω_j})(우리) ↔ 동일 종별 점유식(Verbrugge 2017) · f=F/RT ↔ f=F/RT · X_j ↔ 종별 host 자리 분율 · U_j^0 ↔ 농도무관 표준전위 · ω_j ↔ 무질서 파라미터 · Σ_j X_j θ_j ↔ x=Σ_j x_j · "MSMR" 명명 ↔ Baker–Verbrugge 2018. 등치식 eq:br-msmr-1: f(U−U_j^0)/ω_j →[F/RT 흡수, ω_j↦w_j=n_jRT/F]→ σ_d(V−U_j^d)/w_j, 계수비교 f=+σ_d.
- ② Verbrugge 등이 삽입 전극 OCV 를 치환 격자 열역학 종별 점유(자리 보존 Σ_j X_j)의 Nernst-형 합으로 닫아 eq:msmr 를 세우고, Baker–Verbrugge 가 다공전극 다반응 정식화로 확장하며 MSMR 명명.
- ③ 원계열=방향 없는 평형 등온선·무차원 폭 ω_j / 본문=F/RT 를 폭에 흡수(ω_j→w_j)·방향 부호 f=+σ_d 남김·히스 분기(γ_j)·전자항 추가(함수형 동형이지 물리량 동일 아님).
- 검증: eq:msmr 형태·f·X_j/U_j^0/ω_j 정의 = PyBaMM MSMR 구현 문서(Verbrugge 2017 재현·정의 명기) 대조 확인 → **형태·정의 확인분, 재현 가능**. 원 논문 내부 식번호만 직접 대조 미완(경미·다리 핵 아님).

### 4. reynier2004 → eq:lco-decomp + eq:lco-Sadd (§14) — [load-bearing 추가 후보 = YES]
- ① ∂U_j/∂T=ΔS_rxn,j/F(측정경로) ↔ ΔS=F dU_oc/dT(평형전압 온도의존 실측) · ΔS^config(지배 >½) ↔ Li·빈자리 무질서 config(O3 조성추세 대부분) · ΔS^vib 음 baseline ↔ phonon(INS, x-변화 작음) · ΔS_e(T1 MIT) ↔ electronic(O3 서 작으나 MIT 서 config 와 비등). 등치식 eq:br-reynier2004-1: ∂U_j/∂T=ΔS_rxn,j^cat/F ⇔ ΔS_rxn=F dU_oc/dT.
- ② 평형 전압 온도의존에서 리튬화 엔트로피를 실측하고 config(Li·빈자리)·phonon(INS)·electronic(계산) 세 기여로 갈라 O3 상(0.5<x≤1.0) 엔트로피 해석.
- ③ Reynier=실제 시료 리튬화 전체 엔트로피의 3기여 분해(실측·계산) / 본문=전이별 중심 표준값 ΔS_j^0 성분 나누기(혼합항은 w_j 가 담음, 이중계산 금지) — 점대점 등치 아닌 부호·척도·지배성분 수준 대조.
- 검증: 측정원리·3기여 분해·config 지배(조성추세 대부분)·phonon 음 baseline·**MIT 서 electronic≈config(우리 §15 핵심 주장 직접 뒷받침)**·척도(O3 4.2 kB/atom, 총 9.0 kB/atom) = WebSearch 초록(ASU pure) 확인. ★확인 필요: 본문 §15 "O3 총 부분몰 ≈0.18 kB/atom" 값은 초록 미명기(초록은 4.2/9.0 kB/atom) → 원문 본문/표 직접 대조 요.

## "확인 필요" 집계

- **원문 수식 재현 관련 ★확인 필요 = 2건**: marianetti2004(원 모델 Hamiltonian·Mott 판별식·식번호) · vanderven1998(클러스터 전개 에너지식·ECI·식번호). **두 건 모두 방법·결과(기작·조성경계·x=½ 질서)는 WebSearch 초록으로 검증**됐고, 논문 식을 재현하지 않고 결과/기작 수준 대응으로 제시(규칙 준수 — 구 Nature/APS PDF 가 기계 판독 불가 포맷).
- **검증 완료(형태·정의 확인, 재현 가능) = 1건**: msmr_lineage(eq:msmr 형태·f=F/RT·X_j/U_j^0/ω_j 정의 = PyBaMM 구현 문서 대조 확인; 원 식번호만 경미 미완, 다리 핵 아님).
- **부수 ★확인 필요(특정 수치, 다리 핵 아님) = 1건**: reynier2004(§15 의 "0.18 kB/atom O3 부분몰" 값 — 초록 미명기; 측정원리·분해·척도·지배성분은 확인분).
- **다리에서 논문 수식 직접 재현 = 0건**(등치 중간식은 전부 우리 기호/우리 축약; 유일하게 형태가 원 논문과 동일한 eq:br-msmr-1 은 PyBaMM 대조로 검증됨).
