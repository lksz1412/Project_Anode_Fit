"""Execute an immutable conformance snapshot; preserve actual child evidence."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
PLAN = ROOT / "Codex/plans/2026-09-07-phase068-step095-conformance-model-manifest-addendum.md"
RESULT = ROOT / "Codex/results/PHASE_068_STEP_095_CONFORMANCE_MODEL_ADJUDICATION_RESULT.md"
TESTS = "Codex/work/v1025_2_physics_branch/tests"
MODEL = "Codex/work/v1025_2_physics_branch"

def capture(command, cwd):
    child = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="strict",
                           env=os.environ | {"PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    return {"command": command, "exit_code": child.returncode,
            "stdout": child.stdout, "stderr": child.stderr}

def verify_file(path, oid):
    raw = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if actual != oid:
        raise ValueError("source blob mismatch: " + str(path))
    return {"blob": actual, "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "lines": len(raw.splitlines())}

def write_new(path, payload):
    raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      indent=2, allow_nan=False) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(raw)

def export():
    rows = re.findall(r"^\| ((?:Codex|Claude)/[^|]+?) \| ([0-9a-f]{40}) \|",
                      PLAN.read_text(encoding="utf-8"), re.M)
    if len(rows) != 49 or len({p for p, _ in rows}) != 49:
        raise ValueError("exact 49 frozen source paths required")
    directory = Path(tempfile.mkdtemp(prefix="anode-step95-"))
    identities = []
    for relative, oid in rows:
        raw = subprocess.check_output(["git", "show", TIP + ":" + relative], cwd=ROOT)
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        identities.append({"path": relative, **verify_file(path, oid)})
    return directory, identities

PROBES = r'''
import json, sys, warnings
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.cwd() / "Codex/work/v1025_2_physics_branch"))
import conformance_model as m
rows = []
def probe(name, inputs, call):
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        try:
            value = np.asarray(call(), dtype=float)
            outcome = {"value_repr": repr(value.tolist()), "all_finite": bool(np.isfinite(value).all())}
        except Exception as exc:
            outcome = {"exception": type(exc).__name__, "message": str(exc)}
    rows.append({"id": name, "inputs": inputs, "outcome": outcome,
                 "warnings": [str(w.message) for w in recorded]})
initial = m.CausalInitialState(0.0, m.InitialConditionProvenance.SUPPLIED_STATE, "bounded probe")
tiny = float(np.nextafter(0.0, 1.0))
huge = float(np.finfo(float).max)
probe("C92-19", {"time": [0,1], "target": [0,0], "tau": tiny},
      lambda: m.relax_time_trajectory(np.array([0.,1.]), np.array([0.,0.]), tiny, initial))
probe("C92-20", {"V": .2, "T": 298.15, "z": huge},
      lambda: m.IdealTransition(.1, 1., 1, huge).dstate_dv(.2, 298.15))
probe("C92-21", {"center": 0., "V": 0., "width": tiny, "alpha": 2.},
      lambda: m.EmpiricalSkewComponent(0., tiny, 1., 2.).density(0.))
probe("C92-22-reversible", {"I": huge, "T": 300., "dU_dT": 1.},
      lambda: m.reversible_heat_generation_w(huge, 300., 1.))
probe("C92-22-terminal", {"I": huge, "U": 2., "V": 0.},
      lambda: m.terminal_irreversible_heat_w(huge, 2., 0.))
probe("C92-22-network", {"Q": huge, "z": 1., "T": 1e308, "Jplus": 1e-308, "Jminus": 5e-309},
      lambda: m.local_network_irreversible_heat_w(huge, 1., 1e308, 1e-308, 5e-309))
print(json.dumps(rows, allow_nan=False))
'''

def execute(directory, identities):
    versions = {}
    for package in ("numpy", "pandas", "scipy"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "MISSING"
    collect_code = (
        "import unittest,json; s=unittest.defaultTestLoader.discover('.',pattern='test_*.py'); "
        "print(json.dumps({'collected_cases':s.countTestCases(),"
        "'loader_errors':unittest.defaultTestLoader.errors}))")
    commands = {
        "collection": [sys.executable, "-B", "-c", collect_code],
        "suite": [sys.executable, "-B", "run_all.py"],
        "manuscript": [sys.executable, "-B", "verify_manuscript.py"],
    }
    runs = {key: capture(command, directory / TESTS) for key, command in commands.items()}
    runs["bounded_probes"] = capture([sys.executable, "-B", "-c", PROBES], directory)
    diagnostic = (
        "import json,math,numpy as np; from _reference import *; "
        "m=import_model(); p=m.empirical_blend14_v10252(); v,y=processed_blend_curve(); "
        "pred=p.evaluate(v); residual=y-pred; direct=canonical_release_prediction(v); "
        "print(json.dumps({'points':len(v),'hashes':{k:le_f64_sha256(a) for k,a in "
        "[('voltage',v),('observed',y),('parameters',stored_parameter_vector()),"
        "('prediction',pred),('residual',residual)]},"
        "'r2':coefficient_of_determination(y,pred),"
        "'bic57':len(v)*math.log(float(np.sum(residual**2))/len(v))+57*math.log(len(v)),"
        "'max_abs_prediction_vs_independent':float(np.max(np.abs(pred-direct))),"
        "'all_arrays_finite':bool(all(np.isfinite(a).all() for a in [v,y,pred,residual]))},allow_nan=False))")
    runs["empirical_diagnostics"] = capture([sys.executable, "-B", "-c", diagnostic], directory / TESTS)
    for row in identities:
        verify_file(directory / row["path"], row["blob"])
    result_hash = hashlib.sha256(RESULT.read_bytes().replace(b"\r\n", b"\n")).hexdigest() if RESULT.is_file() else None
    return {"schema": "P068-STEP95-RUNTIME-1", "frozen_tip": TIP,
            "python": sys.version, "executable": sys.executable,
            "dependencies": versions, "snapshot_directory": str(directory),
            "sources": identities, "sources_unchanged_after_execution": True,
            "runs": runs, "result_lf_sha256": result_hash,
            "authority": "INTERNAL_TEST_AND_BOUNDED_PROBE_ONLY",
            "runner_lf_sha256": hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", type=Path)
    parser.add_argument("--baseline-python", type=Path)
    args = parser.parse_args()
    if args.record and not RESULT.is_file():
        raise FileNotFoundError("result-first required")
    if args.record and args.record.exists():
        raise FileExistsError(args.record)
    directory, identities = export()
    evidence = execute(directory, identities)
    if args.baseline_python:
        evidence["baseline_runtime"] = capture(
            [str(args.baseline_python), "-B", str(Path(__file__).resolve())], ROOT)
    if args.record:
        write_new(args.record, evidence)
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
