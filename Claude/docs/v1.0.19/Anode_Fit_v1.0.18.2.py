# -*- coding: utf-8 -*-
# ============================================================================
# ★ Anode_Fit  release 버전 = 1.0.16  — 문건 Ch1/Ch2 1.0.16 와 동일 버전·matched
#   (구현 계보: v11_final → use_w_eff 제거 → 1.0.10 → 1.0.12 → 1.0.13 → 1.0.14 → 1.0.15 → 1.0.16. 코드·문건 버전 통일.
#    1.0.13 = 통계역학-first 재구조화(Part 0/I/II) 동반판. 1.0.14 = 어투·엄밀성·Appendix 개정 동반판(물리 로직 승계). 1.0.15 = 이산 격자 퇴출·점별 연속 아키텍처. 1.0.16 = 폭 다중도 n 의 온도 함수 n(T) 피팅 지원·가역열 config 항 ∂w/∂T 전파[증판 시점 v1.0.15 승계].)
# ----------------------------------------------------------------------------
# Anode_Fit 흑연 음극 dQ/dV 물리 구현 — 1.0.16 (v11_final 기반 계보, 2026-07-06)
#   [1.0.10 변경] use_w_eff 경로 제거: ξ_eq 폭·분모 w 불일치로 면적보존 깨짐(버그) — w=자유 피팅 파라미터만.
#   [폭 정합 주의] 전이 폭 w=nRT/F (_n_factor: 'n' 우선 → 없으면 'w' 역산 → 없으면 n=1).
#     GRAPHITE_STAGING_LIT 는 'n':1.0 보유 → 기본 폭=RT/F≈25.7mV(298K); 'w' 폴백(0.012 등)은
#     'n' 존재 시 inert. 문건 "w=현상학적 자유 피팅"의 피팅 핸들=n(또는 'n' 제거 시 'w').
#     dQ/dV 개형 = 정상 종(면적 보존; plot_dqdv.py 실증).
# ============================================================================
# Anode_Fit 흑연 음극 dQ/dV 물리 구현 — v11_final (체리픽 통합 + 재검수·보완 최종, 2026-06-29)
#   v10(체리픽 통합본) 을 adversarial 재검수 후 보완한 최종본(20번째 산출).
#   재검수 정리: func_U_branch 활성화(인라인 중복 제거)·死변수 U_j_rep 제거·
#   v_span_floor 인자화 + per-transition override 격리 self-test 추가(회귀 가드).
#   9건 독립 구현 → 보완(9b) → 2회 검토를 거쳐 master(Opus)가 보완본들의 장점만
#   체리픽한 10번째 통합본. 베이스 = v04b(6차원 무결함). 추가 흡수:
#     · 남은 매직넘버 전부 인자화(grid_pad_lo/hi·n_work_min·min_lag_grid_steps)
#     · per-transition override(z_cut·A_cap_RT·use_dH_eff) — "모든 인자 입력" 완성
#   v04b 의 χ_d 주입·가드·facade·D1·충전부호·원형보존·포괄검증은 그대로 계승.
#   (이식금지였던 v09b −σ_d 부호회귀·v08b func 적출/gamma 무조건주입은 채택 안 함.)
#   ─────────────────────────────────────────────────────────────────────────
#   v04_opus(6차원 무결함 골격)의 1차 보완본. 충·방전 부호·인자 완전노출·원형
#   보존·비변조·clean 을 그대로 유지하면서 4가지 강점을 흡수한다(별도 사본; v04 보존):
#     (A) 교체 가능한 χ_d 규칙 : 방향별 전달계수 χ_d 를 고정 분기 대신 주입 가능한
#         callable(chi_split)로 노출 — 히스/χ_d 규칙 사용자 교체(기본 = func_chi_d).
#     (B) 매직넘버 hoist + 유한 가드 : z_cut·A_cap_RT 등 남은 상수를 named 인자로
#         확정·검증하고, 비유한/음수 입력(T·I·Q_cell·dict 값)을 막는 가드를 둔다.
#     (C) 편의 facade : curve(q|sto, 방향, C-rate, Q_cell, T) — 실험조건으로 바로 호출
#         (내부는 기존 dqdv 재사용; C-rate→|I|·방향 문자열→σ_d 환산만).
#     (D) D1(ΔH_a^eff) 응집 : 분산됐던 χ_d·ΔH_a^eff 산출을 단일 헬퍼로 모음.
#
#   [보존] 사용자 원형 함수 그대로(보완·노출만):
#     func_w · func_U_j · func_ksi_eq · func_L_q · GRAPHITE_STAGING_LIT.
#
#   [근거 문건] graphite_ica_ch1_v1.0.16.tex(+ch2) — 커브식 명세(계보 원천 Opus_v6). 본 구현이 따르는 식:
#     · 분극        V_n = V_app − σ_d|I|R_n                         (eq:vn)
#     · 평형 중심   U_j(T) = (−ΔH_rxn + TΔS_rxn)/F                  (eq:Uj/func_U_j)
#     · 히스 gap    ΔU_hys = (2/F)[Ωu − 2RT·artanh u], u=√(1−2RT/Ω) (eq:dUhys)
#     · 분기 중심   U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_hys                (eq:Ubranch)
#     · 폭          w = nRT/F  — 두-상 전이에선 현상학적 자유 피팅 폭  (eq:wbase/func_w)
#     · 평형 진행률 ξ_eq = logistic[ s(V_n−U)/w ]                   (eq:xieq/func_ksi_eq)
#     · 평형 peak   Q_j·ξ_eq(1−ξ_eq)/w  (방향 불변)                 (eq:eqpeak/eq:belliden)
#     · 전달계수    χ_d = χ(방전) / 1−χ(충전)  (callable 교체 가능)  (eq:chid)
#     · 지연 길이   L_q = (|I|h/Q_cell kB T)·e^{(ΔH_a^eff−TΔS_a−χ_d A)/RT}/(1+e^{−A/RT})
#                   L_V = |dV_n/dq|_qa · L_q                        (eq:Lqfull/eq:LV/func_L_q)
#     · 유효장벽    ΔH_a^eff = ΔH_a − χ_d·Ω                         (eq:dHeff)
#     · 꼬리        인과 지수기억 (eq:memory 합성곱) — σ_d 방향                (eq:peakshape)
#     · 합산        dQ/dV = C_bg + Σ_j Q_j[ 평형 peak − 지연 꼬리 ]   (eq:sum)
#
#   [v04 → v04b 변경 요약]
#     (A) func_chi_d 모듈 함수 신설 + 생성자 chi_split: Callable[[float,int],float]
#         주입(기본 func_chi_d). _chi_d 가 이를 호출 — 기본 동작 불변, 규칙 교체 가능.
#     (B) __init__ 가드 : chi/z_cut/A_cap_RT/seed_* 유한·범위 검증(_finite_pos 등).
#         dqdv·_resolve_lag_length·_build_seed_L_V : T·I·Q_cell·dict 값 유한·음수 가드.
#     (C) curve(...) facade : C-rate·방향문자열·sto→실험조건 → 내부 dqdv 재사용.
#     (D) _chi_and_dH_eff(tr, σ_d) 단일 헬퍼로 χ_d·ΔH_a^eff 응집(_resolve_lag_length 정리).
# ============================================================================
from __future__ import annotations
import numpy as np
from typing import Dict, Any, List, Union, Callable, Optional, Tuple

R  = 8.314
F  = 96485.0
kB = 1.380649e-23
h  = 6.62607015e-34

# 수치 해상 가드(D6): 지수 기억 커널이 한 격자 간격 안에서 e^{−a} 로 완전히 소진되는
#   (a=char_h/L_V > 이 상한) 미해상 영역에서만 (ξ_eq−ξ_lag)/L_V 가 0/0 로 불안정하다 →
#   그 영역은 평형 종(L_V→0 해석적 극한, Ch1 eq:tail-limit)을 직접 쓴다. 이 상한에서
#   기억식(유한차분 Δξ/h)과 평형 종이 이미 일치하므로 불연속이 없다. 물리 분기가 아니라
#   부동소수 안전장치 — 해상 가능한 꼬리는 격자 밀도와 무관하게 항상 기억식으로 계산한다.
_LAG_RESOLVE_DECAY_CAP = 40.0

ScalarOrArray = Union[float, np.ndarray]


# ===== 사용자 원형 보존(추출본 그대로 — 1바이트도 변조 X) =====================
def func_w(T: ScalarOrArray, n: float = 1.0) -> ScalarOrArray:
    return n * R * T / F


def func_U_j(T: ScalarOrArray, dH_rxn: float, dS_rxn: float) -> ScalarOrArray:
    return (-dH_rxn + T * dS_rxn) / F


def func_ksi_eq(T: ScalarOrArray, V_n: ScalarOrArray, U: ScalarOrArray,
                n: float = 1.0, s: int = 1) -> ScalarOrArray:
    z = s * (V_n - U) / func_w(T, n)
    return np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z)))


