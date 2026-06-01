# Chapter 1 §7–§11 보강 검토 결과 (이식부 봉합선 복구)

- 일자: 2026-06-01
- 대상: `Claude/docs/_body_ch1_v2.tex` (Chapter 1 본문; 통합본·단독본 양쪽이 `\input`)
- 계기: 사용자 지적 — "§7(=7번째 섹션)부터 신규 변수가 정의·용도 설명 없이 등장하고,
  적분 유도가 단계 생략된 채 진행되어 논리를 따라갈 수 없다. Chapter 1만으로 실데이터
  피팅 근사식을 만들 수준이 아니다."

## 진단 (사실 확인 결과)

- §1–6: 무비약(GS-1)으로 작성됨 — 문제 없음.
- §7 제목이 "((A) 엔진 이식)" — relaxation-length spectrum/kernel/closure 기계장치를 다른
  계보에서 이식한 봉합선. 이식부 연결 유도가 비어 4개 결함 누적:
  1. `A_0(L)` 가 "per-mode amplitude·population weight·accessibility" 3개 명사만 붙고
     정의식·단위·결정법 없는 catch-all.
  2. 장벽 `G`(§5) ↔ `g`(§7 적분) 표기 혼용, 관계 미명시.
  3. per-class 해(eq:single_dxidq) + 인구평균(eq:xi_dist) → kernel 적분(eq:kernel_integral)
     의 치환·합산 사슬 생략 ("r(q_a)는 A_0에 흡수" 한 줄로 덮음).
  4. §8 1-시점 tail 적분 → §9 2-시점 Volterra 승격의 단계 비약.
- 추가: prefactor 표기 `k_0(T)` vs `ν_j(T)` 불일치.
- §11: 평가 순서만 있고 실측에 바로 맞출 명시적 근사 함수형 없음.

## 보강 내용

- §7: `g`=`G`의 적분 더미임 명시 / per-class ODE(eq:xi_class_ode)와 인구평균(eq:xi_dist)
  연결 / barrier→length 매핑(eq:L_of_G, 표기 `ν_j` 통일, `k_0≡ν_j`) / 질량보존 Jacobian
  (eq:massconv) → 정규화 인구 spectrum φ_L(eq:popspectrum) / A_L=φ_L·A_0(eq:spectrum)는
  A_0 정의를 §8로 명시 연결.
- §8: S1–S5 5단계로 kernel 적분 완전 유도 — 전하보존 정의(eq:theta_from_classes) →
  q-미분(eq:dtheta_step) → per-class 해 대입(eq:class_dxidq) → g→L 변수변환
  (eq:tail_derived) → **A_0 정체 확정(eq:A0_def: 용량가중·잔차·accessibility 곱, 무차원,
  자유 knob 아님)** → eq:kernel_integral. single-mode 극한 일치 점검 포함.
- §9: §8(정지 target)→Volterra 일반화를 Duhamel(변수변환 적분) 단계 + charge balance
  self-consistency 단계로 명시.
- §11: 최소 피팅 함수형 추가 — L_φ,j(eq:Lphi_fit), dQ/dV 최소모델(eq:minfit, EMG 유사
  but 파라미터가 물리량이라 전 T·I 동시 fit), 실데이터 추출 절차 F1–F5(sec:minfit).

## 검증

- xelatex 빌드: 단독본 `graphite_ica_consolidated_ch1.tex` exit=0, 19쪽.
- 마스터 통합본 `graphite_ica_consolidated_full.tex` 3-pass exit=0, 64쪽,
  미해소 reference 0 / citation 0 / 에러 0.
- 신규 라벨(eq:massconv, eq:popspectrum, eq:A0_def, eq:Lphi_fit, eq:minfit,
  eq:class_dxidq, eq:theta_from_classes, eq:dtheta_step, eq:tail_derived,
  eq:xi_class_ode, sec:minfit) 전부 해소.

## 남은 추가 후보 (미수정, 보고만)

- spectrum 폭 σ_j 도입 시 log-normal length-mixture 의 닫힌 근사(stretched tail) 명시식.
- Plan A(Refs 6/7) closed-form 의 Plan B(g-grid) 대비 ε 수치검증(Ch6 범위).
- §10 ICA/DVA 의 D Θ_tail/dQ ↔ §8 결과 연결을 §8 보강에 맞춰 한 번 더 점검(현재 참조 정합).
