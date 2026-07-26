# -*- coding: utf-8 -*-
"""v1.0.25 게이트 하네스 — C1 @2 skew(alpha)·C2 인과 pad·C3 SI(opt-in)·C7 Si 7-gallery.

★기존 게이트(test_gates_v1024·_reflect·_selfconsistent)와 별개·증축. 저들이 기본 경로의
  골든 bit-exact(G1 max|d|=0)·회귀·블렌드를 증빙하고, 본 파일은 v1.0.25 신규 opt-in 의
  '정확성'과 '부재 시 현행 동일'을 증빙한다(계획서 G0).

G-α1  alpha 부재 == 현행: (a) alpha=1.0 명시 == 부재 np.array_equal(equilibrium·dqdv 미해상/
      해상(pad)·entropy·solve_U_oc), (b) 부재 == v1.0.24.1 원본 모듈 np.array_equal.
G-α2  면적: α∈{0.25,0.5,1,2,4} 에서 |∫(dQ/dV)dV − Q|/Q ≤ 1e-6 (equilibrium skew peak).
G-α3  C¹: skew peak(α=2) 격자 반감 시 max|Δy′|/max|y| 비 ≈ 0.5 (kink 없음) — equilibrium 과
      dqdv(인과 pad 경로, L_V=0.02) 양쪽.
G-α4  축퇴 가드: 같은 전이에 alpha≠1 + L_V>0 동시 지정 → warnings.warn 발생(단독 지정은 무경고).
G-창  평가창 불변: 같은 물리점(전이 1개·L_V=0.02)이 V_app 시작점 3종에서 상대오차 ≤1%
      (원본 v1.0.24.1 은 시작점을 피크 안에 두면 ~100% — 참고 출력).
G-극단 L_V/w∈{0.1,1,3}×α∈{0.25,1,4}: 유한·비음·면적 보존(≤1e-4; 인과 적분+구적 오차 포함).
G-SI  C3 self-test: use_si_constants(True) 별도 모듈 인스턴스에서 RT/F 표시=25.693 mV·
      회귀 기준(−0.204/−0.134/−0.070 mV/K·+60.8 mV) 표시 정밀도 유지·U_oc 는 raw |Δ|≤5 µV
      (레거시 74.3511 mV 가 .1f 절벽 74.35 위 — SI −1.4 µV 이동이 display 만 74.4→74.3 로
      뒤집는 반올림 인공물이라 raw 로 게이트; doc worked-example 각주는 cascade 소관) +
      기본(미호출) 모듈은 레거시 R/F(8.314·96485.0) 그대로(골든 bit-exact 계약).
G-si7 C7: SI_MSMR7_LIT = 7 전이·0.433/0.456 V feature 포함·순수 로지스틱·유한·면적 보존 +
      기본 데이터셋(GRAPHITE_*·SI_*_LIT·LCO_MSMR_LIT) v1.0.24.1 과 동일(additive 증빙).

[재현] python test_gates_v1025.py   (../v1.0.24.1/Anode_Fit_v1.0.24.py 원본 필요 — G-α1(b)·G-창 참고)
"""
import sys, os, importlib.util, warnings
sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "Anode_Fit_v1.0.24.py")
CODE_PREV = os.path.normpath(os.path.join(HERE, "..", "v1.0.24.1", "Anode_Fit_v1.0.24.py"))
_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")

AREA_RTOL_EQ = 1e-6      # G-α2 equilibrium 면적 상대 공차(계획서)
AREA_RTOL_LAG = 1e-4     # G-극단 인과 경로 면적 공차(적분 절단+구적 오차 포함)
C1_RATIO_LO, C1_RATIO_HI = 0.40, 0.60   # G-α3 격자 반감 비(≈0.5; kink 면 ~1.0)
WIN_RTOL = 0.01          # G-창 시작점 3종 상대오차 ≤1%


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RESULTS = []


