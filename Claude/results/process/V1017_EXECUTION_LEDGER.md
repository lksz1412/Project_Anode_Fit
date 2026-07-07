# V1.0.17 EXECUTION LEDGER — 교재 register·정합·완결성 정련 + Ch2 서지 보강 (이규섭 완전 리뷰 반영)

> 근거 = `V1017_REVIEW_COMPLETE.md`(이규섭 S6 재추출·교차검증 — Ch1 26 + Ch2 7 + Appendix 9). 방법 = v1.0.15/16 동일(증판·phase·9종 체리피킹 검수·verify·phase별 commit+push). 상태 ⬜/🔄/✅.
> **정정 기록**: 원 S6 추출물이 Ch2/Appendix 전량 누락·"미포착" 거짓 → 원본 사진 재추출로 완전 복원. 물리·수식 무변경(register·정합·완결·서지).

## 방향
Ch1 26 + Ch2 7 + Appendix 9 = **register(코드/구현 본문참조→물리·모델 용어)·수식-주도(box (a-d) 라벨)·기호정합·완결성·서지 보강(참고문헌 7건 저자명·DOI 실조회)**. 코드 = matched version bump(bit-exact). 반영 = 9종 체리피킹(9 독립 리뷰어 확인·확장 → master 체리픽·적용).

| Phase | 이름 | 산출 | Gate | 상태 |
|---|---|---|---|---|
| P1 | 증판(v1.0.16→v1.0.17)·코드 matched bump | docs/v1.0.17 | 빌드(3-tex)·회귀 bit-exact | ✅ |
| P2 | 9종 체리피킹 검토 수집(Ch1+Ch2+Appendix) | 통합 fix-list | 커버리지·확장·중복제거·타당성 | ✅ |
| P3 | Ch1 반영(26항목, 단위 루프) | ch1 v1.0.17 | 본문 코드참조 grep=대응표 외 0·box·기호·빌드 | ✅ |
| P4 | Ch2 반영(register+서지 저자명 실조회+정합) | ch2 v1.0.17 | 코드참조 0·저자 7건 보충·derbox·용어·빌드 | ✅ |
| P5 | Appendix 반영(버전 1.0.17·단위·결정 유지) | appendix | date 1.0.17·단위·broadening 참조·빌드 | ✅ |
| P6 | 적대검수 + 3대 무결 + HANDOVER·INDEX | 마감 | 3대 무결·수렴·commit+push | ✅ |

