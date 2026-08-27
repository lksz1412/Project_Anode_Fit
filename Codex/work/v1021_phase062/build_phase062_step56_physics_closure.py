#!/usr/bin/env python3
"""Build deterministic Phase 062 Step 56 physics-closure evidence."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "c700d4ff887af6bb66f2c0118f75832202856bf8"
SENTINEL = "P062_STEP56_RESULT_FIRST_PRECOMMIT"
MATRIX = "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json"
RESULT = "Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md"
STRUCTURAL_SCHEMA_SHA = "36ec5282b3e305aae3bc9ea9f05bac146c3d4a253a2e50f4a1b08cf802104f7f"
STRUCTURAL_SCHEMA_PATHS = 5442

ALLOWLIST = [
    "Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex",
    "Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex",
]

CODE_ROWS = [
    ("ch1_appC_navaid.tex",132),("ch1_appD_si.tex",75),("ch1_sec00_intro.tex",19),
    ("ch1_sec00_intro.tex",96),("ch1_sec01_n0n1.tex",38),("ch1_sec03_center.tex",113),
    ("ch1_sec08_lag.tex",128),("ch1_sec10_sum.tex",18),("ch1_sec12_lcocenter.tex",105),
    ("ch1_sec15_lcoelec.tex",336),("ch1_sec15_lcoelec.tex",339),("ch1_sec18_inputs.tex",29),
    ("ch1_sec18_inputs.tex",36),("ch1_sec18_inputs.tex",66),("ch2_appA_traps.tex",8),
    ("ch2_appA_traps.tex",66),("ch2_appA_traps.tex",67),("ch2_bib.tex",20),
    ("ch2_sec00_intro.tex",71),("ch2_sec04_einstein.tex",96),("ch2_sec08_synthesis.tex",95),
]

def ast_canonical_value(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"node": type(value).__name__, "fields": [[name, ast_canonical_value(getattr(value, name))] for name in value._fields]}
    if isinstance(value, list): return {"list": [ast_canonical_value(item) for item in value]}
    if isinstance(value, tuple): return {"tuple": [ast_canonical_value(item) for item in value]}
    if isinstance(value, bytes): return {"bytes": value.hex()}
    if isinstance(value, complex): return {"complex": [value.real, value.imag]}
    if value is Ellipsis: return {"ellipsis": True}
    return value

def builder_full_ast_sha() -> str:
    source=Path(__file__).read_bytes().replace(b"\r\n",b"\n")
    raw=json.dumps(ast_canonical_value(ast.parse(source.decode())),ensure_ascii=False,sort_keys=False,separators=(",",":"),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()

FIGURES = [f"FF1-{i}" for i in range(1,8)] + [f"FF2-{i}" for i in range(1,6)] + \
          [f"FF3-{i}" for i in range(1,8)] + [f"FO1-{i}" for i in range(1,5)] + \
          [f"FO2-{i}" for i in range(1,5)] + [f"FO3-{i}" for i in range(1,5)]
ADOPTED_FIGURES = {
    "FF1-1": ("Claude/docs/v1.0.21/_sections/ch1_sec04_hys.tex", "fig:hysgap", [25,25], "118-226", 25),
    "FF2-1": ("Claude/docs/v1.0.21/_sections/ch2_sec08_synthesis.tex", "fig:qrevsoc", [22,22], "135-221", 31),
    "FF2-5": ("Claude/docs/v1.0.21/_sections/ch2_sec04_einstein.tex", "fig:svibid", [13,13], "106-181", 27),
    "FF3-3": ("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex", "fig:sumcurve", [44,45], "60-122", 31),
    "FO3-4": ("Claude/docs/v1.0.21/_sections/ch1_sec03_center.tex", "fig:UjT", [22,22], "61-105", 24),
}

SOURCE_IDENTITIES = [
 ("appendix", "Claude/docs/v1.0.21/appendix_phase_separation.tex", "4e17bf", "18e670", "Claude/docs/v1.0.21/appendix_phase_separation.pdf", "292c4c", "33da6e", 8),
 ("ch1_basic", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex", "45ab296", "d9e7af", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf", "72b0e92", "50746b", 76),
 ("ch1_navigation", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex", "fcb91c", "cc39dd", "Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf", "40859f", "fe544e", 78),
 ("ch2_basic", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex", "357e3d", "cb66a5", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf", "e797c5", "08a1b8", 26),
 ("ch2_navigation", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex", "d605eb", "4f9aad", "Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf", "87ae4d", "ff3163", 26),
]

BUILDS = [
 ("appendix",8,30,0,0,0,0,0,"c7773cc4f816a26bf512038bccc98e0e27eb59e9e218aeaf4a8ce65b4c40a107"),
 ("ch1_basic",76,248,0,0,0,0,2,"d277029a306832bd5d3581a24545024012a3f36a1ac39744761be739d5914aba"),
 ("ch1_navigation",78,255,0,0,0,0,4,"1d2e8432beb10040bb0ed713fb3357d9a8a2cccd008eae9a747cc18189a2a971"),
 ("ch2_basic",26,72,0,0,0,0,3,"b69491c2ab85987ef2e856f571d8e812562ec76dd194d603352db9d38af2eaa8"),
 ("ch2_navigation",26,72,0,0,0,0,3,"eff2b4ffe170c1a7c2f3f52ade30620ae0688f505ab558981d0c7e4c5e960e09"),
]

def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, text=True, encoding="utf-8", errors="strict",
                          capture_output=True, timeout=45, check=True).stdout.strip()

def blob(commit: str, path: str) -> bytes:
    return subprocess.run(["git","show",f"{commit}:{path}"],cwd=REPO,capture_output=True,timeout=45,check=True).stdout

def identity(path: str) -> dict[str, Any]:
    data = subprocess.run(["git","show",f"{BASELINE}:{path}"], cwd=REPO, capture_output=True,
                          timeout=45, check=True).stdout
    return {"path":path,"git_blob":git("rev-parse",f"{BASELINE}:{path}"),
            "sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}

def identity_at(commit: str, path: str) -> dict[str, Any]:
    data = subprocess.run(["git","show",f"{commit}:{path}"], cwd=REPO, capture_output=True,
                          timeout=45, check=True).stdout
    return {"path":path,"commit":commit,"git_blob":git("rev-parse",f"{commit}:{path}"),
            "sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}

def traversal_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + len(value) + sum(traversal_count(v) for v in value.values())
    if isinstance(value, list):
        return 1 + sum(traversal_count(v) for v in value)
    return 1

def json_evidence(path: str, schema: str, terminal: str | None = None) -> dict[str, Any]:
    value=json.loads(subprocess.run(["git","show",f"{PARENT}:{path}"],cwd=REPO,capture_output=True,
                                   timeout=45,check=True).stdout)
    row=identity_at(PARENT,path)|{"schema":schema,"traversal":traversal_count(value)}
    if terminal is not None: row["terminal"]=terminal
    return row

def anchored_line(path: str, line: int) -> dict[str, Any]:
    data=subprocess.run(["git","show",f"{BASELINE}:{path}"],cwd=REPO,capture_output=True,
                        timeout=45,check=True).stdout
    raw=data.splitlines(keepends=True)[line-1]
    return {"path":path,"line_start":line,"line_end":line,"line_text":raw.decode("utf-8").rstrip("\r\n"),
            "line_sha256":hashlib.sha256(raw).hexdigest()}

def anchored_span(path: str, start: int, end: int) -> dict[str, Any]:
    data=subprocess.run(["git","show",f"{BASELINE}:{path}"],cwd=REPO,capture_output=True,
                        timeout=45,check=True).stdout
    raw=b"".join(data.splitlines(keepends=True)[start-1:end])
    return {"path":path,"line_start":start,"line_end":end,"slice_text":raw.decode("utf-8").rstrip("\r\n"),
            "slice_sha256":hashlib.sha256(raw).hexdigest()}

def artifact() -> dict[str, Any]:
    step50=json.loads((REPO/"Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json").read_text(encoding="utf-8"))
    topology=json.loads((REPO/"Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json").read_text(encoding="utf-8"))
    routes={x["candidate_id"]:x for x in step50["figure_genealogy_routes"]}
    figures=[]
    for cid in FIGURES:
        source=routes[cid]["candidate"]
        row={"candidate_id":cid,"asset_class":"FIGURE","source_identity":identity(source["path"])|{"source_id":source["source_id"]},
             "decision":"ADOPTED" if cid in ADOPTED_FIGURES else "NON_ADOPTED",
             "decision_evidence":{"path":"Claude/docs/v1.0.20/results/FIGS_PICK_JUDGMENT.md",
               "git_blob":routes[cid]["consolidated_judgment"]["blob_sha1"],
               "sha256":routes[cid]["consolidated_judgment"]["sha256"],"route_id":routes[cid]["route_id"]},
             "individual_reviewer_vote":None,"vote_edge":"GROUND_NOT_FOUND","vote_route":"P061-STEP50-GNF-011"}
        if cid in ADOPTED_FIGURES:
            tex,label,pages,span,root_line=ADOPTED_FIGURES[cid]
            row.update({"candidate_source":row["source_identity"]["path"],"final_tex":tex,"label":label,
                        "final_line_span":span,"root_include_line":root_line,
                        "release_pages":{"basic":pages[0],"navigation":pages[1]}})
        figures.append(row)
    comp={x["source_id"]:x for x in step50["competitive_source_records"]}
    draft_ids={"Q2F1":207,"Q2F2":208,"Q2F3":209,"Q2F4":210,"Q2O1":211,"Q2O2":212,
               "Q3F1":215,"Q3F2":216,"Q3F3":217,"Q3F4":218,"Q3O1":219,"Q3O2":220}
    drafts=[]
    adopted={"Q2F1","Q2F2","Q2O1","Q3F1","Q3F2","Q3F3","Q3O1"}
    for q, countf, counto in (("Q2",4,2),("Q3",4,2)):
        for kind,n in (("F",countf),("O",counto)):
            for i in range(1,n+1):
                did=f"{q}{kind}{i}"
                record=comp[f"P061-SRC-{draft_ids[did]:04}"]
                drafts.append({"candidate_id":did,"asset_class":"TEX_DRAFT",
                    "source_identity":identity(record["path"])|{"source_id":record["source_id"]},
                    "decision":"ADOPTED_COMPOSITE_INPUT" if did in adopted else "NON_ADOPTED",
                    "decision_evidence":{"path":"Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",
                        "line":10 if q=="Q2" else 13,"state":"EXACT_ADOPTION_EDGE" if did in adopted else "NO_ADOPTION_EDGE"},
                    "final_tex":"Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex" if q=="Q2" and did in adopted else
                                "Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex" if q=="Q3" and did in adopted else None,
                    "final_line_span":"280-385" if q=="Q2" and did in adopted else
                                      "46-118" if q=="Q3" and did in adopted else None,
                    "root_include_line":23 if q=="Q2" and did in adopted else
                                        26 if q=="Q3" and did in adopted else None,
                    "release_pages":{"basic":[18,19,20],"navigation":[19,20,21]} if q=="Q2" and did in adopted else
                                    {"basic":[27],"navigation":[27]} if q=="Q3" and did in adopted else None})
    png_names=["P4_lco_heat_validation.png","anode_fit_v1_0_14_dqdv.png","graph_suite_v1015.png","graph_suite_v1016.png","graph_suite_v1019.png"]
    pngs=[{"candidate_id":f"PNG-{i}","asset_class":"PACKAGED_PNG",
           "source_identity":identity(f"Claude/docs/v1.0.20/figs/{name}"),"decision":"NON_ADOPTED",
           "decision_evidence":{"state":"ABSENT_FROM_V1021_TREE_AND_INCLUDE_GRAPH"},"release_include_edges":0}
          for i,name in enumerate(png_names,1)]
    code=[anchored_line(f"Claude/docs/v1.0.21/_sections/{name}",line)|
          {"disposition":"FORBIDDEN_RENDERED_MAIN_BODY_CODE_OR_IMPLEMENTATION_MENTION"} for name,line in CODE_ROWS]
    label_rows=[("ch1_appC_navaid.tex",127),("ch1_appD_si.tex",61),("ch1_sec00_intro.tex",95),
      ("ch1_sec03_center.tex",111),("ch1_sec03_center.tex",114),("ch1_sec08_lag.tex",129),
      ("ch1_sec11_lcointro.tex",41),("ch1_sec11_lcointro.tex",62),("ch1_sec11_lcointro.tex",118),
      ("ch1_sec11_lcointro.tex",170),("ch1_sec14_lcodecomp.tex",97),("ch1_sec15_lcoelec.tex",183),
      ("ch1_sec15_lcoelec.tex",298),("ch1_sec15_lcoelec.tex",302),("ch1_sec15_lcoelec.tex",337),
      ("ch1_sec17_msmr.tex",4),("ch1_sec17_msmr.tex",12),("ch1_sec17_msmr.tex",72),
      ("ch1_sec18_inputs.tex",7),("ch1_sec18_inputs.tex",30)]
    labels=[anchored_line(f"Claude/docs/v1.0.21/_sections/{n}",l)|{"disposition":"LABEL_TOKEN_ONLY"} for n,l in label_rows]
    preamble=[anchored_line(f"Claude/docs/v1.0.21/_sections/{n}",l)|{"disposition":"NONRENDERED_PREAMBLE_DECLARATION"}
              for n,l in (("ch1_preamble.tex",32),("ch1_preamble.tex",51),("ch2_preamble.tex",49))]
    source_ids=[identity(x[1])|{"root_id":x[0]} for x in SOURCE_IDENTITIES]
    pdf_ids=[identity(x[4])|{"root_id":x[0],"pages":x[7],"class":"GENERATED_WITNESS","source_authority":False,"scientific_authority":False,"projection_only":True} for x in SOURCE_IDENTITIES]
    snapshots=[]
    for row in topology["process_artifacts"]:
        if row.get("artifact_kind")=="SNAPSHOT" and row.get("existence_state")=="PRESENT" and row.get("q_id") in {"Q0","Q2","Q3","Q4","Q5NAV","Q5","Q5B","Q6","Q7"}:
            snapshots.append(identity(row["path"])|{"event":row["q_id"],"authored_commit":row["commit"],"class":"GENERATED_WITNESS","source_authority":False,"scientific_authority":False})
    snapshots.sort(key=lambda x:["Q0","Q2","Q3","Q4","Q5NAV","Q5","Q5B","Q6","Q7"].index(x["event"]))
    q8=topology["history"]["implementation_chain"][9]
    process_note_ids=["P061-SRC-0205","P061-SRC-0206","P061-SRC-0213","P061-SRC-0214"]
    process_notes=[identity(comp[x]["path"])|{"source_id":x,"class":"PROCESS_NOTE",
                   "member_of_content_denominator":False,"source_authority":False,"scientific_authority":False}
                   for x in process_note_ids]
    builds=[{"root_id":x[0],"engine":"MiKTeX-XeTeX 4.16 / MiKTeX 25.12","command":["xelatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",next(y[1] for y in SOURCE_IDENTITIES if y[0]==x[0]).split("/")[-1]],"timeout_seconds_each":180,"passes":3,"exit_codes":[0,0,0],
             "pages":x[1],"labels":x[2],"unresolved_references":x[3],"unresolved_citations":x[4],
             "multiply_defined_labels":x[5],"missing_glyphs":x[6],"font_fallback_warnings":x[7],
             "raw_pdf_sha256_excluded_from_deterministic_projection":x[8]} for x in BUILDS]
    changelog="Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md"
    controlled_spec=[
      ("A-001",10,["GOVERNING_EQUATION","BACKGROUND_EQUATION","NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex"),("A-002",11,["NAVIGATION","NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex"),("A-003",12,["NAVIGATION","NARRATIVE","IMPLEMENTATION"],"Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex;Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex"),("A-004",13,["BACKGROUND_EQUATION","NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex"),("A-005",14,["NAVIGATION","NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex"),("A-006",27,["WORKED_EXAMPLE"],"Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex"),("A-007",29,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec01_n0n1.tex"),("A-008",32,["WORKED_EXAMPLE"],"Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex"),("A-009",33,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex"),("A-010",35,["MATERIAL_SCOPE_MAP","NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_appD_si.tex"),
      ("R-001",17,["FIGURE"],"Claude/docs/v1.0.21/_sections/ch1_sec03_center.tex"),("R-002",18,["FIGURE"],"Claude/docs/v1.0.21/_sections/ch1_sec04_hys.tex"),("R-003",19,["FIGURE"],"Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex"),("R-004",20,["FIGURE"],"Claude/docs/v1.0.21/_sections/ch2_sec08_synthesis.tex"),("R-005",21,["FIGURE"],"Claude/docs/v1.0.21/_sections/ch2_sec04_einstein.tex"),
      ("N-001",23,["IMPLEMENTATION"],"Claude/docs/v1.0.21/_sections/ch1_preamble.tex;Claude/docs/v1.0.21/_sections/ch2_preamble.tex"),("N-002",24,["NAVIGATION","FIGURE"],"Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex"),("N-003",25,["NAVIGATION"],"Claude/docs/v1.0.21/_sections/ch1_sec00_intro.tex;Claude/docs/v1.0.21/_sections/ch2_sec00_intro.tex"),("N-004",28,["NAVIGATION"],"Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex"),("N-005",37,["NAVIGATION"],"Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex"),
      ("C-020",15,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_bib.tex"),("C-021",16,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_bib.tex"),("C-022",30,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_bib.tex"),("C-023",31,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_bib.tex")]+[(f"C-{i:03}",36,["NARRATIVE"],"Claude/docs/v1.0.21/_sections/ch1_bib.tex") for i in range(24,38)]
    final_specs={
      "A-001":[("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",280,385)],"A-002":[("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",431,440)],"A-003":[("Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex",20,23),("Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex",23,25)],"A-004":[("Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",46,118)],"A-005":[("Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex",97,99)],"A-006":[("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",125,163)],"A-007":[("Claude/docs/v1.0.21/_sections/ch1_sec01_n0n1.tex",204,218)],"A-008":[("Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",300,341)],"A-009":[("Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex",56,58)],"A-010":[("Claude/docs/v1.0.21/_sections/ch1_appD_si.tex",7,86)],
      "R-001":[("Claude/docs/v1.0.21/_sections/ch1_sec03_center.tex",61,105)],"R-002":[("Claude/docs/v1.0.21/_sections/ch1_sec04_hys.tex",118,226)],"R-003":[("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",60,122)],"R-004":[("Claude/docs/v1.0.21/_sections/ch2_sec08_synthesis.tex",135,221)],"R-005":[("Claude/docs/v1.0.21/_sections/ch2_sec04_einstein.tex",106,181)],
      "N-001":[("Claude/docs/v1.0.21/_sections/ch1_preamble.tex",74,77),("Claude/docs/v1.0.21/_sections/ch2_preamble.tex",53,56),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex",15,15),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex",43,45),("Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex",18,18),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex",1,8),("Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex",1,8)],"N-002":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",6,109)],"N-003":[("Claude/docs/v1.0.21/_sections/ch1_sec00_intro.tex",91,103),("Claude/docs/v1.0.21/_sections/ch2_sec00_intro.tex",67,76)],"N-004":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",111,138)],"N-005":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",7,10)],
      "C-020":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",9,9)],"C-021":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",10,10)],"C-022":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",19,19)],"C-023":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",20,20)],**{f"C-{i:03}":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",i+24,i+24)] for i in range(24,38)}}
    controlled_labels={"A-001":["sec:sm-mc","eq:sm-mc-factor","eq:sm-mc-occ","eq:sm-mc-balance","eq:sm-mc-fluc"],"A-004":["eq:tst-qrc","eq:tst-freq","eq:tst-rate","eq:tst-dG","eq:tst-box"],"A-006":["sec:sum-worked"],"A-008":["sec:lco-worked"],"A-010":["sec:appendix-si","ssec:si-facts","ssec:si-map","tab:simap","ssec:si-anchor","ssec:si-gap","ssec:si-partial"],"R-001":["fig:UjT"],"R-002":["fig:hysgap"],"R-003":["fig:sumcurve"],"R-004":["fig:qrevsoc"],"R-005":["fig:svibid"],"N-002":["sec:appendix-nav","ssec:nav-map","fig:navmap","ssec:nav-symbols","tab:navsymbols"],"N-004":["ssec:nav-roadmap","tab:navroadmap"]}
    bib_labels={20:"bib:glasstone1941",21:"bib:laidlerking1983",22:"bib:weppner_huggins1977",23:"bib:baek_pilon2022",24:"bib:wen_huggins1981",25:"bib:limthongkul2003",26:"bib:li_dahn2007",27:"bib:obrovac_christensen2004",28:"bib:chevrier_dahn2009",29:"bib:beaulieu2001",30:"bib:sethuraman_stressevo2010",31:"bib:sethuraman_stresspot2010",32:"bib:liu_sizefracture2012",33:"bib:obrovac_chevrier2014",34:"bib:verbrugge_lisi2016",35:"bib:jiang_sihys2020",36:"bib:larchecahn1973",37:"bib:koebbing2024"}
    origins={"A-001":"Q2 q2f1 base + q2f2 uniqueness + q2o1 boundary; D21-5","A-002":"Q2 execution addition; draft-specific origin GROUND_NOT_FOUND","A-003":"Q2 execution addition; draft-specific origin GROUND_NOT_FOUND","A-004":"Q3 q3o1 base + q3f1/q3f2/q3f3","A-005":"Q3 placement bridge; q3f1 route","A-006":"D21-2 top3-1; GENERAL iv-1","A-007":"D21-2 top3-3; GENERAL v-1","A-008":"SI/LCO Q6.1 L1","A-009":"SI/LCO Q6.4 L6","A-010":"SI/LCO Q7; architecture conflict with D21-3","R-001":"FIGS_PICK FO3-4 N-3","R-002":"FIGS_PICK FF1-1 N-2","R-003":"FIGS_PICK FF3-3 N-5","R-004":"FIGS_PICK FF2-1 N-1","R-005":"FIGS_PICK FF2-5 N-4","N-001":"D21-1","N-002":"D21-1 navigation 1/2","N-003":"D21-1 navigation 3","N-004":"D21-2 top3-2; GENERAL iii-1","N-005":"Q7 source hardening; independent proposal edge GROUND_NOT_FOUND"}
    controlled_rows=[]
    for i,line,classes,paths in controlled_spec:
        controlled_rows.append({"id":i,"classes":classes,"subtype":"BIBLIOGRAPHIC_PROVENANCE" if i.startswith("C-") else None,"closure_authority":False,"generated_witness":False,"source_paths":paths.split(";"),"final_source_anchors":[anchored_span(*x) for x in final_specs[i]],"labels":([bib_labels[int(i[-3:])]] if i.startswith("C-") else controlled_labels.get(i,[])),"primary_consumer":"EXACT_FINAL_ROOT_OR_CITED_SECTION_RECORDED_IN_SOURCE_SPAN","adoption_origin":origins.get(i,"Q3/Q5/Q7 bibliographic provenance"),"change_log_anchor":anchored_line(changelog,line),"adoption_edge":"EXACT_CHANGE_LOG_TO_FINAL_SOURCE"})
    allowlisted=[]; environment_controls=[]; pattern=re.compile(r"(code|코드|implementation|구현|Python)")
    control_lines={"Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex":{141,149,150,155}}
    for path in ALLOWLIST:
        data=blob(BASELINE,path); lines=data.splitlines(keepends=True)
        for number,raw in enumerate(lines,1):
            visible=re.split(r"(?<!\\)%",raw.decode("utf-8"),maxsplit=1)[0]; match=pattern.search(visible)
            if not match: continue
            row={"path":path,"line":number,"column":match.start()+1,"match":match.group(0),"line_text":raw.decode("utf-8").rstrip("\r\n"),"line_sha256":hashlib.sha256(raw).hexdigest()}
            (environment_controls if number in control_lines.get(path,set()) else allowlisted).append(row)
    if len(allowlisted)!=119 or len(environment_controls)!=4: raise RuntimeError("allowlist inventory drift")
    def direction_row(path: str, route_id: str, start: int, end: int, decision: str,
                      targets: list[str], **extra: Any) -> dict[str, Any]:
        return {"route_id":route_id,"proposal_anchor":anchored_span(path,start,end),"decision":decision,
                "adopted_targets":targets,"source_authority":False,"scientific_authority":False}|extra
    general_path="Claude/docs/v1.0.20/results/DIRECTION_GENERAL_REPORT.md"
    general_adopted=[direction_row(general_path,r,s,e,"ADOPTED",t) for r,s,e,t in (
        ("candidate-(iii-1)",94,100,["N-004"]),("candidate-(iv-1)",116,122,["A-006"]),
        ("candidate-(v-1)",152,161,["A-007"]))]
    general_non=[direction_row(general_path,r,s,e,"NOT_ADOPTED_V1021",[],decision_kind="EXPLICIT_REMAINDER_14") for r,s,e in (
        ("candidate-(i-1)",29,35),("candidate-(i-2)",36,42),("candidate-(i-3)",43,49),("candidate-(i-4)",50,60),
        ("candidate-(ii-1)",65,71),("candidate-(ii-2)",72,78),("candidate-(ii-3)",79,89),
        ("candidate-(iii-2)",101,111),("candidate-(iv-2)",123,129),("candidate-(iv-3)",130,136),
        ("candidate-(iv-4)",137,147),("candidate-(v-2)",162,168),("candidate-(v-3)",169,175),
        ("candidate-(v-4)",176,187))]
    silco_path="Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md"
    silco_adopted=[
        direction_row(silco_path,"L1",166,166,"ADOPTED",["A-008"]),
        direction_row(silco_path,"L6",171,171,"ADOPTED",["A-009"]),
        direction_row(silco_path,"Q7.0",228,228,"PARTIAL_ADOPTED_WITH_GROUND_NOT_FOUND",["C-036","C-037"],ground_not_found=["Si partial-molar entropy primary source"]),
        direction_row(silco_path,"Q7.1",229,229,"PARTIAL_ADOPTED",[f"C-{i:03}" for i in range(24,36)],nonselected_keys=["mcdowell2013","wang_twophase2013","mcdowell_asitem2013","verbrugge_lisi2015","ogata_nmr2014"]),
        *[direction_row(silco_path,f"Q7.{i}",228+i,228+i,"ADOPTED_COMPOSITE_ROUTE",["A-010"]) for i in range(2,6)]
    ]
    silco_non=[
        direction_row(silco_path,"L2",167,167,"DEFERRED_V1021",[],phase_plan_anchor=anchored_line(silco_path,220),final_disposition_anchor=anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",34)),
        direction_row(silco_path,"L3",168,168,"DEFERRED_V1021",[],phase_plan_anchor=anchored_line(silco_path,223),final_disposition_anchor=anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",34)),
        direction_row(silco_path,"L4",169,169,"DEFERRED_V1021",[],phase_plan_anchor=anchored_line(silco_path,223),final_disposition_anchor=anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",34)),
        direction_row(silco_path,"L5",170,170,"DEFERRED_V1021",[],phase_plan_anchor=anchored_line(silco_path,221),final_disposition_anchor=anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",34)),
        direction_row(silco_path,"L7",172,172,"ALREADY_RESOLVED_NO_REEXECUTION",[],final_disposition_anchor=anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",34))]
    silco_process=[direction_row(silco_path,"Q7.6",234,234,"PROCESS_VALIDATION_ONLY",[],
                                  q8_event="Q8",q8_class=["TEST_ONLY","IMPLEMENTATION"],content_authority=False)]
    stat_path="Claude/docs/v1.0.20/results/DIRECTION_STATMECH_REPORT.md"
    stat_adopted=[direction_row(stat_path,r,s,e,"ADOPTED",t) for r,s,e,t in (
        ("candidate-(i)",24,76,["A-001","A-002","A-003"]),
        ("candidate-(ii)",77,124,["A-004","A-005","C-020","C-021"]),
        ("axis-A",262,272,["A-001","A-002","A-003"]))]
    stat_non=[
        direction_row(stat_path,"candidate-(iii)",125,168,"NOT_ADOPTED_V1021",[],decision_kind="EXHAUSTIVE_RELEASE_NONADOPTION",direct_rejection_anchor=None),
        direction_row(stat_path,"candidate-(iv)-light",188,189,"NOT_ADOPTED_V1021",[],decision_kind="EXHAUSTIVE_RELEASE_NONADOPTION",direct_rejection_anchor=None),
        direction_row(stat_path,"candidate-(iv)-heavy",190,190,"DEFERRED_USER_DECISION",[],decision_kind="REPORT_EXPLICIT_SEPARATE_GO_REQUIRED",supporting_anchor="DIRECTION_STATMECH_REPORT.md:208,211-212"),
        direction_row(stat_path,"candidate-(iv)-gamma-prediction",191,191,"EXPLICITLY_PROHIBITED",[],decision_kind="REPORT_NATIVE_NONRECOMMENDATION"),
        direction_row(stat_path,"candidate-(v)",216,254,"DEFERRED_V1021",[],decision_kind="REPORT_NATIVE_HOLD_RECOMMENDATION",supporting_anchor="DIRECTION_STATMECH_REPORT.md:253-254"),
        direction_row(stat_path,"axis-B",273,277,"DEFERRED_OUT_OF_SCOPE",[],decision_kind="REPORT_NATIVE_SCOPE_BOUNDARY"),
        direction_row(stat_path,"axis-C",279,283,"EXPLICITLY_NOT_ADOPTED",[],decision_kind="REPORT_NATIVE_NONRECOMMENDATION"),
        direction_row(stat_path,"axis-D",285,286,"NOT_ADOPTED_WITH_PARENT_III",[],decision_kind="REPORT_NATIVE_CHILD_ROUTE"),
        *[direction_row(stat_path,r,s,e,"NOT_ADOPTED_V1021",[],decision_kind="EXHAUSTIVE_RELEASE_NONADOPTION",direct_rejection_anchor=None) for r,s,e in (("flow-1",292,294),("flow-2",296,298),("flow-3",300,302))]]
    controls=["SNAPSHOT_AS_ADOPTION","PROPOSAL_AS_FINAL","AGGREGATE_VOTE_INFLATION","GENERATED_PDF_AS_SOURCE",
              "BUILD_AS_SCIENCE","BACKGROUND_AS_GOVERNING_LAW","UNNUMBERED_EQUATION_OMISSION","PARTIAL_ALL_OF_CLOSURE",
              "ALLOWLIST_BASENAME_MATCH","CODE_MENTION_COUNT","TABLE8_LAYOUT_SUPPRESSION","A05_UNRESOLVED_REF",
              "A06_FALSE_CLOSE","A07_FALSE_CLOSE","PARENT_FALSE_CLOSE","NEW_PHYSICS_FALSE_PROMOTION",
              "ADOPTED_PAGE_TAMPER","FIGURE_DENOMINATOR","CONTENT_DENOMINATOR","BUILD_PAGE_COUNT",
              "SOURCE_IDENTITY","MATRIX_SCHEMA","RESULT_FIRST","GATE_TAMPER","CONTROLLED_ASSET_ROWS",
              "NUMBERED_EQUATION_ANCHORS","UNNUMBERED_DISPLAY_ANCHORS","DIRECTION_ROUTES","DRAFT_ADOPTION_ROUTES",
              "EVIDENCE_LINKS","EVIDENCE_LINK_REMOVAL","DRAFT_PAGE_TAMPER","FINDING_SET","BUILD_COMMAND_PROVENANCE","Q_CHAIN","CODE_ANCHOR","FIGURE_SET","NEGATIVE_MANIFEST","GENERATED_WITNESS_LAYERS","Q8_PROCESS_CLAIM_BOUNDARY",
              "BUILD_AUDIT_SCHEMA","AUTHORITY_CONTRACT","FIGURE_VOTE_CONTRACT","FIGURE_DECISION_EVIDENCE","CONTROLLED_ASSET_PROVENANCE","PAGE_GENEALOGY_CONTRACT","BUILD_RUNTIME_METADATA","PHYSICS_CLOSURE_CONTRACT","RELEASE_PDF_CONTRACT","ACCEPTANCE_CONTRACT","A02_DECISION_CONTRACT","FULL_NESTED_SCHEMA"]
    controls.extend(["MATRIX_CANONICAL_DIGEST","SCAN_CONTRACT"])
    source_controls=["BUILDER_FULL_AST_CONTRACT"]
    document_controls=["DOC_RESULT_GATE_UNIQUENESS","DOC_RESULT_TERMINAL_UNIQUENESS","DOC_PARENT_LEDGER_STEP56_ROW","DOC_ACTIVE_LEDGER_STEP56_ROW","DOC_HANDOVER_STEP56_ROW","DOC_CONTENT_DIGEST"]
    git_controls=["GIT_BRANCH","GIT_HEAD","GIT_WORKTREE_EXACT_SEVEN","GIT_EXTRA_DIRTY","GIT_STAGED_MISMATCH","GIT_WORKTREE_INDEX_DIVERGENCE","GIT_LOCAL_PROTECTED","GIT_PERSISTENCE_PARENT","GIT_PERSISTENCE_SUBJECT","GIT_PERSISTENCE_EXACT_SEVEN","GIT_REMOTE_ACTIVE","GIT_REMOTE_PROTECTED","GIT_REMOTE_MAIN"]
    return {
      "schema":"P062_STEP56_PHYSICS_CLOSURE_MATRIX_V1","input_commit":PARENT,"frozen_baseline":BASELINE,
      "result_first":{"sentinel":SENTINEL,"containing_commit":"PENDING_AT_PRECOMMIT_BY_DESIGN"},
      "evidence_links":{"step52_topology":identity_at(PARENT,"Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json")|{"schema":1,"traversal":9785},
        "step52_read_attestation":identity_at(PARENT,"Codex/results/PHASE_062_V1021_READ_ATTESTATION.json")|{"schema":1,"traversal":7129},
        "step50_matrix":identity_at(PARENT,"Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json")|{"schema":"phase061-step50-review-artifact-v1","terminal":"PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS","traversal":16260,"figure_routes":31},
        "step53_result":identity_at(PARENT,"Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md")|{"terminal":"PASS_P062_STEP53_STATMECH_TST_REDERIVATION"},
        "step53_statmech_tst":json_evidence("Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json","1.0.0","PASS_P062_STEP53_STATMECH_TST_REDERIVATION"),
        "step54_result":identity_at(PARENT,"Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md")|{"terminal":"PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"},
        "step54_lco_si":json_evidence("Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json","phase062-step54-v1","PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"),
        "step55_result":identity_at(PARENT,"Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md")|{"terminal":"PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS"},
        "step55_code_delta":json_evidence("Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json","P062_STEP55_CODE_DELTA_MATRIX_V1","PASS_WITH_CONCERNS"),
        "step55_runtime_attestation":json_evidence("Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json","P062_STEP55_RUNTIME_ATTESTATION_V1")},
      "release":{"source_roots":source_ids,"release_pdfs":pdf_ids,"page_total":214,"root_count":5},
      "delta_classification":{"q_chain":["Q0","Q2","Q3","Q4","Q5NAV","Q5","Q5B","Q6","Q7"],
        "states":[x|{"structural_delta":"EXACT_CHANGED_PATH_SET","source_text_delta":"EXACT_PATCH_SHA256",
                     "classification":"NAVIGATION" if x["event"]=="Q5NAV" else "NARRATIVE_AND_CONTROLLED_ASSET_DELTA"}
                  for x in topology["history"]["implementation_chain"][:9]],
        "snapshot_witnesses":snapshots,"snapshot_witness_count":9,
        "release_pdf_witness_ids":[x["path"] for x in pdf_ids],"release_pdf_witness_count":5,
        "q8_process_claim":{"event":"Q8","commit":q8["commit"],"parent":q8["parents"][0],"patch_sha256":q8["patch_sha256"],"class":["TEST_ONLY","IMPLEMENTATION"],"self_report_only":True,"scientific_authority":False,"member_of_q_chain":False,"claim":"code matched 유지(변경 함수 0)"},
        "allowed_classes":["NARRATIVE","NAVIGATION","FIGURE","BACKGROUND_EQUATION","GOVERNING_EQUATION","WORKED_EXAMPLE","MATERIAL_SCOPE_MAP","IMPLEMENTATION","TEST_ONLY","GENERATED_WITNESS"],
        "direction_reports":[
          {"source_id":"P061-SRC-0065","source_identity":identity(general_path),"route":"corroborating_route","disposition":"PARTIAL_ADOPTED","adopted_targets":["A-006","N-004","A-007"],"adopted_routes":general_adopted,"adoption_evidence":[anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",x) for x in (27,28,29)],"decision_anchor":anchored_line("Claude/plans/2026-07-16-v1021-master-plan.md",68),"nonadopted_or_deferred":general_non,"primary_owner":"Phase 082","status":"OPEN","scientific_authority":False},
          {"source_id":"P061-SRC-0066","source_identity":identity(silco_path),"route":"corroborating_route","disposition":"PARTIAL_ADOPTED","adopted_targets":["A-008","A-009","A-010",*[f"C-{i:03}" for i in range(24,38)]],"adopted_routes":silco_adopted,"process_routes":silco_process,"adoption_evidence":[anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",x) for x in (32,33,34,35,36)],"nonadopted_or_deferred":silco_non,"primary_owner":"Phase 082","status":"OPEN","scientific_authority":False},
          {"source_id":"P061-SRC-0067","source_identity":identity(stat_path),"route":"corroborating_route","disposition":"PARTIAL_ADOPTED","adopted_targets":["A-001","A-002","A-003","A-004","A-005","C-020","C-021"],"adopted_routes":stat_adopted,"adoption_evidence":[anchored_line("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md",x) for x in (10,11,12,13,14,15,16)],"nonadopted_or_deferred":stat_non,"primary_owner":"Phase 082","status":"OPEN","scientific_authority":False}]},
      "content_denominator":{"count":48,"figures":figures,"packaged_png":pngs,"tex_drafts":drafts,
        "counts":{"figures":31,"packaged_png":5,"tex_drafts":12},"decision_counts":{"ADOPTED":12,"NON_ADOPTED":36},"process_notes":{"count":4,"member_of_content_denominator":False,"rows":process_notes}},
      "build_audit":{"clean_selected_asset_build":True,"drivers":5,"passes_per_driver":3,"runs_exit_zero":"15/15",
        "builds":builds,"zero_unresolved_all":True,"normalized_page_text_exact":"212/214",
        "line_wrap_only_pages":[{"root_id":"ch2_basic","page":7},{"root_id":"ch2_navigation","page":7}],
        "raw_pdf_hash_temp_timing_in_deterministic_projection":False,"temp_cleanup":"VERIFIED_OUTSIDE_WORKTREE_AND_REMOVED"},
      "page_genealogy":{"adopted_figures":5,"adopted_q2_inputs":3,"adopted_q3_inputs":4,
        "exact_routes":[x for x in figures if x["decision"]=="ADOPTED"] + [x for x in drafts if x["decision"]=="ADOPTED_COMPOSITE_INPUT"]},
      "review_vote_authority":{"candidate_routes":31,"ground_not_found":31,"individual_votes":0,"aggregate_counts_not_votes":True},
      "acceptance":{"A01":"PASS","A02":"PASS","A03":"PASS","A04":"PASS","A05":"PASS","A06":"OPEN","A07":"OPEN","P061-BD-NEW-001":"OPEN"},
      "physics_closure":{"new_physics_closure":False,"q2":"GOVERNING_CHARGE_BALANCE_DERIVATION",
        "q3":"BACKGROUND_TST_WITH_OPEN_AUTHORITY_LIMITS","figure_source_assets":"FIGURE","generated_projection_witnesses":"SNAPSHOT_AND_PDF_ONLY",
        "nine_registered_equations":"NOT_NINE_NEW_CLOSED_PHYSICAL_LAWS","si_governing_equation":"ABSENT",
        "implementation_consumer_validation_complete":False},
      "controlled_assets":{"rows":controlled_rows,"row_count":38,"family_counts":{"A":10,"R":5,"N":5,"C":18},
        "numbered_equations":[anchored_span(path,start,end)|{"id":eid,"label":label,"parent_asset":parent,"class":"GOVERNING_EQUATION" if eid=="Q2-03" else "BACKGROUND_EQUATION","authority":"NOT_NEW_CLOSED_LAW"} for eid,label,parent,path,start,end in (("Q2-01","eq:sm-mc-factor","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",301,306),("Q2-02","eq:sm-mc-occ","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",316,323),("Q2-03","eq:sm-mc-balance","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",340,344),("Q2-04","eq:sm-mc-fluc","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",356,361),("Q3-01","eq:tst-qrc","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",59,62),("Q3-02","eq:tst-freq","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",67,72),("Q3-03","eq:tst-rate","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",78,81),("Q3-04","eq:tst-dG","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",84,87),("Q3-05","eq:tst-box","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",92,96))],
        "unnumbered_displays":[anchored_span(path,start,end)|{"id":did,"phase":phase,"parent_asset":parent,"class":"BACKGROUND_EQUATION" if phase=="Q2" else "WORKED_EXAMPLE","authority":"LOAD_BEARING_UNNUMBERED_NOT_OMITTED"} for did,phase,parent,path,start,end in (("UQ2-01","Q2","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",331,336),("UQ5-01","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",136,142),("UQ5-02","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",146,148),("UQ5-03","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",151,154),("UQ6-01","Q6","A-008","Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",311,315),("UQ6-02","Q6","A-008","Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",320,326))]},
      "code_mentions":{"allowlist_exact_posix_paths":ALLOWLIST,"visible_lexical_matches":163,"allowlisted":119,
        "outside_allowlist_semantic_total":44,"forbidden_rendered_count":21,"label_token_only_count":20,
        "nonrendered_preamble_count":3,"forbidden_rendered":code,"label_token_only":labels,"nonrendered_preamble":preamble,
        "allowlisted_occurrences":allowlisted,"allowlisted_occurrence_count":119,"nonrendered_environment_control":environment_controls,"nonrendered_environment_control_count":4,"raw_allowlist_matching_lines":123,
        "scan_contract":{"pattern":"(code|코드|implementation|구현|Python)","root_reachable_tex_files":46,"include_edges":43,"exact_path_allowlist":True}},
      "findings":[
        {"id":"P062-S56-SCI-Q2","severity":"P1","state":"OPEN","finding":"domain/capacity/Legendre authority gaps"},
        {"id":"P062-S56-SCI-Q3","severity":"P1","state":"OPEN","finding":"standard-state/kappa/electrode authority gaps"},
        {"id":"P062-S56-SCI-Q6","severity":"P1","state":"OPEN","finding":"gate-off/on mixes xbar=0.50/0.85; same-x and T_ref counterfactual absent; tier-C demo cannot promote to material truth or exact implementation assertion"},
        {"id":"P062-S56-SCI-Q7","severity":"P1","state":"OPEN","finding":"Si-specific governing equation absent"},
        {"id":"P062-S56-DIRECTION","severity":"P1","state":"OPEN","finding":"direction rows corroborating only; A07 owner Phase 082"},
        {"id":"P062-S56-CODE","severity":"P1","state":"OPEN","finding":"21 rendered code/implementation mentions outside allowlist"}],
      "layout_findings":[{"id":"P062-VIS-001","severity":"P1_LAYOUT","path":"Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex","lines":"62-102","release_pages":{"basic":69,"navigation":69},"overfull_pt":555.52608,"status":"OPEN"}],
      "authority":{"external_scientific":False,"material":False,"experimental":False,"canonical":False,"final_release":False},
      "source_contract":{"builder_full_ast_sha256":builder_full_ast_sha()},
      "structural_schema_contract":{"sha256":STRUCTURAL_SCHEMA_SHA,"path_count":STRUCTURAL_SCHEMA_PATHS},
      "required_negative_controls":controls,"required_negative_control_count":len(controls),
      "required_source_controls":source_controls,"required_source_control_count":len(source_controls),
      "required_document_controls":document_controls,"required_document_control_count":len(document_controls),
      "required_git_controls":git_controls,"required_git_control_count":len(git_controls),
      "required_total_control_count":len(controls)+len(source_controls)+len(document_controls)+len(git_controls),"required_attack_fixture_count":112,
      "gate":"PASS_WITH_CONCERNS","terminal":"PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS"}

def canonical(x: Any) -> bytes:
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False)+"\n").encode()

def result_text(matrix_sha: str) -> str:
    return f"""# Phase 062 Step 56 Physics Closure Result

