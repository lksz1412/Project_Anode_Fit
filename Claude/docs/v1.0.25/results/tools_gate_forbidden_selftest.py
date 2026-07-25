# -*- coding: utf-8 -*-
"""G-금지 게이트가 공허하지 않은지 검사 — 음성(위반 탐지) + 면제(금지 서술 통과) 시험.

RULES 는 test_gates_v1025.py 의 gate_forbidden() 과 동일해야 한다(수동 동기).
"""
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RULES = {
    "C5-a": (r"이 한 식으로 연속화", None),
    "C5-b": (r"(?:w_\\?\\?eff[^\n]{0,24}(?:유효\s*폭|반높이\s*폭|폭으로 읽)"
             r"|(?:유효\s*폭|반높이\s*폭)[^\n]{0,24}w_\\?\\?eff)",
             r"(금지|아니|말 것|않는다|안\s?된다|오독|주의|한정|과대|3/2|중심 \\emph\{높이\})"),
    "C5-c": (r"w_\\eff\(\\?Omega\)|w_\\mathrm\{eff\}\(\\Omega\)",
             r"(금지|쓰지 않는다|한정|허용이다|별개)"),
    "C6":   (r"kernel'?\s*[:=]\s*'?regsol|채택 커널.{0,12}Frumkin",
             r"(삭제|미채택|미구현|무시|아니)"),
}

BAD = [   # 미래 저자가 되살릴 수 있는 형태 → 전건 '탐지' 되어야 한다
    ("C5-a", r"폭식의 이중지위가 이 한 식으로 연속화된다."),
    ("C5-b", r"단일상 peak 의 유효 폭은 $w_\eff=(RT/F)(1-\Omega/2RT)$ 이다."),
    ("C5-b", r"$w_\eff$ 를 반높이 폭으로 삼아 피팅한다."),
    ("C5-c", r"두-상 폭에 $w_\eff(\Omega)$ 축소식을 쓴다."),
    ("C6",   r"전이에 kernel='regsol' 을 주어 채택 경로로 계산한다."),
]
GOOD = [  # 금지를 서술·정정하는 형태 → 전건 '통과'(면제) 되어야 한다
    ("C5-b", r"그러나 이 $w_\eff$ 를 \emph{반높이 폭}으로 읽어서는 안 된다."),
    ("C5-b", r"정확히 재는 것은 중심 \emph{높이} $Q/(4w_\eff)$ 이고 반높이 폭은 $\lambda^{3/2}$"),
    ("C5-c", r"본 장은 두-상 폭에 $w_\eff(\Omega)$ 류를 쓰지 않는다(두-상 폭 한정 재도입 금지)."),
    ("C6",   r"'kernel':'regsol' 키가 남아 있어도 무시된다(= 로지스틱)."),
]


def fires(lab, line):
    pat, exc = RULES[lab]
    rx = re.compile(pat)
    rxe = re.compile(exc) if exc else None
    return bool(rx.search(line) and not (rxe and rxe.search(line)))


print("=== 음성 시험: 위반이어야 하는 문장 (전건 '탐지' 기대) ===")
miss = 0
for lab, s in BAD:
    f = fires(lab, s)
    miss += (0 if f else 1)
    print(f"  [{'탐지  ' if f else '**놓침**'}] {lab}  {s[:64]}")
print()
print("=== 면제 시험: 금지를 서술하는 문장 (전건 '통과' 기대) ===")
fp = 0
for lab, s in GOOD:
    f = fires(lab, s)
    fp += (1 if f else 0)
    print(f"  [{'**오탐**' if f else '통과  '}] {lab}  {s[:64]}")
print()
ok = (miss == 0 and fp == 0)
print(f"결론: 놓침 {miss}건 · 오탐 {fp}건 → G-금지 게이트 = "
      f"{'유효(비-공허)' if ok else '★보정 필요'}")
sys.exit(0 if ok else 1)
