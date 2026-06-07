# Ch5 D2b 교과서 품질 전면 개정 — Result Ledger

> 계획서: `Claude/plans/2026-06-07-ch3-5-textbook-quality-overhaul-plan.md` (S46–S53)
> 대상: `Claude/docs/graphite_ica_ch5.tex` (충전 branch·히스테리시스). 단일 통합 문건(Ch1–4 뒤 연결).

## 1. 수행 요약
D2b 방식 적용(구조 변환 M1–M6). 구조 매핑 = Explore subagent(838줄), 편집 = master가 Ch1/2/3/4 source 맵 대조 직접. 빌드 16p→14p clean. **D2b 변환은 Codex 검수에서 매핑·추출 오류 0**.

## 2. 적용 변환
- **M1** 수식번호 5.x.
- **M2** §15 「Chapter 5 의 결론」 삭제.
- **M3** §14 「실데이터 피팅으로 전달되는 항목」 삭제.
- **M4** §1 inheritbox(C1–C7) → 「기호와 규약」 식 번호 포인터 + 신규기호 table. newtheorem 제거. "본 장이 여는 것"(충전 부호 유도) 프레이밍 보존.
- **M5** 본문 (Cn) 2곳 + 구체 수식 인용 → 식 (N.x). branch 확장형 base 매핑: 구동력 일반형 (3.2)·과전압 (4.2)·비가역열 일반형 (4.14)·이상 affinity (1.23)·V_app (1.3). 표 (C7) → (4.14).
- **M6** §13 「식별성과 필요한 실험 제약」 전체 → `Claude/work/ch6_fitting_material/ch5_identifiability.tex` 이관·삭제. 본문 dangling \S\ref{sec:ch5_ident} 3곳(L501·536·690) → "(피팅 장 Ch6)" plain-text 정정.
- **M7** 친절 재작성: 불요(Codex 가독성 "구조 균형 잡힘").

## 3. Codex 검수(foreground, --fresh) 결과 — ★ 2분류 ★
### 3a. D2b 변환 정합(내 작업) — 전부 통과
- 참조 번호 매핑: Codex가 오류 0 ("산출물 수식 번호 매핑 자체보다 개념적 불일치가 먼저"라고 명시 — 매핑은 문제 아님).
- 식별성 추출·dangling 정정: 지적 0.
- 구조 완결(§12→bib): 정상.
- register: "못박" 0(전수 정정).

### 3b. ★ Ch5 기존 물리 설계에 대한 Codex 우려 (사용자 판정 회부, 미검증) ★
**중요: 아래는 내 D2b 변환이 아니라 이전 세션에 작성된 Ch5 충전-branch 부호 아키텍처에 대한 Codex의 우려다. 불확실("후보/의심")하며, Codex가 같은 리뷰에서 미독을 보였으므로(item 6 = "이는 곧"→직후 boxed 식 (5.x)로 정상 완결인데 "미완 문장"으로 오판) 확정 오류가 아니다. P5·문건 보호·4-tier 규율상 밤샘에 일방 재작성하지 않고 사용자(도메인 전문가) 판정에 회부한다.**

| Codex 등급 | 위치 | 우려 요지 | 내 판정 |
|---|---|---|---|
| MAJOR | L218–227·361–364 | 방전 기준 ξ_j 유지 + 충전서 logistic 기울기 반전이 충돌 가능 | 미검증. §3가 s_φ^chg=−1을 규약 귀결로 유도(eq:ch5_schg)하는 의도적 설계. 검증 필요. |
| MAJOR | L456–476 | η_{j,prog}^b "촉진 양수"와 발열 비음(I_jη_j≥0)이 단일 정의서 양립 불가? | 미검증. 부호 상쇄(I_j·η_j 동시 반전) 주장의 정합성 정밀 검토 필요. |
| MAJOR | L206–226 | logistic 출발식이 RT/F 폭 고정인데 w_j^b/n_eff^b 도입 혼재? | 미검증. Ch3의 n_eff=RT/(Fw_j) 일반형 정합과 동일 쟁점일 가능성. |
| HIGH | L711+361 | rest s_φ^rst=0 을 branch logistic 대입 시 ξ_tar=1/2 비물리 | 미검증. rest 전용 target 분리 필요 여부. |
| HIGH | L676 | 가역열 branch 부호 인자 1/s_φ^b 누락/이중계상 의심 | 미검증. |
| MEDIUM | L240 | "이는 곧" 미완 문장 | ✗ Codex 미독(직후 boxed 식으로 정상 완결). 오류 아님. |
| MEDIUM | L357 | n_j(물질량) vs n_j^eff 기호 충돌 | presentation, 표 주석 후보. |
| MEDIUM | L491–519 | R_n^b 단독 apparent vs 복합 성분 이중 역할 | presentation. |
| MEDIUM | L606–618 | E_loop=∮VdQ>0 양수성 과강(signed 혼재 시) | 검토 후보. |

## 4. Gate 통과(D2b 한정)
- G-build: exit 0, 14p, undefined ref/citation 0, Overfull 0. PASS.
- G-preserve: eq:ch5_ 33, boxed 5. 이관(식별성=무라벨)으로 eq 손실 없음. PASS.
- G-numref: (Cn) 0, dangling 0, 못박 0. PASS.
- G-ident: §13 삭제, Ch6 재료 존재, 본문 포인터 정정. PASS.
- **G-physics(기존 설계): Codex 우려 3b는 D2b 범위 밖·미검증 → 사용자 판정 보류.**

## 5. Read Coverage
구조·cross-ref = Explore subagent 전수(838줄). §1·§3·§13 등 편집 region master 직접 정독. Ch1/2/3/4 .aux 맵 대조.

## 6. 미해결/다음
- **★ Ch5 충전-branch 부호 물리(3b) 사용자 검토 필요 — 실재 오류 시 별도 물리 정정 phase.**
- Ch6(피팅 장) 통합: ch2/ch3/ch4/ch5_identifiability.tex 4건 + Archive_old appendixB 병합, 라벨 재지정.
- Ch2–5 D2b 완료(밤샘 인계 스코프 완결).

## 7. 커밋
graphite_ica_ch5.tex + .pdf 명시 스테이징(auto-commit+push).
