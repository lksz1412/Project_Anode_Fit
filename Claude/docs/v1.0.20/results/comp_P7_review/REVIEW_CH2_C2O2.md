# REVIEW_CH2_C2O2 — 독립 검수 (v1.0.20 Ch2 + Appendix)

> 검수자: C2O2 (독립). 언어: 한국어. 다른 REVIEW_*.md 미열람(독립성 보존).
> 대상: `_sections/ch2_*.tex` + `appendix_phase_separation.tex`
> 신본: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/`
> 구본(대조 read-only): `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/`
> 검수 3축: ① 신본 자체 결함 · ② v1.0.19 regression · ③ 신설 다리 물리·서지 정확성
> 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
> 발견 # = C2O2-NN

기준 문건 정독 완료: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md
이 창 소관 변경: C-017 · C-018 · B-005 · C-019 (CHANGE_LOG) · U9 · U10 (CITATION_BASELINE)

---

## 발견 목록 (파일별 — 정독 완료 시 append)

발견 형식: | # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
Cross-ref(특별축)·수치검산은 전용 섹션에서 별도 정리.

---

### ch2_preamble.tex (전문 정독 완료, 52행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본 line 35 `\newtheorem*{bgbox}{배경}` 1행 추가 외 v1.0.19와 완전 동일. B-003(bgbox 환경 신설) 의도된 변경과 1:1 대응 — regression 없음. | CHANGE_LOG B-003; 구본 51행 vs 신본 52행 diff = bgbox 1행. | 조치 불요. |

가장 약한 곳: bgbox 신설이 ch2에서 실제로 사용되는지는 sec03 서두(페르미온/보손 배경 참조)에서 검증 예정 — 환경만 있고 미사용이면 orphan 후보(A3). → sec03에서 확인.

### ch2_sec00_intro.tex (전문 정독 완료, 69행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(69행, byte-identical 수준). 의미 약화·자산 유실 없음. | 구본/신본 대조. | 조치 불요. |

물리 검산: line 8 $U_j=(-\Delta H+T\Delta S)/F$ = $-\Delta G/F$ (정합), line 26 $\dot Q_\rev=-IT\partial U/\partial T=-(IT/F)\Delta S$ 는 $\partial U/\partial T=\Delta S/F$ 식별과 내부 정합. cross-ref: Ch1 §3(평형중심전위)·§15(LCO 전자엔트로피) — 특별축에서 검증.
가장 약한 곳: line 61 "그 상세 전개는 Chapter 1 §15" — §15 실제 내용이 LCO 전자엔트로피인지 Ch1 대조 필요(특별축).

### ch2_sec01_partition.tex (전문 정독 완료, 145행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(145행). regression 없음. | 대조. | 조치 불요. |
| C2O2-01 | ch2_sec01_partition.tex:82,85 | L | ① | keybox 일반형 $w_j=n_jRT/F$ 도입하면서 두-상 임계는 $\Omega_j>2RT$ 로 적음 — spinodal 유도(eq:slope_BW)는 $n_j{=}1$ 격자기체 기준이라, $n_j\ne1$ 서식에서 임계값이 $2RT$ 그대로인지 $2n_jRT$ 인지 본문상 미봉합. | line 82 일반형 $w_j=n_jRT/F$ 도입 vs line 131 임계 $\Omega=2RT$(n=1 유도). 구본에도 동일 존재 → 신규 결함 아님(선재). | 선재·방어가능(평균장 임계는 자리당 정의). 지적은 정직성 차원 L; 수정 불요. |

수식 재검산(전부 정합): eq:occ FD형 마지막 등식(분자분모 ÷$e^{-\beta(\varepsilon_0-\mu)}$) OK · line 45 $s_\mathrm{int}=-\partial f_\mathrm{int}/\partial T$, $f_\mathrm{int}=-\kB T\ln q$ ⇒ $\kB\partial(T\ln q)/\partial T$, 선도항 $+\kB\ln q$ OK · eq:logistic θ/ξ 부호·극한(ξ→1 고전위) OK · eq:Vxi Nernst OK · eq:Veq_BW $\partial g/\partial\theta$ 미분 OK · eq:slope_BW $\theta=1/2$서 $(2\Omega-4RT)/F$, 임계 $\Omega=2RT$ OK.
cross-ref 표시(특별축 검증): §2 Part0(line 13·39·42·47·113)·§1 σ_d(line 58-59)·§5 ξ_eq(line 77)·§4 spinodal(line 133)·ε̃=ε_0−k_BT ln q(T)(line 43)·Ξ₁ 표기(line 39).

