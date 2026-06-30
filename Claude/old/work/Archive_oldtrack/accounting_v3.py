# -*- coding: utf-8 -*-
import re
BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'

def read(ch):
    return open(f'{BASE}/graphite_ica_ch{ch}_rebuilt.tex', encoding='utf-8').read()

def extract_body(ch):
    txt = read(ch)
    s = re.search(r'\\maketitle', txt)
    b = re.search(r'\\begin\{thebibliography\}', txt)
    body = txt[s.end():b.start()]
    body = re.sub(r'\\tableofcontents\s*\n', '', body)
    body = re.sub(r'^\\newpage\s*$\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\\sloppy\s*$\n', '', body, flags=re.MULTILINE)
    return body.strip('\n')

tot = 0
for ch in [1, 2, 3, 4, 5]:
    body = extract_body(ch)
    n = body.count('\n') + 1
    tot += n
    print(f'Ch{ch} extracted body lines: {n}')
print('SUM of chapter body lines:', tot)

full = open(f'{BASE}/graphite_ica_full_rebuilt.tex', encoding='utf-8').read()
print('FULL total lines:', full.count('\n') + 1)
refs = open(f'{BASE}/graphite_ica_refs_rebuilt.tex', encoding='utf-8').read()
print('REFS total lines:', refs.count('\n') + 1)
