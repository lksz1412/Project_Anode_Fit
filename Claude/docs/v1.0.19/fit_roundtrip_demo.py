# -*- coding: utf-8 -*-
"""v1.0.19 피팅 round-trip 실증 데모 — 시뮬(합성) → 피팅 → 파라미터 회복 (G-usable C1).

[무엇을] "피팅은 코드 작성 가능 수준(시뮬 + round-trip 실증)" 기준의 실행체.
  알려진 참 파라미터 θ* 로 forward dQ/dV 합성곡선(+측정잡음)을 만들고, 문헌 초기값
  (GRAPHITE_STAGING_LIT 원본)에서 출발한 optimizer 가 θ* 를 회복하는지 전 과정을
  실행·판정한다 — FITTING_GUIDE §3 보충규정 "코드 검증 = round-trip: 알려진 θ* 로
  합성 곡선 + 측정 수준 잡음 → 전 파이프라인이 θ* 를 회복하는지"의 구현.

[구성 — FITTING_GUIDE §2 Phase A(저율 등온·tier-1) 시나리오]
  (a) 합성 데이터 : θ* = GRAPHITE_STAGING_LIT 의 내부 사본에 알려진 교란
        중심 ΔU_j*(± 몇 mV, dH_rxn 경유) · 폭 n_j*(0.40~0.55 협폭 — 실측 흑연 ICA
        의 분해된 staging 봉우리 대응, §1.5 'w' 폴백 12–20 mV ≈ n 0.47–0.78) ·
        면적 Q_j*(±~15%) 를 가한 4-전이 참 모델의 equilibrium(V, 298.15 K)
      + Gaussian 잡음(SNR = peak/σ = 200 명시; 시드 고정 = 재현 가능).
  (b) 손실함수   : 정규화 residual — 합성 데이터 peak max = 1 스케일 후 점별 제곱
      평균 L = mean[((model−data)/max(data))²]. §6 게이트 "잔차 ΣΔ²/N < 1e-4
      (정규화 dQ/dV)"와 동일 정규화(C4 해소). 잡음 바닥 E[L] = (1/SNR)² = 2.5e-5.
  (c) 최적화     : 단계 개방(굵은 것부터 — 과식별 회피, §2·§3 동결 사슬 축소판)
        stage-1 중심만(4) → stage-2 +폭 n_j(8) → stage-3 +면적 Q_j(12).
      ★중심은 §1 tier 표의 제약 "U_j 순서보존"을 모수화에 내장 — U_1 자유 +
      아래로 내려가는 gap 의 log(U_j = U_{j-1} − e^{g_j}) 로 내림차순을 구조적으로
      강제한다. 전이 합산이 (U,n,Q) triple 의 순열에 불변이라 순서 제약 없이는
      겹친 봉우리에서 라벨-축퇴 해(뒤바뀜·섞임)로 수렴할 수 있음을 본 데모 개발
      중 실측 확인(제약 도입 근거). n·Q 는 log-재모수화로 >0 경계 내재화.
      scipy.optimize.least_squares(trf); scipy 부재 환경은 순수 numpy
      Nelder-Mead 폴백(동일 손실).
  (d) 판정       : 회복오차 |Û−U*| ≤ 0.5 mV · n̂,Q̂ 상대오차 ≤ 2% · 최종 L < 1e-4
      (§6 게이트) · ΣQ̂/ΣQ* ∈ [0.95,1.05](면적보존) · U_j 순서보존 → 전항 충족 시
      "ROUND-TRIP: PASS". 그림 samples/fig_fit_roundtrip.png (참/합성+잡음/초기값/
      회복 곡선 · 정규화 잔차 · 수렴곡선 · 파라미터 회복오차).

[불변 조건] Anode_Fit_v1.0.19.py 는 import 만(무수정) — 교란·피팅은 전부 스크립트
  내부 사본(dict 복사)에만 가한다. 종료 시 GRAPHITE_STAGING_LIT 원본 무변조를 assert.
  Cbg 는 알려진 값으로 동결(§4 울타리 ⑨), 평형 곡선이라 Rn·꼬리 비활성(Phase A).

[재현] PYTHONIOENCODING=utf-8 python fit_roundtrip_demo.py
  (스크립트 폴더 기준 상대경로 — 어느 cwd 에서도 동일. 종료코드 0=PASS/1=FAIL.)
"""
import sys, os, copy, importlib.util
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp949 콘솔서도 실행 보장
except Exception:
    pass
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.environ.get("ANODEFIT_CODE", os.path.join(HERE, "Anode_Fit_v1.0.19.py"))
FIG = os.path.join(HERE, "samples", "fig_fit_roundtrip.png")

