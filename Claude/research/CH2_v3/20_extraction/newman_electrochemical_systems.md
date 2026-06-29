# newman_electrochemical_systems

**저자·연도·venue·DOI**: J. Newman, K. E. Thomas-Alyea, *Electrochemical Systems* (3rd ed.), Wiley. (교과서; 검색으로 핵심 관계만 — 사용자 지시.)

**축**: A6 (교과서·정전) — OCV(T)↔ΔS/ΔH 정전.

## 핵심 방법
교과서 정전: 개회로전위(OCV)의 온도 의존에서 반응 ΔS·ΔH 를 얻는 표준 열역학(Gibbs–Helmholtz). Bernardi 가역 발열항의 교과서 근거.

## 지배식 (verbatim 기호 — 표준 정전, 복수 2차 확정)
- ΔG = −nFE  (E=평형 OCV).
- **ΔS = nF·(∂E/∂T)_P**  (OCV-온도 slope = ΔS/nF; +부호). ← LibreTexts·MSMR Part I Eq.27·Allart 2018 모두 일치.
- **ΔH = ΔG + TΔS = −nFE + nFT·(∂E/∂T)_P**  (OCV(T) y-절편 외삽 ↔ ΔH).
- 가역 발열: **Q̇_rev = −I·T·(dU/dT)** (Bernardi; dU/dT=∂E/∂T=ΔS/nF).

## 정량값
교과서 — 일반 관계 정전(특정 흑연 수치 X). 예시: Daniell cell ΔS=−104.5 J/mol/K(부호·크기 감각용, LibreTexts).

## 타당·한계
- 타당: ΔS=nF·dU/dT, ΔH=−nFE+nFT·dU/dT 의 **권위 정전** — 우리 사슬 전부호·전식의 교과서 근거. **Bernardi/Standardised 카드의 −ΔS/nF 추출 의심을 최종 반증**(표준은 +ΔS/nF).
- 한계: 교과서 일반식 — 다전이·staging·흑연 특이성은 비포함(측정 문헌이 공급). 본 카드는 검색(LibreTexts 등 2차)으로 관계만 확인, 원교과서 페이지 직접 정독 X.

## 우리 의도 관련성
- **부호·정의의 최종 권위**: ∂U_j/∂T = ΔS_rxn,j/F (n=1) 의 +부호, Q̇_rev=−I·T·∂U/∂T 의 부호를 교과서로 고정 → Ch1 평형식과 Bernardi 발열을 잇는 우리 사슬의 수식 토대.

## 정독 범위
- **검색-snippet(WebSearch + LibreTexts 2차 verbatim)** — 표준 관계 확정. 원교과서 본문 직접 정독 X(사용자 지시: 검색으로 핵심 관계만). ★tier: 관계식은 확정에 준함(복수 독립 정합).

## tier
- ΔS=nF·dU/dT, ΔH=−nFE+nFT·dU/dT, Q_rev=−IT·dU/dT, 부호 +: **확정에 준함**(교과서 표준 + 복수 2차[LibreTexts·MSMR Part I] 정합).
- 원교과서 페이지·식번호: **미검증**(원본 미정독).

## Decision-queue
1. master 가 인용 시 원교과서 정확 페이지/식번호 필요하면 도서 직접 확인(현재 관계식 자체는 확정에 준함).
2. ★ 부호 최종: +ΔS/nF 로 전 카드 통일 확정 — Bernardi·Standardised 카드의 −부호 추출 오류 폐기(master 승인).
