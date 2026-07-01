# V1010_INSPECT_draft_C3

검수자: C3  
역할/렌즈: G-follow(독자 따라가나), G-usable(재현가능), 완결성, 시각(PDF 판독), 그래프 개형, radius 연구 회의적 독립검증  
대상: Anode_Fit v1.0.10 문제점 대검수. 코드/문건 수정 없음. 검수 의견만 기록.

## 0. 직접 확인 범위

- base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/inspect_base.txt` 1-26행 전문 확인.
- 계획서: `Claude/plans/2026-07-05-v1010-problem-inspection-plan.md` 1-35행 전문 확인.
- 프로젝트 지침: 루트 `AGENTS.md` 없음 확인, `CLAUDE.md` 전문 확인.
- 현재 v1.0.10: `Anode_Fit_v1.0.10.py` 1-851행, `graphite_ica_ch1_v1.0.10.tex` 1-1937행, `graphite_ica_ch2_v1.0.10.tex` 1-750행, `FITTING_GUIDE.md` 1-46행 전문 확인. Ch1 1339-1396행은 출력 누락 의심 구간 재확인.
- 그래프 스크립트: `plot_dqdv.py` 1-135행, `graph_suite_p5.py` 1-105행, `demo_lco_heat.py` 1-72행, `test_regression_graphite.py` 1-80행 전문 확인.
- 그래프 실측: 원본 `figs` 덮어쓰기 방지를 위해 별도 임시 위치 `Claude/results/process/C3_graph_check/c3_graphite_lco_check.png`에 직접 실행 결과 생성 후 육안 판독. 기존 `figs/anode_fit_v1_0_10_dqdv.png`, `figs/P4_lco_heat_validation.png`, `figs/P5_graph_suite.png`, `results/research/radius/fig_bell_vs_spike.png` 육안 판독.
- PDF 판독: Ch1 PDF 35쪽, Ch2 PDF 13쪽을 `pdftoppm`으로 렌더링해 contact sheet 및 핵심 페이지를 육안 판독. 주요 확인 페이지: Ch1 p24, p29, Ch2 p10.
- radius 연구: `RADIUS_VERDICT.md`, `ORIGIN_VERDICT.md`, `BAND_VERDICT.md`, `CODE_w_check.md`, `DOCS_say_about_distribution.md`, `PHASE_RADIUS_RESULT.md`, `RADIUS_LEDGER.md`, `50_report.md`, `40_scope_band.md`, `41_gitt_residual_equilibrium.md` 확인. 장문 축별 카드는 회의적 포인터로만 취급.
- 구버전 대비: 계획서 지정 구버전 중 v3/v4/v5/v10 및 Ch2 v4의 핵심 문구를 직접 대조했다. 특히 `rho_G`, 역산 금지, forward-only, two broadening, `w_eff`, solid-solution/two-phase 문구를 확인했다. 구버전 전체 전문 판정은 하지 않고, 누락/유지 판단에 필요한 근거 라인을 직접 대조했다.

## 1. 문제 목록

### [HIGH] 기본 graphite dQ/dV가 4 staging peak가 아니라 1개 넓은 봉우리로 붕괴한다

- 위치: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py:294-306`, `:380-388`, `:680-708`; `figs/anode_fit_v1_0_10_dqdv.png`; 직접 실행 그래프 `Claude/results/process/C3_graph_check/c3_graphite_lco_check.png`.
- 무엇이 물리적으로 틀렸나: base prompt가 요구한 graphite 4 staging peak 위치 U≈0.210/0.140/0.120/0.085 V가 기본 출력에서 분리되어 보이지 않는다. 직접 실행에서 full equilibrium의 significant peak는 `V=0.100266`, 높이 `7.3001`의 1개뿐이었다.
- 왜 문제인가: 현재 `GRAPHITE_STAGING_LIT` 네 전이는 모두 `'n': 1.0`을 갖고 `_n_factor`가 `n`을 우선하므로, 298 K에서 모든 단일 전이 폭은 `RT/F=25.69 mV`, FWHM은 약 `90.56 mV`로 동일하다. 전이 간격은 0.2109-0.1399=71.0 mV, 0.1399-0.1203=19.6 mV, 0.1203-0.0853=35.0 mV라 FWHM보다 작거나 비슷해 병합이 필연적이다. 실제 실행 측정도 단일 전이별 FWHM `90.559 mV`, full curve peak 1개로 나왔다.
- refute 시도: 면적 보존은 finite window에서 약 `0.978`로 크게 깨지지는 않는다. 그러나 면적 보존은 peak 분리성의 반증이 아니다. 육안 그래프와 수치 peak 검출 모두 4개 staging peak 재현을 반박한다.
- 렌즈: 그래프 개형, G-usable, 완결성.

