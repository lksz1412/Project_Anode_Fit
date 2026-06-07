# Ch3–5 교과서 품질 전면 개정 계획서 (D2b 방식 sibling 적용)

> 상위 방식 문서: `2026-06-07-ch2-textbook-quality-overhaul-plan.md` (D2b). 본 계획은 D2b 방식을 Ch3·4·5에 동일 적용하는 sibling 확장이다. 방식 세부는 D2b 본문을 권위로 하고, 여기서는 챕터별 특이사항·단계만 기재한다.

## 1. Summary

Ch2에서 확정·검증(Codex MAJOR 0)된 교과서 품질 방식 D2b를 Ch3(반응속도론)·Ch4(통합 상태방정식)·Ch5(히스테리시스)에 동일 적용한다. 단일 통합 문건(Ch1 뒤에 이어 붙임) 전제로, 중복 인계 박스 제거·식 번호 N.x 체계·이전 장 수식 번호 지칭·식별성→Ch6 이관·결론/전달 절 삭제·친절(접근성) 서술을 수행한다. **Ch3·4·5는 이미 rigorous하므로 내용 thinning 금지 — 접근성만 개선하고 모든 수식·라벨·물리·식 번호를 보존한다.**

## 2. Scope / Targets

- 대상: `Claude/docs/graphite_ica_ch3.tex` (764L), `graphite_ica_ch4.tex` (842L), `graphite_ica_ch5.tex` (838L)
- 산출물 위치 동일(in-place 개정), Ch6 이관 재료 = `Claude/work/ch6_fitting_material/`
- 경계: Ch1(확정 exemplar)·Ch2(완료) 불변. Codex/ 폴더 read/write 금지.

## 3. Method (D2b 변환 6종, Ch2와 동일)

| # | 변환 | 위험도 | 비고 |
|---|------|--------|------|
| M1 | `\renewcommand{\theequation}{N.\arabic{equation}}` 추가(\title 앞) | 0 | 기계적 |
| M2 | §결론 절 삭제 | 0 | 교과서엔 논문식 결론 없음 |
| M3 | §전달항목(Chapter N→ 전달) 절 삭제/흡수 | 저 | 단일 문건 scaffolding |
| M4 | §1 inheritbox(C1–C7 재기술) → 신규기호 table 전용 + "그 외 기준식·규약은 직전 장들을 따른다(필요 시 식 번호 지칭)" 1줄 | 중 | 본문 (Cn) 참조를 식 (N.x)로 전환 동반 |
| M5 | 본문 "Chapter N 의 …" cross-ref → "식 (N.x)" 번호 지칭 | 중 | Ch1/Ch2 label-번호 맵 사용 |
| M6 | 식별성(identifiability) 내용 → Ch6 이관 추출(물리 kinetics는 잔류) | 중 | 혼재 절은 surgical split |
| M7 | 친절(접근성) 서술 패스 — **thinning 금지, 수식·물리 보존** | 고 | Codex 검수로 의미 drift 차단 |

### Ch1/Ch2 inherit 매핑 (M4/M5용 권위 맵)
- (C1) 전하보존 → 식 (1.1), Q_bg 식 (1.2)
- (C2) logistic → 식 (1.11), 도함수 식 (1.13)
- (C3) 완화 → 식 (1.16), 정전류 좌표 식 (1.18)
- (C4) 유효배리어·Eyring → 식 (1.27)·(1.23)·(1.17)
- (C5) 세 전위 → 식 (1.3)
- (C6) BV 방향성 장벽 → 식 (1.24)·(1.25)·(1.26)
- (C7) Ch2 두 force·reaction entropy → 식 (2.12)[∂U/∂T=ΔS/(sF)]·(2.29)[flux×force]·(2.31)[|I|η]

## 4. 챕터별 특이사항

