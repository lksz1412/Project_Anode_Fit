# Ch2 v4 — 체리픽 플랜 (검토1 누적 → 보완·체리픽 입력)

> 검토1 R1–R5 차원별 추천·결함 누적. ★단일 완벽 초안 없음 — 강한 유도(v4-05)와 정확 exo/endo(v4-07/01/03)가 분리. 보완서 교정 후 체리픽.

## ★확정 (master 재검증)
- **exo/endo**: Q_rev=−(IT/F)ΔS. 방전(I>0)·희박 +ΔS → Q_rev<0=**흡열**. stage2→1 음ΔS → **발열**. (내부 일관성 — 규약 무관.)
- **config 부호**: `+R ln[ξ/(1-ξ)]`(ξ=탈리튬화, ξ→1 희박 +∞). **w_eff**: `w(1-Ω/2RT)`(V-폭→0 at Ω=2RT, dQ/dV peak 발산).

## 차원별 (검토1)
### R3 가역열·exo/endo·충실도 ✅
- **exo/endo PASS = v4-01·03·07·08·09 / FAIL CRITICAL = v4-02·04·05·06**(역매핑·v4-02 대수오류).
- **best**: exo/endo clean = v4-07(per-stage 절제)·v4-01·v4-03. 챕터 충실도 = v4-05>04>06(단 exo/endo FAIL).
- **체리픽**: base 부호-clean(v4-07) + v4-05 챕터 골격 + v4-03 per-stage exo/endo + v4-06 봉합 문장. ★FAIL 4종 exo/endo 문단 이식 금지.
- 교차: v4-08 w_eff 역수(위험7), v4-04 config+exo/endo → base 부적격.
### R2 섞임·w_eff·B ✅
- ★**w_eff 정답 = v4-05 단 1종**. 나머지 8(01·02·03·04·06·07·08·09) 전부 역수 `w/(1-Ω/2RT)` 상속(CRITICAL·극한표 `w_eff→∞` 물리 역). v4-07/09 합리화(MED).
- 이중계산 B 분리 = 9종 substance PASS. config 부호 FAIL = v4-02(전수 역수)·v4-04(B분해 자기모순).
- v4-02 삼중 FAIL(w_eff+config+물리). v4-04 삼중결함 → base 부적격.
- ★**섞임 best = v4-05**(A 음함수 2조각·수치검증 인용·I 6corner·D 가역평균/비가역gap 분리 최상). v4-05 line233 `−R ln[(1-ξ)/ξ]`는 음부호로 정답 동치(결함 아님).
→ ★**base 1순위 = v4-05**(유일 정확 w_eff + 최강 섞임/분포). 약점 = exo/endo(R3 FAIL) → 보완서 국소 교정.
### R1 분포·부호 ✅
- config 부호 PASS = v4-03·05·06·07(v4-01 θ→ξ 무명시 MED). FAIL = v4-02·04(진성 역수 자기모순), v4-08·09(LaTeX `+` 탈락·렌더 곱). v4-08 ξ/θ 말때움+silent N_A.
- ★**유도 best = v4-07**(부호 4렌즈 PASS·G-derive 점프0·유일 명시 N_A 단위다리 L230·유일 S_config W/Stirling 완전유도·θ=1−ξ 명시·LaTeX 무결). 차순위 v4-05·06.
- v4-04 = config 역수 + μ(V) C1 = 2 CRITICAL → base 부적격.
→ ★**base 2강 정리**: **v4-07**(유도 backbone·exo/endo clean / 약점 w_eff 역수) vs **v4-05**(mixing·w_eff 정답·깊이 / 약점 exo/endo). 체리픽: 한쪽 base + 다른쪽 강점 graft + 양쪽 약점 교정. R5 holistic 후 확정.
### R5 G-usable·범위·best-base ✅
- ★**best-base = v4-05**(유일 config ✅ + w_eff ✅ 동시·G-usable best=완전식+피팅절차+175점 검증표·깊이). G-follow best=v4-07(procedurebox).
- 범위 위반 직접 0. 경계: v4-06(standardised2024 전셀 0.3-0.5 mV/K 라벨 없이 수치화)·v4-04. → 체리픽서 전셀 값 라벨.
- graft: procedurebox→v4-07, 분포 framing/ΔS 문헌표→v4-06, 검증 내러티브→v4-04 Part5-6.
### R4 인용·빌드·문체 ✅
- ★**인용·문체 best = v4-05**(fabrication 0·dangling 0·문체 클린). fabrication: v4-07/08 huggins1941/42(다른 Huggins)·v4-09 cogswell/chemmater·**chemmater2015 8/9 템플릿 오염**(체리픽서 제거). 문체 위반=v4-01·02·03·04·06 / 클린=v4-05·07·08·09.
- 공통 정정(전 9종): jpcc2021 title "Calculations" 누락·standardised2024 전셀 라벨 미명시.
→ ★v4-05 = R1 config PASS·R2 w_eff/mixing BEST·R3 깊이 best·R4 인용/문체 BEST·R5 best-base. **4.5/5 차원 최강**. base 확정.

## ★최종 조립 스펙
- **base = v4-05** 복사 → v4-10.
- **fix(국소)**: ① ★exo/endo 라벨 반전(희박 +ΔS→방전 흡열·stage2→1 음ΔS→발열, Q_rev=−(IT/F)ΔS 일관; v4-07/01/03 문구 참조) ② 인용: 14-master 대조·chemmater2015 등 오염/fabrication 제거·jpcc2021 "Calculations" 추가·standardised2024 전셀 라벨 ③ procedurebox 명료성 v4-07 참조(v4-05 보유분 보강).
- **유지(v4-05 강점)**: config 부호 `+R ln[ξ/(1-ξ)]`·w_eff `w(1-Ω/2RT)`·이중계산 B·문체 클린·완전식+피팅절차+175점 검증표.
- **이식 금지**: 8종 w_eff 역수·v4-02/04 config 역수·fabricated bibitem.

## ★조립 결정 (R1·R2·R3·R5 수렴)
- **base = v4-05**(config+w_eff 유일 정확·mixing/I/D 최강·G-usable·깊이).
- **fix in base**: ★exo/endo 라벨 반전(Q_rev=−(IT/F)ΔS 일관: 희박 +ΔS→방전 흡열·stage2→1 음ΔS→발열) — v4-07/01/03 정확 문구 참조. standardised2024 전셀 값 라벨.
- **graft IN**: v4-07 procedurebox 명료성 + W/Stirling 완전유도/N_A 단위다리(이미 v4-05 보유 — 보강만) · v4-06 분포 framing·ΔS 문헌표.
- **이식 금지**: v4-02·04(config 역수)·8종 w_eff 역수 form. exo/endo는 PASS 초안(07/01/03)서만.
- ★**9b 압축 사유**: v4-05 가 config+w_eff 유일 정확으로 압도 → 비-base 8종 균일 교정(w_eff·부호)은 비목적적(과병렬 절제). 체리픽 1회 교정 + adversarial 재검수로 품질 게이트 유지. (Ch1 은 상보적이라 9b 수행, Ch2 는 단일 우세라 압축.)

## 보완(9b) 예고 — 교정 항목
- exo/endo FAIL 4(02·04·05·06): Q_rev=−(IT/F)ΔS 와 일관되게 흡열/발열 라벨 *반전 교정*.
- w_eff 역수형 초안: w(1-Ω/2RT) 로 교정.
- config 부호 역수 초안: ln[ξ/(1-ξ)] 통일. ξ/θ 치환 명시.
- 텔레그래프 문체·인용 정정(R4 후).
