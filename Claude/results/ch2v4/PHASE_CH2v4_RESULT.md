# Phase Result — Ch2 v4 (통계열역학 챕터) [Track 2 완료]

> plan = `Claude/plans/2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md`. 9종 competition-cherrypick. 최종 = `Claude/docs/graphite_ica_ch2_v4.tex`(759줄·13p).

## 1. 목표·달성
Ch2(v3 = Bernardi 가역열 survey, 5p "Ch1+ΔS 한 절" 수준)를 **코인 하프셀 데이터 해석용 엔트로피·가역 발열 *통계열역학 챕터*** 로 심화 — ★**분포(distribution)를 명시 전개**. 코인 하프셀(단일 전극 vs Li) 단독, 전셀 합성 범위 외.

## 2. 추가된 통계열역학 콘텐츠
- ★**분배함수→점유 분포**: 단일 자리 $Z=1+e^{-\beta\Delta\mu}$ → $\langle n\rangle$=Fermi-함수 = **Ch1 logistic 의 기원**. Bragg–Williams $g(\theta)$·Ω.
- ★**분포→configurational 엔트로피**: $S_\mathrm{config}=-R\sum p_i\ln p_i=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$, 부분몰 = ∂U/∂T 봉우리 내부 항. (W/Stirling 유도.)
- **vib(포논 BE)·electronic(FD Sommerfeld, Ch1 v9 확장)** 분해 — 세 분포 기반 엔트로피.
- ★**섞임/겹침 수식**: A 겹침 가중 $\partial U_\oc/\partial T=\frac1F\sum Q_jg_j\Delta S_{\rxn,j}/\sum Q_jg_j$(★수치검증 완전식 FD 0.000 mV/K 일치)·봉우리 내부 config(★이중계산 B: ΔS^0_j=중심 표준값)·C $w_\eff=w(1-\Omega/2RT)$(V-폭→0·dQ/dV peak 발산)·D 히스 가역/비가역 분리.
- ★**극한·코너(I)**: 6코너 → "ΔS_rxn,j 전이당 상수" 근사 타당성(비선형 = 겹침+분포 config 자동).
- **가역 발열 = 분포 재배열 열**: $\dot Q_\rev=-(IT/F)\Delta S(x)$, exo/endo 정합(희박 +ΔS→방전 흡열).

## 3. 방법 (competition-cherrypick·일부 압축)
- **Phase C 설계**(선행): C.1 분포 spine + C.2 섞임 A/B/C/D/I + ★A 수치검증(Ch1 코드 실행, 완전식 FD 0.000 일치 PASS).
- **Phase D.2**: 9 독립 빌드(3S·3O·3C) → 커밋#6.
- **D.3a 검토1**: 5차원(분포·부호/섞임·w_eff·B/가역열·exo-endo/인용·문체/G-usable). base=v4-05 확정(config+w_eff 유일 정확).
- **D.3b 체리픽 v4-10**: base v4-05 + exo/endo 교정 + 인용 정정 + v4-07 procedurebox graft. (★9b 압축 — v4-05 단일 우세로 비-base 균일교정 비목적적·과병렬 절제.)
- **D.3c adversarial**(A1 물리·A2 섞임·A3 인용빌드, refute) → CRIT 0 → finalizer v4-11(4 정정·11라운드 수렴) → 커밋#8.

## 4. 품질 게이트 (전수 PASS)
- ★**4대 부호 견고**(adversarial 반증 실패): config `+R ln[ξ/(1-ξ)]`(5식 일관·역수 0)·w_eff `w(1-Ω/2RT)`(정답·역수 0)·exo/endo(Q_rev=−(IT/F)ΔS 6매핑 일관)·μ(V)/단위다리 단계 명시.
- **이중계산 B 0**·범위 코인 하프셀 CLEAN(전셀 유도 혼입 0).
- **인용 14건 검증**(fabrication 0·chemmater2015 정당·jpcc2021 "Calculations"). **문체 클린**(전보체 0). **TikZ 한글 0**(3블록). xelatex 0-error·13p.

## 5. 경쟁이 적발한 결함 (competition value)
- ★**w_eff 부호 = master 설계 doc 오류**(w/(1-Ω/2RT) 역수) — adversarial·v4-05 가 독립 적발(sympy+FWHM 삼중검증) → master 정정 w(1-Ω/2RT). 9 작가 상속분 → v4-05 만 정확.
- ★**config 부호 역수**(ln[(1-ξ)/ξ]) — v4-02·04 FAIL, Sonnet·v4-05/06 자체 적발.
- ★**exo/endo 반전** — Opus 3종(04·05·06) FAIL, Sonnet·Codex PASS → 체리픽서 교정.
- v4-04 자체 검토 sub 4개 위반 spawn(그 child 가 v4-04 결함 다수 적발=bonus).

## 6. 잔여(불확실·범위 밖)
- line 390 "T g(E_F) 상쇄" 교육적 약식(결과 차원 엄밀 정확, R11 결함 아님 판정).
- electronic 엔트로피 상세 유도는 Ch1 v9 §전자엔트로피 참조(Ch2=확장).

## 7. 산출물
- 최종: `Claude/docs/graphite_ica_ch2_v4.tex`(+pdf, 13p).
- 빌드 기록: `results/ch2v4/v4-01..11/`·`v4-00_spine/`(brief·tracking·risk-patterns·cherrypick·fix-list)·`review1/`·`review2/`.
- 설계: `research/CH2v4/`(41 분포 spine·40 섞임(정정)·42 수치검증).
