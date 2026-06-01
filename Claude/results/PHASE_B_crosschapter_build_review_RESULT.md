# Phase B — 장간 정합 + 통합본 빌드 검수 Result

> **소급 작성(2026-05-30)**: Phase A 와 동일 사유(즉시 미저장)로 소급 기록. 컴팩션 환각 방지.

## Summary
Phase A(장별)에서 의심된 cross-chapter 공통 결함 3종($s_\phi$, $V_n$ vs $V_{n,\drive}$, $n^\eff$)을
6장 관통 대조로 확정/기각하고, 통합본(`_full` + `_body_ch1~6` + `_bib_merged_v2`) 빌드 정합을 검수.
적대 sub-agent 2개(장간 정합 1 + 빌드/bib 1).

## Step Range
pre-RB audit (Phase A 후속). RB cumulative step 부여 전.

## Inputs (전수 정독)
- 장간: `graphite_ica_consolidated_ch1~6.tex` 6장 전수
- 빌드: `graphite_ica_consolidated_full.tex`(163), `_body_ch1~6_v2.tex`(804/412/434/358/342/338), `_bib_merged_v2.tex`(33)

## Read Coverage
장간 agent: 6장 전수. 빌드 agent: full+6 body+bib 전수 + standalone↔body md5 대조(2 엔진).

## 확정 결과

### 교차결함 1 — $s_{\phi,j}$ 부호 인자 [HIGH]
- Ch3 `eq:ch3_Aj` 명시 / **Ch4 verifybox(L184/187)·Ch5 branch affinity(L211) 누락 = 사실.**
- 단 $q_\irr\ge0$ 은 $\eta$ 기반 별도 보장이라 \emph{수치 모순은 미발생} → CRITICAL 아닌 HIGH.
- **Ch5 L220 충전 branch 부호 상쇄 유도 부재** = 출판 시 1순위 지적.
- 권고: Ch3 명시형 기준으로 통일, Ch5 충전 유도 명시. → RB Phase 0.1 규약 1.

### 교차결함 2 — 구동전위 $V_n$ vs $V_{n,\drive}$ [MEDIUM]
- Ch4 내부 (L3)=$V_{n,\drive}$ ↔ verifybox(L187)=$V_n$ 분기 = 사실.
- 기본가정 $V_{n,\drive}=V_n$ 에선 무해, verifybox 가 전제 미명시. 강구동서 균열.
- 권고: Ch2 `eq:ch2_fluxforce`($V_{n,\drive}$) 기준 통일 + 기본가정 명시. → RB Phase 0.1 규약 2.

### 교차결함 3 — $n_j^\eff$ [기각]
- Ch2 "계통오차" 의심 \emph{기각}: Ch2=특수형($n^\eff=1$), Ch4=일반형 위계 정합. Ch3 boundbox 선제 해소.
- 권고: Ch2 에 forward-ref 1줄(LOW). → RB Phase 0.1 규약 3(위계 명문화).

### keystone 전파 [LOW]
- Ch1 "좁게"(ξ_ss→ξ_eq) / Ch3 결론 "Level A=Level B" 표현차 있으나 한정어 존재, Ch5/6 정합 계승.
- 권고: detailed-balance 극한 한정 통일. → RB Phase 0.1 규약 4.

### 통합본 빌드 정합 [PASS]
- **label 충돌 0**(6 body 239개 label 전부 고유; ch2~6 은 `chN_` prefix 네임스페이스).
- 미정의 매크로 0(40 union 중 39 사용, `\dd` dead), 미정의 환경 0(8 중 anchorbox dead), undefined cite 0.
- **standalone ↔ body 무손실 확정**(6쌍 md5 일치; 유일차 = standalone 의 TOC/newpage 2줄, 의도).

### bibliography [LOW]
- **`newman` ≡ `newman2004` 동일 문헌 이중 키**(참고문헌 중복 출력) → 통일 필요.
- dead bibitem 3(`baker1999`,`brenan1996`,`hindmarsh2005` 미인용).
- 30 cite 키 전부 bibitem 존재(undefined 0).

## Validation
모든 판정에 라인 인용 + 재유도/2엔진 대조 근거. DOI 는 Phase A Ch2/Ch4 검수서 web 검증(Phase A 별도).

## Gate
PASS. cross-chapter 규약 4종 + bib 정리 항목을 RB Phase 0.1/7.1 로 이관.

## Confirmed Non-Changes
원본 미수정. Codex 미read.

## Open Issues / Decision Queue
- RB Phase 0.1 = 규약 1~4 동결(본 Phase 권고 직접 입력).
- RB Phase 7.1 = `newman` 중복키·dead bibitem 정리.

## Next
RB 계획 확정 → 사용자 GO → RB Phase 0.1(규약 동결) = cumulative step 1.