Gate: `PASS_WITH_CONCERNS`

Terminal: `PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS`

Result-first sentinel: `{SENTINEL}`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

## Reconciled prerequisite

- Step 55 exact-eight containing commit: `{PARENT}`
- Step 55 terminal: `PASS_P062_STEP55_PERSISTENCE`

## Frozen audit result

- baseline: `{BASELINE}`
- matrix content SHA-256: `{matrix_sha}`
- content denominator: `48/48` = figures `31/31` + packaged PNG `5/5` + Q2/Q3 TeX drafts `12/12`; process notes `4` remain outside the content denominator.
- A02 decision denominator: adopted `12/12` = figures `5` + drafts `7`; non-adopted `36/36` = figures `26` + PNG `5` + drafts `5`. Every row retains exact decision evidence and final-field disposition.
- adopted genealogy: figures `5/5`, Q2 inputs `3/3`, Q3 inputs `4/4`; exact basic/navigation PDF pages are recorded.
- candidate-level individual reviewer votes: `0/31`; explicit `GROUND_NOT_FOUND`: `31/31`; aggregate review counts were not inflated into votes.
- clean selected-asset XeLaTeX build: drivers `5/5`, passes `15/15`, pages `8/76/78/26/26`, unresolved references/citations/multiply-defined labels/missing glyphs `0/0/0/0`.
- A01/A02/A03/A04/A05: `PASS/PASS/PASS/PASS/PASS`.
- A06/A07/`P061-BD-NEW-001`: `OPEN/OPEN/OPEN`; partial ALL_OF closure is forbidden.
- new physics closure: `false`; Q2 charge-balance derivation and Q3 background TST retain bounded authority; figure source assets are `FIGURE`, while generated snapshot/PDF projections are witness-only.
- scholarly-body code/implementation mentions outside exact POSIX allowlist: forbidden rendered `21`; label token only `20`; non-rendered preamble `3`.
- `P062-VIS-001`: `P1_LAYOUT`, Table 8 clipping on Chapter 1 basic/navigation page `69`.

