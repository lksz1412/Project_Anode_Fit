# V1.0.15 P3 RESULT — Ch1 이산 전압 격자 완전 퇴출(점별 연속 메모리 적분) + 승인 물리수정

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P3(Steps 9–14). 방법 = 검증 모델(theory-first) + 스킬 `competition-cherrypick-authoring` N+N+1+1(9,9,1,1). Fable 불가 → 드래프터 N=9(Sonnet 3 + Opus 3 + Codex 3)·체리픽/통합/최종/재검 = Opus(master). 대상 = `docs/v1.0.15/graphite_ica_ch1_v1.0.15.tex`. 상태 = ✅ 완주(수렴).

## 1. 목표 (사용자 확정)
균일 "작업 전압 격자"(리샘플→1차 저역통과 점화식→역보간) 아키텍처를 **아키텍처에서 완전 제거**하고 모든 평가를 점별(pointwise)로. 인과 꼬리는 연속 메모리 적분의 점별 수치 적분으로 직접 얻고, 평형 종은 그 $L_V\to0$ 해석적 극한(분기·스위치 원천 불요). 세 최우선 원칙 = ①교과서 register ②논문 깊이 ③수식-주도.

## 2. 산출 (Deliverable)
- `docs/v1.0.15/graphite_ica_ch1_v1.0.15.tex`(+.pdf) — 격자 퇴출·점별 재작성 통합본. 58p.
- 신설 라벨 4종: `eq:memory`(인과 메모리 승격)·`eq:lag`(부분적분 유도, 중간식 노출)·`eq:tail-limit`($L_V\to0$ 치환+지배수렴 극한)·`eq:reversal`(충전 방향 반전).
- 제거 라벨 3종: `eq:branch`(ν 스위치)·`eq:vwork`(작업 격자)·`eq:lowpass`(이산 점화식) — dangling \eqref 0.

## 3. 방법 실행 (9,9,1,1)
- **① 9 드래프트**: §1.3(N1)·§1.9(N8) 재작성 독립 경쟁(Sonnet 3·Opus 3·Codex 3, Agent 무통신). 전 드래프터 전체 문건 정독·목소리 체화 후 재작성. 공유 사양 = `V1015_P3_AUTHOR_BRIEF.md`(목표 물리·세 원칙·KNOWN_DEFECTS D1–D6·출력형식).
- **③ 체리픽 통합(Opus)**: base = D-S2, graft = D-S1(0/0 해소)·D-O1(도입 다리). 체리픽 §1.9 = `V1015_P3_cherrypick_sec19.tex`. 체리픽 비교 베이스에 v1.0.14(Fable 근접 정답) 포함.
- **정합 갱신**: spine(branch-select 노드 제거·N6–N8 단일 꼬리)·sec:sum(제목 "합산 (N9)"·역보간 제거·미분 사슬 노출)·staging 주석·LCO 방향(격자→적분 방향 반전)·R3/R5 재유도·keybox 6단계·tab:nodecode(N6/N8/N9 점별)·tab:inputs(격자 param 3행 삭제)·tab:symcode(V_app→배열)·body 기호표.
- **② 방향성 보완/검토2**: 별도 라운드 대신 ④ adversarial 재검수로 통합(스킬 §4.1 검증 모드 + §3 N회 가변청크).

## 4. 승인 물리수정 (P2 Decision Gate, 박사 승인 "권고대로 반영")
- **P2-1**(Sommerfeld 유효경계): "g'(k_BT)² Mott 항" → 고정 $E_F$서 s(ζ) 짝함수로 g' 상쇄, 첫 보정 $\tfrac12 k_B g''(E_F)(k_BT)^3$; 고정 조성 x서 μ(T) 이동이 같은 차수 g'²/g 항 공존(둘 다 O(T³)); Mott는 transport 소관. 상대크기 O[(k_BT/E_F)²] 무시가능.
- **P2-3**(verifybox +80 라벨): "+80 = config+vib+elec 세 성분 합" → "+80 = MIT 창 밖(elec≈0) config+vib 기저" 재규정 → 창 중심 −46 더해 +34, 창 밖 +80. 이중차감 오독 제거.
- **P2-4**(vib T-무관 전제, Ch1분): "T² 곡률=전자 신호" 식별이 config 엄밀 T-무관 + vib 상수 전제 위에 섬을 명시. vib T-무관은 고전극한 $k_BT\gg\hbar\omega$ 근사(LiCoO₂ 포논 수백 K → 300 K 준양자, 잔여 T-의존 소량); 다온도 곡률 피팅서 vib 잔여가 전자 신호에 섞일 수 있음. (Ch2 §vibel분은 P4.)
- **P2-2**(two-phase config caveat) = P4 소관.