def func_L_q(T: float, I: float, Q_cell: float, dH_a: float, dS_a: float,
             x: float, A: float) -> float:
    if I <= 0:
        return -np.inf
    T_attempt = (I / Q_cell) * h / kB
    dG_a = dH_a - T * dS_a
    ln_Lq = np.log(T_attempt / T) - np.log(1.0 + np.exp(-A / (R * T))) + dG_a / (R * T) - x * A / (R * T)
    return np.exp(ln_Lq)


def _causal_memory_pointwise(V_prog: np.ndarray,
                             ksi_eq: np.ndarray,
                             lag_length: float) -> np.ndarray:
    """인과 기억 적분 ξ_lag(V)=(1/L_V)∫ ξ_eq(u) e^{−(V−u)/L_V} du 의 점별 평가(Ch1 eq:lag).

    V_prog : 진행 방향으로 정렬된 내부 전위(방전 오름차순·충전 내림차순, eq:reversal).
    ksi_eq : 같은 순서의 평형 진행률.
    반환   : 같은 순서의 지연 진행률 ξ_lag.

    지수 커널을 구간 [i−1,i] 마다 정확 적분(ξ_eq 구간 선형 가정)한다 — 균일 작업 격자·
    리샘플 없이 임의 간격의 입력점에서 직접 성립. 간격 h=|ΔV|, a=h/L_V, e=e^{−a} 에서
        seg = ξ_i(1−e) − (Δξ/a)(1−(1+a)e),   ξ_lag[i] = e·ξ_lag[i−1] + seg
    (a→0 = 사다리꼴 평균 = 연속 완화 dξ_lag/dV=(ξ_eq−ξ_lag)/L_V; a→∞ = Δξ/h 유한차분
    도함수 = 평형 종으로 매끈히 수렴.)
    """
    n = ksi_eq.size
    out = np.empty(n, dtype=float)
    out[0] = float(ksi_eq[0])  # 진행 시작 이전 ξ_eq 상수 근사(하한 자연경계 −∞)
    for i in range(1, n):
        h = abs(float(V_prog[i] - V_prog[i - 1]))
        a = h / lag_length
        if a < 1e-4:  # 조밀 구간: 사다리꼴 극한(seg 둘째항 파괴적 상쇄·언더플로 회피)
            out[i] = (1.0 - a) * out[i - 1] + a * 0.5 * (float(ksi_eq[i]) + float(ksi_eq[i - 1]))
        else:
            e = float(np.exp(-a))
            dksi = float(ksi_eq[i]) - float(ksi_eq[i - 1])
            seg = float(ksi_eq[i]) * (1.0 - e) - (dksi / a) * (1.0 - (1.0 + a) * e)
            out[i] = e * out[i - 1] + seg
    return out
# ===========================================================================


# ===== 보완: 분기 중심·유효폭·유효장벽·전달계수 — 인자 전부 노출 ===============
def func_dU_hys(T: float, Omega: float) -> float:
    """spinodal 상한 분기 gap ΔU_hys [V] (eq:dUhys).
    Ω≤2RT 면 0(제곱근 NaN 영역 명시 분기). Ω 만 인자(하드코딩 없음)."""
    two_RT = 2.0 * R * T
    if Omega <= two_RT:
        return 0.0
    u = np.sqrt(1.0 - two_RT / Omega)
    return float((2.0 / F) * (Omega * u - two_RT * np.arctanh(u)))


def func_U_branch(T: float, U_j: float, Omega: float, gamma: float,
                  sigma_d: int, h_eta: float = 1.0) -> float:
    """분기 중심 U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_hys (eq:Ubranch).
    partial_hys 를 h_eta(부분 cycle 인자, 기본 1.0)로 노출 — 하드코딩 제거."""
    return float(U_j + 0.5 * sigma_d * h_eta * gamma * func_dU_hys(T, Omega))



def func_dH_a_eff(dH_a: float, Omega: float, chi_d: float) -> float:
    """유효 활성화 엔탈피 ΔH_a^eff = ΔH_a − χ_d·Ω (eq:dHeff).
    깊은 꼬리에서 상호작용 상수 몫 +Ω 가 장벽에 흡수. 방향별(χ_d)."""
    return float(dH_a - chi_d * Omega)


def func_chi_d(chi: float, sigma_d: int) -> float:
    """방향별 전달계수 χ_d (eq:chid 합-1): 방전(σ_d≥0) χ_d=χ, 충전 χ_d=1−χ.
    꼬리 깊은 쪽 거울 대칭(방전 ξ→1 / 충전 ξ→0)으로 역방향 장벽 상수몫이 갈린다.
    ★기본 규칙 — 생성자 chi_split 인자에 다른 callable 을 주입해 교체 가능
       (예: 비대칭 분배, 부분 cycle 보정 규칙). 시그니처 = (chi, sigma_d)->χ_d."""
    return chi if sigma_d >= 0 else (1.0 - chi)


# ===== LCO 양극 확장: 전자 엔트로피(MIT) — Ch1 sec:lco-Se, eq:dSegate =============
EV_TO_J = 1.602176634e-19  # eV→J 다리 (elementary charge; eq:gunit: g_J = g_eV / e_V)


def func_dSe_molar(x: ScalarOrArray, T: float,
                   g_max_eV: float, x_MIT: float, dx_MIT: float) -> ScalarOrArray:
    """부분몰 전자 엔트로피 ΔS_e(x,T) [J/(mol·K)] — MIT 게이트형(Ch1 eq:dSegate;
    몰당 환산·게이트 대입형은 eq:dSemolar·eq:ggate).

    금속-절연체 전이(MIT) 창 안에서 상태밀도 g(E_F) 가 급변하며 부분몰 전자 엔트로피가
    골(음의 피크)을 이룬다. σ=1/(1+exp(−(x−x_MIT)/dx_MIT)) 로 창을 열고 σ(1−σ) 게이트:
        ΔS_e = −(π²/3)·R·(k_B·T/e_V)·(g_max_eV/dx_MIT)·σ(1−σ)
    ★단위 3중 가드: 부호 leading −(삽입 시 g 감소, Ch1 규약 ΔS_e<0) · ÷e_V(eV⁻¹→J⁻¹,
      곱하면 ~4e37배 오류) · 몰당 R·k_B(자리당 k_B² 아님; N_A k_B²=R k_B). 검산:
      g_max_eV=13·dx_MIT=0.05·T=298 → 골 깊이 ≈ −45.7 J/mol/K (Ch1 검증값 −46 정합).
    x-의존 골이나 U_j(T) 온도이동에만 작용(면적·폭 불변, Ch1 sec:lco-decomp).
    """
    z = (np.asarray(x, dtype=float) - x_MIT) / dx_MIT
    sig = 1.0 / (1.0 + np.exp(-z))
    gate = sig * (1.0 - sig)
    return -(np.pi**2 / 3.0) * R * (kB * T / EV_TO_J) * (g_max_eV / dx_MIT) * gate


# --- (B) 입력 가드 헬퍼 — 비유한/음수 차단(named, 작은 단위) ------------------
def _finite(name: str, value: float) -> float:
    """유한성 가드. NaN/±inf 면 ValueError(메시지에 인자명)."""
    v = float(value)
    if not np.isfinite(v):
        raise ValueError(f"{name} must be finite (got {value!r}).")
    return v


def _finite_pos(name: str, value: float) -> float:
    """유한 + 양수 가드(>0). 폭·용량·온도 같은 분모/지수 인자용."""
    v = _finite(name, value)
    if v <= 0.0:
        raise ValueError(f"{name} must be > 0 (got {v!r}).")
    return v


def _finite_nonneg(name: str, value: float) -> float:
    """유한 + 비음수 가드(≥0). |I|·저항 같은 크기 인자용."""
    v = _finite(name, value)
    if v < 0.0:
        raise ValueError(f"{name} must be >= 0 (got {v!r}).")
    return v
# ===========================================================================


