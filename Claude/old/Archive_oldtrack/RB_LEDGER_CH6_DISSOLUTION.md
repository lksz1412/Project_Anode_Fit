# RB_LEDGER_CH6_DISSOLUTION — Ch6 해체 + Ch1 부록 B 흡수 Result (2026-06-02 자율)

> 트리거: 사용자 지시 7("챕터 6을 없에고 각 챕터에 해당 내용들을 포함") + 본 세션 A과정 GO + "누락되는 내용 없도록 세세히". 핸드오버 §6-1.
> 원칙: 누락 0 + dangling ref 0 + 빌드 GREEN + 문건 보호(이전 result 덮어쓰기 X, 본 문건 신규).

## 1. 진단 (read-only 매핑 에이전트 청크 정독 기반, 확정)
- Ch1 은 이미 Ch6 코어(spectrum/kernel/volterra/planA/planB/fiteq/**simplefit**/falsify/**numeric**)를 §7~§15 로 보유, 전달절에 "Ch6 흡수" 선언 존재.
- Ch6 **고유분**(Ch1 미보유): ① index-1 DAE "왜 index-1" 유도 + 시간적분 T1~T5 ② dynamic vs OCV root Jacobian 구분 ③ 식별성 분리(R_n·χ_j 공선형, 3저항 EIS/ICA/calorimetry, 동시자유화 금지집합 eq:ch6_no_free) ④ 순차제약 실험절차(저속 OCV O1~O6 / GITT G1~G4 / 다온도 Arrhenius + ★A_j 고정해도 유효엔탈피 정정 boundbox / C-rate C1~C6) ⑤ closure 축약 카탈로그 3종 + Prony 완전단조성(eq:ch6_prony) + M1~M5 승격조건 ⑥ 금지 피팅편의 통합목록 ⑦ heat(calorimetry 부재 예측)·extension(충전·양극·full-cell) ⑧ AL-60~69(특히 64~69 신규) ⑨ 데이터 인벤토리 표.
- Ch6 내부 \ref 85개가 조밀 상호참조(kept↔grid/falsify/selfcheck/inherit) → **부분 발췌 시 dangling ref 다발** → 본문 전체 통째 흡수가 정답.

## 2. 실행 (Ch6 본문 140–806 → Ch1 부록 B 통째 흡수)
- **Ch1 부록 B 신설**: `\section*{부록 B — 유도식의 실데이터 피팅 워크플로 (구 Chapter 6)}\label{sec:ch1_fitting_practice}` (sec:ch1_numeric 뒤, 전달절 앞). Ch6 body 140–806(667줄)을 sed 바이트복사로 삽입(전사오류 0). 모든 ch6_* 라벨 유지(ch1_* 와 namespace 분리, 충돌 0건) → 내부 85 ref 전부 resolve, dangling 0.
- **Ch1 preamble 보강**: 매크로 16개(`\irr \rev \ct \transp \cb \dyn \sstat \conv \stt \hys \tar \loss \obs \tol \noise \brk`) + theorem box 4종(`linkbox verifybox practicebox loopbox`). Ch1 body 는 이 4 box 미사용(충돌 0).
- **bibitem 병합 4개**: brenan1996 · hindmarsh2005 · bernardi1985 · thomasnewman2003 (나머지 9개 cite 키는 Ch1 기존 보유).
- **부록 내부 prose reframe 9건**: "Chapter 6 은…/(Ch6)/Ch.3·Ch.6 검증" → "부록 B/본 부록"(코히런스 G-follow). 섹션 제목 3개 "(구 Chapter 6)" 병기.
- **전달절 갱신**: 흡수처에 부록 B(\ref{sec:ch1_fitting_practice}) 추가 + "Ch.6 은 해체되었다" 명시.
- **Ch6 파일 삭제**: `graphite_ica_ch6_rebuilt.tex` git rm.
- **Ch2~5 참조 재지정 21곳**: "Chapter 6 / Ch.6 / Ch6" → "Ch1 부록 B"(sed, 인코딩 검증). 전달 섹션 헤더 3개(ch4_transmit·ch5_transmit·ch5 전달) 문맥 다듬음.

## 3. 빌드·무결성 (GREEN)
- **Ch1**: 923 → **1591줄**. xelatex 3-pass EXIT 0, `!` 0, undefined ref/cite 0, dup label 0, **rerun 0**(부록 대량 신규 라벨 cross-ref 정착까지 3패스). overfull 21(6개 >20pt, 최대 138pt — 전부 Ch6 본문에서 따라온 cosmetic, 말미 sweep 예정). PDF → `Claude/results/graphite_ica_ch1_rebuilt.pdf`.
- **Ch2~5**: 각 2-pass EXIT 0, `!` 0, undefined ref/cite 0(prose-only 변경, 구조 불변).

## 4. 미결(잔여, 본 dissolution 범위 밖)
- (cosmetic) Ch1 부록 overfull 6개 >20pt sweep.
- 통합본 full_rebuilt 재생성 시 Ch6 제외 + 재작업 Ch1(부록 B 포함) 반영 — 전 챕터 검수 후 단순 concat 단계에서 수행.
- Ch6 selfcheck 표는 "부록 B 자체 검수표"로 잔존(메타지만 검증기록 가치, 폐기 안 함).

## 5. 누락 0 점검
- Ch6 27개 절 중 **선두 intro(98–139, 메타 framing) + bibliography 만 미흡수**. intro 의 GS-4'/GS-4'' 원칙 substance 는 흡수된 §epsilon(tolerance 근거화)·§forbidden(practicebox 격리)에 실현되어 있음 → 물리 substance 손실 0. bibliography 는 cite 키 union 으로 Ch1 bib 에 4개 병합 완료.
