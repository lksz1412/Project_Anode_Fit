# Phase R.3 — 유효배리어·분포·종합·겹침·반증 Result

**Date**: 2026-06-03 · **Plan**: `2026-06-03-ch1-rerevision2-foundation-first-plan.md` · **Step Range**: 23–31

## Summary
§dist·§synth 의 용량보존(C3)·중첩(superpose)·식별순서(C4)·반쪽전지(C8)를 교정. §overlap·§falsify 는 검수 후 클린(편집 불요). Codex 적대검토에서 추가 3건(I-1 포화근사 미명시, I-2 superpose ∝→= V축, I-3 ΔS_a 과대분리)+잔존 1건(L721 모순) 적발 → 전부 정직화·정합.

## Step Range
Steps 23–31 (R.3). 다음 = 32 (R.4).

## Files Updated (`graphite_ica_ch1.tex`)
- C3: eq:simplefit 꼬리 진폭 Q_j/L_V → Q_j·r_{a,j}/L_V + 용량보존 서술(포화근사 ξ_eq(q_a)≈1 명시) + 기호표 r_{a,j} 행.
- eq:superpose: 진폭 1/L_q(G) → r_a(G)/L_V(G), \emph{∝→= 등호·V축·Q_j 포함}(I-2). δ극한 eq:simplefit 정확환원 명시. 분산문단·rigorbox L_V/L_q 정합.
- C4: 식별순서 스왑 — S3=다전류/전위(χ 먼저)·S4=다온도 Arrhenius(χ 기지값). 비순환 명시. S4 헤더·종료줄 ΔS_a 결합식별로 정합(I-3).
- C8: §synth boundbox (iv) 반쪽전지 V_n·dQ/dV_n vs full-cell dV_cell 단서.
- I-1: 용량보존 = 포화근사 의존 정직 명시. I-3: S4 "고정→ΔH_a(순수); ΔS_a 절편조합으로만" — 종료줄과 정합.

## Read Coverage
- §dist L596–645·§synth L647–746 편집 후 재정독 + §overlap L748–784·§falsify L786–808 **전문 정독**(eq:total·반증논리 부호 확인).

## Execution Evidence
- 빌드: xelatex ×3(I-1/2/3·L721 수정 후 재빌드 포함) → `!`0·undefined ref/cite 0·**18페이지**.
- \textbf{분량 무결성 정밀검사}: `Measure-Object -Line` 가 767 로 오산(아티팩트) → \emph{신뢰 카운트} `[IO.File]::ReadAllLines`=**835줄**(원본 803 대비 증가), 68481 B. \section 10개·핵심 18 라벨·\end{document}·15 bibitem 전부 존재 확인 — \textbf{누락 0}.

## Validation (4-tier)
- **G-build/local/flow/convention**: PASS — 용량보존·δ극한 환원 재검산, §overlap/§falsify 참조(S3·S4·eq:arrhenius) 스왑 후 정합 확인.
- **G-review(Codex)**: 1차 C3·C4·C8 적용 확인 + I-1·I-2·I-3 적발 → 수정 → 2차 I-1·I-2 CLOSED, I-3 잔존(L721) → L721 수정(Codex 지정 remedy 그대로) → 두 위치 정독 자체확인 CLOSED.

## Gate
**PASS_R3_SYNTH**.

## Confirmed Non-Changes
- §overlap·§falsify 본문(eq:total·반증): 검수 클린, 편집 불요. eq:closed·3×3 표·rigorbox 구조 보존.

## Open Issues / Decision Queue
- 없음(R.3 범위). R.4 = C9 인용 보강.

## Next
R.4 (Steps 32–35): C9 인용 보강(Newman & Thomas-Alyea·Bloom/Dubarry·완화시간 분포) bibitem·DOI + 전 문서 재빌드. R.5 = Codex 전영역 재리뷰 + 적대 재검증 + Decision Gate.
