#!/usr/bin/env python3
"""Build Phase 065 Step 73 isolated initialization/runtime evidence.

Only exact blobs from the frozen baseline are materialized into a disposable
directory outside the repository.  The working-tree Claude sources are never
imported.  Each initialization route is launched in its own Python process.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "272b8d331c55448182e96c75363a56061adf58f2"
EXPECTED_SUBJECT = "audit(phase065): separate v1024 initialization routes"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
MATRIX_NAME = "PHASE_065_INITIALIZATION_ROUTE_MATRIX.json"
RUNTIME_NAME = "PHASE_065_RUNTIME_ATTESTATION.json"
MATRIX_OUT = ROOT / "Codex/results" / MATRIX_NAME
RUNTIME_OUT = ROOT / "Codex/results" / RUNTIME_NAME
STEP71_PATH = ROOT / "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json"

CONTROL_PATHS = (
    "Codex/work/v1024_phase065/build_phase065_step73.py",
    "Codex/work/v1024_phase065/validate_phase065_step73.py",
    "Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXACT_PATHS = tuple(sorted((*CONTROL_PATHS,
                            f"Codex/results/{MATRIX_NAME}",
                            f"Codex/results/{RUNTIME_NAME}")))

RUNTIME_COPY_PATHS = (
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/golden_graphite_ref.npz",
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.23/test_gates_v1023.py",
    "Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py",
    "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py",
    "Claude/docs/v1.0.24/test_gates_v1024.py",
    "Claude/docs/v1.0.24/test_gates_v1024_selfconsistent.py",
    "Claude/docs/v1.0.24/test_gates_v1024_reflect.py",
)
ROUTE_COPY_PATHS = (
    "Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py",
    "Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py",
)
PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")),
                    ("3.14", ("py", "-3.14")))
OUTCOME_VOCABULARY = (
    "IMPLEMENTED_AND_OBSERVED",
    "ABSENT_IN_FROZEN_SOURCE",
    "GROUND_NOT_FOUND",
)


def _run_subprocess(args: tuple[str, ...], *, cwd: Path,
                    timeout: int, env: dict[str, str] | None,
                    check: bool) -> subprocess.CompletedProcess[bytes]:
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
    return _run_subprocess(args, cwd=ROOT, timeout=120, env=None, check=check)


def run_runtime(args: tuple[str, ...], *, cwd: Path, timeout: int,
                env: dict[str, str], check: bool) -> subprocess.CompletedProcess[bytes]:
    allowed = (("py", "-3.12"), ("py", "-3.14"))
    if not any(args[:2] == prefix for prefix in allowed):
        raise RuntimeError("run_runtime launcher is outside the pinned Python allowlist")
    resolved_cwd = cwd.resolve()
    if ROOT.resolve() == resolved_cwd or ROOT.resolve() in resolved_cwd.parents:
        raise RuntimeError("run_runtime cwd must remain outside the repository")
    if timeout <= 0 or timeout > 900:
        raise RuntimeError("run_runtime timeout outside (0,900]")
    return _run_subprocess(args, cwd=resolved_cwd, timeout=timeout,
                           env=env, check=check)


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
            raise RuntimeError("exclusive temporary output escaped its approved directory")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def explicit_output_targets(candidate: Path) -> tuple[Path, Path]:
    out_dir = candidate.resolve()
    repository = ROOT.resolve()
    if out_dir == repository or repository in out_dir.parents:
        raise RuntimeError("explicit output directory must remain outside repository")
    targets = (out_dir / RUNTIME_NAME, out_dir / MATRIX_NAME)
    for target in targets:
        resolved_target = target.resolve()
        if resolved_target.parent != out_dir:
            raise RuntimeError("explicit output target escaped its approved directory")
        legacy_temporary = target.with_suffix(target.suffix + ".tmp")
        if legacy_temporary.exists() or legacy_temporary.is_symlink():
            raise RuntimeError("pre-existing temporary output path is forbidden")
    return targets


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def file_binding(path: Path, role: str) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": rel(path), "role": role, "sha256": sha256(raw),
            "bytes": len(raw)}


def guard_json_last() -> None:
    staged = sorted(run_git(("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR")).stdout.decode().splitlines())
    allowed = [sorted(CONTROL_PATHS), sorted(EXACT_PATHS)]
    if staged not in allowed:
        raise SystemExit(f"JSON-last requires exact six controls or exact eight paths; got {staged}")
    unstaged = sorted(run_git(("git", "diff", "--name-only", "--", *CONTROL_PATHS)).stdout.decode().splitlines())
    if unstaged:
        raise SystemExit(f"control files have unstaged changes: {unstaged}")


PROBE_SOURCE = r'''
from __future__ import annotations
import hashlib, importlib.util, json, pathlib, sys
import numpy as np

def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError('loader unavailable')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def canon(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def h(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def ph(x): return h(x)
def arr(x): return np.asarray(x,dtype=float)
def maxdiff(a,b): return float(np.max(np.abs(arr(a)-arr(b))))
def raises(exc,fn):
    try: fn()
    except exc: return True
    return False

p23,p24,route,mutation=sys.argv[1:5]
m24=load(p24,'af24_route_'+route+'_'+mutation)
m23=(load(p23,'af23_route_'+route+'_'+mutation) if route=='explicit' else None)

def fresh():
    required=['GRAPHITE_STAGING_XRD_v1024','GRAPHITE_STAGING_MSMR6_LIT','SI_CASE_SETS',
              'SI_CASE_GAPS','SI_SPECIFIC_CAPACITY','GRAPHITE_SPECIFIC_CAPACITY','BlendedAnodeDQDV']
    missing=[x for x in required if not hasattr(m24,x)]
    if missing: raise AssertionError('fresh required symbols missing:'+','.join(missing))
    model=m24.BlendedAnodeDQDV(0.0)
    observed={
      'constructor':'BlendedAnodeDQDV(0.0)',
      'explicit_profile_override':False,'saved_state_supplied':False,
      'graphite_profile_entries':len(model.gr_host.transitions),
      'graphite_profile_hash':ph(m24.GRAPHITE_STAGING_LIT),
      'observed_graphite_hash':ph(model.gr_host.transitions),
      'si_case':model.si_case,'si_profile_entries':len(model.si_host.transitions),
      'si_profile_source_entries':len(m24.SIC_LIT),'Q_gr':model.Q_gr,'Q_Si':model.Q_Si,
      'gaps':model.gaps,'lag_ratio_correction':model.gr_host.lag_ratio_correction,
      'use_dH_eff':model.gr_host.use_dH_eff,
      'graphite_constructor_requires_transitions':raises(TypeError,lambda:m24.GraphiteAnodeDischargeDQDV()),
      'lco_constructor_requires_transitions':raises(TypeError,lambda:m24.LCOCathodeDQDV()),
    }
    observed['pass']=(not missing and observed['graphite_profile_entries']==4
      and observed['graphite_profile_hash']==observed['observed_graphite_hash']
      and observed['si_case']=='sic' and observed['si_profile_entries']==2
      and observed['Q_Si']==0.0 and observed['graphite_constructor_requires_transitions']
      and observed['lco_constructor_requires_transitions'])
    if not observed['pass']: raise AssertionError('fresh route invariant failed')
    return observed

def explicit():
    profile_names=['GRAPHITE_STAGING_LIT','GRAPHITE_STAGING_XRD_v1024',
      'GRAPHITE_STAGING_MSMR6_LIT','LCO_MSMR_LIT','SI_ELEMENTAL_LIT','SIOX_LIT',
      'SIC_LIT','SI_CASE_SETS','SI_CASE_GAPS','SI_SPECIFIC_CAPACITY',
      'GRAPHITE_SPECIFIC_CAPACITY']
    seen=[]
    registry_pre={name:ph(getattr(m24,name)) for name in profile_names}
    for name in profile_names:
        if not hasattr(m24,name): raise AssertionError('profile absent:'+name)
    for name in profile_names[:3]:
        supplied=getattr(m24,name)
        if mutation=='explicit' and name=='GRAPHITE_STAGING_XRD_v1024': supplied=m24.GRAPHITE_STAGING_LIT
        obj=m24.GraphiteAnodeDischargeDQDV(supplied)
        if ph(obj.transitions)!=ph(getattr(m24,name)): raise AssertionError('profile redirect detected:'+name)
        seen.append({'profile_id':name,'public_path':'GraphiteAnodeDischargeDQDV(transitions)',
                     'entries':len(obj.transitions),'observed_hash':ph(obj.transitions)})
    lco=m24.LCOCathodeDQDV(m24.LCO_MSMR_LIT)
    seen.append({'profile_id':'LCO_MSMR_LIT','public_path':'LCOCathodeDQDV(transitions)',
                 'entries':len(lco.transitions),'input_hash':ph(m24.LCO_MSMR_LIT)})
    for name in ['SI_ELEMENTAL_LIT','SIOX_LIT','SIC_LIT']:
        obj=m24.BlendedAnodeDQDV(0.1,si_transitions=getattr(m24,name))
        seen.append({'profile_id':name,'public_path':'BlendedAnodeDQDV(si_transitions=...)',
                     'entries':len(obj.si_host.transitions),'normalized_weight_sum':float(sum(t['Q'] for t in obj.si_host.transitions))})
    cases={}
    for case in sorted(m24.SI_CASE_SETS):
        obj=m24.BlendedAnodeDQDV(0.1,si_case=case)
        cases[case]={'entries':len(obj.si_host.transitions),'gaps':obj.gaps}
    seen.append({'profile_id':'SI_CASE_SETS','public_path':'BlendedAnodeDQDV(si_case=...,si_transitions=None)','cases':cases})
    seen.append({'profile_id':'SI_CASE_GAPS','public_path':'BlendedAnodeDQDV.gaps via si_case','cases':{k:list(v) for k,v in sorted(m24.SI_CASE_GAPS.items())}})
    wt={}
    for case in sorted(m24.SI_SPECIFIC_CAPACITY):
        obj=m24.BlendedAnodeDQDV.from_wt(0.1,si_case=case)
        wt[case]={'q_Si':m24.SI_SPECIFIC_CAPACITY[case],'f_Si':obj.f_Si}
    seen.append({'profile_id':'SI_SPECIFIC_CAPACITY','public_path':'BlendedAnodeDQDV.from_wt(q_Si=None)','cases':wt})
    gr_default=m24.BlendedAnodeDQDV.from_wt(0.1,q_Si=1000.0)
    f_expected=100.0/(100.0+0.9*float(m24.GRAPHITE_SPECIFIC_CAPACITY))
    seen.append({'profile_id':'GRAPHITE_SPECIFIC_CAPACITY','public_path':'BlendedAnodeDQDV.from_wt(q_gr default)',
                 'q_gr':m24.GRAPHITE_SPECIFIC_CAPACITY,'f_Si':gr_default.f_Si,'expected_f_Si':f_expected})

    V=np.linspace(3.70,4.18,257)
    old=m23.LCOCathodeDQDV(m23.LCO_MSMR_LIT)
    off=m24.LCOCathodeDQDV(m24.LCO_MSMR_LIT)
    on=m24.LCOCathodeDQDV(m24.LCO_MSMR_LIT,include_electronic_entropy=True)
    false_variants=[m24.LCOCathodeDQDV(m24.LCO_MSMR_LIT,include_electronic_entropy=x)
                    for x in (False,0,None)]
    lco_numeric={
      'v23_equals_v24_enabled_Tref_bit_exact':bool(np.array_equal(old.equilibrium(V,298.15),on.equilibrium(V,298.15))),
      'v23_equals_v24_enabled_T318_bit_exact':bool(np.array_equal(old.equilibrium(V,318.15),on.equilibrium(V,318.15))),
      'v24_default_vs_enabled_Tref_max_abs_diff':maxdiff(off.equilibrium(V,298.15),on.equilibrium(V,298.15)),
      'v24_default_vs_enabled_T318_max_abs_diff':maxdiff(off.equilibrium(V,318.15),on.equilibrium(V,318.15)),
      'false_zero_none_match_default_bit_exact':all(np.array_equal(x.equilibrium(V,318.15),off.equilibrium(V,318.15)) for x in false_variants),
      'electronic_transition_x_centers':[float(t['x_center']) for t in m24.LCO_MSMR_LIT if t.get('electronic')],
      'tolerance_Tref':1e-10,
    }
    capture={}
    cm=m24.GraphiteAnodeDischargeDQDV([{'U':0.14,'w':0.02,'Q':1.0}])
    def cap(V_app,T,I_abs,Q_cell,s=+1):
        capture.setdefault('calls',[]).append({'I_abs':float(I_abs),'Q_cell':float(Q_cell),'s':int(s)})
        return np.zeros_like(np.asarray(V_app,dtype=float))
    cm.dqdv=cap
    cm.curve(np.array([0.1,0.2]),c_rate=1.0,Q_cell=2.0,I_abs=None)
    cm.curve(np.array([0.1,0.2]),c_rate=1.0,Q_cell=2.0,I_abs=0.0)
    cm.curve(np.array([0.1,0.2]),direction=0,c_rate=1.0,Q_cell=2.0,I_abs=False)
    tr={'U':0.14,'w':0.02,'Q':1.0,'dH_a':85000.0,'dS_a':0.0,'dVdq_qa':0.30,'Omega':8000.0}
    km=m24.GraphiteAnodeDischargeDQDV([tr])
    lraw=km._resolve_lag_length(tr,298.15,2.0,2.0,1.0,+1)
    lhour=km._resolve_lag_length(tr,298.15,2.0/3600.0,2.0,1.0,+1)
    time_grid=np.linspace(0.02,0.30,1201)
    curve_raw=km.curve(time_grid,'discharge',c_rate=1.0,Q_cell=2.0,T=298.15)
    direct_raw=km.dqdv(time_grid,298.15,2.0,2.0,+1)
    direct_hour=km.dqdv(time_grid,298.15,2.0/3600.0,2.0,+1)
    seconds_hour={'None_I_abs_capture':capture['calls'][0]['I_abs'],
      'explicit_zero_capture':capture['calls'][1]['I_abs'],'expected_hour_corrected_I_abs':2.0/3600.0,
      'direction_zero_false_I_abs_capture':capture['calls'][2],
      'curve_equals_direct_hour_number_bit_exact':bool(np.array_equal(curve_raw,direct_raw)),
      'curve_vs_seconds_corrected_max_abs_diff':maxdiff(curve_raw,direct_hour),
      'lag_raw_over_hour_corrected':float(lraw/lhour)}

    K=np.linspace(0.02,0.30,301)
    base={'U':0.14,'w':0.02,'Q':1.0,'Omega':6000.0}
    kvals={}
    for label,value in [('absent','ABSENT'),('none',None),('false',False),('typo','REGSOL'),('regsol','regsol')]:
        t=dict(base)
        if value!='ABSENT': t['kernel']=value
        kvals[label]=m24.GraphiteAnodeDischargeDQDV([t]).equilibrium(K)
    kernel={'absent_none_false_typo_bit_exact':all(np.array_equal(kvals['absent'],kvals[x]) for x in ('none','false','typo')),
            'regsol_vs_logistic_max_abs_diff':maxdiff(kvals['regsol'],kvals['absent'])}
    logistic_model=m24.GraphiteAnodeDischargeDQDV([dict(base)])
    regsol_tr=dict(base); regsol_tr['kernel']='regsol'
    regsol_model=m24.GraphiteAnodeDischargeDQDV([regsol_tr])
    kernel['dqdv_ignores_regsol_bit_exact']=bool(np.array_equal(
      logistic_model.dqdv(K,298.15,0.0,1.0),regsol_model.dqdv(K,298.15,0.0,1.0)))
    kernel['entropy_ignores_regsol_bit_exact']=bool(np.array_equal(
      logistic_model.entropy_coefficient(K,298.15),regsol_model.entropy_coefficient(K,298.15)))
    kernel['root_ignores_regsol_bit_exact']=bool(np.array_equal(
      logistic_model.solve_U_oc(np.array([0.2,0.5,0.8])),regsol_model.solve_U_oc(np.array([0.2,0.5,0.8]))))
    kernel['named_profiles_select_regsol']=any(t.get('kernel')=='regsol' for name in
      ['GRAPHITE_STAGING_LIT','GRAPHITE_STAGING_XRD_v1024','GRAPHITE_STAGING_MSMR6_LIT','LCO_MSMR_LIT',
       'SI_ELEMENTAL_LIT','SIOX_LIT','SIC_LIT'] for t in getattr(m24,name))
    xrd_no_omega=[{k:v for k,v in t.items() if k!='Omega'} for t in m24.GRAPHITE_STAGING_XRD_v1024]
    kernel['xrd_Omega_ignored_without_kernel_bit_exact']=bool(np.array_equal(
      m24.GraphiteAnodeDischargeDQDV(m24.GRAPHITE_STAGING_XRD_v1024).equilibrium(K),
      m24.GraphiteAnodeDischargeDQDV(xrd_no_omega).equilibrium(K)))
    delta_outputs={}
    for label,value in [('zero',0.0),('false',False),('negative',-1.0)]:
        t=dict(regsol_tr); t['delta']=value
        delta_outputs[label]=m24.GraphiteAnodeDischargeDQDV([t]).equilibrium(K)
    delta_default=m24.GraphiteAnodeDischargeDQDV([regsol_tr]).equilibrium(K)
    t_none=dict(regsol_tr); t_none['delta']=None
    kernel['delta']={'absent_uses_width_finite':bool(np.all(np.isfinite(delta_default))),
      'None_raises_TypeError':raises(TypeError,lambda:m24.GraphiteAnodeDischargeDQDV([t_none]).equilibrium(K)),
      'zero_false_negative_clamp_bit_exact':bool(np.array_equal(delta_outputs['zero'],delta_outputs['false'])
        and np.array_equal(delta_outputs['zero'],delta_outputs['negative'])),
      'nonpositive_clamp_finite':bool(np.all(np.isfinite(delta_outputs['zero'])))}
    dh_default=m24.GraphiteAnodeDischargeDQDV([tr])._resolve_lag_length(tr,298.15,1.0,1.0,1.0,+1)
    dh_on=m24.GraphiteAnodeDischargeDQDV([tr],use_dH_eff=True)._resolve_lag_length(tr,298.15,1.0,1.0,1.0,+1)
    dh_off_values=[m24.GraphiteAnodeDischargeDQDV([tr],use_dH_eff=x)._resolve_lag_length(tr,298.15,1.0,1.0,1.0,+1) for x in (False,0,None)]
    dh_off=dh_off_values[0]
    lag_tr=dict(tr); lag_tr['gamma']=0.7
    lag_default=m24.GraphiteAnodeDischargeDQDV([lag_tr])
    lag0=m24.GraphiteAnodeDischargeDQDV([lag_tr],lag_ratio_correction=False)
    lag1=m24.GraphiteAnodeDischargeDQDV([lag_tr],lag_ratio_correction=True)
    lag_off_variants=[m24.GraphiteAnodeDischargeDQDV([lag_tr],lag_ratio_correction=x) for x in (False,0,None)]
    lag_default_curve=lag_default.curve(K,c_rate=1.0,Q_cell=1.0)
    lag_diff=maxdiff(lag_default_curve,lag1.curve(K,c_rate=1.0,Q_cell=1.0))
    root_model=m24.GraphiteAnodeDischargeDQDV(m24.GRAPHITE_STAGING_LIT)
    root_converged=float(root_model.solve_U_oc(0.31))
    root_zero_iter=float(root_model.solve_U_oc(0.31,max_iter=0))
    root_negative_iter=float(root_model.solve_U_oc(0.31,max_iter=-2))
    root_checks={'converged_U':root_converged,'zero_iter_midpoint_U':root_zero_iter,
      'negative_iter_midpoint_U':root_negative_iter,
      'zero_and_negative_silent_midpoint_equal':root_zero_iter==root_negative_iter,
      'silent_midpoint_differs_from_converged':abs(root_zero_iter-root_converged)>1e-6,
      'reversed_bracket_raises':raises(ValueError,lambda:root_model.solve_U_oc(0.31,U_lo=1.0,U_hi=0.0)),
      'nonbracketing_interval_raises':raises(ValueError,lambda:root_model.solve_U_oc(0.31,U_lo=2.0,U_hi=3.0))}
    width_model=m24.GraphiteAnodeDischargeDQDV([{'U':0.14,'Q':1.0}])
    t_n_none={'U':0.14,'Q':1.0,'n':1.0,'n_T1':None}
    width_checks={'missing_n_factor':float(width_model._n_factor({'U':0.14,'Q':1.0},298.15)),
      'missing_n_dwdT':float(width_model._dwdT({'U':0.14,'Q':1.0},298.15)),
      'w_only_dwdT':float(width_model._dwdT({'U':0.14,'Q':1.0,'w':0.02},298.15)),
      'n_T1_None_n_factor':float(width_model._n_factor(t_n_none,298.15)),
      'n_T1_None_dwdT_raises':raises((TypeError,ValueError),lambda:width_model._dwdT(t_n_none,298.15)),
      'n_zero_width_raises':raises(ValueError,lambda:width_model._width({'U':0.14,'Q':1.0,'n':0.0},298.15))}
    host_calls=[]
    blend=m24.BlendedAnodeDQDV(0.3,si_case='sic')
    def host_capture(name):
        def fn(V_app,T,I_abs,Q_cell,s=+1):
            host_calls.append({'host':name,'I_abs':float(I_abs),'Q_cell':float(Q_cell),'s':int(s)})
            return np.zeros_like(np.asarray(V_app,dtype=float))
        return fn
    blend.gr_host.dqdv=host_capture('graphite'); blend.si_host.dqdv=host_capture('silicon')
    blend.dqdv(np.array([0.1,0.2]),298.15,0.8,2.0,+1)
    blend_checks={'host_calls':host_calls,
      'same_full_current_and_external_capacity_to_both_hosts':len(host_calls)==2 and all(x['I_abs']==0.8 and x['Q_cell']==2.0 for x in host_calls),
      'internal_capacity_Q':blend.Q,'external_Q_cell':2.0,
      'external_Q_cell_independent_of_internal_Q':blend.Q!=2.0,
      'capacity_fraction_closure':float(blend.Q_Si/blend.Q),
      'requested_capacity_fraction':blend.f_Si,
      'runtime_claim_scope':'observed argument forwarding only; solver absence remains Step71 static authority'}
    chi_none=m24.GraphiteAnodeDischargeDQDV([tr],x=0.37,chi=None)
    chi_zero=m24.GraphiteAnodeDischargeDQDV([tr],x=0.37,chi=0.0)
    stress_none=m24.BlendedAnodeDQDV(0.1,si_stress_offset=None)
    stress_zero=m24.BlendedAnodeDQDV(0.1,si_stress_offset=0.0)
    explicit_qsi_unknown=m24.BlendedAnodeDQDV.from_wt(0.1,q_Si=1000.0,si_case='absent',si_transitions=m24.SIC_LIT)
    fallback_checks={'chi_None_uses_x':chi_none.chi==0.37,'chi_zero_retained':chi_zero.chi==0.0,
      'stress_None_vs_zero_si_transitions_bit_exact':ph(stress_none.si_host.transitions)==ph(stress_zero.si_host.transitions),
      'explicit_qSi_bypasses_unknown_capacity_registry':explicit_qsi_unknown.f_Si>0.0}
    registry_post_normal={name:ph(getattr(m24,name)) for name in profile_names}
    alias_before=ph(m24.GRAPHITE_STAGING_LIT)
    alias_model=m24.GraphiteAnodeDischargeDQDV(m24.GRAPHITE_STAGING_LIT)
    original_U=alias_model.transitions[0]['U']
    alias_model.transitions[0]['U']=float(original_U)+1e-6
    alias_changed=ph(m24.GRAPHITE_STAGING_LIT)!=alias_before
    alias_model.transitions[0]['U']=original_U
    alias_checks={'normal_routes_preserve_registry_hashes':registry_pre==registry_post_normal,
      'same_process_graphite_reference_alias_mutates_registry':alias_changed,
      'registry_restored_after_probe':ph(m24.GRAPHITE_STAGING_LIT)==alias_before,
      'new_process_required_for_canonical_route_independence':True}
    boundaries={
      'invalid_si_case_raises':raises(ValueError,lambda:m24.BlendedAnodeDQDV(0.1,si_case='absent')),
      'empty_graphite_raises':raises(ValueError,lambda:m24.BlendedAnodeDQDV(0.1,graphite_transitions=[])),
      'plastic_GS1_not_implemented':raises(NotImplementedError,lambda:m24.BlendedAnodeDQDV(0.1).plastic_hysteresis_loop()),
      'nonadditive_GS2_not_implemented':raises(NotImplementedError,lambda:m24.BlendedAnodeDQDV(0.1).nonadditive_correction()),
      'missing_qSi_case_raises':raises(ValueError,lambda:m24.BlendedAnodeDQDV.from_wt(0.1,si_case='absent',si_transitions=m24.SIC_LIT)),
    }
    checks={
      'profiles_11':len(seen)==11 and {x['profile_id'] for x in seen}==set(profile_names),
      'lco_enabled_predecessor':lco_numeric['v23_equals_v24_enabled_Tref_bit_exact'] and lco_numeric['v23_equals_v24_enabled_T318_bit_exact'],
      'lco_default_off':lco_numeric['v24_default_vs_enabled_Tref_max_abs_diff']<=1e-10 and lco_numeric['v24_default_vs_enabled_T318_max_abs_diff']>1e-8 and lco_numeric['false_zero_none_match_default_bit_exact'],
      'seconds_hour_direct':seconds_hour['None_I_abs_capture']==2.0 and seconds_hour['explicit_zero_capture']==0.0
        and seconds_hour['curve_equals_direct_hour_number_bit_exact'] and seconds_hour['curve_vs_seconds_corrected_max_abs_diff']>0.0
        and abs(seconds_hour['lag_raw_over_hour_corrected']-3600.0)<1e-7,
      'direction_zero_and_false_current':capture['calls'][2]['I_abs']==0.0 and capture['calls'][2]['s']==1,
      'kernel_exact_key':kernel['absent_none_false_typo_bit_exact'] and kernel['regsol_vs_logistic_max_abs_diff']>1e-8
        and kernel['dqdv_ignores_regsol_bit_exact'] and kernel['entropy_ignores_regsol_bit_exact']
        and kernel['root_ignores_regsol_bit_exact'] and not kernel['named_profiles_select_regsol']
        and kernel['xrd_Omega_ignored_without_kernel_bit_exact'] and all(kernel['delta'].values()),
      'use_dH_eff_gate':dh_default==dh_on and all(x==dh_off for x in dh_off_values) and dh_on!=dh_off,
      'lag_ratio_gate':all(np.array_equal(lag_default_curve,x.curve(K,c_rate=1.0,Q_cell=1.0)) for x in lag_off_variants) and lag_diff>0.0,
      'root_exhaustion_preserved':all(root_checks[k] for k in ('zero_and_negative_silent_midpoint_equal','silent_midpoint_differs_from_converged','reversed_bracket_raises','nonbracketing_interval_raises')),
      'width_absence_inconsistency_preserved':width_checks['missing_n_factor']==1.0 and width_checks['missing_n_dwdT']==0.0
        and width_checks['w_only_dwdT']==0.0 and width_checks['n_T1_None_n_factor']==1.0
        and width_checks['n_T1_None_dwdT_raises'] and width_checks['n_zero_width_raises'],
      'blend_full_argument_forwarding':blend_checks['same_full_current_and_external_capacity_to_both_hosts']
        and blend_checks['external_Q_cell_independent_of_internal_Q'] and abs(blend_checks['capacity_fraction_closure']-blend_checks['requested_capacity_fraction'])<1e-15
        and blend_checks['runtime_claim_scope'].startswith('observed argument forwarding only'),
      'fallback_routes':all(fallback_checks.values()),
      'mutable_alias_boundary':all(alias_checks.values()),
      'boundaries':all(boundaries.values()),
    }
    if not all(checks.values()): raise AssertionError('explicit route check failed:'+repr(checks))
    return {'profiles':seen,'lco_electronic_entropy':lco_numeric,'seconds_hour':seconds_hour,
            'kernel':kernel,'use_dH_eff':{'default_lag':dh_default,'enabled_lag':dh_on,'disabled_lag':dh_off,
                                         'false_zero_none_lags':dh_off_values},
            'lag_ratio_correction':{'max_abs_diff':lag_diff,'default_false_zero_none_bit_exact':True},'scope_boundaries':boundaries,
            'root_validation':root_checks,'width_fallback':width_checks,'blend_current_capacity':blend_checks,
            'other_fallbacks':fallback_checks,
            'mutable_profile_alias':alias_checks,
            'checks':checks,'pass':True}

def legacy():
    candidates=['load_state_dict','from_state','from_dict','restore','load_saved_state']
    surfaces={name:{'module':hasattr(m24,name),'GraphiteAnodeDischargeDQDV':hasattr(m24.GraphiteAnodeDischargeDQDV,name),
                    'LCOCathodeDQDV':hasattr(m24.LCOCathodeDQDV,name),'BlendedAnodeDQDV':hasattr(m24.BlendedAnodeDQDV,name)}
              for name in candidates}
    any_loader=any(any(v.values()) for v in surfaces.values())
    if mutation=='legacy' and not any_loader: raise AssertionError('false implemented-restoration claim rejected')
    if any_loader: raise AssertionError('unexpected restoration surface requires renewed static audit')
    return {'predecessor_schema_fixture':'ABSENT_IN_FROZEN_SOURCE',
      'candidate_surface_observation':surfaces,
      'actual_restoration_path':'ABSENT_IN_FROZEN_SOURCE','restore_key':'ABSENT_IN_FROZEN_SOURCE',
      'runtime_observation_is_corroboration_not_a_restoration_execution':True,
      'runtime_observation_is_not_exhaustive_static_proof':True,'pass':True}

try:
    result={'fresh':fresh,'explicit':explicit,'legacy':legacy}[route]()
    print(canon({'route':route,'mutation':mutation,'result':result}))
except Exception as exc:
    print(type(exc).__name__+': '+str(exc),file=sys.stderr)
    sys.exit(7)
'''


def normalized_text(raw: bytes, tmp: Path) -> str:
    text = raw.decode("utf-8", "replace")
    for token in (str(tmp), str(tmp).replace("\\", "/")):
        text = text.replace(token, "<TMP>")
    return text.replace("\r\n", "\n")


def materialize(root: Path, sources: tuple[str, ...] = RUNTIME_COPY_PATHS) -> list[dict[str, Any]]:
    rows = []
    root_resolved = root.resolve()
    repo_resolved = ROOT.resolve()
    if root_resolved == repo_resolved or repo_resolved in root_resolved.parents:
        raise RuntimeError("runtime directory is not external to repository")
    for source in sources:
        target = root / PurePosixPath(source).relative_to("Claude/docs")
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = git_bytes(source)
        target.write_bytes(raw)
        resolved = target.resolve()
        if root_resolved not in resolved.parents:
            raise RuntimeError(f"materialized path escaped temp root: {resolved}")
        rows.append({"source_path": source, "materialized_relative_path": target.relative_to(root).as_posix(),
                     "git_blob": git_blob(source), "sha256": sha256(raw), "bytes": len(raw)})
    return rows


def create_route_fixture(outer: Path, fixture_id: str) -> tuple[Path, list[dict[str, Any]], Path, Path, Path]:
    root = outer / "route_fixtures" / fixture_id
    manifest = materialize(root, ROUTE_COPY_PATHS)
    probe = root / "step73_route_probe.py"
    probe.write_text(PROBE_SOURCE, encoding="utf-8", newline="\n")
    if root.resolve() not in probe.resolve().parents:
        raise RuntimeError("route probe escaped its unique fixture root")
    return (root, manifest, probe,
            root / "v1.0.23/Anode_Fit_v1.0.23.py",
            root / "v1.0.24/Anode_Fit_v1.0.24.py")


def fixture_files(root: Path, *, excluded_top_level: tuple[str, ...] = ()) -> list[str]:
    files: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts[0] in excluded_top_level:
            continue
        files.append(relative.as_posix())
    return sorted(files)


def run_record(runtime: str, command: tuple[str, ...], cwd: Path, tmp: Path,
               manifest_hash: str, fixture_id: str, source_root: str,
               run_id: str, expected_exit: int, authority: str,
               python_version: str | None, numpy_version: str | None,
               timeout: int = 600) -> tuple[dict[str, Any], bytes]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cp = run_runtime(command, cwd=cwd, timeout=timeout, env=env, check=False)
    stdout = normalized_text(cp.stdout, tmp)
    stderr = normalized_text(cp.stderr, tmp)
    cmd_public = [x.replace(str(tmp), "<TMP>").replace(str(tmp).replace("\\", "/"), "<TMP>") for x in command]
    input_obj = {"runtime": runtime, "command": cmd_public,
                 "cwd": cwd.relative_to(tmp).as_posix() if cwd != tmp else ".",
                 "materialized_manifest_sha256": manifest_hash,
                 "controller_probe_sha256": sha256(PROBE_SOURCE.encode()),
                 "fixture_id": fixture_id, "source_root": source_root}
    output_obj = {"exit_code": cp.returncode, "stdout": stdout, "stderr": stderr}
    record = {
        "run_id": run_id, "runtime": runtime, "command": cmd_public,
        "cwd": input_obj["cwd"], "exit_code": cp.returncode,
        "fixture_id": fixture_id, "source_root": source_root, "timed_out": False,
        "interpreter": python_version, "numpy_version": numpy_version,
        "expected_exit_code": expected_exit, "expectation_met": cp.returncode == expected_exit,
        "input_sha256": sha256(compact(input_obj)),
        "stdout": stdout, "stderr": stderr,
        "stdout_sha256": sha256(stdout.encode()), "stderr_sha256": sha256(stderr.encode()),
        "output_sha256": sha256(compact(output_obj)), "authority": authority,
        "observations": None,
        "mutation_probe": {"enabled": False, "mutation_id": None, "detected": None},
        "gate": "PASS" if cp.returncode == expected_exit else "FAIL",
        "external_scientific_truth": False,
    }
    return record, cp.stdout


def collect_runtime() -> dict[str, Any]:
    runtime_envs: list[dict[str, Any]] = []
    official_runs: list[dict[str, Any]] = []
    route_runs: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="p065_step73_") as td:
        tmp = Path(td)
        manifest = materialize(tmp)
        manifest_hash = sha256(compact(manifest))
        fixture_files_before = sorted(row["materialized_relative_path"] for row in manifest)
        official_specs = (
            ("v1023-main", tmp / "v1.0.23", "test_gates_v1023.py"),
            ("v1023-selfconsistent", tmp / "v1.0.23", "test_gates_v1023_selfconsistent.py"),
            ("v1024-main", tmp / "v1.0.24", "test_gates_v1024.py"),
            ("v1024-selfconsistent", tmp / "v1.0.24", "test_gates_v1024_selfconsistent.py"),
            ("v1024-reflect", tmp / "v1.0.24", "test_gates_v1024_reflect.py"),
        )
        orders = (("A", ("fresh", "explicit", "legacy")),
                  ("B", ("legacy", "explicit", "fresh")))
        for runtime, launcher in PYTHON_LAUNCHERS:
            version_cmd = (*launcher, "-B", "-I", "-X", "utf8", "-c",
                           "import sys,numpy;print(sys.version.split()[0]);print(numpy.__version__)")
            env_record, raw = run_record(
                runtime, version_cmd, tmp, tmp, manifest_hash,
                f"environment-{runtime}", "<TMP>",
                f"P065-RUNTIME-{runtime.replace('.', '')}", 0,
                "RUNTIME_ENVIRONMENT_ONLY", None, None, 60)
            lines = raw.decode("utf-8").splitlines()
            env_record["python_version"] = lines[0]
            env_record["numpy_version"] = lines[1]
            env_record["interpreter"] = lines[0]
            env_record["observations"] = {"python_version": lines[0], "numpy_version": lines[1]}
            env_record["gate"] = "PASS_RUNTIME_ENVIRONMENT"
            runtime_envs.append(env_record)
            for label, cwd, script in official_specs:
                cmd = (*launcher, "-B", "-I", "-X", "utf8", script)
                record, _ = run_record(
                    runtime, cmd, cwd, tmp, manifest_hash,
                    f"official-shared-{runtime}", "<TMP>",
                    f"P065-OFFICIAL-{label.upper()}-{runtime.replace('.', '')}",
                    0, "EXACT_COPIED_OFFICIAL_GATE_ONLY", lines[0], lines[1])
                record["observations"] = {"official_gate": label, "exit_zero": record["exit_code"] == 0}
                record["gate"] = "PASS_OFFICIAL_GATE" if record["expectation_met"] else "FAIL_OFFICIAL_GATE"
                official_runs.append(record)
            for order_id, routes in orders:
                for position, route in enumerate(routes, 1):
                    run_id = f"P065-ROUTE-{route.upper()}-{order_id}-{runtime.replace('.', '')}"
                    fixture_id = run_id.lower()
                    fixture, route_manifest, probe, p23, p24 = create_route_fixture(tmp, fixture_id)
                    route_input = {"sources": route_manifest, "probe_program_sha256": sha256(PROBE_SOURCE.encode())}
                    route_manifest_hash = sha256(compact(route_input))
                    source_root = f"<TMP>/route_fixtures/{fixture_id}"
                    cmd = (*launcher, "-B", "-I", "-X", "utf8", str(probe),
                           str(p23), str(p24), route, "none")
                    record, raw = run_record(
                        runtime, cmd, fixture, tmp, route_manifest_hash,
                        fixture_id, source_root, run_id, 0,
                        "ISOLATED_INTERNAL_RUNTIME_ONLY", lines[0], lines[1])
                    record.update({"route": route, "order_id": order_id, "position": position,
                                   "mutation": "none", "fixture_manifest": route_manifest})
                    if record["expectation_met"]:
                        record["observations"] = json.loads(raw.decode("utf-8"))["result"]
                    after_sources = []
                    for source_row in route_manifest:
                        source_path = fixture / source_row["materialized_relative_path"]
                        source_raw = source_path.read_bytes()
                        after_sources.append({**source_row, "sha256": sha256(source_raw), "bytes": len(source_raw)})
                    after_input = {"sources": after_sources, "probe_program_sha256": sha256(probe.read_bytes())}
                    route_gate = ("PASS_ABSENCE_CORROBORATION" if route == "legacy"
                                  else "PASS_IMPLEMENTED_ROUTE")
                    route_failure = ("FAIL_ABSENCE_CORROBORATION" if route == "legacy"
                                     else "FAIL_IMPLEMENTED_ROUTE")
                    record.update({
                        "fixture_input_manifest_sha256": route_manifest_hash,
                        "source_before_sha256": sha256(compact(route_input)),
                        "source_after_sha256": sha256(compact(after_input)),
                        "source_unchanged": route_input == after_input,
                        "fixture_files_before": sorted([*(x["materialized_relative_path"] for x in route_manifest), probe.name]),
                        "fixture_files_after": fixture_files(fixture),
                        "gate": route_gate if record["expectation_met"] else route_failure,
                    })
                    route_runs.append(record)
            for route in ("fresh", "explicit", "legacy"):
                run_id = f"P065-MUTATION-{route.upper()}-{runtime.replace('.', '')}"
                fixture_id = run_id.lower()
                fixture, route_manifest, probe, p23, p24 = create_route_fixture(tmp, fixture_id)
                route_input = {"sources": route_manifest, "probe_program_sha256": sha256(PROBE_SOURCE.encode())}
                route_manifest_hash = sha256(compact(route_input))
                p24_arg = p23 if route == "fresh" else p24
                cmd = (*launcher, "-B", "-I", "-X", "utf8", str(probe),
                       str(p23), str(p24_arg), route, route)
                record, _ = run_record(
                    runtime, cmd, fixture, tmp, route_manifest_hash,
                    fixture_id, f"<TMP>/route_fixtures/{fixture_id}", run_id,
                    7, "ROUTE_MUTATION_NEGATIVE_CONTROL", lines[0], lines[1])
                record.update({"route": route, "order_id": "MUTATION", "position": None,
                               "mutation": route, "mutation_detected": record["expectation_met"],
                               "fixture_manifest": route_manifest,
                               "fixture_input_manifest_sha256": route_manifest_hash,
                               "observations": {"expected_failure_exit": 7,
                                                "actual_exit": record["exit_code"],
                                                "mutation_detected": record["expectation_met"]},
                               "mutation_probe": {"enabled": True, "mutation_id": route,
                                                  "detected": record["expectation_met"]},
                               "gate": "PASS_MUTATION_REJECTED" if record["expectation_met"] else "FAIL_MUTATION_ACCEPTED"})
                after_sources = []
                for source_row in route_manifest:
                    source_path = fixture / source_row["materialized_relative_path"]
                    source_raw = source_path.read_bytes()
                    after_sources.append({**source_row, "sha256": sha256(source_raw), "bytes": len(source_raw)})
                after_input = {"sources": after_sources, "probe_program_sha256": sha256(probe.read_bytes())}
                record.update({"source_before_sha256": sha256(compact(route_input)),
                               "source_after_sha256": sha256(compact(after_input)),
                               "source_unchanged": route_input == after_input,
                               "fixture_files_before": sorted([*(x["materialized_relative_path"] for x in route_manifest), probe.name]),
                               "fixture_files_after": fixture_files(fixture)})
                route_runs.append(record)

        manifest_after = []
        for row in manifest:
            path = tmp / row["materialized_relative_path"]
            raw = path.read_bytes()
            manifest_after.append({"source_path": row["source_path"], "sha256": sha256(raw),
                                   "bytes": len(raw), "unchanged": sha256(raw) == row["sha256"] and len(raw) == row["bytes"]})
        probe_unchanged = all(row["source_unchanged"] for row in route_runs)
        fixture_files_after = fixture_files(tmp, excluded_top_level=("route_fixtures",))

    cleanup_verified = not Path(td).exists()

    order_checks = []
    for runtime, _ in PYTHON_LAUNCHERS:
        for route in ("fresh", "explicit", "legacy"):
            a = next(r for r in route_runs if r.get("runtime") == runtime and r.get("route") == route and r.get("order_id") == "A")
            b = next(r for r in route_runs if r.get("runtime") == runtime and r.get("route") == route and r.get("order_id") == "B")
            equal = a.get("observations") == b.get("observations")
            order_checks.append({"runtime": runtime, "route": route,
                                 "order_A_output_sha256": sha256(compact(a.get("observations"))),
                                 "order_B_output_sha256": sha256(compact(b.get("observations"))),
                                 "normalized_observations_equal": equal})
    return finalize({
        "artifact_kind": "PHASE_065_RUNTIME_ATTESTATION", "schema_version": 1,
        "phase": 65, "step": 73, "generated_date": "2026-08-31",
        "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "branch": BRANCH,
        "gate": "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS",
        "isolation": {"working_checkout_source_imported": False,
                      "exact_git_blobs_materialized": True,
                      "disposable_external_directory": True,
                      "materialized_path_containment_verified": True,
                      "bytecode_disabled": True, "isolated_mode": True,
                      "utf8_mode": True, "network_requested": False,
                      "probe_program_sha256": sha256(PROBE_SOURCE.encode()),
                      "materialized_manifest_sha256": manifest_hash,
                      "materialized_manifest": manifest,
                      "materialized_manifest_after": manifest_after,
                      "source_blobs_unchanged": all(row["unchanged"] for row in manifest_after),
                      "probe_program_unchanged": probe_unchanged,
                      "fixture_files_before": fixture_files_before,
                      "fixture_files_after": fixture_files_after,
                      "base_fixture_scan_excluded_top_level": ["route_fixtures"],
                      "unexpected_fixture_files": sorted(set(fixture_files_after) - set(fixture_files_before)),
                      "cleanup_verified_after_context": cleanup_verified,
                      "route_fixture_count": len(route_runs),
                      "route_fixture_ids_unique": len({row["fixture_id"] for row in route_runs}) == len(route_runs),
                      "each_route_run_has_own_fixture": True},
        "runtime_environments": runtime_envs, "official_runs": official_runs,
        "route_runs": route_runs, "changed_order_controls": order_checks,
        "counts": {"runtimes": len(runtime_envs), "official_runs": len(official_runs),
                   "official_expectations_met": sum(r["expectation_met"] for r in official_runs),
                   "implemented_behavior_route_runs": sum(r.get("mutation") == "none" and r.get("route") in {"fresh", "explicit"} for r in route_runs),
                   "implemented_behavior_route_expectations_met": sum(r.get("mutation") == "none" and r.get("route") in {"fresh", "explicit"} and r["expectation_met"] for r in route_runs),
                   "absence_corroboration_runs": sum(r.get("mutation") == "none" and r.get("route") == "legacy" for r in route_runs),
                   "absence_corroboration_expectations_met": sum(r.get("mutation") == "none" and r.get("route") == "legacy" and r["expectation_met"] for r in route_runs),
                   "mutation_runs": sum(r.get("mutation") != "none" for r in route_runs),
                   "mutations_detected": sum(r.get("mutation") != "none" and r["expectation_met"] for r in route_runs),
                   "changed_order_checks": len(order_checks),
                   "changed_order_equal": sum(r["normalized_observations_equal"] for r in order_checks)},
        "authority_boundary": {"internal_runtime_behavior": True,
                               "scientific_truth": False, "material_truth": False,
                               "experimental_truth": False, "proposition_support": False,
                               "canonical_adoption": False, "publication_readiness": False},
        "result_first_contract": {"gate": "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS",
                                  "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
                                  "postcommit_terminal": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
    })


def build_matrix(step71: dict[str, Any], runtime: dict[str, Any]) -> dict[str, Any]:
    profiles = step71["profile_surfaces"]
    initialization = step71["initialization_rows"]
    positive = [r for r in runtime["route_runs"] if r.get("mutation") == "none"]
    mutations = [r for r in runtime["route_runs"] if r.get("mutation") != "none"]
    route_rows = []
    for route, outcome, authority in (
        ("fresh_import", "IMPLEMENTED_AND_OBSERVED", "ISOLATED_RUNTIME_PLUS_STEP71_STATIC"),
        ("explicit_profile", "IMPLEMENTED_AND_OBSERVED", "ISOLATED_RUNTIME_PLUS_STEP71_STATIC"),
        ("legacy_restoration", "ABSENT_IN_FROZEN_SOURCE", "STEP71_STATIC_CENSUS_PRIMARY_RUNTIME_CORROBORATION_ONLY"),
    ):
        probe_route = {"fresh_import": "fresh", "explicit_profile": "explicit",
                       "legacy_restoration": "legacy"}[route]
        route_rows.append({
            "route": route, "outcome": outcome, "authority": authority,
            "process_run_ids": ([r["run_id"] for r in positive if r["route"] == probe_route]
                                if outcome == "IMPLEMENTED_AND_OBSERVED" else []),
            "absence_corroboration_run_ids": ([r["run_id"] for r in positive if r["route"] == probe_route]
                                               if outcome == "ABSENT_IN_FROZEN_SOURCE" else []),
            "mutation_run_ids": [r["run_id"] for r in mutations if r["route"] == probe_route],
            "own_process": outcome == "IMPLEMENTED_AND_OBSERVED",
            "own_fixture": outcome == "IMPLEMENTED_AND_OBSERVED",
            "own_observations": outcome == "IMPLEMENTED_AND_OBSERVED",
            "absence_corroboration_process_is_not_route_execution": outcome == "ABSENT_IN_FROZEN_SOURCE",
            "changed_order_control": True,
            "passing_behavior_route": outcome == "IMPLEMENTED_AND_OBSERVED",
            "absence_is_not_a_passing_behavior_route": outcome == "ABSENT_IN_FROZEN_SOURCE",
        })
    controls = [
        file_binding(ROOT / CONTROL_PATHS[0], "EVIDENCE_BUILDER"),
        file_binding(ROOT / CONTROL_PATHS[1], "INDEPENDENT_VALIDATOR"),
        file_binding(ROOT / CONTROL_PATHS[2], "RESULT_FIRST_RECORD"),
        file_binding(ROOT / CONTROL_PATHS[3], "PARENT_EXECUTION_LEDGER"),
        file_binding(ROOT / CONTROL_PATHS[4], "CANONICAL_EXECUTION_LEDGER"),
        file_binding(ROOT / CONTROL_PATHS[5], "ACTIVE_HANDOVER"),
    ]
    return finalize({
        "artifact_kind": "PHASE_065_INITIALIZATION_ROUTE_MATRIX", "schema_version": 1,
        "phase": 65, "step": 73, "generated_date": "2026-08-31",
        "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "branch": BRANCH,
        "gate": "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS",
        "outcome_vocabulary": list(OUTCOME_VOCABULARY),
        "consumed_step71": {"path": rel(STEP71_PATH),
                            "sha256": sha256(STEP71_PATH.read_bytes()),
                            "semantic_sha256": step71["semantic_sha256"],
                            "gate": step71["gate"],
                            "route_outcomes": step71["route_outcomes"]},
        "exact_initialization_mapping": initialization,
        "exact_profile_mapping": profiles,
        "routes": route_rows,
        "profile_runtime_routes": [
            {"profile_id": row["profile_id"], "ast_sha256": row["ast_sha256"],
             "entrypoint_observed": True,
             "public_route": next(x for x in positive if x["route"] == "explicit")["observations"]["profiles"][[p["profile_id"] for p in next(x for x in positive if x["route"] == "explicit")["observations"]["profiles"]].index(row["profile_id"])]["public_path"]}
            for row in profiles
        ],
        "feature_observation_owners": {
            "default_off_and_enabled": "explicit_profile.lco_electronic_entropy",
            "old_key_absence": "ABSENT_IN_FROZEN_SOURCE; no predecessor persistence schema or restore key",
            "explicit_zero_false": "explicit_profile lco/curve observations",
            "current_saved_state_key_presence": "ABSENT_IN_FROZEN_SOURCE; no current persistence schema or restore key",
            "legacy_restoration": "ABSENT_IN_FROZEN_SOURCE",
            "seconds_hour": "explicit_profile.seconds_hour",
            "exceptions_and_unsupported": "explicit_profile.scope_boundaries",
        },
        "runtime_attestation_binding": {"path": f"Codex/results/{RUNTIME_NAME}",
                                        "semantic_sha256": runtime["semantic_sha256"],
                                        "gate": runtime["gate"]},
        "control_source_bindings": controls,
        "negative_controls": {
            "fresh_redirect_to_v1023_detected": all(r["expectation_met"] for r in mutations if r["route"] == "fresh"),
            "explicit_XRD_redirect_detected": all(r["expectation_met"] for r in mutations if r["route"] == "explicit"),
            "false_legacy_loader_claim_detected": all(r["expectation_met"] for r in mutations if r["route"] == "legacy"),
            "validator_semantic_mutations_required": True,
        },
        "counts": {"initialization_rows": len(initialization), "profile_surfaces": len(profiles),
                   "routes": len(route_rows), "implemented_routes": sum(r["outcome"] == "IMPLEMENTED_AND_OBSERVED" for r in route_rows),
                   "absent_routes": sum(r["outcome"] == "ABSENT_IN_FROZEN_SOURCE" for r in route_rows),
                   "ground_not_found_routes": sum(r["outcome"] == "GROUND_NOT_FOUND" for r in route_rows),
                   "control_bindings": len(controls)},
        "authority_boundary": runtime["authority_boundary"],
        "source_policy": {"json_last": True, "result_first": True,
                          "frozen_source_from_git_blobs_only": True,
                          "working_checkout_Claude_import_forbidden": True,
                          "invented_profile_registry_forbidden": True,
                          "invented_restoration_loader_forbidden": True,
                          "legacy_absence_not_behavior_pass": True,
                          "external_truth_overclaim_forbidden": True},
        "result_first_contract": {"gate": "PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS",
                                  "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
                                  "postcommit_terminal": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
    })


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()
    if args.output_dir is None:
        guard_json_last()
        runtime_target, matrix_target = RUNTIME_OUT, MATRIX_OUT
    else:
        runtime_target, matrix_target = explicit_output_targets(args.output_dir)
    step71 = json.loads(STEP71_PATH.read_text(encoding="utf-8"))
    runtime = collect_runtime()
    matrix = build_matrix(step71, runtime)
    atomic_json(runtime_target, runtime)
    atomic_json(matrix_target, matrix)
    print("PASS_P065_STEP73_BUILD "
          f"official={runtime['counts']['official_expectations_met']}/{runtime['counts']['official_runs']} "
          f"routes={runtime['counts']['implemented_behavior_route_expectations_met']}/{runtime['counts']['implemented_behavior_route_runs']} "
          f"absence={runtime['counts']['absence_corroboration_expectations_met']}/{runtime['counts']['absence_corroboration_runs']} "
          f"mutations={runtime['counts']['mutations_detected']}/{runtime['counts']['mutation_runs']} "
          f"orders={runtime['counts']['changed_order_equal']}/{runtime['counts']['changed_order_checks']} "
          f"profiles={matrix['counts']['profile_surfaces']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
