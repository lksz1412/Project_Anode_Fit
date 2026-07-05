# V1.0.15 P4 RESULT — Ch2 발열 상세화(additive) + 승인 P2-2·P2-4(Ch2분)

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P4(Steps 15–19). 성격 = additive(Fable 기존 논리 보존·추가만). 대상 = `docs/v1.0.15/graphite_ica_ch2_v1.0.15.tex`. 상태 = ✅ 완주.

## 1. 목표 (계획 L59)
Ch2 발열 교재 상세화: worked example 신설(현재 0)·표 보강·그림 위치 선정·코드 결합점 식별 + 승인 P2-2(two-phase config caveat use-this 박스 전파)·P2-4(Ch2 §vibel vib T-무관 고전극한 각주).

## 2. 산출 (Deliverable)
- `docs/v1.0.15/graphite_ica_ch2_v1.0.15.tex`(+.pdf) — 14p→16p. additive 3종.
- **worked example 신설**(\S ssec:worked "계산 예제 — stage 2→1 부근 한 점의 가역 발열"): Chapter 1 4-전이 staging 파라미터로 대표점 $\bar x=0.25$·298.15 K 를 5단계((a)전하보존 $U_\oc$=82.4 mV → (b)전이별 $\xi_j$·봉우리 가중 $g_j$[표 tab:worked] → (c)겹침 가중 단순식 $\partial U_\oc/\partial T=-0.152$ mV/K → (d)round-trip 실증 → (e)$\Delta S=-14.7$ J/mol·K·$\dot Q_\rev/I=+45.4$ mV 발열)로 끝까지. + 표 tab:qrev(SOC 5점 흡·발열 부호 교대).
- P2-2·P2-4 caveat(§4).

## 3. worked example 수치 (자립 스크립트 계산·검증)
- 자립 numpy 스크립트로 종합식(음함수 $\sum Q_j\xi_j=Q\bar x$ 풀이 → 봉우리 가중 → Bernardi 출구) 직접 구현.
- **round-trip 실증**: 폭 $w_j$ 고정·중심 $U_j(T)$ 만 이동 시 유한차분 $\partial U_\oc/\partial T$ = 해석 단순식과 **전 SOC <0.01 μV/K 일치**(해석식 수치 실증).
- **부호 교대**(tab:qrev): 저-$\bar x$(Li-rich, 음 ΔS) 방전 발열 → 고-$\bar x$(Li-poor, config 양 발산) 방전 흡열. doc 서사(§sec:revheat)·calorimetry 정합.
- 대표점 검산(master): $\Delta S=F\partial U/\partial T=96485\times(-0.152\text{e-}3)=-14.7$·$\dot Q_\rev/I=-T\partial U/\partial T=+45.4$ mV·$\Delta S<0$·방전 $I>0$→$\dot Q_\rev>0$ 발열(eq:qrev 부호 일치).

## 4. 승인 caveat (P2 Decision Gate)
- **P2-2**(use-this 박스 + 맺음): 지배 두-상 전이($2\mathrm L\!\to\!2$·$2\!\to\!1$)의 완전식 config 항은 폭 열적 서식 $w=n_jRT/F$ 전제 위에 서므로, 실측 $w_j$ 가 $T$-동결이면 완전식↔단순식 우열 ~0.3 mV/K 뒤집힘(파생 A srcbox) → 지배 두-상 config 는 다온도 round-trip 확정 대상·단순식이 보수적 기준. 맺음 "측정급 비선형 자동 생성 확정" → "모델 안 자기일관 산출(두-상 폭 T-의존 round-trip 대상)" 완화.
- **P2-4**(§sec:vibel vib 절): $\Delta S_\vib$ 중심 흡수는 $T$-무관 상수 근사(고전 극한 $k_BT\gg\hbar\omega$)이며, 준양자 모드의 잔여 $T$-의존이 다온도 곡률 피팅서 electronic 신호에 소량 섞일 수 있음(Ch1 P2-4 대응 한정).

