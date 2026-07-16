# eval_ff1_coords.py — FF1 그림 좌표 생성 (문서 본문 식 그대로의 수치 평가)
# 사용 식: eq:dUhys, eq:lco-dope(극한), eq:Acut/eq:chid/eq:dHeff/eq:Lqfull/eq:LV,
#          eq:implicit/eq:weighted/eq:complete(+tab:staging·tab:ds 초기값),
#          eq:app-fxi 미분(=Maxwell loop), eq:app-cnt/eq:app-rstar, eq:app-ch-R,
#          eq:Svib-einstein/eq:dSvib/eq:dUvib, eq:lag(기억 적분).
import math

R = 8.314462618        # J/(mol K)
F = 96485.33212        # C/mol
kB = 1.380649e-23      # J/K
h = 6.62607015e-34     # J s

def fmt(pairs, nd=4, per=8):
    out, line = [], []
    for x, y in pairs:
        line.append(f"({round(x,nd):g},{round(y,nd):g})")
        if len(line) == per:
            out.append(" ".join(line)); line = []
    if line: out.append(" ".join(line))
    return "\n".join(out)

OUT = []
def sec(t): OUT.append("\n%% ===== " + t + " =====")

# ---------------------------------------------------------------- P1(a)
sec("P1a gap dimensionless: y=2[w u - 2 artanh u], u=sqrt(1-2/w)  (eq:dUhys)")
def gap_dimless(w):
    if w <= 2: return 0.0
    u = math.sqrt(1 - 2.0/w)
    return 2*(w*u - 2*math.atanh(u))
ws = [2.0,2.02,2.05,2.1,2.2,2.35,2.5,2.75,3.0,3.25,3.5,3.75,4.0,4.5,5.0,5.5,6.0]
OUT.append("exact:");  OUT.append(fmt([(w, gap_dimless(w)) for w in ws]))
def u_of(w): return math.sqrt(max(0.0,1-2.0/w))
OUT.append("approx (8/3)u^3:")
OUT.append(fmt([(w, (8.0/3.0)*u_of(w)**3) for w in ws if w<=3.5]))
OUT.append("wrong -(4/3)u^3:")
OUT.append(fmt([(w, -(4.0/3.0)*u_of(w)**3) for w in ws if w<=3.5]))
for w in (3.0,4.0):
    OUT.append(f"marker w={w}: y={gap_dimless(w):.4f}")

# ---------------------------------------------------------------- P1(b)
sec("P1b gap vs T [mV] for Omega=6000/8000/10000/13000 (tab:staging), Tc=Omega/2R")
def gap_mV(Om, T):
    x = 2*R*T/Om
    if x >= 1: return 0.0
    u = math.sqrt(1-x)
    return (2.0/F)*(Om*u - 2*R*T*math.atanh(u))*1e3
