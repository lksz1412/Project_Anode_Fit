# Phase 054 — v1.0.25.2 최신 대응 실행 원장

작성일: 2026-07-27

## 1. 계보 고정

| 확인 | 결과 |
|---|---|
| 작업 브랜치 | `codex/v1025_2-physics-conformance` |
| 기존 후보 tip | `2abf019c7fee9bebd84b49cc9530f6983b08a8fa` |
| 최신 인정 v1.0.25.2 tip | `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` |
| 핵심 기본값 정정 | `7b342dd88aad6bf9ff08cb3568da374837008ca7` |
| merge-base | `ab196b292e14492b647f87a6c0d1d8c9ed0630ab` |
| 구 후보와 최신 계보 차이 | 구 후보 전용 1커밋 / 최신 전용 3커밋 |
| 통합 방법 | 기존 공개 이력 보존을 위한 non-force merge |
| merge commit | `4316d8a5423d0ba229931a3c43c1f833fdc2fe1e` |
| v1.0.26 사용 | no |
| `main` 수정 | no |

실행한 핵심 계보 명령:

```text
git fetch origin --prune
git merge-base 2abf019 3b5fd05
git rev-list --left-right --count 2abf019...3b5fd05
git merge --no-ff origin/claude/version-1026-regsol-review-kl88j7
```

## 2. 최신 입력 동결

명령:

```text
python3 Codex/work/v1025_2_physics_branch/phase054_latest_source_manifest.py
```

결과:

- PASS
- 출력:
  `Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST.json`
- 최신 legacy code SHA-256:
  `c28101568b1b57f7dcb1e20c19fcdaa997fb5022d6230f839657216e1872ae44`
- 최신 legacy code 행수: 2,024
- 정칙용액 절 SHA-256:
  `0444633ca12ce1212a2a98f4378db1a6d6d33e92f6856b767447e54b52c4d13a`

## 3. 최신 배포 배선 probe

명령:

```text
python3 Codex/work/v1025_2_physics_branch/phase054_latest_source_probes.py
python3 -m json.tool Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json
```

결과:

- script exit: PASS
- JSON parse: PASS
- fresh default: 흑연 4 + `sic` Si 2
- fresh default 288.15→308.15 K 최대 차:
  `0.5252164419568519`
- 7+7 opt-in 최대 차: `6.394884621840902e-14`
- 현 기본 invalid `si_case`: `ValueError`
- 7+7 opt-in invalid `si_case`: 조용히 수용, Si 7성분
- 현 기본의 블렌드 wiring 진단:
  `R²=0.07507231361482658`
- 7+7 opt-in wiring 진단:
  `R²=-1.6132166646788586`
- 저장 direct14 재구성:
  `R²=0.99964941790404`, `BIC=-4760.653827485789`
- 기대된 결함 관측:
  eager logistic overflow/invalid warning 3건

경고 3건은 probe 실패가 아니라 감사 대상 결함의 재현이다. JSON은
stderr 경고와 분리해 정상 생성·파싱했다.

## 4. 정칙용액 교차검증

명령:

```text
python3 Codex/work/v1025_2_physics_branch/phase054_regsol_crosscheck.py
python3 -m json.tool Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json
```

결과:

- script exit: PASS
- JSON parse: PASS
- sweep:
  `alpha={1,4,8}`,
  `Omega/(RT)={0,1,1.999,2,2.001,3,4,8}`
- 해석 면적: Q
- ±1 V 수치 면적 최대 오차:
  `7.771561172376096e-16`
- `Omega/(RT)<=2` 최대 gap weight: 0
- 임계점 우측 값 연속: PASS
- “1차 Omega 도함수 발산”: FAIL

## 5. 최신 legacy 검증

실행 환경은 bytecode/cache 출력을 `/tmp`로 분리하거나 쓰지 않게 했다.

| 명령 | 결과 |
|---|---|
| `python3 -m py_compile .../Anode_Fit_v1.0.24.py` | PASS |
| `python3 .../test_gates_v1025.py` | PASS 9/9 |
| `python3 .../test_gates_v1024.py` | G1/G2/G3/n(T), R6 전 항목 PASS |
| `python3 .../test_gates_v1024_reflect.py` | PASS 4/4 |
| `python3 .../test_gates_v1024_selfconsistent.py` | PASS 5/5 |

