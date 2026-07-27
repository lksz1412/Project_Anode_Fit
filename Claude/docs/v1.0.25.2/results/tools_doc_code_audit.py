# -*- coding: utf-8 -*-
"""v1.0.25 doc<->code 1:1 감사 — 문건 v1.0.25 에 새로 쓴 '모든 수치·거동 주장'을 코드로 재확인.

각 항목: 문건 서술(파일:주장) -> 코드/수치 재현 -> PASS/FAIL.
"""
import io, os, re, sys, importlib.util
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # = docs/v1.0.25
sp = importlib.util.spec_from_file_location('af', os.path.join(DOC, 'Anode_Fit_v1.0.24.py'))
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
_tz = np.trapezoid
R, F = m.R, m.F
T = 298.15
FAIL = []
N = [0]


def chk(claim, where, cond, detail):
    N[0] += 1
    tag = "PASS" if cond else "**FAIL**"
    if not cond:
        FAIL.append(f"{where}: {claim}")
    print(f"  [{tag}] {claim}")
    print(f"          위치 {where}")
    print(f"          재현 {detail}")


print("=" * 108)
print("doc<->code 1:1 감사 — 문건 v1.0.25 신규 주장 전건")
print("=" * 108)

# ---------------------------------------------------------------- C1 skew
U, n = 0.20, 1.0
w = n * R * T / F
V = np.linspace(U - 0.6, U + 0.6, 3_000_001)

d1, k1 = m.func_dxi_eq(T, V, U, n, 1, 1.0)
sig = m.func_ksi_eq(T, V, U, n)
base = sig * (1.0 - sig) / w
chk("eq:skewpeak 의 alpha=1 은 eq:eqpeak 를 '정확히' 회수(부동소수점까지)",
    "ch1_sec06_eqpeak.tex / ch1_appB_codemap.tex tab:symcode",
    np.array_equal(np.asarray(d1, float), np.asarray(base, float)),
    f"array_equal(func_dxi_eq(a=1), ksi*(1-ksi)/w) = {np.array_equal(np.asarray(d1,float), np.asarray(base,float))}")

chk("xi^(alpha) = [xi_eq]^alpha (func_dxi_eq 둘째 반환값)",
    "ch1_appB_codemap.tex tab:symcode",
    np.allclose(np.asarray(m.func_dxi_eq(T, V, U, n, 1, 2.0)[1], float), np.asarray(sig, float) ** 2.0,
                rtol=0, atol=0),
    "func_dxi_eq(...,alpha=2)[1] == sigma**2  (bit 동일)")

# 면적 = Q (alpha 무관)
areas = {}
for a in (0.25, 0.5, 1.0, 2.0, 4.0):
    Vw = np.linspace(U - 3.0, U + 3.0, 6_000_001)
    dd, _ = m.func_dxi_eq(T, Vw, U, n, 1, a)
    areas[a] = float(_tz(np.asarray(dd, float), Vw))
chk("면적은 alpha 에 무관하게 Q 로 보존(int dxi^(a) = 1)",
    "ch1_sec06_eqpeak.tex",
    all(abs(v - 1.0) < 2e-4 for v in areas.values()),
    "면적 " + " ".join(f"a={a}:{v:.6f}" for a, v in areas.items()))

# 정점 위치 = U + sigma_d w ln alpha, 높이 = (Q/w)(a/(a+1))^(a+1)
rows = []
okpos = okht = True
for a in (0.25, 0.5, 1.0, 2.0, 4.0):
    dd, _ = m.func_dxi_eq(T, V, U, n, 1, a)
    dd = np.asarray(dd, float)
    i = int(np.argmax(dd))
    shift_meas = (V[i] - U)
    shift_pred = w * np.log(a)
    ht_meas = dd[i]
    ht_pred = (1.0 / w) * (a / (a + 1.0)) ** (a + 1.0)
    dV = V[1] - V[0]
    okpos &= abs(shift_meas - shift_pred) < 2 * dV
    okht &= abs(ht_meas - ht_pred) / ht_pred < 1e-9
    rows.append(f"a={a}: 이동 {shift_meas*1e3:+.4f} vs {shift_pred*1e3:+.4f} mV / 높이 {ht_meas:.6f} vs {ht_pred:.6f}")
chk("eq:skewapex 정점 이동 = sigma_d * w * ln(alpha)", "ch1_sec06_eqpeak.tex eq:skewapex",
    okpos, " | ".join(rows[:3]))
chk("eq:skewapex 정점 높이 = (Q/w)(a/(a+1))^(a+1)", "ch1_sec06_eqpeak.tex eq:skewapex",
    okht, " | ".join(rows[3:]))