spec = importlib.util.spec_from_file_location("anodefit_roundtrip", CODE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# ---------------------------------------------------------------------------
# 0. 설정 — 전부 명시 상수(매직넘버 없음)
# ---------------------------------------------------------------------------
T0 = 298.15                    # 등온 [K] (Phase A: 저율 등온)
CBG = 0.05                     # 배경 dQ/dV — 알려진 값으로 동결(울타리 ⑨)
V_GRID = np.linspace(0.03, 0.34, 800)   # 측정 전압 격자 [V]
SNR = 200.0                    # peak/σ — §6 게이트(1e-4)와 정합(잡음바닥 2.5e-5 < 1e-4)
SEED = 20260713                # 잡음 시드(재현성)
W_TH = m.R * T0 / m.F          # 열적 폭 RT/F ≈ 25.69 mV — 중심오차의 % 환산 기준

# 참 교란 θ* (알려진 값 — 회복 대상). 초기값 = 교란 0 / n=1 / Q=표값.
#   ★식별 가능 구성: n*<1 협폭(§1.5 — 실측 흑연 ICA 의 분해된 staging 봉우리에 대응;
#   'w' 폴백 12–20 mV ≈ n 0.47–0.78). n≈1(FWHM 3.53·RT/F≈91 mV)이면 4봉우리가 한
#   혹으로 합쳐져 자유 12-파라미터 분해가 잡음 수준에서 축퇴 — 본 데모 개발 중 실측
#   확인(§3 round-trip 이 잡아내도록 설계된 바로 그 공선형 실패 모드).
DU_TRUE = np.array([+0.006, +0.005, -0.005, -0.003])   # 중심 이동 [V]
N_TRUE = np.array([0.55, 0.45, 0.50, 0.40])            # 폭 다중도(무차원, 협폭)
Q_TRUE = np.array([0.115, 0.105, 0.280, 0.460])        # 전이 용량

# 판정 임계(명시)
TOL_U_MV = 0.5     # |Û−U*| ≤ 0.5 mV
TOL_REL = 0.02     # n̂·Q̂ 상대오차 ≤ 2%
GATE_L = 1e-4      # §6 수렴 게이트(정규화 잔차 제곱평균)

BASE = copy.deepcopy(m.GRAPHITE_STAGING_LIT)           # 내부 사본(원본 불가침)
_BASE_SNAPSHOT = copy.deepcopy(m.GRAPHITE_STAGING_LIT) # 종료 시 무변조 assert 용
N_TR = len(BASE)


# ---------------------------------------------------------------------------
# 1. forward 모델 — θ=(ΔU, n, Q) → equilibrium dQ/dV (코드 무수정, 사본 dict 만)
# ---------------------------------------------------------------------------
def build_transitions(dU, n, Q):
    """BASE 사본에 θ 를 입힌 새 전이 리스트. 중심 이동은 dH_rxn 경유:
    U_j(T)=(−ΔH+TΔS)/F 이므로 ΔH → ΔH − F·ΔU 가 정확히 U_j += ΔU (T-무관)."""
    trs = []
    for j, base in enumerate(BASE):
        tr = dict(base)                       # shallow copy per dict — BASE 무변조
        tr['dH_rxn'] = base['dH_rxn'] - m.F * float(dU[j])
        tr['n'] = float(n[j])
        tr['Q'] = float(Q[j])
        trs.append(tr)
    return trs


def forward(dU, n, Q, V=V_GRID):
    """θ → 평형 dQ/dV (Phase A 대상; |I|→0 이라 Rn·꼬리 비활성).
    errstate: func_ksi_eq 의 np.where 이중분기가 극단 trial θ 에서 내는 무해한
    overflow 경고만 국소 억제(코드 자체가 가드된 설계 — 값은 정확)."""
    model = m.GraphiteAnodeDischargeDQDV(build_transitions(dU, n, Q),
                                         x=0.5, Rn=0.0, Cbg=CBG)
    with np.errstate(over='ignore', invalid='ignore'):
        return np.asarray(model.equilibrium(V, T=T0), dtype=float)


# ---------------------------------------------------------------------------
# 2. (a) 합성 데이터 — 참 곡선 + Gaussian 잡음(SNR 명시)
# ---------------------------------------------------------------------------
y_true = forward(DU_TRUE, N_TRUE, Q_TRUE)
rng = np.random.default_rng(SEED)
sigma = float(np.max(y_true)) / SNR
y_data = y_true + rng.normal(0.0, sigma, size=y_true.size)
SCALE = float(np.max(y_data))                 # peak max = 1 정규화 스케일(§6·C4)
NOISE_FLOOR = (1.0 / SNR) ** 2                # E[L] 잡음 바닥 ≈ (σ/peak)²
L_TRUE = float(np.mean(((y_true - y_data) / SCALE) ** 2))   # 참 θ* 의 손실(이 시드의 실측 잡음)

U_BASE_298 = np.array([float(m.func_U_j(T0, tr['dH_rxn'], tr['dS_rxn'])) for tr in BASE])
U_TRUE_298 = U_BASE_298 + DU_TRUE


# ---------------------------------------------------------------------------
# 3. (b) 손실함수 — 정규화 residual 점별 제곱평균(§6 게이트와 동일 정규화)
# ---------------------------------------------------------------------------
_eval_log = []   # 손실 평가마다 L 기록 — 수렴곡선(running-min)용


def residuals(theta, stage):
    """stage 별 자유변수 → 정규화 residual 벡터 r/√N (Σr² = L)."""
    dU, n, Q = unpack(theta, stage)
    r = (forward(dU, n, Q) - y_data) / SCALE
    L = float(np.mean(r * r))
    _eval_log.append(L)
    return r / np.sqrt(r.size)


def loss(theta, stage):
    r = residuals(theta, stage)
    return float(np.sum(r * r))


def pack_centers(U):
    """내림차순 중심 → [U_1, ln(gap_2), ln(gap_3), ln(gap_4)] (§1 tier 표 제약
    "U_j 순서보존"의 구조 강제 — 전이 합산의 (U,n,Q)-triple 순열 불변이 만드는
    라벨-축퇴 해를 모수화 수준에서 배제)."""
    U = np.asarray(U, dtype=float)
    return np.concatenate([[U[0]], np.log(-np.diff(U))])


def unpack_centers(p):
    """[U_1, ln(gap)] → 내림차순 중심 U_j = U_{j-1} − e^{g_j} (순서 항상 성립)."""
    gaps = np.exp(np.asarray(p[1:], dtype=float))
    return float(p[0]) - np.concatenate([[0.0], np.cumsum(gaps)])


def unpack(theta, stage):
    """자유변수 벡터 → (ΔU, n, Q). stage-1: 중심만 / stage-2: +log n / stage-3: +log Q.
    잠긴 그룹은 동결값(_frozen). log-재모수화 = n,Q>0·중심 내림차순 내재화."""
    theta = np.asarray(theta, dtype=float)
    dU = unpack_centers(theta[:N_TR]) - U_BASE_298
    n = np.exp(theta[N_TR:2 * N_TR]) if stage >= 2 else _frozen['n']
    Q = np.exp(theta[2 * N_TR:3 * N_TR]) if stage >= 3 else _frozen['Q']
    return dU, n, Q


_frozen = {'n': np.ones(N_TR), 'Q': np.array([tr['Q'] for tr in BASE], dtype=float)}


# ---------------------------------------------------------------------------
# 4. (c) 최적화 — scipy least_squares(우선) / 순수 Nelder-Mead 폴백
# ---------------------------------------------------------------------------
def _nelder_mead(f, x0, maxfev=20000, xatol=1e-10, fatol=1e-14):
    """의존성 없는 최소 Nelder-Mead(표준 계수 1/2/0.5/0.5) — scipy 부재 폴백."""
    x0 = np.asarray(x0, dtype=float)
    ndim = x0.size
    sim = [x0]
    for k in range(ndim):
        y = x0.copy()
        y[k] += 0.02 if x0[k] == 0.0 else 0.05 * abs(x0[k]) + 1e-3
        sim.append(y)
    sim = np.asarray(sim)
    fs = np.array([f(v) for v in sim])
    nfev = ndim + 1
    while nfev < maxfev:
        idx = np.argsort(fs); sim, fs = sim[idx], fs[idx]
        if (np.max(np.abs(sim[1:] - sim[0])) < xatol and
                np.max(np.abs(fs[1:] - fs[0])) < fatol):
            break
        cen = np.mean(sim[:-1], axis=0)
        xr = cen + (cen - sim[-1]); fr = f(xr); nfev += 1
        if fr < fs[0]:
            xe = cen + 2.0 * (cen - sim[-1]); fe = f(xe); nfev += 1
            sim[-1], fs[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < fs[-2]:
            sim[-1], fs[-1] = xr, fr
        else:
            xc = cen + 0.5 * (sim[-1] - cen); fc = f(xc); nfev += 1
            if fc < fs[-1]:
                sim[-1], fs[-1] = xc, fc
            else:
                for k in range(1, ndim + 1):
                    sim[k] = sim[0] + 0.5 * (sim[k] - sim[0])
                    fs[k] = f(sim[k]); nfev += 1
    idx = np.argsort(fs)
    return sim[idx][0]


try:
    from scipy.optimize import least_squares as _scipy_ls
    OPTIMIZER = "scipy.optimize.least_squares (trf)"
except Exception:            # scipy 부재 환경 — 순수 구현 폴백
    _scipy_ls = None
    OPTIMIZER = "pure-numpy Nelder-Mead fallback"


def run_stage(stage, theta0):
    """한 stage 최적화 실행 → (θ̂, 최종 L, eval 수)."""
    n_before = len(_eval_log)
    if _scipy_ls is not None:
        sol = _scipy_ls(residuals, theta0, args=(stage,),
                        method="trf", xtol=1e-14, ftol=1e-14, gtol=1e-14,
                        max_nfev=5000)
        theta_hat = sol.x
    else:
        theta_hat = _nelder_mead(lambda th: loss(th, stage), theta0)
    L_hat = loss(theta_hat, stage)
    return theta_hat, L_hat, len(_eval_log) - n_before


# --- stage 스케줄: 굵은 것부터 개방(§2 Phase A 내 단계 개방·warm start) ---
print(f"=== v1.0.19 fitting round-trip demo (optimizer: {OPTIMIZER}) ===")
print(f"  synthetic: {V_GRID.size} pts, T={T0} K, SNR={SNR:.0f} "
      f"(sigma={sigma:.4f}, noise floor L~{NOISE_FLOOR:.2e}), seed={SEED}")
theta_init = pack_centers(U_BASE_298)                       # 문헌표 중심에서 출발
L_init = loss(theta_init, 1)
print(f"  initial (literature table) L = {L_init:.3e}   "
      f"L(theta*) on this noise draw = {L_TRUE:.3e}")

tier_marks = []            # (누적 eval 경계, stage 라벨, L)
th1, L1, ne1 = run_stage(1, theta_init)
tier_marks.append((len(_eval_log), "stage-1 (U)", L1))
print(f"  stage-1 open centers ({N_TR} params): L={L1:.3e}  evals={ne1}")

th2 = np.concatenate([th1, np.log(_frozen['n'])])           # stage-2 warm start
th2, L2, ne2 = run_stage(2, th2)
tier_marks.append((len(_eval_log), "stage-2 (+n)", L2))
print(f"  stage-2 open +n_j    ({2*N_TR} params): L={L2:.3e}  evals={ne2}")

th3 = np.concatenate([th2, np.log(_frozen['Q'])])           # stage-3 warm start
th3, L3, ne3 = run_stage(3, th3)
tier_marks.append((len(_eval_log), "stage-3 (+Q)", L3))
print(f"  stage-3 open +Q_j    ({3*N_TR} params): L={L3:.3e}  evals={ne3}")

dU_hat, n_hat, Q_hat = unpack(th3, 3)
U_hat_298 = U_BASE_298 + dU_hat
y_fit = forward(dU_hat, n_hat, Q_hat)
y_init = forward(np.zeros(N_TR), _frozen['n'], _frozen['Q'])

# ---------------------------------------------------------------------------
# 5. (d) 보고·판정 — 회복오차 / §6 게이트 / 면적보존 / 순서보존
# ---------------------------------------------------------------------------
print("--- parameter recovery (theta* -> theta_hat) ---")
err_U_mV = (U_hat_298 - U_TRUE_298) * 1e3
err_n = (n_hat - N_TRUE) / N_TRUE
err_Q = (Q_hat - Q_TRUE) / Q_TRUE
for j in range(N_TR):
    print(f"  tr{j+1}: U*={U_TRUE_298[j]*1e3:8.3f} mV  U^={U_hat_298[j]*1e3:8.3f} mV "
          f"(err {err_U_mV[j]:+7.4f} mV) | n*={N_TRUE[j]:.3f} n^={n_hat[j]:.4f} "
          f"({err_n[j]*100:+6.3f}%) | Q*={Q_TRUE[j]:.3f} Q^={Q_hat[j]:.4f} "
          f"({err_Q[j]*100:+6.3f}%)")

ok_U = bool(np.max(np.abs(err_U_mV)) <= TOL_U_MV)
ok_n = bool(np.max(np.abs(err_n)) <= TOL_REL)
ok_Q = bool(np.max(np.abs(err_Q)) <= TOL_REL)
ok_gate = bool(L3 < GATE_L)
ratio_Q = float(np.sum(Q_hat) / np.sum(Q_TRUE))
ok_area = bool(0.95 <= ratio_Q <= 1.05)
ok_order = bool(np.all(np.diff(U_hat_298) < 0.0))   # 표 순서 = 중심 내림차순
print("--- gates ---")
print(f"  max|U err| = {np.max(np.abs(err_U_mV)):.4f} mV (tol {TOL_U_MV}) -> {ok_U}")
print(f"  max|n err| = {np.max(np.abs(err_n))*100:.3f}% (tol {TOL_REL*100:.0f}%) -> {ok_n}")
print(f"  max|Q err| = {np.max(np.abs(err_Q))*100:.3f}% (tol {TOL_REL*100:.0f}%) -> {ok_Q}")
print(f"  final L = {L3:.3e} < gate {GATE_L:.0e} (S6 normalized residual) -> {ok_gate}"
      f"   [noise floor ~{NOISE_FLOOR:.2e}]")
print(f"  area conservation sum(Q^)/sum(Q*) = {ratio_Q:.4f} in [0.95,1.05] -> {ok_area}")
print(f"  U_j order preserved (descending) -> {ok_order}")

untouched = (m.GRAPHITE_STAGING_LIT == _BASE_SNAPSHOT)
print(f"  GRAPHITE_STAGING_LIT untouched (import-only invariant) -> {untouched}")

all_pass = ok_U and ok_n and ok_Q and ok_gate and ok_area and ok_order and untouched
print(f"\n>>> ROUND-TRIP: {'PASS' if all_pass else 'FAIL'} "
      f"(synthetic theta* recovered from literature initial values)")

# ---------------------------------------------------------------------------
# 6. 그림 — samples/fig_fit_roundtrip.png (4패널)
# ---------------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))

    # (a) curves: true vs synthetic+noise vs init vs recovered
    ax[0, 0].plot(V_GRID, y_data, '.', color='0.7', ms=2.5, label=f"synthetic data (SNR={SNR:.0f})")
    ax[0, 0].plot(V_GRID, y_true, 'k-', lw=1.2, label="true curve (theta*)")
    ax[0, 0].plot(V_GRID, y_init, 'C0--', lw=1.0, label="initial guess (lit. table)")
    ax[0, 0].plot(V_GRID, y_fit, 'C3-', lw=1.0, label="recovered fit (theta^)")
    ax[0, 0].set_xlabel("V [V]"); ax[0, 0].set_ylabel("dQ/dV")
    ax[0, 0].set_title("(a) forward synthesis -> fit recovery")
    ax[0, 0].legend(fontsize=8)

    # (b) normalized residual after fit vs noise band
    res_n = (y_fit - y_data) / SCALE
    ax[0, 1].plot(V_GRID, res_n, 'C3-', lw=0.7, label="(fit - data)/peak")
    ax[0, 1].axhspan(-sigma / SCALE, sigma / SCALE, color='0.85',
                     label="noise +/-1 sigma")
    ax[0, 1].axhline(0.0, color='k', lw=0.5, ls=':')
    ax[0, 1].set_xlabel("V [V]"); ax[0, 1].set_ylabel("normalized residual")
    ax[0, 1].set_title("(b) residual at recovered theta^ (peak-max=1 scale)")
    ax[0, 1].legend(fontsize=8)

    # (c) convergence: running-min L vs eval, tier boundaries, gate & noise floor
    run_min = np.minimum.accumulate(np.asarray(_eval_log, dtype=float))
    ax[1, 0].semilogy(np.arange(1, run_min.size + 1), run_min, 'C0-', lw=1.2,
                      label="running-min loss L")
    for xe, lab, Lv in tier_marks:
        ax[1, 0].axvline(xe, color='0.6', lw=0.7, ls='--')
        ax[1, 0].text(xe, run_min.min() * 2.2, f"{lab}  L={Lv:.1e} ",
                      fontsize=7, va='bottom', ha='right', rotation=90)
    ax[1, 0].axhline(GATE_L, color='C3', ls='--', lw=0.9,
                     label="convergence gate 1e-4 (S6)")
    ax[1, 0].axhline(NOISE_FLOOR, color='C2', ls=':', lw=0.9,
                     label=f"noise floor (1/SNR)^2={NOISE_FLOOR:.1e}")
    ax[1, 0].set_xlabel("loss evaluations (cumulative)")
    ax[1, 0].set_ylabel("L = mean normalized residual^2")
    ax[1, 0].set_title("(c) convergence (staged opening: U -> +n -> +Q)")
    ax[1, 0].legend(fontsize=8)

    # (d) recovery error bars (all in %, centers scaled by thermal width RT/F)
    labels = ([f"U{j+1}" for j in range(N_TR)] + [f"n{j+1}" for j in range(N_TR)]
              + [f"Q{j+1}" for j in range(N_TR)])
    errs_pct = np.concatenate([np.abs(err_U_mV) / (W_TH * 1e3) * 100.0,
                               np.abs(err_n) * 100.0, np.abs(err_Q) * 100.0])
    colors = ['C0'] * N_TR + ['C1'] * N_TR + ['C2'] * N_TR
    ax[1, 1].bar(np.arange(errs_pct.size), errs_pct, color=colors)
    ax[1, 1].axhline(TOL_REL * 100.0, color='C3', ls='--', lw=0.9,
                     label=f"tolerance {TOL_REL*100:.0f}% (U: % of RT/F)")
    ax[1, 1].set_xticks(np.arange(errs_pct.size)); ax[1, 1].set_xticklabels(labels, fontsize=8)
    ax[1, 1].set_ylabel("|recovery error| [%]")
    ax[1, 1].set_title("(d) parameter recovery error (U scaled by RT/F=25.7 mV)")
    ax[1, 1].legend(fontsize=8)

    fig.suptitle(f"Anode_Fit v1.0.19 fitting round-trip: {'PASS' if all_pass else 'FAIL'}"
                 f"  (final L={L3:.2e}, gate 1e-4, noise floor {NOISE_FLOOR:.1e})",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(FIG, dpi=110)
    print(f"figure saved: {FIG}")
except Exception as exc:      # 그림은 부속 산출 — 실패해도 판정 자체는 유효
    print(f"[warn] figure generation skipped: {exc!r}")

sys.exit(0 if all_pass else 1)
