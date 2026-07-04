# V1.0.14 P5.1 Step 33 — 경연 승자 8안 ch1 편입 결과

대상 파일: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex`
방식: master 확정 승자를 `\begin{figure}[t]\centering` + 승자 파일 내용 그대로 + `\end{figure}` 로 기계적 치환. 새 판단·재작성 없음.

## 대상별 결과

| # | label | 승자 파일 | 캡션 정리 | label 정정 | 원본 보존 |
|---|-------|-----------|-----------|-----------|-----------|
| T1 | fig:spine | sonnet2/T1_spine.tex | 없음(계약 내 calc.py/경연 언급 없음) | 불필요(label 일치) | `_replaced_originals.tex` 1번째 블록 |
| T2 | fig:staging | sonnet1/T2_staging.tex | 없음 | 불필요 | 2번째 블록 |
| T3 | fig:hysloop | opus2/T3_hysloop.tex | 없음(헤더 주석의 `T3_calc.py`는 캡션 밖이라 원문 그대로 보존) | 불필요 | 3번째 블록 |
| T4 | fig:barrier | opus2/T4_barrier.tex | 없음(헤더 주석 `T4_calc.py`는 캡션 밖, 보존) | 불필요 | 4번째 블록 |
| T5 | fig:flux | opus2/T5_flux.tex | 없음(헤더 주석 `T5_calc.py`는 캡션 밖, 보존) | 불필요 | 5번째 블록 |
| T6 | fig:logistic | opus2/T6_logistic.tex | 없음(헤더 주석 `T6_calc.py`는 캡션 밖, 보존) | 불필요 | 6번째 블록 |
| T7 | fig:reversal | opus2/T7_reversal.tex | 없음(헤더 주석 `T7_calc.py`는 캡션 밖, 보존) | 불필요 | 7번째 블록 |
| T8 | fig:widthbudget | sonnet3/T8_widthbudget.tex | **3건** — 캡션 안 `T8\_calc.py` 언급 삭제(문장 자연 연결 유지): ①"(Gaussian $\sigma_\eta=1.25\sigma_\mathrm{int}$, T8\_calc.py)" → "(Gaussian $\sigma_\eta=1.25\sigma_\mathrm{int}$)" ②"peak 가 약 10% 높다(T8\_calc.py --- 분산은...)" → "peak 가 약 10% 높다(분산은...)" ③"1차 저역통과 재귀로 계산 --- T7 과 같은 수학)" → "1차 저역통과 재귀로 계산)" | 불필요(label 일치) | 8번째 블록 |

비고 — 각 승자 파일 최상단의 `% T{n} fig:xxx (opus2/sonnet3 — quantitative-density)` 류 헤더 주석과 `(see T{n}_calc.py)` 등은 모두 `%` LaTeX 주석으로 **캡션 밖**에 위치해 규칙 (a)(캡션 안 정리) 적용 대상이 아니므로 원문 그대로 보존했다(1차 편입 시 T3 블록에서 이를 임의 삭제했다가 범위 초과임을 인지하고 즉시 원복함 — 그 외 전 대상은 처음부터 verbatim 유지).

## 원본 보존

`Claude/results/process/fig_contest/_replaced_originals.tex` 에 T1..T8 순서대로 원본 `\begin{figure}...\end{figure}` 블록 8개를 라벨 주석과 함께 append 보존(원 위치 라인 번호 병기).

## 빌드 게이트 (xelatex 2-pass, PowerShell)

- 빌드 위치: scratchpad 임시 디렉터리(문서 원본 폴더에 aux/log 미생성).
- Pass 1: exit 0. Pass 2: exit 0.
- `^!` (fatal LaTeX error) 매치: **0**
- `Undefined control sequence` / `Multiply defined` / `Undefined reference` 매치: **0**
- 출력: `graphite_ica_ch1_v1.0.14.pdf`, 57 pages 정상 생성.
- Overfull \hbox 전체: 9건. **10pt 초과: 2건**
  - `(12.79pt too wide)` — L204-211 (fig:spine 캡션 문단)
  - `(13.24pt too wide)` — L1726-1737 (fig:widthbudget 캡션 문단)
  - 둘 다 캡션 \emph{텍스트} 문단의 자연스러운 줄바꿈 여유 초과(타이포그래피 통상 수준)이며 tikzpicture 그림 자체의 폭 초과가 아님. 승자 캡션 내용은 편입 규칙상 재작성 대상이 아니므로 수정하지 않음.

## 결론

8개 대상 전부 [성공] — 원복 발생 없음.
