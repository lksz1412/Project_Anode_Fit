# Ch3 D2b 교과서 품질 전면 개정 — Result Ledger

> 계획서: `Claude/plans/2026-06-07-ch3-5-textbook-quality-overhaul-plan.md` (S31–S37)
> 대상: `Claude/docs/graphite_ica_ch3.tex` (반응속도론). 단일 통합 문건(Ch1·2 뒤 연결) 전제.

## 1. 수행 요약
Ch2에서 검증된 D2b 방식을 Ch3에 적용. 구조 변환 6종(M1–M6) + Codex 검수 정정 완료. 빌드 clean(16p→14p).

## 2. 적용 변환
- **M1** 수식번호 3.x: `\renewcommand{\theequation}{3.\arabic{equation}}` 추가.
- **M2** §13 결론 삭제(교과서엔 논문식 결론 없음).
- **M3** §12 「Chapter 4·5 로 전달되는 항목」 삭제(단일 문건 scaffolding).
- **M4** §1 inheritbox(C1–C7 재기술) → 「기호와 규약」 제목 + 식 번호 포인터 단락 + 신규기호 table 보존. inheritbox newtheorem 정의 제거. C7의 두 구동력(중심 𝒜_j vs 국소 η_j) 구분은 Ch3 핵심이라 보존.
- **M5** 본문 (Cn)·"Chapter N 의 [수식]" → 식 (N.x) 번호 지칭(14 (Cn) + ~13 구체 수식 인용). 개념·원칙·표 출처 언급은 보존.
- **M6** §11 「온도 의존 kinetics 와 식별성」 → 「온도 의존 kinetics」로 retitle. 식별성(공선형 쌍·eq:ch3_ident_chain·독립실험) → `Claude/work/ch6_fitting_material/ch3_identifiability.tex` 이관. 물리(eq:ch3_T, eq:ch3_eyring, ΔH‡/ΔS‡ 다온도 분리, 병목 boundbox) 잔류.
- **M7** 친절 재작성: **불요**(Codex PASS4 가독성 "충분" — Ch3는 이미 rigorous, 구어 2곳·ρ_G gloss만 반영).

## 3. Codex 검수 (foreground, --fresh) 및 정정
- 참조 매핑 29 CORRECT / 6 SUSPECT, 부호 사슬 11/11 CORRECT, 식별성 추출 GAPLESS.
- **SUSPECT 6건 = 내가 도입한 참조 오류(R2). Ch1 source 직접 정독으로 판정·정정:**
  1. §8 단조성 floor: (1.1)→**(1.2)** [eq:cbg = `C_bg≡∂Q_bg/∂V_n≥ε_Q>0`].
  2. §5 직렬 율속(2곳): (1.27)은 활성화율 `ΔG_eff=ΔG_a−χ𝒜`이지 직렬식 아님 → "Chapter 1 무번호 직렬 율속(식 (1.27) 활성화율+병목)"으로 재서술.
  3. §9 ∂lnL/∂V_drive: (1.28)=`−[k_lim/(k_act+k_lim)]χsF/RT` → "(1.28) 활성화 지배 극한 →−χsF/RT, 일반형 limiter 인자 포함"으로 한정.
  4. §11·표 χ: (1.23 affinity)→**(1.27)** [χ는 barrier-lowering 계수].
  5. §1 (1.3) 과대인용 → "측정 전위 V_app (1.3)(다른 전위 구분과 함께)"로 한정.
- register: "못 박는다"→"명시한다", "속도 한 덩어리"→"단일 lumped 속도". ρ_G(G;T) → 식 (1.29) gloss 추가.

## 4. Gate 통과
- G-build: xelatex 2-pass exit 0, 14 pages, undefined ref/citation 0, Overfull hbox 0. PASS.
- G-preserve: eq:ch3_ 라벨 29(원 30 − 이관 eq:ch3_ident_chain), boxed 11 보존. PASS.
- G-codex: MAJOR 5건 전수 정정(Ch1 source 대조 확정), 부호 사슬 11/11 CORRECT. PASS.
- G-numref: 본문 구체 수식 인용 식 번호화 완료(L508 R_{n,eff} 역할정의·L119 등 표/개념 보존). PASS.
- G-ident: 공선형 쌍·ident_chain 본문 부재(grep 0), Ch6 재료 파일 존재. PASS.

## 5. Read Coverage
graphite_ica_ch3.tex 전문(1–764) 2-pass 정독. Ch1 eq:cbg/eq:keff/eq:LqV/eq:density source 직접 확인. Ch1·Ch2 .aux label-번호 맵 추출.

## 6. 미해결/다음
- Ch4(S38–45), Ch5(S46–53) 동일 D2b 루프 미착수.
- Ch6 통합 시 ch3_identifiability.tex 의 라벨(eq:ch3_*) 재지정 필요.
- 권고: Ch4/Ch5도 참조 번호 매핑은 Ch1/Ch2 source 직접 대조(Codex가 Ch 내부 추정 → 반드시 source 검증).

## 7. 커밋
graphite_ica_ch3.tex + .pdf 명시 스테이징(auto-commit+push 규율). 아카이브·zip 불혼입.
