# V1.0.18 EXECUTION LEDGER — 2-버전(18.1 이월 완결 / 18.2 +제안1 vib Einstein +로드맵)

> 근거 = `../../plans/2026-07-08-v1018-physics-extension-master-plan.md`(신규 발전 제안서·이월·누적 이력). 방법 = v1.0.16/17 동일(증판·phase·9종 체리피킹·doc↔code sync·verify·phase별 commit+push). 상태 ⬜/🔄/✅.
> 사용자 결정(2026-07-08): **18.1 = v1.0.17 + register 이월 완결** · **18.2 = 18.1 base + 제안1 vib Einstein 구현 + 제안2~5 로드맵**. 18.2 는 18.1 superset.

## 방향
- **18.1**(이월 완결): v1.0.17 이월 [선택] register/cosmetic(verifybox·longtable·signcheck ✓·N3 재배열·N/n·ω 다리·z 각주·Appendix 단위) 완결. doc-only·물리 무변경(matched bit-exact).
- **18.2**(물리 심화): 동결 ΔS_vib → **S_vib(T;θ_E)=R[−ln(1−e^{−θ_E/T})+(θ_E/T)/(e^{θ_E/T}−1)]** additive(θ_E 부재=현 동결=bit-exact, v1.0.16 n(T) 패턴). doc(Ch2 유도 9종 체리피킹+Ch1 decomp+GUIDE)+code(entropy_coefficient vib+∂S_vib/∂T 발열)+verify(고온극한 환원·round-trip). + 제안2~5 연구 로드맵.

| Phase | 버전 | 이름 | Gate | 상태 |
|---|---|---|---|---|
| P1 | 18.1 | 증판(v1.0.17→v1.0.18.1)·코드 matched | 3-tex 빌드·회귀 bit-exact | ✅ |
| P2 | 18.1 | register 이월 완결(Ch1/Ch2/Appendix [선택]) | 이월 전건·빌드 GREEN | ✅ |
| P3 | 18.1 | 적대검수+3대 무결+HANDOVER·INDEX·commit | 3대 무결·수렴 | ✅ |
| P4 | 18.2 | 증판(v1.0.18.1→v1.0.18.2)·코드 matched | 3-tex 빌드·회귀 bit-exact | ⬜ |
| P5 | 18.2 | 제안1 코드(S_vib(T;θ_E) additive+∂S_vib/∂T) | θ_E부재 bit-exact·고온극한·round-trip·골든 | ⬜ |
| P6 | 18.2 | 제안1 문건(Ch2 vib Einstein[9종]+Ch1 decomp+GUIDE) | 수식-주도·doc↔code·빌드 | ⬜ |
| P7 | 18.2 | 연구 로드맵(제안2~5+물리-데이터 이월) | 5제안·이월 완전 캡처·외부위임 형식 | ⬜ |
| P8 | 18.2 | 적대검수+3대 무결+HANDOVER·INDEX·commit | 3대 무결·수렴 | ⬜ |

## ★최종 검수(맨 끝, best-effort): Fable 서브세션 1회(2% 잔량)
- 모든 작업 완료·commit+push **후**, Agent(model:fable) 1회로 **최종 Ch1(v1.0.18.2) + 작업이력(레저·HANDOVER) 검토**. 2% 미완 가능성 높음 → 실패해도 무방(보너스). 9종 체리피킹은 비-Fable(Sonnet/Opus). 사용자 지침 7-08.

## 진행 로그 (append-only)
- **2026-07-08 P1 18.1 증판 ✅**: docs/v1.0.17 → v1.0.18.1 복제(tex 3·py 6·guide·golden·figs). py 버전태그 sed 1.0.18.1·v1018_1(path 정합). tex 현행 버전 bump 1.0.18.1(계보 1.0.17). **빌드 GREEN**(Ch1 58p·Ch2 16p·appendix 8p·전 undef0/of0/err0) · **회귀 GRAPHITE 0-DIFF PASS**(코드 bit-identical). 잔여 "1.0.17" 1건 = Ch2 계보 참조(정상).
- **2026-07-08 P2 18.1 register 이월 ✅**: Sonnet 서브세션 2(Ch1·Appendix, 자체 빌드) → master 통합·적대검증. Ch1 8건(verifybox 활성 5·longtable tab:inputs/nodecode·signcheck-R ✓열·tab:staging 서식·z 각주·ω 다리 2·§sm-lattice N/n 통일·U_j (b)(c) 병합) + tab:notation \endfirsthead(master, multiply-defined 해소) + Appendix 4건(N_A 각주·γ/v_m/Δg_v 단위·(c) 분류표·kinetics note). **적대검증(diff 대조)**: 12항목 clean(N/n 정확 3곳·과치환 0·라벨 181 불변) + 결함 1 MEDIUM(signcheck-R ✓열 축소로 R1 셀 overflow 7.3pt) → `$\cdot$` 뒤 공백 삽입 수정·overfull>5pt=0. 
- **2026-07-08 P3 18.1 마감 ✅**: 3대 무결(Ch1 59p·Ch2 16p·appendix 8p·전 undef0/multiply0/overfull>5pt 0/err0·회귀 GRAPHITE 0-DIFF PASS) + HANDOVER_v1.0.18.1·INDEX(v1.0.18 계열). N3 재배열(#5)=의도 보류(그룹헤더 분할 애매·현행 그룹핑 타당). **v1.0.18.1 완결**(물리 무변경·matched bit-exact).