## 5. 검수 (방법론 §3, 2 렌즈 적대 + master 재유도)
- **라운드 1(2 렌즈, Agent)**: (A)물리·수치·수식-주도 [Opus] (B)register·정합·D1–D6 [Sonnet]. 부호 규약·수치 내부정합·수식-주도 집중.
  - **PASS(재계산 확인)**: 단순식 −0.152·ΔS −14.7·Q_rev +45.4·부호 물리(ΔS<0 방전 발열)·라벨 충돌 처리(Bernardi vs Ch1, I 부호로 읽음)·tab:qrev 5행 부호교대·가중합·비중합=1·ΣQg=11.57·ΔS/F 열·P2-4 vib 물리 — 전건 통과.
  - **확정 결함 6건 → 전건 수정**: **[물리 F1 HIGH]** 완전식 config 보정(−0.044)이 자기모순(g_j는 고정 협폭 w=12mV인데 config 계수는 n=1 열적 R/F) → 고정폭이면 config=0(FD=단순식), 열적폭이면 config≠0(FD=완전식). **무효 완전식 수치(−0.196/+58.3) 제거**·config는 round-trip 대상으로 유보. **[물리 F2 HIGH]** round-trip (d)가 완전식 검증한다 오독 → 폭-고정↔열적 전제 분리 명시. **[물리 F3/register F2 HIGH]** logistic 부호 오타 $\{1{-}\exp\}$→$\{1{+}\exp\}$(정본 eq:logistic 인용). **[register F1 CRITICAL]** D1 내부라벨 누출("P6 그림 후보·구현 대응·최종 게이트·함수명")→본문서 제거(§6·§7로 이관). **[register F3 MED]** (b) 인라인 표→floating tab:worked(문건 표 관례 정합). **[물리 F5 LOW]** 0.3 mV/K caveat = 파생 A worst-case 유지.
  - master 재유도: 단순식·부호·tab:qrev 정확 확인, 완전식 자기모순 확정(1.9× 과대) → 제거가 정답.

## 6. 그림 위치 (P6 이관 — 본문서 제거분)
- **P6 그림 후보**: tab:qrev 의 $\dot Q_\rev(\bar x)$ 곡선(방전 발열→흡열 부호 천이 도해). ssec:worked 마무리 위치. (본문엔 표로 충분·그림은 P6 경연에서 편입 판단.)

## 7. 코드 결합점 (P5·P7 이관 — 본문서 제거분)
- Ch2 발열 종합식의 코드 대응: `entropy_coefficient`(평형 엔트로피 계수, 음함수 풀이→가중)·`reversible_heat`(Bernardi 출구 $\dot Q_\rev=-IT\partial U/\partial T$)·`_effective_dS_rxn`·`func_dSe_molar`(계획 L47). worked example 수치를 코드가 재현하는지 = **P7 문건↔코드 수치 대조 게이트**. (P5 코드 개정은 dqdv 격자 퇴출 중심 — 발열 함수는 격자 무관이라 P5 필수 변경 아님, 수치 대조만 P7.)

## 8. Gate (검증)
- **빌드 GREEN**: `xelatex` 2-pass exit 0 / undefined ref·citation 0(LastPage 해소) / Overfull >10pt 0 / **16 pages**(14→16, worked example+표 2개+caveat).
- **D1 grep 0**(렌더링): P6·최종 게이트·구현 대응·이전 판·구판 잔존 0. (L824 "한계·갭(정직)"은 Fable 원본 절 제목 = 정상.)
- **additive 보존**: Fable 기존 논리(config·vib·elec·overlap·srcbox·revheat·procedurebox) 무변경, 추가·caveat만.

## 9. Read Coverage
- Ch2 전문(sec:partition~맺음) 정독: sec:vibel(vib/elec)·sec:mixing(overlap srcbox·weff·hys)·sec:limits·sec:revheat(eq:qrev·use-this·procedurebox) 라인 정독. 검토 2 렌즈 전문 정독 + master 재유도.

## 10. 미결/이월
- **P5**: 코드 점별 재아키텍처(dqdv·dead 삭제·골든 재정초). 발열 함수(entropy_coefficient·reversible_heat)는 격자 무관.
- **P6**: 그림 9종 경연 — Ch1(spine/relaxode/reversal 데이터 recompute) + Ch2 tab:qrev $\dot Q_\rev(\bar x)$ 곡선 후보.
- **P7**: 변경분 검수 + 문건↔코드 수치 대조(worked example) + 최종 마감.

## 11. 상태·커밋
✅ **P4 완주**. worked example(round-trip 실증) + P2-2/P2-4 + 검수 6결함 전건 수정. 빌드 GREEN. 커밋 = main·attribution 없음·명시 스테이징(Ch2 tex/pdf + P4 결과 + 레저).
