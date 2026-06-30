# Phase Result — Ch1 v9 (LCO 양극 통합 확장) [Track 1 완료]

> plan = `Claude/plans/2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md`. 9종 competition-cherrypick(N+9+9+1+1). 최종 = `Claude/docs/graphite_ica_ch1_v9.tex`(1644줄·30p).

## 1. 목표·달성
Ch1(흑연 음극 dQ/dV forward 교과서, v8-11)을 **LCO 양극까지 통합 확장**해 v9 완성 — 단일 하프셀 문건(흑연 보존 + 양극 추가). 코인 하프셀(vs Li) 범위. 전셀 합성 범위 외(후속 v10/별도).

## 2. 추가된 LCO 콘텐츠 (파생 F·H)
- **LCO 전이표**(N0): T1 MIT ~3.90V·T2/T3 order–disorder ~4.05/4.17V(tier A=Xia).
- ★**전자 엔트로피 절**(파생 F, 신규 §sec:lco-electronic): $S_e=\frac{\pi^2}{3}k_B^2T\,g(E_F)$ (Fermi–Dirac→Sommerfeld 유도), 부분몰 $\Delta S_e=\partial S_e/\partial x<0$(삽입 기준), MIT-logistic 게이트 $g(E_F,x)$(초기값 13 e/eV·0.85·0.05·피팅 위임), ∝T·자리당→몰당 단위 다리, 흑연 대비(전자항 0).
- **ξ_eq 분포 프레이밍**(통계역학 1점 보강): 단일 자리 $Z=1+e^{-\beta\Delta\mu}$→⟨n⟩ Fermi-함수=ξ_eq, kinetic+thermo 통합 + 전자 Fermi–Dirac 다리.
- **ΔS 분해**: ΔS_rxn^cat=config+vib+electronic(이중계산 B 금지·직교 자유도 가산).
- **코드 일반화**(파생 H): MSMR↔Ch1 transition-logistic 동형(f=−σ_d)·파라미터 교체+전자항 plug-in.

## 3. 방법 (competition-cherrypick)
- **Phase A 조사**(선행): master 검색 6축 + 정독-추출 서브(9카드·full 5건) → 전자 엔트로피 식·전이 파라미터 근거화.
- **Phase B.2**: 9 독립 빌드(3 Sonnet·3 Opus·3 Codex, 무통신) → 커밋#1.
- **B.3a 검토1**: 5 차원(전자엔트로피·부호·분포B·보존빌드·인용). ★master 부호 판정(R1↔R2 충돌→흑연 본문 직접검증) = ΔS_e 삽입 기준 <0.
- **B.3b 9b 보완**(방향성-만) + 검토2(부호·인용 마스터) → 커밋#2.
- **B.3c 체리픽 v9-10**: base=v9-06 + graft(v9-04 분포·유도·단위, v9-03 규약·decomp, v9-05 인용8·σ_d, v9-02 self-test) → 커밋#3.
- **B.3d adversarial 재검수**(A1 물리·A2 부호흑연·A3 인용빌드, refute) → CRIT/HIGH 0 → finalizer v9-11(7 정정+11라운드 수렴) → 커밋#4.

## 4. 품질 게이트 (전수 PASS)
- 흑연 **byte-동일**(diff 4 hunk=헤더3+bib만, 물리·수식 0변경). ΔS표 +29/0/−5/−16·U 0.085·S1-S8·R1-R5 intact.
- ΔS_e=∂S_e/∂x<0(삽입) **6앵커 일관**·이중계산 0·∝T.
- 인용 **8건 검증**(V2 마스터: Reimers&Dahn·Ménétrier·Motohashi PRB80·Xia JES154·Reynier PRB70·Świderska-Mocek PCCP21=+0.83mV·MSMR ECS Adv3·Teichert JMPS190). fabrication 0(v9-03 "R.Aronson" 폐기).
- xelatex **0-error·30p·bibitem 15**·한글그림 0·orphan 0.

## 5. 경쟁이 적발한 결함 (competition value)
- ★**ΔS_e 부호-기준 오류**: 유도 최고 5초안(01/04/06/08/09)이 제거-positive>0 역부호 → master 흑연 본문 검증으로 삽입<0 확정.
- ★**인용 fabrication·오귀인**: v9-03 "R.Aronson"(생성)·+0.83 mV/K 6종 오귀인(→Świderska-Mocek)·MSMR 구버전 → 웹검증·V2 마스터로 정정.
- v9-04 Δμ 부호버그(자체 적발·1e-12 검증)·D-PEAK 비전파.

## 6. 잔여(HELD·범위 밖, 사용자 판단)
- **A3-1 overfull 22.6pt**: 흑연-verbatim 단락이라 미수정(흑연 byte-동일 > LOW 조판, 더 제한적 통제).
- **tab:lco-staging T3 config 1.49 J/K·mol**: 표 x범위(≈0.48 전이조성)와 문헌 측정조성(x=2/3) 표기 불일치 — coherence soft-spot(수치 모순 아님, 문헌 앵커 정직 병기). 표 x범위 컬럼 의미 1줄 주석으로 해소 가능(교수님 피드백 v10 후보).

## 7. 산출물
- 최종: `Claude/docs/graphite_ica_ch1_v9.tex`(+pdf, 30p).
- 빌드 기록: `results/ch1v9/v9-01..11/`·`v9-00_spine/`(brief·tracking·cherrypick·fix-list)·`review1/`·`review2/`.
- 조사: `research/CH1v9_LCO/`(scope·sources·추출 9카드·전자엔트로피 설계).
- v10 = 교수님 피드백 후속(전셀 합성·표 주석 등).
