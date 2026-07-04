# V1.0.14 P5.1 이미지 경연 -- sonnet3 제출 보고

노선: 교과서 삽화 전통(Newman-Bard & Faulkner 류 -- 곡선 가족, 점근선, 기하 보조선, 영역 음영으로
물리가 말하게). 대상당 1안, 8/8 제출. 문건 원본(graphite_ica_ch1_v1.0.14.tex)은 읽기만 했고
수정하지 않았다. 좌표 조작 없음 -- 모든 안이 T{n}_calc.py 의 식 수치 평가 출력을 그대로 옮긴
좌표를 쓴다.

## 검증

sonnet3\_check.tex(스켈레톤 사본)에 8안을 각각 \input 해 xelatex 로 개별 컴파일, 각각의 로그를
_check_T{n}_*.log 로 보존했다. 8/8 전부 exit code 0, 로그 내 "! " 오류 라인 0건(0-err 확인 완료).
\label 은 전부 기존 라벨 유지(fig:spine 등), 그림 내부 텍스트는 전수 영어 ASCII(tikzpicture 본문에
비-ASCII 문자 0건, awk+grep 으로 8파일 전수 재확인 -- 캡션만 한글).

## 대상별 개선 요지

- T1 (fig:spine) -- 각 노드 옆에 대응 식 번호 배지(표 tab:nodemap 과 1:1 대응, T1_calc.py 가 그
  대응을 전수 검증), 전이별 반복 루프를 실선 상자 + "iterate j->j+1" 순환 화살표로, N5 이후 분기
  (평형 peak 직행 vs 지연 길이->인과 꼬리)를 결정 노드로 명시화(식 eq:branch, nu=2 문턱의 약 23%
  불연속도 계산 재현).
- T2 (fig:staging) -- 기존 갤러리 채움 도식(구조 정보 그대로 보존)에 진짜-축척 전위 축을 추가, 표
  tab:staging 의 U/Q/w 초기값으로 실제 dQ/dV peak(eq:belliden 종, 높이 Q_j/4w_j)를 얹어 스키매틱
  균등 칸 배치와 실제 불균등 전위 간격의 차이를 점선 연결선으로 드러냈다(3->2L, 2L->2 겹침이 자연히
  보임).
- T3 (fig:hysloop) -- 기존 Omega=4RT 곡선은 그대로 두되, 표에 실재하는 가장 작은/큰 Omega/RT 비
  (4->3, 2->1)를 같은 식으로 평가한 곡선 가족을 추가해 gap 이 Omega 와 함께 커짐을 보이고, Maxwell
  전위선과 gap 수치(2.131 RT/sF)를 명시.
- T4 (fig:barrier) -- 기존의 freehand 곡선을 없애고, eq:bv 가 지정하는 우물, 장벽 높이를 잇는
  명시적 raised-cosine 보간(T4_calc.py, 형태 함수까지 공개)으로 대체. chi:(1-chi) 분할을 반응좌표
  축 치수선으로 시각화하고, Delta H_a^eff = Delta H_a - chi_d*Omega(다른 절의 관계식)와의 연결을
  곁상자로 명시.
- T5 (fig:flux) -- A=0 / RT ln2(기존) / RT ln4 세 사례를 공통 총속도 규격화 하에 오버레이, 세
  교점이 eq:logisticsolve 닫힌 꼴과 정확히 일치함을 T5_calc.py 로 검산, detailed balance 식을
  곁상자로 명시.
- T6 (fig:logistic) -- 기존 그림은 무차원 z 축이라 온도 의존을 전혀 못 보였던 구조적 한계를
  지적하고, 실제 전위 축(mV)에서 268/298/328 K 세 폭을 두 패널(logistic, 미분 종)로 분리해 실제로
  다른 곡선으로 그림. 중심 기울기 1/(4w)의 기하적 의미를 접선으로 시각화.
- T7 (fig:reversal) -- 기존 freehand 곡선을 없애고, eq:lowpass 점화식을 미세 격자(1 mV)에서 실제로
  돌려 방전/충전 두 peak shape 를 얻음(eq:reversal 격자 역전 포함). 충전이 방전의 정확한 거울상임을
  1e-14 수준까지 수치 검산.
- T8 (fig:widthbudget) -- 기존 3-겹침 단일 패널을 4단(델타->②->②(x)③->+①) waterfall 로 서사화,
  ②(x)③ 을 본문의 "같은 함수족 shortcut" 대신 실제 Gaussian 수치 합성곱으로 계산 -- 분산 가법은
  정확히 일치하지만(sigma_sym=2.90w_j, 피타고라스), shortcut 의 logistic 종 peak 이 실제보다 약
  10% 높다는 점을 정직하게 캡션에 보고(분산 vs 모양 근사의 한계 구분). ①꼬리는 T7 과 동일한
  저역통과 재귀로 계산해 두 그림의 수학을 통일.

## 파일 목록

T1_spine.tex ... T8_widthbudget.tex + 동명 _calc.py 8쌍, _check.tex(검증용 스켈레톤 사본),
_check_T1_spine.log ... _check_T8_widthbudget.log(개별 컴파일 로그, 0-err 증거), 본 REPORT.md.
