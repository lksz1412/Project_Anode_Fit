#!/usr/bin/env python3
"""Emit the bounded source manifest used by the Phase 054 latest review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
INPUTS = {
    "latest_release_code": (
        "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
    ),
    "latest_archive_note": "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md",
    "latest_handover": (
        "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md"
    ),
    "latest_graphite_two_layer_section": (
        "Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex"
    ),
    "latest_input_contract_section": (
        "Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex"
    ),
    "latest_regular_solution_section": (
        "Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex"
    ),
    "legacy_gate_v1024": "Claude/docs/v1.0.25.2/test_gates_v1024.py",
    "legacy_gate_v1025": "Claude/docs/v1.0.25.2/test_gates_v1025.py",
    "candidate_master_manuscript": (
        "Codex/results/v1025_2_physics_branch/manuscript/"
        "anode_physics_master.tex"
    ),
    "candidate_implementation_appendix": (
        "Codex/results/v1025_2_physics_branch/manuscript/"
        "appendices/implementation_interface.tex"
    ),
}


def run() -> dict:
    files = {}
    for role, relative_path in INPUTS.items():
        path = REPO / relative_path
        payload = path.read_bytes()
        files[role] = {
            "path": relative_path,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
            "lines": len(payload.decode("utf-8").splitlines()),
        }
    return {
        "lineage": {
            "historical_candidate_tip": (
                "2abf019c7fee9bebd84b49cc9530f6983b08a8fa"
            ),
            "historical_candidate_baseline": (
                "ab196b292e14492b647f87a6c0d1d8c9ed0630ab"
            ),
            "latest_accepted_v1025_2_tip": (
                "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
            ),
            "default_correction_commit": (
                "7b342dd88aad6bf9ff08cb3568da374837008ca7"
            ),
            "integration_method": (
                "non-force merge into codex/v1025_2-physics-conformance"
            ),
            "v1026_excluded": True,
        },
        "scope": (
            "Bounded latest-lineage review inputs. This intentionally replaces "
            "the stale ancestry-sensitive Phase 044 manifest for latest-release "
            "claims; it does not erase the historical manifest."
        ),
        "files": files,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