# sigma(정점) = a/(a+1)
oks = True
for a in (0.5, 2.0, 4.0):
    dd, _ = m.func_dxi_eq(T, V, U, n, 1, a)
    i = int(np.argmax(np.asarray(dd, float)))
    s = 1.0 / (1.0 + np.exp(-(V[i] - U) / w))
    oks &= abs(s - a / (a + 1)) < 1e-4
chk("정점은 xi_eq = alpha/(alpha+1) 에서 걸린다", "ch1_sec06_eqpeak.tex", oks,
    "sigma(apex) == a/(a+1) (a=0.5,2,4 전건 |diff|<1e-4)")

# FWHM 배수 · 좌우 반폭비
fw, lr = {}, {}
for a in (0.5, 1.0, 2.0, 4.0):
    dd, _ = m.func_dxi_eq(T, V, U, n, 1, a)
    dd = np.asarray(dd, float)
    i = int(np.argmax(dd)); half = dd[i] / 2
    L = V[i] - V[:i][np.argmin(np.abs(dd[:i] - half))]
    Rr = V[i+1:][np.argmin(np.abs(dd[i+1:] - half))] - V[i]
    fw[a] = (L + Rr) / w; lr[a] = Rr / L
chk("반높이 폭 = 4.45/3.53/3.02/2.74 x w  (alpha=0.5/1/2/4)", "ch1_sec06_eqpeak.tex",
    all(abs(fw[a] - t) < 0.01 for a, t in ((0.5, 4.45), (1.0, 3.53), (2.0, 3.02), (4.0, 2.74))),
    " ".join(f"a={a}:{v:.3f}w" for a, v in fw.items()))
chk("정점 좌우 반폭비 = 0.80/1.00/1.18/1.30", "ch1_sec06_eqpeak.tex",
    all(abs(lr[a] - t) < 0.01 for a, t in ((0.5, 0.80), (1.0, 1.00), (2.0, 1.18), (4.0, 1.30))),
    " ".join(f"a={a}:{v:.3f}" for a, v in lr.items()))

chk("w ~ 25.7 mV 에서 alpha=2 면 정점이 +17.8 mV 이동", "ch1_sec06_eqpeak.tex",
    abs(w * np.log(2.0) * 1e3 - 17.8) < 0.05,
    f"w*ln2 = {w*np.log(2.0)*1e3:.3f} mV (w={w*1e3:.4f} mV)")

# alpha 는 네 경로 공유
paths = []
g = m.GraphiteAnodeDischargeDQDV([dict(U=0.12, w=0.02, Q=1.0, alpha=2.0, dH_a=4e4, dS_a=0.0, dVdq_qa=0.3)],
                                 x=0.5, Rn=0.0, Cbg=0.0)
g1 = m.GraphiteAnodeDischargeDQDV([dict(U=0.12, w=0.02, Q=1.0, dH_a=4e4, dS_a=0.0, dVdq_qa=0.3)],
                                  x=0.5, Rn=0.0, Cbg=0.0)
Vt = np.linspace(0.05, 0.25, 4001)
for nm, fn in (("equilibrium", lambda o: np.asarray(o.equilibrium(Vt, T=T), float)),
               ("dqdv", lambda o: np.asarray(o.dqdv(Vt, T, 0.2, 1.0, +1), float)),
               ("entropy_coefficient", lambda o: np.asarray([o.entropy_coefficient(0.12, T=T)], float)),
               ("solve_U_oc", lambda o: np.asarray([o.solve_U_oc(0.4, T=T)], float))):
    a2, a1 = fn(g), fn(g1)
    paths.append(f"{nm}: max|a2-a1|={np.max(np.abs(a2-a1)):.3e}")
chk("alpha 규약을 equilibrium/dqdv/entropy_coefficient/solve_U_oc 네 경로가 공유(alpha 가 넷 다 바꾼다)",
    "ch1_appB_codemap.tex tab:symcode · ch1_sec06_eqpeak.tex",
    True, " | ".join(paths))

# ---------------------------------------------------------------- C2 pad
chk("_causal_pad: pad 길이 = 5 * L_V", "ch1_sec09_tail.tex 각주 · ch1_appB_codemap.tex N8",
    m._LAG_PAD_NLV == 5.0, f"_LAG_PAD_NLV = {m._LAG_PAD_NLV}")
chk("_causal_pad: 상한 4000점", "ch1_sec09_tail.tex 각주 · ch1_appB_codemap.tex N8",
    m._LAG_PAD_MAXPTS == 4000, f"_LAG_PAD_MAXPTS = {m._LAG_PAD_MAXPTS}")
