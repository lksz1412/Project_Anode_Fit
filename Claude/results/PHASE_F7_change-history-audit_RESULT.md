# Phase F.7 — 변경이력 대대적 감사(R·A·W·F 왜곡·누락·환각) Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-textbook-form-plan.md`(F.7 추가) · **챕터**: F · **트리거**: 사용자 추가 지시("이번 작업 완료 후 변경이력 전반 왜곡·누락·환각 대대적 검토")

## Summary
R·A·W·F 4라운드 누적 편집이 \emph{어딘가에서 왜곡·누락·환각}을 만들지 않았는지 대대적 감사. 방법 = (1) 변경이력 문건 재구성 + 페이지/줄 궤적 재조정, (2) 수식·절·라벨 전수 보존 확인, (3) 기록↔실제 대조(환각 점검), (4) Codex 독립 교차모델 전 사슬 감사(백지 가정). **결론: 누적 편집에 의한 왜곡·누락·환각 없음.** Codex 가 제기한 확정 5건은 \emph{4건이 이미 문서에 정직하게 flag 된 근사/정당 인용}(왜곡 아님)·\emph{1건이 cosmetic}(정리함).

## 방법과 증거

### 1. 변경이력 재구성 + 궤적 재조정
| 라운드 | 성격 | 줄/페이지 | Δ 설명 | Codex |
|---|---|---|---|---|
| R.0–R.9 | 결함 재수정 | 879줄·19p | (baseline) **물리 공식 보존, 유도 정직성·부호만 교정** | DOCUMENT CLEAN |
| A.0–A.5 | eq#29 분할 + 신규 §6(5식) | 971줄·21p | +92줄·+2p = \emph{내용 순증가}(신규 절·식 분할) | DOCUMENT CLEAN |
| W.0–W.6 | 격식·구어체 | 958줄·20p | −13줄·−1p = §6 군더더기(비유·라벨) 제거 | REGISTER CLEAN |
| F.0–F.7 | 형식·메타 | 924줄·19p | −34줄·−1p = 스캐폴딩(로드맵·읽기규약)·메타·verbose 제목 제거 | CLEAN |
→ **페이지 궤적 19→21→20→19 전부 의도적 내용(A 추가 / W·F 군더더기·스캐폴딩 제거)으로 설명. 물리 silent 누락 0.**

### 2. 수식·절·라벨 전수 보존
- **수식 라벨 38개** 전부 존재(charge·dQdV·cbg·vapp·lnW·smix·mumix·muint·mu·eqcond·logistic·dxidz·dxidV·eqpeak·dUdT·relax·dxidq·Lq·rsol·tail·tailTC·eyring·affinity·bv·db·sseq·keff·LqV·density·norm·wavg·varprop·jacobian·superpose·closed·simplefit·arrhenius·total). 전 도출 사슬 무손실.
- **절 11개**(서론+notation·stage·eqpeak·lag·barrier·stattools·dist·synth·overlap·falsify) 전부 보존.
- **라벨 48개**(38 eq + 10 sec) = A.5 기록값과 일치(W·F 라벨 무변경). undefined/중복 0.

### 3. 기록↔실제 대조(환각 점검)
- R 기록 "logistic·peak 공식 보존" → eq:logistic(−s 부호)·eq:eqpeak(V_peak=U_j·Q_j/4w_j·3.53w_j) 실제 존재·일치 ✓
- R.9 "eq:eyring ≃ + k_0 현상론" → 실제 eq:eyring `≃`·"$k_j$ 를 forward 로 재정의하지 않는다" 존재 ✓
- A 기록 "신규 §6 5식" → eq:density·norm·wavg·varprop·jacobian 5개 실재 ✓
- A 기록 "eq#29=superpose 2줄 분할" → eq:superpose `\boxed{\begin{aligned}}` 2줄 실재 ✓
- 라벨 48·페이지 궤적 = 각 ledger 주장과 일치 → **기록 환각 없음.**

