# -*- coding: utf-8 -*-
"""v1.0.24 하드 게이트 하네스 — G1·G2·G3 전건 수치 증빙 (doc-leads: 문건 v1.0.24 Ch1 부록(코드 요구명세) 요구명세).

[G1 하위호환] 신기능(θ_E·n_T1) 전부 미지정 상태에서 v1.0.19 모듈과 동일 입력 그리드 출력 비교
  — 전 경로(흑연 equilibrium/dqdv/curve/entropy_coefficient(+return_terms)/reversible_heat/
    x̄ 진입점 3종/seed_L_V + LCO equilibrium/curve/entropy_coefficient) max|Δ| ≤ 1e-12.
    보조: v1.0.19 골든(golden_graphite_ref.npz, 원 캡처 머신 기준) 대비 ≤ 1e-12
    (본 컨테이너 환경 잡음 기준 P0: ≤ 4.33e-15 — RESULT_P0_setup.md).
[G2 회귀 기준 — ch2_appB B.2, 표시 정밀도 일치] 298.15 K·4-전이 staging·w=RT/F 에서
  U_oc(x̄=0.25)=74.4 mV / ∂U_oc/∂T 완전식 −0.204·단순식 −0.134·config −0.070 mV/K /
  round-trip [U(T+3)−U(T−3)]/6K=−0.204·해석식과 <0.001 µV/K / ΔS=−19.7 J/mol/K·
  Q̇_rev/I=+60.8 mV / tab:qrev 5점(U_oc·∂U/∂T·ΔS·Q̇_rev/I 전 열) / tab:worked 중간값 /
  파생 A: x̄∈[0.05,0.95] 175점 완전식 vs 유한차분(T1=292.15·T2=298.15, 해석식 295.15 K 평가
  — 원 검증 42_numerical_verification.md 규약) 표시 정밀도(≲1e-2 mV/K) 일치·내부 경계 3곳
  연속 블렌드(인접 ΔS⁰/F 사이 값·계단 없음).
[G3 θ_E bit-exact] vib 가산 4곳(equilibrium·dqdv·entropy_coefficient·solve_U_oc)을 소스에서
  제거한 '보정 도입 이전' 변형 모듈을 즉석 생성, θ_E 미지정 v1.0.24 과 전 경로 np.array_equal
  (bit-exact) 대조. + 발효 확인(θ_E=700 K: T_ref 서 불변·T≠T_ref 서 변화·C-62 수치
  −3.74/0/+3.70/+9.14 µV/K).
[부록 — n(T) 전파 증빙(ch1_appB)] n_T1 부재=상수 n bit-exact(값 수준)·발효 시
  ∂w/∂T=(R/F)(n(T)+T·n_T1) 해석=수치 일치·n_T1≠0 round-trip 정합.

[R6 블렌드 게이트 — 문건 §3.5 doc-leads 요구명세(BlendedAnodeDQDV)] ★위 G1/G2/G3 과 별개 번호계다
  (혼동 금지 — 위는 v1.0.19 하위호환/B.2 회귀/θ_E; 아래는 §3.5 블렌드 G1/G2/G3):
  · R6-G1(bit-exact): f_Si=0 에서 BlendedAnodeDQDV ≡ GraphiteAnodeDischargeDQDV 부동소수점 동일
    (equilibrium·dqdv(dis/chg×C-rate)·curve·solve_U_oc 전 경로 np.array_equal; eq:si-code-bitexact)
    + 발효(f_Si=0.3 이 곡선을 실제로 바꿈).
  · R6-G2(스윕 연속성): m_Si∈(0,0.30] wt% 균일 그리드(f_Si=C-052 환산)에서 인접 스윕 점 간 곡선
    sup-편차가 (i) 전부 유한 (ii) 점프 없음(max/mean < 5) (iii) 그리드 2배 세분 시 최대 스텝 ~½
    (Lipschitz 연속의 수치 서명; 불연속이면 세분화에도 안 줄어듦) — 공통-μ 1차 근사 안의 연속성.
  · R6-G3(용량 보존): 평형 산출 ∫(dQ/dV−C_bg)dV = Q_gr+Q_Si 가 f_Si 전 구간 성립. 검사 창 = 전
    전이 U_j±k·w_j(k=20), 잘림 상한 Σ Q_j e^{-k}, 상대 공차 |Δ|/Q ≤ 1e-6.
  · 커버리지: 3 케이스('elemental'·'siox'·'sic') 구성·실행 + SiOₓ 공백 경고 발효(조용한 날조 금지).

[재현] PYTHONIOENCODING=utf-8 python test_gates_v1020.py
  (v1.0.19 폴더는 읽기 전용 사용 — sys.dont_write_bytecode 로 pyc 미생성.
   G3 변형 모듈 임시 파일 위치는 env ANODEFIT_TMP 지정 가능, 기본 tempfile.)
"""
import sys, os, importlib.util, tempfile
sys.dont_write_bytecode = True   # v1.0.19 폴더(읽기 전용 취급)에 __pycache__ 미생성
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_V20 = os.path.join(HERE, "Anode_Fit_v1.0.24.py")
CODE_V19 = os.path.normpath(os.path.join(HERE, "..", "v1.0.19", "Anode_Fit_v1.0.19.py"))
GOLD = os.path.normpath(os.path.join(HERE, "..", "v1.0.19", "golden_graphite_ref.npz"))

