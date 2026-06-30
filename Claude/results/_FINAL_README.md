# _FINAL — 결과물 한 곳 모음 (버전별·코드 분리)

> 2026-06-30 정리. 흩어져 있던 최종 산출물을 **버전별 폴더**로 한 곳에 모음. **원본은 보존**(원본불가침) — 이 폴더는 *복사 모음 뷰*. 흩어진 원본 제거를 원하시면 지시 주세요.
> ⚠️ **이 산출물들은 "완성"이 아님** — `MISSING_CONTENT_REVIEW.md`(누락 검토) 참조. 특히 v8/v9 는 종모양 broadening 설명 누락·w_eff 버그 상속.

## 폴더 = 버전 (계보)
| 폴더 | 문건/코드 | 정체 | 원본 위치 |
|---|---|---|---|
| `Ch1_v7_codeflow/` | v7-11.tex/.pdf (17p) | Ch1 코드흐름 간결판(수식 나열, 유도 압축) | `results/v7-11/` |
| `Ch1_v8_derivation/` | v8-11.tex/.pdf (21p) | Ch1 유도 확장판(v7 의 생략 유도 복원) | `results/v8-11/` |
| `Ch1_v9_LCO/` | graphite_ica_ch1_v9.tex/.pdf (30p) | ★Ch1 최신 — 흑연 + LCO 양극 통합(전자 엔트로피) | `docs/` |
| `Ch2_v3_revheat/` | graphite_ica_ch2_v3.tex/.pdf (5p) | Ch2 가역 발열 survey 초안 | `docs/` |
| `Ch2_v4_statmech/` | graphite_ica_ch2_v4.tex/.pdf (13p) | ★Ch2 최신 — 통계열역학 챕터(분포·섞임) | `docs/` |
| `code_v11/` | Anode_Fit_v11_final.py (706줄) | ★코드 최신 — Ch1 forward dQ/dV 모델 | `results/v7-00_spine/`(매몰돼 있던 것) |

## 계보 요약
- **Ch1 문서**: v7(간결) → v8(유도확장) → v9(LCO 통합). v9 가 최신.
- **Ch2 문서**: v3(가역열 survey) → v4(통계열역학). v4 가 최신.
- **코드**: Anode_Fit_v11_final.py (v11) — Ch1 v8 의 학술 요약이 코드화 대상. (★단 v8/v9 와 코드 모두 `MISSING_CONTENT_REVIEW.md` 의 누락·버그 보유.)
- (참고) docs/ 에 더 오래된 변종 다수: graphite_ica_ch1_Opus_v4/v5/v6·_Fable_v3 — ★이들이 *종모양 broadening 설명을 보유*(v8 이 덜어낸 것). 누락 검토의 원천.

## ★주의 — 정리 방식
- 이 폴더는 **복사 모음**(원본 보존). 원본 흩어진 위치(docs/·results/v7-11·v8-11·v7-00_spine)에 그대로 둠.
- 사용자 확인 후: (a) 흩어진 원본 제거(단일화) or (b) 이대로 유지 — 지시 대기.
- results/ 의 70+ process .md(PHASE_*·LEDGER·HANDOVER)는 *과정 기록*이라 별도(미이동). 원하시면 `results/_process/`로 모음.
