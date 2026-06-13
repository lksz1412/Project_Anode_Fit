# Ch1 v3 — X pass (코드 절 개편·절간 다리·특수 케이스 회수·그림 재설계) Plan

## Summary
8차 피드백 6건: (1) Fig3(mudecomp)↔Fig5(isofamily) 중복 — 이미지 구성·퀄리티 전면 재투자,
(2) 절→절 전환부 논리 점프(앞 절 결과가 식으로 이어지지 않음), (3) PDF 렌더 검수 부족 — 강화,
(4) 일반식→가정·극한·코너 케이스 입증 패턴 부족, (5) §1.17 코드: 주석 과다(본문 문단으로)·
타자기 폰트(가독 모노스페이스로)·폭 70%(좌우 활용·두 줄 나눔 제거), (6) 수식 친화 독자 — 방향 유지.

## Phase Range (우선순위 순)
X.1 코드 절 전면 개편 → X.2 절간 다리 17곳 → X.3 특수 케이스 회수 블록 → X.4 그림 재설계
→ X.R 검수(시각 고해상 전수 포함, 수렴까지).

## X.1 코드 절
- 폰트: fontspec \setmonofont{Consolas}(Windows 표준) — verbatim 가독성.
- 폭: 코드 줄 제한 68→~96자로 올리고 두 줄 나눔 합치기(재포맷). \footnotesize 유지로 본문 폭 채움.
- 주석: 인라인·docstring 을 핵심 식별자((1.x)/M/S 한 줄)만 남기고 대폭 축소 — 설명은 §1.17 본문
  문단으로 이전(수식-본문-코드 3중 중복 제거).
- 동반: graphite_ica_model.py 재작성(동작 불변 — run_example 수치 동일 검증), verbatim 재동기,
  comment_gate 템플릿 재설계(남는 주석 기준), diff 게이트.
## X.2 절간 다리
- 17개 절 도입부 표준화: 첫 문장이 앞 절의 결과식 번호를 명시적으로 받아 출발("식 (1.x) 가 ~을
  닫았다. 이번 절은 그 식의 ~를 연다"). 점프 심한 곳 우선(피드백: 절 전환 전반).
## X.3 일반식→특수 케이스
- 주요 결과식 6–8곳 직후 case 회수 display/박스: 일반식이 알려진 특수 결과(이상 극한·코너)를
  재현함을 식으로 — eyring(ΔG→0)·logistic(Ω=0 회수는 기존)·memory(L→0/∞)·master(r_a→0·
  |I|→0)·hysmaster(Ω≤2RT·γ→0·σ_d 대칭)·superpose(δ)·keff(𝒜≫RT) 중 미비점.
## X.4 그림
- mudecomp↔isofamily 통합 재설계: mudecomp 는 "몫 분해" 패널(성분 정보 — isofamily 에 없음)로
  차별화하거나 2패널 한 그림으로 합치고 본문 결속 재정렬.
- 기존 6종(isofamily·doublewell·kernel·anatomy·fusion·vdwloop) 축 눈금·정량 라벨 일괄.
- 전 그림 스타일 통일(선굵기·폰트 크기·패널 라벨) — 렌더 고해상 검수 의무화(매 그림 변경 직후).
## X.R 검수
확립 체계 — 신규분 전담 검수→Codex→시각 고해상 전수(이번 지적 반영: 매 단계 렌더 확인을
gate 화)→fresh 수렴.

## Gates
build/comment/diff/run + ★렌더 게이트(변경 그림·코드 페이지는 커밋 전 반드시 렌더 확인) + 커밋·푸쉬.

## Assumptions
"ㄱㄱ" = GO — 무중단. 코드 동작·수치 불변 원칙 유지. v2 동결.

## Correction History
(없음)