## Inputs and direct-read scope

- governing instructions: `Codex/AGENTS.md` 1–180, active master plan 1–665, Phase 062 plan 1–762 including Step 56 lines 416–445, Step 55 result 1–41.
- frozen roots read 1–EOF: appendix 497 lines; Chapter 1 basic root 48 and navigation driver 8; Chapter 2 basic root 38 and navigation driver 8.
- root-reachable scholarly TeX closure: `46/46` files and `43/43` include edges; frozen PDF text traversal `214/214`; Step 52 stored visual attestation `214/214` is hash-linked; this Step 56 audit directly inspected selected/rebuilt pages plus the page-69 defect, `12` pages total.
- strict JSON traversal: Step 52 topology `9,785`, Step 52 read attestation `7,129`, Step 50 review matrix `16,260`, Q2/Q3 carry `23,959` value/key nodes.
- recovery evidence links are exact Git identities: Step 53 result + statmech/TST matrix (`1,780` nodes), Step 54 result + LCO/Si matrix (`105,225` nodes), and Step 55 result + code-delta matrix/runtime attestation (`29,384/800` nodes); schema/gate terminals are preserved without promotion.

## Q-chain and distinct identity layers

- structural chain: `Q0→Q2→Q3→Q4→Q5NAV→Q5→Q5B→Q6→Q7`, `9/9` full semantic rows with exact keys, all parents, changed paths, changed-path digest, raw diff-tree digest, subject, patch SHA-256 and Step 56 classification fields; Q8 is excluded from this source chain.
- full recursive matrix structural schema: `{STRUCTURAL_SCHEMA_PATHS}` typed paths, SHA-256 `{STRUCTURAL_SCHEMA_SHA}`; every nested dict key set and list shape is fail-closed.
- final controlled assets: CHANGE_LOG `A-001..010` + `R-001..005` + `N-001..005` + `C-020..037` = `38/38`, each with final-source Git slice, label set and adoption origin.
- registered equations: Q2 `4/4`, Q3 `5/5`; unnumbered load-bearing displays: Q2 `1/1`, Q5 `3/3`, Q6 `2/2`.
- generated witnesses remain distinct: snapshots `9/9` and release PDFs `5/5`; source/scientific authority is false. Q8 `e96147fe4d5cefcccf733702e9bee78ba0beb025` / patch `6cdaa521bb7373b3a697b225dd677ad17ab4fa5522bb3e9a13f4cd14dbfe2a08` is a `TEST_ONLY+IMPLEMENTATION` self-report only.

