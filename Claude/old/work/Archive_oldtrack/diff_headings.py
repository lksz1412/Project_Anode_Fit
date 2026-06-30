# -*- coding: utf-8 -*-
import re

BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'

def standalone_body(ch):
    txt = open(f'{BASE}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()
    s = re.search(r'\\maketitle', txt).end()
    e = re.search(r'\\begin\{thebibliography\}', txt).start()
    return txt[s:e]

full = open(f'{BASE}/graphite_ica_full_rebuilt.tex', encoding='utf-8').read()
marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'\\label\{chap:ch(\d)\}', full)]
bibm = re.search(r'\\section\{통합 참고문헌', full)
bounds = {}
for i, (pos, ch) in enumerate(marks):
    end = marks[i+1][0] if i+1 < len(marks) else bibm.start()
    # include the chapter divider line that sits just before the label
    line_start = full.rfind('\n', 0, pos) + 1
    bounds[ch] = full[line_start:end]

HEAD = re.compile(r'\\((?:sub)*section)(\*?)\{')

def heads(text):
    res = []
    for m in HEAD.finditer(text):
        # capture the heading title (rough, up to first closing brace at depth 0)
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        title = text[start:i-1]
        res.append((m.group(1) + m.group(2), title[:40]))
    return res

ch = 1
hs = heads(standalone_body(ch))
hf = heads(bounds[ch])
print(f'Chapter {ch}: standalone headings={len(hs)}  full headings={len(hf)}')
print('--- standalone ---')
for lvl, t in hs:
    print(f'   {lvl:<14} {t}')
print('--- full region ---')
for lvl, t in hf:
    print(f'   {lvl:<14} {t}')