class GraphiteAnodeDischargeDQDV:
    """흑연 음극 dQ/dV 물리 모델 — 충전·방전·온도·C-rate 작동.

    [인자 노출 원칙] 커브식의 모든 기호 = 코드 입력. 전이 dict 키 또는
    생성자/호출 인자. 내부 하드코딩 상수는 없다(전부 기본값+override).

    생성자 인자
    ----------
    transitions : List[dict]
        전이별 파라미터. 키:
          U | (dH_rxn, dS_rxn) : 평형 중심 [V] 또는 열역학 환산
          w | n                : 폭 [V] 또는 다중도(없으면 1)
          Q                    : 전이 용량(전하) 가중
          Omega, gamma         : 정규용액 상호작용 [J/mol]·분기 축소 인자(히스)
          dH_a, dS_a           : 활성화 엔탈피·엔트로피 [J/mol]·[J/mol/K] (동역학)
          dVdq_qa              : 컷점 OCV 기울기 |dV/dq| [V] (L_q→L_V 환산)
          h_eta                : 부분 cycle 인자(기본 1.0)
          L_V                  : (선택) 지연 길이 직접 지정 [V] — 있으면 동역학 우회
    x : float                  : 전이상태 분율 위치 χ(방전 기준, 0~1; 기본 0.5)
    Rn : float                 : 직렬 저항 [Ω] (분극)
    Cbg : float|callable       : 배경 dQ/dV (상수 또는 V 함수)
    chi : float|None           : χ 직접 지정(없으면 x 사용)
    chi_split : callable        : (chi, σ_d)→χ_d 방향별 전달계수 규칙(기본 func_chi_d).
                                 ★주입 교체 가능 — 히스/χ_d 분배 규칙을 사용자가 바꿈.
    use_dH_eff : bool          : ΔH_a^eff=ΔH_a−χ_d·Ω 보강 적용(기본 True; eq:dHeff)
    z_cut : float              : 꼬리 컷점 affinity 의 z=A/(nRT) (기본 4.357 = 미분 종 ξ(1−ξ) 정점 5% 컷)
    A_cap_RT : float           : 컷 affinity 상한 A ≤ A_cap_RT·RT (기본 4.0)
    """

    # 탈리튬화에 대응하는 셀 라벨(Ch1 eq:lco-sigmaslot): 음극(흑연) = 방전.
    #   curve() 의 direction 라벨→σ_d 환산에만 쓰이고, dqdv(s=...) 저수준 경로는 무관.
    _delith_is_discharge: bool = True

    def __init__(self, transitions: List[Dict[str, Any]], x: float = 0.5,
                 Rn: float = 0.0, Cbg: Union[float, Callable] = 0.0,
                 chi: Optional[float] = None,
                 chi_split: Callable[[float, int], float] = func_chi_d,
                 use_dH_eff: bool = True,
                 z_cut: float = 4.357, A_cap_RT: float = 4.0,
                 seed_T: float = 298.15, seed_I: float = 0.1,
                 seed_Q_cell: float = 1.0):
        self.transitions = transitions
        # (B) 매직넘버·스칼라 인자 유한·범위 가드(생성 시 즉시 fail-fast).
        self.x = _finite("x", x)
        self.Rn = _finite_nonneg("Rn", Rn)
        self.Cbg = Cbg  # float 또는 callable — 호출 시 유한성은 출력에서 검사 X(사용자 책임)
        self.chi = _finite("chi", chi) if chi is not None else self.x
        if not callable(chi_split):
            raise TypeError("chi_split must be callable (chi, sigma_d) -> chi_d.")
        self.chi_split = chi_split
        self.use_dH_eff = bool(use_dH_eff)
        self.z_cut = _finite_pos("z_cut", z_cut)
        self.A_cap_RT = _finite_pos("A_cap_RT", A_cap_RT)

        # [보완(1)] transition 에 없는 파생 초기값(L_V seed)을 물리로 계산해 채움.
        #   ★원본 line 81 `self.transitions["L_V"] = self._init_L_V` 는 List 에
        #     문자열 키 대입이라 TypeError — 그 "파생 초기값 채움" 의도를 살려,
        #     별도 리스트 self.seed_L_V 에 전이별 seed 값을 계산·저장한다(삭제 X).
        #   seed 는 대표 조건(seed_T/seed_I/seed_Q_cell, 방전 기준)에서의 L_V —
        #     dqdv() 가 실제 (T,I,Q_cell) 로 재산출하므로 seed 는 진단·초기값용.
        self.seed_L_V: List[float] = self._build_seed_L_V(
            _finite_pos("seed_T", seed_T),
            _finite_nonneg("seed_I", seed_I),
            _finite_pos("seed_Q_cell", seed_Q_cell))

    # ---- 보완(1): 파생 초기값(L_V seed) 산출 ------------------------------
    def _build_seed_L_V(self, T: float, I: float, Q_cell: float) -> List[float]:
        """전이별 L_V 시작값(seed)을 물리로 계산. 방전(σ_d=+1) 기준."""
        seeds: List[float] = []
        for tr in self.transitions:
            n_j = float(np.asarray(self._n_factor(tr, T)).reshape(-1)[0])
            seeds.append(self._resolve_lag_length(
                tr, T, I, Q_cell, n_j, sigma_d=+1))
        return seeds

    # ---- 폭 다중도 n (선택적 온도 함수 n(T)) -----------------------------
    def _n_factor(self, tr: Dict[str, Any], T: ScalarOrArray) -> ScalarOrArray:
        """폭 다중도 n (eq:wbase 의 n_j). 'n' 직접, 또는 'w' 에서 n=w·F/(RT) 역산, 없으면 1.

        ★1.0.16 — 'n' 경로에 선형 온도 함수 n(T) 지원(폭 T-의존 피팅). 전이 dict 에
        'n_T1'(계수 [1/K], 기본 부재=0=상수 n)·'n_T_ref'(기준온도 [K], 기본 298.15)가 있으면
        n(T) = n + n_T1·(T − n_T_ref). 폭 w=n(T)·RT/F 가 되어 열적 스케일 위에 잔여 T-의존을
        얹는다(가역열 config 항은 _dwdT 가 ∂w/∂T 를 정합 전파). 'w'-단독은 T-동결 폭이라 n(T) 미적용."""
        if tr.get('n_T1') is not None and tr.get('n') is None:
            raise ValueError("transition 'n_T1' requires 'n' (n(T)=n+n_T1·(T−n_T_ref)).")
        if tr.get('n') is not None:
            n0 = _finite("n", tr['n'])
            n_T1 = tr.get('n_T1')
            if n_T1 is None:
                return n0
            n_T1 = _finite("n_T1", n_T1)
            T_ref = _finite("n_T_ref", tr.get('n_T_ref', 298.15))
            return n0 + n_T1 * (np.asarray(T, dtype=float) - T_ref)
        if tr.get('w') is not None:
            return tr['w'] * F / (R * T)
        return 1.0

    # ---- 폭 w (자유 피팅 파라미터: w|n 직접 지정, 없으면 n=1) ----------------
    def _width(self, tr: Dict[str, Any], T: ScalarOrArray) -> ScalarOrArray:
        """전이 폭 w [V] = nRT/F(=func_w, eq:wbase). w|n 직접 지정 우선, 없으면 n=1.
        (use_w_eff 경로는 ξ_eq 폭·분모 불일치로 면적보존 깨지는 버그 — 1.0.10에서 제거.)
        ★1.0.16 — n(T) 도입으로 폭이 음/영이 될 수 있어(n(T)≤0) w>0 fail-fast 가드."""
        w = func_w(T, self._n_factor(tr, T))
        if not np.all(np.asarray(w, dtype=float) > 0.0):
            raise ValueError("width w=n(T)·RT/F must be > 0 (n(T)≤0 at some T — check n/n_T1/n_T_ref).")
        return w

    # ---- ∂w/∂T (가역열 config 항 계수; n(T) 정합 전파) -------------------
    def _dwdT(self, tr: Dict[str, Any], T: ScalarOrArray) -> ScalarOrArray:
        """봉우리 폭의 온도 미분 ∂w_j/∂T [V/K] — 가역열 config 항 계수(Ch2 eq:dxidT 둘째 조각).

        열적 폭 w=n(T)·RT/F 이므로 ∂w/∂T = (R/F)·d[n(T)·T]/dT = (R/F)·(n(T) + T·n_T1).
        상수 n(n_T1=0): (R/F)·n = n·R/F (1.0.15 형과 bit-exact). 'w'-단독·기본 = T-동결 → 0."""
        if tr.get('n') is None:
            return 0.0  # 'w'-단독 또는 기본 = T-동결 폭 취급(단순식 경로)
        n0 = _finite("n", tr['n'])
        n_T1 = _finite("n_T1", tr.get('n_T1', 0.0))
        T_ref = _finite("n_T_ref", tr.get('n_T_ref', 298.15))
        Tv = np.asarray(T, dtype=float)
        nT = n0 + n_T1 * (Tv - T_ref)
        return (R / F) * (nT + Tv * n_T1)

    # ---- 제안 1: vib 엔트로피 Einstein 양자 보정 (v1.0.18.2, additive) ----
    def _vib_theta(self, tr: Dict[str, Any]) -> Optional[float]:
        """전이의 Einstein 온도 θ_E [K](키 'theta_E'), 부재=None."""
        te = tr.get('theta_E')
        if te is None:
            return None
        te = _finite("theta_E", te)
        if te <= 0.0:
            raise ValueError("transition 'theta_E' (Einstein 온도) must be > 0 K.")
        return te

    def _S_vib(self, T: ScalarOrArray, theta_E: float) -> ScalarOrArray:
        """단일 모드 Einstein 진동 엔트로피 [J/(mol·K)]
           S_vib(T) = R[−ln(1−e^{−x}) + x/(e^x−1)], x=θ_E/T.
           고온극한(kT≫ℏω): →R[1+ln(T/θ_E)](고전값·현 동결과 정합), 저온: →0."""
        Tv = np.asarray(T, dtype=float)
        x = theta_E / Tv
        return R * (-np.log1p(-np.exp(-x)) + x / np.expm1(x))

    def _vib_dU(self, tr: Dict[str, Any], T: ScalarOrArray) -> ScalarOrArray:
        """vib 양자 보정의 평형 중심 U_j 이동 [V] — Helmholtz 자유에너지 편차.
           ΔU_vib(T) = −(1/F)[ΔF_vib(T) − ΔF_vib(T_ref) + S_vib(T_ref)·(T−T_ref)],
           ΔF_vib(T)=R·T·ln(1−e^{−θ_E/T}), T_ref='theta_E_Tref'(기본 298.15).
           θ_E 부재 → 0(additive·bit-exact). ∂ΔU_vib/∂T = [S_vib(T)−S_vib(T_ref)]/F
           = _vib_dS/F 이므로 entropy_coefficient 와 round-trip 정합(∂U/∂T=ΔS(T)/F)."""
        te = self._vib_theta(tr)
        if te is None:
            return 0.0
        Tref = _finite("theta_E_Tref", tr.get('theta_E_Tref', 298.15))
        Tv = np.asarray(T, dtype=float)
        dF = lambda t: R * np.asarray(t, dtype=float) * np.log1p(-np.exp(-te / np.asarray(t, dtype=float)))
        Sref = float(self._S_vib(Tref, te))
        return -(dF(Tv) - float(dF(Tref)) + Sref * (Tv - Tref)) / F

    def _vib_dS(self, tr: Dict[str, Any], T: ScalarOrArray) -> ScalarOrArray:
        """vib 양자 보정의 표준엔트로피 편차 S_vib(T)−S_vib(T_ref) [J/(mol·K)] —
           entropy_coefficient dS_eff 에 가산(가역열 ∂U/∂T 의 vib T-signature,
           전자항 ∝T 와 분리 식별용). θ_E 부재 → 0(bit-exact)."""
        te = self._vib_theta(tr)
        if te is None:
            return 0.0
        Tref = _finite("theta_E_Tref", tr.get('theta_E_Tref', 298.15))
        return self._S_vib(T, te) - float(self._S_vib(Tref, te))

    # ---- 방향별 χ_d (주입 callable; 기본 충전 χ→1−χ, eq:chid) -----------
    def _chi_d(self, sigma_d: int) -> float:
        """전달계수 χ_d = chi_split(χ, σ_d). 기본 func_chi_d(방전 χ / 충전 1−χ).
        ★규칙 자체는 self.chi_split 로 교체 가능(히스/χ_d 확장성)."""
        return float(self.chi_split(self.chi, sigma_d))

    # ---- (D) χ_d·ΔH_a^eff 응집 헬퍼 -------------------------------------
    def _chi_and_dH_eff(self, dH_a: float, Omega: float, sigma_d: int,
                        use_dH_eff: Optional[bool] = None) -> Tuple[float, float]:
        """방향별 (χ_d, ΔH_a^eff) 한 곳에서 산출(eq:chid·eq:dHeff).
        use_dH_eff=False 면 ΔH_a^eff=ΔH_a(보강 없음). per-tr override(None=전역)."""
        chi_d = self._chi_d(sigma_d)
        ud = self.use_dH_eff if use_dH_eff is None else bool(use_dH_eff)
        dH_a_use = func_dH_a_eff(dH_a, Omega, chi_d) if ud else float(dH_a)
        return chi_d, dH_a_use

    # ---- 보완(2): 지연 길이 resolver (이름 통일·완성) --------------------
    def _resolve_lag_length(self, transition: Dict[str, Any], T: float,
                            I: float, Q_cell: float, n_j: float,
                            sigma_d: int = +1) -> float:
        """전이 하나의 지연 길이 L_V [V] (eq:LV: L_V=|dV/dq|_qa·L_q).

        - 'L_V' 직접 지정이 있으면 그대로(피팅·테스트, 동역학 우회).
        - 없으면 동역학 산출: 컷 affinity A → func_L_q → ×|dVdq_qa|.
        - I≤0 또는 동역학 키 부재 → 0(평형 종, 꼬리 없음).
        χ_d·ΔH_a^eff 방향 의존을 sigma_d 로 받는다(충방전 별 꼬리 길이 갈림).
        (B) 직접 L_V·dict 동역학 값의 유한성 가드 포함."""
        L_V_override = transition.get('L_V')
        if L_V_override is not None:
            v = float(L_V_override)
            if not np.isfinite(v) or v < 0.0:
                raise ValueError(f"transition 'L_V' must be finite & >=0 (got {v!r}).")
            return v
        if I <= 0 or transition.get('dH_a') is None:
            return 0.0

        # [원본 _init_L_V 의도 복원] 미정의였던 s/OCV/U/dOCVdsto 를 물리로 연결:
        #   · A = 꼬리 컷점 affinity(eq:Acut). 원천 dξ_eq/dq 가 정점의 ~5%(z_cut=4.357)로
        #         떨어지는 컷에서 A=z_cut·n·RT (충·방전 동일 크기), A_cap_RT·RT 상한.
        #         (원본 `min(s·F·(OCV−U), 4RT)` 의 등가형 — s 는 크기에 안 들어가고
        #          방향은 아래 χ_d/ΔH_eff 가 받는다. s 를 min 밖에 두면 충전서 음수
        #          상한이 되던 원본 버그를 정정.)
        n_safe = abs(_finite("n_j", n_j))
        z_cut = _finite_pos("z_cut", transition.get('z_cut', self.z_cut))
        A_cap = _finite_pos("A_cap_RT", transition.get('A_cap_RT', self.A_cap_RT))
        A = float(min(z_cut * n_safe * R * T, A_cap * R * T))

        dH_a = _finite("dH_a", transition['dH_a'])
        dS_a = _finite("dS_a", transition.get('dS_a', 0.0))
        Omega = _finite_nonneg("Omega", transition.get('Omega', 0.0))

        # (D) χ_d·ΔH_a^eff 응집 헬퍼 — eq:dHeff 방향별. use_dH_eff 로 on/off.
        chi_d, dH_a_use = self._chi_and_dH_eff(
            dH_a, Omega, sigma_d, transition.get('use_dH_eff'))

        # func_L_q(x=χ_d) — 원형 그대로. x 자리에 방향별 χ_d 주입(충전 χ→1−χ).
        L_q = func_L_q(T, I, Q_cell, dH_a_use, dS_a, chi_d, A)
        if not np.isfinite(L_q):
            return 0.0

        # [_init_L_V 의 dOCVdsto] = 컷점 OCV 기울기 |dV/dq| → 전이 dict 'dVdq_qa'.
        return abs(_finite("dVdq_qa", transition.get('dVdq_qa', 0.0))) * float(L_q)

    # ---- 평형 곡선(|I|→0 기준선) ----------------------------------------
    def equilibrium(self, V_n: ScalarOrArray, T: float = 298.15) -> ScalarOrArray:
        """평형 dQ/dV (|I|→0). 충방전 방향 불변(평형 peak; eq:eqpeak)."""
        T = _finite_pos("T", T)
        V = np.asarray(V_n, dtype=float)
        baseline = (np.asarray(self.Cbg(V), dtype=float) * np.ones_like(V)
                    if callable(self.Cbg)
                    else np.full_like(V, float(self.Cbg)))
        dqdv = baseline
        for tr in self.transitions:
            if 'dH_rxn' in tr and 'dS_rxn' in tr:
                U_j = float(func_U_j(T, tr['dH_rxn'], self._effective_dS_rxn(tr, T)) + self._vib_dU(tr, T))
            else:
                U_j = tr['U']
            n_j = self._n_factor(tr, T)
            w = self._width(tr, T)
            ksi_eq = func_ksi_eq(T, V, U_j, n_j)
            dqdv = dqdv + tr['Q'] * ksi_eq * (1.0 - ksi_eq) / w
        return dqdv

    # ---- 보완(3)(4): 충방전·온도·C-rate dQ/dV ---------------------------
    def dqdv(self,
             V_app: ScalarOrArray,
             T: Union[float, np.ndarray],
             I_abs: float,
             Q_cell: float,
             s: int = +1) -> ScalarOrArray:
        """관측 dQ/dV (eq:vn 분극 → eq:sum 점별 합산).

        V_app  : 인가(측정) 전위 배열 [V] (스칼라 또는 배열). 모든 평가는 이 전위에서
                 점별(pointwise) — 균일 작업 격자·리샘플·역보간 없음. 스칼라·단일점은
                 스윕 이력이 없어 꼬리 미정의 → 평형 종.
        T      : 온도 [K] (스칼라 등온, 또는 V_app 길이 배열 = 비등온 T(V))
        I_abs  : 전류 크기 |I| (>= 0)
        Q_cell : 셀 용량(전하) — q=Q/Q_cell 환산 (> 0)
        s      : 방향 부호 σ_d (방전 +1 / 충전 −1)

        반영: 분극 V_n=V_app−σ_d|I|R_n · 분기중심 U^d(σ_d) · peak 모양 (ξ_eq−ξ_lag)/L_V
              (Ch1 eq:peakshape; ξ_lag=인과 기억 적분 eq:lag, 방향 반전 eq:reversal).
              L_V→0 극한은 평형 종 ξ_eq(1−ξ_eq)/w (eq:tail-limit) — 분기 없음, 수치 가드만.
        (B) I_abs·Q_cell·T 유한·범위 가드.
        """
        sigma_d = +1 if s >= 0 else -1

        # (B) 입력 가드 — fail-fast.
        I_abs = _finite_nonneg("I_abs", I_abs)
        Q_cell = _finite_pos("Q_cell", Q_cell)

        V_in = np.asarray(V_app, dtype=float)
        is_scalar = (V_in.ndim == 0)
        V_in = np.atleast_1d(V_in)
        if V_in.size == 0:
            raise ValueError("V_app must be non-empty.")
        if not np.all(np.isfinite(V_in)):
            raise ValueError("V_app contains non-finite entries.")

        T_input = np.asarray(T, dtype=float)
        T_is_array = (T_input.ndim >= 1 and T_input.size > 1)
        if not np.all(np.isfinite(T_input)) or np.any(T_input <= 0.0):
            raise ValueError("T must be finite and > 0 (K).")
        if T_is_array and T_input.size != V_in.size:
            raise ValueError("T array length must match V_app (per-point T(V)).")

        # 분극: V_n = V_app − σ_d|I|R_n (eq:vn) — 이후 모든 평가는 V_n 위에서 점별.
        V_n = V_in - sigma_d * I_abs * self.Rn
        n_pts = V_n.size

        # 진행 방향 정렬(eq:reversal): 인과 기억은 "진행 방향의 과거"를 훑는다.
        #   방전(σ_d=+1) 진행=V 증가 → 오름차순 / 충전(σ_d=−1) 진행=V 감소 → 내림차순.
        order = np.argsort(V_n, kind="stable")
        if sigma_d < 0:
            order = order[::-1]
        inv_order = np.empty(n_pts, dtype=int)
        inv_order[order] = np.arange(n_pts)
        V_prog = V_n[order]
        T_prog = (T_input[order] if T_is_array
                  else np.full(n_pts, float(T_input), dtype=float))
        T_rep = float(np.mean(T_prog))

        # 배경 미분용량(입력 전위에서 직접).
        if callable(self.Cbg):
            bg = np.asarray(self.Cbg(V_n), dtype=float) * np.ones_like(V_n)
        else:
            bg = np.full_like(V_n, float(self.Cbg))

        # 수치 해상 가드용 대표 간격(진행 격자의 양수 중앙값).
        if n_pts >= 2:
            dV_pos = np.abs(np.diff(V_prog))
            dV_pos = dV_pos[dV_pos > 0.0]
            char_h = float(np.median(dV_pos)) if dV_pos.size else 0.0
        else:
            char_h = 0.0

        acc_prog = np.zeros(n_pts, dtype=float)  # 진행 순서 전이 합
        for tr in self.transitions:
            # 평형 중심 U_j(T) — 배열 T 대응
            if 'dH_rxn' in tr and 'dS_rxn' in tr:
                U_j = func_U_j(T_prog, tr['dH_rxn'], self._effective_dS_rxn(tr, T_prog)) + self._vib_dU(tr, T_prog)
            else:
                U_j = float(tr['U'])

            # ★히스테리시스 분기 중심 U^d = U + ½·σ_d·h_η·γ·ΔU_hys (eq:Ubranch). γ=0 → 0.
            Omega = float(tr.get('Omega', 0.0))
            gamma = float(tr.get('gamma', 0.0))
            h_eta = float(tr.get('h_eta', 1.0))
            if gamma != 0.0 and Omega > 0.0:
                center = U_j + func_U_branch(T_rep, 0.0, Omega, gamma, sigma_d, h_eta)
            else:
                center = U_j

            n_j = self._n_factor(tr, T_prog)
            w = self._width(tr, T_prog)
            # 평형 진행률 ξ_eq(진행 순서) — 방향 s 는 logistic 부호. 분기중심 center.
            ksi_eq = np.asarray(func_ksi_eq(T_prog, V_prog, center, n_j, sigma_d), dtype=float)

            # 지연 길이 — 전이당 상수(대표 T_rep·대표 n)로 1회. χ_d·ΔH_eff 방향별.
            n_rep = float(np.asarray(self._n_factor(tr, T_rep)).reshape(-1)[0])
            lag_len_V = self._resolve_lag_length(
                tr, T_rep, I_abs, Q_cell, n_rep, sigma_d)

            # 수치 가드(D6): 스칼라·단일점·비유한·미해상(커널이 한 격자점 안에서 소진,
            #   a=char_h/L_V > _LAG_RESOLVE_DECAY_CAP) 또는 char_h≤0(전 V 동일) → 평형 종 직접.
            #   ξ_lag→ξ_eq 인 (ξ_eq−ξ_lag)/L_V 0/0 을 피하는 수치 안전장치. 평형 종은
            #   (ξ_eq−ξ_lag)/L_V 의 L_V→0 해석적 극한(eq:tail-limit)이지 물리 분기가 아니다.
            unresolved = (char_h <= 0.0) or (lag_len_V * _LAG_RESOLVE_DECAY_CAP < char_h)
            if (is_scalar or n_pts < 2 or (not np.isfinite(lag_len_V))
                    or lag_len_V <= 0.0 or unresolved):
                peak_shape = ksi_eq * (1.0 - ksi_eq) / w
            else:
                # 인과 기억 적분 ξ_lag(진행 방향, eq:lag·eq:reversal) → peak(eq:peakshape).
                ksi_lag = _causal_memory_pointwise(V_prog, ksi_eq, lag_len_V)
                peak_shape = (ksi_eq - ksi_lag) / lag_len_V

            acc_prog = acc_prog + tr['Q'] * peak_shape

        # 진행 순서 누적을 입력 순서로 되돌려 배경 위에 점별 합산(역보간 없음).
        dqdv_out = bg + acc_prog[inv_order]
        return float(dqdv_out[0]) if is_scalar else dqdv_out

    # ---- (C) 편의 facade : 실험조건으로 바로 호출 ------------------------
    def curve(self,
              V_app: ScalarOrArray,
              direction: Union[int, str] = "discharge",
              c_rate: float = 0.0,
              Q_cell: float = 1.0,
              T: Union[float, np.ndarray] = 298.15,
              I_abs: Optional[float] = None) -> ScalarOrArray:
        """실험조건 → dQ/dV 상위 편의 메서드(내부는 dqdv 재사용, 새 물리 X; 환산은 eq:n0map).

        V_app     : 인가 전위 격자 [V]
        direction : 방향 — 'discharge'/'d'/'dis'/+1  또는 'charge'/'c'/'chg'/−1
        c_rate    : C-rate [1/h]. |I| = c_rate · Q_cell 로 환산(I_abs 미지정 시).
        Q_cell    : 셀 용량(전하). c_rate→|I| 환산·q 환산에 공용(> 0).
        T         : 온도 [K] (scalar 또는 V_app 길이 array — 비등온 T(V)).
        I_abs     : (선택) 전류 크기 직접 지정. 주면 c_rate 무시(우선).

        반환 = dqdv(V_app, T, |I|, Q_cell, σ_d) 결과(동일 배열/스칼라 규약).
        """
        sigma_d = self._direction_to_sigma(direction)
        if not self._delith_is_discharge:
            # 전극 인지 환산(Ch1 eq:lco-sigmaslot): σ_d 슬롯의 물리 = 탈리튬화 = +1.
            # 양극(LCO)은 '충전' 라벨이 탈리튬화이므로 셀 라벨 부호를 뒤집어 먹인다.
            # 저수준 경로(dqdv 의 s 인자 직접 지정)는 환산 없이 물리 부호 그대로.
            sigma_d = -sigma_d
        Q_cell = _finite_pos("Q_cell", Q_cell)
        if I_abs is None:
            c = _finite_nonneg("c_rate", c_rate)
            I_use = c * Q_cell          # |I| = C-rate · Q_cell (전류 = 율 × 용량)
        else:
            I_use = _finite_nonneg("I_abs", I_abs)
        return self.dqdv(V_app, T, I_use, Q_cell, s=sigma_d)

    # ===== 가역 발열 · 전자엔트로피 seam (P4: LCO 양극·발열 확장) ================
    def _effective_dS_rxn(self, tr: Dict[str, Any],
                          T: Union[float, np.ndarray]) -> ScalarOrArray:
        """전이의 유효 표준 엔트로피 ΔS_rxn [J/(mol·K)] — 흑연 base = 항등(값 그대로).

        ★seam: equilibrium·dqdv·entropy_coefficient 세 경로가 공유하는 dS_rxn 진입점.
        LCO 서브클래스가 전자항 ΔS_e 를 이 한 곳에서 가산 → 세 산출의 T1 전자항 일치
        (검토1 ⑤ 결함 해소). 흑연은 tr['dS_rxn'] 을 그대로 반환하므로 func_U_j 인자가
        완전히 동일 → 흑연 곡선 byte 0-diff 보장(가산·부동소수점 연산 자체가 없음).
        """
        return tr['dS_rxn']

    def entropy_coefficient(self, V_n: ScalarOrArray,
                            T: Union[float, np.ndarray] = 298.15) -> ScalarOrArray:
        """가역 엔트로피 계수 ∂U_oc/∂T(x) [V/K] — Ch2 가중식 eq:weighted 의 완전식 확장(§2.6 keybox 종합식).

        관측 ∂U_oc/∂T = Σ_j [Q_j g_j / Σ_k Q_k g_k]·(ΔS_eff,j/F + (n_j·R/F)·ln[ξ_j/(1−ξ_j)]).
        ★config 항 계수 = ∂w_j/∂T = n_j·R/F (v1.0.14 R2 정정 — 구판은 R/F 로 n_j=1 특수형;
          기본 데이터셋 n_j=1.0 에서는 수치 동일(bit-exact), n_j≠1 피팅 시에만 발현).
        ★config 항은 폭의 열적 서식 w=nRT/F('n' 키 경로) 전제 — 'w'-단독 전이는 폭이
          T-동결(∂w/∂T=0)이라 config 항을 가산하지 않는다(단순식이 옳음, Ch2 파생 A srcbox).
        첫 항 = 봉우리 중심 표준 엔트로피 ΔS⁰_j/F(seam 경유 = LCO 전자항 포함;
        LCO 개별 전이의 이 관계식은 eq:lco-dUdT), 둘째 항 =
        봉우리 내부 configurational 분포항. ★dqdv 곡선은 이 config 항을 넣지 않는다(폭
        w 가 이미 담음, Ch2 파생 B) — q_rev 경로만 명시 가산한다. 두 경로는 같은 물리의
        다른 산출(직교; 이중계산 아님). 평형 진행률 ξ_eq(|I|→0) 기준. 히스 분기평균 가역열
        (Ch2 eq:hys_rev)은 평형 중심 U_j(히스 shift 無)를 써서 자동 근사 달성한다 — γ 대칭
        전제이며, 비대칭 분기별 ∂U/∂T 는 미구현(Ch2 범위 밖 선언, 후속 과제).
        """
        # T: 스칼라(등온) 또는 V_n 길이 배열 T(V)(비등온 — dqdv 와 동일). 각 점 실측 온도.
        T = np.asarray(T, dtype=float)
        if not np.all(np.isfinite(T)) or np.any(T <= 0.0):
            raise ValueError("T must be finite and > 0 (K).")
        V = np.atleast_1d(np.asarray(V_n, dtype=float))
        if T.ndim >= 1 and T.size > 1 and T.size != V.size:
            raise ValueError("T array length must match V_n (per-point T(V)).")
        num = np.zeros_like(V)
        den = np.zeros_like(V)
        eps = 1e-12
        for tr in self.transitions:
            if 'dH_rxn' in tr and 'dS_rxn' in tr:
                dS0 = self._effective_dS_rxn(tr, T)
                dS_eff = dS0 + self._vib_dS(tr, T)   # 제안1: vib Einstein 편차(θ_E 부재=0=bit-exact)
                U_j = func_U_j(T, tr['dH_rxn'], dS0) + self._vib_dU(tr, T)
            else:
                dS_eff = 0.0
                U_j = float(tr['U'])
            n_j = self._n_factor(tr, T)
            w = self._width(tr, T)
            xi = np.asarray(func_ksi_eq(T, V, U_j, n_j), dtype=float)
            g = xi * (1.0 - xi) / w
            xi_c = np.clip(xi, eps, 1.0 - eps)
            # config 항 = ∂w_j/∂T · ln[ξ/(1−ξ)] (Ch2 eq:dxidT 둘째 조각). _dwdT 가 열적/n(T)/
            #   T-동결('w'-단독·기본)을 정합 처리: 상수 n → n·R/F(1.0.15 bit-exact),
            #   n(T) → (R/F)(n(T)+T·n_T1), 'w'-단독·기본 → 0(단순식).
            config = self._dwdT(tr, T) * np.log(xi_c / (1.0 - xi_c))
            Qg = tr['Q'] * g
            num = num + Qg * (dS_eff / F + config)
            den = den + Qg
        dUdT = np.where(den > 0.0, num / np.maximum(den, eps), 0.0)
        return dUdT

    def reversible_heat(self, V_n: ScalarOrArray, T: Union[float, np.ndarray] = 298.15,
                        I: float = 1.0) -> ScalarOrArray:
        """가역 발열 q_rev = −I·T·∂U_oc/∂T [W] (Ch2 eq:qrev, ★T 한 번).

        ∂U_oc/∂T 가 이미 [V/K] 이므로 −I·T·(∂U/∂T) 로 T 는 한 번만 곱한다(T² 금지).
        방전 I>0: ΔS>0(∂U/∂T>0) → q_rev<0 흡열 / ΔS<0(∂U/∂T<0) → 발열(Ch2 부호규약).
        ★라벨 층위 주의: 이 '방전(I>0)'은 Bernardi 셀-수지 라벨(흑연 하프셀 = 리튬화)로,
          curve() 의 direction='discharge'(σ_d=+1, 탈리튬화)와 반대 화학 방향이다 —
          부호는 라벨이 아니라 전류 부호 I 로 읽는다(Ch2 eq:qrev 라벨 층위 주의).
        """
        T = np.asarray(T, dtype=float)  # 스칼라/배열 — 유한·양수·길이 검증은 entropy_coefficient 가 수행
        return -float(I) * T * self.entropy_coefficient(V_n, T)

    def irreversible_heat(self, U_oc: ScalarOrArray, V: ScalarOrArray,
                          I: float) -> ScalarOrArray:
        """비가역 발열(과전압 소산) q_irr = I·(U_oc−V) ≥ 0 [W] — lumped(Ch2 eq:qrev 첫 항).

        ★3분해(I²R_n + I·η_ct + I·η_diff)는 Ch2 에 boxed 식이 없다(eq:qrev 주변 prose·srcbox 는
        lumped 만 제시) → 본 구현은 lumped 만 둔다. 개별 과전압 분해는 다온도·율의존
        피팅 단계의 과제(근거 미발견, 옵션)로 분리한다.
        """
        return np.asarray(I) * (np.asarray(U_oc, dtype=float) - np.asarray(V, dtype=float))

    @staticmethod
    def _direction_to_sigma(direction: Union[int, str]) -> int:
        """방향 입력(문자열/정수)을 σ_d(+1 방전 / −1 충전)로 환산.
        문자열: discharge/d/dis/+ → +1, charge/c/chg/− → −1 (대소문자 무시).
        정수/실수: ≥0 → +1, <0 → −1."""
        if isinstance(direction, str):
            key = direction.strip().lower()
            if key in ("discharge", "dis", "d", "+", "+1", "1", "sigma+"):
                return +1
            if key in ("charge", "chg", "c", "-", "-1", "sigma-"):
                return -1
            raise ValueError(
                f"direction must be discharge/charge (or +1/-1), got {direction!r}.")
        val = _finite("direction", direction)
        return +1 if val >= 0 else -1