### [HIGH] `w` 폴백값이 실제 기본 경로에서는 죽어 있어, 문서의 폭 설명과 재현 경로가 독자에게 위험하다

- 위치: `Anode_Fit_v1.0.10.py:294-306`, `:680-708`; `plot_dqdv.py:50-76`; `graphite_ica_ch1_v1.0.10.tex:736-743`, `:1686-1688`.
- 무엇이 물리적으로 틀렸나: 표와 문서는 `w=0.020/0.016/0.014/0.012 V`를 폭 출발값/폴백으로 말하지만, 코드 기본 전이 dict에는 모두 `n=1.0`이 있어 `_n_factor`가 `w`를 보지 않는다. 즉 독자가 기본 데이터셋을 그대로 실행하면 `w` 값이 폭에 반영되지 않는다.
- 왜 문제인가: Ch1은 이 사실을 일부 명시하지만, 실제 그래프 재현 관점에서는 매우 취약하다. `plot_dqdv.py`도 `STAGING_W_ACTIVE`에서 `n`을 `pop`해야만 `w=12 mV`류 좁은 폭을 보여준다. 이는 "기본 모델"과 "폭 폴백이 활성화된 비교 모델"이 서로 다른 dict 경로라는 뜻이다. 독자는 표의 `w`를 조정해도 `n`을 제거하지 않으면 그래프가 변하지 않는다는 점에서 쉽게 실패한다.
- refute 시도: 코드 주석 `Anode_Fit_v1.0.10.py:8-10`과 Ch1 상단 주석은 `n` 우선과 `w` 폴백 비활성을 밝힌다. 따라서 완전 은폐는 아니다. 그러나 base prompt의 그래프 재현성과 실사용 관점에서는 "명시되어 있으니 무결"로 보기 어렵다. 실제 기본 출력이 1개 봉우리라 피해가 발생한다.
- 렌즈: G-follow, G-usable, 그래프 개형.

### [HIGH] `FITTING_GUIDE.md`의 Ω 하한이 Ch1의 solid-solution/two-phase 구분을 피팅 단계에서 막는다

- 위치: `FITTING_GUIDE.md:13`; `graphite_ica_ch1_v1.0.10.tex:736-743`, `:1227-1233`; `graphite_ica_ch2_v1.0.10.tex:202-204`, `:539-562`.
- 무엇이 물리적으로 틀렸나: guide는 Tier 2 `Ω`에 대해 공통 하한 `>2RT(≈4958@298K)`와 제약 `Ω>2RT(spinodal)`을 둔다. 그러나 Ch1은 graphite staging 중 dilute→stage4 및 4L↔3L은 solid-solution으로 `Ω<2RT` 쪽에 피팅될 것으로 기대하고, LiC12/LiC6 두 전이만 two-phase로 남는다고 설명한다.
- 왜 문제인가: 피팅 guide를 그대로 따르면 첫 두 전이를 `Ω<2RT`로 보낼 수 없어, 문서가 회복하려는 전이별 물리 구분을 알고리즘/운용 지침이 봉쇄한다. 이는 "전부 두-상은 초기값일 뿐"이라는 Ch1의 완화 문구와 정면 충돌한다.
- refute 시도: guide가 매우 짧고 초안적 운용표라는 점은 감안할 수 있다. 하지만 사용자는 guide를 보고 실제 피팅 bounds를 잡게 되므로, 이 행 하나가 재현 가능한 잘못된 피팅 제약을 만든다.
- 렌즈: G-usable, 완결성, 물리 제약.

### [MED] LCO 그래프/코드 demo가 문서의 세 peak anchor와 맞지 않는다

- 위치: `Anode_Fit_v1.0.10.py:623-640`, `:657-673`; `graph_suite_p5.py:72-75`; `graphite_ica_ch1_v1.0.10.tex:1180-1214`, `:1729-1737`; `FITTING_GUIDE.md:28`; `figs/P4_lco_heat_validation.png`, `figs/P5_graph_suite.png`.
- 무엇이 물리적으로 틀렸나: Ch1은 LCO half-cell의 세 peak를 T1≈3.90 V(MIT), T2≈4.05 V, T3≈4.17-4.20 V로 설명한다. 하지만 코드의 `LCO_MSMR_LIT`는 `U=3.930/3.880/4.050`, 전자항 `x_MIT=0.50`이며 모두 `n=1.0`이다. 직접 실행과 기존 P4/P5 육안 판독에서 LCO는 세 개의 명확한 anchor peak가 아니라 넓은 주봉+어깨에 가깝다.
- 왜 문제인가: 문서가 "흑연 forward 교과서가 LCO까지 한 틀로 닫힌다"는 방향을 제시하는 반면, 현재 코드는 guide가 말하는 Phase D 이전의 tier-C demo에 가깝다. 그래프 제목/검증 이미지가 이를 validation처럼 보이면 독자는 LCO 세 peak 재현을 기대하고 실패할 수 있다.
- refute 시도: `FITTING_GUIDE.md:28`은 Phase D에서 `x_MIT=0.85` 및 T-ref freeze/T² curvature를 고쳐야 한다고 적어, 미완성을 인정한다. 따라서 fatal한 은폐는 아니다. 문제는 "현재 graph suite가 실제 anchor 재현이 아니라 placeholder demo"라는 시각적 표시가 약하다는 점이다.
- 렌즈: 그래프 개형, G-follow, 완결성.

