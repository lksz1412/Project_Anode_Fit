# Codex build task — Ch2 v4 작가 (v4-07/08/09 공용)

너는 Ch2 v4 의 9 독립 작가 중 하나(Codex). 무통신(다른 v4-0X 읽지 마라). 경쟁·체리픽. 경계: 네 폴더만(v4-0X/). 허위 attribution 금지·tier 정직.

## 과제
Ch2 를 **코인 하프셀 데이터 해석용 엔트로피·가역 발열 *통계열역학 챕터*** 로 — 분포(distribution)를 명시 전개. base `base_ch2_v3.tex`(265줄, Bernardi 가역열 survey)는 *얇은 출발 skeleton*(대폭 심화·구조 재편). ★Ch1 한 절 아닌 챕터급. 코인 하프셀 단독(전셀 합성 범위 외).

## 먼저 정독 (Claude/)
- `results/ch2v4/v4-00_spine/AUTHOR_BRIEF.md` (목표·범위·통계열역학 spine·품질 렌즈)
- `research/CH2v4/41_statmech_spine.md` (분배함수→점유분포→config/vib/electronic 엔트로피)
- `research/CH2v4/40_mixing_term_design.md` (섞임 A 겹침가중·B 이중계산·C w_eff(Ω)·D 히스·I 극한)
- `research/CH2v4/42_numerical_verification.md` (파생 A 수치검증 결과)
- `results/ch2v4/v4-00_spine/base_ch2_v3.tex` (출발 skeleton)

## 챕터 구조 (심화)
1. 도입: 왜 엔트로피엔 통계가 필요한가(분포·앙상블, 가역열=분포 재배열).
2. ★격자기체 분배함수 Z=1+e^{-βΔμ} → 점유 분포 ⟨n⟩=Fermi-함수 = Ch1 logistic 기원. Bragg-Williams g(θ)·Ω.
3. ★분포→configurational 엔트로피 S_config=-R∑p ln p=-R[θlnθ+(1-θ)ln(1-θ)]. 부분몰 -R ln[θ/(1-θ)].
4. vib(포논 BE)·electronic(FD, Ch1 v9 확장) 분해.
5. ★섞임/겹침: A 겹침 가중 ∂U_oc/∂T=(1/F)∑Q_j g_j ΔS_rxn,j/∑Q_j g_j (+수치검증)·봉우리 내부 config(★이중계산 B: ΔS^0_j=중심 표준값)·C w_eff=w(1-Ω/2RT)(★V-폭, Ω↑→0)·D 히스 분기별(가역 평균/비가역 분리).
6. ★극한·코너(I): ξ→0,1 발산·ξ=½ 표준·Ω→2RT plateau·단일봉우리 환원·고온 electronic → "ΔS_rxn,j 상수" 근사 판정.
7. 가역 발열 Q_rev=-IT ∂U/∂T=-(IT/F)ΔS(x)=분포 재배열 열. v3 다온도 dQ/dV 추정·synthesis 심화.

## 품질
G-derive(분포→엔트로피 단계 유도·점프 금지)·이중계산 B(ΔS^0_j=중심 표준값·config 는 w 가 줌)·부호(ξ=탈리튬화·ΔS_e 삽입<0)·G-follow/usable(이 식으로 하프셀 ∂U/∂T 산출)·챕터급 충실도(분량은 콘텐츠 자연 결과)·tier 정직. 그림 분포·겹침·w_eff(TikZ 영어 ASCII).

## 빌드
xelatex(kotex/D2Coding) 0-error: `cd Claude/results/ch2v4/v4-0X && xelatex -interaction=nonstopmode v4-0X.tex` 2회. 증분 편집(거대 단일 쓰기 금지). 인용 = v3 11출처 + 통계역학 정전(정확 DOI·허위 0).

## 산출
네 v4-0X.tex(xelatex 0-error). 짧은 노트(분포 전개·섞임 수식·이중계산·페이지·자체 10회 수렴·불확실 1곳).
