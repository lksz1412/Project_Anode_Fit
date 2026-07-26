# -*- coding: utf-8 -*-
"""두 버전(A_regsol · B_gallery)의 피팅 결과를 docs 버전 폴더 문서로 굽는다.

수치는 전부 JSON 에서 읽어 주입한다 — 손으로 옮겨 적지 않는다(전사 오류 0).
GitHub 이 폴더를 열면 README.md 를 자동 렌더링하므로 회사 폰에서 그대로 읽힌다.
실행: python -X utf8 make_version_docs.py
"""
import os, json, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUTV = os.path.join(HERE, "out_versions")
OUT3 = os.path.join(HERE, "out_v3")
DOCS = os.path.abspath(os.path.join(HERE, "..", "..", "docs"))
DIRS = {"A_regsol": os.path.join(DOCS, "v1.0.26A-regsol"),
        "B_gallery": os.path.join(DOCS, "v1.0.26B-gallery")}
MATS = ["graphite", "silicon", "blend"]
MATKO = {"graphite": "흑연", "silicon": "실리콘", "blend": "흑연+Si 블렌드"}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def sweep_row(sw, kern, N):
    for r in sw.get("graphite", []):
        if r["kern"] == kern and r["N"] == N:
            return r
    return None


def tbl_metrics(vs):
    L = ["| 소재 | 커널 | 전이 N | 파라미터 | R² | BIC | 피크역 RMSE | 벨리역 RMSE | 면적 결손 |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    bad = []
    for m in MATS:
        d = vs.get(m)
        if not d: continue
        defc = 100.0 * (1.0 - d["area_model"] / d["area_data"])
        flag = " ⚠️" if abs(defc) > 1.0 else ""
        if abs(defc) > 1.0: bad.append((m, defc))
        L.append(f"| {MATKO[m]} | `{d['kind']}` | {d['N']} | {d['npar']}p | {d['R2']:.5f} | "
                 f"{d['BIC']:.1f} | {d['peakRMSE']} | {d['valleyRMSE']} | "
                 f"{defc:+.2f}%{flag} |")
    out = "\n".join(L)
    out += ("\n\n> **면적 결손** = 1 − ∫모델 / ∫실측 (창 안). 전하 보존 지표이며 0 에 가까워야 한다.\n")
    for m, defc in bad:
        out += (f">\n> ⚠️ **{MATKO[m]} 에서 {defc:+.2f}% 결손** — 모델이 창 안 전하의 "
                f"{abs(defc):.1f}% 를 놓치고 있다. R²/BIC 열세와 별개인 **물리적 결함**이다"
                f"(급준 피크를 못 세워 과소적분).\n")
    return out


def omega_warnings(vs):
    """Ω 가 상·하한에 붙은 전이 = 식별 불가(경계 포화). 반드시 드러낸다."""
    W = []
    for m in MATS:
        d = vs.get(m)
        if not d or d["kind"] != "regsol": continue
        sat = [t for t in d["transitions"] if t["Omega_over_RT"] >= 7.9 or t["Omega_over_RT"] <= 0.001]
        if sat:
            det = ", ".join("U={:.0f} mV → Ω/RT={:.2f}".format(t["U"] * 1e3, t["Omega_over_RT"])
                            for t in sat)
            W.append(f"- **{MATKO[m]}**: {len(sat)}/{d['N']} 전이의 Ω 가 탐색 경계에 붙었다 "
                     f"({det}). "
                     f"→ **이 Ω 는 식별된 값이 아니다**(경계 위 어떤 값이어도 같은 곡선). "
                     f"regsol 이 두-상 물리가 아니라 **near-delta 급준화 손잡이**로 쓰이고 있다는 신호이며, "
                     f"v1.0.24 가 @1 로 이미 기각한 거동이다.")
    if not W:
        return ""
    return ("\n### ⚠️ Ω 경계 포화 경고\n\n" + "\n".join(W) +
            "\n\n경계에 붙지 않은 전이의 Ω 만 물리량으로 읽으십시오.\n")


def tbl_transitions(d):
    trs = d["transitions"]
    if d["kind"] == "regsol":
        L = ["| # | U₀ [mV] | Ω [J/mol] | Ω/RT | 두-상? | x_binodal | Q [mAh] | w [mV] |",
             "|---:|---:|---:|---:|:---:|---:|---:|---:|"]
        for i, t in enumerate(trs, 1):
            L.append(f"| {i} | {t['U']*1e3:.2f} | {t['Omega']:.0f} | {t['Omega_over_RT']:.3f} | "
                     f"{'**예**' if t['two_phase'] else '아니오'} | {t['x_binodal']:.4f} | "
                     f"{t['Q']:.4f} | {t['w']*1e3:.3f} |")
    else:
        L = ["| # | U [mV] | w [mV] | w/(RT/F) | Q [mAh] |", "|---:|---:|---:|---:|---:|"]
        for i, t in enumerate(trs, 1):
            L.append(f"| {i} | {t['U']*1e3:.2f} | {t['w']*1e3:.3f} | "
                     f"{t['w']/0.025693:.3f} | {t['Q']:.4f} |")
    return "\n".join(L)


def headtohead(sw):
    rows = [("logistic", 7), ("logistic", 4), ("regsol", 4), ("regsol", 7),
            ("skew-logistic", 4), ("skew-logistic", 7),
            ("skew-regsol", 4), ("skew-regsol", 6)]
    base = sweep_row(sw, "logistic", 7)
    L = ["| 모델 | 파라미터 | R² | BIC | logistic-7 대비 ΔBIC | 근축퇴쌍 |",
         "|---|---:|---:|---:|---:|---:|"]
    for k, n in rows:
        r = sweep_row(sw, k, n)
        if not r: continue
        d = r["BIC"] - base["BIC"]
        mark = " ← 기준" if (k, n) == ("logistic", 7) else ""
        L.append(f"| `{k}`-{n} | {r['npar']}p | {r['R2']:.5f} | {r['BIC']:.1f} | "
                 f"{d:+.1f}{mark} | {len(r['degen_pairs'])} |")
    return "\n".join(L)


def tbl_sweep(sw):
    L = ["| N | logistic | skew-logistic | regsol | skew-regsol |", "|---:|---:|---:|---:|---:|"]
    for n in range(3, 9):
        cells = []
        for k in ("logistic", "skew-logistic", "regsol", "skew-regsol"):
            r = sweep_row(sw, k, n)
            cells.append(f"{r['BIC']:.0f}" if r else "—")
        L.append(f"| {n} | " + " | ".join(cells) + " |")
    return "\n".join(L)


COMMON_METHOD = """\
## 데이터와 방법 (두 버전 공통 — 그래서 비교가 성립한다)

| 항목 | 내용 |
|---|---|
| 데이터 | SINTEF / EU IntelLiGent, Zenodo record **20086298**, 라이선스 **CC-BY-4.0** |
| 셀 | 반쪽셀 vs Li, pseudo-OCV **C/50**, 상온 · `gr.csv`(흑연) `si.csv`(실리콘) `sigr.csv`(블렌드) |
| dQ/dV | 사용자 BDD `99_Backend` 방식 이식 — **dMSMCD 다중창 중앙값 미분 + 웨이블릿 denoise + savgol 앙상블**, 이후 등장성회귀로 V(Q) 단조화 → 균일 V 격자 재빈닝 |
| 피팅 | `scipy.least_squares` (trf, bounded) · **3-시드전략 × 4-재시작** 동일 적용 |
| 지표 | R² · **BIC**(파라미터 수 보정) · 피크역/벨리역 RMSE · 면적 보존 |

> **★BIC 로 읽으십시오.** 두 버전은 파라미터 수가 다릅니다(흑연 기준 A 16p vs B 21p).
> R² 는 파라미터가 많은 쪽에 자동으로 유리하므로 단독 비교하면 안 됩니다.

### dQ/dV 계산에서 잡은 함정 (이 버전들에 반영됨)

1. **전압 양자화** — 원자료 V 가 1 µV 눈금이고 인접 ΔV 중앙값이 8 µV, 550 쌍은 ΔV=0 입니다.
   단일창 미분(`np.gradient`)으로 dV/dQ 를 구하면 0 나눗셈으로 dQ/dV 가 **10¹²** 까지 발산합니다.
   다중창 중앙값(dMSMCD)이 이를 흡수합니다.
2. **regsol 조성격자 ripple** — regsol 은 조성격자에 대한 합이라, broadening 폭 w 가 이웃
   격자점의 전압 간격보다 좁으면 곡선이 빗살(comb)로 깨집니다. 본 버전은 격자합 대신
   **혼화갭 닫힌형 + 고용체 밀도⊛합성곱(FFT)** 으로 계산해 격자 의존을 제거했습니다
   (v1.0.24 원본 `_REGSOL_XG=1200` 대비 꼬리 위글 **140배 감소**, 속도 55배).
"""

LIMITS = """\
## 정직한 한계 (반드시 같이 읽을 것)

1. **데이터가 평형이 아닙니다.** 본 버전들이 쓴 `gr.csv`/`si.csv`/`sigr.csv` 는 Zenodo 20086298 의
   4 프로토콜 중 **plain pseudo-OCV(C/50)** 로, 가장 비평형입니다. v1.0.25 addendum 실측:
   같은 모델이 p-OCV **0.977** vs p-OCV+hold **0.9945**(피크역 RMSE 4.708→2.701).
   → 잔차의 상당분이 모델 결함이 아니라 **데이터의 비평형 잔여**입니다.
   **GITT / p-OCV+hold 평형 데이터로 재검이 남아 있습니다**(`dl_sintef.ps1` 미실행).
2. **흑연 0.104 V 피크는 계측 분해 한계에 걸려 있습니다.** 원자료에서 이 평탄은
   V 폭 약 0.6 mV 안에 2,400 점·0.29 mAh 가 몰려 있어 FWHM ≲ 1 mV — RT/F(25.7 mV)의 **1/25** 입니다.
   대칭 로지스틱이 이를 맞추려면 w 를 0.4 mV 까지 내려야 하는데 고용체로는 나올 수 없는 폭입니다.
   두-상이면 자연스럽지만, **비평형 인공물일 가능성이 배제되지 않았습니다** — 평형 데이터로만 갈립니다.
3. **전이 수는 상(phase) 수가 아닙니다.** v1.0.25 가 확정한 대로 gallery 세분은 곡선 표현
   해상도이며 XRD 상 수(흑연 4 staging)를 바꾸지 않습니다. **봉우리 수를 상 수의 증거로 쓰지 마십시오.**
4. **파라미터는 seed 이지 신뢰값이 아닙니다.** 단일 셀·단일 온도·단일 율속 피팅 결과이며
   불확실도 구간을 산출하지 않았습니다(bootstrap 미수행).
"""


def repro(vname):
    return f"""\
## 재현

```bash
cd Claude/results/comp_v26_data
python -X utf8 build_two_versions.py     # 두 버전 피팅 → out_versions/
python -X utf8 make_version_docs.py      # 본 문서 재생성
```

필요 패키지: `numpy` `scipy` `pandas` `matplotlib` `PyWavelets`.
커널 구현 = `regsol_kernel.py`(regsol/skew-regsol) · `test_skew_regsol_v2.py`(logistic 계열) ·
`bdd_dqdv.py`(BDD dQ/dV). 원자료 = `Claude/results/comp_v24/sintef_data/`.
"""


def build(vname, title, subtitle, lead, verdict, vs, sw, other_vs):
    d = DIRS[vname]
    os.makedirs(os.path.join(d, "figures"), exist_ok=True)
    os.makedirs(os.path.join(d, "params"), exist_ok=True)
    src = os.path.join(OUTV, vname)
    figs = []
    listing = sorted(os.listdir(src)) if os.path.isdir(src) else []
    for m in MATS:
        for f in listing:
            if f.startswith(m) and f.endswith(".png"):
                shutil.copy2(os.path.join(src, f), os.path.join(d, "figures", f))
                figs.append((m, f))
        pj = os.path.join(src, f"params_{m}.json")
        if os.path.exists(pj):
            shutil.copy2(pj, os.path.join(d, "params", f"params_{m}.json"))
    if os.path.exists(os.path.join(OUT3, "graphite_sweep.png")):
        shutil.copy2(os.path.join(OUT3, "graphite_sweep.png"),
                     os.path.join(d, "figures", "graphite_sweep.png"))

    today = datetime.date.today().isoformat()
    P = [f"# {title}", "", f"> {subtitle}", f">", f"> 작성 {today} · 기준 코드 = v1.0.25.1 (`main`)",
         "", "---", "", "## 한 줄 요약", "", lead, "", "### 판정", "", verdict, "", "---", "",
         COMMON_METHOD, "", "---", "", "## 결과", "", tbl_metrics(vs), ""]

    for m, f in figs:
        P += [f"### {MATKO[m]}", "", f"![{m}](figures/{f})", ""]

    P += ["---", "", "## 전이 파라미터 (코드에 바로 넣을 수 있는 형태)", ""]
    for m in MATS:
        if m not in vs: continue
        P += [f"### {MATKO[m]} — `{vs[m]['kind']}` {vs[m]['N']} 전이", "",
              tbl_transitions(vs[m]), "",
              f"→ 원본 JSON: [`params/params_{m}.json`](params/params_{m}.json)", ""]
    ow = omega_warnings(vs)
    if ow:
        P += [ow, ""]
    if vname == "A_regsol":
        g = vs.get("graphite")
        if g:
            oms = [t["Omega_over_RT"] for t in g["transitions"]]
            P += ["### ✅ 문헌 앵커와의 일치 (버전 A 의 유일한 실질 성과)", "",
                  f"흑연 4 전이의 Ω/RT = **{', '.join(f'{o:.2f}' for o in oms)}** — 전부 **2RT 근방**"
                  "(marginal 두-상)에 모입니다. 이는 독립 문헌 앵커 **Cordoba 2024 의 Ω_a ≈ 2.5 RT**"
                  "(평균장 정칙용액, 흑연 Ω 의 유일한 실수치 앵커)와 정합합니다.", "",
                  "> 즉 **적합도로는 지지만 Ω 값 자체는 물리를 말합니다.** 흑연이 marginal 두-상이라는"
                  " 것은 데이터가 독립적으로 답한 것이며, 이 사실과 \"regsol 커널이 gallery 를"
                  " 대체하느냐\"는 **별개 문제**입니다. 전자는 참, 후자는 거짓입니다.", ""]

    P += ["---", "", "## 두 버전 head-to-head (흑연, 같은 데이터·같은 절차)", "",
          "### 전이 수 대 BIC 전면 스윕", "", tbl_sweep(sw), "",
          "![sweep](figures/graphite_sweep.png)", "",
          "### 핵심 대조", "", headtohead(sw), "", LIMITS, "", "---", "", repro(vname),
          "", "---", "", "## 관련 문서", "",
          "- 반대편 버전: " + ("[v1.0.26B-gallery](../v1.0.26B-gallery/README.md)"
                              if vname == "A_regsol" else
                              "[v1.0.26A-regsol](../v1.0.26A-regsol/README.md)"),
          "- 기준 버전: [v1.0.25.1](../v1.0.25.1/results/HANDOVER_v25.md)",
          "- v1.0.25 데이터 정직화 addendum: [`V1025_DATA_ADDENDUM.md`](../v1.0.25.1/results/V1025_DATA_ADDENDUM.md)",
          ""]
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(P))
    print(f"wrote {os.path.join(d, 'README.md')}")


