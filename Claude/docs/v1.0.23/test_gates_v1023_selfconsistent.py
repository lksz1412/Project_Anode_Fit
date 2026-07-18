# -*- coding: utf-8 -*-
"""v1.0.23 자기일관 해법(부록 E) 하드 게이트 — ratio 보정·전달함수 옵션 검증.

★ 기존 test_gates_v1023.py(G1/G2/G3/R6)와 별개. 저 파일이 lag_ratio_correction=False(기본)에서
   v1.0.19 bit-exact 를 이미 증빙(G1 max|d|=0) → 본 게이트는 신 옵션의 '정확성'만 검증한다.

G-E1  동결 회수: _causal_memory_ratio(g_eff=0) == _causal_memory_pointwise (부록 eq:sc-ratio 동결극한).
G-E2  dqdv bit-exact: g_eff=0 조건(Ω=0 / use_dH_eff=False)에서 ratio ON == OFF (np.array_equal).
G-E3  차수 이득(코드 자기참조 Picard): 1차 ratio = 코드 참 자기일관해로의 첫 Picard 스텝, err1<err0 & 수축.
G-E4  전달함수: transfer_apparent(H=1/(1+iωL_V)) 가 동결 인과 합성곱 peak 를 재현(균일 격자).
G-E5  liveness(발효): ratio ON(Ω>0)이 dqdv 를 실제로 바꾼다(무작동 아님).
"""
import numpy as np
import importlib.util

