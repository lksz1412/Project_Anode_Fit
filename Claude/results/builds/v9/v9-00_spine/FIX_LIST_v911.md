# Ch1 v9-11 — adversarial 재검수 fix-list (v9-10 → v9-11)

> A1/A2/A3 결함 누적. master 삼각검증 후 v9-11 에서 정정. CRIT/HIGH 우선.

## A1 물리·유도 ✅ (CRIT/HIGH 0 — 물리 견고. MED 4)
- **F1 (MED)**: c_e→S_e 유도에 g(E)≈g(E_F) 동결 가정 미명시(점프) → "g(E) 를 E_F 근방 상수로 근사(Sommerfeld 표준)" 한 문장 추가.
- **F3 (MED·구현)**: nodemap N5+·L1437 코드 plug-in 이 자리당 eq:dSe 참조 → **몰당 eq:dSemolar 로 정정**(N_A배 오류 방지).
- **F8 (MED·가장 약한 곳)**: 이중계산 B 논증이 config 내부만 — T1 MIT 에서 config(자리점유)·ΔS_e(밴드 전자) **가법 직교성**(다른 자유도라 독립 가산·잔차 0) 한 문장 명시 → 피팅 시 측정 ΔS 초과 방지.
- **F2 (MED)**: S_e tier 라벨이 식형(A)/anchor(A 단일점)/연속곡선(부재) 3층 뭉갬 → tier 분리 표기.

## A2 부호사슬·흑연 ✅ (CRIT/HIGH/MED 0)
- 흑연 byte-동일(diff 제거 0·헤더 4줄만 치환)·부호사슬 PASS·graft 봉합 PASS(dangling/orphan 0)·단/전셀 분리 PASS.
- **A2-L1 (LOW)**: MSMR eq:msmr↔eq:xieq 동형서 방향인자 f↔−σ_d 대응 명시 생략 → 한 줄 추가.
- **A2-2 (권고)**: T1 MIT 부호 공존(verifybox ΔS_rxn^cat≈+80>0 vs ΔS_e<0) — "전자항은 ~1.5 J/mol·K 소수 음의 보정, 총 부호 불변" 한 줄 보강(오독 방지).
## A3 인용·빌드·완결 ✅ (CRIT/HIGH 0)
- 인용 8건 V2 마스터 정확·fabrication 0·+0.83=swiderska·MSMR ECS Adv·Teichert 완전·dangling 0·undefined 0·한글 0·흐름 정상·tier 정직.
- **A3-1 (LOW)**: line 1485–1488 Overfull 22.6pt(조판) → 정정(>20pt 유일).

## 정정 원칙
base=v9-10 복사→v9-11, CRIT/HIGH 전수 정정 + MED 가능한 한, 흑연 verbatim 유지, 정식 10회 후 xelatex 0-error.