# ===== LCO 양극 MSMR 시연 데이터셋 — Ch1 sec:lco-code ==============================
#   MSMR 동형: X_j↔Q_j, U_j⁰↔U_j^d, ω_j↔w_j, f↔+σ_d(진행률↔진행률 pairing —
#   원계열 f=F/RT>0 의 재모수화, Ch1 eq:lco-msmrmap). 방전 σ_d=+1(LCO 리튬화 — 평형·∂U/∂T 경로 한정,
#   방향 작용처의 슬롯은 탈리튬화=+1 = LCO 충전, eq:lco-sigmaslot; curve 라벨은 자동 환산)·
#   부호 골격 흑연 동일(Ch1 Part II sec:lco-map·sec:lco-direction). 전자항(MIT)은 'electronic' 전이에
#   x_MIT 창의 ΔS_e 골(eq:dSegate)로 부여.
#   ★[출처 라벨] tier-C 시연 기본값 — round-trip 피팅 前 placeholder(실측 신뢰값 아님,
#     피팅 함수의 시연용 초기값). U(298) 는 dH_rxn/dS_rxn 로 목표 전위에 정합.
LCO_MSMR_LIT = [
    {   # T1 주 평탄역(MIT, U≈3.930 V) — x≈0.75-0.95, MIT 창 포함 → 전자 엔트로피 골(ΔS_e<0)
        # ΔH = T_ref·ΔS_eff − F·U — 전자항 ΔS_e(T_ref)≈−45.678 을 흡수해 T_ref 평탄역이
        #   U 에 놓이게 재보정(측정 OCV=총엔트로피 반영). ΔS_e 는 ∂U/∂T(가역열)에만 작용.
        # [v1.0.14 루프 B] 전자항을 물리 anchor(T1=MIT, x_MIT≈0.85 — Ch1 tab:lco-staging)
        #   dict 로 재정렬(구판은 중간 dict x_MIT=0.50 tier-C 시연 배정).
        #   역산 상수 = 본 모듈 F=96485.0 (CODATA 96485.332 로 역산하면 −391017.4,
        #   순전파 U(298) +13 μV 어긋남 — 코드 자체 상수 기준으로 정합).
        'U': 3.930, 'w': 0.030, 'Q': 0.55,
        'dH_rxn': -391016.1, 'dS_rxn': +6.0, 'n': 1.0,
        'electronic': True, 'x_center': 0.85,
        'g_max_eV': 13.0, 'x_MIT': 0.85, 'dx_MIT': 0.05,
    },
    {   # order-disorder(≈3.880 V) — x≈0.5 (전자항 흡수 해제로 ΔH 재보정, F=96485.0 역산)
        'U': 3.880, 'w': 0.024, 'Q': 0.30,
        'dH_rxn': -375554.4, 'dS_rxn': -4.0, 'n': 1.0,
    },
    {   # 고전위 곁가지(≈4.050 V) — x≈0.35
        'U': 4.050, 'w': 0.028, 'Q': 0.15,
        'dH_rxn': -391360.0, 'dS_rxn': -2.0, 'n': 1.0,
    },
]


