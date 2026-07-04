# opus2 — V1.0.14 P5.1 이미지 경연 제출 (8안)

작성자: opus2. 노선(개성): 정량 밀도 극대화 — 모든 특징점에 검산 가능한 수치 좌표·눈금·보조선을 얹고,
모든 곡선 좌표는 대응 식의 수치 평가(schematic 금지)로 산출해 T{n}_calc.py 에 동봉했다. 그림 내부 텍스트는 영어
ASCII, 캡션은 본문 표기(peak·sigma_d·xi_eq·U_j^d 등)와 정합, 색은 회색조 인쇄 내성(선종 solid/dashed/dotted).

## 검증
- _check.tex = _skeleton.tex 프리앰블 그대로 복사(라이브러리 positioning,arrows.meta,calc,fit,backgrounds 동일 —
  shapes.geometric 등 미로드 라이브러리 미사용). 8안 전부 input 후 xelatex EXIT=0, "!" 오류 0건, Overfull hbox 0건
  (증거 = 동봉 _check.pdf, 5쪽). 미해결 참조 40건은 스켈레톤에 라벨·bib 이 없어 나는 warning(오류 아님)뿐.
- 각 T{n}_calc.py 는 해당 그림의 좌표·특징점을 계산·출력(무의존, 표준 라이브러리만). 전 스크립트 재실행 오류 0.
- 시각 검수: 5쪽 전부 130 dpi 래스터 육안 확인 — 라벨-곡선/라벨-라벨 교차 0, 물리 정보 소실 0(기존 유지 + 정량 추가).

## 대상별 요약 (파일 = tikzpicture + caption + label 만; 기존 label 유지)
- T1_spine.tex (fig:spine): N0-N9 흐름 + 노드별 산출량·지배식 번호 병기 + 화살표 전달량 라벨. peak 단계 분기
  (mode switch eq:branch -> N6 평형종 / N8 인과꼬리) 시각화, 전이 loop(N2-N8) 파선 상자.
- T2_staging.tex (fig:staging): stage 4->1 갤러리 채움(주기 4/3/2/2/전부) + 전이 전위 축에 U=0.210/0.140/0.120/0.085 V
  dropline, 종 glyph 폭 ~ w=0.020/0.016/0.014/0.012 V, Q 표기(표 tab:staging 정합).
- T3_hysloop.tex (fig:hysloop): y=ln[xi/(1-xi)]+4(1-2xi) 수치 평가. spinodal (0.146,+1.066)/(0.854,-1.066)
  (u=sqrt(1/2)), gap dU^hys=2.131 RT/F(298K 54.8mV), Maxwell y=0, 과주행 화살표.
- T4_barrier.tex (fig:barrier): 이중 포물선 G_base=0.1+0.9 sin^2[pi(x-1)/4], 구동 -A*phi. 장벽 정방향 0.65·역방향
  1.15·정점 강하 chiA=0.25·골 강하 A=0.50 명기, dH_a^eff 주석.
- T5_flux.tex (fig:flux): r-=1 고정->역선 y=xi 공통, A/RT=0,ln2,2ln2 (r+=1,2,4) 3케이스 오버레이, 교점
  xi_eq=1/2,2/3,4/5 dropline·눈금. detailed balance readout.
- T6_logistic.tex (fig:logistic): 이중 축(좌 xi_eq·우 dxi/dV), T=268/298/328K 종 3개: w=23.1/25.7/28.3 mV,
  정점 1/(4w)=10.83/9.74/8.85 /V, FWHM 3.53w=90.5mV(298K), 중심 접선 기울기 1/(4w).
- T7_reversal.tex (fig:reversal): 저역통과 점화식 실제 수치 평가(schematic 아님): rho=0.967, peak shape
  (xi_eq-xi_lag)/L_V. 방전 정점 (+1.00w,0.192)/충전 (-1.00w,0.192)=정확한 거울(eq:reversal), 평형종 점선 중첩.
- T8_widthbudget.tex (fig:widthbudget): 이산 합성곱 실제 수치 평가: 델타->내재 종(0.25)->conv Gaussian(sig_eta=1.25
  sig_int)->+단측 지수꼬리. sig_int=1.81w·sig_eta=2.27w·sig_sym=2.90w·L_V=1.50w 막대 대비, tailed 정점 (+1.26w,0.127).

## 공통 수칙 6 준수
1. 모든 곡선 = 식 수치 평가(캡션 식 번호 명기), calc.py 재현 가능. 2. 라벨 무교차(5쪽 육안). 3. 내부 ASCII·캡션 본문 정합.
4. 기존 물리 정보 유지 + 정량 추가(소실 0). 5. 스켈레톤 단독 0-err. 6. label 8종 원본 유지.

## 주의/설계 선택
- T1: 스켈레톤 shapes.geometric 미로드 -> mode-switch 노드는 다이아몬드 대신 스타일 상자(라이브러리 제약 준수).
- T2: 종 glyph 정점은 가독 위해 균일화(실제 높이 ~ Q/4w 편차 큼) — 위치·상대폭은 정확(캡션 명시).
- T7·T8: 저역통과·합성곱을 근사 없이 이산 수치 적분으로 평가(문건 만족 그림보다 충실). T7 은 두 패널 세로 적층로 여백 확보.
- 원본 문건(graphite_ica_ch1_v1.0.14.tex) 무수정, 좌표 조작 없음(전량 calc.py 산출).
