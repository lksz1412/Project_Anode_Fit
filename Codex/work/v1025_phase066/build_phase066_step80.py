#!/usr/bin/env python3
"""Build Phase 066 Step 80 profile/default/temperature evidence.

Frozen baseline blobs are materialized outside the repository.  Every profile
route is imported and evaluated in a separate isolated Python process.  The
working-tree Claude tree is never imported or modified.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "d091e7881f9f22d5dfe9511427afdf4ef22e3280"
EXPECTED_SUBJECT = "audit(phase066): verify profile default temperature routes"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
MATRIX_NAME = "PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"
RUNTIME_NAME = "PHASE_066_RUNTIME_ATTESTATION.json"
MATRIX_OUT = ROOT / "Codex/results" / MATRIX_NAME
RUNTIME_OUT = ROOT / "Codex/results" / RUNTIME_NAME

CONTROL_PATHS = (
    "Codex/work/v1025_phase066/build_phase066_step80.py",
    "Codex/work/v1025_phase066/validate_phase066_step80.py",
    "Codex/results/PHASE_066_STEP_080_PROFILE_TEMPERATURE_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_PATHS = tuple(sorted((*CONTROL_PATHS,
                            f"Codex/results/{MATRIX_NAME}",
                            f"Codex/results/{RUNTIME_NAME}")))

SOURCE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
TEST1024_PATH = "Claude/docs/v1.0.25.2/test_gates_v1024.py"
TEST1025_PATH = "Claude/docs/v1.0.25.2/test_gates_v1025.py"
HANDOVER_PATH = "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md"
ARCHIVE_PATH = "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md"
GUIDE_PATH = "Claude/docs/v1.0.25.2/FITTING_GUIDE.md"
SERIALIZED_PATHS = {
    "serialized_regsol_8": "Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json",
    "serialized_gallery_14": "Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json",
    "serialized_skew_14": "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
}
INPUT_PATHS = (SOURCE_PATH, TEST1024_PATH, TEST1025_PATH, HANDOVER_PATH,
               ARCHIVE_PATH, GUIDE_PATH, *SERIALIZED_PATHS.values())
PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")),
                    ("3.14", ("py", "-3.14")))
ROUTE_IDS = (
    "fresh_default_4_2",
    "explicit_legacy_4_2",
    "from_wt_sic_4_2",
    "toggle_skew_7_7",
    "explicit_skew_7_7",
    "explicit_xrd_5_2",
    "explicit_msmr6_6_2",
    "explicit_legacy_4_si7",
    "explicit_skew7_symmetric7",
    "explicit_legacy_4_elemental2",
    "explicit_legacy_4_siox1",
    "lco3_electronic_off",
    "lco3_electronic_on",
    "serialized_regsol_8",
    "serialized_gallery_14",
    "serialized_skew_14",
)


def _subprocess(args: tuple[str, ...], *, cwd: Path, timeout: int = 180,
                env: dict[str, str] | None = None,
                check: bool = True) -> subprocess.CompletedProcess[bytes]:
    cp = subprocess.run(list(args), cwd=cwd, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, timeout=timeout, check=False,
                        shell=False)
    if check and cp.returncode != 0:
        raise RuntimeError(
            f"command failed ({cp.returncode}): {args!r}\n"
            f"stdout={cp.stdout.decode('utf-8', 'replace')}\n"
            f"stderr={cp.stderr.decode('utf-8', 'replace')}"
        )
    return cp


def run_git(args: tuple[str, ...], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    if not args or args[0] != "git":
        raise RuntimeError("run_git accepts only an explicit git argv tuple")
    return _subprocess(args, cwd=ROOT, timeout=120, check=check)


def run_runtime(args: tuple[str, ...], *, cwd: Path,
                env: dict[str, str]) -> subprocess.CompletedProcess[bytes]:
    if not any(args[:2] == launcher for _, launcher in PYTHON_LAUNCHERS):
        raise RuntimeError("runtime launcher outside pinned allowlist")
    resolved = cwd.resolve()
    if resolved == ROOT.resolve() or ROOT.resolve() in resolved.parents:
        raise RuntimeError("runtime cwd must remain outside repository")
    return _subprocess(args, cwd=resolved, timeout=300, env=env, check=False)


def git_bytes(path: str) -> bytes:
    return run_git(("git", "cat-file", "blob", f"{BASELINE}:{path}")).stdout


def git_blob(path: str) -> str:
    return run_git(("git", "rev-parse", f"{BASELINE}:{path}")).stdout.decode().strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def semantic_projection(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("semantic_sha256", None)
    return out


def finalize(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = sha256(compact(semantic_projection(value)))
    return value


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                         allow_nan=False) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
        if temporary.resolve().parent != path.parent.resolve():
            raise RuntimeError("temporary output escaped approved directory")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def explicit_targets(candidate: Path) -> tuple[Path, Path]:
    out_dir = candidate.resolve()
    if out_dir == ROOT.resolve() or ROOT.resolve() in out_dir.parents:
        raise RuntimeError("explicit output directory must remain outside repository")
    return out_dir / RUNTIME_NAME, out_dir / MATRIX_NAME


def guard_json_last() -> None:
    staged = sorted(run_git(("git", "diff", "--cached", "--name-only")).stdout.decode().splitlines())
    if staged not in (sorted(CONTROL_PATHS), sorted(EXACT_PATHS)):
        raise SystemExit(f"JSON-last requires exact six controls or exact eight paths; got {staged}")
    unstaged = sorted(run_git(("git", "diff", "--name-only", "--",
                               *CONTROL_PATHS)).stdout.decode().splitlines())
    if unstaged:
        raise SystemExit(f"control files have unstaged changes: {unstaged}")


def source_ref(path: str, line_start: int, line_end: int,
               evidence: str) -> dict[str, Any]:
    return {
        "commit": BASELINE,
        "path": path,
        "blob": git_blob(path),
        "line_start": line_start,
        "line_end": line_end,
        "evidence": evidence,
    }


def input_binding(path: str) -> dict[str, Any]:
    raw = git_bytes(path)
    return {
        "commit": BASELINE,
        "path": path,
        "blob": git_blob(path),
        "sha256": sha256(raw),
        "bytes": len(raw),
        "lines": len(raw.decode("utf-8").splitlines()),
    }


def assignment_name(node: ast.AST) -> str | None:
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        target = node.targets[0] if isinstance(node, ast.Assign) else node.target
        if isinstance(target, ast.Name):
            return target.id
    return None


def static_analysis() -> dict[str, Any]:
    raw = git_bytes(SOURCE_PATH)
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=SOURCE_PATH)
    assignments = {assignment_name(node): node for node in tree.body
                   if assignment_name(node) is not None}
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    literal_names = (
        "GRAPHITE_STAGING_LIT", "GRAPHITE_STAGING_XRD_v1024",
        "GRAPHITE_STAGING_MSMR6_LIT", "GRAPHITE_MSMR7_LIT",
        "SI_ELEMENTAL_LIT", "SIOX_LIT", "SIC_LIT", "SI_MSMR7_LIT",
        "SI_MSMR7_SKEW_LIT",
    )
    literals: dict[str, Any] = {}
    for name in literal_names:
        node = assignments[name]
        value_node = node.value
        value = ast.literal_eval(value_node)
        literals[name] = {
            "count": len(value),
            "keys_union": sorted({key for item in value for key in item}),
            "has_thermodynamic_center": all(
                "dH_rxn" in item and "dS_rxn" in item for item in value),
            "has_thermal_width": all("n" in item for item in value),
            "all_w_only_or_fixed_u": all("U" in item and "w" in item for item in value),
            "line_start": node.lineno,
            "line_end": node.end_lineno,
        }

    default_gr = assignments["DEFAULT_GRAPHITE_TRANSITIONS"]
    default_si = assignments["DEFAULT_SI_TRANSITIONS"]
    toggle = functions["use_skew7_default"]
    toggle_global = next(node for node in toggle.body if isinstance(node, ast.Global))
    toggle_if = next(node for node in toggle.body if isinstance(node, ast.If))
    toggle_true = {
        node.targets[0].id: ast.unparse(node.value)
        for node in toggle_if.body
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
    }
    toggle_false = {
        node.targets[0].id: ast.unparse(node.value)
        for node in toggle_if.orelse
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
    }
    blended = classes["BlendedAnodeDQDV"]
    init = next(node for node in blended.body
                if isinstance(node, ast.FunctionDef) and node.name == "__init__")
    from_wt = next(node for node in blended.body
                   if isinstance(node, ast.FunctionDef) and node.name == "from_wt")
    name_loads = {name: 0 for name in ("DEFAULT_CBG_GRAPHITE", "DEFAULT_CBG_SI")}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in name_loads:
            name_loads[node.id] += 1

    return {
        "production_ast": {
            "parse": "PASS",
            "source_lines": len(text.splitlines()),
            "literal_profiles": literals,
            "fresh_default_assignments": {
                "graphite": ast.unparse(default_gr.value),
                "silicon": ast.unparse(default_si.value),
                "line_range": [default_gr.lineno, default_si.end_lineno],
            },
            "toggle_function": {
                "present": True,
                "name": toggle.name,
                "parameter": {
                    "name": toggle.args.args[0].arg,
                    "annotation": ast.unparse(toggle.args.args[0].annotation),
                    "default": ast.literal_eval(toggle.args.defaults[0]),
                },
                "global_names": sorted(toggle_global.names),
                "true_assignments": toggle_true,
                "false_assignments": toggle_false,
                "line_range": [toggle.lineno, toggle.end_lineno],
            },
            "legacy_function": {
                "present": "use_legacy_4transition" in functions,
                "comment_occurrences": text.count("use_legacy_4transition"),
            },
            "absent_named_routing_apis": {
                "load_profile": "GROUND_NOT_FOUND" if "load_profile" not in functions else "PRESENT",
                "from_profile": "GROUND_NOT_FOUND" if "from_profile" not in functions else "PRESENT",
                "PROFILE_ALIASES": "GROUND_NOT_FOUND" if "PROFILE_ALIASES" not in assignments else "PRESENT",
                "SAVED_PROFILES": "GROUND_NOT_FOUND" if "SAVED_PROFILES" not in assignments else "PRESENT",
                "module___all__": "GROUND_NOT_FOUND" if "__all__" not in assignments else "PRESENT",
            },
            "blended_constructor": {
                "line_range": [init.lineno, init.end_lineno],
                "default_graphite_pointer_load": "DEFAULT_GRAPHITE_TRANSITIONS" in ast.unparse(init),
                "default_si_pointer_load": "DEFAULT_SI_TRANSITIONS" in ast.unparse(init),
                "si_case_fallback_load": "SI_CASE_SETS" in ast.unparse(init),
                "explicit_override_precedence": (
                    "graphite_transitions is None" in ast.unparse(init)
                    and "si_transitions is None" in ast.unparse(init)
                ),
            },
            "from_wt_alias": {
                "line_range": [from_wt.lineno, from_wt.end_lineno],
                "returns_constructor": "return cls(" in ast.unparse(from_wt),
            },
            "background_constants_runtime_load_count": name_loads,
        },
        "evidence_columns": {
            "stale_header_comment": {
                "claim": "7-gallery defaults and use_legacy_4transition",
                "status": "CONTRADICTED_BY_LATER_PRODUCTION_ASSIGNMENT",
                "source": source_ref(SOURCE_PATH, 3, 6, "comment-only release header"),
            },
            "production_assignment": {
                "claim": "fresh default is thermodynamic graphite-4 plus si_case fallback",
                "status": "STATIC_PRODUCTION_ROUTE",
                "source": source_ref(SOURCE_PATH, 1439, 1470,
                                     "corrective assignment and toggle implementation"),
            },
            "stale_class_docstring": {
                "claim": "constructor docstring says default graphite is 7-gallery",
                "status": "CONTRADICTED_BY_PRODUCTION_ASSIGNMENT_AND_RUNTIME",
                "source": source_ref(SOURCE_PATH, 1596, 1601,
                                     "class documentation, not executable default"),
            },
            "stale_alpha_comment": {
                "claim": "graphite 7-gallery comment says alpha is absent although every literal row carries alpha",
                "status": "CONTRADICTED_WITHIN_ADJACENT_SOURCE",
                "source": source_ref(SOURCE_PATH, 1394, 1406,
                                     "comment and seven literal rows must be read together"),
            },
            "divergent_7_7_pair_examples": {
                "claim": "one example pairs graphite skew7 with symmetric Si7 while the confirmed pair names Si skew7",
                "status": "EXPLICIT_ROUTE_REQUIRES_CALLER_CHOICE",
                "source": source_ref(SOURCE_PATH, 1396, 1420,
                                     "two distinct 7+7 source declarations"),
            },
            "test_mutation": {
                "claim": "v1024 gate forces use_skew7_default(False) after import",
                "status": "TEST_MUTATION_NOT_FRESH_PUBLIC_DEFAULT",
                "source": source_ref(TEST1024_PATH, 70, 79,
                                     "test-only global default restoration"),
            },
            "release_handover": {
                "claim": "7/7/14 is explicit seed/switch, not public default; 4 route retains temperature dependence",
                "status": "DOCUMENTED_CORRECTION",
                "source": source_ref(HANDOVER_PATH, 12, 75,
                                     "release handover correction and temperature table"),
            },
            "archive_history": {
                "claim": "U10 default reversal was later withdrawn by U12",
                "status": "HISTORICAL_SUPERSESSION",
                "source": source_ref(ARCHIVE_PATH, 253, 364,
                                     "archive chronology, not production authority"),
            },
            "fitting_guide": {
                "claim": "w-only is not a multi-temperature profile; n/dH/dS inputs are required",
                "status": "STATIC_GUIDANCE",
                "source": source_ref(GUIDE_PATH, 29, 49,
                                     "temperature-fitting guidance"),
            },
        },
    }


PROBE_SOURCE = r'''
from __future__ import annotations
import hashlib, importlib.util, json, pathlib, sys, warnings
import numpy as np
warnings.filterwarnings('ignore')

def load(path):
    spec=importlib.util.spec_from_file_location('af_step80',path)
    if spec is None or spec.loader is None: raise RuntimeError('loader unavailable')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(a):
    x=np.asarray(a,dtype='<f8')
    return hashlib.sha256(x.tobytes(order='C')).hexdigest()
def stats(a):
    x=np.asarray(a,dtype=float)
    return {'size':int(x.size),'min':float(np.min(x)),'max':float(np.max(x)),
            'sum':float(np.sum(x)),'sha256_f64le':digest(x),'finite':bool(np.all(np.isfinite(x)))}
def maxdiff(a,b): return float(np.max(np.abs(np.asarray(a,dtype=float)-np.asarray(b,dtype=float))))

source=pathlib.Path(sys.argv[1]); mode=sys.argv[2]; route=sys.argv[3]
serialized_dir=pathlib.Path(sys.argv[4])
m=load(source)
V=np.linspace(0.03,0.70,1401); TL=288.15; TH=308.15

def public_model(route):
    kw={'f_Si':0.2,'si_case':'sic','Cbg':0.0}
    meta={'route_kind':'PUBLIC_BLEND','serialized_kernel':None,'serialized_compatibility':'NOT_APPLICABLE'}
    if route=='fresh_default_4_2':
        model=m.BlendedAnodeDQDV(**kw); declared=['DEFAULT_GRAPHITE_TRANSITIONS','SI_CASE_SETS[sic]']
    elif route=='explicit_legacy_4_2':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_LIT,
                                 si_transitions=m.SIC_LIT,**kw); declared=['GRAPHITE_STAGING_LIT','SIC_LIT']
    elif route=='from_wt_sic_4_2':
        model=m.BlendedAnodeDQDV.from_wt(0.05,si_case='sic',Cbg=0.0); declared=['from_wt','DEFAULT_GRAPHITE_TRANSITIONS','SI_CASE_SETS[sic]']
    elif route=='toggle_skew_7_7':
        m.use_skew7_default(True)
        model=m.BlendedAnodeDQDV(**kw); declared=['use_skew7_default(True)','DEFAULT_GRAPHITE_TRANSITIONS','DEFAULT_SI_TRANSITIONS']
    elif route=='explicit_skew_7_7':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_MSMR7_LIT,
                                 si_transitions=m.SI_MSMR7_SKEW_LIT,**kw); declared=['GRAPHITE_MSMR7_LIT','SI_MSMR7_SKEW_LIT']
    elif route=='explicit_xrd_5_2':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_XRD_v1024,
                                 si_transitions=m.SIC_LIT,**kw); declared=['GRAPHITE_STAGING_XRD_v1024','SIC_LIT']
    elif route=='explicit_msmr6_6_2':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_MSMR6_LIT,
                                 si_transitions=m.SIC_LIT,**kw); declared=['GRAPHITE_STAGING_MSMR6_LIT','SIC_LIT']
    elif route=='explicit_legacy_4_si7':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_LIT,
                                 si_transitions=m.SI_MSMR7_LIT,**kw); declared=['GRAPHITE_STAGING_LIT','SI_MSMR7_LIT']
    elif route=='explicit_skew7_symmetric7':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_MSMR7_LIT,
                                 si_transitions=m.SI_MSMR7_LIT,**kw); declared=['GRAPHITE_MSMR7_LIT','SI_MSMR7_LIT']
    elif route=='explicit_legacy_4_elemental2':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_LIT,
                                 si_transitions=m.SI_ELEMENTAL_LIT,**kw); declared=['GRAPHITE_STAGING_LIT','SI_ELEMENTAL_LIT']
    elif route=='explicit_legacy_4_siox1':
        model=m.BlendedAnodeDQDV(graphite_transitions=m.GRAPHITE_STAGING_LIT,
                                 si_transitions=m.SIOX_LIT,**kw); declared=['GRAPHITE_STAGING_LIT','SIOX_LIT']
    elif route=='lco3_electronic_off':
        model=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,Cbg=0.0,include_electronic_entropy=False)
        declared=['LCO_MSMR_LIT','include_electronic_entropy=False']; meta['route_kind']='PUBLIC_LCO'
    elif route=='lco3_electronic_on':
        model=m.LCOCathodeDQDV(m.LCO_MSMR_LIT,Cbg=0.0,include_electronic_entropy=True)
        declared=['LCO_MSMR_LIT','include_electronic_entropy=True']; meta['route_kind']='PUBLIC_LCO'
    else: raise KeyError(route)
    meta['declared_sources']=declared
    return model,meta

def build(route):
    if route.startswith('serialized_'):
        payload=json.loads((serialized_dir/(route+'.json')).read_text(encoding='utf-8'))
        trs=[dict(t) for t in payload['transitions']]
        model=m.GraphiteAnodeDischargeDQDV(trs,Cbg=payload['metrics']['bg'])
        return model,{'route_kind':'SERIALIZED_POOLED','declared_sources':[route+'.json'],
                      'serialized_kernel':payload['kernel'],
                      'serialized_compatibility':('CURRENT_PUBLIC_LOGISTIC_ONLY_KERNEL_METADATA_NOT_DISPATCHED'
                                                  if payload['kernel']=='regsol' else 'CURRENT_PUBLIC_ROUTE_EXECUTABLE')}
    return public_model(route)

def evaluate(route):
    model,meta=build(route)
    Vlocal=(np.linspace(3.65,4.25,1401) if route.startswith('lco3_') else V)
    blended=hasattr(model,'gr_host') and hasattr(model,'si_host')
    if blended:
        grn=len(model.gr_host.transitions); sin=len(model.si_host.transitions)
    else:
        grn=None; sin=None
    yl=np.asarray(model.equilibrium(Vlocal,TL),dtype=float)
    yh=np.asarray(model.equilibrium(Vlocal,TH),dtype=float)
    derivative=(yh-yl)/(TH-TL)
    curve_l=np.asarray(model.curve(Vlocal,direction='discharge',c_rate=0.2,Q_cell=1.0,T=TL),dtype=float)
    curve_h=np.asarray(model.curve(Vlocal,direction='discharge',c_rate=0.2,Q_cell=1.0,T=TH),dtype=float)
    u_l=float(model.solve_U_oc(0.25,TL)); u_h=float(model.solve_U_oc(0.25,TH))
    temp_delta=maxdiff(yl,yh); curve_delta=maxdiff(curve_l,curve_h)
    out={'route_id':route,**meta,
         'profile':{'graphite_count':grn,'silicon_count':sin,
                    'total_count':len(model.transitions),
                    'f_Si':(float(model.f_Si) if blended else None),
                    'Cbg':(float(model.Cbg) if not callable(model.Cbg) else 'CALLABLE')},
         'temperature':{'temperatures_K':[TL,TH],'equilibrium_low':stats(yl),'equilibrium_high':stats(yh),
                        'equilibrium_max_abs_delta':temp_delta,
                        'finite_difference_derivative':stats(derivative),
                        'curve_low':stats(curve_l),'curve_high':stats(curve_h),
                        'curve_max_abs_delta':curve_delta,
                        'temperature_dependent_observed':bool(max(temp_delta,curve_delta)>1e-12),
                        'U_oc_x025_V':[u_l,u_h],'U_oc_delta_V':u_h-u_l},
         'analytic_temperature_coefficient':{'status':'NOT_APPLICABLE'},
         'contributions':{'status':'NOT_APPLICABLE'},
         'limits':{'f_Si_zero_bit_exact':None,'status':'NOT_APPLICABLE'}}
    if not blended and not route.startswith('serialized_'):
        out['analytic_temperature_coefficient']={'status':'OBSERVED',
            'low':stats(model.entropy_coefficient(Vlocal,TL)),
            'high':stats(model.entropy_coefficient(Vlocal,TH))}
    if blended:
        gl,sl=model.host_contributions(Vlocal,TL); gh,sh=model.host_contributions(Vlocal,TH)
        zero=m.BlendedAnodeDQDV(0.0,graphite_transitions=model.gr_host.transitions,
                                si_transitions=model.si_host.transitions,Cbg=model.Cbg)
        z=np.asarray(zero.equilibrium(Vlocal,TL),dtype=float)
        g=np.asarray(zero.gr_host.equilibrium(Vlocal,TL),dtype=float)
        gr_tc=np.asarray(model.gr_host.entropy_coefficient(Vlocal,TL),dtype=float)
        si_tc=np.asarray(model.si_host.entropy_coefficient(Vlocal,TL),dtype=float)
        out['analytic_temperature_coefficient']={'status':'HOSTS_OBSERVED_NO_BLEND_PUBLIC_DELEGATE',
                                                  'graphite_low':stats(gr_tc),'silicon_low':stats(si_tc)}
        out['contributions']={'status':'OBSERVED','graphite_low':stats(gl),'graphite_high':stats(gh),
                              'graphite_max_abs_delta':maxdiff(gl,gh),'silicon_low':stats(sl),
                              'silicon_high':stats(sh),'silicon_max_abs_delta':maxdiff(sl,sh)}
        out['limits']={'status':'OBSERVED','f_Si_zero_bit_exact':bool(np.array_equal(z,g)),
                       'f_Si_zero_max_abs_delta':maxdiff(z,g)}
    out['observation_sha256']=hashlib.sha256(canon(out).encode()).hexdigest()
    return out

def snapshot(label):
    x=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    y=x.equilibrium(V,298.15)
    return {'label':label,'counts':[len(x.gr_host.transitions),len(x.si_host.transitions)],'sha256_f64le':digest(y)}

if mode=='route':
    print(canon(evaluate(route)))
elif mode=='order':
    events=[snapshot('fresh_default_before_any_mutation')]
    if route=='permutation_a':
        m.use_skew7_default(True); events.append(snapshot('toggle_true'))
        explicit,_=public_model('explicit_legacy_4_2'); events.append({'label':'explicit_legacy_while_toggled','counts':[len(explicit.gr_host.transitions),len(explicit.si_host.transitions)],'sha256_f64le':digest(explicit.equilibrium(V,298.15))})
        m.use_skew7_default(False); events.append(snapshot('restored_false'))
    elif route=='permutation_b':
        explicit,_=public_model('explicit_skew_7_7'); events.append({'label':'explicit_skew_before_toggle','counts':[len(explicit.gr_host.transitions),len(explicit.si_host.transitions)],'sha256_f64le':digest(explicit.equilibrium(V,298.15))})
        m.use_skew7_default(True); events.append(snapshot('toggle_true'))
        m.use_skew7_default(False); events.append(snapshot('restored_false'))
    else: raise KeyError(route)
    out={'permutation':route,'events':events,'fresh_first':events[0]['label']=='fresh_default_before_any_mutation',
         'restored_equals_fresh':events[-1]['counts']==events[0]['counts'] and events[-1]['sha256_f64le']==events[0]['sha256_f64le']}
    out['observation_sha256']=hashlib.sha256(canon(out).encode()).hexdigest()
    print(canon(out))
else: raise KeyError(mode)
'''


def parse_stdout(cp: subprocess.CompletedProcess[bytes]) -> dict[str, Any]:
    if cp.returncode != 0:
        raise RuntimeError("runtime probe failed")
    text = cp.stdout.decode("utf-8", "strict")
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"runtime probe must emit one JSON line; got {len(lines)}")
    return json.loads(lines[0])


def run_attestation() -> dict[str, Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="p066_step80_"))
    if temp_root == ROOT.resolve() or ROOT.resolve() in temp_root.parents:
        raise RuntimeError("temporary root escaped isolation policy")
    runs: list[dict[str, Any]] = []
    try:
        source = temp_root / "Anode_Fit_v1.0.24.py"
        source.write_bytes(git_bytes(SOURCE_PATH))
        probe = temp_root / "probe_step80.py"
        probe.write_text(PROBE_SOURCE, encoding="utf-8", newline="\n")
        serialized = temp_root / "serialized"
        serialized.mkdir()
        for route_id, path in SERIALIZED_PATHS.items():
            (serialized / f"{route_id}.json").write_bytes(git_bytes(path))
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8",
               "PYTHONDONTWRITEBYTECODE": "1"}
        for version, launcher in PYTHON_LAUNCHERS:
            for route_id in ROUTE_IDS:
                argv = (*launcher, "-B", "-I", "-X", "utf8", str(probe),
                        str(source), "route", route_id, str(serialized))
                cp = run_runtime(argv, cwd=temp_root, env=env)
                parsed = parse_stdout(cp)
                runs.append({
                    "python": version, "mode": "route", "route_id": route_id,
                    "argv": ["<PYTHON>", "-B", "-I", "-X", "utf8",
                             "<PROBE>", "<SOURCE>", "route", route_id, "<SERIALIZED_DIR>"],
                    "cwd": "<DISPOSABLE_ROOT>", "exit_code": cp.returncode,
                    "stdout_utf8": cp.stdout.decode("utf-8", "strict"),
                    "stderr_utf8": cp.stderr.decode("utf-8", "strict"),
                    "stdout_sha256": sha256(cp.stdout), "stderr_sha256": sha256(cp.stderr),
                    "observation": parsed,
                })
            for permutation in ("permutation_a", "permutation_b"):
                argv = (*launcher, "-B", "-I", "-X", "utf8", str(probe),
                        str(source), "order", permutation, str(serialized))
                cp = run_runtime(argv, cwd=temp_root, env=env)
                parsed = parse_stdout(cp)
                runs.append({
                    "python": version, "mode": "order", "route_id": permutation,
                    "argv": ["<PYTHON>", "-B", "-I", "-X", "utf8",
                             "<PROBE>", "<SOURCE>", "order", permutation, "<SERIALIZED_DIR>"],
                    "cwd": "<DISPOSABLE_ROOT>", "exit_code": cp.returncode,
                    "stdout_utf8": cp.stdout.decode("utf-8", "strict"),
                    "stderr_utf8": cp.stderr.decode("utf-8", "strict"),
                    "stdout_sha256": sha256(cp.stdout), "stderr_sha256": sha256(cp.stderr),
                    "observation": parsed,
                })
    finally:
        shutil.rmtree(temp_root)
    cleanup = not temp_root.exists()
    if not cleanup:
        raise RuntimeError("disposable runtime root cleanup failed")

    route_runs = [run for run in runs if run["mode"] == "route"]
    order_runs = [run for run in runs if run["mode"] == "order"]
    by_route: dict[str, list[dict[str, Any]]] = {}
    for run in route_runs:
        by_route.setdefault(run["route_id"], []).append(run["observation"])
    agreement = {}
    for route_id, observations in by_route.items():
        if len(observations) != 2:
            raise RuntimeError(f"missing runtime pair for {route_id}")
        a, b = observations
        numeric = (
            abs(a["temperature"]["equilibrium_max_abs_delta"] - b["temperature"]["equilibrium_max_abs_delta"]) <= 1e-12
            and abs(a["temperature"]["curve_max_abs_delta"] - b["temperature"]["curve_max_abs_delta"]) <= 1e-12
            and abs(a["temperature"]["U_oc_delta_V"] - b["temperature"]["U_oc_delta_V"]) <= 1e-12
        )
        agreement[route_id] = {
            "profile_counts_equal": a["profile"] == b["profile"],
            "temperature_class_equal": (a["temperature"]["temperature_dependent_observed"]
                                        == b["temperature"]["temperature_dependent_observed"]),
            "numeric_summary_within_1e_12": numeric,
            "observation_sha256_equal": a["observation_sha256"] == b["observation_sha256"],
        }

    return finalize({
        "schema": "phase066.step080.runtime-attestation.v1",
        "baseline": BASELINE,
        "source": input_binding(SOURCE_PATH),
        "probe_sha256": sha256(PROBE_SOURCE.encode("utf-8")),
        "process_contract": {
            "fresh_process_per_route": True,
            "fresh_import_before_any_mutation": True,
            "python_versions": ["3.12", "3.14"],
            "isolated_flags": ["-B", "-I", "-X", "utf8"],
            "working_tree_claude_imported": False,
            "disposable_root_cleanup_completed": cleanup,
        },
        "runs": runs,
        "cross_runtime_agreement": agreement,
        "aggregate": {
            "route_runs": len(route_runs), "order_runs": len(order_runs),
            "successful_processes": sum(run["exit_code"] == 0 for run in runs),
            "stderr_empty": sum(run["stderr_utf8"] == "" for run in runs),
            "temperature_dependent_routes": sorted({
                run["route_id"] for run in route_runs
                if run["observation"]["temperature"]["temperature_dependent_observed"]
            }),
            "temperature_independent_routes": sorted({
                run["route_id"] for run in route_runs
                if not run["observation"]["temperature"]["temperature_dependent_observed"]
            }),
            "order_restoration_pass": all(
                run["observation"]["fresh_first"] and run["observation"]["restored_equals_fresh"]
                for run in order_runs
            ),
        },
        "authority_ceiling": {
            "runtime_agreement_is_external_material_validation": False,
            "temperature_response_is_multi_temperature_experimental_validation": False,
            "profile_execution_is_profile_selection_authority": False,
            "serialized_metric_is_current_kernel_equivalence": False,
        },
    })


def build_matrix(runtime: dict[str, Any]) -> dict[str, Any]:
    static = static_analysis()
    first_runtime = {
        run["route_id"]: run["observation"] for run in runtime["runs"]
        if run["mode"] == "route" and run["python"] == "3.12"
    }
    rows = []
    categories = {
        "fresh_default_4_2": "FRESH_PUBLIC_DEFAULT",
        "explicit_legacy_4_2": "EXPLICIT_PRODUCTION_LITERAL",
        "from_wt_sic_4_2": "PUBLIC_ALIAS_FROM_WT",
        "toggle_skew_7_7": "GLOBAL_TOGGLE",
        "explicit_skew_7_7": "EXPLICIT_PRODUCTION_LITERAL",
        "explicit_xrd_5_2": "EXPLICIT_ALTERNATIVE_LITERAL",
        "explicit_msmr6_6_2": "EXPLICIT_ALTERNATIVE_LITERAL",
        "explicit_legacy_4_si7": "EXPLICIT_ALTERNATIVE_LITERAL",
        "explicit_skew7_symmetric7": "DIVERGENT_SOURCE_EXAMPLE",
        "explicit_legacy_4_elemental2": "EXPLICIT_FALLBACK_CASE",
        "explicit_legacy_4_siox1": "EXPLICIT_FALLBACK_CASE",
        "lco3_electronic_off": "PUBLIC_LCO_TOGGLE",
        "lco3_electronic_on": "PUBLIC_LCO_TOGGLE",
        "serialized_regsol_8": "SERIALIZED_HISTORICAL_PROFILE",
        "serialized_gallery_14": "SERIALIZED_HISTORICAL_PROFILE",
        "serialized_skew_14": "SERIALIZED_HISTORICAL_PROFILE",
    }
    for route_id in ROUTE_IDS:
        obs = first_runtime[route_id]
        rows.append({
            "id": f"R80-{len(rows)+1:02d}",
            "route_id": route_id,
            "route_class": categories[route_id],
            "profile": obs["profile"],
            "declared_sources": obs["declared_sources"],
            "serialized_kernel": obs["serialized_kernel"],
            "serialized_compatibility": obs["serialized_compatibility"],
            "temperature_dependent_observed": obs["temperature"]["temperature_dependent_observed"],
            "equilibrium_max_abs_delta": obs["temperature"]["equilibrium_max_abs_delta"],
            "curve_max_abs_delta": obs["temperature"]["curve_max_abs_delta"],
            "U_oc_delta_V": obs["temperature"]["U_oc_delta_V"],
            "contributions_status": obs["contributions"]["status"],
            "limit_status": obs["limits"]["status"],
            "f_Si_zero_bit_exact": obs["limits"]["f_Si_zero_bit_exact"],
            "runtime_cross_version": runtime["cross_runtime_agreement"][route_id],
            "internal_runtime_observed": True,
            "external_material_authority": False,
            "profile_selection_authority": False,
            "multi_temperature_experimental_authority": False,
            "owner": ("P067-CODE-HISTORY" if route_id == "serialized_regsol_8"
                      else "PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS"),
        })

    return finalize({
        "schema": "phase066.step080.profile-default-temperature-matrix.v1",
        "baseline": BASELINE,
        "inputs": [input_binding(path) for path in INPUT_PATHS],
        "source_coverage": {
            "production_python": "READ_FULL_LINES_1_2024",
            "test_gates_v1025": "READ_FULL_LINES_1_398",
            "test_gates_v1024": "READ_FULL_LINES_1_637_DELEGATED_PLUS_AST_CALL_PIN",
            "targeted_release_handover": "LINES_12_75",
            "targeted_archive_history": "LINES_253_364",
            "targeted_fitting_guide": "LINES_29_49",
            "serialized_profile_json": "THREE_FILES_FULL_STRICT_JSON",
        },
        **static,
        "route_rows": rows,
        "default_adjudication": {
            "fresh_public_default": "GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2",
            "fresh_public_default_temperature_dependent": first_runtime["fresh_default_4_2"]["temperature"]["temperature_dependent_observed"],
            "skew_7_7_status": "EXPLICIT_OR_TOGGLE_OPT_IN_ONLY",
            "skew_7_7_temperature_dependent": first_runtime["explicit_skew_7_7"]["temperature"]["temperature_dependent_observed"],
            "test_mutated_default_is_public_default": False,
            "stale_header_or_docstring_is_executable_default": False,
            "global_order_leakage_observed": not runtime["aggregate"]["order_restoration_pass"],
            "background_constants_auto_applied": False,
        },
        "negative_control_contract": [
            "fresh_import_after_test_mutation_rejected",
            "test_only_default_promoted_to_public_rejected",
            "omitted_profile_row_rejected",
            "temperature_independent_route_marked_dependent_rejected",
            "order_restoration_failure_rejected",
            "runtime_observation_promoted_to_external_authority_rejected",
            "serialized_regsol_marked_current_kernel_equivalent_rejected",
            "stale_comment_promoted_over_assignment_rejected",
            "probe_source_hash_mismatch_rejected",
            "runtime_argv_mutation_rejected",
            "runtime_unknown_field_rejected",
            "cross_runtime_observation_divergence_rejected",
            "matrix_runtime_field_fabrication_rejected",
        ],
        "aggregate": {
            "route_rows": len(rows),
            "public_and_explicit_routes": sum(not row["route_id"].startswith("serialized_") for row in rows),
            "serialized_routes": sum(row["route_id"].startswith("serialized_") for row in rows),
            "temperature_dependent": sum(row["temperature_dependent_observed"] for row in rows),
            "temperature_independent": sum(not row["temperature_dependent_observed"] for row in rows),
            "external_authority_true": sum(row["external_material_authority"] for row in rows),
            "profile_selection_authority_true": sum(row["profile_selection_authority"] for row in rows),
            "multi_temperature_experimental_authority_true": sum(row["multi_temperature_experimental_authority"] for row in rows),
        },
        "runtime_binding": {
            "path": f"Codex/results/{RUNTIME_NAME}",
            "semantic_sha256": runtime["semantic_sha256"],
            "processes": runtime["aggregate"]["route_runs"] + runtime["aggregate"]["order_runs"],
            "cleanup_completed": runtime["process_contract"]["disposable_root_cleanup_completed"],
        },
        "selected_gate": "PASS_P066_STEP80_PROFILE_DEFAULT_TEMPERATURE_VERIFICATION",
        "authority_ceiling": {
            "internal_static_and_runtime_behavior_verified": True,
            "external_scientific_authority": False,
            "material_phase_authority": False,
            "profile_selection_authority": False,
            "multi_temperature_experimental_authority": False,
        },
    })


def validate_persistence(expected_commit: str) -> None:
    if re.fullmatch(r"[0-9a-f]{40}", expected_commit) is None:
        raise SystemExit("expected commit must be exact lowercase 40-hex")
    head = run_git(("git", "rev-parse", "HEAD")).stdout.decode().strip()
    if head != expected_commit:
        raise SystemExit(f"HEAD mismatch: {head} != {expected_commit}")
    branch = run_git(("git", "branch", "--show-current")).stdout.decode().strip()
    if branch != BRANCH:
        raise SystemExit(f"branch mismatch: {branch}")
    parent = run_git(("git", "rev-parse", "HEAD^")).stdout.decode().strip()
    subject = run_git(("git", "show", "-s", "--format=%s", "HEAD")).stdout.decode().strip()
    changed = sorted(run_git(("git", "diff-tree", "--no-commit-id", "--name-only",
                              "-r", "HEAD")).stdout.decode().splitlines())
    if parent != EXPECTED_PARENT or subject != EXPECTED_SUBJECT or changed != sorted(EXACT_PATHS):
        raise SystemExit("persistence commit identity/path contract failed")
    upstream = run_git(("git", "rev-parse", "@{upstream}")).stdout.decode().strip()
    remote = run_git(("git", "ls-remote", "--heads", "origin", BRANCH)).stdout.decode().split()
    if upstream != head or len(remote) != 2 or remote[0] != head:
        raise SystemExit("upstream/live remote does not equal HEAD")
    if run_git(("git", "status", "--porcelain=v1")).stdout:
        raise SystemExit("worktree is not clean")
    print(f"PASS_P066_STEP80_PERSISTENCE commit={head}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.persistence:
        if args.output_dir is not None or args.expected_commit is None:
            raise SystemExit("persistence requires only --expected-commit")
        validate_persistence(args.expected_commit)
        return
    if args.expected_commit is not None:
        raise SystemExit("--expected-commit is persistence-only")
    runtime = run_attestation()
    matrix = build_matrix(runtime)
    if args.output_dir is None:
        guard_json_last()
        runtime_out, matrix_out = RUNTIME_OUT, MATRIX_OUT
    else:
        runtime_out, matrix_out = explicit_targets(args.output_dir)
    atomic_json(runtime_out, runtime)
    atomic_json(matrix_out, matrix)
    print("PASS_P066_STEP80_BUILD "
          f"routes={matrix['aggregate']['route_rows']} "
          f"processes={runtime['aggregate']['route_runs'] + runtime['aggregate']['order_runs']} "
          f"matrix_semantic={matrix['semantic_sha256']} "
          f"runtime_semantic={runtime['semantic_sha256']}")


if __name__ == "__main__":
    main()
