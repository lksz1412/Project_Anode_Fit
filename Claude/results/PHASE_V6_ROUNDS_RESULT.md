# PHASE V6 RESULT — Ch1 플로우차트-순서 재조립 (v6)

> 마스터 = `Claude/plans/2026-06-22-ch1-v6-flowchart-reassembly-MASTER.md`. 베이스 = v5(V5RR 검증판, 불가침). 플로우차트 = BD `Lib_LKS_BatteryData_99_Anode_Fit.py` 코드 파이프라인(헤더 코멘트로 추가 완료).

## 1. 목표·범위
BD 코드(이 문건 기반)의 계산 흐름도 순서로 v3~v5 문건을 v6 으로 재조립. point0 시작값 도입·point1 흐름도 순·point2 무관 토픽만 배제·point3 의존 보존·point4 요약 아님·완성도 보존. §1.18 배제.

## Phase V6.0 — 설계 (완료)
- BD 코드 전문 정독 → 플로우차트 구성(코드 헤더 코멘트로 추가, Task A) → 코드 완성도 검토(point0, `BD/Claude/results/ANODE_FIT_code_completeness_review.md`).
- 마스터 플랜: 플로우차트→절 배열 맵 + 의존 안전 증명(V5RR 의존그래프) + 배제≈0 보수 분석.

## Phase V6.1 — 재조립 (완료)
### 수행
- v5 절 블록을 플로우차트 순서로 재배치: notation→rate→thermo→fwdrev→regsol→**hys**→charge→eqpeak→lag→potbranch→tempbranch→synth→overlap→**master→hyspol**→falsify→code.
- ★핵심 이동 2: (a) §1.13 hys(분기중심)을 §1.5 직후로 — 코드 전이루프 첫 단계가 branch_center. 의존 안전: 식 1.84~1.91 ← isotherm(1.29)·gpp(1.39)·spinodal(1.40)=전부 §1.5만. (b) §1.15 master 를 §1.14 hyspol 앞으로 — master ← 1.79/1.82/1.91/1.45(전부 앞), hyspol ← 1.51/1.45/1.91(전부 앞).
- **Part A 시작값 절(point0)**: §1.1 직후 `sec:inputs` 신설 — 실험 시작값 U_j/(H_j,S_j)·w_j·Q_j·(H_a,j,S_a,j)·Ω_j,γ_j 과 진입 식(eqref) 표 + 흐름도 순서 예고. 새 물리 아님(기존 식의 입력 명시).
- 재배열로 식 번호 재계산 → 임베디드 §1.17 코드 listing 하드코딩 번호를 v6 aux 기준 동기(hysdU 1.88→1.46·hyscenter 1.91→1.49·lnLq 1.69→1.77·vapp 1.45→1.53·simplefit 1.79→1.87 등). 공유 companion `.py`(v5)는 불가침 — v6 listing만 수정.

### 빌드·정합
- build_gate Opus_v6 **0/0/0 41p**(v5 40p + 시작값 절 1p). undef(reference) 0 — **재배열이 모든 \eqref/\ref 보존**(라벨 기반). 2 'undefined'=한글 italic 폰트 shape 경고(v5 동일·무해).
- v6 listing↔v6 aux 14/14 정합(임베디드 코드 번호 동기 완료).

### 의존 검증 (point3) = PASS (V6.1 범위)
재배열 후 빌드 cross-ref 0 undefined + 이동 2건의 선행집합이 전부 앞에 옴(의존그래프 대조). 절내 식 사슬 무변경(블록 통째 이동).

## 2. Next (V6.2~V6.4)
- **V6.2**: 프로즈 정합 — 서론 roadmap 을 흐름도 순으로 resync + 절간 다리(이동된 §1.13/§1.15 전후) 재봉합 + forward 참조 자연스러움. (point3 논리 무붕괴 prose 측면.)
- **V6.3**: N회 가변-청크 검수 — 완성도 v5≥ 대조(97식·표·figure·코드 누락 0, point4) + 배제 토픽 재확인(point2, 보수) + 시각 렌더 + 수렴.
- **V6.4**: 종합 게이트·RESULT 11항목·commit.

## 4-tier (V6.1 시점)
- 확정: 구조 재조립·식번호 동기·빌드 GREEN·이동 2건 의존 안전.
- 미검증(V6.2~3 예정): 프로즈 절간 다리 정합·완성도 대조(누락 0)·배제 토픽 재확인·N회 검수.

