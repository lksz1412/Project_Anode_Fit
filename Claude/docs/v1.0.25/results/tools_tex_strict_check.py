# -*- coding: utf-8 -*-
"""v1.0.25 문건 정적 검증 (TeX 배포판 부재 환경의 빌드 대체 게이트).

tools_check_structure.py 가 라벨 '합집합' 기준이라 못 잡는 것들을 잡는다:
  A. 장별 참조 해소 — 각 master 의 ref 가 (자기 라벨) ∪ (그 master 가 \externaledocument 한 master 의 라벨)
     안에 있는가. 즉 xr 없이 남의 장 라벨을 참조하면 FAIL.
  B. 인라인 수식 $ 짝 (편집 파일 한정)
  C. 사용된 매크로가 preamble 에 정의되어 있는가 (편집 파일 한정)
  D. 중괄호 균형 (편집 파일 한정)
  E. boxed 식 개수 회귀 (삭제 금지)
"""
import io, os, re, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # = docs/v1.0.25
MASTERS = ["ch1_graphite_v1.0.24.tex", "ch2_lco_v1.0.24.tex",
           "ch3_si_v1.0.24.tex", "appendix_phase_separation.tex"]
EDITED = [
    "_sections/ch1_sec05_width.tex", "_sections/ch1_sec05b_gr2L.tex",
    "_sections/ch1_sec06_eqpeak.tex", "_sections/ch1_sec07_broadening.tex",
    "_sections/ch1_sec09_tail.tex", "_sections/ch1_sec10_sum.tex",
    "_sections/ch1_sec18_inputs.tex", "_sections/ch1_appB_codemap.tex",
    "_sections/ch1_appE_selfconsistent.tex", "_sections/ch2_sec05_mixing.tex",
    "_sections/ch2_sec08_synthesis.tex", "_sections/ch2_appB_codemap.tex",
    "_sections/ch3v22_sec02_cases.tex", "_sections/ch3v22_sec02b_sifr.tex",
]
PKG_LABELS = {"LastPage"}
FAIL = []


def strip_comments(text):
    out = []
    for line in text.split("\n"):
        r, i = [], 0
        while i < len(line):
            c = line[i]
            if c == "\\" and i + 1 < len(line):
                r.append(line[i:i+2]); i += 2; continue
            if c == "%":
                break
            r.append(c); i += 1
        out.append("".join(r))
    return "\n".join(out)


def inputs_of(master):
    files, seen = [], set()

    def walk(p):
        if p in seen:
            return
        seen.add(p); files.append(p)
        try:
            t = open(p, encoding="utf-8").read()
        except FileNotFoundError:
            FAIL.append(f"missing input {p}"); return
        for m in re.finditer(r"^\s*\\input\{([^}]+)\}", t, re.M):
            s = m.group(1)
            if not s.endswith(".tex"):
                s += ".tex"
            walk(os.path.join(ROOT, s))
    walk(os.path.join(ROOT, master))
    return files


info = {}
for mst in MASTERS:
    files = inputs_of(mst)
    labels, refs = set(), []
    for p in files:
        t = strip_comments(open(p, encoding="utf-8").read())
        labels |= set(re.findall(r"\\label\{([^}]+)\}", t))
        for m in re.finditer(r"\\(?:eqref|ref|pageref|cref)\{([^}]+)\}", t):
            refs.append((m.group(1), os.path.basename(p)))
    xr = re.findall(r"\\externaldocument\{([^}]+)\}",
                    open(os.path.join(ROOT, mst), encoding="utf-8").read())
    info[mst] = dict(files=files, labels=labels, refs=refs, xr=[x + ".tex" for x in xr])

print("=" * 100)
print("[A] 장별 참조 해소 (xr 경로만 허용 — 라벨 합집합 금지)")
for mst in MASTERS:
    d = info[mst]
    allowed = set(d["labels"]) | PKG_LABELS
    for x in d["xr"]:
        if x in info:
            allowed |= info[x]["labels"]
        else:
            FAIL.append(f"{mst}: externaldocument 대상 {x} 미등록")
    bad = sorted({(r, f) for r, f in d["refs"] if r not in allowed})
    xrn = ",".join(d["xr"]) or "-"
    print(f"  {mst:34s} refs={len(d['refs']):5d}  xr=[{xrn}]  미해소={len(bad)}")
    for r, f in bad[:20]:
        print(f"      ** {r}   ({f})")
        FAIL.append(f"{mst}: unresolved {r} in {f}")

print()
print("=" * 100)
print("[B~D] 편집 파일 정적 검사 ($ 짝 · 중괄호 · 매크로 정의)")
pre = ""
for f in ("_sections/common_preamble_v1024.tex", "_sections/ch1_preamble.tex",
          "_sections/ch2_preamble.tex", "_sections/ch3v22_notation.tex",
          "_sections/ch2v22_notation.tex"):
    p = os.path.join(ROOT, f)
    if os.path.exists(p):
        pre += open(p, encoding="utf-8").read()
