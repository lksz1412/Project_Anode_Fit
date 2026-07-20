# gr_2L_b — refine_b NOTE (Phase-② improver)

대상: `_sections/ch1_sec05b_gr2L.tex` (live) 의 비파괴 개선 사본 → `refine_b/gr_2L_b.tex`.
방향(수정 지시)만 받고 해법은 자체 판단. live 파일 미편집. refine_b/ 밖 어떤 파일도 미접촉.

---

## 1. 무엇을 왜 바꿨나 (direction 1·2 대응)

### Direction 1 — §7 분류 위임을 문장 단위로 airtight 화
문제: 일부 문장이 "두-상4 + 고용체1"(dilute 1'→4·3→2L·2L→2·2→1 = 두-상, 4→3 = 고용체) XRD 분류를
**단정**하는 것으로 읽힐 위험. 이는 §7(`sec:broadening-class`)의 분류(dilute→4·4→3·3→2L = 고용체,
2L→2·2→1 = 두-상)와 정면 충돌. (CHERRYPICK_R1.md line 24·27 이 "9창 전부 이 단정 → 전부 §7 위반,
'§7 분류 단정 재도입' 은 이식금지" 로 확인.)

- **(d)(ii) 전면 교체 [핵심].** 삭제: "세분에서 4→3 을 연속 고용체 shoulder 로, **나머지를 두-상으로 배치**"
  — 이 한 구절이 dilute→4·3→2L 을 두-상으로 (§7 과 반대로) 배치하는 잔재였음. 대체: 5-feature 시드는
  staging 특징의 **개수·위치(XRD 구조 해상도)만** 세분하고 **전이별 두-상/고용체 상성격은 배정하지 않는다**;
  성격 확정은 세분 전과 똑같이 §7(실측 plateau) + 피팅된 Ω_j 소관, 본 시드가 분류를 다시 여는 것이 아님.
- **도입부 (i) 보강.** "판정자" 뒤에 "(전이별 분류를 확정하는 도구가 아니라 그 판정 기준 --- 확정은 §7 소관)"
  삽입. 판정자가 판결이 아니라 기준식임을 첫 등장에서 못박음.
- **(a) 도입 문장 완화.** "…화학퍼텐셜 부호가 **정한다**" → "…부호가 **준다**(이 기준이 전이별 분류를 혼자
  확정하지는 않고 §7 실측 plateau 와 맞물리는 방식은 아래 검산에서 닫는다)". 판정식이 분류를 단독 결정한다는
  읽힘 제거.
- **(a) 후단 보강.** "이 부등호가 실재 전이를 두-상/고용체로 확정하는 것은 아님은 아래 검산에서 §7 과 맞춘다"
  괄호절 추가. "판정은 이 한 부호다" → "판정 **기준**은 이 한 부호다".
- **warnbox (iv) 보강.** "…기준 4-전이를 대체하지 않는다" → "…대체하지 않고, **전이별 상성격도 배정하지
  않는다(그 성격은 §7 + 피팅된 Ω_j)**".

### Direction 2 — 역사적 stage명 ↔ 표 행 대응(gate-7) 정밀화
문제: 원 (iii) 이 "표의 고전위 행 4→3(0.21V) ↔ 세분 시드의 dilute 1'→4 슬롯에 대응, 세분은 그 사이에
4→3 shoulder 를 하나 더 끼운다" 로 서술 — 이는 표의 4→3 을 dilute 1'→4 로 **개명**하는 셈이라 "표 라벨
보존" 과 모순되고, 5-feature 라벨과 4-전이 기준선을 혼동시킴.

- **(iii) 전면 교체.** 명확한 "4 + 추가 1" 프레임으로 정정: 피팅 기준선 = 표의 **네 행**
  {4→3, 3→2L, 2L→2, 2→1}; 5-feature 시드 = 그 네 행을 **라벨 그대로 1:1 로 물려받은 위에** 고전위 끝에
  dilute 1'→4 **하나만** 더 얹은 것(5 = 표의 4 + 추가 1). 더한 그 한 특징은 §7 이 이미 고용체로 분류·명명한
  dilute→stage4 영역(표는 별행 없이 고전위 끝에 접어 둠). 표의 네 행은 개명·재배치 없음.
  이 대응은 §7 line 14–15("dilute→stage4 영역**과** 4→3·3→2L 두 전이(각각 표의 4→3·3→2L 행)")와 정확히 일치.
- **keybox 정밀화.** "…4-전이 기준을 보존하는 추가 후보" → "…4-전이 기준을 **라벨 그대로** 보존하고 고전위 끝
  dilute 1'→4 하나만 더 얹는(5 = 4 + 1) 추가 후보(선택 시드, **상성격은 §7 소관**)".

### 부기
- 헤더 주석에 refine_b 변경 요지 4줄, 말미 자산주석 [GR2L-1]·[GR2L-5]·[GR2L-6] 태그를 변경 반영해 갱신.

---

## 2. 자기 회귀검사 (self regression-check)

- **\eqref/\ref 타깃 존재(전수).** 사용된 외부 라벨 10개 모두 실재 확인(grep):
  `eq:wbase`(ch1_sec05_width), `eq:gpp`·`eq:spinodal`(ch1_sec04_hys), `eq:Uj`·`fig:UjT`(ch1_sec03_center),
  `eq:gxi`(ch1_sec02b_part0), `tab:staging`·`sec:sum-staging`(ch1_sec10_sum),
  `sec:broadening-class`(ch1_sec07_broadening), `sec:width`(ch1_sec05_width).
  자체 정의 라벨 5개: `ssec:gr-2L`·`eq:gr2l-mu`·`eq:gr2l-disc`·`eq:gr2l-split`·`eq:gr2l-box` (모두 본 파일 내 정의).
  **존재하지 않는 라벨 신규 참조 0.** 인용 5개(dahn1991·ohzuku1993·persson2010b·reynier2003·schmitt2022)
  모두 기존 키(신규 cite 도입 0 — persson2010b 는 기존키 유지).
- **§7 과의 신규 모순 없음.** (d)(ii)(iii)·(a)·(i) 모두 이제 분류를 §7 로 위임하거나 §7 분류에 **동의·귀속**만
  한다(dilute→4 = 고용체 를 "§7 이 분류한" 으로 귀속). "두-상4+고용체1" 단정 문구는 전부 제거됨. verifybox 의
  "regsol2 Ω_j/RT 전부 >2 이나 확정은 실측 plateau" 정합 논증은 §7 line 23–26 과 동일 논리라 유지.
  tab:staging **미편집**(+15/−14 는 초기값 갱신 대상=피팅 target 으로만 제시, 표 수치 불변). stage-2L 은
  다온도 서명(상온 R² 이득 아님, −0.44%p 하락 caveat 유지)로 유지.
- **괄호·환경 균형.** 스크립트 검사: `{` 233 / `}` 233 균형(`\{`·`\}` 제외 후). 환경 begin/end 카운트 일치
  — equation×4, aligned×1, verifybox·srcbox·signbox·warnbox·keybox 각 1. `\boxed` 1개(eq:gr2l-box) 보존.
- **원본 대비 diff.** 변경은 헤더주석·(i)·(a)·(d)(ii)(iii)·warnbox(iv)·keybox·자산주석에 국한(surgical).
  boxed 4식 본문·verifybox·srcbox·signbox·warnbox(i)(ii)(iii)(v)·적대 3점 블록은 byte 단위 불변.

---

## 3. 의도적으로 그대로 둔 것 (강점 보존)

- **판정자 유도** eq:gr2l-mu → eq:gr2l-disc (로그항 항별 미분·θ=½ 에서 4RT−2Ω·eq:gpp 대칭점 동치) 전체 유지.
- **boxed U(T) 분리 지도** eq:gr2l-box + FWHM≈3.53 w_j 임계 — 라벨·식 불변(하드제약 e).
- **verifybox**(§7 정합·과대주장 금지·경계값 2.02 민감점) — 이미 airtight 한 위임 논증이라 골자 보존(제목·귀결 그대로).
- **srcbox**(단일 Ω_j = 다중-부분격자 평균장 축약·persson2010b·근사 한계) 유지.
- **signbox**(0.30 mV/℃ 분리·10℃ 병합·schmitt2022 operando XRD 부호정합·reynier2003) 유지.
- **warnbox** 정직한 한계 (i) 절대 ΔS vs 차 (ii) 온도등급 미검증·tier B (iii) 분류 §7 소관 (v) ★상온 R²
  −0.44%p 하락 caveat — 전부 유지(하드제약 c·d).
- **w_eff = (RT/F)(1−Ω/2RT) 다리**(판정자 강성 ↔ eq:wbase 폭 이중지위 연속화) 유지(하드제약 3).
- **역사적 명칭 가드**(stage번호 ↔ ver.N/Chapter N 무관) 및 tab:staging 초기값 +15/−14 를 피팅 target 으로만
  제시하는 처리 유지.

### 남긴 판단 노트 (추가 수정 안 함)
- keybox 의 "tab:staging" 은 원문이 라벨명을 그대로 텍스트로 쓴 관행(P5 이름 보존)이라 `\ref` 로 바꾸지 않음.
- verifybox 문두 "판정자와 §7 분류의 정합" 은 이미 §7 로 위임하는 강점이라 재작성하지 않고 그대로 둠.