G1_TOL = 1e-12          # 게이트 문턱(환경 잡음 P0 4.33e-15 여유 포함)
G2_FD_ANALYTIC_UVK = 1e-3   # round-trip |FD-해석| < 0.001 µV/K (B.2)
G2_DERIVA_MVK = 1e-2        # 파생 A 표시 정밀도 ≲ 1e-2 mV/K
G2_STEP_UVK = 25.0          # 경계 국소 계단 부재: 격자 스텝당 < 25 µV/K
                            # (원 검증 최대 13 µV/K/step; 최소 인접 plateau 간격 52 µV/K 미만)

# --- R6 블렌드 게이트 상수(문건 §3.5 codebox 제안값) ------------------------------
R6_G2_JUMP_FACTOR = 5.0     # 점프 없음 판정: 인접 스윕 sup-편차 max/mean 상한(연속·매끈 진화 판정)
R6_G2_REFINE_LO = 0.40     # 그리드 2배 세분 시 최대 스텝 비 하한(Lipschitz 연속 ~0.5)
R6_G2_REFINE_HI = 0.62     #   상한(불연속이면 세분화에도 ~1.0 유지 → 이 창 밖이면 FAIL)
R6_G3_K = 20               # 검사 창 여유 배수 k(전 전이 U_j±k·w_j; 잘림 상한 Σ Q_j e^{-k})
R6_G3_RTOL = 1e-6          # 용량 보존 상대 공차 |∫(dQ/dV−C_bg)dV − Q|/Q
R6_G3_NPTS = 400001        # 구적 격자점(창 폭에 대해 w≫ΔV — 사다리꼴 잘림·구적 오차 ≪ 공차)

