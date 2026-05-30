# 심층 재검토 Ledger — 물리적 논리 전개 기반 (부문별 + 통합)

**대상**: 합류 G1(Ch1)/G2(Ch2~4)/G3(Ch5~6) + 통합본.
**지시**: "각 부문별 10회 + 통합 10회 재검, 특히 물리적 논리 전개 기반 검토."
**성격**: 이전 10-pass(표현·grounding·빌드 위주)가 못 잡은 \*\*물리 전개 자체의 비약·숨은 전제\*\* 발굴. 매 수정 후 xelatex 빌드 확인. **일자**: 2026-05-29.

---

## 발견·수정 (물리 논리, 빌드 검증 완료)

| # | 심각도 | 위치 | 물리적 비약/빈틈 | 수정 |
|---|---|---|---|---|
| **P-CRIT-1** | HIGH | G1 §rate→§kernel | `eq:single_kernel`은 \*\*잔차 `r`\*\*의 거동인데 `eq:kernel_integral`은 \*\*진행률 도함수 `dΘ/dq`\*\*의 중첩 — 둘을 잇는 `dξ/dq=r/L` 단계 생략 → kernel의 `1/L` 인자 출처 불명(비약) | `eq:single_dxidq` 신설($d\xi_j/dq=(r_a/L)e^{-(q-q_a)/L}$); kernel 절에서 "1/L 출처=진행률 도함수" 명시 |
| **P-HIGH-2** | HIGH | G1 §spectrum | `A_L=ρ_G(G(L))·RT/L·A_0`에서 \*\*변수변환 밀도보존\*\*(`A_L dL=ρ_G dG`) 논리 생략 → Jacobian이 "곱해지는" 이유 비약 | 질량보존 명시; `dG/dL=RT/L>0` 단조성→일대일(역변환 유일) 단서; `A_0≡1`서 규격보존 |
| **P-MED-2b** | MED | G1 §rate | `eq:single_kernel`의 $L$=상수가 `dξ_eq/dq≈0` \*\*뿐 아니라\*\* `d𝒜/dq≈0`($V_n$ 완만)도 요구함이 누락(숨은 전제) | 별개 가정 2개 명시; $V_n$ 급변 시 $L=L(q)$+직접적분 |
| **P-MED-3** | MED | G2 §reconcile | "detailed balance 만족하면 ξ_ss=ξ_eq"가 \*\*동어반복\*\* — \*언제\* Level B가 thermo eq에서 DB를 만족하는지(물리 조건) 누락 | 두 조건 명시: (i)$\Pi^0=1$, (ii)$V_{n,drive}=V_n$(과전압 0); Level A↔B \*\*차이 크기 = $\eta_{drive}$\*\* |
| **P-MED-4** | MED | G2 §levelB | 병목이 forward/backward에 \*\*비대칭\*\* 삽입 시 `r⁺/r⁻` 변→detailed balance 충돌 (원본 (B) Ch3 경고였으나 합류본 누락) | boundbox 추가: 병목이 (a)mobility 전체/(b)방향 flux 중 어디 작용인지 명시 의무; 평형근방=미세가역성→대칭, 비대칭은 강구동서만 정당 |

---

## 부문별 10관점 점검 결과 (요지)
\*\*G1(Ch1)\*\*: ① 잔차↔진행률(P-CRIT-1✔) ② 변수변환 보존(P-HIGH-2✔) ③ post-peak 전제 분리(P-MED-2b✔)
④ Marcus bound 유효범위 PASS ⑤ k_lim 직렬(전 검토 R9-G3) PASS ⑥ 단조성↔root 유일 PASS ⑦ 빠른-kinetics 극한(M4) PASS
⑧ 차원 PASS ⑨ non-uniqueness forward-only PASS ⑩ 피팅식 평가순서 PASS.

\*\*G2(Ch2~4)\*\*: ① keystone 일치조건 정밀화(P-MED-3✔) ② 비대칭 병목 vs DB(P-MED-4✔) ③ $(\mathcal J^+-\mathcal J^-)\ln(\cdot)\ge0$ 단조성 PASS
④ R3-1 effective-width 정합 PASS ⑤ 가역열 double-count 금지 PASS ⑥ $dV_{app}/dT$ 금지 PASS ⑦ Schnakenberg grounding PASS
⑧ log floor=domain guard PASS ⑨ Level B→비가역열 정당화 PASS ⑩ 부호 convention PASS.

\*\*G3(Ch5~6)\*\*: ① branch-local DB에 R3-1 적용 PASS ② metastable≠true-eq(Dreyer) PASS ③ ΔV_obs≠ΔV_hys PASS
④ dynamic vs OCV root 도함수 PASS ⑤ Plan B reference/Plan A dossier caveat PASS ⑥ broad-kernel 열화 PASS
⑦ χ vs η_ct 분리 PASS ⑧ hysteresis heat≠loop area PASS ⑨ Prony $a_\ell\ge0$ PASS ⑩ 확장순서(방전 먼저) PASS.

## 통합 10관점 점검
장간 기호/keystone 전파(P3-6) PASS · $V_{n,drive}$ 정의 일관(P-MED-3로 강화) PASS · $\Theta$↔$\xi_j$ 연결(전 검토 R9-1) PASS ·
단일 preamble 중복정의 0 PASS · 미정의 cite/ref 0 PASS · 중복 label 0 PASS · 빌드 4문서 에러 0 PASS ·
TOC/상호참조 안정 PASS · 폰트 대체 경고만(무해) · PDF 생성(G1 9p/G2 8p/G3 7p/full 25p) PASS.

## 사고(incident) 기록 — 작업 중 파일 손상·복구
편집 중 G1 일부 라인이 손상(표시 아티팩트 텍스트 혼입)됨을 \*\*빌드 에러로 즉시 검출\*\* →
`git checkout HEAD -- G1`로 마지막 정상본 복구 → 3개 물리편집을 \*\*하나씩 빌드 확인하며\*\* 재적용.
교훈: 매 편집 후 빌드 게이트가 손상을 조기 차단. (최종 G1 손상흔적 0 확인.)

## 사고(incident) 2 — 빌드 깨진 채 커밋(a1383b6) → 즉시 핫픽스
초판 커밋에서 (i) P-MED-4 가 G2 에 `\xi_\ss` 사용(G2 엔 `\ss` 미정의 → 컴파일 에러),
(ii) P-MED-3(reconcile 정밀화)가 `file modified` 충돌로 \*\*미적용\*\*된 채 커밋됨.
핫픽스: G2 `\ss`→`\mathrm{ss}` 2곳 교체, P-MED-3 재적용, body 재생성, 4문서 재빌드(에러 0) 확인.
교훈 보강: \*\*커밋 직전\*\* 전체 빌드 게이트를 반드시 통과(이번엔 일괄 빌드를 커밋 후 확인하는 순서 오류).

## 결과
- 물리 논리 비약 \*\*5건 발견·전부 수정\*\*(HIGH 2/MED 3), CRIT 0 잔존.
- 4개 문서 xelatex 에러 0 재확인(G1 9p/G2 8p/G3 8p/full 26p), 미정의 참조 0. keystone 전파·N-1/N-2/N-4 유지.
- 핵심 성과: tail 엔진의 \*\*잔차→진행률→spectrum→kernel\*\* 사슬이 이제 학부 수준 무비약(GS-1)으로 닫힘;
  Level A↔B 차이가 \*\*kinetic 과전압 $\eta_{drive}$\*\*로 정량화됨; 비대칭 병목의 DB 충돌 경계 복원.
