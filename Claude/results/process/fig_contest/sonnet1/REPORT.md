# sonnet1 제출 -- V1.0.14 P5.1 이미지 경연 (8/8)

노선: 정보 위계-주석 밀도 강화(각 노드/곡선에 대응 식 번호-수치를 명시 태그로 병기). 전 안 xelatex 0-err
확인(_check.tex, sonnet1/ 내부에서 상대경로로 각 파일 순차 \input). 공통 하우스룰(그림 내부 텍스트 영어
ASCII, 캡션 한글+본문 표기 정합, \label 유지) 준수.

## T1 -- fig:spine
- 의도: 기존 노드-화살표 스파인에 (a) 각 노드 아래 식 번호 태그(예: [eq:Uj]) 병기, (b) N7 이후 실제
  분기(식 eq:branch -- L_V<nu*Delta_grid 면 평형 peak 로 skip, 아니면 N8 꼬리)를 도식 그대로
  시각화, (c) 전이별 반복 루프(N2-N8)에 좌측 순환 화살표 + "repeat x N_p" 라벨.
- 좌표 근거: 순수 흐름도(노드-화살표)라 수치 곡선 없음 -- calc.py 불필요. 노드 내용-식 번호는 본문
  N0-N9 절 라벨(eq:n0map, eq:vn, eq:Uj, eq:Ubranch, eq:wbase/eq:xieq, eq:eqpeak, eq:Acut/eq:chid/eq:dHeff/eq:LV,
  eq:peakshape/eq:reversal, eq:sum)과 1:1 대응 확인(본문 grep 교차 검증).
- 컴파일: 0-err (xelatex, sonnet1/_check.tex 경유).

## T2 -- fig:staging
- 의도: 기존 갤러리 채움 도식(상단, 원안 유지 + 열별 점유 주기 라벨 "1:4->1:1" 추가)에 실제
  dQ/dV peak 4개(하단, 신규 축)를 연결. 위는 범주형 스케치, 아래는 실제 전위 축임을 캡션에 명시(정직성
  -- 3->2L / 2L->2 은 20 mV 차이라 갤러리 등간격에 선형 정렬 불가하다는 점을 캡션에 적음).
- 좌표 근거: T2_calc.py -- 식 eq:eqpeak(dQ/dV=Q_j*xi_eq(1-xi_eq)/w_j, gamma=0 초기상태이므로
  분기-꼬리 없는 순수 평형 종)을 표 tab:staging 의 U_j,Q_j,w_j(0.210/0.140/0.120/0.085 V; 0.10/0.12/0.25/0.50
  Q_cell; 0.020/0.016/0.014/0.012 V) 그대로 대입, V grid 0.02-0.27 V 에서 평가 후 3-포인트 서브샘플.
  피크 높이 Q_j/(4w_j) = 1.25/1.875/4.46/10.42 (실제 값, 정규화 없음).
- 컴파일: 0-err. (1차 렌더에서 상하 패널 겹침-범례 줄간격 버그 발견 -> yshift-범례 y-간격 재조정으로 해결,
  렌더 재확인 완료.)

## T3 -- fig:hysloop
- 의도: 기존 과주행 곡선에 (a) 방향 화살표 강조(이미 존재, 유지), (b) Maxwell 등면적선(y=0) 명시 라벨,
  (c) 분기 gap 실제 수치(약 54.8 mV, T=298.15 K) 주석.
- 좌표 근거: T3_calc.py -- 식 eq:Veq y=ln[xi/(1-xi)]+(Omega_j/RT)(1-2xi), Omega_j=4RT(본문
  그림 그대로의 case)로 61점 큐레이션 grid(양끝-spinodal 조밀) 계산. spinodal xi_s^+- = 식 eq:spinodal
  (u=sqrt(1-2RT/Omega_j)=sqrt(0.5)) 로 정확히 0.1464/0.8536. gap 은 식 eq:dUhys 닫힌꼴과 y-range*RT/F
  두 경로로 교차검산 -- 0.05476 V 일치.
- 컴파일: 0-err. (1차 렌더에서 라벨 3곳 상호 crossing 발견 -> anchor 재배치-leader 분리로 해결.)

## T4 -- fig:barrier
- 의도: 기존 손그림풍 이중 우물을 닫힌 함수형(사차 이중우물 + 구간선형 반응좌표 기울임)으로 대체,
  chi/(1-chi) 분할을 축 아래 괄호로 명시, N7 유효장벽 Delta H_a^eff=Delta H_a-chi_d*Omega 와의 연결을
  캡션에 명시.
- 좌표 근거: T4_calc.py -- G0(x)=Gmin+DeltaGa(1-u^2)^2, u=(x-x_ts)/2
  (닫힌 사차식, Gmin=0.10, DeltaGa=0.90), 구동 시 G(x)=G0(x)-A*h(x)(h=구간선형 반응좌표
  분율, h(xR)=0, h(x_ts)=chi, h(xP)=1). 검산: 정방향 장벽 = DeltaGa-chi*A=0.69, 역방향
  = DeltaGa+(1-chi)*A=1.29 -- 계산값이 eq:bv 관계식과 정확히 일치(스크립트 assert 아님, print 비교 확인).
- 컴파일: 0-err. (1차 렌더에서 (a)/(b) 캡션이 축 라벨과 겹침, chi 괄호가 축 라벨과 겹침 발견 -> y-오프셋
  재조정으로 해결.)

