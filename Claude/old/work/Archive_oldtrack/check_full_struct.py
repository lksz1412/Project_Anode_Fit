import re
f = r'd:/Projects/Project_Anode_Fit/Claude/docs/graphite_ica_full_rebuilt.tex'
txt = open(f, encoding='utf-8').read()

def count(pat):
    return len(re.findall(pat, txt))

# strip comment lines for command counting (lines starting with %)
noncomment = '\n'.join(l for l in txt.split('\n') if not l.lstrip().startswith('%'))

print('REAL \\documentclass:', count(r'\\documentclass'))
print('REAL \\begin{document}:', len(re.findall(r'\\begin\{document\}', noncomment)))
print('REAL \\end{document}:', len(re.findall(r'\\end\{document\}', noncomment)))
print('REAL \\maketitle (noncomment):', len(re.findall(r'\\maketitle', noncomment)))
print('REAL \\tableofcontents (noncomment):', len(re.findall(r'\\tableofcontents', noncomment)))
print('REAL \\title{ (noncomment):', len(re.findall(r'\\title\{', noncomment)))
print('REAL \\begin{thebibliography}:', count(r'\\begin\{thebibliography\}'))
print('REAL \\bibitem:', count(r'\\bibitem\{'))
print('REAL \\newtheorem\\*:', count(r'\\newtheorem\*'))
print()
print('chapter \\section{Chapter headings:')
for m in re.finditer(r'\\section\{(Chapter[^}]*(?:\{[^}]*\}[^}]*)*)\}', txt):
    print('   ', m.group(1)[:60])
# simpler: lines beginning with \section{Chapter
for i, l in enumerate(txt.split('\n'), 1):
    if l.startswith(r'\section{Chapter'):
        print(f'   line {i}: {l[:70]}')

# heading demotion sanity: there should be NO \section{ inside chapter bodies except the 6 chapter dividers + 2 (bib + note handled as \section/\section*)
sec_all = re.findall(r'(?<!sub)\\section\*?\{[^}]*', noncomment)
print('\ntotal \\section / \\section* (noncomment, top-level):', len(sec_all))
for s in sec_all:
    print('   ', s[:70])