미포착 경고/stderr는 없었다. 예상된 alpha/LV 축퇴 경고와 SiOx 공백
경고는 각 gate의 계약대로 처리됐다.

범위 한계:

- v1024 gate는 로드 직후 `use_skew7_default(False)`를 강제한다.
- v1025 gate는 global default 대신 명시 transition/dataset을 쓴다.
- reflect/selfconsistent도 명시 transition을 쓴다.
- reflect/selfconsistent는 `Anode_Fit_v1.0.24.py`를 현재 작업 디렉터리
  기준으로 연다. 저장소 루트에서 실행하면 `FileNotFoundError`이고,
  위 PASS는 `Claude/docs/v1.0.25.2`를 작업 디렉터리로 실행한 결과다.

따라서 이 전체 PASS는 shipped fresh-import default의 회귀검사가 아니다.
그 계약은 Phase 054 source probe가 별도로 측정했다.

## 6. 독립 후보 검증

| 명령 | 결과 |
|---|---|
| `python3 -W error Codex/work/v1025_2_physics_branch/tests/run_all.py` | PASS 51/51 |
| `python3 Codex/work/v1025_2_physics_branch/tests/verify_manuscript.py` | PASS |

원고 구조 결과:

- sources: 16
- include edges: 15
- labels: 183
- references: 32
- missing/duplicate/orphan/cycle: 없음

51개 시험 분해:

- physical equilibrium: 11
- empirical direct14/public API: 11
- numerics/observation: 8
- causal dynamics: 7
- kinetics/heat: 8
- manuscript static: 6

범위 한계:

- 이 시험은 `Codex/.../conformance_model`만 import한다.
- 최신 legacy의 4+2/7+7 global default를 실행하지 않는다.
- 원 optimizer 재현, material/phase identification,
  regular-solution closure의 진실성을 자동 증명하지 않는다.
- 원고 gate는 구조·lexical boundary 검사이며 물리 의미의 진실성
  판정기는 아니다.

## 7. PDF 검증

- 기존 전달 PDF:
  `output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf`
- 상태: Git 추적 산출물, A4 28쪽, 암호화 없음, 286,990 bytes
- SHA-256:
  `9832400c55df88874699a0eaaf0f392da6dcdcd82e9389990b25b62e07978f83`
- 기존 PDF의 NanumGothic/Bold 등 열거 글꼴: embedded
- fresh `latexmk -xelatex` 재빌드: BLOCKED
- 차단 원인:
  빌드가 명시적으로 허용한 `Noto Serif CJK KR`/`NanumGothic`이
  현재 실행 환경에 없음
- 판정:
  기존 PDF inspect는 PASS, fresh reproducible build는 환경 차단이며
  원고 소스 실패로 판정하지 않음

## 8. 커밋·원격 기록

| 체크포인트 | 커밋 | 원격 상태 |
|---|---|---|
| Phase 054 계획 | `eed5d48` | pushed |
| 최신 v1.0.25.2 병합 | `4316d8a` | pushed |
| 리뷰·행렬·probe·manifest | `30a874e906f2be72a36efaac7cb8fd8138e7b401` | pushed |

`git ls-remote` 확인 시:

```text
30a874e906f2be72a36efaac7cb8fd8138e7b401  refs/heads/codex/v1025_2-physics-conformance
4069cb36a8a52b1b88c29d68aa54dcbe915b1618  refs/heads/main
```

즉 리뷰 체크포인트는 원격 브랜치에 있고 `main`은 그대로다.
이 실행 원장과 handover correction은 위 체크포인트 뒤의 별도 기록
커밋으로 추가한다.

## 9. 작업트리 보존

작업 시작 전부터 있던 다음 사용자 변경은 읽기·수정·stage하지 않았다.

```text
Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html
```

Phase 054는 기존 Phase 044/046–053 결과를 덮어쓰지 않고 새 addendum,
matrix, manifest, probe, correction만 추가했다.