## Adoption and direction-report decisions

- adopted figures: `FF1-1`, `FF2-1`, `FF2-5`, `FF3-3`, `FO3-4`; non-adopted figures `26/26`.
- adopted Q2 drafts: `Q2F1,Q2F2,Q2O1`, each mapped to Chapter 1 basic pages `[18,19,20]` and navigation pages `[19,20,21]`; adopted Q3 drafts: `Q3F1,Q3F2,Q3F3,Q3O1`, each mapped to basic/navigation page `[27]`. Remaining drafts `5/5` and packaged PNG `5/5` are non-adopted.
- `P061-SRC-0065`: `PARTIAL_ADOPTED` to `A-006,N-004,A-007`, other `14` non-adopted/deferred.
- `P061-SRC-0066`: L1→`A-008`, L6→`A-009`, Q7.0/Q7.1→`C-024..037`, Q7.2–Q7.5→composite `A-010`; L2–L5 deferred, L7 already resolved without re-execution, and Q7.6 is process-only. Five report bibliography keys were not selected and the Si partial-molar entropy primary source remains GROUND_NOT_FOUND.
- `P061-SRC-0067`: candidate (i)+axis A→`A-001..003`, candidate (ii)→`A-004,A-005,C-020,C-021`; `11` native remainder rows preserve not-adopted, deferred, prohibited and scope-boundary dispositions. All three reports are corroborating routes only; A07 owner Phase 082 and status OPEN are unchanged.

