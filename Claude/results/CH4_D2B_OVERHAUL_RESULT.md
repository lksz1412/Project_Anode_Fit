# Ch4 D2b 교과서 품질 전면 개정 — Result Ledger

> 계획서: `Claude/plans/2026-06-07-ch3-5-textbook-quality-overhaul-plan.md` (S38–S45)
> 대상: `Claude/docs/graphite_ica_ch4.tex` (발열 통합 entropy production). 단일 통합 문건(Ch1·2·3 뒤 연결).

## 1. 수행 요약
D2b 방식 적용. 구조 변환 M1–M6 + Codex 검수 정정. 빌드 16p→14p clean. 구조 매핑은 Explore subagent(842줄 정독 위임), 편집은 master가 Ch1/2/3 source 맵 대조로 직접 수행.

## 2. 적용 변환
- **M1** 수식번호 4.x.
- **M2** §15 「Chapter 4 의 결론」 삭제.
- **M3** §14 「Chapter 5 로 전달되는 항목」 삭제.
- **M4** §1 inheritbox(C1–C7) → 「기호와 규약」 식 번호 포인터 + 신규기호 table. inheritbox newtheorem 제거. 두 일반화 대상(Σn_eff I_j η_j) + reaction/activation entropy 구분은 보존.
- **M5** 본문 (Cn) 4곳 + 구체 수식 인용(logistic·정/역·detailed balance ln·이상 affinity·위치 온도계수) → 식 (N.x). 모호한 Ch1-vs-Ch3 귀속은 source 맵으로 확정(정/역 (3.4)·detailed balance ln (3.6)은 Ch3 numbered eq).
- **M6** §13 「식별성과 필요한 실험 제약」 전체(순수 식별성) → `Claude/work/ch6_fitting_material/ch4_identifiability.tex` 이관·삭제. eq:ch4_ident 외부 참조 0(안전).
- **M7** 친절 재작성: 불요(Codex 가독성 "충분", Ch4 이미 rigorous).

## 3. Codex 검수(foreground, --fresh) 및 정정
- 참조 매핑 17 CORRECT / 1 MAJOR, 부호 사슬 대부분 CORRECT, 구조 완결 GAPLESS.
- **MAJOR 3건 판정·처리:**
  1. (mine) §1 η_j 번호: (2.30)은 V_eq,j 식 → η_j 는 **(2.29)**, V_eq,j 는 (2.30)으로 분리. 정정.
  2. eq:ch4_consistency strict `=`: 직후 boundbox가 "strict 등호 아님"+폐쇄조건(∂w_j/∂T=0) 명시 = **Ch2 eq:ch2_consistency 동일 합의 패턴**. Codex 과flag, 실재 오류 아님 → 보존(Ch2 일관).
  3. §6 "η_j 각각 ≥0": dissipative 성분(η_ct·η_ohm·η_conc)은 구성상 ≥0이나, signed η_j 오인 소지 → "전이별 η_j는 부호 있는 양(ξ_j>ξ_eq면 <0), 핵심 양정치 Σn_eff I_j η_j≥0 은 항별 I_jη_j≥0(같은 부호)에서 나옴" 정밀화. 정정(Ch2 A-5 교훈 정합).
- MINOR: §8 Bernardi에 (2.12) 병기, §11 완화에 (3.4) 병기, §2 affinity 표기 `sF(V−U)/(n_eff F)`→`𝒜_j/(n_eff F)=s(V−U)` (식 (3.2) 둘째식, 분모 F 중복 해소), 구어 "못박"×2→"명시", 타이포 "factor 다피팅"→"factor 다. 피팅".

## 4. Gate 통과
- G-build: exit 0, 14p, undefined ref/citation 0, Overfull 0. PASS.
- G-preserve: eq:ch4_ 30(원 31 − 이관 eq:ch4_ident), boxed 11. PASS.
- G-codex: MAJOR(실재 2건: η_j 번호·η_j signed) 정정, MAJOR(과flag 1건: consistency=) 판정 후 보존, 부호 사슬 CORRECT. PASS.
- G-numref: (Cn) 0, 못박 0. PASS.
- G-ident: §13 삭제, eq:ch4_ident 외부 참조 0, Ch6 재료 존재. PASS.

## 5. Read Coverage
graphite_ica_ch4.tex 구조·cross-ref = Explore subagent 전수 추출(842줄). §1·§6·§8·§12·§13 등 편집 대상 region master 직접 정독. Ch1/2/3 .aux label-번호 맵 대조.

## 6. 미해결/다음
- Ch5(S46–53) 동일 D2b 루프 미착수. Ch5는 Ch1–4 인계 → Ch4 label 맵도 필요.
- Ch6 통합 시 ch4_identifiability.tex 라벨 재지정.

## 7. 커밋
graphite_ica_ch4.tex + .pdf 명시 스테이징(auto-commit+push).
