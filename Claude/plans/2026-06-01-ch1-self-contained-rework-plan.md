# Ch1 자기완결 재작업 + Ch6 해체 Plan (2026-06-01)

**트리거**: 사용자 검토 — Ch1 §7+ 가 부실(식이 뜬금없이 적분으로 등장·물리의미 불명·연결 부족, 따라갈 수 없음). Ch1만으로 심플 실데이터 피팅 근사식을 못 뽑음. 검수가 정확성만 보고 따라갈 수 있음/쓸 수 있음을 못 봄. 전문을 작은 청크로 쪼개 절별 빡센 검수 미반영.

## 1. 진단 (사실 확정 — 원천 대조)
재구성 rebuilt Ch1 §7+(spectrum/kernel/fiteq/falsify 4절)가 원천 consolidated_ch1 §7+(11절)의 실무·닫힌형 내용을 Ch6으로 이관·압축:
- **드롭/이관된 것**: §closure(Plan B + Plan A **eq:closed 닫힌형** 유도) / §ica 3-subsection 단계유도 / **§crate 0.2C 기준식**(eq:02c 실용 근사) / §tailT spectrum shift 상세 / §ident 식별성 / EMG 경험식.
- **결과**: Volterra 가 뜬금없이 등장(닫는 §closure 부재), fiteq 가 안 풀린 Volterra 의존(닫힌형 부재), 심플 근사식 부재(0.2C 드롭).

## 2. 목표
- **Ch1 자기완결**: §7+ 가 물리 동기(각 변수·적분의 의미) + 무비약 연결로 따라가지고, **끝에서 심플 실데이터 피팅 근사식**(0.2C 기준 + single-mode tail closed-form)이 명시적으로 나옴.
- **Ch6 해체**: 수치 solver·closure·C-rate·식별성·EMG 내용을 Ch1(주로)·해당 챕터로 흡수. Ch6 파일 제거(또는 빈 stub + 안내).
- 원천의 완전성 복원 + rebuilt 의 가독(display 식·step 라벨·grounding) 결합. 원천의 "줄줄이 나열" 단점은 개선.

## 3. 방법 (★ 재발 방지 = 사용자 핵심 지시)
- **절별 청크 작업**: §7~끝을 절 단위로 하나씩 재작성(전체 한 번에 X).
- **절별 청크 검수**: 각 절 재작성 직후, 그 절 본문만 범위로 적대검수 1회(따라갈 수 있나/쓸 수 있나/식 동기 충분한가 + 정확성). 전체 tex 한 번에 검수 금지.
- 각 절 = (a)물리 동기 prose 선행 (b)display 식 + step 라벨 (c)각 변수·적분의 \*의미\* 1줄 (d)무비약 연결 (e)grounding.
- 매 절 완료 = 부분 빌드 무결성 + 본 계획서 진행 체크.

## 4. 작업 단위 (절별, Ch1)
- **W1 §spectrum**: A_L(relaxation-length spectrum)의 물리 의미 명확화 — "각 완화 길이 L 을 갖는 mode 가 꼬리에 얼마나 기여하는가의 분포". ρ_G→A_L 변환의 의미. (현행 dense 박스 풀어 설명)
- **W2 §kernel → closure**: kernel integral 의 물리(단일지수의 연속중첩=관측꼬리) + Volterra 가 \*왜\* 자기참조인지(V_n↔Θ charge-balance 결합) 동기. **원천 §closure 복원**: Plan B(g-grid 직접적분, 항상 보존) + Plan A 닫힌형(단계0 선형화 b=−(Q_p/C_bg)∂Θ_eq/∂V_n → 단계1 ratio → 단계2 **eq:closed Θ_A=c/[1−∫Kb...]**) 무비약. JCP2017 Fredholm↔graphite Volterra 가정차 BOUNDED.
- **W3 §ica/dva**: 원천 §ica 복원 — 내부전위 미분(등온/비등온) → apparent 미분 → ICA/DVA(eq:icadva). monotone 제약.
- **W4 §fiteq (usable)**: fiteq 가 \*닫힌\* Θ_A 로 실제 계산되는 닫힌식임을 명시. 평가순서 S1~S6 + 피팅 파라미터.
- **W5 §tailT + crate**: spectrum shift(저T/고T/전위) 상세 복원 + **§crate 0.2C 기준식 복원**(eq:02c) + **single-mode tail 근사**(A_L=δ → Θ=Θ_0(1−e^{−q/L}), L=|I|/(Q_cell k) 로 데이터 직접 피팅 가능한 최단순 닫힌식) 명시 = 사용자 "심플 근사식".
- **W6 §falsify + ident**: 3계층 분해 + 원천 §ident 식별성(파라미터 제한 순서) 복원 + EMG 초기값.
- **W7 Ch6 해체**: 위 흡수 후 Ch6 잔여(순수 수치 DAE/solver 상세)를 Ch1 closure 의 "수치 평가" 보조로 축약 흡수 or 별도 부록 최소화. full 통합본·refs 재빌드.

## 5. Gate (절별, verifiable)
- G-follow(신규): 해당 절을 학부생이 앞 식+본문만으로 따라갈 수 있는가(적대 agent 재현). G-usable(신규): §fiteq/§crate 끝에서 실데이터에 대입 가능한 닫힌식이 명시됐는가.
- 기존: G-noleap(자명/clearly 0)·G-dim·G-ground(AL+DOI)·G-cross(CHARTER)·G-latex(빌드).

## 6. 산출
- `graphite_ica_ch1_rebuilt.tex` 개정(자기완결). Ch6 해체. full/refs 재빌드. result `RB_LEDGER_CH1_REWORK.md`. AL 보강분 등재.

## 7. 중단/결정
- 사용자 GO 후 절별 연속 진행. 0.2C 근사식의 정확한 형태(원천 eq:02c 채택)·Ch6 해체 범위(완전 제거 vs 최소 stub)는 권고값(원천 채택/최소 흡수)로 진행, 본문 평문 가정 명시.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-01 | 최초 — 사용자 Ch1 §7+ 부실 지적 + 원천 대조 진단 후 작성. |