- **Ch3**: §11 「온도 의존 kinetics 와 식별성」 = 혼재. eq:ch3_T·eq:ch3_eyring(ΔH‡/ΔS‡ 다온도 분리)는 **물리 → 잔류**; 공선형 쌍·eq:ch3_ident_chain·식별성 boundbox는 **→ Ch6**. §9 R_n 분해·§10 C-rate의 식별성 단서도 Ch6 포인터로. §12 전달항목·§13 결론 삭제.
- **Ch4**: §ch4_ident(748~) 식별성 → Ch6. §ch4_concl(796) 결론 삭제. inheritbox(Ch1–3) → table.
- **Ch5**: §ch5_ident(741~) 식별성 → Ch6. 결론 절(있으면) 삭제. inheritbox(Ch1–4) → table. 수치해법·validation pipeline은 이미 "Chapter 1 부록 B(=Ch6)로 분리" 명시 → Ch6 포인터 정합.

## 5. Steps (cumulative; Ch2 plan 이후 연속)

- S30: Ch3 전문 정독 (완료)
- S31: Ch3 M1·M2·M3 (eq#, 결론·전달 삭제)
- S32: Ch3 M4 (§1 table-only + (Cn)→식번호)
- S33: Ch3 M5 (본문 cross-ref 번호화)
- S34: Ch3 M6 (§11 식별성 Ch6 추출, kinetics 잔류)
- S35: Ch3 M7 (접근성 패스, 보존)
- S36: Ch3 빌드 clean + Codex foreground 검수 until MAJOR 0
- S37: Ch3 커밋·푸쉬 + 결과 ledger
- S38–S45: Ch4 동일 루프
- S46–S53: Ch5 동일 루프

## 6. Gates (확인 가능 조건)

- G-build: `xelatex` 2-pass exit 0, `Output written … (Np pages)`, undefined ref 0(`grep -c "undefined" build.log`=0), Overfull hbox 0
- G-preserve: 변환 전후 `\label{eq:chN_*}` 집합 불변(식별성 이관분 제외), boxed 수식 개수 불변 — `grep -c 'boxed' ` 전후 비교
- G-codex: Codex foreground 검수 결과 MAJOR=0, 부호사슬 일관 확정
- G-numref: 잔존 "Chapter~?[0-9]" 본문 cross-ref(서론·표 의미설명 제외) → 식 번호로 전환됨을 grep 확인
- G-ident: 식별성 핵심(공선형 쌍·ident_chain) 본문 부재 + Ch6 재료 파일 존재

## 7. Risks

- R1(thinning): 친절 패스가 rigorous 내용을 축소 → **금지**, Codex로 검출. M7은 prose만, 수식 블록 불변.
- R2(meaning drift): cross-ref 번호 오매핑 → §3 맵 권위, 빌드 ref 검증.
- R3(식별성 over-extraction): kinetics 물리를 식별성으로 오인 이관 → 혼재 절은 수식 단위로 분리.
- R4(컴팩션): 챕터 단위 완결·커밋·ledger로 복구지점 확보.

## 8. Dependencies

- Ch1/Ch2 .aux label 맵(추출 완료). Ch2 완료본(42ff6ee) = register/구조 reference.
- xelatex(MiKTeX kotex), Codex foreground(codex:codex-rescue, --wait).

## 9. Validation

각 챕터 S36에서 G-build·G-preserve·G-codex·G-numref·G-ident 전수 통과. 통과 전 커밋 금지.

## 10. Rollback

각 챕터 in-place 개정 전 git 상태가 복구지점(이전 커밋). 실패 시 `git checkout -- <file>`로 환원.

## 11. Correction History

- 2026-06-07: 최초 작성. Ch2 D2b 완료(42ff6ee) 직후, 밤샘 인계("챕터2~5 진행")의 GO-until-done 규율로 Ch3–5 연속 진행 착수. 사용자 명시 "챕터2 다시 작업해와"는 Ch2 완결로 충족; Ch3–5는 동일 방식 sibling 적용(중복 method 재확정 불필요, D2b 권위 승계).