_s = importlib.util.spec_from_file_location("af1023", "Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(_s); _s.loader.exec_module(af)

R = af.R
PASS = []

def _logistic(V, Vc, w):
    z = (V - Vc) / w
    return np.where(z >= 0, 1.0/(1.0+np.exp(-z)), np.exp(z)/(1.0+np.exp(z)))

# ---------- G-E1 동결 회수 (g_eff=0) ----------
def g_e1():
    V = np.linspace(0.0, 0.3, 2000)
    xeq = _logistic(V, 0.15, 0.02)
    L0 = 0.01
    x0 = af._causal_memory_pointwise(V, xeq, L0)
    x1, Lloc = af._causal_memory_ratio(V, xeq, x0, L0, 0.0)
    d = float(np.max(np.abs(x1 - x0)))
    dL = float(np.max(np.abs(Lloc - L0)))
    ok = (d < 1e-14) and (dL == 0.0)
    print(f"G-E1 동결회수(g_eff=0): max|x1-x0|={d:.2e} (<1e-14), max|Lloc-L0|={dL:.1e}  {'PASS' if ok else 'FAIL'}")
    PASS.append(ok)

# ---------- G-E2 dqdv bit-exact (g_eff=0 두 경로) ----------
def g_e2():
    # L_V override 0.006(=L_V/w 0.3, 해상 regime)로 인과 경로를 실제 실행시켜 bit-exact 확인.
    base = [{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'dVdq_qa':0.30}]  # Ω 부재
    m_off = af.GraphiteAnodeDischargeDQDV(base)
    m_on  = af.GraphiteAnodeDischargeDQDV(base, lag_ratio_correction=True)
    V = np.linspace(0.05, 0.25, 600)
    a = m_off.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    b = m_on.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    ok_a = np.array_equal(a, b)
    # use_dH_eff=False + Ω>0 (게이트로 g_eff=0)
    base2 = [{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'Omega':8000.0,'dVdq_qa':0.30}]
    m_off2 = af.GraphiteAnodeDischargeDQDV(base2, use_dH_eff=False)
    m_on2  = af.GraphiteAnodeDischargeDQDV(base2, use_dH_eff=False, lag_ratio_correction=True)
    a2 = m_off2.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    b2 = m_on2.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    ok_b = np.array_equal(a2, b2)
    ok = ok_a and ok_b
    print(f"G-E2 dqdv bit-exact(g_eff=0): Ω부재 array_equal={ok_a}, use_dH_eff=False array_equal={ok_b}  {'PASS' if ok else 'FAIL'}")
    PASS.append(ok)

# ---------- G-E3 차수 이득 (코드 자기참조 Picard) ----------
def g_e3():
    # 참해 = 코드 _causal_memory_ratio 의 자기일관 고정점(ξ*=ratio(ξ*)) — Picard 수렴.
    # 1차 = 첫 스텝(기준=동결). err1<err0 & 수축률≈ε 면 코드가 부록 E 차수이득을 구현.
    V = np.linspace(-0.05, 0.30, 4000)
    xeq = _logistic(V, 0.10, 0.02); L0 = 0.006; w = 0.02
    chi_d = 0.5
    rows = []; allok = True
    for g in [0.0, 1.0, 2.0]:
        g_eff = 2.0*chi_d*g
        x0 = af._causal_memory_pointwise(V, xeq, L0)
        # 참 고정점: Picard 60회
        xk = x0.copy()
        for _ in range(60):
            xk, _ = af._causal_memory_ratio(V, xeq, xk, L0, g_eff)
        xstar = xk
        x1, _ = af._causal_memory_ratio(V, xeq, x0, L0, g_eff)
        e0 = float(np.max(np.abs(x0 - xstar)))
        e1 = float(np.max(np.abs(x1 - xstar)))
        eps = 2.0*chi_d*g*(L0/(4.0*w))
        improve = (e1 <= e0 + 1e-15)
        rows.append((g, eps, e0, e1, (e1/e0 if e0>0 else 0.0)))
        allok = allok and improve
    print("G-E3 차수이득(코드 Picard·참=고정점):")
    for g,eps,e0,e1,r in rows:
        print(f"   Ω/RT={g:.1f} ε={eps:.3e} err0={e0:.3e} err1={e1:.3e} err1/err0={r:.3f}")
    ok = allok and rows[0][2] < 1e-14 and rows[2][3] < rows[2][2]  # g=0 정확·g=2 개선
    print(f"   → err1≤err0 전부 & g=0 정확회수 & g=2 개선  {'PASS' if ok else 'FAIL'}")
    PASS.append(ok)

# ---------- G-E4 전달함수 (H filter vs 동결 합성곱) ----------
def g_e4():
    V = np.linspace(-0.4, 0.6, 4096); Vc=0.1; w=0.02; L0=0.01
    xeq = _logistic(V, Vc, w)
    peak_eq = xeq*(1.0-xeq)/w                      # dξ_eq/dV (평형 봉우리, L_V→0 극한)
    xlag = af._causal_memory_pointwise(V, xeq, L0)
    peak_frozen = (xeq - xlag)/L0                  # 동결 인과 합성곱 봉우리
    peak_H = af.transfer_apparent_from_equilibrium(V, peak_eq, L0)  # 전달함수 필터
    # 경계 평탄(0/0 잘 정의)한 내부창에서 비교
    m = (V > Vc-8*w) & (V < Vc+12*w)
    num = float(np.sqrt(np.mean((peak_H[m]-peak_frozen[m])**2)))
    den = float(np.max(np.abs(peak_frozen[m])))
    rel = num/den
    ok = rel < 1e-4   # 실측 ~4e-6 대비 ~25× 여유(회귀 감지력 확보; AUD-4 F-7)
    print(f"G-E4 전달함수 H=1/(1+iωL_V) vs 동결합성곱: rel RMS={rel:.2e} (<1e-4)  {'PASS' if ok else 'FAIL'}")
    PASS.append(ok)

# ---------- G-E5 liveness (발효) ----------
def g_e5():
    # L_V override 0.006(해상 regime)·Ω=8000·use_dH_eff 기본 True → g_eff≈3.2 → ratio 실작동.
    tr = [{'U':0.14,'w':0.02,'Q':0.12,'L_V':0.006,'Omega':8000.0,'dVdq_qa':0.30}]
    m_off = af.GraphiteAnodeDischargeDQDV(tr)                          # use_dH_eff 기본 True
    m_on  = af.GraphiteAnodeDischargeDQDV(tr, lag_ratio_correction=True)
    V = np.linspace(0.05, 0.25, 800)
    a = m_off.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    b = m_on.curve(V, 'discharge', c_rate=1.0, Q_cell=1.0)
    d = float(np.max(np.abs(a-b)))
    fin = bool(np.all(np.isfinite(b)))
    ok = (d > 1e-6) and fin
    print(f"G-E5 liveness(Ω>0·use_dH_eff): max|on-off|={d:.3e} (>1e-6) finite={fin}  {'PASS' if ok else 'FAIL'}")
    PASS.append(ok)

if __name__ == "__main__":
    print("="*74)
    g_e1(); g_e2(); g_e3(); g_e4(); g_e5()
    print("="*74)
    allok = all(PASS)
    print(f">>> SELF-CONSISTENT GATES: {'ALL PASS' if allok else 'FAIL'}  ({sum(PASS)}/{len(PASS)})")
    import sys; sys.exit(0 if allok else 1)