## Clean build and page evidence

- materialization: exact frozen Git archive in a verified external temporary directory; command per driver: `xelatex -interaction=nonstopmode -halt-on-error -file-line-error <driver>`; timeout `180 s`; three passes.
- environment: MiKTeX-XeTeX `4.16`, MiKTeX `25.12`; Poppler `26.05`; ko.TeX/amsmath/TikZ/hyperref/booktabs/longtable resolved.
- drivers `5/5`, passes `15/15`, page counts `8/76/78/26/26`, label counts `30/248/255/72/72`.
- unresolved refs/cites/multiply-defined/missing glyph: `0/0/0/0`; normalized frozen/rebuild page text `212/214`, with line-wrap-only deltas on both Chapter 2 page 7.
- selected figure pages were directly inspected; the external temp tree was boundary-checked and removed. Raw PDF hash, temp path and timing are excluded from the deterministic projection.

## P061-BD-NEW-001 acceptance

| Component | Decision | Evidence boundary |
|---|---|---|
| A01 | PASS | exact content denominator `48/48` |
| A02 | PASS | explicit adopted/non-adopted rows |
| A03 | PASS | adopted source→final TeX span→root include→basic/navigation page routes |
| A04 | PASS | individual reviewer vote `0/31`, explicit GROUND_NOT_FOUND `31/31` |
| A05 | PASS | independent clean selected-asset build `15/15`, unresolved `0` |
| A06 | OPEN | not closed by Step 56 |
| A07 | OPEN | Phase 082 primary owner unchanged |
| parent | OPEN | ALL_OF cannot close partially |

