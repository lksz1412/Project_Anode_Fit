#!/usr/bin/env python3
r"""Static verifier for the physics-conformance manuscript.

The verifier deliberately reads every reachable TeX source in full.  It checks
the resolved ``\input``/``\include`` graph, labels and references, stable label
identifiers, orphan sources, and the physics-only/implementation boundary.

It is standalone and uses only the Python standard library:

    python3 verify_manuscript.py [path/to/anode_physics_master.tex]
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
from pathlib import Path
import re
import sys
from typing import Iterable


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[4]
DEFAULT_MANUSCRIPT_ROOT = (
    REPO_ROOT / "Codex/results/v1025_2_physics_branch/manuscript"
)
DEFAULT_MASTER = DEFAULT_MANUSCRIPT_ROOT / "anode_physics_master.tex"
IMPLEMENTATION_ALLOWLIST = frozenset(
    {Path("appendices/implementation_interface.tex")}
)

INCLUDE_RE = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
LABEL_RE = re.compile(r"\\label\s*\{([^{}]+)\}")
PHYSID_RE = re.compile(r"\\physid\s*\{([^{}]+)\}")
REFERENCE_RE = re.compile(
    r"\\(?:ref|eqref|autoref|pageref|cref|Cref)\*?\s*\{([^{}]+)\}"
)
STABLE_ID_RE = re.compile(
    r"(?:^|:)"
    r"(?:OBS|BAL|EQ|KIN|THM|HYS|EMP|ASM|MAT-(?:GR|LCO|SI))"
    r"(?:-[A-Z0-9]+)+"
    r"(?:$|:)"
)
EXTERNAL_LABELS = frozenset({"LastPage"})

# The physics manuscript may use mathematical terms such as "mapping" and
# "model".  The patterns below are intentionally limited to implementation
# artifacts, programming syntax, work-history vocabulary, and named software.
FORBIDDEN_IMPLEMENTATION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "code-literal",
        re.compile(r"`[^`\n]+`"),
    ),
    (
        "source-file",
        re.compile(
            r"(?<![\\\w])[\w.-]+\.(?:py|json|yaml|yml|toml|md|html|csv|npz|"
            r"tex|bib)"
            r"(?!\w)",
            re.IGNORECASE,
        ),
    ),
    (
        "repository-path",
        re.compile(
            r"(?<!\w)(?:Codex|Claude|src|tests?)/[\w./-]+",
            re.IGNORECASE,
        ),
    ),
    (
        "programming-term",
        re.compile(
            r"\b(?:API|NumPy|SciPy|pandas|Python|pytest|"
            r"unit[ -]?test|test[ -]?gate|source[ -]?code|implementation[ -]?"
            r"symbol)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "implementation-symbol",
        re.compile(
            r"\b(?:safe_logistic|EmpiricalSkewComponent|EmpiricalSkewProfile|"
            r"empirical_blend14_v10252|ObservationContract|IdealTransition|"
            r"LinearChemicalBackground|PhysicalHost|PhysicalHostBlend|"
            r"CausalInitialState|relax_monotonic_curve|relax_time_trajectory|"
            r"EyringRateSI|LegacyCompatibleHourRate|"
            r"c_rate_per_hour_to_per_second|reversible_heat_generation_w|"
            r"terminal_irreversible_heat_w|local_network_irreversible_heat_w|"
            r"GraphiteAnodeDischargeDQDV|BlendedAnodeDQDV)\b"
        ),
    ),
    (
        "test-output",
        re.compile(
            r"\b(?:test output|test_[A-Za-z0-9_]+|"
            r"(?:PASS|FAIL)\s+\d+\s*/\s*\d+)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "work-history",
        re.compile(
            r"\b(?:commit|pull request|merge|phase\s+\d+|step\s+\d+|"
            r"version history|changelog|work log|"
            r"(?:git|working|feature|release)\s+branch|branch\s+(?:name|tip))\b",
            re.IGNORECASE,
        ),
    ),
)
ALWAYS_EXTERNAL_CATEGORIES = frozenset(
    {"source-file", "repository-path", "work-history", "test-output"}
)


@dataclass(frozen=True, order=True)
class Issue:
    """One deterministic verifier finding."""

    code: str
    path: Path
    line: int
    detail: str

    def render(self, root: Path) -> str:
        try:
            shown = self.path.relative_to(root)
        except ValueError:
            shown = self.path
        suffix = f":{self.line}" if self.line > 0 else ""
        return f"{self.code}: {shown}{suffix}: {self.detail}"


@dataclass(frozen=True)
class VerificationReport:
    """Complete graph and findings from one verification pass."""

    master: Path
    sources: tuple[Path, ...]
    edges: tuple[tuple[Path, Path], ...]
    labels: tuple[str, ...]
    references: tuple[str, ...]
    issues: tuple[Issue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


def _strip_comments(text: str) -> str:
    r"""Remove TeX comments without treating escaped ``\%`` as comments."""

    cleaned: list[str] = []
    for raw_line in text.splitlines(keepends=True):
        comment_at: int | None = None
        for index, character in enumerate(raw_line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and raw_line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                comment_at = index
                break
        if comment_at is None:
            cleaned.append(raw_line)
        elif raw_line.endswith("\n"):
            cleaned.append(raw_line[:comment_at] + "\n")
        else:
            cleaned.append(raw_line[:comment_at])
    return "".join(cleaned)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _resolve_include(source: Path, raw_target: str) -> Path:
    target = Path(raw_target.strip())
    if target.suffix == "":
        target = target.with_suffix(".tex")
    return (source.parent / target).resolve()


def _relative_or_absolute(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _iter_forbidden_terms(text: str) -> Iterable[tuple[str, int, str]]:
    # Include commands necessarily contain file-like paths.  They are graph
    # metadata, not manuscript prose, and are checked independently.
    scan_text = INCLUDE_RE.sub("", text)
    for category, pattern in FORBIDDEN_IMPLEMENTATION_PATTERNS:
        for match in pattern.finditer(scan_text):
            yield category, _line_number(scan_text, match.start()), match.group(0)


def verify_manuscript(
    master: Path = DEFAULT_MASTER,
    *,
    implementation_allowlist: frozenset[Path] = IMPLEMENTATION_ALLOWLIST,
    require_stable_ids: bool = True,
    require_all_sources_reachable: bool = True,
) -> VerificationReport:
    """Read and verify the complete manuscript source graph."""

    master = master.resolve()
    root = master.parent
    issues: list[Issue] = []
    sources: list[Path] = []
    edges: list[tuple[Path, Path]] = []
    texts: dict[Path, str] = {}
    include_locations: dict[tuple[Path, Path], int] = {}
    visiting: list[Path] = []
    visited: set[Path] = set()

    def visit(source: Path) -> None:
        if source in visiting:
            cycle = visiting[visiting.index(source) :] + [source]
            issues.append(
                Issue(
                    "INCLUDE_CYCLE",
                    source,
                    0,
                    " -> ".join(str(_relative_or_absolute(p, root)) for p in cycle),
                )
            )
            return
        if source in visited:
            return
        if not source.is_file():
            issues.append(Issue("MISSING_SOURCE", source, 0, "source does not exist"))
            return
        try:
            source.relative_to(root)
        except ValueError:
            issues.append(
                Issue(
                    "OUTSIDE_MANUSCRIPT_ROOT",
                    source,
                    0,
                    "included source escapes the manuscript root",
                )
            )
            return

        visiting.append(source)
        raw_text = source.read_text(encoding="utf-8")
        text = _strip_comments(raw_text)
        texts[source] = text
        sources.append(source)

        for match in INCLUDE_RE.finditer(text):
            target = _resolve_include(source, match.group(1))
            edge = (source, target)
            if edge in include_locations:
                issues.append(
                    Issue(
                        "DUPLICATE_INCLUDE",
                        source,
                        _line_number(text, match.start()),
                        f"{match.group(1)!r} is already included from this source",
                    )
                )
            else:
                include_locations[edge] = _line_number(text, match.start())
                edges.append(edge)
            if not target.is_file():
                issues.append(
                    Issue(
                        "MISSING_INCLUDE",
                        source,
                        _line_number(text, match.start()),
                        f"{match.group(1)!r} resolves to missing {target}",
                    )
                )
                continue
            visit(target)

        visiting.pop()
        visited.add(source)

    if not master.is_file():
        issues.append(Issue("MISSING_MASTER", master, 0, "master source does not exist"))
    else:
        visit(master)

    if require_all_sources_reachable and root.is_dir():
        all_sources = {path.resolve() for path in root.rglob("*.tex")}
        for orphan in sorted(all_sources - visited):
            issues.append(
                Issue(
                    "ORPHAN_SOURCE",
                    orphan,
                    0,
                    "TeX source is not reachable from the master include graph",
                )
            )

    labels_by_name: dict[str, list[tuple[Path, int]]] = {}
    references: list[tuple[str, Path, int]] = []
    for source, text in texts.items():
        relative = source.relative_to(root)
        for match in LABEL_RE.finditer(text):
            label = match.group(1).strip()
            # A label containing a TeX macro argument token is a template in a
            # command definition, not a concrete label in the resolved graph.
            if "#" in label:
                continue
            line = _line_number(text, match.start())
            labels_by_name.setdefault(label, []).append((source, line))
            if require_stable_ids and not STABLE_ID_RE.search(label):
                issues.append(
                    Issue(
                        "UNSTABLE_LABEL",
                        source,
                        line,
                        f"{label!r} has no stable physics identifier",
                    )
                )
        for match in PHYSID_RE.finditer(text):
            identifier = match.group(1).strip()
            if "#" in identifier:
                continue
            label = f"phys:{identifier}"
            line = _line_number(text, match.start())
            labels_by_name.setdefault(label, []).append((source, line))
            if require_stable_ids and not STABLE_ID_RE.search(label):
                issues.append(
                    Issue(
                        "UNSTABLE_PHYSICS_ID",
                        source,
                        line,
                        f"{identifier!r} is outside the stable ID namespaces",
                    )
                )
        for match in REFERENCE_RE.finditer(text):
            # cleveref accepts comma-separated labels in one command.
            line = _line_number(text, match.start())
            for raw_label in match.group(1).split(","):
                label = raw_label.strip()
                if label:
                    references.append((label, source, line))

        for category, line, token in _iter_forbidden_terms(text):
            if (
                relative not in implementation_allowlist
                or category in ALWAYS_EXTERNAL_CATEGORIES
            ):
                issues.append(
                    Issue(
                        "IMPLEMENTATION_TERM_OUTSIDE_BOUNDARY",
                        source,
                        line,
                        f"{category}: {token!r}",
                    )
                )

    for label, locations in labels_by_name.items():
        if len(locations) > 1:
            for source, line in locations:
                issues.append(
                    Issue(
                        "DUPLICATE_LABEL",
                        source,
                        line,
                        f"{label!r} is defined {len(locations)} times",
                    )
                )
    for label, source, line in references:
        if label not in labels_by_name and label not in EXTERNAL_LABELS:
            issues.append(
                Issue(
                    "UNRESOLVED_REFERENCE",
                    source,
                    line,
                    f"{label!r} is not defined in the resolved source graph",
                )
            )

    issues.sort()
    return VerificationReport(
        master=master,
        sources=tuple(sources),
        edges=tuple(edges),
        labels=tuple(sorted(labels_by_name)),
        references=tuple(sorted(label for label, _, _ in references)),
        issues=tuple(issues),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "master",
        nargs="?",
        type=Path,
        default=DEFAULT_MASTER,
        help="top-level TeX source",
    )
    parser.add_argument(
        "--allow-unstable-labels",
        action="store_true",
        help="do not require OBS/BAL/EQ/KIN/THM/HYS/MAT/EMP/ASM label IDs",
    )
    parser.add_argument(
        "--allow-orphans",
        action="store_true",
        help="do not fail on TeX sources unreachable from the master",
    )
    args = parser.parse_args(argv)
    report = verify_manuscript(
        args.master,
        require_stable_ids=not args.allow_unstable_labels,
        require_all_sources_reachable=not args.allow_orphans,
    )
    if report.ok:
        print(
            "PASS: "
            f"{len(report.sources)} sources, {len(report.edges)} include edges, "
            f"{len(report.labels)} labels, {len(report.references)} references"
        )
        return 0
    print(
        "FAIL: "
        f"{len(report.issues)} issue(s) across {len(report.sources)} resolved source(s)",
        file=sys.stderr,
    )
    for issue in report.issues:
        print(issue.render(report.master.parent), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