### [MED] graph suite PNG의 한글 글리프가 깨져 시각 검증물로서 판독성이 떨어진다

- 위치: `graph_suite_p5.py` 전반, 특히 한글 title/label 문자열; `figs/P5_graph_suite.png`.
- 무엇이 물리적으로 틀렸나: 물리식 자체의 오류는 아니지만, P5 graph suite의 일부 제목/라벨이 네모 박스/깨진 글리프로 렌더링되어 검증 그림을 육안 판독하기 어렵다.
- 왜 문제인가: base prompt가 시각 판독과 그래프 개형 확인을 요구한다. 그래프 suite가 validation artifact라면 label이 깨지는 순간 어떤 panel이 무엇을 입증하는지 추적성이 떨어진다. 특히 여러 validation panel이 한 장에 모여 있어 라벨 의존도가 높다.
- refute 시도: 데이터 곡선 자체는 보인다. 그러나 validation artifact는 곡선뿐 아니라 panel 의미와 axis/legend를 함께 읽어야 하므로, 글리프 깨짐은 낮은 위험이 아니라 재현 보고 품질 문제다.
- 렌즈: 시각, G-usable.

### [MED] PDF 본문은 읽히지만 실제 코드 출력 graph shape 불일치를 본문 그림만으로는 잡기 어렵다

- 위치: Ch1 PDF p24 Figure 9, p29 Figure 11/Table 3; Ch2 PDF p10; `graphite_ica_ch1_v1.0.10.tex:1357-1390`, `:1686-1688`.
- 무엇이 물리적으로 틀렸나: PDF 레이아웃 자체는 대체로 정상 렌더링된다. 다만 핵심 broadening 그림은 schematic이며, 실제 v1.0.10 코드 기본 출력의 "4 transition collapse into one bell"을 그대로 보여주지 않는다.
- 왜 문제인가: 문서 독자는 Figure 9의 "near-delta -> bell" 설명과 Table 3의 네 transition을 보고 기본 코드가 네 staging feature를 그릴 것이라고 기대할 수 있다. 하지만 실제 code-output graph는 넓은 단일 봉우리다. PDF만 읽어서는 이 개형 실패가 드러나지 않고, 반드시 코드 실행 그래프를 봐야 한다.
- refute 시도: Ch1은 `n=1` active와 `w` fallback inert를 상단 및 표 주변에 명시한다. 그러나 시각 자료는 이 사실의 그래프 결과를 충분히 경고하지 않는다.
- 렌즈: 시각(PDF), G-follow, 그래프 개형.

### [LOW-MED] finite-window area ratio를 area 보존 검증처럼 쓰면 오해 소지가 있다

- 위치: `graph_suite_p5.py:89-94`; `figs/P5_graph_suite.png`.
- 무엇이 물리적으로 틀렸나: P5 V9는 graphite area ratio를 약 `0.979`로 보여준다. 직접 실행에서도 0.0-0.34 V finite window에서 area/Qsum≈`0.9783`이었다. 이는 넓은 `n=1` tail이 plotting/integration window 밖으로 빠진 효과로 보인다.
- 왜 문제인가: 단일 transition의 logistic 면적 보존 자체는 수학적으로 맞다. 하지만 graph suite가 finite plotting window의 ratio를 "area preservation" 검증처럼 보이면, tail truncation과 물질량 보존을 혼동할 수 있다.
- refute 시도: 이 항은 물리 모델 자체의 핵심 오류라기보다 validation 표시 방식 문제다. 넓은 전압 범위로 적분하면 보존성은 더 좋아질 가능성이 높다. 따라서 등급은 LOW-MED로 둔다.
- 렌즈: G-usable, 그래프 검증.

## 2. cross-version 누락/회귀 판정