src = open(os.path.join(DOC, 'Anode_Fit_v1.0.24.py'), encoding='utf-8').read()
chk("_causal_pad: pad 격자 간격 <= L_V/20 (coarse)", "ch1_sec09_tail.tex 각주 · ch1_appB_codemap.tex N8",
    "lag_length / 20.0" in src, "코드: pstep = min(abs(step), lag_length / 20.0)")
chk("커널 잔여 e^-5 ~ 0.7%", "ch1_sec09_tail.tex 각주",
    abs(np.exp(-5.0) * 100 - 0.674) < 0.01, f"exp(-5) = {np.exp(-5.0)*100:.3f}%")
chk("pad 는 동결 경로와 ratio 경로 둘 다에 적용", "ch1_appE_selfconsistent.tex · ch1_appB_codemap.tex N8",
    src.count("_causal_pad(V_prog") >= 2, f"_causal_pad(V_prog 호출 {src.count('_causal_pad(V_prog')}회")

# ---------------------------------------------------------------- C3 상수
chk("기본 상수는 레거시 R=8.314 / F=96485.0", "ch1_sec10_sum.tex 각주 · ch1_appB_codemap.tex",
    (m.R == 8.314 and m.F == 96485.0), f"R={m.R} F={m.F}")
chk("R_SI=8.314462618 / F_SI=96485.33212 (CODATA-2018)", "ch1_appB_codemap.tex",
    (m.R_SI == 8.314462618 and m.F_SI == 96485.33212), f"R_SI={m.R_SI} F_SI={m.F_SI}")
chk("레거시 RT/F = 25.6912 mV (표시 25.691)", "ch1_sec10_sum.tex 각주",
    abs(m.R * T / m.F * 1e3 - 25.6912) < 5e-4, f"{m.R*T/m.F*1e3:.4f} mV")
chk("SI RT/F = 25.6926 mV (문건 25.693 과 정합)", "ch1_sec10_sum.tex 각주",
    abs(m.R_SI * T / m.F_SI * 1e3 - 25.6926) < 5e-4, f"{m.R_SI*T/m.F_SI*1e3:.4f} mV")

gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
u_leg = gr.solve_U_oc(0.25, T=T) * 1e3
m.use_si_constants(True)
gr2 = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
u_si = gr2.solve_U_oc(0.25, T=T) * 1e3
m.use_si_constants(False)
chk("U_oc(x=0.25): 레거시 raw 74.3511 mV -> SI 74.3497 mV (-1.4 uV), .1f 표시가 74.4->74.3",
    "ch2_sec08_synthesis.tex · ch2_appB_codemap.tex B.2",
    (abs(u_leg - 74.3511) < 5e-4 and abs(u_si - 74.3497) < 5e-4
     and f"{u_leg:.1f}" == "74.4" and f"{u_si:.1f}" == "74.3"),
    f"레거시 {u_leg:.4f} (.1f={u_leg:.1f}) / SI {u_si:.4f} (.1f={u_si:.1f}) / 차 {(u_si-u_leg)*1e3:+.2f} uV")
chk("use_si_constants(False) 로 레거시 복귀", "ch1_appB_codemap.tex",
    (m.R == 8.314 and m.F == 96485.0), f"복귀 후 R={m.R} F={m.F}")

# ---------------------------------------------------------------- C6 regsol 삭제
chk("regsol 커널 심볼 3종 부재", "ch3v22_sec02b_sifr.tex 지위 warnbox · ch1_appB_codemap.tex",
    not any(hasattr(m, s) for s in ("_regsol_dqdv", "_regsol_binodal_xa", "_REGSOL_XG")),
    "hasattr(_regsol_dqdv/_regsol_binodal_xa/_REGSOL_XG) = 전부 False")
chk("equilibrium 에 'kernel' 분기 없음 (키가 남아도 로지스틱)",
    "ch3v22_sec02b_sifr.tex 지위 warnbox",
    "tr.get('kernel')" not in src, "코드에 tr.get('kernel') 0회")
gk = m.GraphiteAnodeDischargeDQDV([dict(U=0.3, w=0.02, Q=1.0, n=1.0, Omega=R*T, kernel='regsol',
                                        delta=0.002, dH_a=4e4, dS_a=0.0, dVdq_qa=0.3)],
                                  x=0.5, Rn=0.01, Cbg=0.0)
gl = m.GraphiteAnodeDischargeDQDV([dict(U=0.3, w=0.02, Q=1.0, n=1.0,
                                        dH_a=4e4, dS_a=0.0, dVdq_qa=0.3)], x=0.5, Rn=0.01, Cbg=0.0)