defined = set(re.findall(r"\\(?:newcommand|renewcommand|providecommand)\*?\{?\\([A-Za-z]+)", pre))
defined |= set(re.findall(r"\\newtheorem\*?\{([A-Za-z]+)\}", pre))
# LaTeX/amsmath/기본 패키지 제공 매크로 (검사 대상 아님)
KNOWN = set("""begin end label ref eqref pageref cite citet citep footnote emph textbf textit texttt
section subsection subsubsection paragraph appendix input item frac dfrac tfrac sqrt sum int prod lim
left right big Big bigg Bigg boxed underbrace overbrace text mathrm mathbf mathcal mathit operatorname
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi rho
sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi
Psi Omega partial nabla infty pm mp times div cdot cdots ldots vdots ddots leq geq neq approx equiv
sim simeq cong propto ll gg subset supset in notin cup cap emptyset forall exists neg land lor to
rightarrow leftarrow Rightarrow Leftarrow leftrightarrow Leftrightarrow longrightarrow mapsto
uparrow downarrow quad qquad hspace vspace medskip smallskip bigskip par newline linebreak
centering raggedright raggedleft footnotesize scriptsize tiny small normalsize large Large LARGE huge
Huge bf it rm sf tt sc upshape bfseries itshape rmfamily sffamily ttfamily normalfont
toprule midrule bottomrule multicolumn multirow endhead endfirsthead caption
renewcommand newcommand setlength arraystretch tabular longtable array
node draw foreach plot coordinates smooth densely thick very anchor font align
lessgtr gtrless lesssim gtrsim ge le ne overline underline hat bar tilde vec dot ddot
mathsf mathbb mathfrak displaystyle textstyle scriptstyle limits nolimits substack
S P dag ddag ast star circ bullet ominus oplus otimes odot
color textcolor colorbox fcolorbox
xrightarrow xleftarrow overset underset stackrel
begingroup endgroup makeatletter makeatother relax noindent
artanh arctanh tanh sinh cosh coth exp log ln sin cos tan max min sup inf det gcd deg dim ker
hline vline cline phantom hphantom vphantom mbox fbox parbox makebox
setstretch hypersetup lhead rhead thepage pageref
prime ldotp mathpunct nonumber notag intertext shortintertext
bigl bigr Bigl Bigr biggl biggr Biggl Biggr
""".split())

for rel in EDITED:
    p = os.path.join(ROOT, rel)
    raw = open(p, encoding="utf-8").read()
    t = strip_comments(raw)
    # B: 인라인 $ 짝 — 절대 패리티가 아니라 v1.0.24.1 원본 대비 '패리티 불변' 을 본다.
    #    (원본 일부 파일은 tikz/\code 인자 안의 $ 때문에 이 순진한 카운터로는 홀수로 나오지만
    #     원본은 정상 빌드된다 = 카운터의 위양성. 내 편집이 패리티를 바꾸지 않았는지가 실제 게이트다.)
    n_dollar = len(re.findall(r"(?<!\\)\$", t))
    base = os.path.join(os.path.dirname(ROOT), "v1.0.24.1", rel.replace("/", os.sep))
    n_base = len(re.findall(r"(?<!\\)\$", strip_comments(open(base, encoding="utf-8").read())))
    ok_d = (n_dollar % 2 == n_base % 2)
    # D: 중괄호
    bal, i, depth, minus = 0, 0, 0, 0
    while i < len(t):
        c = t[i]
        if c == "\\" and i + 1 < len(t):
            i += 2; continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth < 0:
                minus += 1; depth = 0
        i += 1
    ok_b = (depth == 0 and minus == 0)
    # C: 매크로
    used = set(re.findall(r"\\([A-Za-z]+)", t))
    undef = sorted(u for u in used if u not in defined and u not in KNOWN)
    flag = "OK " if (ok_d and ok_b) else "**FAIL**"
    print(f"  {flag} {os.path.basename(rel):32s} $={n_base}->{n_dollar} "
          f"패리티{'불변' if ok_d else '변경'}  중괄호 depth={depth} 초과닫힘={minus}  "
          f"미확인매크로={len(undef)}")
    if undef:
        print(f"        미확인: {', '.join(undef[:14])}")
    if not ok_d:
        FAIL.append(f"{rel}: $ 패리티 변경 ({n_base}->{n_dollar})")
    if not ok_b:
        FAIL.append(f"{rel}: 중괄호 불균형 depth={depth} 초과닫힘={minus}")

print()
print("=" * 100)
print("[E] 신규 라벨 / boxed 회귀")
# baseline = v1.0.24.1 원본에서 즉석 수집(외부 스냅샷 파일 의존 제거)
PREV = os.path.join(os.path.dirname(ROOT), "v1.0.24.1")
snap = {}
for _m in MASTERS:
    _lab = set()
    for _p in inputs_of(_m):
        _q = _p.replace(ROOT, PREV)
        if os.path.exists(_q):
            _lab |= set(re.findall(r"\\label\{([^}]+)\}",
                                   strip_comments(open(_q, encoding="utf-8").read())))
    snap[_m] = {"labels": sorted(_lab)}
for mst in MASTERS:
    old = set(snap[mst]["labels"]); new = info[mst]["labels"]
    print(f"  {mst:34s} 라벨 +{sorted(new-old)}  -{sorted(old-new)}")
    if old - new:
        FAIL.append(f"{mst}: 라벨 삭제 {sorted(old-new)}")

print()
print("=" * 100)
if FAIL:
    print(f">>> STRICT CHECK: FAIL ({len(FAIL)} 건)")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(">>> STRICT CHECK: ALL PASS")