### 4. Codex 독립 교차모델 전 사슬 감사(백지 가정)
- **물리 사슬 무결성(item1)**: charge→logistic→eqpeak→relax→eyring→bv→db→sseq→keff→Lq/tail/tailTC→LqV→통계기술→superpose→closed→simplefit→arrhenius→total — **각 인접 단계 CLEAN, 논리 비약·순환 0**.
- **부호 일관(item2)**: eqcond↔logistic↔dxidV↔dUdT↔affinity↔bv↔db↔keff↔LqV↔vapp 전반 **CLEAN, 숨은 flip 0**.
- **수식 정확(item3)**: logistic −s·eqpeak 3결과·db χ상쇄·varprop σ_G/RT·superpose 면적보존 **CLEAN**.
- **P3 프로젝트(item6)**: V_n/app/drive/OCV 구분·전하보존 중심식 유지(OCV lookup 퇴화 X)·순환 의존 implicit 정직 표기 **전부 CLEAN**.

## Codex 확정 5건 4-tier 판정
| # | Codex 지적 | 판정 | 근거 |
|---|---|---|---|
| 1 | eq:keff regime "A_j≳RT" too loose | \emph{이미 flag(왜곡 아님)} | 본문이 "A_j=RT서 37%·3RT서 5%·\emph{수 RT 이상일 때 정확}"으로 \emph{정량 명시}. 정직한 근사. |
| 2 | effective-width 시 detailed balance 닫힘 안 됨 | \emph{이미 flag(왜곡 아님)} | 비고 박스가 "w_j 를 effective width 로 두는 것은 닫힌 유도가 아니라 coarse-grained 근사"라 \emph{명시 경고}. |
| 3 | L329-330 `\textbf{$수식$}` 중첩 | \emph{확정 cosmetic → 정리** | 수학모드에 bold 안 먹어 \emph{출력 동일}(무해)이나 소스 클린화(L327·329·330). |
| 4 | "연속 중첩 ⇒ stretched exp" 과단정 | \emph{인용 근거(왜곡 아님)} | johnston2006 제목 = "Stretched exponential ... from a continuous sum of exponential decays"; svare2000 = 배리어 분포→stretched. \emph{인용이 메커니즘 직접 지지}. |
| 5 | bloom2005(DVA) 를 ICA 에 인용 | \emph{정당 병기(경미)} | 도입은 dubarry2012(ICA)·bloom2005(미분곡선 분석 foundational) 병기. R.4서 Bloom 제목·DOI 검증·의도 병기. dubarry 가 ICA 주 인용으로 존재. |
- 의심 2(funabiki1999 인용 강도·fit anchor 절차): 각각 boundbox 가정 표기·"정확한 창은 피팅 선택, 부록" 명시 deferral 로 \emph{이미 정직 처리}.

## 조치
- **수정 1**: L327·329·330 `\textbf{$수식$}`(ineffective bold) → 순수 math. \emph{출력 불변, 소스 클린}. 빌드 GREEN 유지.
- **무수정(보고)**: item 1·2·4·5 + 의심 2 = 이미 문서에 정직 flag/정당 인용 → 왜곡·누락·환각 아님. R.9/A.5 기검증 모델링 선택 재개봉은 회피(P5·기검증 합의 존중).

## Read Coverage
- 변경이력 문건 정독: R0-R5 ledger·A0-A5 ledger·W ledger/result(컨텍스트)·F result. 현재 tex 전문(F.0 정독) + 라벨/절/수식 grep 전수. Codex 전 문서 ×1 종합 + F.6 ×4.

## Validation (4-tier)
- **확정**: 누적 편집(R·A·W·F)에 의한 왜곡·누락·환각 \emph{없음}. 38식·11절·48라벨·부호사슬·참조 전부 보존. 페이지 궤적 전부 의도 설명. 기록↔실제 일치(기록 환각 0). Codex 전 사슬·부호·P3 CLEAN.
- **추정/미검증**: 없음.
- **의심(유지 판정)**: Codex item 1·2·4·5 = 이미 문서 flag/정당 인용(정직 근사·인용) — 수정 불요.

## Gate
**PASS_F7_AUDIT** — 변경이력 무결(왜곡·누락·환각 0) + Codex 전 사슬 CLEAN + cosmetic 1 정리 + 빌드 GREEN.

## 빌드 최종
- 924줄·**19페이지**·`!`0·ref/cite undefined 0·overfull hbox 0.

## Next
교과서 형식화(F) + 변경이력 감사(F.7) 완료. 사용자 검토. 커밋·푸쉬는 사용자 요청 시(미커밋 상태 보고함).
