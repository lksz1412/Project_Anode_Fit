# -*- coding: utf-8 -*-
"""Standalone <-> full no-loss comparison.
   For each chapter: count boxed equations (\\boxed), \\begin{equation}, \\label{eq:,
   and section-level headings, in (a) the standalone chapter body and (b) the
   corresponding chapter region inside the merged full file. They must match.
"""
import re, sys

BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'

def chapter_body_standalone(ch):
    txt = open(f'{BASE}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()
    s = re.search(r'\\maketitle', txt).end()
    e = re.search(r'\\begin\{thebibliography\}', txt).start()
    return txt[s:e]

# split the full file into chapter regions using the \section{Chapter N ...}\label{chap:chN}
full = open(f'{BASE}/graphite_ica_full_rebuilt.tex', encoding='utf-8').read()
marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'\\label\{chap:ch(\d)\}', full)]
# bibliography section marks the end of chapter 6 region
bibm = re.search(r'\\section\{통합 참고문헌', full)
bounds = {}
for i, (pos, ch) in enumerate(marks):
    end = marks[i+1][0] if i+1 < len(marks) else bibm.start()
    bounds[ch] = full[pos:end]

def counts(text):
    return {
        'boxed': len(re.findall(r'\\boxed', text)),
        'equation_begin': len(re.findall(r'\\begin\{equation\}', text)),
        'equation_end': len(re.findall(r'\\end\{equation\}', text)),
        'align_begin': len(re.findall(r'\\begin\{align\}', text)),
        'multline_begin': len(re.findall(r'\\begin\{multline\}', text)),
        'eqlabel': len(re.findall(r'\\label\{eq:', text)),
        'seclabel': len(re.findall(r'\\label\{sec:', text)),
        # heading count: standalone uses \section/\subsection; full uses \subsection/\subsubsection (demoted)
        'headings': len(re.findall(r'\\(?:sub)*section\*?\{', text)),
    }

print('CHAPTER-BY-CHAPTER NO-LOSS COMPARISON (standalone body vs full-doc region)')
print('='*92)
hdr = f"{'ch':>3} {'metric':<16} {'standalone':>11} {'full':>6} {'match':>6}"
allok = True
for ch in range(1, 7):
    cs = counts(chapter_body_standalone(ch))
    cf = counts(bounds[ch])
    # In full, multline replaced one equation in ch6 (gitt). Account for that:
    # equation_begin(full) + multline_begin(full) should equal standalone equation_begin.
    print(f'--- Chapter {ch} ---')
    # the full region includes exactly ONE extra heading: the prepended chapter divider
    # \section{Chapter N}. Subtract it before comparing internal headings.
    divider = len(re.findall(r'\\section\{Chapter ' + str(ch), bounds[ch]))
    for k in ['boxed', 'eqlabel', 'seclabel']:
        ok = (cs[k] == cf[k])
        mark = 'OK' if ok else 'DIFF'
        if not ok:
            allok = False
        print(f'    {k:<16} standalone={cs[k]:>3}  full={cf[k]:>3}  [{mark}]')
    # headings: full should equal standalone + 1 chapter divider
    okh = (cf['headings'] - divider == cs['headings'])
    if not okh:
        allok = False
    print(f'    {"headings(-div)":<16} standalone={cs["headings"]:>3}  full={cf["headings"]:>3}  '
          f'(divider={divider})  [{"OK" if okh else "DIFF"}]')
    # equation count with multline accounting
    se = cs['equation_begin']
    fe = cf['equation_begin'] + cf['multline_begin']
    ok = (se == fe)
    if not ok:
        allok = False
    eqmark = "OK" if ok else "DIFF"
    print(f'    equation(+mult)  standalone={se:>3}  full={fe:>3}  [{eqmark}]')
print('='*92)
print('ALL MATCH:', allok)
