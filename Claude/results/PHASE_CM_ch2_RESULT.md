# PHASE 2.1–2.8 (Ch2) — 연결고리 + 최종 충방전 모델식 개정 Result

## Summary
Ch2(`graphite_ica_ch2.tex`)를 절 단위 루프로 개정: 최종식 도착점 thread, staging 일차성 보강(P-4), 두 기원 중복 축약(P-3), 신규 §충방전 종합 모델식 절(sec:hys_master), 확정 결함(C2-6·C2-7·C2-8·C2-9·P-5) 시정. 정확성 확인 유도 보존.

## Step Range
Steps 32–54 (Phase 2.1–2.8).

## Inputs
- `Claude/docs/graphite_ica_ch2.tex`(개정 전 391줄, 전문 정독본).
- 검토 결과 REVIEW_CH1_CH2_6LENS(9f06579), 계획서, Ch1 개정본(cf9ffd8 — 인용 대조용).

## Files Created
- `Claude/results/PHASE_CM_ch2_RESULT.md`(본 문건), `Claude/docs/graphite_ica_ch2.pdf`(9p).

## Files Updated
- `graphite_ica_ch2.tex`:
  - §1 기호표: γ_j 정의역 (0,1]→[0,1] (C2-6); 서론: 최종식 도착점 thread(\S\ref{sec:hys_master}) [2.1]
  - §2.1: staging 일차성 기원(Li-Li 유효 상호작용·c축 변형·정전 반발·동종자리 선호→상분리) 보강(P-4) [2.2]
  - §2.4: 두 기원 (i)(ii) 중복을 §3 포인터로 축약, 다입자 자유도만 잔류(P-3) [2.3]
  - §5: ΔU_hys 두 분기 로그 차 = −4 artanh u·Ω 항 차 2u 명시(C2-8) [2.4]
  - §6: bare V→V_n (C2-9); w_j^b 독립 근거(입자크기·kinetic broadening, Ω_j 단독 X)(P-5) [2.5]
  - §2.2: reynier2004 \cite 추가, orphan 해소(C2-7) [2.6]
  - **신규 §충방전 종합 모델식(sec:hys_master, eq:hys_master + eq:hys_master_center)**: 분기별 master 식 + 중심 갈림식 + 환원검산(Ω≤2RT·I→0) + 파라미터/데이터 표 + 예측 keybox [2.7]

## Read Coverage
- ch2.tex 1–391 전문 정독(직전 세션). 본 phase 개정 구간 재확인. Ch1 개정본 인용식(1.3/1.4/1.19) 대조.

## Execution Evidence
- 빌드: `xelatex` 2-pass, pass1=0, pass2=0. `Output written on graphite_ica_ch2.pdf (9 pages)`.
- undefined ref/citation 0, multiply-defined 0(grep). reynier2004 인용 해소, sec:hys_master·eq:hys_master(_center) 정의.

## Validation (4-tier)
- **확정 PASS** — G2.1~G2.7 편집 반영(grep/diff), 빌드 0 undefined(G2.8 빌드분).
- **확정 PASS** — 손검: eq:hys_master_center U_dis/chg=U_j±½γ_jΔU_hys, ΔU_hys=(2/sF)[Ω u−2RT artanh u]=eq:hys_dU 일치; eq:hys_master = Ch1 eq:master의 분기 확장. Ω≤2RT→ΔU→0 단일 peak, I→0→ΔV_obs→ΔV_hys 환원 검산 정합.
- **확정 PASS** — Ch1↔Ch2 인용: (1.3)vapp·(1.4)dQdV·(1.19)Lq 정확. 단일문건 규율(§1 Chapter-1 언급 0, 신규 절은 도착식이지 인계/전달/결론 절 아님) 유지.
- **확정 PASS** — Codex 교차 적대검수(foreground, agent ade8faf5) 완료. 신규 master 식·연결편집 검증; 원문 대조로 Ch1 인용(1.3/1.4/1.19) 일치 확인. 지적 4건 시정:
  - B1 eq:hys_master_center: u_j 허수 방지 정의역 가드 `(Ω>2RT; Ω≤2RT⇒ΔU=0)` 추가.
  - B2 §2.1: "Ω_j>0가 두 상으로 갈라지게"→"충분히 크면(Ω>2RT)" 상분리 기준 정정.
  - S2 환원검산: 분기 폭 단상 폭 합쳐짐(w_dis=w_chg=w_j) 명시.
  - S4 §2.1: "고용체라면 히스테리시스 없다"→"열역학적 히스테리시스 없다(분극 남음)".
  - S1(eq:master 꼬리 게이트)·S3(충전 꼬리 방향)은 underbrace 조건/Ch1 단방향성으로 이미 커버 — 정상 판정.
  재빌드 9p, 0 undefined.

## Gate
**PASS** — 빌드·손검·Ch1정합·Codex(MAJOR 시정 후 0) 전부 PASS.

## Confirmed Non-Changes
- 정확성 확인 유도(V_eq 2.5·spinodal 2.7·ΔU_hys 2.10 본체) 불변. 기존 §hys_param·§hys_fit 보존(신규 master 절이 통합·강화). 기존 라벨 불변(신규 sec:hys_master·eq:hys_master(_center)만 add).

## Open Issues / Decision Queue
- 없음(파라미터 집합 IF-2대로).

## Next
- Codex foreground 적대검수(Ch1·Ch2 신규 master 절+연결편집) → MAJOR 시 정정·재커밋. 이후 종합 보고.
