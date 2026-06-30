# -*- coding: utf-8 -*-
"""Integrity check for refs + full files: environment begin/end balance,
   equation balance, boxed count, bibitem count, label uniqueness."""
import re

BASE = r'd:/Projects/Project_Anode_Fit/Claude/docs'

def check(fn):
    txt = open(f'{BASE}/{fn}', encoding='utf-8').read()
    print(f'\n=== {fn} ===')
    # generic environment balance
    begins = re.findall(r'\\begin\{([^}]+)\}', txt)
    ends = re.findall(r'\\end\{([^}]+)\}', txt)
    from collections import Counter
    cb, ce = Counter(begins), Counter(ends)
    envs = set(cb) | set(ce)
    imbal = {e: (cb[e], ce[e]) for e in envs if cb[e] != ce[e]}
    print(f'  total \\begin={len(begins)}  total \\end={len(ends)}  (diff={len(begins)-len(ends)})')
    print(f'  imbalanced environments: {imbal if imbal else "NONE"}')
    # equation specifically
    print(f'  equation begin/end: {cb["equation"]}/{ce["equation"]}   '
          f'align: {cb["align"]}/{ce["align"]}   multline: {cb["multline"]}/{ce["multline"]}   '
          f'longtable: {cb["longtable"]}/{ce["longtable"]}   thebibliography: {cb["thebibliography"]}/{ce["thebibliography"]}')
    # boxed
    print(f'  \\boxed count: {len(re.findall(r"\\boxed", txt))}')
    # bibitems
    bibs = re.findall(r'\\bibitem\{([^}]+)\}', txt)
    print(f'  \\bibitem count: {len(bibs)}  unique: {len(set(bibs))}  dup: {len(bibs)-len(set(bibs))}')
    # labels
    labs = re.findall(r'\\label\{([^}]+)\}', txt)
    dup = [k for k, c in Counter(labs).items() if c > 1]
    print(f'  \\label count: {len(labs)}  unique: {len(set(labs))}  DUPLICATES: {dup if dup else "NONE"}')

check('graphite_ica_refs_rebuilt.tex')
check('graphite_ica_full_rebuilt.tex')
