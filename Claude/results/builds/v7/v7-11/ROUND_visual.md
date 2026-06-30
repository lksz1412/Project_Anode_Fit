# ROUND_visual — v7-11 시각·그림·형식·완결성 검수 (PDF 렌더 판독)

대상: `v7-11.tex` (890행) + `v7-11.pdf` (17p, A4). 렌더 = `pdftoppm` 110/150/200 dpi.
기준: `v7-00_spine/AUTHOR_BRIEF.md` (§5 그림 규약·§4 형식). refute mandate·가장 약한 1곳·빈 통과 금지.

---

## 1. 그림 5개 — 판정 (혼란 유발 유무 = 핵심)

| 그림 | 위치 | 신규 TikZ | 내부텍스트 ASCII | \ref orphan | 식 정합 | 혼란 유발 | 판정 |
|------|------|-----------|------------------|-------------|---------|-----------|------|
| `fig:spine` | p2 | O | O (N0–N9, loop) | 0 (서론 1회) | spine 노드 순서 = 절 순서 정합 | 없음 | PASS |
| `fig:staging` | p5 | O | O (stage 4/3/2L/2/1, lith/delith) | 0 (§1.1 1회) | 4 전이 = `GRAPHITE_STAGING_LIT` 정합 | 없음 | PASS |
| `fig:hysloop` | p8 | O | O (overshoot, ξ_s±, ΔU_hys) | 0 (§1.3 1회) | **spinodal 부호순 정합(아래)** | 없음 | PASS |
| `fig:logistic` | p10 | O | O (ξ_eq, w|dξ/dV|) | 0 (§1.5 1회) | logistic·종 미분 정합 | 없음 | PASS |
| `fig:reversal` | p13 | O | O (discharge/charge 2-panel) | 0 (§1.8 1회) | 충전 거울·격자 역전 방향 정합 | 없음 | PASS |

**혼란 유발 그림: 0개.** 5개 모두 신규 TikZ·내부 텍스트 영어 ASCII 전용(한글 0)·캡션만 한글. 각 그림 = 앞 식이 동기·뒤 본문이 사용.

### 가장 약한 1곳 (적대 검산) — `fig:hysloop` spinodal 방향
브리프가 최고위험으로 지목한 그림. 200 dpi 판독으로 식 대조:
- `eq:spinodal` ξ_s^± = ½(1±u) ⇒ ξ_s^− < 0.5 < ξ_s^+. 그림: ξ_s^− = 좌상(ξ≈0.146, 곡선 **극대**), ξ_s^+ = 우하(ξ≈0.854, 곡선 **극소**). Ω=4RT ⇒ u≈0.707, ½(1−u)≈0.146 — **좌표 정확 일치**.
- discharge overshoot = ξ≈0→극대 ξ_s^−(상승 가지, 좌상 굵은 경로). charge overshoot = ξ≈1→극소 ξ_s^+(우하 굵은 경로). 방향 정합.
- y축 = (sF/RT)(V_eq−U_j): discharge 극대 = +1.066(높은 V), charge 극소 = −1.066(낮은 V) ⇒ U_dis>U_chg(`eq:Ubranch` 부호 일치). **부호순 결함 0.**
- γ→0 plateau at U_j (y=0) 표기로 가역 한계도 시각화 — 이해를 돕고 혼란 없음.

---

## 2. 표 4종 — 가독성

| 표 | 위치 | 열수 | 오버플로/잘림 | 페이지 분리 | 판정 |
|----|------|------|----------------|-------------|------|
| notation longtable | p4–5 | 3 | 본문 무넘침(\code 셀 underfull 다수·아래 §3) | `\endhead` 헤더 반복으로 양 페이지 가독 | PASS |
| `tab:staging` | p14 | 8 | 무 — 4전이·8열 booktabs 정렬 정상 | 단일 페이지 | PASS |
| `tab:inputs` | p15 | 4 | 무(표 본체) — 3 그룹(전이키/생성자/호출) 정상 | 단일 페이지 | PASS |
| `tab:nodemap` | p16 | 4 | 무 — N0–N9 10행 정렬·식↔코드 매핑 정상 | 단일 페이지 | PASS |

**표 가독 결함: 0개.** longtable 헤더 재출력·booktabs 룰 정상, 4종 모두 잘림 없음.

---

## 3. 시각 — overfull/underfull·헤더·페이지번호

- **Overfull \hbox 4건**(전부 경미, 본문 외관 영향 미미):
  - L193 (4.62pt) — notation longtable `func_w/func_w_eff` 셀
  - L202 (17.33pt) — longtable `center,func_U_branch` 셀 (가장 큰 셀 넘침이나 longtable 셀 내부, 렌더상 인접 셀 침범 관측 안 됨)
  - L386–391 (2.15pt) — §1.3 본문 `func_U_branch(...)` 인라인 코드
  - L787–790 (22.55pt) — §1.9 본문 단락(코드 식별자 없는 산문, ~2자 마진 초과; 렌더상 우측 거의 닿음, 잘림 아님)
- **Underfull \hbox 10건**: 9건이 notation longtable 셀(L180–211, 좁은 p{} 열이 단어 못 채워 badness 10000). 시각 결함 아님(좁은 열의 구조적 부산물). 1건 L611–615 codebox.
- **헤더/페이지번호 3-pass 수렴**: 모든 페이지 `\thepage/\pageref{LastPage}` = `n/17` 정상 표시, `17/17` 마지막 페이지 LastPage 해소 확인. lhead 한글 헤더 정상 렌더.

**시각 심각 결함: 0개** (overfull 최대 22.5pt = 본문 ~2자, 잘림·가독 저하 없음 — LOW).

---

## 4. 형식 — 수식 주도·전보체·절 다리·완결성

- **수식 주도**: 24개 번호식 전부 `\eqref` 참조(orphan 0), 핵심 결과식 `\boxed` 처리. 논리를 식 사슬이 운반.
- **완결성(orphan 0)**: 그림 5/표 3(라벨) 전부 ≥1 `\ref`, 식 24 라벨 = 24 unique eqref. 모든 추가물 앞 동기·뒤 사용.
- **절 다리**: 각 절 도입(앞 절 인수)·마무리(다음 절 다리) 확인 — 예 §1.2 말미 "다음 절은 …U_j(T)으로", §1.3 말미 "다음 절 평형 점유로" 등 연결 정상.
- **괄호 전보체**: 렌더 본문 표본 점검상 주술 갖춘 보충은 완결 문장, 괄호는 식·기호 병기 위주. 위반 미발견.
- **6단계 재현 keybox**(p15) + `tab:inputs`(전 인자) + `tab:staging`(초기값) = G-usable 닫힘 시각 확인.

**형식 결함: 0건(심각도 기준).** (overfull 4건은 §3에서 LOW로 별도 계상.)

---

## 종합
- 신규 TikZ 5개 전부 ASCII·orphan 0·식 정합·혼란 유발 0.
- 표 4종 잘림·오버플로 0(본체), longtable 헤더 반복 가독.
- overfull 4건 전부 LOW(최대 22.5pt, 잘림 아님)·underfull은 좁은 셀 구조 부산물.
- 헤더·페이지번호 17/17 수렴. 형식(수식주도·다리·완결성) 결함 0.
- 가장 약한 1곳 = fig:hysloop spinodal 방향 → 적대 검산 PASS.