class LCOCathodeDQDV(GraphiteAnodeDischargeDQDV):
    """LCO 양극 dQ/dV — MSMR 동형(Ch1 sec:lco-code: X_j↔Q_j, U_j⁰↔U_j^d, ω_j↔w_j,
    f↔+σ_d — 진행률↔진행률 pairing, 원계열 f=F/RT>0 의 재모수화).

    흑연 음극 모델을 그대로 상속한다 — 곡선 골격(분극·히스 분기·평형/꼬리·면적보존
    DC=1)은 부호까지 동일하다(Ch1 sec:lco-map: 방전 σ_d=+1 은 LCO 엔 리튬화이며
    ∂U_j/∂T=ΔS_rxn/F 의 부호 관계가 흑연과 같으므로 σ_d 를 뒤집지 않는다 — 단
    이는 평형·∂U/∂T 경로 한정이다. 평형 종은 방향 불변이나, 방향 의존 작용처
    (분극·분기·꼬리)에 LCO 데이터를 걸 때는 셀 라벨이 아니라 탈리튬화 여부로 s 를
    준다(충전 곡선↦s=+1 — Ch1 sec:lco-direction 방향 규약, eq:lco-sigmaslot). 현재 LCO_MSMR_LIT 는
    Omega·dH_a 미배정으로 분기·꼬리 비활성이라 실질 방향 의존은 분극뿐이다.
    ★전극 인지 환산(v1.0.14 루프 B 구현): 본 클래스는 _delith_is_discharge=False 라
    curve() 의 direction 셀 라벨('charge'/'discharge')이 자동으로 탈리튬화 부호로
    환산된다 — LCO 충전 곡선은 direction='charge' 그대로 주면 σ_d=+1 슬롯에 간다.
    저수준 dqdv(s=...) 는 환산 없이 물리 부호(탈리튬화=+1)를 직접 받는다).

    유일한 확장 = 금속-절연체 전이(MIT)의 전자 엔트로피 항을 seam _effective_dS_rxn
    한 곳에서 'electronic' 전이의 ΔS_rxn 에 가산하는 것뿐이다(Ch1 sec:lco-code). 이
    항은 U_j(T) 의 온도이동에만 작용하고 봉우리 면적·폭은 바꾸지 않는다. equilibrium·
    dqdv·entropy_coefficient(발열) 세 경로가 같은 seam 을 공유하므로 T1 전자항이 세
    산출에 일관되게 반영된다.
    """

    # 양극(LCO): 탈리튬화 = '충전' 라벨 (Ch1 eq:lco-sigmaslot — curve() 라벨 환산용)
    _delith_is_discharge: bool = False

    def _effective_dS_rxn(self, tr: Dict[str, Any],
                          T: Union[float, np.ndarray]) -> ScalarOrArray:
        """LCO 유효 표준 엔트로피 = ΔS_rxn + (MIT 전이면) 전자항 ΔS_e
        (config+vib+electronic 분해; eq:lco-decomp).

        ★전자항은 기준온도 T_ref 에서 동결한 상수 오프셋으로 더한다(단일-기준 근사).
          → dS_eff 가 T-무관이 되어 U_j(T)=(−ΔH+T·dS_eff)/F 가 T-선형이고
            ∂U_oc/∂T=dS_eff/F 가 평형 peak(equilibrium·dqdv)와 발열(entropy_coefficient)
            세 경로에서 factor-2 없이 일관된다(검토1·adversarial 항목7 해소).
          ΔS_e 의 Sommerfeld T-스케일(∝T)과 eq:U1T2 의 center-T_ref 별도적분(½=a_e/2F
            인자)은 다온도 round-trip 피팅 단계의 과제로 분리한다(P4 미구현, 라벨).
        """
        dS = tr['dS_rxn']
        if tr.get('electronic'):
            T_ref = 298.15
            dS = dS + func_dSe_molar(tr['x_center'], T_ref,
                                     tr['g_max_eV'], tr['x_MIT'], tr['dx_MIT'])
        return dS


