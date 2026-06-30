# Ch1 교과서 형식화 (F.0–F.7) Execution Ledger

**Plan**: `Claude/plans/2026-06-06-ch1-textbook-form-plan.md`
**대상**: `Claude/docs/graphite_ica_ch1.tex`

| Phase | Steps | Block | Purpose | Status | Validation | Gate |
|---|---:|---|---|---|---|---|
| F.0 | 1–4 | 인벤토리·설계 | 전문 정독 + 메타·구조 전수 + §FT/§BX/§TT/서trim 확정 | PASS | 정독 100%·결정 확정 | PASS |
| F.1 | 5–8 | front matter | 제목 교과서식·author/date 제거·서론 표제·스캐폴딩(전개뼈대·읽기규약) 제거 | PASS | 빌드 GREEN 19p·관측/stagebox 보존 | PASS |
| F.2 | 9–12 | 박스·메타 | 박스 5종 리네임(미확정→비고·줄기밖→심화)·자기참조 9곳 제거 | PASS | grep 메타 0 | PASS |
| F.3–F.5 | 13–30 | 절 구조 | 소제목 의문형·문장형 9곳→명사구 | PASS | grep 의문형 0·빌드 GREEN | PASS |
| F.6 | 31–34 | 교차모델 | Codex 적대(형식·의미·논리·참조) → 판정 → 반복 | PASS | Codex 4라운드 → **CLEAN**; 빌드 GREEN 19p; 메타·의문형·원고이력·authoring 잔재 0; 참조 무손상 | PASS_F |
| F.7 | 35–37 | 변경이력 감사 | R·A·W·F 전체 변경이력 왜곡·누락·환각 대대적 검토 | PASS | 누적편집 왜곡·누락·환각 0; 38식·11절·48라벨 보존; 궤적 19→21→20→19 전부 의도설명; Codex 전사슬·부호·P3 CLEAN; cosmetic 1 정리 | PASS_F7_AUDIT |

**Result**: `PHASE_F7_change-history-audit_RESULT.md`. 빌드 GREEN 924줄·19p.

## 챕터 F 완료
F.0~F.7 전부 PASS. 교과서 형식화 + 변경이력 감사 완료. PDF=`Claude/docs/graphite_ica_ch1.pdf`(19p). 커밋·푸쉬 미실행(사용자 요청 대기).

## F.6 1차 Codex 판정·조치(완료)
- **확정 수용**: A-271 "부호의 정직성"→"부호의 물리적 의미" · C-506 "왜 χ…1인가"→"전달계수 분할과 합 1의 근거"(누락분) · C-697 "왜 저온서 더 늘어지나"→"저온 꼬리 확장"(누락분) · A-562 "step-function 금지의 물리적 구현"→"불연속 절단을 피하는 구현".
- **추가 통일**: C-363 keybox "평형만으로는 관찰을 설명할 수 없다"→"평형 기준선의 한계" · 마감 D: §lag·§barrier "의미."→keybox 「핵심」(동역학 지연의 요지/세 인자의 peak 진입), §dist 중간 "의미."→"중첩 결과의 해석".
- **오바 경감**: A-817 "본 장 식만으로"→"위 도출식만으로"(식별가능성 주장 보존, 자기참조 색채만 제거).
- **정상 확인**: 박스 6종 격식 OK·참조 \ref/\eqref/label/cite 무손상·로드맵 제거 후 논리 공백 없음.

## 현재 상태
- 빌드 GREEN: 19p·`!`0·ref/cite undefined 0·overfull 0. keybox 5개(§stage·eqpeak·lag·barrier·stattools) 마감 일관.
- grep 감사: 의미./정직/금지/의문형/줄기/만으로 사용 = **0**.

## Result 문건
- `PHASE_F0_inventory-design_RESULT.md` · `PHASE_F1-F5_form-edits_RESULT.md` · (F.6 result 작성 예정)
