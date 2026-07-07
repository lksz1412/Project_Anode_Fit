# HANDOVER v1.0.17 — 교재 register·정합·완결성 정련 + Ch2 서지 보강 (이규섭 리뷰 완전 반영)

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.17/HANDOVER_v1.0.17.md` (v1.0.17 완결)
- 근거 = `results/process/V1017_REVIEW_COMPLETE.md`(이규섭 S6 재추출·완전목록) ← `docs/v1.0.16/HANDOVER_v1.0.16.md`(n(T) 지원) ← `docs/v1.0.15/CLOSING_v1.0.15.md`(헌법 3종·확정 w/T) ← `docs/v1.0.15/HANDOVER_v1.0.15.md`(격자 퇴출) ← v1.0.14 ← …
- 레저/fix-list = `results/process/V1017_EXECUTION_LEDGER.md`·`V1017_FIXLIST_CONSOLIDATED.md`. 커밋 = 423f7d5(P1+P3 Ch1)·f227ffc(P4 Ch2)·d398dbf(P5 Appendix)·P6(본).

## ① 본 세션 지시·작업 요약
**지시**(사용자): 외부 리뷰 `S6_AnodeFit_review.md` 참고 → v1.0.16 기반 v1.0.17 작성. 타당한 것만 걸러 반영. **9종 체리피킹**으로 제대로. 출근 중이라 피드백 불가 — 팝업·대기 없이 자율·완성 시 commit+push. 하위 모델로 서칭, master 는 고등 작업.

**★추출 오류 정정(핵심)**: 원 추출물 `S6_AnodeFit_review.md` 는 **Ch1 26항목만 뽑고 Ch2·Appendix 를 통째 누락**한 뒤 "Ch2 미포착"이라 거짓 기재. 사용자 지적으로 **원본 사진 4장(idx 481-484) master 직접 재추출** → Ch2 7·Appendix 9 복원, 실제 tex 교차검증 → `V1017_REVIEW_COMPLETE.md` 확정.

**방법**: 9종 체리피킹 = sonnet 리뷰어 9(Ch1 register/수식주도/기호/완결 4·Ch2 3·Appendix 2) + CrossRef 저자조회 1 병렬 → master(opus) 체리픽·적대검증·정밀 적용. SEED 엄정 검증 + 신규 다수 발굴(CR1 register 15·CR3 기호 3·CR4 완결 2). SEED 정정: #3 "결합"→실제 "결함", #6 병합 2곳→1곳, #9 ω_j→ω_i, #4 q→ζ 충돌→q_int.

**완주(P1–P6, 전 phase commit+push)**:
- **P1 증판**: docs/v1.0.16 → v1.0.17(코드 matched bit-exact·회귀 PASS·3-tex 빌드 GREEN).
- **P3 Ch1(~42편집)**: register 23(★제목/헤더/pdftitle "코드 진행→계산 진행"·버전 1.0.17·본문 코드/구현/dict/진입점/토글→물리·모델·내부라벨 삭제 2) + 수식주도 5(eq:lco-mit underbrace 전자항 명료화·(d)박스 라벨 2·(b)(c) 분리) + 기호 8(T_c→T_{c,j}·q(T) 각주·s(ζ)→ŝ(ζ)·사전→대응표 3) + 완결 4(메모리→기억·마스터표 caption/label·T_rep/T_{c,j} 행) + gap G1/G3.
- **P4 Ch2**: register 2·**참고문헌 7 저자 보충(CrossRef)+DOI 2 정정+vol/page**·C4 맺음 payoff 1문장·eq:complete label+(use-this)→(실전 사용식)·용어 가역열→가역 발열·박스 keybox→warnbox·derbox 삭제·헤더 v1.0.17.
- **P5 Appendix**: A1 date 1.0.17·A2 소스주석 이력 보존·A3 §1.7 리터럴 참조·A5 κ/M 단위+f 부피밀도 기준(CH 차원정합).
- **P6 마감**: 3대 무결(회귀 bit-exact·Ch1 58p·Ch2 16p·appendix 8p·전 undef0·overfull0) + 적대검증 + HANDOVER·INDEX.

## ② 다음 세션 주의
1. **★가장 눈에 띄는 변경 = 제목/헤더 문구**: Ch1 pdftitle·러닝헤더·챕터 제목·서론의 "**코드 진행을 따라가는**" → "**계산 진행을 따라가는**"(본문 L138-142 이미 "계산"). register 테마(교과서=물리 서술, 코드는 구현 대응표에만)의 최대 노출 사례라 반영. N0–N9 파이프라인 구조·문건 목표("이 문건만으로 재현 코드 작성 가능")는 유지. **원치 않으면 여기부터 되돌리면 됨**(v1.0.16 동결).
2. **참고문헌 DOI 2건 정정**(실오류 수정): occupation2019 `135634`(404) → `10.1016/j.electacta.2019.134774` · hysteresis2018 `05.060`(오배정=fuel cell 논문) → `10.1016/j.jpowsour.2018.05.052`. 저자 7건 = CrossRef raw JSON. **⚠standardised2024 저자 2인(A. Hales, J. Bulman)은 CrossRef 기준이나 이례적 — 원문 재확인 권장**.
3. **코드 무변경**: 물리·방정식·수치·알고리즘 불변 = matched version bump만. 회귀 골든 bit-exact(재캡처 불요). v1.0.16 이월(다온도 per-T n 진단·two-phase 폭 T-의존·LCO 실값) 그대로 유효.
4. **부록 A2 소스주석**: v1.0.14 는 "최초 작성" 이력 스탬프라 **버전업 시에도 보존**(A1 렌더링 date 만 현행 1.0.17). 향후 재플래그 금지.

## ③ 미완료/이월 (v1.0.17 [선택]·신규발굴 후속 — 물리·필수 아님)
9종 체리피킹이 발굴했으나 저위험 아닌 구조/cosmetic or 신규발굴이라 이월(다음 정련판 후보):
- **Ch1**: verifybox/derivbox 활성화(#11, "극한 검산" 5곳)·longtable 통일(#25 tab:inputs·nodecode)·signcheck-R 판정열 ✓(#24)·표 서식 micro 통일(#26)·N3 그룹 물리적 재배열(#5, 그룹헤더 분할 필요)·z 4번째용례 각주(#8)·ω_0→ω_i→ω_k 다리(#9)·§sm-lattice N/n 대소문자 통일(CR3 신규)·L1017/L1159 (b)(c)·(d)순서(CR2 신규).
- **Appendix(초안)**: N_A(아보가드로) vs N_A(A종수) 각주(CR9 신규)·γ 옆 v_m/Δg_v 단위 병기(CR9 신규)·(c) 중간식→분류표 라벨(L252)·§app:kinetics 두 소절 (a-d) 박스 라벨(CR9 신규).
- 상세 = `V1017_FIXLIST_CONSOLIDATED.md`.
