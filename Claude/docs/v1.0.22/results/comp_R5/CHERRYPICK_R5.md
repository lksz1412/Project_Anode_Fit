# CHERRYPICK_R5 — 마스터 체리픽 판정 (Step 51~52 집행 기록, 2026-07-17)

## 절 단위 판정 (3창 경쟁 → best-of + 그래프팅)
| 절 | 채택 | 근거 | 그래프트·수정 |
|---|---|---|---|
| §3.1 생존 지도 | **W3**(교육) | arc 서사·판정표 캡션의 LCO 대비("다섯 결")·지도=목차 동선 — 교육 가치 최대. 확립 사실 8건 노드별 재배열 | `표~\eqref{tab:lco-staging}`→`\ref` 오식 정정 |
| §3.2 케이스별 | **W2**(실측) | tier 각주 6건(상충=처리·조성 차 명시)·열특성 소절(−40~−105 μV/K)·확인 필요 명시 밀도 최고 | `sec:si-survival`→`sec:si-map` 재지정 |
| §3.3 블렌드 | **W1**(이론) | (a)~(d) 유도 사슬·검산 3건(유일근 이월·f_Si→0 회수 eq:blend-limit·부호)·GS-2 층 분리 논증 최정밀 | +W3 `eq:blend-dqdv` 합성식 그래프트(키박스 연동)·`ssec:si-anchor-body`→`ssec:si-carry`·키 정규화(ai_composite2022·zhan_siox2026) |
| §3.4 기계 히스 | **W1**(이론) | 가역 결합 실제 닫힘(eq:si-lcmu→vshift→coupling, Λ_σ=v̄/F ~O(100 mV/GPa) 마스터 물리 검산 통과: 부호·대수·크기 전건 옳음)·공백을 소성 구성식으로 1단계 좁힘 | `arnot_si2021`→`arnot_calorimetry2021` |
| §3.5 코드 명세 | **W3**(교육) | 실 코드 식별자(GraphiteAnodeDischargeDQDV·*_LIT) 참조·bit-exact 계약식·GS-1/GS-2 코드 경계 1:1·σ 오프셋 훅 | 라벨 재지정 5종(eq:blend-fsi→balance·ssec:blend-*→si-blend-*·eq:si-lc-U→eq:si-vshift·k_σ→Λ_σ) |
| 기호표 | **W3** 기반 정합화 | 표 형식 완비 | 채택 본문 기호로 통일(k_σ→Λ_σ·V̄→v̄·ΔU_mech→ΔV^mech)·도입 절 라벨 재지정 |
| 미채택 | W1 s31·s32·s35 / W2 s31·s33·s34·s35·notation / W3 s32·s33·s34 | 경쟁 보관(comp_R5/W* — 삭제 없음). W2 tab:blend-evidence 는 W1 srcbox 와 중복이라 미그래프트(기록) | — |

## 집행 검증
- 서지: 후보 19키 전건 **Crossref 재생성 등재**(전 저자·권·쪽 — 기억 서지 0). 정정 2건: arnot 쪽 110536→**110509**(Crossref 기준)·ogata article 4217 유지(Crossref article-number 요동 — DOI 접미 기준, 원장 비고). lee_sic2025 = early view(e04250·권 미배정).
- appD 은퇴: `ch1_appD_si` 조립 제외(§3.1 이 본문체 대체 — 파일은 보존·자산 이력 유지). 유일 의존(ch3v22_notation 의 ssec:si-gap)은 기호표 확정판 대체로 해소.
- 자산 앵커 [V22-R5-01]~[V22-R5-26] 일련 재번호(창 간 충돌 해소). 서술형 앵커라 구조 도구 카운트 밖(V21 계열과 동일 규약 — 게이트 357 은 Ch1+Ch2 불변).
- 빌드: ch3 16p(5→16)·err0·미해소 0·cite-undef 0·bib-uncited 0·구조 PASS·boxed 2(eq:blend-balance·eq:si-coupling).
