# REVIEW_CH2_C2F2 — v1.0.20 Ch2 + appendix_phase_separation 독립 검수 (검수자 C2F2)

> 일시: 2026-07-16 · 검수자: C2F2 (독립 창 — 타 REVIEW 파일 미열람)
> 대상(신본): `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/ch2_*.tex` 16종 + `appendix_phase_separation.tex`
> 대조(구본, read-only): `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/` 동명 파일
> 기준 문건 정독 완료: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md
> 검수 3축: ① 신본 자체 결함 ② v1.0.19 대비 regression ③ 신설 다리(C-017·C-018·B-005·C-019·U9·U10)의 물리·서지 정확성 + 교차 정합(Ch1 리터럴 참조 전건) + 수치 검산

발견 형식: | # | 위치(파일:행) | 심각도(H/M/L) | 축 | 발견 | 근거 | 제안 |

---
### ch2_preamble.tex (전문 정독 완료, 52행)
- diff 대 v1.0.19: 버전 스탬프(v1.0.19→v1.0.20) 2곳 + `\newtheorem*{bgbox}{배경}` 신설(35행) — CHANGE_LOG B-003 의도 변경과 정확히 일치. regression 없음.
- refute 시도: bgbox 가 Ch2 본문에서 실제 사용되는지 후속 파일에서 추적(미사용이어도 결함 아님 — B-003 은 양 preamble 공통 신설 명시). → 후속 확인 결과 Ch2 본문 사용 0회, B-003 명시 범위 내.
- 발견: 없음.

### ch2_sec00_intro.tex (전문 정독 완료, 68행)
- diff 대 v1.0.19: IDENTICAL — regression 불가능.
- 검산: 서두 가역 발열 식 \(\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S\) 는 사슬 박스(49행)의 \(\partial U_\oc/\partial T=\Delta S/F\) 와 자기정합. 사슬 박스 절번호 매핑(§partition→§synthesis) label 전건 실존 확인.
- Ch1 리터럴 참조 2건(§3 평형 중심 전위 · §15 LCO 전자 엔트로피)은 교차 정합 절에서 일괄 대조(후술).
- refute 시도: "상수 ΔS 는 봉우리·골·부호 반전 자유도 없음"(20–21행) — 전이별 상수 ΔS_j 라도 여러 전이의 가중이 겹치면 x-축 구조는 생기므로 과장 아닌가? → 본문이 "전이마다 상수 ΔS_rxn,j 를 가정하는 평형 정전 식만으로는"이라 한정하며, §2.5 에서 상수-ΔS 골격+섞임 항 보정으로 정확히 이 논지를 전개 — 일관됨. 기각.
- 발견: 없음.

### ch2_sec01_partition.tex (전문 정독 완료, 144행)
- diff 대 v1.0.19: IDENTICAL.
- 재검산(손): eq:Z1·eq:occ(마지막 등식 나눗셈 포함)·eq:muV 부호(V↑⇒μ↓⇒⟨n⟩↓)·몰 환산(N_Aε₀≡μ⁰ 상쇄, F/RT=1/w)·eq:logistic 양식·eq:Vxi 역전(θ=1−ξ 대입)·eq:BW 미분→eq:Veq_BW(Ω=0 에서 eq:Vxi 회수)·eq:slope_BW(θ=1/2 에서 1/[θ(1−θ)]=4 ⇒ (2Ω−4RT)/F, 임계 Ω=2RT) — 전 단계 옳음.
- refute 시도: "⟨n⟩ = 분배함수 로그 미분"(25행) — 엄밀히는 ⟨n⟩=(1/β)∂lnΞ₁/∂μ 이고 본문 계산은 확률 가중 평균으로 수행 — 두 서술 동치이므로 결함 아님. 기각.
