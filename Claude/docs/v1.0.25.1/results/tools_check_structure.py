#!/usr/bin/env python3
# tools_check_structure.py — v1.0.20 구조 검증 + 변경 통제 스냅샷 도구
# 용도:
#   (1) check: 라벨 중복 / \ref·\eqref 미해소 / \cite↔\bibitem 불일치 / \begin·\end 짝 / 자산 앵커 수
#   (2) snapshot: eq 라벨 집합 + 수식 환경(특히 \boxed 포함) 정규화 해시 → JSON
#   (3) diff: 두 snapshot JSON 비교 → 추가/삭제/변경 라벨·블록 목록 (CHANGE_LOG 대조용)
# 사용:
#   python3 tools_check_structure.py check   <chapter-root> <master.tex> [master2.tex ...]
#   python3 tools_check_structure.py snapshot <chapter-root> <out.json> <master.tex> [...]
#   python3 tools_check_structure.py diff <old.json> <new.json>
import sys, re, json, hashlib, os

MATH_ENVS = ("equation", "align", "gather", "multline", "eqnarray", "alignat")

def resolve_inputs(root, master):
    """master tex 의 \\input 을 따라 파일 목록(순서대로) 반환."""
    files, seen = [], set()
    def walk(path):
        if path in seen: return
        seen.add(path); files.append(path)
        try:
            txt = open(path, encoding="utf-8").read()
        except FileNotFoundError:
            print(f"[WARN] missing input: {path}"); return
        for m in re.finditer(r"^\s*\\input\{([^}]+)\}", txt, re.M):
            sub = m.group(1)
            if not sub.endswith(".tex"): sub += ".tex"
            walk(os.path.join(root, sub))
    walk(os.path.join(root, master))
    return files

def strip_comments(text):
    # 각 줄에서 비이스케이프 % 이후 제거 (자산 앵커 스캔은 원문 사용)
    out = []
    for line in text.split("\n"):
        r, i = [], 0
        while i < len(line):
            c = line[i]
            if c == "\\" and i + 1 < len(line):
                r.append(line[i:i+2]); i += 2; continue
            if c == "%": break
            r.append(c); i += 1
        out.append("".join(r))
    return "\n".join(out)

def collect(files):
    labels, label_locs = [], {}
    refs, cites, bibitems = [], [], []
    env_errors, asset_tags = [], []
    eqblocks = []  # (labels_in_block, normalized_hash, has_boxed, file, lineno)
    for path in files:
        raw = open(path, encoding="utf-8").read()
        txt = strip_comments(raw)
        for m in re.finditer(r"% 자산: (.+)$", raw, re.M):
            asset_tags += re.findall(r"\[([A-Z0-9\-]+)\]", m.group(1))
        for m in re.finditer(r"\\label\{([^}]+)\}", txt):
            labels.append(m.group(1))
            label_locs.setdefault(m.group(1), []).append(f"{os.path.basename(path)}:{txt[:m.start()].count(chr(10))+1}")
        for m in re.finditer(r"\\(?:eqref|ref|pageref|cref)\{([^}]+)\}", txt):
            refs.append(m.group(1))
        for m in re.finditer(r"\\cite[tp]?\{([^}]+)\}", txt, re.S):
            for k in m.group(1).replace("\n", " ").split(","):
                cites.append(k.strip())
        for m in re.finditer(r"\\bibitem\{([^}]+)\}", txt):
            bibitems.append(m.group(1))
        # env pairing (per file)
        stack = []
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", txt):
            kind, env = m.group(1), m.group(2)
            line = txt[:m.start()].count("\n") + 1
            if kind == "begin": stack.append((env, line))
            else:
                if not stack or stack[-1][0] != env:
                    env_errors.append(f"{os.path.basename(path)}:{line} \\end{{{env}}} 짝 오류 (stack={stack[-3:]})")
                    if stack and stack[-1][0] != env:  # try recovery
                        continue
                else: stack.pop()
        for env, line in stack:
            env_errors.append(f"{os.path.basename(path)}:{line} \\begin{{{env}}} 미닫힘")
        # math env blocks
        for m in re.finditer(r"\\begin\{(" + "|".join(MATH_ENVS) + r")\*?\}(.*?)\\end\{\1\*?\}", txt, re.S):
            body = m.group(2)
            blabels = re.findall(r"\\label\{([^}]+)\}", body)
            norm = re.sub(r"\s+", "", re.sub(r"\\label\{[^}]+\}", "", body))
            h = hashlib.sha1(norm.encode()).hexdigest()[:12]
            eqblocks.append({
                "labels": blabels, "hash": h, "boxed": "\\boxed" in body,
                "file": os.path.basename(path),
                "line": txt[:m.start()].count("\n") + 1,
            })
    return dict(labels=labels, label_locs=label_locs, refs=refs, cites=cites,
                bibitems=bibitems, env_errors=env_errors, asset_tags=asset_tags,
                eqblocks=eqblocks)