## Physics and document findings

- P1 Q2: domain/capacity/equation-of-state/Legendre authority gaps remain OPEN.
- P1 Q3: standard-state, `kappa`, electrode and peak-width authority gaps remain OPEN.
- P1 Q6: gate-off/on comparison mixes `xbar=0.50/0.85`; without same-x and `T_ref` counterfactual it cannot promote the tier-C demonstration to material truth or an exact implementation assertion.
- P1 Q7: Si-specific governing equation remains absent; SiOx/Si-C/blend/mechanics closure remains OPEN.
- P1 D21-3/direction: direction reports are corroborating routes, not authority transfer.
- P1 code: exact allowlist-visible `119`; non-rendered codebox environment controls `4`; outside allowlist forbidden rendered `21`, label-token-only `20`, non-rendered preamble `3`.
- P1_LAYOUT: `P062-VIS-001`, Table 8 (`ch1_appB_codemap.tex:62-102`) clips on Chapter 1 basic/navigation page 69.

## Confirmed, GROUND_NOT_FOUND and UNVERIFIED

- confirmed: frozen identities, internal adoption routes, page genealogy, build output, exact text/code/equation anchors and bounded classifications.
- GROUND_NOT_FOUND: candidate-level individual reviewer votes `31/31`; A-002/A-003 draft-specific origin; N-005 independent proposal edge.
- UNVERIFIED_EXTERNAL: scientific propositions, material/experimental validity, primary-source proposition anchors and final canonical physics closure.

