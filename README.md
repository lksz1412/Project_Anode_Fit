# Project_Anode_Fit

리튬이온전지 흑연 음극의 ICA(dQ/dV) · DVA(dV/dQ) 동역학 기반 해석 및 피팅 프레임워크.

## 구조

- `docs/` — LaTeX 작업 문건
  - `graphite_ica_dynamic_ver5.tex` — 마스터 문건. 내부에 `ver.1 기본식` ~ `ver.5 히스테리시스` 5개 블록 (사실상 Chapter 1~5)
  - `graphite_ica_charge_balance_ver1_rechecked2.tex` — Chapter 1 (기본식) 재작성판. 전하 보존식 기반의 내부 전위 결정 흐름 도입
- `_local_only/` — 공개 추적 제외 (저자 본인 논문 PDF · 손글씨 노트 사진 등)

## 현재 작업 방향

1. ver5 마스터의 Chapter 1 골격을 유지한 채, ver1_rechecked2 의 전하 보존식 흐름으로 디벨롭
2. ver1_rechecked2 에 남은 self-consistent 되먹임 변수 문제는 본 저자의 JCP 147 (14) 144111 (2017) 의 ref 6, 7 적분식 해법을 응용해 해결
3. Chapter 2~5 인계 (`ver.N 으로 전달되는 기준식`) 정합성 유지
