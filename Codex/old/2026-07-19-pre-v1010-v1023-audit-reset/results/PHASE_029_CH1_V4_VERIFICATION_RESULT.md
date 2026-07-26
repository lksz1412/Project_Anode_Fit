# PHASE 029 - Chapter 1 V4 Verification Result

## 1. Target

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex`

- Lines: 945
- SHA256: `C1607A7E101B1D3BA4BD4CDF9D88D0C8AEDAFADCEA6BBFF1E525EC540C876517`

## 2. Static TeX integrity

| Check | Result |
|---|---:|
| labels | 48 |
| duplicate labels | 0 |
| eqref/ref | 148 |
| missing refs | 0 |
| cite commands | 32 |
| bibitems | 23 |
| missing cites | 0 |
| unused bibitems | 0 |
| begin environments | 54 |
| end environments | 54 |

## 3. Risk-pattern scan

| Pattern | Count | 판단 |
|---|---:|---|
| `RB 재구성본` | 0 | PASS |
| `RB plan` | 0 | PASS |
| `Author:` | 0 | PASS |
| `Date:` | 0 | PASS |
| `동일물` | 0 | PASS |
| `AL{9}` | 0 | PASS |
| `Heaviside` | 0 | PASS |
| `H(L-L...)` | 0 | PASS |
| `A_L=\delta` | 0 | PASS |
| `CHARTER` | 0 | PASS |
| `$$` | 0 | PASS |
| placeholder bibliography strings | 0 | PASS |
| `step-function` | 1 | PASS: GS-4 금지 설명 문맥에서만 등장 |

## 4. XeLaTeX verification

Execution environment:

- Working directory: `C:\Users\lksz1\OneDrive\문서\New project`
- Output directory: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1_v4`
- Engine: `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`

Results:

| Pass | Exit code |
|---|---:|
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |

PDF:

- `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1_v4\graphite_ica_ch1_codex_candidate_v4.pdf`
- Size: 406721 bytes
- Pages from prior successful compile: 20

Final log scan:

| Log item | Count |
|---|---:|
| LaTeX Error | 0 |
| Undefined control sequence | 0 |
| Undefined references | 0 |
| Undefined citations | 0 |
| Rerun requested | 0 |
| Label changed | 0 |
| Missing character | 0 |
| Hyperref PDF-string warnings | 13 |
| Overfull hbox | 7 |
| Underfull hbox | 25 |
| Font warnings | 5 |

## 5. 판단

Compile gate는 PASS다. 남은 hyperref/overfull/underfull/font warning은 TeX 조판 품질 이슈이며 논리식, citation, label, compile success를 깨지 않는다. MiKTeX update warning은 로컬 환경 유지보수 알림이며 문서 실패 원인이 아니다.