# np.trapz 는 numpy 2.0 에서 np.trapezoid 로 개명 — 버전 무관 안전 별칭.
_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- 공통 출력셋
def output_set(m):
    """v1.0.19/v1.0.24/변형 모듈 공통 산출 사전 — 신기능 전부 미지정(θ_E·n_T1 無)."""
    V = np.linspace(0.03, 0.34, 1000)
    xg = np.linspace(0.05, 0.95, 91)
    Tprof = np.linspace(288.15, 308.15, V.size)
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    out = {}
    out["seed_L_V"] = np.asarray(model.seed_L_V, dtype=float)
    out["equilibrium_298"] = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    for s, name in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            out[f"dqdv_{name}_I{I}"] = np.asarray(
                model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s), dtype=float)
    for Tk in (258.15, 298.15, 318.15):
        out[f"dqdv_T{int(Tk)}"] = np.asarray(
            model.dqdv(V, T=Tk, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["dqdv_TV"] = np.asarray(model.dqdv(V, T=Tprof, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["curve_dis_02C"] = np.asarray(
        model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["dqdv_scalarV"] = np.asarray([model.dqdv(0.12, T=298.15, I_abs=0.2, Q_cell=1.0, s=+1)])
    # V_n 진입점 발열 경로(하위호환 유지 대상 — ch2_appB B.1)
    out["entropy_V_298"] = np.asarray(model.entropy_coefficient(V, 298.15), dtype=float)
    out["entropy_V_TV"] = np.asarray(model.entropy_coefficient(V, Tprof), dtype=float)
    rt = model.entropy_coefficient(V, 298.15, return_terms=True)
    for k in ("complete", "simple", "config"):
        out[f"entropy_V_terms_{k}"] = np.asarray(rt[k], dtype=float)
    out["revheat_V"] = np.asarray(model.reversible_heat(V, 298.15, I=1.0), dtype=float)
    # x̄ 진입점 3종(ch2_appB B.1)
    out["Uoc_x"] = np.asarray(model.solve_U_oc(xg, 298.15), dtype=float)
    tx = model.entropy_coefficient_x(xg, 298.15, return_terms=True)
    for k in ("U_oc", "complete", "simple", "config"):
        out[f"entropy_x_terms_{k}"] = np.asarray(tx[k], dtype=float)
    out["qrev_x"] = np.asarray(model.reversible_heat_x(xg, 298.15, I=1.0), dtype=float)
    # LCO 서브클래스 경로(seam·전자항 — 흑연 무섭동 확인 대상)
    VL = np.linspace(3.75, 4.15, 800)
    lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, Rn=0.005, Cbg=0.0)
    out["lco_eq_298"] = np.asarray(lco.equilibrium(VL, T=298.15), dtype=float)
    out["lco_curve_chg"] = np.asarray(
        lco.curve(VL, direction="charge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["lco_curve_dis"] = np.asarray(
        lco.curve(VL, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["lco_entropy"] = np.asarray(lco.entropy_coefficient(VL, 298.15), dtype=float)
    return out


def compare_sets(a, b):
    """두 출력셋 비교 — (전건 bit-exact 여부, 전 키 max|Δ|, 불일치 목록)."""
    assert set(a.keys()) == set(b.keys())
    worst = 0.0
    all_bit = True
    bad = []
    for k in a:
        eq = np.array_equal(a[k], b[k])
        d = float(np.max(np.abs(a[k] - b[k]))) if a[k].shape == b[k].shape else np.inf
        worst = max(worst, d)
        if not eq:
            all_bit = False
            bad.append((k, d))
    return all_bit, worst, bad


def golden_outputs(m):
    """v1.0.19 회귀 하네스(test_regression_v1019.py graphite_outputs)와 동일 13 케이스."""
    V = np.linspace(0.03, 0.34, 1000)
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    out = {"V": V}
    out["equilibrium_298"] = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    for s, name in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            out[f"dqdv_{name}_I{I}"] = np.asarray(
                model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s), dtype=float)
    for Tk in (258.15, 298.15, 318.15):
        out[f"dqdv_T{int(Tk)}"] = np.asarray(
            model.dqdv(V, T=Tk, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    Tprof = np.linspace(288.15, 308.15, V.size)
    out["dqdv_TV"] = np.asarray(model.dqdv(V, T=Tprof, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["curve_dis_02C"] = np.asarray(
        model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    return out


# ---------------------------------------------------------------- G1
def gate_G1(m19, m20):
    print("=" * 74)
    print("G1: backward-compat  v1.0.24 vs v1.0.19  (new features all unspecified)")
    out19 = output_set(m19)
    out20 = output_set(m20)
    all_bit, worst, bad = compare_sets(out19, out20)
    print(f"  compared arrays: {len(out19)}  bit-exact(np.array_equal): {all_bit}  "
          f"max|diff|: {worst:.3e}")
    for k, d in bad:
        print(f"    MISMATCH {k}: max|diff|={d:.3e}")
    ok_main = (worst <= G1_TOL)
    # 보조: v1.0.19 골든 npz(원 캡처 머신) 대비 — 환경 잡음 확인(회귀 하네스 동일 13 케이스)
    gold = np.load(GOLD)
    gout = golden_outputs(m20)
    worst_g = 0.0
    n_exact = 0
    for k in gold.files:
        d = float(np.max(np.abs(gout[k] - gold[k])))
        worst_g = max(worst_g, d)
        n_exact += int(np.array_equal(gout[k], gold[k]))
    print(f"  [aux] golden npz ({len(gold.files)} arrays, other-machine capture): "
          f"max|diff|={worst_g:.3e}  bit-exact {n_exact}/{len(gold.files)} "
          f"(P0 env-noise ref 4.33e-15)")
    ok = ok_main and (worst_g <= G1_TOL)
    print(f"  G1 RESULT: {'PASS' if ok else 'FAIL'}  "
          f"(module-vs-module {worst:.3e} <= {G1_TOL:.0e}; golden {worst_g:.3e} <= {G1_TOL:.0e})")
    return ok, worst, worst_g, all_bit


# ---------------------------------------------------------------- G2
def _disp(v, fmt):
    return format(v, fmt)


def gate_G2(m):
    print("=" * 74)
    print("G2: regression reference values (ch2_appB B.2, display-precision match)")
    ok = True
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    F = m.F

    # --- (a)-(e) worked example, x̄=0.25 · 298.15 K -------------------------
    t = model.entropy_coefficient_x(0.25, 298.15, return_terms=True)
    Uoc = t["U_oc"]; comp = t["complete"]; simp = t["simple"]; conf = t["config"]
    dS = F * comp
    qrev = model.reversible_heat_x(0.25, 298.15, I=1.0)
    rows = [
        ("U_oc [mV]",            Uoc * 1e3,  ".1f",  "74.4"),
        ("dU/dT complete [mV/K]", comp * 1e3, "+.3f", "-0.204"),
        ("dU/dT simple  [mV/K]",  simp * 1e3, "+.3f", "-0.134"),
        ("dU/dT config  [mV/K]",  conf * 1e3, "+.3f", "-0.070"),
        ("dS = F*dU/dT [J/mol/K]", dS,        "+.1f", "-19.7"),
        ("Qrev/I = -T*dU/dT [mV]", qrev * 1e3, "+.1f", "+60.8"),
    ]
    for label, val, fmt, want in rows:
        got = _disp(val, fmt)
        hit = (got == want)
        ok &= hit
        print(f"  {label:26s} value={val:+.6f}  display={got}  doc={want}  {'OK' if hit else 'FAIL'}")

    # round-trip 유한차분 (B.2)
    fd = (model.solve_U_oc(0.25, 298.15 + 3.0) - model.solve_U_oc(0.25, 298.15 - 3.0)) / 6.0
    rt_uVK = abs(fd - comp) * 1e6
    got = _disp(fd * 1e3, "+.3f")
    hit = (got == "-0.204") and (rt_uVK < G2_FD_ANALYTIC_UVK)
    ok &= hit
    print(f"  round-trip [U(T+3)-U(T-3)]/6K = {fd*1e3:+.6f} mV/K (display {got}, doc -0.204); "
          f"|FD-analytic| = {rt_uVK:.3e} uV/K (< {G2_FD_ANALYTIC_UVK}) {'OK' if hit else 'FAIL'}")

    # --- tab:worked 중간값(전이별) -----------------------------------------
    print("  --- tab:worked per-transition intermediates (x=0.25, 298.15 K) ---")
    T0 = 298.15
    xi_doc = ["0.005", "0.072", "0.143", "0.395"]
    g_doc = ["0.19", "2.61", "4.77", "9.30"]
    sh_doc = ["0.003", "0.051", "0.193", "0.753"]
    ds_doc = ["+0.301", "+0.000", "-0.052", "-0.166"]
    cf_doc = ["-0.458", "-0.220", "-0.154", "-0.037"]
    xi_l, g_l, Qg_l, cf_l, ds_l = [], [], [], [], []
    for tr in m.GRAPHITE_STAGING_LIT:
        U_j = m.func_U_j(T0, tr["dH_rxn"], tr["dS_rxn"])
        w = m.func_w(T0, tr["n"])
        xi = float(m.func_ksi_eq(T0, Uoc, U_j, tr["n"]))
        g = xi * (1.0 - xi) / w
        xi_l.append(xi); g_l.append(g); Qg_l.append(tr["Q"] * g)
        ds_l.append(tr["dS_rxn"] / F)
        cf_l.append((tr["n"] * m.R / F) * np.log(xi / (1.0 - xi)))
    den = sum(Qg_l)
    hit_den = (_disp(den, ".2f") == "6.18")
    ok &= hit_den
    print(f"    sum Q_j g_j = {den:.4f} /V (display {den:.2f}, doc 6.18) {'OK' if hit_den else 'FAIL'}")
    for j in range(4):
        got = (_disp(xi_l[j], ".3f"), _disp(g_l[j], ".2f"), _disp(Qg_l[j] / den, ".3f"),
               _disp(ds_l[j] * 1e3, "+.3f"), _disp(cf_l[j] * 1e3, "+.3f"))
        want = (xi_doc[j], g_doc[j], sh_doc[j], ds_doc[j], cf_doc[j])
        hit = (got == want)
        ok &= hit
        print(f"    j={j}: xi={got[0]}({want[0]}) g={got[1]}({want[1]}) share={got[2]}({want[2]}) "
              f"dS/F={got[3]}({want[3]}) config={got[4]}({want[4]}) {'OK' if hit else 'FAIL'}")

    # --- tab:qrev 5점(전 열: U_oc·dU/dT·dS·Qrev/I) --------------------------
    print("  --- tab:qrev 5-point (298.15 K, full columns) ---")
    tabq = {0.10: ("43.5", "-0.307", "-29.6", "+91.5"),
            0.25: ("74.4", "-0.204", "-19.7", "+60.8"),
            0.50: ("109.0", "-0.089", "-8.6", "+26.6"),
            0.75: ("148.8", "+0.044", "+4.3", "-13.2"),
            0.90: ("195.2", "+0.218", "+21.0", "-64.9")}
    for xb, (u_w, d_w, s_w, q_w) in tabq.items():
        tt = model.entropy_coefficient_x(xb, 298.15, return_terms=True)
        q = model.reversible_heat_x(xb, 298.15, I=1.0)
        got = (_disp(tt["U_oc"] * 1e3, ".1f"), _disp(tt["complete"] * 1e3, "+.3f"),
               _disp(F * tt["complete"], "+.1f"), _disp(q * 1e3, "+.1f"))
        hit = (got == (u_w, d_w, s_w, q_w))
        ok &= hit
        print(f"    x={xb:.2f}: U_oc={got[0]}({u_w})  dU/dT={got[1]}({d_w})  "
              f"dS={got[2]}({s_w})  Qrev/I={got[3]}({q_w})  {'OK' if hit else 'FAIL'}")

    # --- 파생 A: 175점 전 범위 완전식 vs 유한차분 + 내부 경계 3곳 연속 -------
    print("  --- derived A: 175-pt full-range complete vs FD + 3-boundary continuity ---")
    T1, T2 = 292.15, 298.15
    Tm = 0.5 * (T1 + T2)                     # 295.15 K — 원 검증 규약(해석식 평가 온도)
    xg = np.linspace(0.05, 0.95, 175)
    U1 = model.solve_U_oc(xg, T1)
    U2 = model.solve_U_oc(xg, T2)
    fd = (U2 - U1) / (T2 - T1)
    tm = model.entropy_coefficient_x(xg, Tm, return_terms=True)
    err_c = np.abs(fd - tm["complete"]) * 1e3    # mV/K
    err_s = np.abs(fd - tm["simple"]) * 1e3
    cfg = tm["config"] * 1e3
    hit = bool(np.max(err_c) <= G2_DERIVA_MVK)
    ok &= hit
    print(f"    complete vs FD: max={np.max(err_c):.3e} mV/K  mean={np.mean(err_c):.3e} "
          f"(gate <= {G2_DERIVA_MVK} mV/K, display precision) {'OK' if hit else 'FAIL'}")
    print(f"    [ref] simple vs FD: max={np.max(err_s):.4f} mV/K (doc grid-max ~0.18; span-dep)")
    print(f"    [ref] config span: [{np.min(cfg):+.3f}, {np.max(cfg):+.3f}] mV/K "
          f"(doc ~[-0.21,+0.14]; span-dep)")
    # 내부 경계 3곳: 인접 봉우리 중심의 x̄ 중점에서 (i) 인접 ΔS⁰/F 사이 값(블렌드),
    # (ii) 국소 계단 부재(격자 스텝당 변화 < G2_STEP_UVK)
    peaks = []
    for tr in m.GRAPHITE_STAGING_LIT:
        U_j = m.func_U_j(Tm, tr["dH_rxn"], tr["dS_rxn"])
        xpk = sum(t2["Q"] * float(m.func_ksi_eq(Tm, U_j, m.func_U_j(Tm, t2["dH_rxn"], t2["dS_rxn"]), t2["n"]))
                  for t2 in m.GRAPHITE_STAGING_LIT) / sum(t2["Q"] for t2 in m.GRAPHITE_STAGING_LIT)
        peaks.append((xpk, tr["dS_rxn"] / F * 1e3))     # (x̄_peak, plateau [mV/K])
    peaks.sort()
    dstep = np.abs(np.diff(tm["complete"])) * 1e6       # µV/K per grid step
    for i in range(3):
        (xa, da), (xb_, db) = peaks[i], peaks[i + 1]
        xmid = 0.5 * (xa + xb_)
        vmid = float(model.entropy_coefficient_x(xmid, Tm)) * 1e3
        lo, hi = min(da, db), max(da, db)
        blend = (lo < vmid < hi)
        k = int(np.argmin(np.abs(xg - xmid)))
        near = dstep[max(0, k - 5):k + 5]
        nostep = bool(np.max(near) < G2_STEP_UVK)
        hit = blend and nostep
        ok &= hit
        print(f"    boundary {i+1}: x_mid={xmid:.3f}  dU/dT={vmid:+.4f} mV/K in "
              f"({lo:+.3f},{hi:+.3f})? {blend}  local max step={np.max(near):.1f} uV/K "
              f"(< {G2_STEP_UVK}) {'OK' if hit else 'FAIL'}")
    print(f"    [ref] global max per-step change: {np.max(dstep):.1f} uV/K "
          f"(175-pt grid; original 181-pt verification: max 13 uV/K/step)")
    print(f"  G2 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- G3
_VIB_PATCHES = [  # '보정 도입 이전' 소스 변형(발생 횟수 고정 — 어긋나면 즉시 FAIL)
    (" + self._vib_dU(tr, T)", "", 3),        # equilibrium·entropy_coefficient·solve_U_oc
    (" + self._vib_dU(tr, T_prog)", "", 1),   # dqdv
    ("dS0 + self._vib_dS(tr, T)", "dS0", 1),  # entropy_coefficient
]


def gate_G3(m20):
    print("=" * 74)
    print("G3: theta_E bit-exact  (unspecified path == pre-correction code)")
    ok = True
    src = open(CODE_V20, encoding="utf-8").read()
    for pat, rep, n_want in _VIB_PATCHES:
        n = src.count(pat)
        if n != n_want:
            print(f"  FAIL: patch pattern {pat!r} count {n} != {n_want} (source drift)")
            return False
        src = src.replace(pat, rep)
    tmpdir = os.environ.get("ANODEFIT_TMP") or tempfile.mkdtemp(prefix="anodefit_g3_")
    os.makedirs(tmpdir, exist_ok=True)
    vpath = os.path.join(tmpdir, "Anode_Fit_v1020_previb_variant.py")
    with open(vpath, "w", encoding="utf-8") as f:
        f.write(src)
    m_pre = load(vpath, "anodefit_previb")
    out20 = output_set(m20)
    outpre = output_set(m_pre)
    all_bit, worst, bad = compare_sets(out20, outpre)
    ok &= all_bit
    print(f"  v1.0.24(no theta_E) vs pre-correction variant: arrays={len(out20)}  "
          f"bit-exact={all_bit}  max|diff|={worst:.3e}  {'OK' if all_bit else 'FAIL'}")
    for k, d in bad:
        print(f"    MISMATCH {k}: max|diff|={d:.3e}")

    # 발효 확인: theta_E=700 K 부여 — T_ref(298.15) 불변·T=318.15 변화 + C-62 수치
    trs = [dict(t) for t in m20.GRAPHITE_STAGING_LIT]
    trs[3]["theta_E"] = 700.0
    V = np.linspace(0.03, 0.34, 1000)
    mth = m20.GraphiteAnodeDischargeDQDV(trs, x=0.5, Rn=0.01, Cbg=0.05)
    mno = m20.GraphiteAnodeDischargeDQDV(
        [dict(t) for t in m20.GRAPHITE_STAGING_LIT], x=0.5, Rn=0.01, Cbg=0.05)
    same_ref = np.array_equal(mth.equilibrium(V, 298.15), mno.equilibrium(V, 298.15))
    d318 = float(np.max(np.abs(mth.equilibrium(V, 318.15) - mno.equilibrium(V, 318.15))))
    eff = same_ref and (d318 > 0.0)
    ok &= eff
    print(f"  effectiveness: theta_E=700K on tr[3] -> T_ref outputs equal: {same_ref}; "
          f"T=318.15K max|diff|={d318:.3e} (>0) {'OK' if eff else 'FAIL'}")
    # C-62: dDeltaU_vib/dT = DeltaS_vib(T)/F @ 278.15/298.15/318.15/348.15 (doc -3.74/0/+3.70/+9.14 uV/K)
    c62_doc = {278.15: "-3.74", 298.15: "+0.00", 318.15: "+3.70", 348.15: "+9.14"}
    for Tk, want in c62_doc.items():
        v = float(mth._vib_dS(trs[3], Tk)) / m20.F * 1e6   # uV/K
        got = _disp(v, "+.2f")
        hit = (got == want) or (want == "+0.00" and got in ("+0.00", "-0.00"))
        ok &= hit
        print(f"    C-62 dDU_vib/dT @T={Tk}: {v:+.4f} uV/K (display {got}, doc {want}) "
              f"{'OK' if hit else 'FAIL'}")
    print(f"  G3 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------- 부록: n(T) 전파 증빙
def check_nT(m):
    print("=" * 74)
    print("APPENDIX: n(T)=n+n_T1*(T-T_ref) propagation evidence (ch1_appB)")
    ok = True
    V = np.linspace(0.03, 0.34, 1000)
    base = [dict(t) for t in m.GRAPHITE_STAGING_LIT]
    with0 = [dict(t, n_T1=0.0) for t in m.GRAPHITE_STAGING_LIT]
    mb = m.GraphiteAnodeDischargeDQDV(base, x=0.5, Rn=0.01, Cbg=0.05)
    m0 = m.GraphiteAnodeDischargeDQDV(with0, x=0.5, Rn=0.01, Cbg=0.05)
    pairs = [
        ("equilibrium_298", mb.equilibrium(V, 298.15), m0.equilibrium(V, 298.15)),
        ("dqdv_dis_0.2", mb.dqdv(V, 298.15, 0.2, 1.0, +1), m0.dqdv(V, 298.15, 0.2, 1.0, +1)),
        ("entropy_V", mb.entropy_coefficient(V, 298.15), m0.entropy_coefficient(V, 298.15)),
        ("Uoc_x", mb.solve_U_oc(np.linspace(0.05, 0.95, 31), 298.15),
                  m0.solve_U_oc(np.linspace(0.05, 0.95, 31), 298.15)),
    ]
    for k, a, b in pairs:
        eq = np.array_equal(np.asarray(a), np.asarray(b))
        ok &= eq
        print(f"  n_T1=0.0 == absent (value bit-exact) {k}: {eq}")
    # 발효: n_T1=5e-4 — ∂w/∂T 해석 vs 중심차분(2차식이라 이론상 정확 일치)
    tr = dict(m.GRAPHITE_STAGING_LIT[3], n_T1=5e-4)
    mx = m.GraphiteAnodeDischargeDQDV([tr], x=0.5, Rn=0.0, Cbg=0.0)
    T0, dT = 298.15, 0.5
    dw_an = float(mx._dwdT(tr, T0))
    dw_fd = float((mx._width(tr, T0 + dT) - mx._width(tr, T0 - dT)) / (2 * dT))
    rel = abs(dw_an - dw_fd) / abs(dw_an)
    hit = rel < 1e-9
    ok &= hit
    print(f"  n_T1=5e-4: dw/dT analytic={dw_an:.9e} V/K  centered-FD={dw_fd:.9e}  "
          f"rel-diff={rel:.2e} (<1e-9) {'OK' if hit else 'FAIL'}")
    # 발효: round-trip 정합 — config 계수 (R/F)(n(T)+T·n_T1) 가 솔버·완전식에 동반 전파
    trs = [dict(t, n_T1=5e-4) for t in m.GRAPHITE_STAGING_LIT]
    mr = m.GraphiteAnodeDischargeDQDV(trs, x=0.5, Rn=0.01, Cbg=0.05)
    fd = (mr.solve_U_oc(0.25, T0 + 3.0) - mr.solve_U_oc(0.25, T0 - 3.0)) / 6.0
    an = mr.entropy_coefficient_x(0.25, T0)
    d_uVK = abs(fd - an) * 1e6
    hit = d_uVK < 1e-2
    ok &= hit
    print(f"  n_T1=5e-4 round-trip @x=0.25: FD={fd*1e3:+.6f} analytic={an*1e3:+.6f} mV/K  "
          f"|diff|={d_uVK:.3e} uV/K (<1e-2) {'OK' if hit else 'FAIL'}")
    print(f"  n(T) RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ============================================================================
# R6 블렌드 게이트 — BlendedAnodeDQDV (문건 §3.5 doc-leads 요구명세)
#   ★번호계 주의(P3 항목 7): 아래 R6-G1/G2/G3 은 문건 §3.5 codebox 의 블렌드 게이트로, 위쪽
#     G1/G2/G3(v1.0.19 하위호환·B.2 회귀·θ_E bit-exact)과 이름만 같을 뿐 별개다.
# ============================================================================
def gate_R6_G1(m):
    """R6-G1: f_Si=0 에서 흑연 단독과 부동소수점 동일(eq:si-code-bitexact)."""
    print("=" * 74)
    print("R6-G1 (blend): f_Si=0 bit-exact vs graphite-only  (eq:si-code-bitexact)")
    V = np.linspace(0.03, 0.55, 1200)          # 흑연~Si 전위대 포함
    xg = np.linspace(0.05, 0.95, 91)
    kw = dict(x=0.5, Rn=0.01, use_dH_eff=True)  # 흑연 단독 회귀 조건과 동일
    gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, Cbg=0.05, **kw)
    bl = m.BlendedAnodeDQDV(0.0, si_case='sic',
                            graphite_transitions=m.GRAPHITE_STAGING_LIT, Cbg=0.05, **kw)
    checks = [("equilibrium",
               np.asarray(gr.equilibrium(V, 298.15)),
               np.asarray(bl.equilibrium(V, 298.15)))]
    for s, nm in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            checks.append((f"dqdv_{nm}_I{I}",
                           np.asarray(gr.dqdv(V, 298.15, I, 1.0, s=s)),
                           np.asarray(bl.dqdv(V, 298.15, I, 1.0, s=s))))
    checks.append(("curve_dis_0.2C",
                   np.asarray(gr.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15)),
                   np.asarray(bl.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15))))
    checks.append(("solve_U_oc",
                   np.asarray(gr.solve_U_oc(xg, 298.15)),
                   np.asarray(bl.solve_U_oc(xg, 298.15))))
    ok = True
    worst = 0.0
    for nm, a, b in checks:
        eq = np.array_equal(a, b)
        d = float(np.max(np.abs(a - b))) if a.shape == b.shape else np.inf
        worst = max(worst, d)
        ok &= eq
        print(f"  {nm:16s} array_equal={eq}  max|diff|={d:.3e}")
    # 발효: f_Si>0 이면 Si 항이 실제로 곡선을 바꾼다(무효 no-op 아님을 확인)
    bl2 = m.BlendedAnodeDQDV(0.3, si_case='sic',
                             graphite_transitions=m.GRAPHITE_STAGING_LIT, Cbg=0.05, **kw)
    d_on = float(np.max(np.abs(np.asarray(bl2.equilibrium(V, 298.15))
                               - np.asarray(gr.equilibrium(V, 298.15)))))
    q_ok = abs(bl2.Q_Si / bl2.Q - 0.3) < 1e-12   # 용량 배분 Q_Si/Q=f_Si 검산
    eff = (d_on > 0.0) and q_ok
    ok &= eff
    print(f"  effectiveness: f_Si=0.3 changes equilibrium (max|diff|={d_on:.3e}>0) & "
          f"Q_Si/Q={bl2.Q_Si/bl2.Q:.6f}(=0.3): {eff}")
    print(f"  R6-G1 RESULT: {'PASS' if ok else 'FAIL'}  (worst bit-diff={worst:.3e})")
    return ok


def gate_R6_G2(m):
    """R6-G2: m_Si∈(0,0.30] wt% 스윕 곡선 연속성(f_Si=C-052 환산; 공통-μ 1차 근사 안)."""
    print("=" * 74)
    print("R6-G2 (blend): m_Si sweep continuity on (0,0.30] wt%  (f_Si via C-052)")
    V = np.linspace(-0.1, 0.7, 1600)           # 흑연+Si 전 전이 덮게
    kw = dict(x=0.5, Rn=0.0, use_dH_eff=True)
    q_Si = m.SI_SPECIFIC_CAPACITY['sic']       # 3117 mAh/g (tier-A)
    q_gr = m.GRAPHITE_SPECIFIC_CAPACITY        # 372 mAh/g (관례)

    def sweep(n):
        ms = np.linspace(0.30 / n, 0.30, n)    # (0,0.30] 균일 그리드
        C, fS = [], []
        for mm in ms:
            bl = m.BlendedAnodeDQDV.from_wt(mm, q_Si=q_Si, q_gr=q_gr,
                                            si_case='sic', Cbg=0.05, **kw)
            C.append(np.asarray(bl.equilibrium(V, 298.15), dtype=float))
            fS.append(bl.f_Si)
        return np.asarray(fS), np.asarray(C)

    n = 60
    fS, C = sweep(n)
    finite = bool(np.all(np.isfinite(C)))
    D = np.max(np.abs(np.diff(C, axis=0)), axis=1)      # 인접 스윕 점 간 sup-norm 편차
    Dmax, Dmean = float(np.max(D)), float(np.mean(D))
    no_jump = finite and (Dmax <= R6_G2_JUMP_FACTOR * Dmean)     # 점프 없음(단일 급증 없음)
    # 세분화 수렴(연속의 강한 서명): 그리드 2배 → 최대 스텝 ~½(불연속이면 안 줄어듦)
    _, C2 = sweep(2 * n)
    _, C4 = sweep(4 * n)
    D2max = float(np.max(np.max(np.abs(np.diff(C2, axis=0)), axis=1)))
    D4max = float(np.max(np.max(np.abs(np.diff(C4, axis=0)), axis=1)))
    r1, r2 = D2max / Dmax, D4max / D2max
    refine = (R6_G2_REFINE_LO <= r1 <= R6_G2_REFINE_HI
              and R6_G2_REFINE_LO <= r2 <= R6_G2_REFINE_HI)
    ok = finite and no_jump and refine
    print(f"  f_Si range over m_Si∈(0,0.30]: [{fS.min():.4f}, {fS.max():.4f}] (doc: wt%→f_Si≈0–0.7)")
    print(f"  finite curves: {finite}")
    print(f"  adjacent sup-diff: max={Dmax:.4e} mean={Dmean:.4e} max/mean={Dmax/Dmean:.2f} "
          f"(<{R6_G2_JUMP_FACTOR} no-jump): {no_jump}")
    print(f"  refinement max-step: n={n}:{Dmax:.4e} 2n:{D2max:.4e} 4n:{D4max:.4e}  "
          f"ratios={r1:.3f},{r2:.3f} (~0.5 Lipschitz): {refine}")
    print(f"  R6-G2 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


def gate_R6_G3(m):
    """R6-G3: 평형 산출 ∫(dQ/dV−C_bg)dV = Q_gr+Q_Si (f_Si 전 구간; eq:blend-dqdv 용량 몫)."""
    print("=" * 74)
    print("R6-G3 (blend): capacity conservation  int(dQ/dV - Cbg) dV = Q_gr + Q_Si")
    T = 298.15
    kw = dict(x=0.5, Rn=0.0, use_dH_eff=True)
    ok = True
    for f_Si in (0.0, 0.1, 0.3, 0.5):
        bl = m.BlendedAnodeDQDV(f_Si, si_case='sic',
                                graphite_transitions=m.GRAPHITE_STAGING_LIT, Cbg=0.05, **kw)
        # 검사 창 = 전 전이 U_j ± k·w_j 를 덮게(pooled = 흑연 + (Q>0) Si 전이)
        cs, ws = [], []
        for tr in bl.transitions:
            if 'dH_rxn' in tr and 'dS_rxn' in tr:
                U = float(m.func_U_j(T, tr['dH_rxn'], tr['dS_rxn']))
            else:
                U = float(tr['U'])
            w = float(m.func_w(T, bl._balance_host._n_factor(tr, T)))
            cs.append(U)
            ws.append(w)
        Vlo = min(c - R6_G3_K * w for c, w in zip(cs, ws))
        Vhi = max(c + R6_G3_K * w for c, w in zip(cs, ws))
        V = np.linspace(Vlo, Vhi, R6_G3_NPTS)
        eq = np.asarray(bl.equilibrium(V, T), dtype=float)
        bg = (np.asarray(bl.Cbg(V), dtype=float) * np.ones_like(V)
              if callable(bl.Cbg) else np.full_like(V, float(bl.Cbg)))
        integ = float(_trapz(eq - bg, V))
        Q = bl.Q                                   # = Q_gr + Q_Si
        rel = abs(integ - Q) / Q
        trunc = sum(abs(tr['Q']) for tr in bl.transitions) * np.exp(-R6_G3_K) / Q
        hit = rel <= R6_G3_RTOL
        ok &= hit
        print(f"  f_Si={f_Si:.2f}: int={integ:.9f} Q={Q:.9f} "
              f"(Q_gr={bl.Q_gr:.4f},Q_Si={bl.Q_Si:.4f}) rel={rel:.2e} "
              f"(<={R6_G3_RTOL:.0e}; trunc<={trunc:.1e}) {'OK' if hit else 'FAIL'}")
    print(f"  R6-G3 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


def gate_R6_coverage(m):
    """R6 커버리지: 3 케이스 구성·실행 + SiOₓ 공백 경고 발효(조용한 날조 금지 확인)."""
    print("=" * 74)
    print("R6 coverage: 3 si_case build/run + SiOx gap warning (no silent fabrication)")
    import warnings
    V = np.linspace(0.0, 0.6, 400)
    kw = dict(x=0.5, Rn=0.01, use_dH_eff=True)
    ok = True
    for case in ('elemental', 'siox', 'sic'):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            bl = m.BlendedAnodeDQDV(0.2, si_case=case, Cbg=0.05, **kw)
            y = np.asarray(bl.equilibrium(V, 298.15), dtype=float)
        runs = bool(np.all(np.isfinite(y)))
        warned = any("확인 필요" in str(w.message) for w in wl)
        want_warn = (len(m.SI_CASE_GAPS.get(case, [])) > 0)
        gap_ok = (warned == want_warn)
        ok &= runs and gap_ok
        print(f"  si_case={case:9s} finite={runs} gaps={m.SI_CASE_GAPS.get(case, [])!r} "
              f"warned={warned}(expect {want_warn}) {'OK' if runs and gap_ok else 'FAIL'}")
    # GS-1/GS-2 명시 경계: 요청 시 NotImplementedError(조용한 날조 금지)
    bl = m.BlendedAnodeDQDV(0.2, si_case='sic', Cbg=0.05, **kw)
    for meth in ('plastic_hysteresis_loop', 'nonadditive_correction'):
        try:
            getattr(bl, meth)()
            hit = False
        except NotImplementedError:
            hit = True
        ok &= hit
        print(f"  boundary {meth}() -> NotImplementedError: {hit}")
    print(f"  R6 coverage RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    m19 = load(CODE_V19, "anodefit_v1019")
    m20 = load(CODE_V20, "anodefit_v1020")
    print(f"v1.0.19: {CODE_V19}\nv1.0.24: {CODE_V20}\nnumpy {np.__version__}, python {sys.version.split()[0]}")
    g1, w_mod, w_gold, bit = gate_G1(m19, m20)
    g2 = gate_G2(m20)
    g3 = gate_G3(m20)
    nt = check_nT(m20)
    # R6 블렌드 게이트(문건 §3.5 — 위 G1/G2/G3 과 별개 번호계) — 기존 게이트 전건 GREEN 유지 위에 증축.
    r6g1 = gate_R6_G1(m20)
    r6g2 = gate_R6_G2(m20)
    r6g3 = gate_R6_G3(m20)
    r6cov = gate_R6_coverage(m20)
    print("=" * 74)
    print(f">>> SUMMARY: G1 {'PASS' if g1 else 'FAIL'} (module max|d|={w_mod:.1e}, "
          f"golden max|d|={w_gold:.1e}, bit-exact={bit}) | G2 {'PASS' if g2 else 'FAIL'} | "
          f"G3 {'PASS' if g3 else 'FAIL'} | n(T) {'PASS' if nt else 'FAIL'}")
    print(f">>> R6 BLEND (§3.5): R6-G1 {'PASS' if r6g1 else 'FAIL'} | R6-G2 {'PASS' if r6g2 else 'FAIL'} | "
          f"R6-G3 {'PASS' if r6g3 else 'FAIL'} | coverage {'PASS' if r6cov else 'FAIL'}")
    all_green = g1 and g2 and g3 and nt and r6g1 and r6g2 and r6g3 and r6cov
    sys.exit(0 if all_green else 1)


if __name__ == "__main__":
    main()