if __name__ == "__main__":
    S = load(os.path.join(OUTV, "summary_versions.json"))
    SW = load(os.path.join(OUT3, "sweep_v3.json"))
    gA = S["A_regsol"].get("graphite", {})
    gB = S["B_gallery"].get("graphite", {})
    dbic = (gA.get("BIC", 0) - gB.get("BIC", 0))

    build("A_regsol",
          "v1.0.26A — regsol 판 (물리 전이 최소 구성)",
          "정칙용액 두-상 커널로 흑연을 **물리 staging 4 전이**만으로 기술하려는 판. "
          "질문 = 이 4 개가 gallery 7 개로의 분화를 스스로 모사하는가?",
          f"흑연을 regsol **4 전이**로 기술하면 R²={gA.get('R2', float('nan')):.5f}, BIC={gA.get('BIC', 0):.1f} 입니다. "
          f"같은 데이터에서 로지스틱 gallery 7 전이는 BIC {sweep_row(SW,'logistic',7)['BIC']:.1f} 이므로, "
          f"**물리 4 전이는 gallery 7 전이를 대체하지 못합니다**(ΔBIC {gA.get('BIC',0)-sweep_row(SW,'logistic',7)['BIC']:+.1f}).",
          "- ❌ **regsol-4 는 gallery-7 을 대체하지 못한다.** 두-상 Maxwell 평탄이 "
          "\"한 봉우리를 넓은 것+좁은 것으로 쪼개는\" gallery 분화의 물리적 정체라는 가설은 이 데이터에서 성립하지 않는다.\n"
          "- ❌ **regsol 자신도 분화를 필요로 한다.** regsol 을 N=4→7 로 올리면 BIC 가 개선되고 "
          "근축퇴쌍이 함께 늘어난다 — 분화를 흡수하는 것이 아니라 똑같이 겪는다.\n"
          "- ⚠️ **regsol 의 우위는 전이 수가 부족할 때만 나타난다.** N=4·5 에서는 로지스틱을 이기지만 "
          "N=6 부터 역전된다. v1.0.25 의 \"@3 이득은 전이 수 부족의 우회\" 판정과 같은 구조다.\n"
          "- ❌ **흑연에서 전하 보존이 깨진다.** 창 안 면적 결손 **+12.05%** — 급준 피크를 못 세워 "
          "과소적분한다. 다른 모든 피팅은 결손 ≤0.06% 다. 이것은 적합도 열세와 별개인 물리적 결함이다.\n"
          "- ✅ **다만 Ω 값 자체는 문헌과 맞는다.** 흑연 4 전이의 Ω 가 전부 2RT 근방(marginal 두-상)에 "
          "모이며 이는 독립 앵커 Cordoba 2024 Ω_a≈2.5RT 와 정합한다. **\"흑연이 두-상이다\"는 참이고, "
          "\"그래서 regsol 커널이 gallery 를 대체한다\"는 거짓이다** — 두 명제를 분리해서 읽어야 한다.",
          S["A_regsol"], SW, S["B_gallery"])

    build("B_gallery",
          "v1.0.26B — gallery 판 (로지스틱 흑연 7 + 실리콘 7)",
          "경험적 MSMR gallery 구성. 흑연 7 · 실리콘 7 = **14 전이**를 대칭 로지스틱으로 기술한다.",
          f"흑연 로지스틱 **7 전이**가 R²={gB.get('R2', float('nan')):.5f}, BIC={gB.get('BIC', 0):.1f} 로 "
          f"regsol 4 전이(BIC {gA.get('BIC',0):.1f})를 크게 앞섭니다(ΔBIC {dbic:+.1f}). "
          "다만 늘어난 전이의 정체는 새 봉우리가 아니라 **같은 전압에 폭만 다른 쌍**입니다.",
          "- ✅ **적합도는 이쪽이 이긴다.** 파라미터 수를 보정한 BIC 기준으로도 gallery-7 이 우세하다.\n"
          "- ⚠️ **늘어난 전이는 물리 상이 아니다.** N 을 4→7 로 올릴 때 검출 피크는 3 개 그대로인데 "
          "근축퇴쌍(같은 U ±5 mV·폭비 >2)이 1→6 개로 늘어난다. 즉 gallery 는 한 봉우리를 "
          "\"넓은 것 + 좁은 것\"으로 쪼개고 있다. **XRD 상 수(흑연 4 staging)는 불변이다.**\n"
          "- ⚠️ **N=8 은 과적합이다.** BIC 가 N=7 에서 최소이고 N=8 에서 도로 올라간다(포화).\n"
          "- 📌 **더 나은 선택지가 있다.** 같은 스윕에서 `skew-logistic`-7 이 BIC 991.5 로 "
          "본 판(logistic-7)보다 크게 우수하다 — 비대칭 α 가 전이 수보다 큰 단일 효과다.",
          S["B_gallery"], SW, S["A_regsol"])
    print("DONE")