## T5 -- fig:flux
- 의도: 기존 2-직선 교점에 세 번째 affinity 케이스를 오버레이해 "A 변화 시 교점 이동"을 직접 시각화.
- 좌표 근거: T5_calc.py -- 식 eq:db r+/r-=e^(A/RT), r-=1 고정, A/RT=0,ln2,ln4 => r+=1,2,4. 교점
  xi_eq=r+/(r++r-)(eq:logisticsolve) = 0.5/0.6667/0.8 -- 직선 자체가 1차식이라 두 점(절편-절편)만으로 정확.
- 컴파일: 0-err. (1차 렌더에서 detailed-balance 수식 박스가 최상단 곡선과 교차 발견 -> 우상단 빈 공간으로
  이동, xi 축 눈금 "0.5" 와 정지점 라벨 "1/2" 겹침 발견 -> 라벨 y-오프셋 확대로 해결.)

## T6 -- fig:logistic
- 의도: 온도 268/298/328 K 세 곡선을 xi_eq(위)-미분 종(아래) 두 패널에 각각 오버레이, 중심 기울기
  1/(4w) 를 폭의 기하적 의미로 명시.
- 좌표 근거: T6_calc.py -- 식 eq:xieq xi_eq=1/(1+e^(-DeltaV/w)), w=RT/F(각 T), 미분
  dxi_eq/dV=xi_eq(1-xi_eq)/w. w(268/298/328K)=23.094/25.680/28.265 mV, 중심 기울기
  1/(4w)=10.825/9.735/8.845 V^-1. DeltaV in [-100,100] mV, 10 mV grid(21점).
- 컴파일: 0-err. (1차 렌더에서 x축 끝 라벨이 "100" 눈금과 겹침, 위-아래 패널 y-축 제목이 서로 겹침 발견 ->
  축 길이-패널 간 yshift 확대로 해결.)

## T7 -- fig:reversal
- 의도: 방전/충전 두 패널에 실제 이산 저역통과(격자 뒤집기 포함) 수치 결과를 그대로 표시 -- 손그림
  근사가 아니라 eq:lowpass 재귀식을 코드로 돌린 결과.
- 좌표 근거: T7_calc.py -- z=(V-U_j^d)/w_j in [-6,6], Delta z=0.1, L_V/w_j=1.5(widthbudget 절에서
  이미 쓰인 예시값과 통일), rho=e^(-Delta z/1.5)=0.9672. 방전은 z 오름차순 그대로 재귀식 적용, 충전은
  배열을 뒤집어 재귀식 적용 후 재역순(식 eq:reversal). peak =(xi_eq-xi_lag)/1.5 -- 방전 최대
  0.188 at z~1.2, 충전은 정확한 거울상(z->-z) -- 코드로 확인.
- 컴파일: 0-err. (1차 렌더에서 (b) 패널이 페이지 우측으로 넘쳐 잘림 발견 -> x-scale-xshift 축소로 해결.)

## T8 -- fig:widthbudget
- 의도: 기존 단일 축 3중 오버레이를 3-패널 서사(단계 화살표 "+2", "+3", "+1")로 재구성, 우측에
  sigma_int:sigma_eta:L_V 막대 인셋 추가.
- 좌표 근거: T8_calc.py -- 단계1 b1(z)=xi(1-xi)(logistic 미분, w=1), 단계2 같은 함수족 유효
  scale 1.6(sigma_eta=1.25*sigma_int, sigma_sym/sigma_int=sqrt(1+1.25^2)=1.6008),
  단계3 = 단계2 와 단측 지수 커널(L=1.5)의 수치 합성곱(사다리꼴 적분, Delta z=0.05). 결과값(peak
  0.25->0.156->0.137 at z~1)이 본문 그림의 값과 독립 재계산으로 일치(교차검증).
- 컴파일: 0-err. (1차 렌더에서 중대 버그 -- 단계 전환 화살표-인셋이 outer y=11cm 스케일을 그대로 물려받아
  실제 캔버스에서 수십 cm 밀려나 다른 패널과 뒤섞이고 인셋이 페이지 밖으로 이탈. 전환 화살표는 로컬 델타를
  1/11 스케일로 축소, 인셋은 별도 y=1cm 스코프로 분리해 해결 -- 재렌더로 정상 배치 확인.)

## 검증 로그
- 방법: fig_contest/_skeleton.tex -> sonnet1/_check.tex 복사, \input 경로를 T{n}_*.tex(접두어 없이,
  같은 폴더 내 상대경로)로 교체하며 8회 개별 xelatex 컴파일. PowerShell 에서 Select-String "^!" 로 에러
  라인 0건 확인 + pdftoppm 렌더 후 이미지 육안 검수(라벨-곡선 교차-페이지 이탈-텍스트 겹침 전수 점검, 위
  "1차 렌더" 메모가 실제 발견-수정한 항목).
- 최종 상태: T1-T8 전건 0-err, _check.tex 는 T1 을 가리키도록 기본 복원.
- 미해결/제약: 본문 라벨 참조(\eqref 등)는 스켈레톤에 해당 label 정의가 없어 (??) 로 렌더 -- 브리프 지시대로
  허용 범위(0-err 만 확인 대상).
