# opus1 — V1.0.14 P5.1 이미지 경연 제출 (8안)

작성자: opus1 · 노선: 물리 서사 극대화(그림 하나가 유도의 줄거리를 재현 — 단계 주석·인과 화살표·거울 구조).
공통: 그림 내부 텍스트 영어 ASCII, 캡션은 본문 표기 정합, 회색조 인쇄 내성(색 미사용 — 선종/그레이 레벨/화살표로만 구분),
\label 원본 유지, 곡선 좌표 = 식 그대로의 수치 평가(대상별 T{n}_calc.py 동봉·재현 가능).

## 컴파일 (전 안 공통)
- 하네스: _check.tex(= _skeleton.tex 프리앰블 + 8안 \input). 명령: xelatex -halt-on-error _check.tex (opus1 폴더에서).
- 결과: 0 error · 0 overfull hbox · 5-page PDF(_check.pdf). 미해결 경고는 \eqref/\ref(본문 라벨 — 스켈레톤에서 ?? 렌더, 브리프 허용)뿐.
- 렌더 육안 검수 완료(pdftocairo 130 dpi): 8안 전부 라벨-곡선/라벨-라벨 교차 0.

| 안 | 의도(서사) | 좌표 근거(식·계산) | 컴파일 |
|---|---|---|---|
| T1 fig:spine | 계산 진행을 세로 척추 + 전이별 반복 파선 블록으로. 블록 안이 두 갈래(방향 불변 평형 종 N6 / 방향 의존 인과 꼬리 N7·N8)로 갈렸다가 peak-shape 분기(eq:branch)에서 재합류 → N9. 각 노드에 결과식·산출량 병기. | 흐름 도식(곡선 없음) → calc.py 대상 아님(곡선 좌표 규정은 곡선에 적용). 현행 spine 물리 보존 + N6/N7/N8 분기 명시. | 0-err |
| T2 fig:staging | 위=stage 4→1 갤러리 채움(stage n=매 n번째, 2L 옅게)·양방향 화살표. 아래=실제 dQ/dV(V), 네 peak 에 전이·U_j 라벨(계단식+점선 leader). V 축 고→저(좌→우)로 stage 순서와 peak 순서 일치. | T2_calc.py: dQ/dV=Σ_j Q_j ξ_eq(1-ξ_eq)/w_j, ξ_eq=logistic((V-U_j)/w_j), U_j=0.210/0.140/0.120/0.085, w_j=0.020/0.016/0.014/0.012 (doc 초기값). eq:xieq·eq:eqpeak. | 0-err |
| T3 fig:hysloop | 얇은 전 구간 V_eq(ξ) 위에 방전(상승→ξ_s^-)·충전(하강→ξ_s^+) 준안정 과주행 굵은 화살표, y=0 Maxwell plateau, spinodal 상한 gap ΔU^hys 브래킷. | T3_calc.py: y=ln[ξ/(1-ξ)]+4(1-2ξ) (eq:Veq, Ω=4RT). ξ_s^±=½(1±u), u=√(1-2/4)=0.7071 → ξ_s^-=0.1464, y=+1.0657 (본문 좌표 일치), gap=2.1314. | 0-err |
| T4 fig:barrier | (a) 평형=대칭 이중골(찬/빈+이온, TS 장벽 ΔG_a). (b) 구동=선형 tilt 로 도착골 ↓A, 정상점 ↓χA → 정방향 ΔG_a-χA·역방향 ΔG_a+(1-χ)A 주석. 두 패널 분리. | T4_calc.py: G_eq=ΔG_a cos²(πx/2), G_drv=G_eq-A(x+1)/2 (ΔG_a=1,A=0.6,χ=½) → 정방향 0.70, 역방향 1.30 검증(eq:bv). | 0-err |
| T5 fig:flux | 정방향 r+(1-ξ) 3직선(r+=1,2,3) + 역방향 r-ξ, 교점 이동을 곡선 화살표+detailed balance 주석으로. 교점 라벨 ξ_eq=½,⅔,¾ 계단 배치. | T5_calc.py: ξ_eq=r+/(r++r-), r-=1, r+=e^{A/RT}=1,2,3 → 교점 0.5,0.6667,0.75 (eq:logisticsolve·eq:db). | 0-err |
| T6 fig:logistic | 2패널: (a) ξ_eq logistic 3온도, (b) 미분 종 3온도(저온=좁고 높음). 폭 w=nRT/F 온도 의존, peak 1/4w. 선종 268 파선/298 실선/328 점선. 제목 하단. | T6_calc.py: ξ_eq=1/(1+e^{-(V-U)/w}), dξ/dV=ξ(1-ξ)/w. 268/298/328 K → w=23.1/25.7/28.3 mV, peak 10.83/9.74/8.84 V⁻¹ (eq:xieq). | 0-err |
| T7 fig:reversal | 2패널 거울: (a) 방전 꼬리→높은 V, (b) 충전 꼬리→낮은 V. 점선=평형 종(방향 불변), 실선=꼬리 얹은 peak, 진행 화살표+인과 기억 방향. | T7_calc.py: 저역통과 점화식 ξ_lag[i]=ρξ_lag[i-1]+(1-ρ)ξ_eq[i], peak=(ξ_eq-ξ_lag)/L_V; 충전=reverse∘lowpass∘reverse(eq:lowpass·eq:peakshape·eq:reversal). 방전 peak V=+1, 충전 V=-1. | 0-err |
| T8 fig:widthbudget | 4단계 서사(델타→②내재 종→②⊗③ 분산 가법→+①단측 지수 꼬리) + 단계 화살표, 선종 범례, 세 척도(σ_int,σ_η,L_V) 막대 대비. | T8_calc.py: 내재 f2=(1/4w)sech²(x/2w); ②⊗③ 유효 scale 1.6w(σ_η=1.25σ_int); +① = f23∗단측 지수(L=1.5w, 수치 적분). 본문 수치 재현(내재 0.25, 광폭 0.15625; eq:widthbudget). | 0-err |

## 재현
각 T{n}_calc.py 를 python 으로 실행하면 tikz plot 좌표 문자열을 출력(그림 파일 좌표와 대조 가능). T1 만 흐름 도식이라 calc 없음.
