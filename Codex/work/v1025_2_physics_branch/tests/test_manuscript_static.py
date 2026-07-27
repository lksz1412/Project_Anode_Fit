"""Self-tests and integration gate for ``verify_manuscript``."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from verify_manuscript import DEFAULT_MASTER, verify_manuscript


class ManuscriptVerifierSelfTest(unittest.TestCase):
    def _write(self, root: Path, relative: str, text: str) -> Path:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def test_valid_graph_and_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = self._write(
                root,
                "master.tex",
                "\\input{chapters/physics}\n"
                "\\input{appendices/implementation_interface}\n",
            )
            self._write(
                root,
                "chapters/physics.tex",
                "\\section{Balance}\\label{sec:BAL-001}\n"
                "물리적 전하 보존은 식~\\ref{eq:BAL-002}를 따른다.\n"
                "\\begin{equation}Q=a\\xi\\label{eq:BAL-002}\\end{equation}\n",
            )
            self._write(
                root,
                "appendices/implementation_interface.tex",
                "The Python class `PhysicalHost` implements the interface.\n",
            )
            report = verify_manuscript(master)
            self.assertTrue(
                report.ok,
                "\n".join(issue.render(root) for issue in report.issues),
            )

    def test_missing_include_duplicate_label_and_reference_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = self._write(
                root,
                "master.tex",
                "\\input{one}\n\\input{missing}\n",
            )
            self._write(
                root,
                "one.tex",
                "\\label{eq:EQ-001}\\label{eq:EQ-001}\\ref{eq:EQ-404}\n",
            )
            report = verify_manuscript(master)
            codes = {issue.code for issue in report.issues}
            self.assertIn("MISSING_INCLUDE", codes)
            self.assertIn("DUPLICATE_LABEL", codes)
            self.assertIn("UNRESOLVED_REFERENCE", codes)

    def test_implementation_term_is_rejected_outside_appendix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = self._write(root, "master.tex", "\\input{physics}\n")
            self._write(
                root,
                "physics.tex",
                "\\section{State}\\label{sec:OBS-001}\n"
                "The Python function `unsafe_solver` is not physics prose.\n",
            )
            report = verify_manuscript(master)
            self.assertTrue(
                any(
                    issue.code == "IMPLEMENTATION_TERM_OUTSIDE_BOUNDARY"
                    for issue in report.issues
                )
            )

    def test_file_and_work_history_remain_external_even_in_appendix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = self._write(
                root,
                "master.tex",
                "\\input{appendices/implementation_interface}\n",
            )
            self._write(
                root,
                "appendices/implementation_interface.tex",
                "PhysicalHost is allowed here, but model.py and commit abc are not.\n",
            )
            report = verify_manuscript(master)
            categories = {issue.detail.split(":", 1)[0] for issue in report.issues}
            self.assertIn("source-file", categories)
            self.assertIn("work-history", categories)

    def test_comments_do_not_create_false_graph_or_reference_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            master = self._write(
                root,
                "master.tex",
                "% \\input{missing}\n"
                "\\section{Observation}\\label{sec:OBS-001}\n"
                "% \\ref{eq:OBS-999}\n",
            )
            report = verify_manuscript(master)
            self.assertTrue(
                report.ok,
                "\n".join(issue.render(root) for issue in report.issues),
            )


class ManuscriptIntegrationTest(unittest.TestCase):
    def test_candidate_manuscript_passes_static_gate(self) -> None:
        self.assertTrue(
            DEFAULT_MASTER.is_file(),
            f"candidate master has not been created: {DEFAULT_MASTER}",
        )
        report = verify_manuscript(DEFAULT_MASTER)
        self.assertTrue(
            report.ok,
            "\n".join(
                issue.render(DEFAULT_MASTER.parent) for issue in report.issues
            ),
        )


if __name__ == "__main__":
    unittest.main()