## 진행 로그 (append-only)
- **2026-07-07 P1 증판 ✅**: docs/v1.0.16 → docs/v1.0.17 복제(tex 3·py 6·guide·golden·figs). py 버전태그 rename 1.0.17. **회귀 GRAPHITE 0-DIFF PASS**(코드 bit-identical). **빌드 gate GREEN**: Ch1 58p·Ch2 16p·appendix 8p, 참조/인용 undefined=0·overfull>10pt=0(Ch1은 3-pass 필요, "undefined" grep 초기 오탐 = 한글폰트 italic shape 경고·무해). tex 내부 버전 선언(title date·매칭코드 참조)은 Ch1 #1·Appendix A1 반영(P3/P5) 시 1.0.17 로 정정(블라인드 sed X).
- **2026-07-07 P2 검토 착수**: 9종 체리피킹 sonnet 리뷰어 9(Ch1 register/수식주도/기호/완결 4·Ch2 register+서지/수식물리/기호box용어 3·Appendix register버전/물리단위 2) + 참고문헌 저자 CrossRef 조회 1 = 병렬 착수. master(opus) = 체리픽·적대검증·정밀 적용 전담(사용자 지침: 하위모델 서칭·master 고등작업).
- **2026-07-07 P2 완료**: 10 리뷰어 전건 회수. SEED 엄정 검증 + 신규 다수 발굴(CR1 register 신규15·CR3 기호 신규3·CR4 완결 신규2). 정정: SEED#3 "결합"→실제 "결함", #6 병합 2곳→1곳, #9 ω_j→ω_i, q→ζ 충돌→q_int. DOI 2건 오류 발견. 통합 fix-list 디스크 확정.
- **2026-07-07 P6 마감 ✅**: **3대 무결 GREEN**(회귀 GRAPHITE 0-DIFF PASS·Ch1 58p·Ch2 16p·appendix 8p·전 undef0/overfull0·중복단어 0). **적대검증**(sonnet, git diff 기반 편집지점만 정독 + CrossRef 독립 재조회): DOI 2정정·저자 7건 전부 확정 일치(standardised2024 실제 2인 Hales/Bulman 확인 — 캐비엇 해소), 서식 무손상. **확정 결함 2건**(메모리→기억 replace_all 조사 미조정: L1999 "기억는"→"은"·L2151 "기억가"→"이") → 수정·재빌드 GREEN. HANDOVER_v1.0.17·INDEX(v1.0.17 현행·v1.0.16 강등) 작성. **v1.0.17 완결**: P1~P6 커밋 423f7d5·f227ffc·d398dbf·P6(본). 물리·수식·코드 무변경(matched bit-exact).
- **2026-07-07 P5 Appendix ✅**: A1 date 1.0.15→1.0.17(렌더링 현행) / A2 소스주석 v1.0.14 이력 스탬프 보존+명시(CR8 override — 버전업 시 보존) / A3 "본문 broadening 절"→"\S1.7(broadening 절)" 리터럴(CR9: 독립컴파일 위해 \ref 금지) / A5 κ·M 단위(CR9 물리 재유도 검증: F=∫[f+κ|∇ξ|²]dV 부피밀도 기준 → [κ]=J/m·[M]=m⁵/(J·s), f 기준 1문장 명시). A4/A6/A7/A8/A9 = CR8 검증 무변경(A4 전제붕괴·나머지 유지). **빌드 GREEN**(8p·undef0·overfull0·에러0). 이월(HANDOVER [선택]): N_A 각주·γ/v_m 단위·(c)분류표 라벨·kinetics 박스라벨(초안 부록 cosmetic).
- **2026-07-07 P4 Ch2 ✅**: register 2(L755·L800 코드→모델) + **참고문헌 7 저자 보충(CrossRef raw JSON) + DOI 2 정정**(occupation 135634→134774[404]·hysteresis 05.060→05.052[오배정 fuel cell]) + vol/page 보강 + numverif v1.0.17 + PASS→확인 / C4 맺음 payoff 1문장(계산예제 round-trip<0.001μV/K·tab:qrev 부호교대·방법론출구) / eq:complete label 부여+(use-this)→(실전 사용식)+prose 참조 정합 / 용어 가역열→가역 발열 4곳·비가역열→비가역 발열 / 혼동금지 박스 keybox→warnbox·derbox(미사용) 삭제 / 헤더 L2·L36·L38 v1.0.17. **빌드 GREEN**(16p·undef0·overfull0·에러0·본문 코드참조 0). ⚠재확인(HANDOVER): standardised2024 저자 2인(CrossRef, 이례적)·numverif 코드ref bump.
- **2026-07-07 P3 Ch1 ✅**: ~42 편집 — register 23(제목/헤더/pdftitle "코드 진행→계산 진행"·버전 1.0.17·본문 코드/구현/dict/진입점/토글→물리·모델·내부라벨 삭제 2곳) + 수식주도 5(eq:lco-mit underbrace 전자항 명료화·L3039/L1914 (d)박스 라벨·#6 (b)(c) 단락분리) + 기호 8(T_c→T_{c,j}·q(T) 각주 disambig·s(ζ)→ŝ(ζ)·사전→대응표 3) + 완결 4(메모리→기억·마스터표 caption/label·T_rep/T_{c,j} 행) + gap G1/G3 태깅. **빌드 GREEN**(58p·undef0·overfull0·에러0). 본문 코드참조 누출 0(잔여=문건목표·구현대응표 appendix 정당). **이월(HANDOVER)**: N/n 통일·verifybox 감쌈(#11)·longtable(#25)·signcheck ✓열(#24)·표서식 micro(#26)·N3 물리재배열(#5)·z각주(#8)·ω다리(#9) = 저위험 아닌 구조/선택 or 신규발굴 → 후속.
- **2026-07-07 리뷰 정정**: S6 추출 오류 발견(사용자 지적) → 원본 사진 4장 master 직접 재추출 → Ch2 7·Appendix 9 복원, tex 교차검증. `V1017_REVIEW_COMPLETE.md` 확정.
