# Codex build task — Ch1 v9 작가 (v9-07/08/09 공용)

너는 Ch1 v9 의 9 독립 작가 중 하나(Codex). 무통신(다른 v9-0X 읽지 마라). 경쟁·체리픽. 경계: 네 폴더만(v9-0X/). 허위 attribution 금지·tier 정직.

## 과제
Ch1(흑연 음극 dQ/dV forward 교과서)을 LCO 양극까지 통합 확장. 네 파일 `Claude/results/ch1v9/v9-0X/v9-0X.tex` 는 *이미* base v8-11(흑연, 1208줄) verbatim 복사본. 흑연 내용·식·부호·그림은 VERBATIM 보존, LCO 를 targeted 삽입(흑연 재작성 금지).

## 먼저 정독 (Claude/)
- `results/ch1v9/v9-00_spine/AUTHOR_BRIEF.md` (빌드 규칙 + LCO 확정값)
- `research/CH1v9_LCO/30_synthesis_gap.md` (절별 통합 지점·새 절 논리)
- `research/CH1v9_LCO/35_electronic_entropy_design.md` (전자 엔트로피 닫힌식·전이표·코드 일반화)
- `research/CH1_statmech_review.md` (ξ_eq 분포 프레이밍 1점 보강)
- 네 v9-0X/v9-0X.tex (편집 대상)

## 추가 (절별)
1. N0: LCO_STAGING_LIT 전이표(3.9/4.05/4.17V).
2. N2/N3: LCO U_j(T)·∂U_j/∂T(양극 부호, U 높음 ~3.9–4.2V vs Li); order–disorder Ω.
3. ★N4/N5: ξ_eq 분포 프레이밍 소절 — ξ_eq=평형 점유 확률 분포(Z=1+e^{−βΔμ}, Ω=0 Fermi-함수), kinetic+thermo 두 경로 통합 + 전자 Fermi–Dirac 다리(결과·부호 불변·유도만 추가).
4. ★새 절(N5뒤 N6앞) — LCO 전자 엔트로피: S_e=(π²/3)k_B²T·g(E_F) (Fermi–Dirac→Sommerfeld 유도); 부분몰 ΔS_e=(π²/3)k_B²T·∂g/∂x; MIT-logistic 게이트 g(E_F,x)≈g_max[1−σ((x−x_MIT)/Δx)](모델 가정·초기값 g_max=13 e/eV·x_MIT≈0.85·Δx≈0.05); 작지만(0.18 kB/atom) MIT 게이트로 필수(config 단독 2상역 재현 불가); 흑연 대비(metallic 천이 없음→전자항 0); ★∝T 명시.
5. N6: LCO dQ/dV peak(3.9/4.05–4.20V) 그림 후보.
6. N9+코드: ΔS_rxn^cat=config+vib+electronic(★이중계산 금지: ΔS^0_j=중심 표준값); MSMR↔Ch1 동형·코드 일반화(파라미터 교체+전자항 plug-in).

## 품질 (자체 10회·청크/렌즈 회전)
G-derive(추가 식 단계 유도·점프 금지·전자항 분포서 유도)·부호 사슬(양극 ∂U_j/∂T=ΔS/F 흑연 1:1)·G-follow/G-usable·orphan-0(통합·부록 아님)·흑연 VERBATIM 보존·tier 정직(문헌 초기값+데이터 피팅).

## 빌드
xelatex(kotex/D2Coding) 0-error: `cd Claude/results/ch1v9/v9-0X && xelatex -interaction=nonstopmode v9-0X.tex` 2회(페이지참조 3회). 전 오류 수정. 증분 편집(거대 단일 쓰기 금지). 그림: v8-11 5그림 보존 + LCO dQ/dV·전자 게이트 신규(TikZ 영어 ASCII 라벨).

## 산출
네 v9-0X.tex(xelatex 0-error) = 산출물. 짧은 노트(추가 절·전자 엔트로피 식·xelatex 오류수·흑연 보존·자체 10회 수렴·불확실 1곳).
