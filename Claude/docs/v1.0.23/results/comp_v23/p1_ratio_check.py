# P1 조건검수 수치 검산 — lag ratio 1차 닫힘
# 목적: (a) 동결극한 회수 (Ω→0 ⇒ ξ1==ξ0==ξ*), (b) 오차 차수 (error_0~O(ε), error_1~O(ε²)),
#       (c) ε 부등식이 0차 오차 크기를 예측하는가.
# 근거식: ch1_sec08_lag.tex eq:lag  dξ_lag/dV=(ξ_eq−ξ_lag)/L_V,  L_V(ξ)=L_V0·exp[2χd(Ω/RT)(1−ξ)]
#   (동결 기준 ξ→1 에서 ρ=1; 유도: 상호작용 몫 −Ω(1−2ξ)의 동결값 +Ω 대비 편차).
import numpy as np

def xi_eq(V, Vc, w):
    return 1.0/(1.0+np.exp(-(V-Vc)/w))

def solve_linear(Vg, xeq, Lfield):
    # dξ/dV=(ξ_eq−ξ)/L(V) 전방적분(후진Euler로 안정). 인과: 낮은 V→높은 V.
    n=len(Vg); x=np.empty(n); x[0]=xeq[0]
    for i in range(1,n):
        h=Vg[i]-Vg[i-1]; L=Lfield[i]
        # 후진Euler: x_i = (x_{i-1}+h/L·xeq_i)/(1+h/L)
        a=h/L; x[i]=(x[i-1]+a*xeq[i])/(1.0+a)
    return x

def solve_true(Vg, xeq, L0, kchi, OmRT):
    # 비선형: L=L0·exp[2·kchi·OmRT·(1−ξ)] with ξ=현 미지. 후진Euler+국소 Picard.
    n=len(Vg); x=np.empty(n); x[0]=xeq[0]
    for i in range(1,n):
        h=Vg[i]-Vg[i-1]; xi=x[i-1]
        for _ in range(60):
            L=L0*np.exp(2.0*kchi*OmRT*(1.0-xi))
            a=h/L; xn=(x[i-1]+a*xeq[i])/(1.0+a)
            if abs(xn-xi)<1e-15: xi=xn; break
            xi=xn
        x[i]=xi
    return x

def rho(x, kchi, OmRT):
    return np.exp(2.0*kchi*OmRT*(1.0-x))

def run(OmRT, L0=0.01, w=0.02, kchi=0.5, Vc=0.10, span=0.12, N=4000):
    Vg=np.linspace(Vc-span, Vc+span, N)
    xeq=xi_eq(Vg, Vc, w)
    # 0차(동결 ρ≡1)
    x0=solve_linear(Vg, xeq, np.full(N, L0))
    # 참(비선형 자기일관)
    xt=solve_true(Vg, xeq, L0, kchi, OmRT)
    # 1차 보정: ρ를 0차 궤적에서 평가 → 변수계수 선형 재해
    Lref=L0*rho(x0, kchi, OmRT)
    x1=solve_linear(Vg, xeq, Lref)
    e0=np.max(np.abs(x0-xt)); e1=np.max(np.abs(x1-xt))
    # ε 부등식 (Δξ_supp=L0/(4w))
    eps=2.0*kchi*OmRT*(L0/(4.0*w))
    return eps, e0, e1

print(f"{'Ω/RT':>6} {'ε':>10} {'err_0':>12} {'err_1':>12} {'err1/err0':>10} {'err0/ε':>10}")
prev=None
for OmRT in [0.0, 0.25, 0.5, 1.0, 2.0]:
    eps,e0,e1=run(OmRT)
    r=(e1/e0) if e0>0 else 0.0
    q=(e0/eps) if eps>0 else 0.0
    print(f"{OmRT:6.2f} {eps:10.4e} {e0:12.4e} {e1:12.4e} {r:10.4f} {q:10.4e}")

# 차수 확인: ε 반감 시 err_0 반감(1차)·err_1 1/4(2차)?
print("\n[차수 스케일링: L0 를 반씩 줄여 ε↓, 오차 차수 관찰]")
print(f"{'ε':>10} {'err_0':>12} {'err_1':>12} {'e0비':>8} {'e1비':>8}")
pe0=pe1=None
for L0 in [0.02,0.01,0.005,0.0025]:
    eps,e0,e1=run(1.0, L0=L0)
    b0=(pe0/e0) if pe0 else 0.0; b1=(pe1/e1) if pe1 else 0.0
    print(f"{eps:10.4e} {e0:12.4e} {e1:12.4e} {b0:8.3f} {b1:8.3f}")
    pe0,pe1=e0,e1
print("(ε 반감→ err_0비≈2[1차], err_1비≈4[2차] 이면 닫힘 차수 확증)")
