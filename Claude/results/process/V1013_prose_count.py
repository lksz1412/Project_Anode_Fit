#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1013_prose_count.py — Anode_Fit v1.0.13 P1.1 S3 prose-budget measurement script.

Purpose
-------
Measure, per \\section / \\subsection heading, in graphite_ica_ch1_v1.0.13.tex and
graphite_ica_ch2_v1.0.13.tex:
  (1) prose sentence count  — main-text Korean/English prose only, excluding display
      math environments, comments, and the LaTeX preamble.
  (2) equation-type environment count — \\begin{equation*?}, align*?, alignat*?,
      multline*?, gather*?, eqnarray*? and bare \\[ ... \\] display-math blocks.
  (3) line count — raw source lines spanned by the heading's block (heading line
      through the line before the next heading, capped at \\begin{thebibliography}
      or \\end{document}).

This script performs READ-ONLY measurement. It never writes to the .tex source files.

Counting rules (operational definitions — reproduce exactly what this script does)
------------------------------------------------------------------------------------
A) Section slicing
   - Headings recognized: \\section*{...}, \\section{...}, \\subsection{...}
     (with or without a following \\label{...}).
   - A heading's "own" text block = from its own line through the line immediately
     before the next heading (section OR subsection, whichever comes first), or
     through the line before \\begin{thebibliography} / \\end{document} for the
     last heading in the file. This means a \\section's own block does NOT include
     its child \\subsection blocks' text — those are separate rows. "Whole section
     incl. subsections" totals are reported separately as roll-ups.
   - LCO classification (Ch1 only): a heading is tagged "LCO" iff its \\label
     string contains the substring "lco" (case-insensitive). Unlabeled headings
     (Ch1 서론) are tagged "공통/서론" and excluded from both the 흑연 and LCO
     subtotal (reported separately, not summed into either).
   - Ch2 has no lco-labeled headings (checked directly against the section list),
     so all Ch2 headings roll up into a single Ch2 subtotal.