# ===== 전이 초기값 데이터셋 — 사용자 원형 보존(GRAPHITE_STAGING_LIT) ==========
#   [출처 라벨] 값은 초기값(시작점)일 뿐 — 신뢰값 아님, 사용자 피팅으로 override 전제.
#   ΔH_rxn/ΔS_rxn = 열역학(U(298) 정합), ΔH_a = DFT 활성화(저SOC→만충 감소 경향),
#   dVdq_qa = 컷 OCV 기울기(fit), Omega = 정규용액(상분리·히스, 추정).
GRAPHITE_STAGING_LIT = [
    {   # stage 4→3 (x=0.08-0.16, U≈0.210 V)
        'U': 0.210, 'w': 0.020, 'Q': 0.10, 'Omega': 6000.0,     # 폴백(하위호환)
        'dH_rxn': -11700.0, 'dS_rxn': +29.0, 'n': 1.0,          # 열역학:
        # ΔH=-11.7 kJ/mol, ΔS=+29.0 J/mol/K
        'dH_a': 48000.0, 'dS_a': 0.0, 'dVdq_qa': 0.30,          # 동역학:
        # DFT ΔH_a~48kJ/mol(저SOC, Anniés empty); dVdq_qa=컷 OCV기울기[V](fit); dS_a→0
    },
    {   # stage 3→2L (x=0.16-0.25, U≈0.140 V)
        'U': 0.140, 'w': 0.016, 'Q': 0.12, 'Omega': 8000.0,     # 폴백(하위호환)
        'dH_rxn': -13500.0, 'dS_rxn': 0.0, 'n': 1.0,            # 열역학:
        # ΔH=-13.5 kJ/mol(=ΔG@ΔS≈0) → U(298)=0.140 정합
        'dH_a': 46000.0, 'dS_a': 0.0, 'dVdq_qa': 0.30,          # 동역학:
        # DFT ΔH_a~46kJ/mol(중간 stage); dVdq_qa=컷 OCV기울기[V](fit); dS_a→0
    },
    {   # stage 2L→2 (x=0.25-0.50, U≈0.120 V)
        'U': 0.120, 'w': 0.014, 'Q': 0.25, 'Omega': 10000.0,    # 폴백(하위호환)
        'dH_rxn': -13100.0, 'dS_rxn': -5.0, 'n': 1.0,           # 열역학:
        # ΔH=-13.1 kJ/mol, ΔS=-5 J/mol/K
        'dH_a': 44000.0, 'dS_a': 0.0, 'dVdq_qa': 0.30,          # 동역학:
        # DFT ΔH_a~44kJ/mol(stage II, Thinius LiC12 45.3); dVdq_qa=컷 OCV기울기[V](fit); dS_a→0
    },
    {   # stage 2→1 (x=0.50-1.00, U≈0.085 V)  — 최대용량/최에너지
        'U': 0.085, 'w': 0.012, 'Q': 0.50, 'Omega': 13000.0,    # 폴백(하위호환)
        'dH_rxn': -13000.0, 'dS_rxn': -16.0, 'n': 1.0,          # 열역학:
        # ΔH=-13.0 kJ/mol, ΔS=-16 J/mol/K
        'dH_a': 40000.0, 'dS_a': 0.0, 'dVdq_qa': 0.30,          # 동역학:
        # DFT ΔH_a~40kJ/mol(만충 stage I, Thinius LiC6 40.5); dVdq_qa=컷 OCV기울기[V](fit); dS_a→0
    },
]