for Om in (6000,8000,10000,13000):
    Tc = Om/(2*R)
    Ts = [240+10*i for i in range(int((Tc-240)//10)+1)]
    # 조밀 근방 (Tc 부근 연성 소멸 형태)
    Ts += [Tc-15, Tc-8, Tc-4, Tc-1.5, Tc-0.3]
    Ts = sorted(t for t in set(round(t,2) for t in Ts) if 240 <= t <= Tc)
    OUT.append(f"Omega={Om}  Tc={Tc:.1f} K  gap(298.15K)={gap_mV(Om,298.15):.2f} mV")
    OUT.append(fmt([(t, gap_mV(Om,t)) for t in Ts], nd=3))

# ---------------------------------------------------------------- P2
sec("P2 lag length: log10(L_V [V]) vs T; eq:Lqfull + eq:LV")
def L_V(T, dHa, crate, dVdq=0.30, Om=13000.0, chi=0.5, dSa=0.0,
        zcut=4.357, Acap=4.0, n=1.0):
    A = min(zcut*n*R*T, Acap*R*T)          # eq:Acut
    dHeff = dHa - chi*Om                    # eq:dHeff (chi_d=chi, discharge)
    Tstar = crate*h/kB                      # T* = |I| h/(Q_cell kB), Q_cell=1, §10 규약
    Lq = (Tstar/T)*math.exp((dHeff - T*dSa)/(R*T))/(1+math.exp(-A/(R*T)))*math.exp(-chi*A/(R*T))
    return dVdq*Lq                          # eq:LV
Ts = [260+5*i for i in range(17)]
for dHa, crate, tag in ((40000,0.1,"dHa=40k C/10"),(48000,0.1,"dHa=48k C/10"),
                        (60000,0.1,"dHa=60k C/10"),(80000,0.1,"dHa=80k C/10"),
                        (80000,1.0,"dHa=80k C/1")):
    OUT.append(tag + f"   L_V(298.15)={L_V(298.15,dHa,crate):.3e} V")
    OUT.append(fmt([(t, math.log10(L_V(t,dHa,crate))) for t in Ts], nd=3))
OUT.append("w band: log10(RT/F) at 260K=%.3f  298.15K=%.3f  340K=%.3f" %
           (math.log10(R*260/F), math.log10(R*298.15/F), math.log10(R*340/F)))

# ---------------------------------------------------------------- P3
sec("P3 blend: dU_oc/dT(xbar) full & simple [mV/K]; eq:implicit/weighted/complete")
T0 = 298.15
w0 = R*T0/F
dH = [-11700.0,-13500.0,-13100.0,-13000.0]
dS = [29.0,0.0,-5.0,-16.0]
Qj = [0.10,0.12,0.25,0.50]
Uj = [(-dH[j]+T0*dS[j])/F for j in range(4)]
Qtot = sum(Qj)
OUT.append("U_j(298.15) [V]: " + " ".join(f"{u:.6f}" for u in Uj))
def xi(U, j, T=T0):
    w = R*T/F
    Ujt = (-dH[j]+T*dS[j])/F
    z = (U-Ujt)/w
    if z >= 0: return 1.0/(1.0+math.exp(-z))
    e = math.exp(z); return e/(1.0+e)
def Uoc(xbar, T=T0):
    lo, hi = -0.15, 0.45
    for _ in range(90):
        mid = 0.5*(lo+hi)
        s = sum(Qj[j]*xi(mid,j,T) for j in range(4))
        if s < Qtot*xbar: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
def dUdT(xbar, full=True, T=T0):
    U = Uoc(xbar, T); w = R*T/F
    num = den = 0.0
    for j in range(4):
        xj = xi(U,j,T); gj = xj*(1-xj)/w
        term = dS[j]/F
        if full:
            zj = (U - (-dH[j]+T*dS[j])/F)/w
            term += (R/F)*zj
        num += Qj[j]*gj*term; den += Qj[j]*gj
    return num/den*1e3   # mV/K
chk = [(0.10,), (0.25,), (0.50,), (0.75,), (0.90,)]
OUT.append("check vs tab:qrev  (xbar, U_oc mV, full mV/K, simple mV/K):")
for (xb,) in chk:
    OUT.append(f"  {xb:.2f}  {Uoc(xb)*1e3:7.1f}  {dUdT(xb,True):+.3f}  {dUdT(xb,False):+.3f}")
xs = [0.02,0.04,0.06,0.08,0.10,0.13,0.16,0.19,0.22,0.25,0.28,0.31,0.34,0.37,0.40,
      0.43,0.46,0.49,0.52,0.55,0.58,0.61,0.64,0.67,0.70,0.73,0.76,0.79,0.82,0.85,
      0.88,0.90,0.92,0.94,0.96,0.98]
OUT.append("full:");   OUT.append(fmt([(x, dUdT(x,True))  for x in xs]))
OUT.append("simple:"); OUT.append(fmt([(x, dUdT(x,False)) for x in xs]))
# 계단(오답) 대조용: 전이 지배 구간 경계 = 누적 용량 분율
cum = []
s = 0.0
for j in (3,2,1,0):   # 탈리튬화 진행 = 2->1 부터
    s += Qj[j]/Qtot; cum.append(s)
OUT.append("step boundaries (xbar, cumulative Q of 2->1,2L->2,3->2L): " +
           " ".join(f"{c:.4f}" for c in cum))
OUT.append("levels dS0/F [mV/K]: " + " ".join(f"{d/F*1e3:+.3f}" for d in dS))

# ---------------------------------------------------------------- P4
sec("P4 Maxwell loop: mu(xi)/RT = ln[xi/(1-xi)] + 3(1-2xi)  (Omega=3RT)")
def mu3(x): return math.log(x/(1-x)) + 3*(1-2*x)
xs4 = [0.02,0.035,0.0707,0.10,0.13,0.16,0.19,0.2113,0.24,0.28,0.32,0.36,0.40,0.45,
       0.50,0.55,0.60,0.64,0.68,0.72,0.7887,0.84,0.87,0.90,0.9293,0.965,0.98]
OUT.append(fmt([(x, mu3(x)) for x in xs4]))
OUT.append(f"extrema mu(0.2113)={mu3(0.2113):+.4f}  mu(0.7887)={mu3(0.7887):+.4f}")
OUT.append(f"binodal check mu(0.0707)={mu3(0.0707):+.5f} mu(0.9293)={mu3(0.9293):+.5f}")
# 등면적 수치(위쪽): ∫[xi_b^-,1/2] mu dξ
n = 4000; a, b = 0.070696, 0.5
sA = sum(mu3(a+(b-a)*(i+0.5)/n) for i in range(n))*(b-a)/n
OUT.append(f"upper area = {sA:.5f} RT (아래쪽 = 대칭으로 동일)")
# 상세 근: mu=0 outer roots
def bis(f, lo, hi):
    for _ in range(80):
        m = 0.5*(lo+hi)
        if f(lo)*f(m) <= 0: hi = m
        else: lo = m
    return 0.5*(lo+hi)
r1 = bis(mu3, 0.01, 0.15); OUT.append(f"binodal root refine: {r1:.6f} / {1-r1:.6f}")

# ---------------------------------------------------------------- P5
sec("P5a nucleation: y=3s^2-2s^3 (total), 3s^2 (surface), -2s^3 (volume)")
ss = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9]
OUT.append("total:");   OUT.append(fmt([(s, 3*s*s-2*s**3) for s in ss]))
OUT.append("surface:"); OUT.append(fmt([(s, 3*s*s) for s in ss if 3*s*s<=3.6]))
OUT.append("volume:");  OUT.append(fmt([(s, -2*s**3) for s in ss if -2*s**3>=-2.9]))
sec("P5b spinodal growth: R/(M|f''|k_c^2): growth k^2(1-k^2), decay -k^2(1+k^2)")
ks = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7071,0.8,0.9,1.0,1.1,1.2,1.3]
OUT.append("growth:"); OUT.append(fmt([(k, k*k*(1-k*k)) for k in ks]))
OUT.append("decay:");  OUT.append(fmt([(k, -k*k*(1+k*k)) for k in ks if k*k*(1+k*k)<=1.05]))

# ---------------------------------------------------------------- P6
sec("P6a S_vib(T;thetaE)/R (eq:Svib-einstein), thetaE=400/700/1000")
def SvibR(T, thE):
    u = thE/T
    return -math.log(1-math.exp(-u)) + u/(math.expm1(u))
Ts6 = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,430,460,500]
for thE in (400,700,1000):
    OUT.append(f"thetaE={thE}:")
    OUT.append(fmt([(t, SvibR(t,thE)) for t in Ts6]))
