# V1.0.14 P5.1 이미지 경연 — opus3 제출 보고

- 제작자: opus3
- 개성(노선): 구조 재발명 — 각 대상의 현행 구도 약점을 진단하고 배치 자체(패널 분할·축 선택·비교 병치·서사 방향)를 근본부터 재설계. 기존 물리 정보 소실 0.
- 공통 수칙 준수: (1) 모든 곡선 좌표는 명시 식의 수치 평가(각 T{n}_calc.py 산출·검증, tikz 에 그 값 사용 — schematic 아님). (2) 라벨 교차 회피(렌더 검수 후 정정). (3) 그림 내부 텍스트=영어 ASCII, 캡션=본문 표기(peak·sigma_d·xi_eq·w_j) 정합. (4) 물리 정보 무손실(추가만). (5) 8안 전부 xelatex 0-err(_check.tex 확인). (6) label 원본 유지.
- 회색조 인쇄 내성: 색 미사용 — 선종(실/파/점선)·굵기·명도(black!24/72)·해칭만으로 구분.

## 대상별 진단 -> 재설계

- T1 fig:spine — 현행: 10칸 수직 사각 나열, 저정보밀도, 루프=단순 파선상자, 분기 미시각화. 재설계: 트렁크(N0·N1 / N9·out) + 파선 루프상자(N2-N8) + next-j 귀환 화살표, xi_eq(N5)에서 평형 peak vs 인과 꼬리 분기(eq:branch)를 두 경로->merge 로 도해, 각 노드에 산출량+식번호 병기. 보존: 노드 물리 전부 + 반복·분기·식번호 추가. 좌표: T1_calc.py(노드<->식 라벨 존재 전수검증, missing=0).
- T2 fig:staging — 현행: 갤러리 도식만, 전이전위·peak 미연결. 재설계: 갤러리 5열 유지 + 하단 실제 선형 전위축에 4전이 정박, 기울어진 leader 가 전위간격 비균일성 노출, 각 전이에 높이~Q_j peak glyph. 보존: 갤러리 채움패턴 + U_j·Q_j·peak 대응 추가. 좌표: T2_calc.py(tab:staging U=0.210/0.140/0.120/0.085 단조감소 검증, 축 매핑).
- T3 fig:hysloop — 현행: 과주행 방향·Maxwell선·gap 상한 주석 부재. 재설계: 비단조 Veq(xi) 유지 + Maxwell(y=0)·두 spinodal(y=+-1.0657) 수평 기준선 3개, gap=두 준위 수직 span, 과주행 방향 화살표 명시. 좌표: T3_calc.py(eq:Veq, Omega=4RT; xi_s+-=0.1464/0.8536, y_s=+-1.0657, gap 2.1314).
- T4 fig:barrier — 현행: 2패널 분리로 비대칭 대비 약함. 재설계: 단일 반응 hop 에 평형(점선)·구동(실선) 오버레이 — chi*A 분할이 한 TS 에서 fwd(dGa-chi*A)/rev(dGa+(1-chi)*A) 직독, detailed balance·dH_a^eff 주석. 보존: 두 골 개형·장벽·chi 분할. 좌표: T4_calc.py(raised-cosine G0/Gdrv; fwd 0.725, rev 1.075).
- T5 fig:flux — 현행: 직선 2개·교점 1개 정적. 재설계: 친화도 3-족 오버레이(r+ in {0.5,1,2}=e^{A/RT}) — 교점 xi_eq 가 reverse 대각선 위에서 1/3->1/2->2/3 이동, logistic 동치 시각화. 좌표: T5_calc.py(교점=r+/(r++r-)=1/3,1/2,2/3; logistic 항등 확인).
- T6 fig:logistic — 현행: 정규화 z 단일곡선으로 온도의존 붕괴. 재설계: 물리 (V-U_j)[mV] 축 + 3온도(268/298/328 K) 이중패널 — (a) xi_eq S-곡선+중심기울기 1/(4w), (b) 미분 종+FWHM=3.53w; w=n_j RT/F 온도의존 가시화. 보존: logistic·미분종·중심기울기 + 온도·물리축·기하의미 추가. 좌표: T6_calc.py(w=23.1/25.7/28.3 mV).
- T7 fig:reversal — 현행: 꼬리 곡선이 손그림(schematic). 재설계: 방전/충전 거울 2패널 유지, 꼬리를 실제 1차 저역통과(eq:lowpass)+격자 역전(eq:reversal)으로 계산, 진행(시간)·인과기억 화살표 추가. 보존: 평형종·거울·양수 peak + 실수치·인과방향 추가. 좌표: T7_calc.py(peak=(xi_eq-xi_lag)/L_V, L_V=1.2w; 방전 꼬리 V=+0.9·충전 -0.9 완전대칭, positive-only).
- T8 fig:widthbudget — 현행: 단일축 4곡선 과밀. 재설계: 위->아래 4단 누적 스택: 델타 -> (+)내재종(sigma_int) -> (x)앙상블(sigma_sym) -> (+)꼬리(L_V); 하단에 이전단 옅게 겹쳐 넓어짐·기울어짐 대비, 3척도 scale bar. 좌표: T8_calc.py(logistic-deriv x Gaussian x exp; sigma_sym=1.60 sigma_int, 면적 보존~1).

## 검증

- 컴파일: _check.tex(제공 _skeleton.tex 복사, 입력경로만 opus3-상대로 조정)로 8안 전부 xelatex halt-on-error exit 0 / bang-error 0. 본문 ref/eqref 는 스켈레톤 단독에선 (??) 로 렌더되나(경고 아님) 전체 문서 편입 시 정상 해결.
- 좌표 검산: 8개 T{n}_calc.py 모두 실행 성공(Python 3.12 + numpy 2.4.3). 곡선안(T3-T8)은 스크립트 인쇄 좌표를 그대로 tikz 에 사용 — 조작 0. 도식안(T1 노드-식 라벨, T2 전위 단조성/축 매핑)은 스크립트가 정합 assert.
- 시각 검수: 8안 130 dpi PNG 렌더 후 라벨-곡선·라벨-라벨 교차 점검 -> T1(루프라벨)·T2(축 과밀)·T3(과주행라벨)·T4(상단주석)·T5(중앙주석)·T8(연결화살표) 정정 완료. T6·T7 은 최초부터 청정.

## 파일 목록

- 그림: T1_spine.tex ... T8_widthbudget.tex (각 = tikzpicture + caption + label)
- 좌표 스크립트: T1_calc.py ... T8_calc.py
- 컴파일 확인: _check.tex (입력=T1_spine.tex 템플릿; 입력줄만 바꿔 8안 확인)
- 렌더 참고: img_T1..8_*.png (검수용)

## 채점 축 대비 자기평가

- 물리 정확(좌표 검산): 전 곡선안 식 수치평가·_calc.py 동봉으로 재현 가능. T7 은 종전 손그림을 실제 저역통과 계산으로 대체(정확도 상향).
- 전달력(한눈 물리): T1 분기·T2 전위정박·T4 단일hop 대비·T5 족·T6 온도의존·T7 인과방향·T8 누적서사 — 각 대상 핵심 물리를 한 시선에 읽도록 배치 재설계.
- 문건 정합·회색조: 캡션 기호·식참조 본문 정합, 색 미사용(선종·명도만) -> 인쇄 내성 확보.