def do_check(root, masters):
    ok = True
    # v1.0.22 패치: 장 간 xr 참조가 설계상 존재 — unresolved 판정은 전 마스터 라벨 합집합 기준
    union_labels = set()
    for master in masters:
        union_labels |= set(collect(resolve_inputs(root, master))["labels"])
    for master in masters:
        files = resolve_inputs(root, master)
        d = collect(files)
        d["labels_union"] = union_labels
        dup = sorted({l for l in d["labels"] if d["labels"].count(l) > 1})
        PKG_LABELS = {"LastPage"}  # lastpage 패키지 제공
        unresolved_refs = sorted({r for r in d["refs"] if r not in d.get("labels_union", d["labels"]) and r not in PKG_LABELS})
        undef_cites = sorted({c for c in d["cites"] if c not in d["bibitems"]})
        uncited_bibs = sorted({b for b in d["bibitems"] if b not in d["cites"]})
        print(f"=== {master} ({len(files)} files) ===")
        print(f"labels: {len(d['labels'])} (dup: {len(dup)}) {dup[:10]}")
        print(f"refs: {len(d['refs'])} (unresolved: {len(unresolved_refs)}) {unresolved_refs[:10]}")
        print(f"cites: {len(d['cites'])} keys, bibitems: {len(d['bibitems'])} "
              f"(cite-undef: {undef_cites}, bib-uncited: {uncited_bibs})")
        print(f"env pairing errors: {len(d['env_errors'])}")
        for e in d["env_errors"][:10]: print("  " + e)
        print(f"asset anchors: {len(d['asset_tags'])} tags, unique {len(set(d['asset_tags']))}")
        print(f"math env blocks: {len(d['eqblocks'])} (boxed: {sum(1 for b in d['eqblocks'] if b['boxed'])})")
        if dup or unresolved_refs or undef_cites or d["env_errors"]: ok = False
    print("STRUCTURE_CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def do_snapshot(root, out, masters):
    snap = {}
    for master in masters:
        files = resolve_inputs(root, master)
        d = collect(files)
        snap[master] = {
            "labels": sorted(set(d["labels"])),
            "eqblocks": {(b["labels"][0] if b["labels"] else f"{b['file']}:{b['line']}"):
                         {"hash": b["hash"], "boxed": b["boxed"], "file": b["file"]}
                         for b in d["eqblocks"]},
            "asset_unique": len(set(d["asset_tags"])),
            "bibitems": sorted(set(d["bibitems"])),
        }
    json.dump(snap, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"snapshot -> {out}")
    return 0

def do_diff(old, new):
    a, b = json.load(open(old, encoding="utf-8")), json.load(open(new, encoding="utf-8"))
    rc = 0
    for master in b:
        ka = a.get(master) or a.get(master.replace("1.0.20", "1.0.19")) \
             or list(a.values())[list(b.keys()).index(master)] if a else None
        if ka is None:
            print(f"[WARN] no baseline for {master}"); continue
        la, lb = set(ka["labels"]), set(b[master]["labels"])
        print(f"=== {master} ===")
        print(f"labels +{sorted(lb-la)} -{sorted(la-lb)}")
        ea, eb = ka["eqblocks"], b[master]["eqblocks"]
        added = [k for k in eb if k not in ea]
        removed = [k for k in ea if k not in eb]
        changed = [k for k in eb if k in ea and eb[k]["hash"] != ea[k]["hash"]]
        print(f"eqblocks +{len(added)} -{len(removed)} ~{len(changed)}")
        for k in added: print(f"  + {k} ({eb[k]['file']})")
        for k in removed: print(f"  - {k} ({ea[k]['file']})")
        for k in changed: print(f"  ~ {k} ({eb[k]['file']}) boxed={eb[k]['boxed']}")
        print(f"asset_unique: {ka['asset_unique']} -> {b[master]['asset_unique']}")
        ba, bb = set(ka["bibitems"]), set(b[master]["bibitems"])
        print(f"bibitems +{sorted(bb-ba)} -{sorted(ba-bb)}")
        if removed: rc = 1  # 삭제는 자산 회귀 후보 — 반드시 CHANGE_LOG 대조
    return rc

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "check": sys.exit(do_check(sys.argv[2], sys.argv[3:]))
    elif mode == "snapshot": sys.exit(do_snapshot(sys.argv[2], sys.argv[3], sys.argv[4:]))
    elif mode == "diff": sys.exit(do_diff(sys.argv[2], sys.argv[3]))
    else: print("mode: check|snapshot|diff"); sys.exit(2)
