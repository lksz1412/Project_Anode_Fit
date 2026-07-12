# V1.0.19 EXECUTION LEDGER — Ch1 전면 재작성 (Fable → 10종 문제검수 → Fable 최종수정, Ch1 문건 전용·코드 제외)

> 근거 = `../../plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md`. 방법 = 우리 방식(분업·단위루프·N회 가변청크·N종 체리피킹·3-Pass) + Fable→10종→Fable 3단계. 상태 ⬜/🔄/✅.
> 사용자 지시(2026-07-08): 자료 = 계획서 1.0.10~1.0.18 + 이력 1.0.18 + 작업물 1.0.18. Ch1만·코드 제외. ①Fable 한 세션 작성(골격→절별 저장→합치기·resume 앵커) ②10종(9 비-Fable+1 Fable, 이전본 vs 신본 union) ③Fable 같은 세션 최종수정. **틀 자유·물리 논리 전부 보존(자산 체크리스트 앵커)·물리=코드 모델·새 물리 X.** 자율 완주.

| Phase | 이름 | Gate | 상태 |
|---|---|---|---|
| P1 | 준비(브리핑·자산 체크리스트·골격) | 자료·체크리스트·골격 완비 | ✅ |
| P2 | ①Fable 재작성(골격→절별→합치기) | 골격 게이트·빌드 exit0·자산 자기대조 | ⬜ |
| P3 | ②10종 문제검수(이전본 vs 신본 union) | 10창 커버리지·자산 유실 0·union | ⬜ |
| P4 | ③Fable 최종수정(같은 세션) | union 반영·빌드 GREEN·유실 0 | ⬜ |
| P5 | 검증·마감(빌드·doc↔code·HANDOVER·INDEX·commit) | 3-pass·물리=코드·최종 | ⬜ |

## 진행 로그 (append-only)
- **2026-07-08 P1 착수**: docs/v1.0.19 골격 생성(Ch2 v1.0.19·appendix·code=18.2 frozen·golden·figs·`_sections/`). 계획서 1.0.10~1.0.18 = plans/ 19개 식별. 이력 1.0.18 = V1018_EXECUTION_LEDGER·HANDOVER_v1.0.18.1·HANDOVER_v1.0.18.2. 작업물 = docs/v1.0.18.2/graphite_ica_ch1_v1.0.18.2.tex(이전본). 자산 체크리스트 = Sonnet 2(전·후반부) 추출 → master 병합·증강(진행). 브리핑 패키지 = V1019_FABLE_BRIEF.md.
- **2026-07-08 P1 완료 ✅**: 골격 승계 빌드 GREEN(Ch2 17p·appendix 8p·undef0·err0). **자산 체크리스트 확정** = `V1019_ASSET_CHECKLIST.md` **336 항목**(A-001~159 전반부 L1-1875 + B2-001~177 후반부 L1850-3544, head→tail 갭0 경계 겹침확인) + CRITICAL 오독방지 앵커 12종 최상단 표기. Fable 브리핑 `V1019_FABLE_BRIEF.md` 완결(§0 한정·§1 골격→절별→합치기·§2 헌법3종·§3 버전진화·§4 자료경로·§5 자산앵커 포인터). → P2 Fable 재작성 착수.
