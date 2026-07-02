# FABLE 재검 — P4(v1.0.12 재작성) RESULT

> 세부계획 = `../../plans/2026-07-02-fable-reaudit-P4-v12-authoring-plan.md`(Decision Gate D1-D5 = GO 권고안 채택). 방식 = N=10 경쟁 작성(3S+3O+3C+1F, Fable 가중 3) → Fable 체리픽 → 검수 N종 union + 10차 재검 → Fable finalizer. 물리·화학 논리 무결 최우선(논문·특허 전제).

## Phase 4.1 (Decision Gate) ✅
D1 Eyring 현행 유지+서사 강화 / D2 §1.18 범위 밖 / D3 S0-S5 = FITTING_GUIDE 선별 복원 / D4 HIGH 2 정정 수행 / D5 ν 보수 유지+권고만 — GO 로 확정.

## Phase 4.2 (증판+위생·정정) ✅
- 4.2a: `docs/v1.0.12/` 증판 + 버전 라벨·헤더 위생(P-1·P-4·H-1 byte-claim 정정) — `fecf70c`.
- 4.2b: 정정 15건(★H-1 BW V_eq 부호 5연동·M-1 fig:staging·M-2 0.18→1.1 k_B 재귀속·M-4 ν=2 ~23% 정직 서술·M-5 꼬리수렴·M-6 우함수·M-8 선형화·M-9 축퇴 타당역 등) — fixer note = `V1012_P42b_fixer_note.md`, 빌드 0-err. fixer 범위 flag 2건(M-2 잔여 L509·L1745)은 master 직접 정정.

## Phase 4.3 (A항 HIGH 2 + C항 LCO 수식화 — N=10 파이프라인) ✅
- **작성 16파일**(F1/S1-S3/O1-O3/C1-C3×s1-s3) `f038104` — 529 파동 3회·Codex 큐 stuck 극복(재발진 규율).
- **체리픽 map v10**(Fable 가중 3, 손 재계산 PASS) `65531b5` — 6절 편입 LaTeX+H-2 문안+신규 적발 4건 §8 분리.
- **검수 10기 union** `bb0b33c` — 물리 불변 계약 10/10 PASS·체리픽 누락 실질 0·쟁점 클러스터 확정(`V1012_P43_review_UNION.md`).
- **10차 재검(verify10, 별세션 Fable)** = `V1012_P43_verify10.md`: B-1 F-1 확정 채택(6중 재유도) / ★B-2 방향규약 원자 판정 — **(i) f=+σ_d 정정 + 진행률 pairing 채택**(정합 pairing 유일해·(ii)는 F-2 채택 순간 클러스터 내 자기모순으로 기각·외부 실측 f=F/RT>0) / B-3 LCO Ω 지위 조건부 문구 / B-4 각 처분(F-4·고정점 heuristic·R-2·R-3·F-6·attribution 4건 기록) / 편입 gate 7종 확정.
- **finalizer(master 직접, 절별 루핑) 커밋 3분할**:
  - 커밋1 `242e2e8` — Ch1 5절(center→hys→peak→decomp→code) (a)-(d) 사슬 편입 + Ch2 H-2 ①②. 원자 결합 3건(§4(c)↔L1728 F-1 / F-2↔R-1↔F-5④ / 삽입점 A↔B↔xmap) 동일 커밋 충족.
  - 커밋2 `cf843fc` — M-fix F-4(충전 꼬리 "큰→낮은 쪽"+시간 중의성 병기, N8 한 구절만).
  - 커밋3 `a260290` — 코드 주석 f=+σ_d 동기화(동작 0: 회귀 exit=0·demo byte-IDENTICAL).
- **게이트 실측**: ① eq:lco-* 정의 28·중복 0·eq:msmr 1회 ② ref/cite/label 경고 0 ③ 부호 sweep — `(1-\xi)/\xi` 0건·`f=-\sigma_d` 단정 0(잔존 1건 = verify10 ④ 자신이 신설한 "직접 등치하면 뒤집힌 부호" **오류-경고 문맥** — gate 취지(단정 0) 충족, 허용 목록) ④ xelatex 2-pass 0-err(Ch1 41p·Ch2 14p) ⑤ 물리 불변 수치(+0.83/+80/−46/1.1k_B/0.47/1.49/8RT/3F/4958/25.7) 전부 잔존 ⑥ 불가침 hunk 0접촉(diff -U0 경계 실측: Ch1 8히든크 전부 승인 범위·Ch2 2헝크) ⑦ v9 기록(AUTHOR_BRIEF·FIX_LIST) 무수정 — verify10 §2 가 supersession 기록.
- 자구 조정 1건(기록): R-3 eq:lco-J 교체 후 후속 문장 "의 각 전이" → "각 전이"(식 말미 쉼표와의 문법 정합 — 내용 불변).

## Phase 4.4 (마감) ✅
- **샘플 이미지**: `sample_test_v1012.py`+`.png`(2×2 — 흑연 staging 분리 n=0.12·LCO MSMR·q_rev 이중축·ΔS_e 골 −45.68). glyph 경고 0(2회 실행 stderr 0)·결정론(PNG 해시 동일)·master 육안 검증 PASS(전 라벨 영어/ASCII·물리 개형 정합). 착수 시 stale v1.0.10 사본 발견 → v1.0.12 판으로 대체(원본 불가침).
- **FITTING_GUIDE v1.0.12**: D3 선별 복원(S0-S5 비순환 식별 사슬·보충 규정·울타리 16·잔차 진단표 — v5 §1.15 L1596-1705 원문 대조) + ★방향 규약 §0(LCO 충전↦direction=+1, F-2 실무 반영) + D5 ν≈8-10 권고(기본값 2.0 보수 유지) + B-3 LCO Ω 미배정 지위 + Phase A-E ↔ S0-S5 대응 명시.
- **INDEX.md**: v1.0.12 릴리스 블록 신설(5행)·1.0.10 블록 superseded 강등.
- 최종 점검(두 축): G-derive/follow = N=10 union 렌즈 + verify10 재검으로 커버(비약 0·전보체 0·코너 메인 승격 0) / 상호충실도 = 코드 주석·가이드·문건 f=+σ_d 3자 일치 + 회귀 13/13 + demo IDENTICAL.

## 이월 (P5 코드개정 후보 — 본 result 가 기록)
`_direction_to_sigma` 전극 인지 확장(전극 타입→탈리튬화 부호 환산) · 다온도 T² 곡률(동결 근사 해제) · 전자항 dict T1 재정렬 · ν 기본값 상향(승인 시·재베이스라인) · LCO Ω/dH_a round-trip 배정 · 장벽 분포 적분(울타리 ②).