B) Equation-type environment count (per heading block, on RAW text, before any
   stripping)
   - Count occurrences of \\begin{equation}, \\begin{equation*}, \\begin{align},
     \\begin{align*}, \\begin{alignat}, \\begin{alignat*}, \\begin{multline},
     \\begin{multline*}, \\begin{gather}, \\begin{gather*}, \\begin{eqnarray},
     \\begin{eqnarray*}, \\begin{displaymath}.
   - PLUS count of bare \\[ ... \\] display-math blocks (opening "\\[" that is not
     part of \\left[ / \\right[ and not \\label[...] etc — in this document \\[
     only ever opens display math, verified by manual read).
   - \\begin{cases}...\\end{cases} is NOT counted separately — in both chapters it
     only ever appears nested inside an already-counted \\begin{equation} block,
     so counting it again would double count. (Verified: every \\begin{cases} in
     both files is preceded by an unclosed \\begin{equation} at that point.)

C) Prose sentence count (per heading block)
   Preprocessing pipeline applied to the raw heading-block text, in order:
     1. Strip \\begin{equation*?}...\\end{equation*?} and the other equation-type
        environments listed in (B), and bare \\[ ... \\] blocks — replaced by a
        single space (so text on either side of a formula stays joined into one
        flowing sentence, matching how these read in the typeset PDF).
     2. Strip \\begin{figure}...\\end{figure}, \\begin{table}...\\end{table},
        \\begin{longtable}...\\end{longtable} in full (this removes nested
        tikzpicture/tabular/caption content along with them) — captions and table
        cells are NOT counted as prose (they are supplementary/structural, not the
        flowing argument prose this budget targets).
     3. Strip \\begin{thebibliography}...\\end{thebibliography} (reference list is
        not prose).
     4. Protect version/decimal numeric chains matching \\d+(\\.\\d+)+ (e.g.
        "1.0.13", "0.0853") by swapping their internal '.' for a private-use
        placeholder character, so they are never mistaken for sentence-ending
        periods.
     5. Strip inline math $...$ (replaced by a single space) — inline math commonly
        contains '.' as a decimal point or ':' etc. that would corrupt sentence
        splitting, and inline math is not itself prose.
     6. Unwrap (keep inner text of, drop the command) \\textbf{...}, \\emph{...},
        \\textit{...}, \\footnote{...}, \\code{...} — one brace-nesting level
        (adequate for this document; verified no nested-brace counter-examples in
        the prose portions of either file).
     7. Drop \\cite{...}, \\ref{...}, \\eqref{...}, \\label{...} entirely (with
        their braces) — bibliographic/cross-reference tokens, not prose content.
     8. Drop remaining bare LaTeX control sequences (\\S, \\S\\ref, \\ldots, environment
        wrapper tokens \\begin{itemize}[...], \\end{itemize}, \\item, etc.) via a
        generic "\\command" / leftover-brace sweep.
     9. Collapse whitespace to single spaces.
   Sentence count = number of chunks produced by scanning left-to-right for the
   next one of . ! ? (after step 4's decimal-protection), i.e.
   len(re.findall(r'[^.!?]*[.!?]', text)) PLUS 1 more if a non-trivial
   (>=5 non-space chars) fragment remains after the last terminal mark.
   This is a simple, fully reproducible rule — not a linguistic sentence
   tokenizer. It is applied IDENTICALLY to every section in both chapters, so
   relative comparisons (which section is prose-heavy, LCO vs 흑연 ratio) are
   valid even though the absolute count is an approximation.

Usage
-----
    python V1013_prose_count.py

Outputs a Markdown table (per heading) and subtotal block to stdout. The
V1013_PROSE_BUDGET.md report was built by capturing this output and adding
narrative framing; re-running this script reproduces the numeric core exactly.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CH1 = Path(r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\graphite_ica_ch1_v1.0.13.tex")
CH2 = Path(r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.13\graphite_ica_ch2_v1.0.13.tex")

EQUATION_ENV_NAMES = [
    "equation\\*?", "align\\*?", "alignat\\*?", "multline\\*?",
    "gather\\*?", "eqnarray\\*?", "displaymath",
]
EQ_BEGIN_RE = re.compile(
    r"\\begin\{(" + "|".join(EQUATION_ENV_NAMES) + r")\}"
)
EQ_BLOCK_RE = re.compile(
    r"\\begin\{(" + "|".join(EQUATION_ENV_NAMES) + r")\}.*?\\end\{\1\}",
    re.DOTALL,
)
# (?<!\\) guards against LaTeX's "\\[<len>]" row-spacing token (e.g. "\\[2pt]"
# inside a cases/align row, or "\\[0.35em]" after a \\ line break in \title) —
# that is TWO backslashes followed by '[', which a naive r"\\\[" pattern matches
# starting at the *second* backslash, misreading a spacing directive as the
# opening of a \[ ... \] display-math block. Verified by grep: every such
# occurrence in both chapters is either in the preamble (excluded already) or
# nested inside a \begin{equation}...\end{equation} that strip_non_prose removes
# first anyway — but the RAW equation-count pass (count_equation_blocks) runs
# before any stripping, so without this guard it over-counts by exactly the
# number of such row-spacing tokens (confirmed: 4 in Ch1, 0 in Ch2 body).
BRACKET_MATH_RE = re.compile(r"(?<!\\)\\\[.*?(?<!\\)\\\]", re.DOTALL)
BRACKET_MATH_OPEN_RE = re.compile(r"(?<!\\)\\\[")

FIGURE_BLOCK_RE = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.DOTALL)
TABLE_BLOCK_RE = re.compile(r"\\begin\{table\}.*?\\end\{table\}", re.DOTALL)
LONGTABLE_BLOCK_RE = re.compile(r"\\begin\{longtable\}.*?\\end\{longtable\}", re.DOTALL)
BIBLIO_BLOCK_RE = re.compile(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.DOTALL)

DECIMAL_CHAIN_RE = re.compile(r"\d+(?:\.\d+)+")
INLINE_MATH_RE = re.compile(r"\$[^$]*\$", re.DOTALL)

UNWRAP_CMDS = ["textbf", "emph", "textit", "footnote", "code"]
UNWRAP_RE = re.compile(
    r"\\(?:" + "|".join(UNWRAP_CMDS) + r")\{([^{}]*)\}"
)
DROP_REF_RE = re.compile(r"\\(?:cite|ref|eqref|label)\{[^{}]*\}")
DROP_CMD_RE = re.compile(r"\\[A-Za-z]+\*?")
DROP_BRACE_ARG_RE = re.compile(r"\[[^\[\]]{0,40}\]")  # optional-arg remnants like [label=...]
STRAY_BRACE_RE = re.compile(r"[{}]")

HEADING_START_RE = re.compile(r"^(?P<cmd>\\(?:sub)?section)\*?\{", re.MULTILINE)


def strip_comments(text: str) -> str:
    """Remove unescaped '%'-to-end-of-line LaTeX comments, line by line."""
    out_lines = []
    for line in text.split("\n"):
        # find first unescaped %
        i = 0
        cut = None
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                cut = i
                break
            i += 1
        out_lines.append(line if cut is None else line[:cut])
    return "\n".join(out_lines)


def count_equation_blocks(raw_text: str) -> int:
    """Count equation-type environments + bare \\[ ... \\] blocks in raw_text."""
    n_env = len(EQ_BEGIN_RE.findall(raw_text))
    n_bracket = len(BRACKET_MATH_OPEN_RE.findall(raw_text))
    return n_env + n_bracket


def strip_non_prose(raw_text: str) -> str:
    """Reduce raw_text to flowing prose per the rules in the module docstring."""
    t = raw_text
    t = EQ_BLOCK_RE.sub(" ", t)
    t = BRACKET_MATH_RE.sub(" ", t)
    t = FIGURE_BLOCK_RE.sub(" ", t)
    t = TABLE_BLOCK_RE.sub(" ", t)
    t = LONGTABLE_BLOCK_RE.sub(" ", t)
    t = BIBLIO_BLOCK_RE.sub(" ", t)

    # protect version/decimal numeric chains from being read as sentence stops
    def _protect(m):
        return m.group(0).replace(".", "")

    t = DECIMAL_CHAIN_RE.sub(_protect, t)

    t = INLINE_MATH_RE.sub(" ", t)

    # unwrap one level of textbf/emph/textit/footnote/code (repeat twice to catch
    # simple sequential wrappers like \textbf{\emph{x}} — no deeper nesting found
    # in either file's prose)
    for _ in range(2):
        t = UNWRAP_RE.sub(r"\1", t)

    t = DROP_REF_RE.sub(" ", t)
    t = DROP_CMD_RE.sub(" ", t)
    t = DROP_BRACE_ARG_RE.sub(" ", t)
    t = STRAY_BRACE_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def count_sentences(prose_text: str) -> int:
    chunks = re.findall(r"[^.!?]*[.!?]", prose_text)
    n = len(chunks)
    consumed = sum(len(c) for c in chunks)
    remainder = prose_text[consumed:].strip()
    if len(remainder.replace(" ", "")) >= 5:
        n += 1
    return n


def find_headings(text_after_document: str):
    """Return list of dicts: level, title, label, start_pos (char offset).

    Title and \\label are extracted with manual brace-depth matching (not
    regex .*?) because titles routinely contain nested braces from inline
    math, e.g. \\section{LCO $\\Delta S_{\\rxn,j}^\\mathrm{cat}$ 분해}\\label{sec:lco-decomp}
    — a naive non-greedy regex stops at the FIRST '}' (inside the math), which
    then fails to see the \\label{...} that follows and silently drops it.
    """
    text = text_after_document
    headings = []
    for m in HEADING_START_RE.finditer(text):
        level = "section" if m.group("cmd") == r"\section" else "subsection"
        i = m.end()  # just after the opening '{'
        depth = 1
        title_start = i
        while i < len(text) and depth > 0:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        title_end = i - 1
        title = text[title_start:title_end]

        j = i
        while j < len(text) and text[j] in " \t":
            j += 1
        label = ""
        if text[j : j + 7] == "\\label{":
            k = j + 7
            depth2 = 1
            lbl_start = k
            while k < len(text) and depth2 > 0:
                if text[k] == "{":
                    depth2 += 1
                elif text[k] == "}":
                    depth2 -= 1
                k += 1
            label = text[lbl_start : k - 1]

        headings.append(
            {"level": level, "title": title, "label": label, "start": m.start()}
        )
    return headings


def analyze_file(path: Path, chapter_label: str):
    raw = path.read_text(encoding="utf-8")
    # isolate body: after \begin{document}
    doc_start = raw.find(r"\begin{document}")
    body = raw[doc_start:] if doc_start != -1 else raw
    # line number of doc_start (1-indexed) to convert char offsets -> line numbers
    prefix_lines = raw[:doc_start].count("\n") if doc_start != -1 else 0

    body_nocomment_for_headings = strip_comments(body)
    headings = find_headings(body_nocomment_for_headings)

    # boundary markers: bibliography start, end{document} — used to cap the
    # last heading's span
    biblio_m = re.search(r"\\begin\{thebibliography\}", body_nocomment_for_headings)
    enddoc_m = re.search(r"\\end\{document\}", body_nocomment_for_headings)
    cap_pos = None
    if biblio_m:
        cap_pos = biblio_m.start()
    elif enddoc_m:
        cap_pos = enddoc_m.start()
    else:
        cap_pos = len(body_nocomment_for_headings)

    rows = []
    for i, h in enumerate(headings):
        start = h["start"]
        end = headings[i + 1]["start"] if i + 1 < len(headings) else cap_pos
        if end > cap_pos and i + 1 >= len(headings):
            end = cap_pos
        raw_block_nocomment = body_nocomment_for_headings[start:end]

        # NOTE: start/end are char offsets into body_nocomment_for_headings
        # (that's where they were found), so newline-counting for line numbers
        # must use THAT string too, not the original `body` (comment removal
        # preserves line count 1:1 but shifts character offsets, so mixing the
        # two strings' coordinate systems silently produces wrong line numbers).
        line_start = prefix_lines + body_nocomment_for_headings[:start].count("\n") + 1
        line_end = prefix_lines + body_nocomment_for_headings[:end].count("\n")
        n_lines = line_end - line_start + 1

        n_eq = count_equation_blocks(raw_block_nocomment)
        prose = strip_non_prose(raw_block_nocomment)
        n_sent = count_sentences(prose)

        is_lco = "lco" in h["label"].lower()
        rows.append(
            {
                "chapter": chapter_label,
                "level": h["level"],
                "title": h["title"],
                "label": h["label"] or "(unlabeled)",
                "line_start": line_start,
                "line_end": line_end,
                "n_lines": n_lines,
                "n_equations": n_eq,
                "n_sentences": n_sent,
                "is_lco": is_lco,
            }
        )
    return rows


def classify_group(row):
    if row["chapter"] == "Ch2":
        return "Ch2"
    if row["is_lco"]:
        return "LCO"
    if row["label"] == "(unlabeled)":
        return "공통/서론"
    return "흑연"


def main():
    all_rows = analyze_file(CH1, "Ch1") + analyze_file(CH2, "Ch2")

    print("| Ch | Level | Title | Label | Lines | #Eq | #Sent | Group |")
    print("|---|---|---|---|---:|---:|---:|---|")
    for r in all_rows:
        title_short = r["title"]
        print(
            f"| {r['chapter']} | {r['level']} | {title_short} | {r['label']} | "
            f"{r['line_start']}-{r['line_end']} ({r['n_lines']}) | {r['n_equations']} | "
            f"{r['n_sentences']} | {classify_group(r)} |"
        )

    print()
    print("### Subtotals")
    groups = {}
    for r in all_rows:
        g = classify_group(r)
        groups.setdefault(g, {"n_lines": 0, "n_equations": 0, "n_sentences": 0, "n_headings": 0})
        groups[g]["n_lines"] += r["n_lines"]
        groups[g]["n_equations"] += r["n_equations"]
        groups[g]["n_sentences"] += r["n_sentences"]
        groups[g]["n_headings"] += 1

    for g, v in groups.items():
        ratio = v["n_sentences"] / v["n_equations"] if v["n_equations"] else float("nan")
        print(
            f"- {g}: headings={v['n_headings']}, lines={v['n_lines']}, "
            f"equations={v['n_equations']}, sentences={v['n_sentences']}, "
            f"sent/eq={ratio:.2f}"
        )

    # Literal 2-way Ch1 split requested by the task ("LCO 관련 절과 흑연 본체 절을
    # 분리 소계"): merge the 3-way {흑연, 공통/서론, LCO} breakdown above into
    # {흑연 본체 (= 흑연 + 공통/서론), LCO} — the unlabeled subsections are
    # overwhelmingly child derivation blocks of a labeled 흑연 parent \section
    # (e.g. sec:center's own text is 3 sentences; its 2 unlabeled child
    # subsections carry the other 24), so folding them into 흑연 본체 is the
    # correct rollup, not a separate bucket.
    g1 = groups.get("흑연", {"n_lines": 0, "n_equations": 0, "n_sentences": 0, "n_headings": 0})
    g2 = groups.get("공통/서론", {"n_lines": 0, "n_equations": 0, "n_sentences": 0, "n_headings": 0})
    merged = {
        k: g1.get(k, 0) + g2.get(k, 0) for k in ("n_lines", "n_equations", "n_sentences", "n_headings")
    }
    mratio = merged["n_sentences"] / merged["n_equations"] if merged["n_equations"] else float("nan")
    print()
    print(
        f"- 흑연 본체 (merged, = 흑연 + 공통/서론): headings={merged['n_headings']}, "
        f"lines={merged['n_lines']}, equations={merged['n_equations']}, "
        f"sentences={merged['n_sentences']}, sent/eq={mratio:.2f}"
    )

    print()
    print("### Top prose/equation ratio headings (compression priority)")
    ranked = sorted(
        all_rows,
        key=lambda r: (r["n_sentences"] / r["n_equations"] if r["n_equations"] else r["n_sentences"] * 1.0),
        reverse=True,
    )
    for r in ranked[:5]:
        ratio = r["n_sentences"] / r["n_equations"] if r["n_equations"] else float("inf")
        print(
            f"- [{r['chapter']}/{classify_group(r)}] {r['title']} ({r['label']}): "
            f"{r['n_sentences']} sent / {r['n_equations']} eq -> ratio {ratio:.2f}"
        )


if __name__ == "__main__":
    main()
