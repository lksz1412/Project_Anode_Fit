# Ch2 v4 — AUTHOR_BRIEF (9종 경쟁 빌드 입력)

> competition-cherrypick 스킬. base = `base_ch2_v3.tex`(265줄·6절, Bernardi 가역열 survey = *얇은 출발 skeleton*). 9 작가(무통신) 동일 배포. ★v4 = intercalation 엔트로피·가역 발열 *통계열역학 챕터*(분포 명시 전개) — v3 의 "Ch1+ΔS 한 절" 수준 탈피.

## 목표 (한 줄)
Ch2 를 **코인 하프셀(전극 vs Li) 데이터 해석용 엔트로피·가역 발열 통계열역학 챕터**로 — ★**분포를 명시 전개**(분배함수→점유 분포→config/vib/electronic 엔트로피), 섞임/겹침 수식(ξ·Ω 닫힌식) 박음. v3 의 Bernardi 가역열 틀은 보존·심화.

## ★범위 가드
- **코인 하프셀 단독**(단일 전극 ∂U/∂T·가역열). ★**전셀 합성(∂U_cell=∂U_cat−∂U_an) 범위 외**(혼동 금지). 흑연 음극 하프셀 중심, LCO 전자항은 분포 사례로 포함(Ch1 v9 확장).
- Ch1(forward dQ/dV) 재유도 금지 — *결과 인용*(logistic·U_j·ΔS_rxn). Ch2 = 그 분포의 엔트로피·온도·가역열.

## ★추가 (통계열역학 spine — C.1·C.2 설계 확정값)
정독: `research/CH2v4/41_statmech_spine.md`(분포 spine)·`40_mixing_term_design.md`(섞임 A/C/D/I)·`42_numerical_verification.md`(파생 A 수치검증)·`base_ch2_v3.tex`.
1. **도입**: 왜 엔트로피엔 통계가 필요한가(분포·앙상블, 가역열=분포 재배열 열).
2. ★**격자기체 분배함수 → 점유 분포**: 단일 자리 $Z=1+e^{-\beta\Delta\mu}$→⟨n⟩=Fermi-함수=**Ch1 logistic 의 기원**. 다자리 Bragg–Williams $g(\theta)$·Ω.
3. ★**분포 → configurational 엔트로피**: $S_\mathrm{config}=-R\sum p\ln p=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$. 부분몰 $-R\ln[\theta/(1-\theta)]$ = ∂U/∂T 의 봉우리 내부 항. ★Ch1 의 $w=RT/F$ 가 이미 담음.
4. **vib(포논 BE)·electronic(FD, Ch1 v9 확장)** 분해 — 세 분포 기반 엔트로피.
5. ★**섞임/겹침 수식**: A 겹침 가중 $\partial U_\oc/\partial T=\frac1F\sum Q_jg_j\Delta S_{\rxn,j}/\sum Q_jg_j$(+수치검증)·봉우리 내부 config(★이중계산 B: ΔS^0_j=중심 표준값)·C $w_\eff=w(1-\Omega/2RT)$(★V-폭, Ω↑→0·dQ/dV peak 발산)·D 히스 분기별 ∂U/∂T(가역 평균/비가역 분리).
6. ★**극한·코너(I)**: ξ→0,1 config 발산·ξ=½ 표준·Ω→2RT plateau·단일봉우리 환원·고온 electronic → "ΔS_rxn,j 전이당 상수" 근사 타당성 판정(비선형은 겹침+분포 config 자동 생성).
7. **가역 발열**: $\dot Q_\rev=-IT\,\partial U/\partial T=-(IT/F)\Delta S(x)$ = 분포 재배열 열. v3 의 다온도 dQ/dV 추정·synthesis 심화.

## 품질 렌즈 (자체 10회 + 검토)
- **G-derive ★**: 분포→엔트로피 단계 유도(분배함수 Z→⟨n⟩→S=−R∑p ln p, 점프 금지). Sommerfeld·BE 도 분포서.
- **이중계산 B**: ΔS^0_j=중심 표준값, config 는 분포(w)가 줌 — 별개 항 명시(이중가산 0).
- **부호**: ξ=탈리튬화 진행률(Ch1 일관)·∂U/∂T=ΔS/F·ΔS_e 삽입<0(Ch1 v9).
- **G-follow·G-usable**: 따라가지고, 이 식으로 하프셀 ∂U/∂T·가역열 산출.
- **챕터급 충실도 ★**: Ch1 한 절 아님 — 분포 전개가 챕터 본체. 분량은 콘텐츠의 자연 결과.
- **그림**: 분포(점유 ⟨n⟩·S_config)·겹침 가중·w_eff(Ω) 시각화(TikZ 영어 ASCII).
- **인용**: Ch2 v3 의 11 출처 + 통계역학 정전(Newman·Huggins·Bazant lattice-gas) — 정확 DOI·허위 0·tier 정직.

## 산출 (작가별)
`results/ch2v4/v4-0X/v4-0X.tex`(xelatex 0-error) + 노트(분포 전개·섞임 수식·이중계산·자체 10회). 9 작가 = v4-01–03 Sonnet·04–06 Opus·07–09 Codex(단계구동·관찰).