OUT.append("classical 1+ln(T/700) (T>=300):")
OUT.append(fmt([(t, 1+math.log(t/700.0)) for t in Ts6 if t>=300]))
sec("P6b dDeltaU_vib/dT = [S_vib(T)-S_vib(Tref)]/F [uV/K], thetaE=700, Tref=298.15")
def dUvib_slope_uV(T, thE=700.0, Tref=298.15):
    return (SvibR(T,thE)-SvibR(Tref,thE))*R/F*1e6
Ts6b = [258,266,274,278.15,282,290,298.15,306,314,318.15,322,330,338,348.15,356]
OUT.append(fmt([(t, dUvib_slope_uV(t)) for t in Ts6b], nd=3))
OUT.append("anchor: " + "  ".join(f"{t}K:{dUvib_slope_uV(t):+.2f}"
            for t in (278.15,298.15,318.15,348.15)))
# electronic 대조 직선(함수형 대조용 정규화: 348.15 K 에서 vib 값과 일치시키는 선형 aT)
aT = dUvib_slope_uV(348.15)/348.15
OUT.append(f"electronic-shape line slope a={aT:.5f} uV/K^2 -> y=a*T; "
           f"y(260)={aT*260:.2f} y(298.15)={aT*298.15:.2f} y(356)={aT*356:.2f}")

# ---------------------------------------------------------------- P7
sec("P7 memory integral (eq:lag, q-axis): xi_eq=logistic((q-1.2)/0.25), L_q=0.4")
Lq, qc, wq = 0.4, 1.2, 0.25
def xieq_q(q): return 1.0/(1.0+math.exp(-(q-qc)/wq))
def xilag_q(q, n=8000, span=14.0):
    # xi_lag(q) = (1/L)∫_{-inf}^{q} xi_eq(u) e^{-(q-u)/L} du,  u=q-L t 치환 후 t∈[0,span]
    s = 0.0; dt = span/n
    for i in range(n):
        t = (i+0.5)*dt
        s += xieq_q(q-Lq*t)*math.exp(-t)
    return s*dt
qs = [0.0,0.2,0.4,0.6,0.8,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2]
OUT.append("xi_eq:");  OUT.append(fmt([(q, xieq_q(q)) for q in qs]))
OUT.append("xi_lag:"); OUT.append(fmt([(q, xilag_q(q)) for q in qs]))
OUT.append("r/L_q (peak shape):")
OUT.append(fmt([(q, (xieq_q(q)-xilag_q(q))/Lq) for q in qs]))
pk_q = max(qs, key=lambda q:(xieq_q(q)-xilag_q(q))/Lq)
# 세밀 탐색
grid = [1.2+0.02*i for i in range(0,41)]
vals = [((xieq_q(q)-xilag_q(q))/Lq, q) for q in grid]
OUT.append("peak of r/L_q: %.4f at q=%.3f" % max(vals))

print("\n".join(OUT))