def record(name, ok):
    RESULTS.append((name, bool(ok)))
    print(f"  {name} RESULT: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)


# ---------------------------------------------------------------- G-α1
def gate_alpha1(m, mp):
    print("=" * 74)
    print("G-α1: alpha absent == status quo (np.array_equal, bit-exact)")
    V = np.linspace(0.03, 0.34, 1000)
    xg = np.linspace(0.05, 0.95, 91)
    kw = dict(x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    ok = True

    # (a) alpha=1.0 명시 == 부재 — 전 경로
    ma = m.GraphiteAnodeDischargeDQDV([dict(t) for t in m.GRAPHITE_STAGING_LIT], **kw)
    mb = m.GraphiteAnodeDischargeDQDV([dict(t, alpha=1.0) for t in m.GRAPHITE_STAGING_LIT], **kw)
    pairs = [
        ("equilibrium", ma.equilibrium(V, 298.15), mb.equilibrium(V, 298.15)),
        ("dqdv_dis_I0.2", ma.dqdv(V, 298.15, 0.2, 1.0, +1), mb.dqdv(V, 298.15, 0.2, 1.0, +1)),
        ("dqdv_chg_I1.0", ma.dqdv(V, 298.15, 1.0, 1.0, -1), mb.dqdv(V, 298.15, 1.0, 1.0, -1)),
        ("entropy_V", ma.entropy_coefficient(V, 298.15), mb.entropy_coefficient(V, 298.15)),
        ("solve_U_oc", ma.solve_U_oc(xg, 298.15), mb.solve_U_oc(xg, 298.15)),
    ]
    # 인과 pad 경로(해상 L_V)에서도 alpha=1.0 명시 == 부재
    trL = [{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'L_V': 0.02}]
    mc = m.GraphiteAnodeDischargeDQDV([dict(t) for t in trL], Cbg=0.0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        md = m.GraphiteAnodeDischargeDQDV([dict(t, alpha=1.0) for t in trL], Cbg=0.0)
    for s in (+1, -1):
        pairs.append((f"dqdv_lag_s{s:+d}",
                      mc.dqdv(V, 298.15, 0.5, 1.0, s), md.dqdv(V, 298.15, 0.5, 1.0, s)))
    for nm, a, b in pairs:
        eq = np.array_equal(np.asarray(a), np.asarray(b))
        ok &= eq
        print(f"  (a) alpha=1.0 == absent  {nm:16s} array_equal={eq}")

    # (b) 부재 == v1.0.24.1 원본 모듈(현행) — 기본 데이터셋(인과 미해상) 경로
    mo = mp.GraphiteAnodeDischargeDQDV([dict(t) for t in mp.GRAPHITE_STAGING_LIT], **kw)
    prev_pairs = [
        ("equilibrium", ma.equilibrium(V, 298.15), mo.equilibrium(V, 298.15)),
        ("dqdv_dis_I0.2", ma.dqdv(V, 298.15, 0.2, 1.0, +1), mo.dqdv(V, 298.15, 0.2, 1.0, +1)),
        ("dqdv_chg_I1.0", ma.dqdv(V, 298.15, 1.0, 1.0, -1), mo.dqdv(V, 298.15, 1.0, 1.0, -1)),
        ("entropy_V", ma.entropy_coefficient(V, 298.15), mo.entropy_coefficient(V, 298.15)),
        ("solve_U_oc", ma.solve_U_oc(xg, 298.15), mo.solve_U_oc(xg, 298.15)),
    ]
    for nm, a, b in prev_pairs:
        eq = np.array_equal(np.asarray(a), np.asarray(b))
        ok &= eq
        print(f"  (b) absent == v1.0.24.1  {nm:16s} array_equal={eq}")
    record("G-α1", ok)
    return ok


# ---------------------------------------------------------------- G-α2
def gate_alpha2(m):
    print("G-α2: area conservation |∫dQ/dV·dV − Q|/Q <= 1e-6 over alpha grid")
    U, w, Q = 0.15, 0.014, 0.7
    ok = True
    for a in (0.25, 0.5, 1.0, 2.0, 4.0):
        lo = U - 45.0 * w / min(a, 1.0)
        hi = U + 45.0 * w
        V = np.linspace(lo, hi, 400001)
        md = m.GraphiteAnodeDischargeDQDV([{'U': U, 'w': w, 'Q': Q, 'alpha': a}], Cbg=0.0)
        y = np.asarray(md.equilibrium(V, 298.15), dtype=float)
        rel = abs(float(_trapz(y, V)) - Q) / Q
        hit = rel <= AREA_RTOL_EQ
        ok &= hit
        print(f"  alpha={a:<5}: rel|area-Q|={rel:.3e} (<= {AREA_RTOL_EQ:.0e}) {'OK' if hit else 'FAIL'}")
    record("G-α2", ok)
    return ok


# ---------------------------------------------------------------- G-α3
def _deriv_jump_ratio(build_y, V1, V2):
    """격자 반감(V1→V2, 간격 ½) 시 max|Δy′|/max|y| 의 비 — C¹ 이면 ≈0.5, kink 면 ≈1."""
    out = []
    for V in (V1, V2):
        y = build_y(V)
        d = np.diff(y) / np.diff(V)
        out.append(float(np.max(np.abs(np.diff(d)))) / float(np.max(np.abs(y))))
    return out[1] / out[0]


def gate_alpha3(m):
    print("G-α3: C1 smoothness — grid halving ratio of max|Δy′|/max|y| ≈ 0.5 (α=2)")
    U, w = 0.15, 0.014
    V1 = np.linspace(0.0, 0.34, 2001)
    V2 = np.linspace(0.0, 0.34, 4001)
    mk = m.GraphiteAnodeDischargeDQDV([{'U': U, 'w': w, 'Q': 1.0, 'alpha': 2.0}], Cbg=0.0)
    r_eq = _deriv_jump_ratio(lambda V: np.asarray(mk.equilibrium(V, 298.15), dtype=float), V1, V2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml = m.GraphiteAnodeDischargeDQDV(
            [{'U': U, 'w': w, 'Q': 1.0, 'alpha': 2.0, 'L_V': 0.02}], Cbg=0.0)
    r_lag = _deriv_jump_ratio(
        lambda V: np.asarray(ml.dqdv(V, 298.15, 0.5, 1.0, +1), dtype=float), V1, V2)
    ok = (C1_RATIO_LO <= r_eq <= C1_RATIO_HI) and (C1_RATIO_LO <= r_lag <= C1_RATIO_HI)
    print(f"  equilibrium skew peak : ratio={r_eq:.3f} (in [{C1_RATIO_LO},{C1_RATIO_HI}])")
    print(f"  dqdv causal+pad (L_V=0.02): ratio={r_lag:.3f} (in [{C1_RATIO_LO},{C1_RATIO_HI}])")
    record("G-α3", ok)
    return ok


# ---------------------------------------------------------------- G-α4
def gate_alpha4(m):
    print("G-α4: degeneracy guard — warn iff alpha(≠1) and L_V(>0) both freed")
    def _warns(trs):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            m.GraphiteAnodeDischargeDQDV(trs, Cbg=0.0)
        return any("G-α4" in str(w_.message) or "alpha" in str(w_.message) for w_ in wl)
    both = _warns([{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'alpha': 2.0, 'L_V': 0.02}])
    only_a = _warns([{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'alpha': 2.0}])
    only_L = _warns([{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'L_V': 0.02}])
    a1_L = _warns([{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'alpha': 1.0, 'L_V': 0.02}])
    ok = both and (not only_a) and (not only_L) and (not a1_L)
    print(f"  alpha=2+L_V=0.02 -> warned: {both} (expect True)")
    print(f"  alpha only: {only_a} / L_V only: {only_L} / alpha=1+L_V: {a1_L} (expect all False)")
    record("G-α4", ok)
    return ok


# ---------------------------------------------------------------- G-창
def gate_window(m, mp):
    print("G-창: window invariance — same physical point, 3 V_app start points (rel <= 1%)")
    tr = [{'U': 0.15, 'w': 0.014, 'Q': 1.0, 'L_V': 0.02}]
    step, end, Vstar = 1e-4, 0.35, 0.21
    starts = [0.03, 0.145, 0.19]   # 피크 前·피크 안·피크 뒤(원본 최악 조건 포함)

    def evals(mod):
        mm = mod.GraphiteAnodeDischargeDQDV([dict(t) for t in tr], Cbg=0.0)
        vals = []
        for st in starts:
            n = int(round((end - st) / step)) + 1
            V = st + step * np.arange(n)
            y = np.asarray(mm.dqdv(V, 298.15, 0.5, 1.0, +1), dtype=float)
            vals.append(float(y[int(round((Vstar - st) / step))]))
        return vals

    v_new = evals(m)
    ref = v_new[0]
    spread_new = max(abs(v - ref) for v in v_new) / abs(ref)
    v_old = evals(mp)
    spread_old = max(abs(v - v_old[0]) for v in v_old) / abs(v_old[0])
    ok = spread_new <= WIN_RTOL
    print(f"  v1.0.25 (pad): values@V*={Vstar} = {[f'{v:.6f}' for v in v_new]}  "
          f"rel spread={spread_new:.2e} (<= {WIN_RTOL})")
    print(f"  [ref] v1.0.24.1 (no pad): {[f'{v:.6f}' for v in v_old]}  "
          f"rel spread={spread_old:.2%} (window-dependent — the defect being fixed)")
    record("G-창", ok)
    return ok


# ---------------------------------------------------------------- G-극단
def gate_extreme(m):
    print("G-극단: L_V/w ∈ {0.1,1,3} × alpha ∈ {0.25,1,4} — finite·non-neg·area")
    U, w, T = 0.15, 0.014, 298.15
    ok = True
    for ratio in (0.1, 1.0, 3.0):
        for a in (0.25, 1.0, 4.0):
            L = ratio * w
            lo = U - (45.0 * w / min(a, 1.0) + 5.0 * L)
            hi = U + 45.0 * w + 25.0 * L
            h = min(w / max(a, 1.0), L, w) / 60.0
            n = int((hi - lo) / h) + 1
            V = np.linspace(lo, hi, n)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")   # G-α4 축퇴 경고(의도된 스트레스 조합)
                md = m.GraphiteAnodeDischargeDQDV(
                    [{'U': U, 'w': w, 'Q': 1.0, 'alpha': a, 'L_V': L}], Cbg=0.0)
            y = np.asarray(md.dqdv(V, T, 0.5, 1.0, +1), dtype=float)
            fin = bool(np.all(np.isfinite(y)))
            nonneg = bool(np.min(y) >= -1e-12)
            rel = abs(float(_trapz(y, V)) - 1.0)
            hit = fin and nonneg and (rel <= AREA_RTOL_LAG)
            ok &= hit
            print(f"  L_V/w={ratio:<4} alpha={a:<5}: finite={fin} min={np.min(y):+.2e} "
                  f"rel|area-1|={rel:.2e} (<= {AREA_RTOL_LAG:.0e}) n={n} {'OK' if hit else 'FAIL'}")
    record("G-극단", ok)
    return ok


# ---------------------------------------------------------------- G-SI
def gate_si_constants(m):
    print("G-SI (C3): SI constants opt-in — regression displays hold; default stays legacy")
    ok = True
    # 기본(미호출) = 레거시 (골든 bit-exact 계약)
    leg = (m.R == 8.314) and (m.F == 96485.0)
    leg_disp = format(m.R * 298.15 / m.F * 1e3, ".3f")
    ok &= leg and (leg_disp == "25.691")
    print(f"  default module: R={m.R} F={m.F} RT/F@298.15={leg_disp} mV (doc-legacy 25.691) "
          f"{'OK' if leg else 'FAIL'}")
    # 별도 모듈 인스턴스에서 SI 발효
    m2 = load(CODE, "af_v1025_si")
    m2.use_si_constants(True)
    si_vals = (m2.R == m2.R_SI == 8.314462618) and (m2.F == m2.F_SI == 96485.33212)
    si_disp = format(m2.R * 298.15 / m2.F * 1e3, ".3f")
    hit = si_vals and (si_disp == "25.693")
    ok &= hit
    print(f"  SI module: R={m2.R} F={m2.F} RT/F@298.15={si_disp} mV (doc 25.693) "
          f"{'OK' if hit else 'FAIL'}")
    model = m2.GraphiteAnodeDischargeDQDV(
        m2.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    t = model.entropy_coefficient_x(0.25, 298.15, return_terms=True)
    q = model.reversible_heat_x(0.25, 298.15, I=1.0)
    rows = [("dU/dT complete [mV/K]", t['complete'] * 1e3, "+.3f", "-0.204"),
            ("dU/dT simple  [mV/K]", t['simple'] * 1e3, "+.3f", "-0.134"),
            ("dU/dT config  [mV/K]", t['config'] * 1e3, "+.3f", "-0.070"),
            ("Qrev/I [mV]", q * 1e3, "+.1f", "+60.8")]
    for label, val, fmt, want in rows:
        got = format(val, fmt)
        hit = (got == want)
        ok &= hit
        print(f"    SI regression {label:24s} display={got} doc={want} {'OK' if hit else 'FAIL'}")
    # U_oc: 레거시 raw 74.3511 mV 가 .1f 반올림 절벽(74.35) 위에 있어 display 동등성은 취약 —
    #   SI 이동은 −1.4 µV(표시양자 50 µV 의 3%)로 물리 불변이나 display 는 74.4→74.3 로 뒤집힌다
    #   (반올림 절벽 인공물). 게이트 = raw 일치 |Δ| ≤ 5 µV(표시 정밀도 內 물리 불변의 수치 증빙);
    #   worked-example 표시값 각주는 doc-cascade(계획서 C3 "어긋나면 표시값만 갱신") 소관.
    model_leg = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    u_leg = float(model_leg.solve_U_oc(0.25, 298.15)) * 1e3
    u_si = float(t['U_oc']) * 1e3
    hit = abs(u_si - u_leg) <= 5e-3
    ok &= hit
    print(f"    SI regression U_oc raw: legacy={u_leg:.4f} SI={u_si:.4f} mV  "
          f"|d|={abs(u_si-u_leg)*1e3:.2f} uV (<=5 uV; display {format(u_si,'.1f')} vs doc 74.4 = "
          f"rounding-cliff artifact) {'OK' if hit else 'FAIL'}")
    # 복귀 동작
    m2.use_si_constants(False)
    ok &= (m2.R == 8.314) and (m2.F == 96485.0)
    print(f"  toggle-back to legacy: R={m2.R} F={m2.F}")
    record("G-SI", ok)
    return ok


# ---------------------------------------------------------------- G-si7
def gate_si7(m, mp):
    print("G-si7 (C7): SI_MSMR7_LIT opt-in — 7 transitions, 0.433/0.456 features, additive")
    s7 = m.SI_MSMR7_LIT
    ok = (len(s7) == 7)
    has433 = any(abs(t['U'] - 0.433) < 1e-12 for t in s7)
    has456 = any(abs(t['U'] - 0.456) < 1e-12 for t in s7)
    logistic = all('kernel' not in t for t in s7)
    ok &= has433 and has456 and logistic
    print(f"  n_transitions={len(s7)}(=7)  0.433V={has433}  0.456V={has456}  pure-logistic={logistic}")
    md = m.GraphiteAnodeDischargeDQDV([dict(t) for t in s7], Cbg=0.0)
    V = np.linspace(-1.0, 1.6, 200001)
    y = np.asarray(md.equilibrium(V, 298.15), dtype=float)
    Qs = float(sum(t['Q'] for t in s7))
    rel = abs(float(_trapz(y, V)) - Qs) / Qs
    fin = bool(np.all(np.isfinite(y)) and np.min(y) >= -1e-12)
    hit = fin and rel <= AREA_RTOL_EQ
    ok &= hit
    print(f"  finite/non-neg={fin}  rel|area-Q|={rel:.2e} (<= {AREA_RTOL_EQ:.0e}) {'OK' if hit else 'FAIL'}")
    # additive: 기본 데이터셋 v1.0.24.1 과 동일 + 원본엔 SI_MSMR7_LIT 부재
    same = (m.GRAPHITE_STAGING_LIT == mp.GRAPHITE_STAGING_LIT
            and m.GRAPHITE_STAGING_MSMR6_LIT == mp.GRAPHITE_STAGING_MSMR6_LIT
            and m.GRAPHITE_STAGING_XRD_v1024 == mp.GRAPHITE_STAGING_XRD_v1024
            and m.SI_ELEMENTAL_LIT == mp.SI_ELEMENTAL_LIT
            and m.SIOX_LIT == mp.SIOX_LIT and m.SIC_LIT == mp.SIC_LIT
            and m.LCO_MSMR_LIT == mp.LCO_MSMR_LIT)
    new_only = not hasattr(mp, 'SI_MSMR7_LIT')
    ok &= same and new_only
    print(f"  default datasets identical to v1.0.24.1: {same}  (SI_MSMR7_LIT new-only: {new_only})")
    record("G-si7", ok)
    return ok


def gate_forbidden():
    """G-금지 (계획서 G0): 문건이 '쓰지 않는다·재도입 금지'로 선언한 표현이 본문에 되살아났는지 grep.

    각 항 = (선언 근거, 금지 정규식, 허용 예외 정규식 or None). 예외는 '금지를 설명하는 문장'
    (금지 자체를 서술하려면 그 표현을 인용해야 하므로) 을 통과시키기 위한 것이며, 예외에
    걸리지 않은 출현만 위반으로 센다.
    """
    print("=" * 74)
    print("G-금지: 문건 금지 표현 재도입 스캔 (계획서 C5/G0 — 선언 ↔ 본문 grep)")
    import re as _re
    sec = os.path.join(HERE, "_sections")
    files = sorted(f for f in os.listdir(sec) if f.endswith(".tex"))
    # (라벨, 금지 패턴, 같은 줄에 있으면 '금지를 서술하는 문장'으로 보고 면제할 패턴)
    RULES = [
        ("C5-a 두-상 델타로의 '연속화' 서술",
         r"이 한 식으로 연속화", None),
        ("C5-b w_eff 를 '유효 폭'으로 읽는 서술",
         # 어순 양방향(폭 표현이 w_eff 앞/뒤 어디에 와도 잡는다)
         r"(?:w_\\?\\?eff[^\n]{0,24}(?:유효\s*폭|반높이\s*폭|폭으로 읽)"
         r"|(?:유효\s*폭|반높이\s*폭)[^\n]{0,24}w_\\?\\?eff)",
         # 면제 = 그 오독을 '금지·정정·정량 대비'하는 문장. 3/2 는 λ^{3/2} 정정 서술의 지문.
         r"(금지|아니|말 것|않는다|안\s?된다|오독|주의|한정|과대|3/2|중심 \\emph\{높이\})"),
        ("C5-c w_eff(Ω) 축소식 재도입",
         r"w_\\eff\(\\?Omega\)|w_\\mathrm\{eff\}\(\\Omega\)",
         r"(금지|쓰지 않는다|한정|허용이다|별개)"),
        ("C6 regsol 커널을 채택 경로로 서술",
         r"kernel'?\s*[:=]\s*'?regsol|채택 커널.{0,12}Frumkin",
         r"(삭제|미채택|미구현|무시|아니)"),
    ]
    total = 0
    for lab, pat, exc in RULES:
        rx = _re.compile(pat)
        rxe = _re.compile(exc) if exc else None
        hits = []
        for fn in files:
            for i, line in enumerate(open(os.path.join(sec, fn), encoding="utf-8"), 1):
                if line.lstrip().startswith("%"):
                    continue                      # 주석(이력·자산 앵커)은 대상 아님
                if rx.search(line) and not (rxe and rxe.search(line)):
                    hits.append(f"{fn}:{i}")
        total += len(hits)
        print(f"  {lab}: 위반 {len(hits)}" + (f" -> {hits[:4]}" if hits else ""))
    ok = (total == 0)
    print(f"  G-금지 RESULT: {'PASS' if ok else 'FAIL'}  (총 위반 {total})")
    record("G-금지", ok)
    return ok


def main():
    print(f"v1.0.25: {CODE}\nv1.0.24.1(ref): {CODE_PREV}\n"
          f"numpy {np.__version__}, python {sys.version.split()[0]}")
    m = load(CODE, "af_v1025")
    mp = load(CODE_PREV, "af_v10241_ref")
    gate_alpha1(m, mp)
    gate_alpha2(m)
    gate_alpha3(m)
    gate_alpha4(m)
    gate_window(m, mp)
    gate_extreme(m)
    gate_si_constants(m)
    gate_si7(m, mp)
    gate_forbidden()
    npass = sum(1 for _, okv in RESULTS if okv)
    allok = (npass == len(RESULTS))
    for nm, okv in RESULTS:
        print(f">>> {nm}: {'PASS' if okv else 'FAIL'}")
    print(f">>> v1.0.25 GATES: {'ALL PASS' if allok else 'FAIL'} ({npass}/{len(RESULTS)})")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