## Phase V6.2 — 프로즈 정합 (완료)
재배열 seam 프로즈 스캔(sub) + master 삼각. 수정 4건(전방참조-과거형·옛 순서 잔재 해소):
1. ★master 도입(CRITICAL) — "hyspol의 eq:hysobsgap까지로 조각 준비됐다"(hyspol은 이제 master 뒤) → "분기 중심(§hys)까지로 방전·확장 조각이 준비됐다".
2. 서론 roadmap — "방전 본론=§rate–§overlap, 히스=§hys 이하"(hys가 이제 그 안) → 흐름도 순 전개 서술(평형→상분리·분기중심→관측·peak→동역학→닫힌식·합산→통합식→관측gap→반증→구현)로 재기술.
3. regsol 도입 — charge 먼저·hys 나중 나열(hys가 바로 다음) → hys 먼저.
4. ★hys 도입 — "방전 본론은 eq:total로 닫혔다"(eq:total은 이제 뒤) → "상분리(§regsol)가 등온선 비틀어 준안정 갈래 낳았다"(sub가 OK로 넘긴 걸 master 재검증으로 적발).
빌드 0/0/0 41p, listing↔aux 유지.

## Phase V6.3 — 검수 (완료, 수렴)
- ★point3 의존(재배열 후 선행<자신): 그래프 97식 검증 — 위반 2(binodal↔gprime·simplefit↔areacons)는 **v5에서도 동일 forward("다음 식이 봉인") 패턴 = 내재**, 재배열이 만든 위반 0(스크립트 확인). 이동 2건(§hys·master/hyspol) 위반 0.
- ★point4 완성도: v5 97식 = v6 97식(누락 0·추가 0), figure 16=16·boxed 13=13·코드 2=2, table 8→9(시작값 +1, 손실 아님). **요약 아님·완성도 보존 확정.**
- 시각+홀리스틱 fresh sub: **확정 결함 0**(41p 잘림·겹침·overfull·그림충돌 0; TOC·서론 roadmap·새 seam 도입문·sec:inputs 정방향 예고 전부 정합). 경미 개선 1 = sec:inputs 표 행을 흐름 순(U,w→Ω,γ→Q→ΔH_a)으로 재배열 적용.

## Phase V6.4 — 최종 종합 (완료) · ★RESULT 11항목
1. 목표·범위: BD 코드 흐름도 순서로 v3~v5를 v6 재조립. point0 시작값·point1 흐름도순·point2 무관배제·point3 의존보존·point4 완성도보존. §1.18 배제.
2. 수행: V6.0 설계(플로우차트·코드검토) → V6.1 재배열+시작값 절+listing 동기 → V6.2 프로즈 정합 → V6.3 의존·완성도·시각 검수 → V6.4 게이트.
3. Read Coverage: v6 전 범위(재배열 블록 + 신설 절) master + sub(seam·시각 41p·홀리스틱 통독). v5 대조.
4. 산출물: graphite_ica_ch1_Opus_v6.tex(+pdf), PHASE_V6_*, MASTER plan. BD: 코드 플로우차트 코멘트 + ANODE_FIT_code_completeness_review.md(point0).
5. 빌드: build_gate Opus_v6 **0/0/0 41p** · listing↔aux 14/14 · undef(ref) 0.
6. 라운드: V6.2 프로즈 4·V6.3 시각/홀리스틱 0 + 표행 1 → 수렴.
7. 확정 결함·수정 누적: listing 14 동기 + 프로즈 4 + 표행 1 = 흐름 정합. 물리·유도 무변경(블록 통째 이동).
8. 4-tier: 확정(구조·식번호·완성도·의존 보존·빌드 GREEN) / 추정(의존 2 플래그=v5 내재 forward) / 미검증(없음 — 시각·홀리스틱·의존·완성도 전수).
9. v5 대비 보존: 97식·figure·boxed·코드 누락 0(+시작값 표 1). **v3·v4·v5·공유 .py 무손상(git diff 0).**
10. Decisions: D1 §hys 이동(코드순+의존안전)·D2 배제 0(보수, point4)·D3 식번호 등장순 재부여+listing 동기·D4 시작값 절=§1.1 확장(새 물리 X) 전부 기본값.
11. Next: v6 완성. 사용자 검토 대기. (point2 배제는 v5가 이미 모델 한정이라 0 — 진짜 무관 토픽 발견 시 개별 보고 후.)