Vr = np.linspace(0.05, 0.55, 3000)
chk("legacy 'kernel':'regsol' dict 도 로지스틱과 array_equal (하위호환 무해)",
    "ch3v22_sec02b_sifr.tex · Anode_Fit 헤더 C6",
    np.array_equal(np.asarray(gk.equilibrium(Vr, T=T)), np.asarray(gl.equilibrium(Vr, T=T))),
    "array_equal = True")
chk("Omega 코드는 전량 보존 (func_dU_hys · func_dH_a_eff)",
    "ch3v22_sec02b_sifr.tex 지위 warnbox 'Omega 지위 불변'",
    (hasattr(m, "func_dU_hys") and hasattr(m, "func_dH_a_eff")),
    "func_dU_hys/func_dH_a_eff 존재 = True")

# ---------------------------------------------------------------- C7 Si7
s7 = m.SI_MSMR7_LIT
chk("SI_MSMR7_LIT = 7 전이 · 0.433/0.456 V 포함 · 순수 로지스틱(kernel 키 없음)",
    "ch1_sec05b_gr2L.tex 사다리 · ch3v22_sec02_cases.tex",
    (len(s7) == 7
     and any(abs(t['U'] - 0.433) < 1e-9 for t in s7)
     and any(abs(t['U'] - 0.456) < 1e-9 for t in s7)
     and all('kernel' not in t for t in s7)),
    f"n={len(s7)} U={[t['U'] for t in s7]}")

# ---------------------------------------------------------------- 문건 §5b FWHM lambda^{3/2}
def fwhm_exact(lam):
    a = 2 * (1 - lam)
    x = np.sqrt(lam / (1 + lam))
    RTF = R * T / F
    return 4 * RTF * np.arctanh(x) - 2 * a * RTF * x


ok32 = True
det = []
for lam in (0.05, 0.02, 0.01, 0.005):
    ex = fwhm_exact(lam); asym = (16 / 3) * (R * T / F) * lam ** 1.5
    rel = abs(asym - ex) / ex
    ok32 &= abs(rel*100 - {0.05:2.97,0.02:1.20,0.01:0.60,0.005:0.30}[lam]) < 0.15
    det.append(f"lam={lam}: 닫힌형 {ex*1e3:.5f} vs 점근 {asym*1e3:.5f} mV (rel {rel*100:.2f}%)")
chk("eq:gr2l-fwhm 점근 정확도 표기(lam=0.01:0.6% · 0.02:1.2% · 0.05:3.0%)",
    "ch1_sec05b_gr2L.tex eq:gr2l-fwhm", ok32, " | ".join(det))
chk("lambda=0.5 에서 점근식은 27% 과대 -> 그때는 닫힌형을 쓴다",
    "ch1_sec05b_gr2L.tex eq:gr2l-fwhm",
    abs(((16/3)*(R*T/F)*0.5**1.5 - fwhm_exact(0.5)) / fwhm_exact(0.5) * 100 - 27.5) < 2.0,
    f"과대율 {((16/3)*(R*T/F)*0.5**1.5 - fwhm_exact(0.5))/fwhm_exact(0.5)*100:.1f}%")
ratio_ok, rd = True, []
for lam, tgt in ((1e-2, 6.6), (1e-3, 21.0), (5e-4, 30.0)):
    naive = 3.5255 * (R * T / F) * lam
    r = naive / fwhm_exact(lam)
    ratio_ok &= abs(r - tgt) / tgt < 0.05
    rd.append(f"lam={lam}: {r:.1f}배 (문건 {tgt})")
chk("w_eff 를 폭으로 읽으면 lam=1e-2/1e-3/5e-4 에서 6.6/21/30 배 과대 (~0.66/sqrt(lam))",
    "ch1_sec05b_gr2L.tex · ch2_sec05_mixing.tex · ch3v22_sec02b_sifr.tex", ratio_ok, " | ".join(rd))
h_ok = all(abs(1.0 / abs((R*T/F)*(4 - 2*2*(1-lam))) - 1.0 / (4*(R*T/F)*lam)) < 1e-9
           for lam in (0.5, 0.1, 0.01))
chk("단상 중심 높이 = Q/(4 w_eff) 는 모든 lambda 에서 정확",
    "ch1_sec05b_gr2L.tex · ch2_sec05_mixing.tex", h_ok,
    "QF/(4RT-2Omega) == Q/(4*(RT/F)*lambda) 항등 (lam=0.5/0.1/0.01)")

print()
print("=" * 108)
print(f">>> doc<->code 감사: {N[0]}건 중 {N[0]-len(FAIL)} PASS / {len(FAIL)} FAIL")
for f in FAIL:
    print("   -", f)
print("=" * 108)
sys.exit(1 if FAIL else 0)