- v3/v4/v5에는 `rho_G` 장벽 분포, 꼬리에서의 분포 역산 금지, ill-posed 경고, forward-only 운용, 융합 뒤 전이별 면적 역산 금지, 두 가지 broadening(입자별 분기 전위 분포 + 동역학 꼬리)이 명시적으로 강했다. 직접 확인 근거: v4 `:1614-1654`, `:1902-1906`, `:2086-2089`; v5 `:1117-1140`, `:1317`, `:1435`.
- v10 및 v1.0.10에는 이 내용이 일부 복원되어 있다. 특히 v1.0.10 Ch1 `:1289-1351`은 `rho(U_app)` forward 평균, 역산 금지, radius/PSD 크기 convolution 배제를 명시한다. 따라서 "구버전의 경고가 완전히 사라졌다"는 주장은 반박된다.
- 그러나 현재 코드 forward 모델은 여전히 단일 effective particle/logistic 폭 경로이고, v1.0.10 기본 graph는 4 staging peak를 하나로 병합한다. 즉 누락은 "문구 삭제"보다 "경고는 남았지만 사용자가 실행하는 기본 그래프/guide가 그 경고를 검증 가능한 형태로 구현하지 못함"에 가깝다.
- Ch2 v4의 `w_eff(Ω)` narrowing 설명은 v1.0.10에서 제거/대체되었다. 이 제거 자체는 radius 연구 및 v1.0.10 Ch2의 회의적 정리와 맞으므로 회귀로 보지 않는다. 단, 제거 후 대체된 two-phase phenomenological width가 기본 코드에서 `n=1` 넓은 폭으로만 드러나는 점이 가장 큰 실사용 회귀다.

## 3. radius 연구 회의적 반영

- radius 연구는 확정근거로 쓰지 않았다. `RADIUS_VERDICT.md`, `ORIGIN_VERDICT.md`, `BAND_VERDICT.md`의 공통 결론은 "입자 radius -> U_j 분포"를 확정 채널로 삼지 말고, kinetic/RTF/구조무질서/메타안정성을 우선하라는 쪽이다.
- 이 결론은 v1.0.10 Ch1의 `rho(U_app)` forward-only, radius/PSD convolution 배제(`:1326-1351`)와 대체로 일치한다.
- 따라서 radius 관련 문서의 방향은 무결 쪽이다. 다만 이 무결성은 graphite 기본 graph가 4 peak를 못 보이는 문제를 방어하지 못한다. radius를 배제해도 현재 폭 경로의 병합 문제는 코드 실행으로 독립 확인된다.

## 4. 무결/낮은 위험으로 본 항목

- PDF 렌더링: Ch1 35쪽, Ch2 13쪽 모두 페이지 단위 렌더링이 가능했고, contact sheet 및 핵심 페이지에서 대형 blank, page loss, 수식 대규모 깨짐은 보지 못했다.
- sign/direction 기본: Ch1/Ch2의 `Ω>2RT` spinodal, `Ω<=2RT` gap 소멸, hysteresis branch 평균, `w_eff` 제거 방향은 문서 내부 논리상 대체로 일관된다.
- radius 배제: v1.0.10의 radius/PSD convolution 배제와 역산 금지 문구는 radius 연구의 회의적 결론과 충돌하지 않는다.
- LCO 미완성 표시: LCO 전자항 및 `x_MIT` 문제는 guide에서 Phase D 과제로 남겨져 있어 완전 은폐는 아니다.

## 5. 가장 약한 1곳

가장 약한 1곳은 `GRAPHITE_STAGING_LIT`의 기본 폭 경로다. `n=1.0`이 네 전이에 모두 들어가면서 `w` 폴백을 죽이고, 모든 transition을 FWHM 약 90.56 mV의 넓은 logistic peak로 만든다. 이 폭은 transition 간격보다 커서 4 staging peak가 실제 출력에서 1개 broad peak로 합쳐진다. 문서가 `n` 우선과 `w` 비활성을 적어 두었더라도, 사용자가 코드와 graph suite를 따라 실행했을 때 가장 먼저 보는 물리 개형이 base prompt의 4 staging peak 기대와 맞지 않는다.

## 6. 5줄 요약

1. v1.0.10 기본 graphite dQ/dV는 코드 직접 실행과 육안 판독에서 4 peak가 아니라 1개 넓은 peak로 나온다.
2. 원인은 `n=1.0` 우선 경로가 `w` 폴백을 비활성화하고, 모든 전이 FWHM을 약 90.56 mV로 만드는 데 있다.
3. `FITTING_GUIDE.md`의 `Ω>2RT` 공통 하한은 Ch1의 solid-solution/two-phase 전이별 구분과 충돌한다.
4. LCO graph demo는 문서의 세 anchor peak 재현이라기보다 Phase D 이전 placeholder이며, P5 PNG는 한글 글리프 깨짐도 있다.
5. radius/PSD 배제와 역산 금지는 대체로 건전하지만, 이 건전성은 현재 기본 graphite graph shape 실패를 해결하지 못한다.