## Exact-seven and protected boundaries

1. `Codex/work/v1021_phase062/build_phase062_step56_physics_closure.py`
2. `Codex/work/v1021_phase062/validate_phase062_step56.py`
3. `Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json`
4. `Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

`Claude/**`, protected `codex/lib-physics-endgame-v1025_2`, and `main` are unchanged by this checkpoint.

## Executed validation contract

- Python 3.12 and 3.14: full content/schema/Git-anchor validation, matrix mutation cases `80/80` with exact expected diagnostic signatures, builder full-AST mutation `1/1`, document fixtures `18/18`, disposable local-Git/bare-origin fixtures `13/13`, builder determinism `2/2`.
- version-neutral full builder AST SHA-256: `{builder_full_ast_sha()}`; an internal `ast.Constant` mutation changes the digest and is rejected.
- Default precommit and `--verify-staged` automatically force one fresh independent selected-asset XeLaTeX `5×3` build; explicit `--run-clean-build` never duplicates that run. `--content-only` suppresses the automatic build unless the explicit build flag is supplied; persistence does not re-force the build.
- precommit requires exact worktree seven; controller-owned staged gate requires exact cached seven and zero worktree/index divergence.

## Controls

- named controls: `74/74` = matrix semantic/schema `54/54` + builder full-AST `1/1` + document structure/content `6/6` + disposable Git boundary `13/13`.
- attack fixtures: `112/112` = matrix mutations `80/80` + builder AST mutation `1/1` + document mutations `18/18` + Git-state attacks `13/13`; coupled matrix signatures `79` and coupled document signatures `17` are reported from the executed expected-signature registries.
- determinism projection excludes raw PDF hash, temporary path and timing.
- external scientific/material/experimental/canonical/final-release authority: `false/false/false/false/false`.

## Persistence boundary

The exact-seven commit subject is `audit(phase062): adjudicate v1021 physics closure`. Post-commit verification must emit `PASS_P062_STEP56_PERSISTENCE` before Step 57.1.
"""

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,default=REPO); p.add_argument("--matrix",type=Path); p.add_argument("--result",type=Path); p.add_argument("--check",action="store_true"); a=p.parse_args()
    if a.repo.resolve()!=REPO.resolve(): raise SystemExit("repo mismatch")
    data=canonical(artifact()); result=result_text(hashlib.sha256(data).hexdigest()).encode()
    matrix=a.matrix or REPO/MATRIX; resultp=a.result or REPO/RESULT
    if a.check:
        if matrix.read_bytes()!=data or resultp.read_bytes()!=result: raise SystemExit("stored output mismatch")
        print("PASS_P062_STEP56_BUILDER_CHECK"); return 0
    resultp.parent.mkdir(parents=True,exist_ok=True); resultp.write_bytes(result)
    matrix.parent.mkdir(parents=True,exist_ok=True); matrix.write_bytes(data)
    print("PASS_P062_STEP56_BUILDER result-first"); return 0

if __name__=="__main__": raise SystemExit(main())
