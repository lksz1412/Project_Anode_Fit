# HANDOVER v1.0.19 — Ch1+Ch2 전면 재작성 (Fable → 10종 → Fable, 문건 전용·코드 제외·doc-leads)

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.19/HANDOVER_v1.0.19.md` (v1.0.19 = Ch1+Ch2 전면 재작성판)
- 근거 = 사용자 지시(2026-07-08, **페이블 → 10종 → 페이블 3단계**·Ch1 후 "챕터2도 같은 방식") + `plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md`(11-section) ← `docs/v1.0.18.2/HANDOVER_v1.0.18.2.md`(제안1 vib Einstein) ← `docs/v1.0.18.1/HANDOVER_v1.0.18.1.md`(이월 완결) ← `docs/v1.0.17/HANDOVER_v1.0.17.md` ← v1.0.16(n(T)) ← v1.0.15(격자 퇴출) ← …
- 레저 = `results/process/V1019_EXECUTION_LEDGER.md`(Ch1 P1~P5·Ch2 C-P1~C-P5). 커밋 = **Ch1**: 7760505(P1)·7cfd6bd(P2)·34c9665(P3)·893ff37(P4)·0651576(P5)·5b7f440(doc-leads 정정) / **Ch2**: 6250d92(C-P1)·24883b8(C-P2)·2d10a76(C-P3)·cdaf00c(C-P4)·본(C-P5).
- 산출 상세 = `V1019_FABLE_BRIEF.md`·`V1019_ASSET_CHECKLIST.md`(Ch1 자산 336)·`V1019_UNION_DEFECTS.md`(Ch1 union 24) / `V1019_CH2_FABLE_BRIEF.md`·`V1019_CH2_ASSET_CHECKLIST.md`(Ch2 자산 133)·`V1019_CH2_UNION_DEFECTS.md`(Ch2 union: HIGH 1 부호+MED 6+LOW).

## ① 본 세션 지시·작업 요약
**지시(사용자 2026-07-08)**: Ch1 문건의 물리·화학 논리 검증 + **Fable 전면 재작성**. 쥐여줄 자료 = 계획서 1.0.10~1.0.18 + 작업이력 1.0.18만 + 작업물(Ch1) 1.0.18만. 3단계 = **①Fable 한 세션 작성(문맥 연속) → ②문제 검수 10종 → ③Fable 최종 수정본**. 기존 틀 폐기·새 framework(구조 문제 해소). **Ch1 문건만·코드 제외.** 절별 개별 저장(쿼터 대비)·세부 절 구조 유지 불필요(물리 논리는 전부 보존). 자율 완주.

**수행(5-phase)**:
- **P1 준비**: docs/v1.0.19 골격(Ch2/appendix 승계·code=18.2 frozen). **자산 체크리스트 336항목**(이전본 v1.0.18.2 Ch1 전수 추출, Sonnet 2 전·후반부 + master 병합, head→tail 갭0) + CRITICAL 오독방지 앵커 12종. Fable 브리핑 패키지.
- **P2 Fable 재작성(한 세션)**: 골격/목차 산출 → master 조기 게이트(336/336 커버·구조 재설계 5건 타당) → 절별 `_sections/ch1_secNN.tex` 24파일 + `\input` 조립. **61p·자산 336/336·CENTRAL 12 박스·CRITICAL 12 앵커 실문장.**
- **P3 10종 검수**: 9 비-Fable + 1 Fable 창(이전본 vs 신본 비교·regression·물리 적대검산) → master union. **★2대 무결: 물리·화학·수학 골격 오류 0(W7 Opus·W10 Fable 독립 재유도 CENTRAL 12·비자명 11·수치 전항 재현, 일부 강화) / regression 자산 유실 0(336 전건 verbatim 보존·강화).** 결함 24 = 전부 구조 재배치 부작용·doc↔code 정정·이전본 계승(물리 무관).
- **P4 Fable 최종수정(같은 세션)**: union 24/24 반영(산문·cross-ref·표·제목만, 식·수치 무변경). 재빌드 61p·undef0·err0.
- **P5 마감**: 최종 빌드·doc↔code 정합·HANDOVER·INDEX·commit.

**Ch2 트랙(사용자 "챕터2도 같은 방식", doc-leads)**: Ch1 완결 후 **Ch2(가역 발열·엔트로피) 동일 3단계 재작성**.
- **C-P1 준비**: Ch2 18.2(958줄) 전수 추출 → **자산 133항목(C-001~133)+CRITICAL 15** + 브리핑(doc-leads).
- **C-P2 Fable 재작성**: 골격 게이트(133/133·**vib Einstein §2.4 전용절 승격** 등 재설계 5건) → `_sections/ch2_*` 15파일 **24p·자산 133/133·CENTRAL 18·register① 본문 코드함수명 0**.
- **C-P3 10종 검수**: **물리 골격 무결(CENTRAL 18·비자명 11·수치 전항 W4 Opus·W10 Fable 독립 재유도 재현)·regression 0(133 전건·narrowing 강화·구본 오류 2건 신본 수정)**. 결함 = **HIGH 1(CU-1 §2.1 vib 엔트로피 부호 오류)**+MED 6+LOW.
- **C-P4 Fable 최종수정**: CU-1~11 전건 반영. **CU-1 부호 정정**(자유에너지 미분 −k_B ln q → 엔트로피 s_int=k_B ∂(T ln q)/∂T 선도 +k_B ln q, C-52 정합)·CU-4 eq:Se→eq:Se-ch2 개명. 24p·undef0·err0·자산 133/133.
- **C-P5 마감**: Ch1 61p·Ch2 24p·appendix 8p 최종 GREEN.

## ② 다음 세션 주의
1. **★문건 권위(doc-leads)·코드 개정 완료**: v1.0.19 = **Ch1+Ch2 문건이 authoritative**, **코드는 이 문건에 맞춰 개정 완료**(K-P1) = `Anode_Fit_v1.0.19.py`. 개정 = 순수 additive(x̄→U_oc eq:implicit 솔버 `solve_U_oc`·x̄ 진입점 `entropy_coefficient_x`·`reversible_heat_x`·`return_terms` 완전/단순식 분리 + 버전 1.0.16→1.0.19·근거문건 v1.0.19). **기존 함수·식별자·데이터 무변경·회귀 골든 13/13 bit-exact.** doc-leads 원칙(문건→코드): 향후 개정도 문건 기준(역방향 축소·억지 matched-bump 금지). 미구현 잔여 = 다온도 LCO 전자항 T-복원(현 T_ref 동결)·total heat q_irr 3분해 = 차기.
2. **구조 재설계 5건(신본 골격)**: ①Part II 단일 §→§11-17 7분할 ②삼분해(§14)를 전자항(§15) 앞으로(forward-ref 축소·G1-G3 일원화) ③broadening N6하위→§7 독립절 승격(제목 "N6 확장", 새 N-노드 아님) ④§5 유도선행(logistic→폭 모수화) ⑤N0+N1→§1 통합. 코드-정합 N0-N9 스파인·부록 이원·라벨 키(eq:/fig:/tab:) 전부 보존 → cross-ref 100% 해소.
3. **자산 앵커**: `V1019_ASSET_CHECKLIST.md` 336항목이 완결성 기준(각 절 말미 `% 자산:` 주석으로 대조). CRITICAL 오독방지 12종(A-035 Fermi-Dirac 가드·A-094 Taylor 함정·A-105 폭 이중지위·A-132 Maxwell/Dreyer·A-137~139 iii-a/iii-b·B2-054 Kirchhoff·B2-069 Ω≠config·B2-084/85/121 단위·B2-105 슬롯·B2-107 가산성·B2-116 동형≠동일·B2-094 세 척도)은 명시 문장 유지.
4. **doc↔code 정정분(P4)**: appB `occ_lagged`→`ksi_lag`(코드 실제 L578)·§10 L_V 단위규약 명시(코드 raw 정규화 Q_cell=1)·§12 부호공존 조건부(부호=round-trip 판정)·T_rep "전 구간 단일평균"·appB "구조 대응". 전부 코드(18.2) 기준으로 문서 교정(코드 무변경).
5. **빌드**: xelatex 3-pass, Ch1 61p·Ch2 24p·appendix 8p, 전 undef0/err0/multiply0. 마스터 = preamble + `\input{_sections/…}` + bib(Ch1 24절·Ch2 15절 각 전용 preamble).
6. **Ch2 재작성 요점**: 자산 `V1019_CH2_ASSET_CHECKLIST.md`(133·CRITICAL 15). 구조 재설계 = ①**vib Einstein §2.4 전용 절 승격**(구본은 §3 vib 안에 섞여 forward-ref·ΔS_vib(T)≠∂S_vib/∂x 혼동 유발) ②구 §6→§2.7 물리/§2.8 종합식/§2.9 방법론 3분할 ③파생 B 본체/재확인 2단 ④부호·기호 함정 부록 A 마스터표 집약(신설) ⑤부록 B = **doc-leads 코드 개정 요구명세**(현 코드 기술 아님, entropy_coefficient=−0.204·tab:qrev·bit-exact 회귀기준). **eq:Se 라벨 = Ch2 로컬은 eq:Se-ch2**(Ch1 §15 eq:Se와 이름 분리). Ch2→Ch1 참조는 서술형(라벨명 평문 인쇄 X)·Ch1 v1.0.19 절번호(Part0=§2·U_j=§3·히스=§4·폭=§5·broadening=§7·전자엔트로피=§15·MSMR=§17).

## ③ 미완료/이월
- **코드 개정 완료(K-P1)**: `Anode_Fit_v1.0.19.py`(additive·회귀 bit-exact). 샘플 이미지 7종+연속성 판정(`samples/`, 전 구간 연속·재검토 불필요) + 3종 정합성·완결성 검수(R-P1) 완료. **차기 이월**: 다온도 LCO 전자항 T-복원(Sommerfeld T-스케일·eq:U1T2 center-T_ref 적분, 현 T_ref 동결)·total heat q_irr 3분해·LCO tier-2/3 실측 초기값. appendix 는 승계(독립 초안, 편입은 사용자 결정 대기).
- **U-24 broadening §승격**: "N6 확장 절"로 표기 처리(새 N-노드 아님) — fig:spine/nodemap 정합 유지. 향후 N6a/N6b 서브라벨 검토 여지.
- **W2-2 신규 라벨**(sec:center-eqcond/Uj) 향후 §hys 역참조 배선 여지(현재 무해 orphan). W1-2 tab:notation s 행은 자산 A-014 보존차 원형 유지(판단).
- **제안 2~5**(`../v1.0.18.2/ROADMAP_future_physics.md`)·v1.0.16 물리-데이터 = 여전히 외부 위임/실측 대기.