# ============================================================================
# 작동 검증 — 충전/방전 × C-rate × 온도 × T(V) (알파: 논리·실행·유한 확인)
#   ※ print 는 ASCII 안전 라벨(콘솔 cp949 등 비UTF 환경에서도 실행 보장).
# ============================================================================
if __name__ == "__main__":
    V = np.linspace(0.03, 0.34, 1000)
    model = GraphiteAnodeDischargeDQDV(
        GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05,
        use_dH_eff=True)

    def _ok(y: np.ndarray) -> bool:
        return bool(np.all(np.isfinite(y)))

    print("=== seed L_V (derived init, discharge rep cond) ===")
    print("  ", [f"{v:.4f}" for v in model.seed_L_V])

    print("=== equilibrium (|I|->0 baseline; U from dH_rxn/dS_rxn) ===")
    yeq = model.equilibrium(V, T=298.15)
    print(f"  min={np.min(yeq):.3f} max={np.max(yeq):.3f} finite={_ok(yeq)}")
    for tr in GRAPHITE_STAGING_LIT:
        U298 = float(func_U_j(298.15, tr['dH_rxn'], tr['dS_rxn']))
        print(f"    U(298)={U298:.3f} V  (target {tr['U']:.3f})")

    print("=== discharge/charge x C-rate (Q_cell=1.0) @298K ===")
    all_ok = True
    for s, name in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            y = model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s)
            all_ok &= _ok(y)
            neg = bool(np.any(y < -1e-9))
            print(f"  {name} I={I:>4}: min={np.min(y):7.3f} max={np.max(y):7.3f} "
                  f"peak@V={V[np.argmax(y)]:.3f} neg={neg} finite={_ok(y)}")

    print("=== temperature dependence (discharge 0.2C) ===")
    for Tk in (258.15, 298.15, 318.15):
        y = model.dqdv(V, T=Tk, I_abs=0.2, Q_cell=1.0, s=+1)
        all_ok &= _ok(y)
        print(f"  {Tk-273.15:+5.0f}C: max={np.max(y):7.3f} peak@V={V[np.argmax(y)]:.3f} finite={_ok(y)}")

    print("=== T(V) non-isothermal profile ===")
    Tprof = np.linspace(288.15, 308.15, V.size)
    yT = model.dqdv(V, T=Tprof, I_abs=0.2, Q_cell=1.0, s=+1)
    all_ok &= _ok(yT)
    print(f"  finite={_ok(yT)} max={np.max(yT):.3f}")

    # ---- (C) facade : curve() with experiment conditions ----
    print("=== (C) facade curve(): C-rate + direction string ===")
    yc_dis = model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15)
    yc_chg = model.curve(V, direction="charge", c_rate=0.2, Q_cell=1.0, T=298.15)
    yc_ref = model.dqdv(V, T=298.15, I_abs=0.2, Q_cell=1.0, s=+1)
    match = float(np.max(np.abs(yc_dis - yc_ref)))
    all_ok &= (_ok(yc_dis) and _ok(yc_chg) and match < 1e-12)
    print(f"  curve(dis,0.2C) == dqdv(I=0.2,s=+1)? max_diff={match:.2e} (expect ~0)")
    print(f"  curve(chg) peak@V={V[np.argmax(yc_chg)]:.3f}  finite={_ok(yc_chg)}")
    # sto convenience: |I| via I_abs override, sto axis = V here (q->V mapping is user's)
    yc_I = model.curve(V, direction="d", I_abs=0.2, Q_cell=2.0, T=298.15)
    all_ok &= _ok(yc_I)
    print(f"  curve(I_abs override) finite={_ok(yc_I)}")

    # ---- (A) chi_split : injectable rule (default vs custom) ----
    print("=== (A) injectable chi_split rule ===")
    m_def = GraphiteAnodeDischargeDQDV(
        [{'U': 0.12, 'w': 0.014, 'Q': 0.5, 'Omega': 10000.0,
          'dH_a': 44000.0, 'dVdq_qa': 0.30}], chi=0.5)
    # custom rule: asymmetric split (charge gets 0.3 instead of 1-chi)
    custom = lambda chi, sd: chi if sd >= 0 else 0.3
    m_cus = GraphiteAnodeDischargeDQDV(
        [{'U': 0.12, 'w': 0.014, 'Q': 0.5, 'Omega': 10000.0,
          'dH_a': 44000.0, 'dVdq_qa': 0.30}], chi=0.5, chi_split=custom)
    Ld_def = m_def._resolve_lag_length(m_def.transitions[0], 298.15, 0.5, 1.0, 1.0, -1)
    Ld_cus = m_cus._resolve_lag_length(m_cus.transitions[0], 298.15, 0.5, 1.0, 1.0, -1)
    print(f"  charge L_V default(1-chi=0.5)={Ld_def:.4e}  custom(0.3)={Ld_cus:.4e}  "
          f"differ={abs(Ld_def-Ld_cus) > 1e-12}")

    print("=== HYSTERESIS branch (gamma>0): dis peak vs chg peak split ===")
    hys = GraphiteAnodeDischargeDQDV(
        [{'U': 0.12, 'w': 0.014, 'Q': 0.5, 'Omega': 12000.0, 'gamma': 1.0}],
        x=0.5, Rn=0.0, Cbg=0.0)
    yhd = hys.dqdv(V, T=298.15, I_abs=1e-4, Q_cell=1.0, s=+1)
    yhc = hys.dqdv(V, T=298.15, I_abs=1e-4, Q_cell=1.0, s=-1)
    Vd, Vc = V[np.argmax(yhd)], V[np.argmax(yhc)]
    dU = func_dU_hys(298.15, 12000.0)
    print(f"  dU_hys={dU*1000:.1f} mV  dis peak@V={Vd:.4f}  chg peak@V={Vc:.4f}  "
          f"d(dis-chg)={(Vd-Vc)*1000:+.1f} mV (expect +gamma*dU_hys={dU*1000:+.1f})")

    print("=== TAIL direction reversal (direct L_V): dis/chg opposite sides ===")
    demo = GraphiteAnodeDischargeDQDV(
        [{'U': 0.12, 'w': 0.014, 'Q': 0.5, 'L_V': 0.02}], x=0.5, Rn=0.0, Cbg=0.0)
    yad = demo.dqdv(V, T=298.15, I_abs=0.5, Q_cell=1.0, s=+1)
    yac = demo.dqdv(V, T=298.15, I_abs=0.5, Q_cell=1.0, s=-1)
    nd = bool(np.any(yad < -1e-9)); nc = bool(np.any(yac < -1e-9))
    print(f"  dis: peak@V={V[np.argmax(yad)]:.3f}  neg={nd}")
    print(f"  chg: peak@V={V[np.argmax(yac)]:.3f}  neg={nc}")

    print("=== reduction checks (limits) ===")
    # Omega<=2RT -> gap 0
    g0 = func_dU_hys(298.15, 2.0 * R * 298.15)
    print(f"  Omega=2RT -> dU_hys={g0:.3e} (expect 0)")
    # |I|->0 -> dis/chg curves coincide (gamma=0 transition)
    m0 = GraphiteAnodeDischargeDQDV([{'U': 0.12, 'w': 0.014, 'Q': 0.5}], Cbg=0.0)
    a = m0.dqdv(V, T=298.15, I_abs=1e-6, Q_cell=1.0, s=+1)
    b = m0.dqdv(V, T=298.15, I_abs=1e-6, Q_cell=1.0, s=-1)
    print(f"  gamma=0,|I|->0: dis/chg max diff={np.max(np.abs(a-b)):.3e} (expect ~0)")

    # ---- (B) finite/range guards ----
    print("=== (B) input guards (expect ValueError each) ===")
    guard_hits = 0
    for label, fn in [
        ("T<=0", lambda: model.dqdv(V, T=0.0, I_abs=0.1, Q_cell=1.0, s=+1)),
        ("Q_cell<=0", lambda: model.dqdv(V, T=298.15, I_abs=0.1, Q_cell=0.0, s=+1)),
        ("I_abs<0", lambda: model.dqdv(V, T=298.15, I_abs=-0.1, Q_cell=1.0, s=+1)),
        ("T NaN", lambda: model.dqdv(V, T=np.nan, I_abs=0.1, Q_cell=1.0, s=+1)),
        ("bad direction", lambda: model.curve(V, direction="sideways")),
        ("z_cut<=0 ctor", lambda: GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_LIT, z_cut=0.0)),
        ("L_V inf in dict", lambda: GraphiteAnodeDischargeDQDV(
            [{'U': 0.12, 'Q': 0.5, 'L_V': np.inf}]).dqdv(V, 298.15, 0.5, 1.0)),
    ]:
        try:
            fn(); print(f"  [MISS] {label}: no error raised")
        except (ValueError, TypeError):
            guard_hits += 1
    print(f"  guards fired: {guard_hits}/7")

    # ---- per-transition override isolation (v11 회귀 가드) ----
    print("=== per-tr override isolation (z_cut on tr[0] only) ===")
    _base = [{'U': 0.12, 'Q': 0.5, 'Omega': 10000.0, 'dH_a': 44000.0, 'dVdq_qa': 0.30},
             {'U': 0.20, 'Q': 0.5, 'Omega': 10000.0, 'dH_a': 44000.0, 'dVdq_qa': 0.30}]
    m_b = GraphiteAnodeDischargeDQDV([dict(t) for t in _base])
    m_o = GraphiteAnodeDischargeDQDV([dict(_base[0], z_cut=2.0), dict(_base[1])])
    L0b = m_b._resolve_lag_length(m_b.transitions[0], 298.15, 0.5, 1.0, 1.0, +1)
    L0o = m_o._resolve_lag_length(m_o.transitions[0], 298.15, 0.5, 1.0, 1.0, +1)
    L1b = m_b._resolve_lag_length(m_b.transitions[1], 298.15, 0.5, 1.0, 1.0, +1)
    L1o = m_o._resolve_lag_length(m_o.transitions[1], 298.15, 0.5, 1.0, 1.0, +1)
    iso = (abs(L0b - L0o) > 1e-15) and (abs(L1b - L1o) < 1e-18)
    print(f"  tr[0] z_cut override -> only tr[0] changes: {iso}")
    print(f"    L0 {L0b:.3e}->{L0o:.3e} (diff)   L1 {L1b:.3e}=={L1o:.3e} (same)")
    all_ok &= iso

    all_ok &= (guard_hits == 7)
    print(f"\n>>> overall OK: {all_ok}  (no exception => reached here)")