## 5. 검수 (④ adversarial 재검수, 방법론 §3 N회 가변청크)
- **라운드 1(3 렌즈 병렬, Agent)**: (A)물리·수학 적대검산 [Opus] (B)격자 퇴출 정합·orphan [Opus] (C)문체·D1–D6·G-follow/usable [Sonnet]. refute+가장약한1곳+빈통과금지.
  - **확정 물리 결함 4건**(master 직접 재유도 확정): **F1[HIGH]** eq:tail-limit·R5가 `σ_d·ξ_eq(1−ξ_eq)/w`로 닫음→충전서 음수·R3 모순 → 방·충전 양쪽 `|dξ_eq/dV|=ξ_eq(1−ξ_eq)/w`(σ_d 불변)로 통일. **F2[MED]** DCT 지배함수 상수 1/(4w)(적분발산)→적분가능 `e^{−t}/(4w)`. **F4[MED]** P2-1 μ(T) 오귀속(고정 x서 g'²/g도 O(T³) 공존)→정정. **F5[LOW]** 보정항 외곽 k_B 누락→추가.
  - **D1 changelog-메타 누출 4건**(렌더링 텍스트): R5 "(구판 감사 결함 코드 D-PEAK)"·fig:reversal 캡션 "이전 판…P6 소관"·fig:relaxode 캡션 "P6 소관"·park2021 bib "구판의 제목 오기 정정" → 전건 삭제.
  - **정합/문체 8건**: GRID-RESID(fig:lco-dirmap "no grid reversal"→"no reversal")·tikz orphan(branchstage/sel 스타일 삭제)·eq:sum assert-jump(미분 중간식 추가)·D2 "가정이 아니다(전제)"→긍정·★ subsection 제목→인라인·"역보간 없다" 대조어법 2곳→긍정·"정직하게"→"수치로"·staging ≈80 중복 정리.
- **라운드 2(수렴 검증, fresh Opus)**: 5개 수정 지점 전건 독립 재유도 PASS(mid→box 부호도약 없음·DCT e^{−t}/(4w) 정당·R3/R5 σ_d 불변 일관·P2-1 k_B+μ(T) g'²/g·eq:sum 미분사슬 2경로·충전 분기 같은 양의 종). **새 결함 0 → 수렴.**

## 6. Gate (검증 명령·증거)
- **격자 grep 0**(렌더링 텍스트): 작업격자·Δ_grid·ν·저역통과·이산 점화식·역보간·23% 점프·모드 스위치·"no grid" 잔존 0. 물리 용어(격자기체 lattice gas·격자진동 phonon·초격자·결정 격자 삽입자리)는 보존. `%` provenance 주석(L38/41/43 D-PEAK)은 비렌더링이라 대상 외.
- **dangling ref 0**: eq:branch·eq:vwork·eq:lowpass \eqref 0. 신설 4라벨 전부 도입(앞)+사용(뒤) orphan 0.
- **빌드 GREEN**: `xelatex` 2-pass exit 0 / undefined ref·citation 0 / Overfull >10pt 0 / **58 pages**. (기존 <7pt overfull 7건 = provenance 주석·기호표 등 기존.)

## 7. Read Coverage
- 편집 대상 전 영역 라인 정독: spine(L155–210)·§1.3(sec:pol)·§1.9 sec:tail 전문(eq:memory~eq:reversal + 두 그림 캡션)·sec:sum+staging·LCO 방향(fig:lco-dirmap)·keybox 6단계·R3/R5(tab:signcheck-R)·tab:nodecode/symcode/inputs·P2-1 Sommerfeld(sec:lco-Se)·P2-3 verifybox·P2-4 다온도 전자항. 검토 3 렌즈 + 수렴 1 = 4 Agent 독립 정독(missing 0 자기선언).

## 8. 미결/이월
- **P4**: Ch2 발열 상세화 + P2-2(two-phase config caveat use-this 박스 전파) + P2-4(Ch2 §vibel분 vib T-무관 각주).
- **P5**: 코드(`Anode_Fit_v1.0.15.py`) 점별 재아키텍처 — 문건이 기술한 점별 메모리 적분으로 dqdv 재작성·dead(_causal_lowpass 등) 삭제·격자 param 제거·골든 재정초(해석적 극한+Δ→0+round-trip 검증 후 재캡처). 문건(P3)이 목표 아키텍처를 확정했으므로 코드가 이를 구현.
- **P6**: 그림 9종 경연(fig:spine·fig:relaxode·fig:reversal 등 데이터 recompute — 현재 캡션은 도식 수치평가로 정합, 점별 재산출 P6).
- **P7**: 변경분 검수 + 최종 마감.

## 9. 산출 위치
- 딜리버러블: `docs/v1.0.15/graphite_ica_ch1_v1.0.15.tex`(+.pdf)
- 프로세스: `results/process/V1015_P3_AUTHOR_BRIEF.md`·`V1015_P3_cherrypick_sec19.tex`·본 RESULT
- 레저: `results/process/V1015_EXECUTION_LEDGER.md`

## 10. 상태
✅ **P3 완주·수렴**. 격자 퇴출 + P2-1/3/4(Ch1) + 검수 2라운드(결함 4물리+12정합/문체 전건 수정·재검 0결함). 빌드 GREEN.

## 11. 커밋
main·attribution 없음·명시 스테이징(tex/pdf + P3 프로세스 + 레저; 탐색물 fig_contest/C3_* 제외).
