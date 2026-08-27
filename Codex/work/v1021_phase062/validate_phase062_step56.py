#!/usr/bin/env python3
"""Independent fail-closed validator for Phase 062 Step 56."""
from __future__ import annotations
import argparse,ast,copy,functools,hashlib,io,json,math,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
from typing import Any,Callable

REPO=Path(__file__).resolve().parents[3]; BASELINE="3b5fd059ed09cdcdde38668c399cb35b8afbcca9"; PARENT="c700d4ff887af6bb66f2c0118f75832202856bf8"
SUBJECT="audit(phase062): adjudicate v1021 physics closure"; BRANCH="codex/anode-fit-v1025_2-canonical-completion"; UPSTREAM="origin/"+BRANCH
PROTECTED_BRANCH="codex/lib-physics-endgame-v1025_2"; PROTECTED="fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"; MAIN="4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BUILDER="Codex/work/v1021_phase062/build_phase062_step56_physics_closure.py"; VALIDATOR="Codex/work/v1021_phase062/validate_phase062_step56.py"
MATRIX="Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json"; RESULT="Codex/results/PHASE_062_STEP_056_PHYSICS_CLOSURE_RESULT.md"
PARENT_LEDGER="Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"; ACTIVE_LEDGER="Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"; HANDOVER="Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_SEVEN=(BUILDER,VALIDATOR,MATRIX,RESULT,PARENT_LEDGER,ACTIVE_LEDGER,HANDOVER)
MATRIX_SHA="1c24478c01692dca82465db273f3b432dac7b65739475f015999922137e1e27d"; BUILDER_LF_SHA="da2d0392e2d8f3281592d0d13095d5a793d49422f2800f52cfd5149032c7264b"; STRUCTURAL_SCHEMA_SHA="36ec5282b3e305aae3bc9ea9f05bac146c3d4a253a2e50f4a1b08cf802104f7f"; STRUCTURAL_SCHEMA_PATHS=5442; BUILDER_FULL_AST_SHA="5c4bc3591fb2622dd56691928527cfaac52752caaba11fe59bbca21bca73383b"
TOP_KEYS={"schema","input_commit","frozen_baseline","result_first","evidence_links","release","delta_classification","content_denominator","build_audit","page_genealogy","review_vote_authority","acceptance","physics_closure","controlled_assets","code_mentions","findings","layout_findings","authority","source_contract","structural_schema_contract","required_negative_controls","required_negative_control_count","required_source_controls","required_source_control_count","required_document_controls","required_document_control_count","required_git_controls","required_git_control_count","required_total_control_count","required_attack_fixture_count","gate","terminal"}
Q_EXPECTED=[("Q0","b4e939b0547cd4bf73bca30abe10fd164954c277","c70bcb6f4e2ca0eba6f1b9cfbb0cff7c2f88d862","3e541928866acbd800b3cb81a672cf150714d9bfefc2addc82a434ff01da955f"),("Q2","1635bc97fb7bd9c3fabc720e91bf09e5ba31798f","b4e939b0547cd4bf73bca30abe10fd164954c277","4759e4ee4fef3c6a88fcc435e4677b7c94c288fa1e4e35bbdeccc21c3598e6e2"),("Q3","c7420915dfae8ef076319737bddcc532a86d9505","1635bc97fb7bd9c3fabc720e91bf09e5ba31798f","7fe20aa0505ec1636249328181e4f036641510a5bdd2242d36d27dc0b4366be8"),("Q4","46360bd0630ee6039d595b6980ad28862b362eb7","c7420915dfae8ef076319737bddcc532a86d9505","cd94c1f4ccf043f180acd726f0e44dc2f9431f377d1f91535838d68fbc3c340b"),("Q5NAV","287d38d36415103cc28822f33c2520f734f1d6a9","46360bd0630ee6039d595b6980ad28862b362eb7","aa3425abbcc89e5506c58330dbff45903dfb7f53155dc2a8ab029ab0948f8078"),("Q5","9d208db8cec382b5d7d0dc79b4fc6a2e88cdb444","287d38d36415103cc28822f33c2520f734f1d6a9","8db1697811077e7805ed5a51b102d6269c941304d3caeba8dcd83b2d33c05227"),("Q5B","7316e7915db8727f794614b61f98d4df7f803bfd","9d208db8cec382b5d7d0dc79b4fc6a2e88cdb444","1880a87cd741cac3e6aa2259b8fd451b31f51c3913b1160c7d954585789f40b9"),("Q6","bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17","7316e7915db8727f794614b61f98d4df7f803bfd","826b6f08c29442c7f7f4f2e0841e951e188d2fbfbcbddb961a8f87c1a68a84a8"),("Q7","9ea5cb23754061261923bab013e279d7f6938723","bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17","b8971beeb7fb250e86e081b8e80046cc31d7aa107945e3c154d4d241610d85dc")]
CONTROLS=("SNAPSHOT_AS_ADOPTION","PROPOSAL_AS_FINAL","AGGREGATE_VOTE_INFLATION","GENERATED_PDF_AS_SOURCE","BUILD_AS_SCIENCE","BACKGROUND_AS_GOVERNING_LAW","UNNUMBERED_EQUATION_OMISSION","PARTIAL_ALL_OF_CLOSURE","ALLOWLIST_BASENAME_MATCH","CODE_MENTION_COUNT","TABLE8_LAYOUT_SUPPRESSION","A05_UNRESOLVED_REF","A06_FALSE_CLOSE","A07_FALSE_CLOSE","PARENT_FALSE_CLOSE","NEW_PHYSICS_FALSE_PROMOTION","ADOPTED_PAGE_TAMPER","FIGURE_DENOMINATOR","CONTENT_DENOMINATOR","BUILD_PAGE_COUNT","SOURCE_IDENTITY","MATRIX_SCHEMA","RESULT_FIRST","GATE_TAMPER","CONTROLLED_ASSET_ROWS","NUMBERED_EQUATION_ANCHORS","UNNUMBERED_DISPLAY_ANCHORS","DIRECTION_ROUTES","DRAFT_ADOPTION_ROUTES","EVIDENCE_LINKS","EVIDENCE_LINK_REMOVAL","DRAFT_PAGE_TAMPER","FINDING_SET","BUILD_COMMAND_PROVENANCE","Q_CHAIN","CODE_ANCHOR","FIGURE_SET","NEGATIVE_MANIFEST","GENERATED_WITNESS_LAYERS","Q8_PROCESS_CLAIM_BOUNDARY","BUILD_AUDIT_SCHEMA","AUTHORITY_CONTRACT","FIGURE_VOTE_CONTRACT","FIGURE_DECISION_EVIDENCE","CONTROLLED_ASSET_PROVENANCE","PAGE_GENEALOGY_CONTRACT","BUILD_RUNTIME_METADATA","PHYSICS_CLOSURE_CONTRACT","RELEASE_PDF_CONTRACT","ACCEPTANCE_CONTRACT","A02_DECISION_CONTRACT","FULL_NESTED_SCHEMA","MATRIX_CANONICAL_DIGEST","SCAN_CONTRACT")
SOURCE_CONTROLS=("BUILDER_FULL_AST_CONTRACT",)
DOC_CONTROLS=("DOC_RESULT_GATE_UNIQUENESS","DOC_RESULT_TERMINAL_UNIQUENESS","DOC_PARENT_LEDGER_STEP56_ROW","DOC_ACTIVE_LEDGER_STEP56_ROW","DOC_HANDOVER_STEP56_ROW","DOC_CONTENT_DIGEST")
GIT_CONTROLS=("GIT_BRANCH","GIT_HEAD","GIT_WORKTREE_EXACT_SEVEN","GIT_EXTRA_DIRTY","GIT_STAGED_MISMATCH","GIT_WORKTREE_INDEX_DIVERGENCE","GIT_LOCAL_PROTECTED","GIT_PERSISTENCE_PARENT","GIT_PERSISTENCE_SUBJECT","GIT_PERSISTENCE_EXACT_SEVEN","GIT_REMOTE_ACTIVE","GIT_REMOTE_PROTECTED","GIT_REMOTE_MAIN")
DOC_LF_SHA={RESULT:"8ca0c7a26f61ba9dcfd223357db32f5d3d980908bd8b3a2e17e7632bbd5a1179",PARENT_LEDGER:"abb3f036f083a3b20a1633c046671cc46d9b0700a2cc5ec9f6156472f5c62172",ACTIVE_LEDGER:"bdbfc2fc1c8131062be979f5f338d8a01a5c23fd1c5817f795add78336206b00",HANDOVER:"9413ac4d41ca1edff434b5c45840db6465aa5454a5213aaede1a97ca964b90d3"}
class ValidationError(RuntimeError):pass
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def proc(cmd:list[str],cwd:Path=REPO,timeout:int=60,text:bool=True,check:bool=False):
    cp=subprocess.run(cmd,cwd=cwd,capture_output=True,text=text,encoding="utf-8" if text else None,errors="replace" if text else None,timeout=timeout)
    if check and cp.returncode:raise ValidationError(f"SUBPROCESS:{cmd}:{cp.returncode}:{cp.stderr}")
    return cp
def git(a:list[str],repo:Path=REPO,text:bool=True,check:bool=True):return proc(["git",*a],repo,45,text,check).stdout
def strict(b:bytes)->Any:
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d:raise ValidationError("JSON_DUPLICATE_KEY")
            d[k]=v
        return d
    x=json.loads(b.decode(),object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValidationError("JSON_NONFINITE")))
    def walk(v):
        if isinstance(v,float) and not math.isfinite(v):raise ValidationError("JSON_NONFINITE")
        for y in v.values() if isinstance(v,dict) else v if isinstance(v,list) else ():walk(y)
    walk(x);return x
def traversal_count(v:Any)->int:
    if isinstance(v,dict):return 1+len(v)+sum(traversal_count(x) for x in v.values())
    if isinstance(v,list):return 1+sum(traversal_count(x) for x in v)
    return 1
@functools.cache
def blob(commit:str,path:str)->bytes:return git(["show",f"{commit}:{path}"],text=False)
@functools.cache
def identity(commit:str,path:str):
    b=blob(commit,path);return git(["rev-parse",f"{commit}:{path}"]).strip(),sha(b),len(b)
def source_ok(x):
    try:return (x.get("git_blob"),x.get("sha256"),x.get("bytes"))==identity(BASELINE,x["path"])
    except Exception:return False
def anchor_ok(x):
    try:
        lines=blob(BASELINE,x["path"]).splitlines(keepends=True);raw=b"".join(lines[x["line_start"]-1:x["line_end"]])
        expected=x.get("line_sha256",x.get("slice_sha256"));return sha(raw)==expected
    except Exception:return False
def independent_allowlist_rows():
    allowed=[];controls=[];pattern=re.compile(r"(code|코드|implementation|구현|Python)");control_lines={"Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex":{141,149,150,155}}
    for path in ("Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex","Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex"):
        for number,raw in enumerate(blob(BASELINE,path).splitlines(keepends=True),1):
            visible=re.split(r"(?<!\\)%",raw.decode(),maxsplit=1)[0];match=pattern.search(visible)
            if not match:continue
            row={"path":path,"line":number,"column":match.start()+1,"match":match.group(0),"line_text":raw.decode().rstrip("\r\n"),"line_sha256":sha(raw)}
            (controls if number in control_lines.get(path,set()) else allowed).append(row)
    return allowed,controls

AUTHORITY_EXPECTED={"external_scientific":False,"material":False,"experimental":False,"canonical":False,"final_release":False}
ACCEPTANCE_EXPECTED={"A01":"PASS","A02":"PASS","A03":"PASS","A04":"PASS","A05":"PASS","A06":"OPEN","A07":"OPEN","P061-BD-NEW-001":"OPEN"}
PHYSICS_EXPECTED={"new_physics_closure":False,"q2":"GOVERNING_CHARGE_BALANCE_DERIVATION","q3":"BACKGROUND_TST_WITH_OPEN_AUTHORITY_LIMITS","figure_source_assets":"FIGURE","generated_projection_witnesses":"SNAPSHOT_AND_PDF_ONLY","nine_registered_equations":"NOT_NINE_NEW_CLOSED_PHYSICAL_LAWS","si_governing_equation":"ABSENT","implementation_consumer_validation_complete":False}
SCAN_EXPECTED={"pattern":"(code|코드|implementation|구현|Python)","root_reachable_tex_files":46,"include_edges":43,"exact_path_allowlist":True}
FINDINGS_EXPECTED=[
 {"id":"P062-S56-SCI-Q2","severity":"P1","state":"OPEN","finding":"domain/capacity/Legendre authority gaps"},
 {"id":"P062-S56-SCI-Q3","severity":"P1","state":"OPEN","finding":"standard-state/kappa/electrode authority gaps"},
 {"id":"P062-S56-SCI-Q6","severity":"P1","state":"OPEN","finding":"gate-off/on mixes xbar=0.50/0.85; same-x and T_ref counterfactual absent; tier-C demo cannot promote to material truth or exact implementation assertion"},
 {"id":"P062-S56-SCI-Q7","severity":"P1","state":"OPEN","finding":"Si-specific governing equation absent"},
 {"id":"P062-S56-DIRECTION","severity":"P1","state":"OPEN","finding":"direction rows corroborating only; A07 owner Phase 082"},
 {"id":"P062-S56-CODE","severity":"P1","state":"OPEN","finding":"21 rendered code/implementation mentions outside allowlist"}]
LAYOUT_EXPECTED=[{"id":"P062-VIS-001","severity":"P1_LAYOUT","path":"Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex","lines":"62-102","release_pages":{"basic":69,"navigation":69},"overfull_pt":555.52608,"status":"OPEN"}]
BUILD_TOP_KEYS={"clean_selected_asset_build","drivers","passes_per_driver","runs_exit_zero","builds","zero_unresolved_all","normalized_page_text_exact","line_wrap_only_pages","raw_pdf_hash_temp_timing_in_deterministic_projection","temp_cleanup"}
BUILD_ROW_KEYS={"root_id","engine","command","timeout_seconds_each","passes","exit_codes","pages","labels","unresolved_references","unresolved_citations","multiply_defined_labels","missing_glyphs","font_fallback_warnings","raw_pdf_sha256_excluded_from_deterministic_projection"}
FIGURE_COMMON_KEYS={"asset_class","candidate_id","decision","decision_evidence","individual_reviewer_vote","source_identity","vote_edge","vote_route"}
FIGURE_ADOPTED_KEYS=FIGURE_COMMON_KEYS|{"candidate_source","final_line_span","final_tex","label","release_pages","root_include_line"}
ASSET_ROW_KEYS={"id","classes","subtype","closure_authority","generated_witness","source_paths","final_source_anchors","labels","primary_consumer","adoption_origin","change_log_anchor","adoption_edge"}
ASSET_ORIGINS={
 "A-001":"Q2 q2f1 base + q2f2 uniqueness + q2o1 boundary; D21-5","A-002":"Q2 execution addition; draft-specific origin GROUND_NOT_FOUND","A-003":"Q2 execution addition; draft-specific origin GROUND_NOT_FOUND","A-004":"Q3 q3o1 base + q3f1/q3f2/q3f3","A-005":"Q3 placement bridge; q3f1 route","A-006":"D21-2 top3-1; GENERAL iv-1","A-007":"D21-2 top3-3; GENERAL v-1","A-008":"SI/LCO Q6.1 L1","A-009":"SI/LCO Q6.4 L6","A-010":"SI/LCO Q7; architecture conflict with D21-3",
 "R-001":"FIGS_PICK FO3-4 N-3","R-002":"FIGS_PICK FF1-1 N-2","R-003":"FIGS_PICK FF3-3 N-5","R-004":"FIGS_PICK FF2-1 N-1","R-005":"FIGS_PICK FF2-5 N-4","N-001":"D21-1","N-002":"D21-1 navigation 1/2","N-003":"D21-1 navigation 3","N-004":"D21-2 top3-2; GENERAL iii-1","N-005":"Q7 source hardening; independent proposal edge GROUND_NOT_FOUND"}

def expected_asset_paths(asset_id:str,final_expected:dict[str,list[tuple[str,int,int]]])->list[str]:
    if asset_id=="N-001":return ["Claude/docs/v1.0.21/_sections/ch1_preamble.tex","Claude/docs/v1.0.21/_sections/ch2_preamble.tex"]
    return list(dict.fromkeys(path for path,_,_ in final_expected.get(asset_id,[])))

def builder_ast_projection(tree:ast.AST)->dict[str,Any]:
    functions=[]
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            a=node.args
            functions.append((node.name,len(a.posonlyargs),len(a.args),len(a.kwonlyargs),a.vararg.arg if a.vararg else None,a.kwarg.arg if a.kwarg else None))
    imports=[]
    for node in tree.body:
        if isinstance(node,ast.Import):imports.extend(alias.name for alias in node.names)
        elif isinstance(node,ast.ImportFrom):imports.append("from:"+(node.module or ""))
    main_guards=sum(isinstance(node,ast.If) and isinstance(node.test,ast.Compare) and isinstance(node.test.left,ast.Name) and node.test.left.id=="__name__" for node in tree.body)
    return {"functions":sorted(functions),"imports":sorted(imports),"main_guards":main_guards}

def structural_projection(value:Any,path:str="$",rows:list[dict[str,Any]]|None=None)->list[dict[str,Any]]:
    if rows is None:rows=[]
    if isinstance(value,dict):
        rows.append({"path":path,"kind":"dict","keys":sorted(value)})
        for key in sorted(value):structural_projection(value[key],path+"/"+key.replace("~","~0").replace("/","~1"),rows)
    elif isinstance(value,list):
        rows.append({"path":path,"kind":"list","length":len(value)})
        for index,item in enumerate(value):structural_projection(item,f"{path}/{index}",rows)
    else:
        kind="null" if value is None else "bool" if isinstance(value,bool) else "int" if isinstance(value,int) else "float" if isinstance(value,float) else "str" if isinstance(value,str) else type(value).__name__
        rows.append({"path":path,"kind":kind})
    return rows

def structural_schema_identity(value:Any)->tuple[int,str]:
    rows=structural_projection(value);raw=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode();return len(rows),sha(raw)

def ast_canonical_value(value:Any)->Any:
    if isinstance(value,ast.AST):return {"node":type(value).__name__,"fields":[[name,ast_canonical_value(getattr(value,name))] for name in value._fields]}
    if isinstance(value,list):return {"list":[ast_canonical_value(item) for item in value]}
    if isinstance(value,tuple):return {"tuple":[ast_canonical_value(item) for item in value]}
    if isinstance(value,bytes):return {"bytes":value.hex()}
    if isinstance(value,complex):return {"complex":[value.real,value.imag]}
    if value is Ellipsis:return {"ellipsis":True}
    return value

def full_ast_identity(tree:ast.AST)->tuple[int,str]:
    raw=json.dumps(ast_canonical_value(tree),ensure_ascii=False,sort_keys=False,separators=(",",":"),allow_nan=False).encode();return len(raw),sha(raw)

BUILDER_AST_EXPECTED={
 "functions":[("anchored_line",0,2,0,None,None),("anchored_span",0,3,0,None,None),("artifact",0,0,0,None,None),("ast_canonical_value",0,1,0,None,None),("blob",0,2,0,None,None),("builder_full_ast_sha",0,0,0,None,None),("canonical",0,1,0,None,None),("direction_row",0,6,0,None,"extra"),("git",0,0,0,"args",None),("identity",0,1,0,None,None),("identity_at",0,2,0,None,None),("json_evidence",0,3,0,None,None),("main",0,0,0,None,None),("result_text",0,1,0,None,None),("traversal_count",0,1,0,None,None)],
 "imports":["argparse","ast","from:__future__","from:pathlib","from:typing","hashlib","json","re","subprocess"],"main_guards":1}

def diagnostics(m:dict[str,Any])->set[str]:
    o=set();c=m.get("content_denominator",{});fig=c.get("figures",[]);png=c.get("packaged_png",[]);draft=c.get("tex_drafts",[]);b=m.get("build_audit",{});acc=m.get("acceptance",{});cm=m.get("code_mentions",{})
    try:
        candidate=(json.dumps(m,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
        if sha(candidate)!=MATRIX_SHA:o.add("MATRIX_CANONICAL_DIGEST")
    except Exception:o.add("MATRIX_CANONICAL_DIGEST")
    if set(m)!=TOP_KEYS:o.add("MATRIX_SCHEMA")
    if structural_schema_identity(m)!=(STRUCTURAL_SCHEMA_PATHS,STRUCTURAL_SCHEMA_SHA) or m.get("structural_schema_contract")!={"sha256":STRUCTURAL_SCHEMA_SHA,"path_count":STRUCTURAL_SCHEMA_PATHS}:o.add("FULL_NESTED_SCHEMA")
    if m.get("schema")!="P062_STEP56_PHYSICS_CLOSURE_MATRIX_V1" or m.get("input_commit")!=PARENT or m.get("frozen_baseline")!=BASELINE:o.add("MATRIX_HEADER")
    if m.get("result_first")!={"sentinel":"P062_STEP56_RESULT_FIRST_PRECOMMIT","containing_commit":"PENDING_AT_PRECOMMIT_BY_DESIGN"}:o.add("RESULT_FIRST")
    if len(fig)!=31 or c.get("counts",{}).get("figures")!=31:o.add("FIGURE_DENOMINATOR")
    if c.get("count")!=48 or len(png)!=5 or len(draft)!=12:o.add("CONTENT_DENOMINATOR")
    expected={f"FF1-{i}" for i in range(1,8)}|{f"FF2-{i}" for i in range(1,6)}|{f"FF3-{i}" for i in range(1,8)}|{f"FO{j}-{i}" for j in range(1,4) for i in range(1,5)}
    if {x.get("candidate_id") for x in fig}!=expected:o.add("FIGURE_SET")
    if any(not source_ok(x.get("source_identity",{})) for x in [*fig,*png,*draft]):o.add("SOURCE_IDENTITY")
    notes=c.get("process_notes",{});note_rows=notes.get("rows",[])
    note_expected={"P061-SRC-0205":"Claude/docs/v1.0.20/results/comp_Q2_gcbalance/NOTE_q2o1.md","P061-SRC-0206":"Claude/docs/v1.0.20/results/comp_Q2_gcbalance/NOTE_q2o2.md","P061-SRC-0213":"Claude/docs/v1.0.20/results/comp_Q3_tst/NOTE_q3f1.md","P061-SRC-0214":"Claude/docs/v1.0.20/results/comp_Q3_tst/NOTE_q3o2.md"}
    if notes.get("count")!=4 or notes.get("member_of_content_denominator") is not False or {(x.get("source_id"),x.get("path")) for x in note_rows}!=set(note_expected.items()) or any(not source_ok(x) or x.get("class")!="PROCESS_NOTE" or x.get("member_of_content_denominator") is not False or x.get("source_authority") is not False or x.get("scientific_authority") is not False for x in note_rows):o.add("CONTENT_DENOMINATOR")
    if any(set(x)!=(FIGURE_ADOPTED_KEYS if x.get("decision")=="ADOPTED" else FIGURE_COMMON_KEYS) for x in fig):o.add("FIGURE_VOTE_CONTRACT")
    if any(x.get("decision")=="ADOPTED" and not x.get("final_tex") for x in fig):o.add("SNAPSHOT_AS_ADOPTION")
    if any(x.get("decision")=="NON_ADOPTED" and x.get("final_tex") for x in fig):o.add("PROPOSAL_AS_FINAL")
    if m.get("review_vote_authority")!={"candidate_routes":31,"ground_not_found":31,"individual_votes":0,"aggregate_counts_not_votes":True}:o.add("AGGREGATE_VOTE_INFLATION")
    if any(x.get("individual_reviewer_vote") is not None or x.get("vote_edge")!="GROUND_NOT_FOUND" or x.get("vote_route")!="P061-STEP50-GNF-011" for x in fig):o.add("FIGURE_VOTE_CONTRACT")
    judgment=identity(BASELINE,"Claude/docs/v1.0.20/results/FIGS_PICK_JUDGMENT.md")
    for index,x in enumerate(fig,1):
        expected_evidence={"path":"Claude/docs/v1.0.20/results/FIGS_PICK_JUDGMENT.md","git_blob":judgment[0],"sha256":judgment[1],"route_id":f"P061-STEP50-FIG-GENEALOGY-{index:03}"}
        if x.get("decision_evidence")!=expected_evidence:o.add("FIGURE_DECISION_EVIDENCE")
    adopted_figure_ids={"FF1-1","FF2-1","FF2-5","FF3-3","FO3-4"};adopted_draft_ids={"Q2F1","Q2F2","Q2O1","Q3F1","Q3F2","Q3F3","Q3O1"}
    png_keys={"asset_class","candidate_id","decision","decision_evidence","release_include_edges","source_identity"};draft_keys={"asset_class","candidate_id","decision","decision_evidence","final_line_span","final_tex","release_pages","root_include_line","source_identity"}
    a02_bad=any(x.get("asset_class")!="FIGURE" or x.get("decision")!=("ADOPTED" if x.get("candidate_id") in adopted_figure_ids else "NON_ADOPTED") for x in fig)
    a02_bad|={x.get("candidate_id") for x in png}!={f"PNG-{i}" for i in range(1,6)} or any(set(x)!=png_keys or x.get("asset_class")!="PACKAGED_PNG" or x.get("decision")!="NON_ADOPTED" or x.get("decision_evidence")!={"state":"ABSENT_FROM_V1021_TREE_AND_INCLUDE_GRAPH"} or x.get("release_include_edges")!=0 for x in png)
    draft_ids={"Q2F1","Q2F2","Q2F3","Q2F4","Q2O1","Q2O2","Q3F1","Q3F2","Q3F3","Q3F4","Q3O1","Q3O2"}
    a02_bad|={x.get("candidate_id") for x in draft}!=draft_ids
    for x in draft:
        candidate=x.get("candidate_id","");adopted=candidate in adopted_draft_ids;line=10 if candidate.startswith("Q2") else 13
        expected_evidence={"path":"Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md","line":line,"state":"EXACT_ADOPTION_EDGE" if adopted else "NO_ADOPTION_EDGE"}
        a02_bad|=set(x)!=draft_keys or x.get("asset_class")!="TEX_DRAFT" or x.get("decision")!=("ADOPTED_COMPOSITE_INPUT" if adopted else "NON_ADOPTED") or x.get("decision_evidence")!=expected_evidence
        if not adopted:a02_bad|=any(x.get(key) is not None for key in ("final_tex","final_line_span","root_include_line","release_pages"))
    adopted_total=sum(x.get("decision")=="ADOPTED" for x in fig)+sum(x.get("decision")=="ADOPTED_COMPOSITE_INPUT" for x in draft)
    nonadopted_total=sum(x.get("decision")=="NON_ADOPTED" for x in [*fig,*png,*draft])
    a02_bad|=(adopted_total,nonadopted_total)!=(12,36) or c.get("decision_counts")!={"ADOPTED":12,"NON_ADOPTED":36}
    if a02_bad:o.add("A02_DECISION_CONTRACT")
    if any(x.get("release_include_edges")!=0 for x in png):o.add("GENERATED_PDF_AS_SOURCE")
    if m.get("authority",{}).get("external_scientific") is not False:o.add("BUILD_AS_SCIENCE")
    if m.get("authority")!=AUTHORITY_EXPECTED:o.add("AUTHORITY_CONTRACT")
    eq=m.get("controlled_assets",{}).get("numbered_equations",[])
    if len(eq)!=9 or any(x.get("authority")!="NOT_NEW_CLOSED_LAW" for x in eq):o.add("BACKGROUND_AS_GOVERNING_LAW")
    if len(m.get("controlled_assets",{}).get("unnumbered_displays",[]))!=6:o.add("UNNUMBERED_EQUATION_OMISSION")
    assets=m.get("controlled_assets",{}); rows=assets.get("rows",[])
    expected_ids={f"A-{i:03}" for i in range(1,11)}|{f"R-{i:03}" for i in range(1,6)}|{f"N-{i:03}" for i in range(1,6)}|{f"C-{i:03}" for i in range(20,38)}
    class_map={"A-001":["GOVERNING_EQUATION","BACKGROUND_EQUATION","NARRATIVE"],"A-002":["NAVIGATION","NARRATIVE"],"A-003":["NAVIGATION","NARRATIVE","IMPLEMENTATION"],"A-004":["BACKGROUND_EQUATION","NARRATIVE"],"A-005":["NAVIGATION","NARRATIVE"],"A-006":["WORKED_EXAMPLE"],"A-007":["NARRATIVE"],"A-008":["WORKED_EXAMPLE"],"A-009":["NARRATIVE"],"A-010":["MATERIAL_SCOPE_MAP","NARRATIVE"]}
    class_map|={f"R-{i:03}":["FIGURE"] for i in range(1,6)};class_map|={"N-001":["IMPLEMENTATION"],"N-002":["NAVIGATION","FIGURE"],**{f"N-{i:03}":["NAVIGATION"] for i in range(3,6)},**{f"C-{i:03}":["NARRATIVE"] for i in range(20,38)}}
    if assets.get("row_count")!=38 or assets.get("family_counts")!={"A":10,"R":5,"N":5,"C":18} or {x.get("id") for x in rows}!=expected_ids or any(x.get("classes")!=class_map.get(x.get("id")) or x.get("adoption_edge")!="EXACT_CHANGE_LOG_TO_FINAL_SOURCE" or x.get("closure_authority") is not False or (x.get("subtype")!="BIBLIOGRAPHIC_PROVENANCE" if x.get("id","").startswith("C-") else x.get("subtype") is not None) or not anchor_ok(x.get("change_log_anchor",{})) for x in rows):o.add("CONTROLLED_ASSET_ROWS")
    final_expected={"A-001":[("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",280,385)],"A-002":[("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",431,440)],"A-003":[("Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex",20,23),("Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex",23,25)],"A-004":[("Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",46,118)],"A-005":[("Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex",97,99)],"A-006":[("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",125,163)],"A-007":[("Claude/docs/v1.0.21/_sections/ch1_sec01_n0n1.tex",204,218)],"A-008":[("Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",300,341)],"A-009":[("Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex",56,58)],"A-010":[("Claude/docs/v1.0.21/_sections/ch1_appD_si.tex",7,86)],"R-001":[("Claude/docs/v1.0.21/_sections/ch1_sec03_center.tex",61,105)],"R-002":[("Claude/docs/v1.0.21/_sections/ch1_sec04_hys.tex",118,226)],"R-003":[("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",60,122)],"R-004":[("Claude/docs/v1.0.21/_sections/ch2_sec08_synthesis.tex",135,221)],"R-005":[("Claude/docs/v1.0.21/_sections/ch2_sec04_einstein.tex",106,181)],"N-001":[("Claude/docs/v1.0.21/_sections/ch1_preamble.tex",74,77),("Claude/docs/v1.0.21/_sections/ch2_preamble.tex",53,56),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex",15,15),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex",43,45),("Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex",18,18),("Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex",1,8),("Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex",1,8)],"N-002":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",6,109)],"N-003":[("Claude/docs/v1.0.21/_sections/ch1_sec00_intro.tex",91,103),("Claude/docs/v1.0.21/_sections/ch2_sec00_intro.tex",67,76)],"N-004":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",111,138)],"N-005":[("Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex",7,10)],"C-020":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",9,9)],"C-021":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",10,10)],"C-022":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",19,19)],"C-023":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",20,20)],**{f"C-{i:03}":[("Claude/docs/v1.0.21/_sections/ch1_bib.tex",i+24,i+24)] for i in range(24,38)}}
    for row in rows:
        asset_id=row.get("id");expected_origin=ASSET_ORIGINS.get(asset_id,"Q3/Q5/Q7 bibliographic provenance")
        if set(row)!=ASSET_ROW_KEYS or row.get("source_paths")!=expected_asset_paths(asset_id,final_expected) or row.get("primary_consumer")!="EXACT_FINAL_ROOT_OR_CITED_SECTION_RECORDED_IN_SOURCE_SPAN" or row.get("adoption_origin")!=expected_origin:o.add("CONTROLLED_ASSET_PROVENANCE")
    for row in rows:
        anchors=row.get("final_source_anchors",[]); simplified=[(x.get("path"),x.get("line_start"),x.get("line_end")) for x in anchors]
        if simplified!=final_expected.get(row.get("id")) or any(not anchor_ok(x) for x in anchors):o.add("CONTROLLED_ASSET_FINAL_ANCHORS")
    label_expected={"A-001":["sec:sm-mc","eq:sm-mc-factor","eq:sm-mc-occ","eq:sm-mc-balance","eq:sm-mc-fluc"],"A-004":["eq:tst-qrc","eq:tst-freq","eq:tst-rate","eq:tst-dG","eq:tst-box"],"A-006":["sec:sum-worked"],"A-008":["sec:lco-worked"],"A-010":["sec:appendix-si","ssec:si-facts","ssec:si-map","tab:simap","ssec:si-anchor","ssec:si-gap","ssec:si-partial"],"R-001":["fig:UjT"],"R-002":["fig:hysgap"],"R-003":["fig:sumcurve"],"R-004":["fig:qrevsoc"],"R-005":["fig:svibid"],"N-002":["sec:appendix-nav","ssec:nav-map","fig:navmap","ssec:nav-symbols","tab:navsymbols"],"N-004":["ssec:nav-roadmap","tab:navroadmap"]}
    bibs=["glasstone1941","laidlerking1983","weppner_huggins1977","baek_pilon2022","wen_huggins1981","limthongkul2003","li_dahn2007","obrovac_christensen2004","chevrier_dahn2009","beaulieu2001","sethuraman_stressevo2010","sethuraman_stresspot2010","liu_sizefracture2012","obrovac_chevrier2014","verbrugge_lisi2016","jiang_sihys2020","larchecahn1973","koebbing2024"]
    label_expected|={f"C-{i+20:03}":["bib:"+name] for i,name in enumerate(bibs)}
    if any(x.get("labels")!=label_expected.get(x.get("id"),[]) for x in rows):o.add("CONTROLLED_ASSET_LABELS")
    eq_expected=[("Q2-01","eq:sm-mc-factor","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",301,306,"BACKGROUND_EQUATION"),("Q2-02","eq:sm-mc-occ","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",316,323,"BACKGROUND_EQUATION"),("Q2-03","eq:sm-mc-balance","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",340,344,"GOVERNING_EQUATION"),("Q2-04","eq:sm-mc-fluc","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",356,361,"BACKGROUND_EQUATION"),("Q3-01","eq:tst-qrc","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",59,62,"BACKGROUND_EQUATION"),("Q3-02","eq:tst-freq","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",67,72,"BACKGROUND_EQUATION"),("Q3-03","eq:tst-rate","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",78,81,"BACKGROUND_EQUATION"),("Q3-04","eq:tst-dG","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",84,87,"BACKGROUND_EQUATION"),("Q3-05","eq:tst-box","A-004","Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex",92,96,"BACKGROUND_EQUATION")]
    if [(x.get("id"),x.get("label"),x.get("parent_asset"),x.get("path"),x.get("line_start"),x.get("line_end"),x.get("class")) for x in eq]!=eq_expected or any(not anchor_ok(x) for x in eq):o.add("NUMBERED_EQUATION_ANCHORS")
    display_expected=[("UQ2-01","Q2","A-001","Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex",331,336,"BACKGROUND_EQUATION"),("UQ5-01","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",136,142,"WORKED_EXAMPLE"),("UQ5-02","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",146,148,"WORKED_EXAMPLE"),("UQ5-03","Q5","A-006","Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex",151,154,"WORKED_EXAMPLE"),("UQ6-01","Q6","A-008","Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",311,315,"WORKED_EXAMPLE"),("UQ6-02","Q6","A-008","Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",320,326,"WORKED_EXAMPLE")]
    displays=assets.get("unnumbered_displays",[])
    if [(x.get("id"),x.get("phase"),x.get("parent_asset"),x.get("path"),x.get("line_start"),x.get("line_end"),x.get("class")) for x in displays]!=display_expected or any(not anchor_ok(x) for x in displays):o.add("UNNUMBERED_DISPLAY_ANCHORS")
    if any(acc.get(x)!="OPEN" for x in ("A06","A07","P061-BD-NEW-001")):o.add("PARTIAL_ALL_OF_CLOSURE")
    if cm.get("allowlist_exact_posix_paths")!=["Claude/docs/v1.0.21/_sections/ch1_appB_codemap.tex","Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex"]:o.add("ALLOWLIST_BASENAME_MATCH")
    if cm.get("scan_contract")!=SCAN_EXPECTED:o.add("SCAN_CONTRACT")
    if (cm.get("forbidden_rendered_count"),len(cm.get("forbidden_rendered",[])),cm.get("label_token_only_count"),len(cm.get("label_token_only",[])),cm.get("nonrendered_preamble_count"),len(cm.get("nonrendered_preamble",[])))!=(21,21,20,20,3,3):o.add("CODE_MENTION_COUNT")
    allowed_rows,environment_rows=independent_allowlist_rows()
    if cm.get("allowlisted_occurrence_count")!=119 or cm.get("allowlisted_occurrences")!=allowed_rows or cm.get("nonrendered_environment_control_count")!=4 or cm.get("nonrendered_environment_control")!=environment_rows or cm.get("raw_allowlist_matching_lines")!=123:o.add("ALLOWLIST_INVENTORY")
    for r in cm.get("forbidden_rendered",[])+cm.get("label_token_only",[])+cm.get("nonrendered_preamble",[]):
        try:
            raw=blob(BASELINE,r["path"]).splitlines(keepends=True)[r["line_start"]-1]
            if sha(raw)!=r["line_sha256"] or raw.decode().rstrip("\r\n")!=r["line_text"]:o.add("CODE_ANCHOR")
        except Exception:o.add("CODE_ANCHOR")
    lay=m.get("layout_findings",[])
    if lay!=LAYOUT_EXPECTED:o.add("TABLE8_LAYOUT_SUPPRESSION")
    builds=b.get("builds",[])
    if set(b)!=BUILD_TOP_KEYS or any(set(x)!=BUILD_ROW_KEYS for x in builds):o.add("BUILD_AUDIT_SCHEMA")
    if len(builds)!=5 or [x.get("pages") for x in builds]!=[8,76,78,26,26]:o.add("BUILD_PAGE_COUNT")
    build_drivers=["appendix_phase_separation.tex","graphite_ica_ch1_v1.0.21.tex","graphite_ica_ch1_v1.0.21_nav.tex","graphite_ica_ch2_v1.0.21.tex","graphite_ica_ch2_v1.0.21_nav.tex"]
    for x,driver,labels in zip(builds,build_drivers,[30,248,255,72,72],strict=False):
        if x.get("command")!=["xelatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",driver] or x.get("passes")!=3 or x.get("exit_codes")!=[0,0,0] or x.get("labels")!=labels:o.add("BUILD_COMMAND_PROVENANCE")
    if b.get("clean_selected_asset_build") is not True or b.get("drivers")!=5 or b.get("passes_per_driver")!=3 or b.get("runs_exit_zero")!="15/15" or b.get("normalized_page_text_exact")!="212/214" or b.get("line_wrap_only_pages")!= [{"root_id":"ch2_basic","page":7},{"root_id":"ch2_navigation","page":7}] or b.get("raw_pdf_hash_temp_timing_in_deterministic_projection") is not False or b.get("temp_cleanup")!="VERIFIED_OUTSIDE_WORKTREE_AND_REMOVED" or any(x.get("engine")!="MiKTeX-XeTeX 4.16 / MiKTeX 25.12" or x.get("timeout_seconds_each")!=180 or x.get("font_fallback_warnings")!=warning or not isinstance(x.get("raw_pdf_sha256_excluded_from_deterministic_projection"),str) or not re.fullmatch(r"[0-9a-f]{64}",x.get("raw_pdf_sha256_excluded_from_deterministic_projection","")) for x,warning in zip(builds,[0,2,4,3,3],strict=False)):o.add("BUILD_RUNTIME_METADATA")
    if not b.get("zero_unresolved_all") or any(any(x.get(k)!=0 for k in ("unresolved_references","unresolved_citations","multiply_defined_labels","missing_glyphs")) for x in builds):o.add("A05_UNRESOLVED_REF")
    if acc!=ACCEPTANCE_EXPECTED:o.add("ACCEPTANCE_CONTRACT")
    if acc.get("A06")!="OPEN":o.add("A06_FALSE_CLOSE")
    if acc.get("A07")!="OPEN":o.add("A07_FALSE_CLOSE")
    if acc.get("P061-BD-NEW-001")!="OPEN":o.add("PARENT_FALSE_CLOSE")
    if m.get("physics_closure",{}).get("new_physics_closure") is not False:o.add("NEW_PHYSICS_FALSE_PROMOTION")
    if m.get("physics_closure")!=PHYSICS_EXPECTED:o.add("PHYSICS_CLOSURE_CONTRACT")
    adopted=[x for x in fig if x.get("decision")=="ADOPTED"]
    adopted_expected={
      "FF1-1":("Claude/docs/v1.0.21/_sections/ch1_sec04_hys.tex","fig:hysgap","118-226",25,{"basic":25,"navigation":25}),
      "FF2-1":("Claude/docs/v1.0.21/_sections/ch2_sec08_synthesis.tex","fig:qrevsoc","135-221",31,{"basic":22,"navigation":22}),
      "FF2-5":("Claude/docs/v1.0.21/_sections/ch2_sec04_einstein.tex","fig:svibid","106-181",27,{"basic":13,"navigation":13}),
      "FF3-3":("Claude/docs/v1.0.21/_sections/ch1_sec10_sum.tex","fig:sumcurve","60-122",31,{"basic":44,"navigation":45}),
      "FO3-4":("Claude/docs/v1.0.21/_sections/ch1_sec03_center.tex","fig:UjT","61-105",24,{"basic":22,"navigation":22})}
    if len(adopted)!=5 or {x.get("candidate_id") for x in adopted}!=set(adopted_expected):o.add("ADOPTED_PAGE_TAMPER")
    for x in adopted:
        expected_adopted=adopted_expected.get(x.get("candidate_id"))
        if expected_adopted is None or (x.get("final_tex"),x.get("label"),x.get("final_line_span"),x.get("root_include_line"),x.get("release_pages"))!=expected_adopted or x.get("candidate_source")!=x.get("source_identity",{}).get("path"):o.add("ADOPTED_PAGE_TAMPER")
    states=m.get("delta_classification",{}).get("states",[])
    topology=strict(blob(PARENT,"Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"));expected_states=[]
    for source in topology.get("history",{}).get("implementation_chain",[])[:9]:
        expected_states.append(source|{"structural_delta":"EXACT_CHANGED_PATH_SET","source_text_delta":"EXACT_PATCH_SHA256","classification":"NAVIGATION" if source.get("event")=="Q5NAV" else "NARRATIVE_AND_CONTROLLED_ASSET_DELTA"})
    if states!=expected_states:o.add("Q_CHAIN")
    for state,fixed in zip(expected_states,Q_EXPECTED,strict=False):
        try:
            commit=state["commit"];parents=git(["rev-list","--parents","-n","1",commit]).strip().split()[1:];subject=git(["show","-s","--format=%s",commit]).rstrip("\r\n");changed=git(["diff-tree","--no-commit-id","--name-only","-r","--root",commit]).splitlines()
            if (state.get("event"),commit,(parents or [None])[0],state.get("patch_sha256"))!=fixed or state.get("parents")!=parents or state.get("subject")!=subject or state.get("changed_paths")!=changed:o.add("Q_CHAIN")
        except Exception:o.add("Q_CHAIN")
    dc=m.get("delta_classification",{});snaps=dc.get("snapshot_witnesses",[])
    if dc.get("snapshot_witness_count")!=9 or [x.get("event") for x in snaps]!=[x[0] for x in Q_EXPECTED] or any(not source_ok(x) or x.get("class")!="GENERATED_WITNESS" or x.get("source_authority") is not False or x.get("scientific_authority") is not False for x in snaps):o.add("GENERATED_WITNESS_LAYERS")
    release=m.get("release",{});pdfs=release.get("release_pdfs",[]);source_roots=release.get("source_roots",[])
    root_spec=[("appendix","Claude/docs/v1.0.21/appendix_phase_separation.tex"),("ch1_basic","Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.tex"),("ch1_navigation","Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.tex"),("ch2_basic","Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.tex"),("ch2_navigation","Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.tex")]
    pdf_spec=[("appendix","Claude/docs/v1.0.21/appendix_phase_separation.pdf",8),("ch1_basic","Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21.pdf",76),("ch1_navigation","Claude/docs/v1.0.21/graphite_ica_ch1_v1.0.21_nav.pdf",78),("ch2_basic","Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21.pdf",26),("ch2_navigation","Claude/docs/v1.0.21/graphite_ica_ch2_v1.0.21_nav.pdf",26)]
    if set(release)!={"source_roots","release_pdfs","page_total","root_count"} or release.get("page_total")!=214 or release.get("root_count")!=5 or [(x.get("root_id"),x.get("path")) for x in source_roots]!=root_spec or any(set(x)!={"root_id","path","git_blob","sha256","bytes"} or not source_ok(x) for x in source_roots) or [(x.get("root_id"),x.get("path"),x.get("pages")) for x in pdfs]!=pdf_spec or any(set(x)!={"root_id","path","git_blob","sha256","bytes","pages","class","projection_only","source_authority","scientific_authority"} or not source_ok(x) or x.get("class")!="GENERATED_WITNESS" or x.get("projection_only") is not True or x.get("source_authority") is not False or x.get("scientific_authority") is not False for x in pdfs):o.add("RELEASE_PDF_CONTRACT")
    if dc.get("release_pdf_witness_count")!=5 or dc.get("release_pdf_witness_ids")!=[x.get("path") for x in pdfs] or any(not source_ok(x) or x.get("class")!="GENERATED_WITNESS" or x.get("projection_only") is not True or x.get("source_authority") is not False or x.get("scientific_authority") is not False for x in pdfs):o.add("GENERATED_WITNESS_LAYERS")
    q8=dc.get("q8_process_claim",{})
    if q8!={"event":"Q8","commit":"e96147fe4d5cefcccf733702e9bee78ba0beb025","parent":"9ea5cb23754061261923bab013e279d7f6938723","patch_sha256":"6cdaa521bb7373b3a697b225dd677ad17ab4fa5522bb3e9a13f4cd14dbfe2a08","class":["TEST_ONLY","IMPLEMENTATION"],"self_report_only":True,"scientific_authority":False,"member_of_q_chain":False,"claim":"code matched 유지(변경 함수 0)"}:o.add("Q8_PROCESS_CLAIM_BOUNDARY")
    directions=m.get("delta_classification",{}).get("direction_reports",[])
    general_adopted=[("candidate-(iii-1)",94,100,"ADOPTED",("N-004",)),("candidate-(iv-1)",116,122,"ADOPTED",("A-006",)),("candidate-(v-1)",152,161,"ADOPTED",("A-007",))]
    general_non=[(r,s,e,"NOT_ADOPTED_V1021",()) for r,s,e in (("candidate-(i-1)",29,35),("candidate-(i-2)",36,42),("candidate-(i-3)",43,49),("candidate-(i-4)",50,60),("candidate-(ii-1)",65,71),("candidate-(ii-2)",72,78),("candidate-(ii-3)",79,89),("candidate-(iii-2)",101,111),("candidate-(iv-2)",123,129),("candidate-(iv-3)",130,136),("candidate-(iv-4)",137,147),("candidate-(v-2)",162,168),("candidate-(v-3)",169,175),("candidate-(v-4)",176,187))]
    silco_adopted=[("L1",166,166,"ADOPTED",("A-008",)),("L6",171,171,"ADOPTED",("A-009",)),("Q7.0",228,228,"PARTIAL_ADOPTED_WITH_GROUND_NOT_FOUND",("C-036","C-037")),("Q7.1",229,229,"PARTIAL_ADOPTED",tuple(f"C-{i:03}" for i in range(24,36))),*((f"Q7.{i}",228+i,228+i,"ADOPTED_COMPOSITE_ROUTE",("A-010",)) for i in range(2,6))]
    silco_non=[(r,l,l,d,()) for r,l,d in (("L2",167,"DEFERRED_V1021"),("L3",168,"DEFERRED_V1021"),("L4",169,"DEFERRED_V1021"),("L5",170,"DEFERRED_V1021"),("L7",172,"ALREADY_RESOLVED_NO_REEXECUTION"))]
    stat_adopted=[("candidate-(i)",24,76,"ADOPTED",("A-001","A-002","A-003")),("candidate-(ii)",77,124,"ADOPTED",("A-004","A-005","C-020","C-021")),("axis-A",262,272,"ADOPTED",("A-001","A-002","A-003"))]
    stat_non=[(r,s,e,d,()) for r,s,e,d in (("candidate-(iii)",125,168,"NOT_ADOPTED_V1021"),("candidate-(iv)-light",188,189,"NOT_ADOPTED_V1021"),("candidate-(iv)-heavy",190,190,"DEFERRED_USER_DECISION"),("candidate-(iv)-gamma-prediction",191,191,"EXPLICITLY_PROHIBITED"),("candidate-(v)",216,254,"DEFERRED_V1021"),("axis-B",273,277,"DEFERRED_OUT_OF_SCOPE"),("axis-C",279,283,"EXPLICITLY_NOT_ADOPTED"),("axis-D",285,286,"NOT_ADOPTED_WITH_PARENT_III"),("flow-1",292,294,"NOT_ADOPTED_V1021"),("flow-2",296,298,"NOT_ADOPTED_V1021"),("flow-3",300,302,"NOT_ADOPTED_V1021"))]
    direction_expected={"P061-SRC-0065":({"A-006","N-004","A-007"},general_adopted,general_non),"P061-SRC-0066":({"A-008","A-009","A-010",*{f"C-{i:03}" for i in range(24,38)}},silco_adopted,silco_non),"P061-SRC-0067":({"A-001","A-002","A-003","A-004","A-005","C-020","C-021"},stat_adopted,stat_non)}
    if {x.get("source_id") for x in directions}!=set(direction_expected):o.add("DIRECTION_ROUTES")
    def route_projection(items):
        return [(r.get("route_id"),r.get("proposal_anchor",{}).get("line_start"),r.get("proposal_anchor",{}).get("line_end"),r.get("decision"),tuple(r.get("adopted_targets",[]))) for r in items]
    for x in directions:
        expected=direction_expected.get(x.get("source_id"),(set(),[],[]));all_routes=x.get("adopted_routes",[])+x.get("nonadopted_or_deferred",[])+x.get("process_routes",[])
        if x.get("route")!="corroborating_route" or x.get("disposition")!="PARTIAL_ADOPTED" or x.get("primary_owner")!="Phase 082" or x.get("status")!="OPEN" or x.get("scientific_authority") is not False or set(x.get("adopted_targets",[]))!=expected[0] or route_projection(x.get("adopted_routes",[]))!=expected[1] or route_projection(x.get("nonadopted_or_deferred",[]))!=expected[2] or not source_ok(x.get("source_identity",{})) or any(not anchor_ok(a) for a in x.get("adoption_evidence",[])) or any(r.get("proposal_anchor",{}).get("path")!=x.get("source_identity",{}).get("path") or not anchor_ok(r.get("proposal_anchor",{})) or r.get("source_authority") is not False or r.get("scientific_authority") is not False for r in all_routes):o.add("DIRECTION_ROUTES")
        if x.get("source_id")=="P061-SRC-0065" and (not anchor_ok(x.get("decision_anchor",{})) or (x.get("decision_anchor",{}).get("path"),x.get("decision_anchor",{}).get("line_start"),x.get("decision_anchor",{}).get("line_end"),x.get("decision_anchor",{}).get("line_sha256"))!=("Claude/plans/2026-07-16-v1021-master-plan.md",68,68,"c311a7165d9ead69604e9b4148dbcb49b6dc20785561bc1fc030044952e56cc2")):o.add("DIRECTION_ROUTES")
        if x.get("source_id")=="P061-SRC-0065" and any(r.get("decision_kind")!="EXPLICIT_REMAINDER_14" for r in x.get("nonadopted_or_deferred",[])):o.add("DIRECTION_ROUTES")
        if x.get("source_id")=="P061-SRC-0066":
            q70=next((r for r in x.get("adopted_routes",[]) if r.get("route_id")=="Q7.0"),{});q71=next((r for r in x.get("adopted_routes",[]) if r.get("route_id")=="Q7.1"),{});process=x.get("process_routes",[])
            if q70.get("ground_not_found")!=["Si partial-molar entropy primary source"] or q71.get("nonselected_keys")!=["mcdowell2013","wang_twophase2013","mcdowell_asitem2013","verbrugge_lisi2015","ogata_nmr2014"] or route_projection(process)!=[("Q7.6",234,234,"PROCESS_VALIDATION_ONLY",())] or len(process)!=1 or process[0].get("q8_event")!="Q8" or process[0].get("q8_class")!=["TEST_ONLY","IMPLEMENTATION"] or process[0].get("content_authority") is not False:o.add("DIRECTION_ROUTES")
            phase_lines={"L2":220,"L3":223,"L4":223,"L5":221};non={r.get("route_id"):r for r in x.get("nonadopted_or_deferred",[])}
            if any(not anchor_ok(non.get(r,{}).get("phase_plan_anchor",{})) or non.get(r,{}).get("phase_plan_anchor",{}).get("line_start")!=line for r,line in phase_lines.items()) or any(not anchor_ok(r.get("final_disposition_anchor",{})) or r.get("final_disposition_anchor",{}).get("line_start")!=34 for r in non.values()):o.add("DIRECTION_ROUTES")
        if x.get("source_id")=="P061-SRC-0067":
            kinds={"candidate-(iii)":"EXHAUSTIVE_RELEASE_NONADOPTION","candidate-(iv)-light":"EXHAUSTIVE_RELEASE_NONADOPTION","candidate-(iv)-heavy":"REPORT_EXPLICIT_SEPARATE_GO_REQUIRED","candidate-(iv)-gamma-prediction":"REPORT_NATIVE_NONRECOMMENDATION","candidate-(v)":"REPORT_NATIVE_HOLD_RECOMMENDATION","axis-B":"REPORT_NATIVE_SCOPE_BOUNDARY","axis-C":"REPORT_NATIVE_NONRECOMMENDATION","axis-D":"REPORT_NATIVE_CHILD_ROUTE","flow-1":"EXHAUSTIVE_RELEASE_NONADOPTION","flow-2":"EXHAUSTIVE_RELEASE_NONADOPTION","flow-3":"EXHAUSTIVE_RELEASE_NONADOPTION"}
            if {r.get("route_id"):r.get("decision_kind") for r in x.get("nonadopted_or_deferred",[])}!=kinds:o.add("DIRECTION_ROUTES")
    adopted_drafts={x.get("candidate_id") for x in draft if x.get("decision")=="ADOPTED_COMPOSITE_INPUT"}
    q2_route=("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex","280-385",23,{"basic":[18,19,20],"navigation":[19,20,21]})
    q3_route=("Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex","46-118",26,{"basic":[27],"navigation":[27]})
    if adopted_drafts!={"Q2F1","Q2F2","Q2O1","Q3F1","Q3F2","Q3F3","Q3O1"} or any((x.get("final_tex"),x.get("final_line_span"),x.get("root_include_line"))!=(q2_route[:3] if x.get("candidate_id","").startswith("Q2") else q3_route[:3]) for x in draft if x.get("candidate_id") in adopted_drafts):o.add("DRAFT_ADOPTION_ROUTES")
    if any(x.get("release_pages")!=(q2_route[3] if x.get("candidate_id","").startswith("Q2") else q3_route[3]) for x in draft if x.get("candidate_id") in adopted_drafts):o.add("DRAFT_PAGE_TAMPER")
    genealogy=m.get("page_genealogy",{});genealogy_rows=genealogy.get("exact_routes",[]);genealogy_by_id={x.get("candidate_id"):x for x in genealogy_rows}
    expected_genealogy_ids=set(adopted_expected)|adopted_drafts
    selected_drafts=[x for x in draft if x.get("candidate_id") in adopted_drafts]
    genealogy_bad=set(genealogy)!={"adopted_figures","adopted_q2_inputs","adopted_q3_inputs","exact_routes"} or (genealogy.get("adopted_figures"),genealogy.get("adopted_q2_inputs"),genealogy.get("adopted_q3_inputs"))!=(5,3,4) or len(genealogy_rows)!=12 or set(genealogy_by_id)!=expected_genealogy_ids or genealogy_rows!=adopted+selected_drafts
    for candidate_id,expected_row in adopted_expected.items():
        row=genealogy_by_id.get(candidate_id,{})
        if (row.get("decision"),row.get("final_tex"),row.get("label"),row.get("final_line_span"),row.get("root_include_line"),row.get("release_pages"))!=("ADOPTED",*expected_row):genealogy_bad=True
    for candidate_id in adopted_drafts:
        row=genealogy_by_id.get(candidate_id,{});route=q2_route if candidate_id.startswith("Q2") else q3_route
        if (row.get("decision"),row.get("final_tex"),row.get("final_line_span"),row.get("root_include_line"),row.get("release_pages"))!=("ADOPTED_COMPOSITE_INPUT",*route):genealogy_bad=True
    if genealogy_bad:o.add("PAGE_GENEALOGY_CONTRACT")
    link_specs={
      "step50_matrix":("Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json",{"schema":"phase061-step50-review-artifact-v1","terminal":"PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS","traversal":16260,"figure_routes":31}),
      "step52_topology":("Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json",{"schema":1,"traversal":9785}),
      "step52_read_attestation":("Codex/results/PHASE_062_V1021_READ_ATTESTATION.json",{"schema":1,"traversal":7129}),
      "step53_result":("Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md",{"terminal":"PASS_P062_STEP53_STATMECH_TST_REDERIVATION"}),
      "step53_statmech_tst":("Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json",{"schema":"1.0.0","terminal":"PASS_P062_STEP53_STATMECH_TST_REDERIVATION","traversal":1780}),
      "step54_result":("Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md",{"terminal":"PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"}),
      "step54_lco_si":("Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json",{"schema":"phase062-step54-v1","terminal":"PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS","traversal":105225}),
      "step55_result":("Codex/results/PHASE_062_STEP_055_CODE_RUNTIME_DELTA_RESULT.md",{"terminal":"PASS_P062_STEP55_CODE_RUNTIME_DELTA_WITH_CONCERNS"}),
      "step55_code_delta":("Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json",{"schema":"P062_STEP55_CODE_DELTA_MATRIX_V1","terminal":"PASS_WITH_CONCERNS","traversal":29384}),
      "step55_runtime_attestation":("Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json",{"schema":"P062_STEP55_RUNTIME_ATTESTATION_V1","traversal":800})}
    links=m.get("evidence_links",{})
    if set(links)!=set(link_specs):o.add("EVIDENCE_LINK_REMOVAL")
    for key,(path,extra) in link_specs.items():
        if key not in links:continue
        try:
            blob_id,digest,size=identity(PARENT,path);expected={"path":path,"commit":PARENT,"git_blob":blob_id,"sha256":digest,"bytes":size}|extra
            if links.get(key)!=expected:o.add("EVIDENCE_LINKS")
            raw=blob(PARENT,path)
            if path.endswith(".json"):
                parsed=strict(raw)
                if traversal_count(parsed)!=extra["traversal"]:o.add("EVIDENCE_LINKS")
                schema_value=parsed.get("schema",parsed.get("schema_version"))
                terminal_value=parsed.get("gate")
                if (schema_value is not None and schema_value!=extra.get("schema")) or ("terminal" in extra and terminal_value!=extra["terminal"]):o.add("EVIDENCE_LINKS")
            elif extra["terminal"].encode() not in raw:o.add("EVIDENCE_LINKS")
        except Exception:o.add("EVIDENCE_LINKS")
    if m.get("findings")!=FINDINGS_EXPECTED:o.add("FINDING_SET")
    if m.get("required_negative_controls")!=list(CONTROLS) or m.get("required_negative_control_count")!=len(CONTROLS) or m.get("required_source_controls")!=list(SOURCE_CONTROLS) or m.get("required_source_control_count")!=len(SOURCE_CONTROLS) or m.get("required_document_controls")!=list(DOC_CONTROLS) or m.get("required_document_control_count")!=len(DOC_CONTROLS) or m.get("required_git_controls")!=list(GIT_CONTROLS) or m.get("required_git_control_count")!=len(GIT_CONTROLS) or m.get("required_total_control_count")!=len(CONTROLS)+len(SOURCE_CONTROLS)+len(DOC_CONTROLS)+len(GIT_CONTROLS) or m.get("required_attack_fixture_count")!=112:o.add("NEGATIVE_MANIFEST")
    if m.get("gate")!="PASS_WITH_CONCERNS" or m.get("terminal")!="PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS":o.add("GATE_TAMPER")
    return o

def validate():
    data=(REPO/MATRIX).read_bytes();m=strict(data);d=diagnostics(m)
    if d:raise ValidationError("CONTENT:"+",".join(sorted(d)))
    if sha(data)!=MATRIX_SHA:raise ValidationError("MATRIX_GOLDEN")
    b=(REPO/BUILDER).read_bytes().replace(b"\r\n",b"\n")
    if sha(b)!=BUILDER_LF_SHA:raise ValidationError("BUILDER_IDENTITY")
    tree=ast.parse(b.decode())
    if builder_ast_projection(tree)!=BUILDER_AST_EXPECTED:raise ValidationError("BUILDER_AST")
    if full_ast_identity(tree)[1]!=BUILDER_FULL_AST_SHA:raise ValidationError("BUILDER_FULL_AST_CONTRACT")
    if m.get("source_contract")!={"builder_full_ast_sha256":BUILDER_FULL_AST_SHA}:raise ValidationError("BUILDER_FULL_AST_ARTIFACT")
    return m

def source_negative():
    source=(REPO/BUILDER).read_bytes().replace(b"\r\n",b"\n");tree=ast.parse(source.decode());baseline=full_ast_identity(tree)[1];mutated=copy.deepcopy(tree)
    target=next((node for node in ast.walk(mutated) if isinstance(node,ast.Constant) and node.value=="P062_STEP56_RESULT_FIRST_PRECOMMIT"),None)
    if target is None:raise ValidationError("BUILDER_AST_MUTATION_TARGET")
    target.value="P062_STEP56_RESULT_FIRST_PRECOMMIT_MUTATED"
    if baseline!=BUILDER_FULL_AST_SHA or full_ast_identity(mutated)[1]==baseline:raise ValidationError("BUILDER_FULL_AST_MUTATION_FALSE_PASS")
    print("PASS_P062_STEP56_SOURCE_CONTROLS 1/1 full_ast_constant_mutation=REJECTED")

def negative(m):
    cases:list[tuple[str,Callable]]=[
      ("SNAPSHOT_AS_ADOPTION",lambda x:[r for r in x["content_denominator"]["figures"] if r["decision"]=="ADOPTED"][0].__setitem__("final_tex",None)),
      ("PROPOSAL_AS_FINAL",lambda x:x["content_denominator"]["figures"][1].__setitem__("final_tex","x")),
      ("AGGREGATE_VOTE_INFLATION",lambda x:x["review_vote_authority"].__setitem__("individual_votes",6)),
      ("GENERATED_PDF_AS_SOURCE",lambda x:x["content_denominator"]["packaged_png"][0].__setitem__("release_include_edges",1)),
      ("BUILD_AS_SCIENCE",lambda x:x["authority"].__setitem__("external_scientific",True)),
      ("BACKGROUND_AS_GOVERNING_LAW",lambda x:x["controlled_assets"]["numbered_equations"][0].__setitem__("authority","CLOSED")),
      ("UNNUMBERED_EQUATION_OMISSION",lambda x:x["controlled_assets"]["unnumbered_displays"].pop()),
      ("PARTIAL_ALL_OF_CLOSURE",lambda x:x["acceptance"].update({"A06":"PASS","A07":"PASS","P061-BD-NEW-001":"PASS"})),
      ("ALLOWLIST_BASENAME_MATCH",lambda x:x["code_mentions"]["allowlist_exact_posix_paths"].__setitem__(0,"ch1_appB_codemap.tex")),
      ("CODE_MENTION_COUNT",lambda x:x["code_mentions"].__setitem__("forbidden_rendered_count",20)),
      ("TABLE8_LAYOUT_SUPPRESSION",lambda x:x["layout_findings"][0].__setitem__("severity","P2")),
      ("A05_UNRESOLVED_REF",lambda x:x["build_audit"]["builds"][0].__setitem__("unresolved_references",1)),
      ("A06_FALSE_CLOSE",lambda x:x["acceptance"].__setitem__("A06","PASS")),
      ("A07_FALSE_CLOSE",lambda x:x["acceptance"].__setitem__("A07","PASS")),
      ("PARENT_FALSE_CLOSE",lambda x:x["acceptance"].__setitem__("P061-BD-NEW-001","PASS")),
      ("NEW_PHYSICS_FALSE_PROMOTION",lambda x:x["physics_closure"].__setitem__("new_physics_closure",True)),
      ("ADOPTED_PAGE_TAMPER",lambda x:[r for r in x["content_denominator"]["figures"] if r["decision"]=="ADOPTED"][0].__setitem__("root_include_line",999)),
      ("FIGURE_DENOMINATOR",lambda x:x["content_denominator"]["counts"].__setitem__("figures",30)),
      ("CONTENT_DENOMINATOR",lambda x:x["content_denominator"].__setitem__("count",47)),
      ("BUILD_PAGE_COUNT",lambda x:x["build_audit"]["builds"][1].__setitem__("pages",75)),
      ("SOURCE_IDENTITY",lambda x:x["content_denominator"]["packaged_png"][0]["source_identity"].__setitem__("sha256","0"*64)),
      ("MATRIX_SCHEMA",lambda x:x.__setitem__("unknown",1)),
      ("RESULT_FIRST",lambda x:x["result_first"].__setitem__("containing_commit","x")),
      ("GATE_TAMPER",lambda x:x.__setitem__("gate","PASS")),
      ("CONTROLLED_ASSET_ROWS",lambda x:x["controlled_assets"]["rows"][0].__setitem__("classes",["NARRATIVE"])),
      ("NUMBERED_EQUATION_ANCHORS",lambda x:x["controlled_assets"]["numbered_equations"][0].__setitem__("line_sha256","0"*64)),
      ("UNNUMBERED_DISPLAY_ANCHORS",lambda x:x["controlled_assets"]["unnumbered_displays"][0].__setitem__("slice_sha256","0"*64)),
      ("DIRECTION_ROUTES",lambda x:x["delta_classification"]["direction_reports"][0].__setitem__("primary_owner","Phase 062")),
      ("DRAFT_ADOPTION_ROUTES",lambda x:[r for r in x["content_denominator"]["tex_drafts"] if r["candidate_id"]=="Q2F1"][0].__setitem__("final_tex","x")),
      ("EVIDENCE_LINKS",lambda x:x["evidence_links"]["step55_code_delta"].__setitem__("sha256","0"*64)),
      ("EVIDENCE_LINK_REMOVAL",lambda x:x["evidence_links"].pop("step53_result")),
      ("DRAFT_PAGE_TAMPER",lambda x:[r for r in x["content_denominator"]["tex_drafts"] if r["candidate_id"]=="Q2F1"][0]["release_pages"]["basic"].__setitem__(0,17)),
      ("FINDING_SET",lambda x:x["findings"][0].__setitem__("severity","P2")),
      ("BUILD_COMMAND_PROVENANCE",lambda x:x["build_audit"]["builds"][0]["command"].__setitem__(0,"pdflatex")),
      ("Q_CHAIN",lambda x:x["delta_classification"]["states"][0].__setitem__("patch_sha256","0"*64)),
      ("CODE_ANCHOR",lambda x:x["code_mentions"]["forbidden_rendered"][0].__setitem__("line_sha256","0"*64)),
      ("FIGURE_SET",lambda x:[r for r in x["content_denominator"]["figures"] if r["decision"]=="NON_ADOPTED"][0].__setitem__("candidate_id","BAD")),
      ("NEGATIVE_MANIFEST",lambda x:x["required_negative_controls"].pop()),
      ("GENERATED_WITNESS_LAYERS",lambda x:x["delta_classification"]["snapshot_witnesses"][0].__setitem__("source_authority",True)),
      ("Q8_PROCESS_CLAIM_BOUNDARY",lambda x:x["delta_classification"]["q8_process_claim"].__setitem__("scientific_authority",True)),
      ("BUILD_AUDIT_SCHEMA",lambda x:x["build_audit"].__setitem__("UNEXPECTED_KEY",True)),
      ("AUTHORITY_MATERIAL",lambda x:x["authority"].__setitem__("material",True)),
      ("AUTHORITY_EXPERIMENTAL",lambda x:x["authority"].__setitem__("experimental",True)),
      ("AUTHORITY_CANONICAL",lambda x:x["authority"].__setitem__("canonical",True)),
      ("AUTHORITY_FINAL_RELEASE",lambda x:x["authority"].__setitem__("final_release",True)),
      ("FIGURE_VOTE_CONTRACT",lambda x:x["content_denominator"]["figures"][0].__setitem__("vote_edge","PRESENT")),
      ("FIGURE_DECISION_EVIDENCE",lambda x:x["content_denominator"]["figures"][0].__setitem__("decision_evidence",{"path":"invented"})),
      ("CONTROLLED_SOURCE_PATHS",lambda x:x["controlled_assets"]["rows"][0].__setitem__("source_paths",[])),
      ("CONTROLLED_PRIMARY_CONSUMER",lambda x:x["controlled_assets"]["rows"][0].__setitem__("primary_consumer","invented")),
      ("CONTROLLED_ADOPTION_ORIGIN",lambda x:x["controlled_assets"]["rows"][0].__setitem__("adoption_origin","invented")),
      ("PAGE_GENEALOGY_CONTRACT",lambda x:x["page_genealogy"].clear()),
      ("BUILD_TEMP_CLEANUP",lambda x:x["build_audit"].__setitem__("temp_cleanup",False)),
      ("BUILD_RAW_PROJECTION",lambda x:x["build_audit"].__setitem__("raw_pdf_hash_temp_timing_in_deterministic_projection",True)),
      ("BUILD_FONT_WARNING",lambda x:x["build_audit"]["builds"][0].__setitem__("font_fallback_warnings",999)),
      ("PHYSICS_CLOSURE_CONTRACT",lambda x:x["physics_closure"].__setitem__("implementation_consumer_validation_complete",True)),
      ("RELEASE_PDF_CONTRACT",lambda x:x["release"]["release_pdfs"][0].__setitem__("pages",999)),
      ("ACCEPTANCE_CONTRACT",lambda x:x["acceptance"].__setitem__("UNEXPECTED_KEY","PASS")),
      ("A02_PNG_ADOPTED",lambda x:x["content_denominator"]["packaged_png"][0].__setitem__("decision","ADOPTED")),
      ("A02_PNG_INVENTED",lambda x:x["content_denominator"]["packaged_png"][0].__setitem__("decision","INVENTED")),
      ("A02_DRAFT_INVENTED",lambda x:next(r for r in x["content_denominator"]["tex_drafts"] if r["decision"]=="NON_ADOPTED").__setitem__("decision","INVENTED")),
      ("A02_PNG_EVIDENCE",lambda x:x["content_denominator"]["packaged_png"][0]["decision_evidence"].__setitem__("state","invented")),
      ("A02_DRAFT_EVIDENCE",lambda x:x["content_denominator"]["tex_drafts"][0]["decision_evidence"].__setitem__("state","invented")),
      ("SCHEMA_Q_STATE",lambda x:x["delta_classification"]["states"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_FINDING",lambda x:x["findings"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_SNAPSHOT",lambda x:x["delta_classification"]["snapshot_witnesses"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_DIRECTION",lambda x:x["delta_classification"]["direction_reports"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_ROUTE",lambda x:x["delta_classification"]["direction_reports"][0]["adopted_routes"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_NUMBERED_EQ",lambda x:x["controlled_assets"]["numbered_equations"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_PAGE_ROW",lambda x:x["page_genealogy"]["exact_routes"][0].__setitem__("UNEXPECTED_KEY",True)),
      ("SCHEMA_NESTED_MISSING",lambda x:x["findings"][0].pop("state")),
      ("Q_CHANGED_PATHS",lambda x:x["delta_classification"]["states"][0].__setitem__("changed_paths",[])),
      ("Q_SUBJECT",lambda x:x["delta_classification"]["states"][0].__setitem__("subject","invented")),
      ("PAGE_SOURCE_IDENTITY",lambda x:x["page_genealogy"]["exact_routes"][0]["source_identity"].__setitem__("sha256","0"*64)),
      ("PAGE_DECISION_EVIDENCE",lambda x:x["page_genealogy"]["exact_routes"][0]["decision_evidence"].__setitem__("path","invented")),
      ("PAGE_CANDIDATE_SOURCE",lambda x:x["page_genealogy"]["exact_routes"][0].__setitem__("candidate_source","invented")),
      ("FINDING_TEXT",lambda x:x["findings"][0].__setitem__("finding","INVENTED")),
      ("LAYOUT_PATH",lambda x:x["layout_findings"][0].__setitem__("path","INVENTED")),
      ("LAYOUT_STATUS",lambda x:x["layout_findings"][0].__setitem__("status","CLOSED")),
      ("SCAN_PATTERN",lambda x:x["code_mentions"]["scan_contract"].__setitem__("pattern","INVENTED")),
      ("ARBITRARY_SCALAR",lambda x:x["source_contract"].__setitem__("builder_full_ast_sha256","f"*64))]
    aliases={"AUTHORITY_MATERIAL":"AUTHORITY_CONTRACT","AUTHORITY_EXPERIMENTAL":"AUTHORITY_CONTRACT","AUTHORITY_CANONICAL":"AUTHORITY_CONTRACT","AUTHORITY_FINAL_RELEASE":"AUTHORITY_CONTRACT","CONTROLLED_SOURCE_PATHS":"CONTROLLED_ASSET_PROVENANCE","CONTROLLED_PRIMARY_CONSUMER":"CONTROLLED_ASSET_PROVENANCE","CONTROLLED_ADOPTION_ORIGIN":"CONTROLLED_ASSET_PROVENANCE","BUILD_TEMP_CLEANUP":"BUILD_RUNTIME_METADATA","BUILD_RAW_PROJECTION":"BUILD_RUNTIME_METADATA","BUILD_FONT_WARNING":"BUILD_RUNTIME_METADATA","A02_PNG_ADOPTED":"A02_DECISION_CONTRACT","A02_PNG_INVENTED":"A02_DECISION_CONTRACT","A02_DRAFT_INVENTED":"A02_DECISION_CONTRACT","A02_PNG_EVIDENCE":"A02_DECISION_CONTRACT","A02_DRAFT_EVIDENCE":"A02_DECISION_CONTRACT","SCHEMA_Q_STATE":"FULL_NESTED_SCHEMA","SCHEMA_FINDING":"FULL_NESTED_SCHEMA","SCHEMA_SNAPSHOT":"FULL_NESTED_SCHEMA","SCHEMA_DIRECTION":"FULL_NESTED_SCHEMA","SCHEMA_ROUTE":"FULL_NESTED_SCHEMA","SCHEMA_NUMBERED_EQ":"FULL_NESTED_SCHEMA","SCHEMA_PAGE_ROW":"FULL_NESTED_SCHEMA","SCHEMA_NESTED_MISSING":"FULL_NESTED_SCHEMA","Q_CHANGED_PATHS":"Q_CHAIN","Q_SUBJECT":"Q_CHAIN","PAGE_SOURCE_IDENTITY":"PAGE_GENEALOGY_CONTRACT","PAGE_DECISION_EVIDENCE":"PAGE_GENEALOGY_CONTRACT","PAGE_CANDIDATE_SOURCE":"PAGE_GENEALOGY_CONTRACT","FINDING_TEXT":"FINDING_SET","LAYOUT_PATH":"TABLE8_LAYOUT_SUPPRESSION","LAYOUT_STATUS":"TABLE8_LAYOUT_SUPPRESSION","SCAN_PATTERN":"SCAN_CONTRACT"}
    coupled={
      "SNAPSHOT_AS_ADOPTION":{"SNAPSHOT_AS_ADOPTION","ADOPTED_PAGE_TAMPER","PAGE_GENEALOGY_CONTRACT","FULL_NESTED_SCHEMA"},"PROPOSAL_AS_FINAL":{"PROPOSAL_AS_FINAL","FIGURE_VOTE_CONTRACT","FULL_NESTED_SCHEMA"},
      "BUILD_AS_SCIENCE":{"BUILD_AS_SCIENCE","AUTHORITY_CONTRACT"},
      "NEW_PHYSICS_FALSE_PROMOTION":{"NEW_PHYSICS_FALSE_PROMOTION","PHYSICS_CLOSURE_CONTRACT"},
      "PARTIAL_ALL_OF_CLOSURE":{"PARTIAL_ALL_OF_CLOSURE","A06_FALSE_CLOSE","A07_FALSE_CLOSE","PARENT_FALSE_CLOSE","ACCEPTANCE_CONTRACT"},
      "A06_FALSE_CLOSE":{"A06_FALSE_CLOSE","PARTIAL_ALL_OF_CLOSURE","ACCEPTANCE_CONTRACT"},"A07_FALSE_CLOSE":{"A07_FALSE_CLOSE","PARTIAL_ALL_OF_CLOSURE","ACCEPTANCE_CONTRACT"},"PARENT_FALSE_CLOSE":{"PARENT_FALSE_CLOSE","PARTIAL_ALL_OF_CLOSURE","ACCEPTANCE_CONTRACT"},
      "GENERATED_PDF_AS_SOURCE":{"GENERATED_PDF_AS_SOURCE","A02_DECISION_CONTRACT"},"UNNUMBERED_EQUATION_OMISSION":{"UNNUMBERED_EQUATION_OMISSION","UNNUMBERED_DISPLAY_ANCHORS","FULL_NESTED_SCHEMA"},"ADOPTED_PAGE_TAMPER":{"ADOPTED_PAGE_TAMPER","PAGE_GENEALOGY_CONTRACT"},"MATRIX_SCHEMA":{"MATRIX_SCHEMA","FULL_NESTED_SCHEMA"},"CONTROLLED_ASSET_ROWS":{"CONTROLLED_ASSET_ROWS","FULL_NESTED_SCHEMA"},"NUMBERED_EQUATION_ANCHORS":{"NUMBERED_EQUATION_ANCHORS","FULL_NESTED_SCHEMA"},"DRAFT_ADOPTION_ROUTES":{"DRAFT_ADOPTION_ROUTES","PAGE_GENEALOGY_CONTRACT"},"EVIDENCE_LINK_REMOVAL":{"EVIDENCE_LINK_REMOVAL","FULL_NESTED_SCHEMA"},"DRAFT_PAGE_TAMPER":{"DRAFT_PAGE_TAMPER","PAGE_GENEALOGY_CONTRACT"},"NEGATIVE_MANIFEST":{"NEGATIVE_MANIFEST","FULL_NESTED_SCHEMA"},"BUILD_AUDIT_SCHEMA":{"BUILD_AUDIT_SCHEMA","FULL_NESTED_SCHEMA"},"FIGURE_VOTE_CONTRACT":{"FIGURE_VOTE_CONTRACT","PAGE_GENEALOGY_CONTRACT"},"FIGURE_DECISION_EVIDENCE":{"FIGURE_DECISION_EVIDENCE","PAGE_GENEALOGY_CONTRACT","FULL_NESTED_SCHEMA"},"CONTROLLED_SOURCE_PATHS":{"CONTROLLED_ASSET_PROVENANCE","FULL_NESTED_SCHEMA"},"PAGE_GENEALOGY_CONTRACT":{"PAGE_GENEALOGY_CONTRACT","FULL_NESTED_SCHEMA"},"BUILD_TEMP_CLEANUP":{"BUILD_RUNTIME_METADATA","FULL_NESTED_SCHEMA"},"ACCEPTANCE_CONTRACT":{"ACCEPTANCE_CONTRACT","FULL_NESTED_SCHEMA"},"A02_DRAFT_EVIDENCE":{"A02_DECISION_CONTRACT","PAGE_GENEALOGY_CONTRACT"},"SCHEMA_Q_STATE":{"FULL_NESTED_SCHEMA","Q_CHAIN"},"SCHEMA_FINDING":{"FULL_NESTED_SCHEMA","FINDING_SET"},"SCHEMA_PAGE_ROW":{"FULL_NESTED_SCHEMA","PAGE_GENEALOGY_CONTRACT"},"SCHEMA_NESTED_MISSING":{"FULL_NESTED_SCHEMA","FINDING_SET"},"Q_CHANGED_PATHS":{"Q_CHAIN","FULL_NESTED_SCHEMA"}}
    seen=set();failures=[];coupled_signatures=0
    if len(cases)!=80:raise ValidationError(f"NEGATIVE_FIXTURE_COUNT:{len(cases)}")
    for name,mut in cases:
        x=copy.deepcopy(m);mut(x);obs=diagnostics(x);expected=set() if name=="ARBITRARY_SCALAR" else set(coupled.get(name,{aliases.get(name,name)}));expected.add("MATRIX_CANONICAL_DIGEST");coupled_signatures+=len(expected)>1
        if obs!=expected:failures.append((name,sorted(expected),sorted(obs)))
        seen.update(obs)
    if failures:raise ValidationError("NEGATIVE_SIGNATURES:"+json.dumps(failures,ensure_ascii=False,separators=(",",":")))
    if seen!=set(CONTROLS):raise ValidationError(f"NEGATIVE_MANIFEST_COVERAGE:missing={sorted(set(CONTROLS)-seen)}:extra={sorted(seen-set(CONTROLS))}")
    print(f"PASS_P062_STEP56_MATRIX_CONTROLS named=54 mutation_cases=80 exact_signatures=80 coupled_signatures={coupled_signatures}")

def determinism():
    with tempfile.TemporaryDirectory(prefix="p062-step56-") as td:
        out=[]
        for i in range(2):
            m=Path(td)/f"m{i}.json";r=Path(td)/f"r{i}.md";cp=proc([sys.executable,str(REPO/BUILDER),"--repo",str(REPO),"--matrix",str(m),"--result",str(r)],timeout=120)
            if cp.returncode:raise ValidationError("BUILDER_RERUN")
            out.append((m.read_bytes(),r.read_bytes()))
        if out[0]!=out[1] or out[0]!=((REPO/MATRIX).read_bytes(),(REPO/RESULT).read_bytes()):raise ValidationError("BUILDER_NONDETERMINISTIC")
    print("PASS_P062_STEP56_DETERMINISM 2/2")
def clean_build(mode:str):
    drivers=[("appendix_phase_separation.tex",8),("graphite_ica_ch1_v1.0.21.tex",76),("graphite_ica_ch1_v1.0.21_nav.tex",78),("graphite_ica_ch2_v1.0.21.tex",26),("graphite_ica_ch2_v1.0.21_nav.tex",26)]
    cp=proc(["git","archive","--format=zip",BASELINE,"--","Claude/docs/v1.0.21"],timeout=120,text=False)
    if cp.returncode:raise ValidationError("CLEAN_BUILD_ARCHIVE")
    archive_sha=sha(cp.stdout)
    with tempfile.TemporaryDirectory(prefix="p062-step56-build-") as td:
        root=Path(td).resolve()
        if REPO.resolve() in root.parents or root==REPO.resolve():raise ValidationError("CLEAN_BUILD_TEMP_BOUNDARY")
        z=zipfile.ZipFile(io.BytesIO(cp.stdout))
        for member in z.infolist():
            target=(root/member.filename).resolve()
            if root not in target.parents and target!=root:raise ValidationError("CLEAN_BUILD_ARCHIVE_TRAVERSAL")
        z.extractall(root);cwd=root/"Claude/docs/v1.0.21"
        observed=[]
        for driver,pages in drivers:
            for _ in range(3):
                run=proc(["xelatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",driver],cwd,180)
                if run.returncode:raise ValidationError(f"CLEAN_BUILD_XELATEX:{driver}:{run.returncode}:{run.stdout[-2000:]}:{run.stderr[-1000:]}")
            log=(cwd/Path(driver).with_suffix(".log")).read_text(encoding="utf-8",errors="replace")
            bad={"refs":len(re.findall(r"undefined references?",log,re.I)),"cites":len(re.findall(r"Citation .* undefined",log,re.I)),"multiply":len(re.findall(r"multiply defined",log,re.I)),"glyph":len(re.findall(r"Missing character",log,re.I))}
            aux=(cwd/Path(driver).with_suffix(".aux")).read_text(encoding="utf-8",errors="replace")
            label_count=len(re.findall(r"^\\newlabel\{",aux,re.M))
            info=proc(["pdfinfo",str(cwd/Path(driver).with_suffix(".pdf"))],cwd,45)
            match=re.search(r"^Pages:\s+(\d+)$",info.stdout,re.M)
            got=int(match.group(1)) if info.returncode==0 and match else -1
            expected_labels=[30,248,255,72,72][len(observed)]
            if got!=pages or label_count!=expected_labels or any(bad.values()):raise ValidationError(f"CLEAN_BUILD_RESULT:{driver}:pages={got}:labels={label_count}:diagnostics={bad}")
            observed.append(got)
    print(f"PASS_P062_STEP56_CLEAN_BUILD mode={mode} drivers=5/5 passes=15/15 pages={'/'.join(map(str,observed))} refs/cites/multiply/glyph=0/0/0/0 archive_sha256={archive_sha}")
def status_paths(repo=REPO):
    raw=git(["status","--porcelain=v1","--untracked-files=all","-z"],repo,text=False);parts=raw.split(b"\0");out=set();i=0
    while i<len(parts) and parts[i]:
        e=parts[i];s=e[:2].decode();out.add(e[3:].decode().replace("\\","/"));i+=1
        if "R" in s or "C" in s:
            if i<len(parts) and parts[i]:out.add(parts[i].decode().replace("\\","/"));i+=1
    return out
def symbolic(repo=REPO):
    cp=proc(["git","symbolic-ref","--quiet","--short","HEAD"],repo,45);return cp.stdout.strip() if cp.returncode==0 else None
def precommit_diagnostics(repo:Path,staged:bool,branch:str,head:str,protected_branch:str,protected:str,exact:tuple[str,...],check_claude:bool)->set[str]:
    o=set();actual=status_paths(repo);expected=set(exact)
    if symbolic(repo)!=branch:o.add("GIT_BRANCH")
    try:
        if git(["rev-parse","HEAD"],repo).strip()!=head:o.add("GIT_HEAD")
    except Exception:o.add("GIT_HEAD")
    try:
        if git(["rev-parse",f"refs/heads/{protected_branch}"],repo).strip()!=protected:o.add("GIT_LOCAL_PROTECTED")
    except Exception:o.add("GIT_LOCAL_PROTECTED")
    if staged:
        cached=set(filter(None,git(["diff","--cached","--name-only"],repo).splitlines()));unstaged=set(filter(None,git(["diff","--name-only"],repo).splitlines()))
        if cached!=expected:o.add("GIT_STAGED_MISMATCH")
        if unstaged:o.add("GIT_WORKTREE_INDEX_DIVERGENCE")
        if actual-cached:o.add("GIT_EXTRA_DIRTY")
    else:
        if expected-actual:o.add("GIT_WORKTREE_EXACT_SEVEN")
        if actual-expected:o.add("GIT_EXTRA_DIRTY")
    if check_claude and not o:
        if git(["diff","--name-only",f"{protected}..HEAD","--","Claude"],repo).strip():o.add("CLAUDE_DRIFT")
    return o

def precommit(staged):
    d=precommit_diagnostics(REPO,staged,BRANCH,PARENT,PROTECTED_BRANCH,PROTECTED,EXACT_SEVEN,True)
    if d:raise ValidationError("PRECOMMIT:"+",".join(sorted(d)))

def live(ref:str,repo:Path=REPO)->str|None:
    cp=proc(["git","ls-remote","origin",ref],repo,45);f=cp.stdout.split()
    return f[0] if cp.returncode==0 and len(f)==2 else None

def persistence_diagnostics(repo:Path,branch:str,parent:str,subject:str,exact:tuple[str,...],protected_branch:str,protected:str,main:str)->set[str]:
    o=set();head=git(["rev-parse","HEAD"],repo).strip()
    if symbolic(repo)!=branch:o.add("GIT_BRANCH")
    if status_paths(repo):o.add("GIT_PERSISTENCE_EXACT_SEVEN")
    if git(["rev-parse","HEAD^"],repo).strip()!=parent:o.add("GIT_PERSISTENCE_PARENT")
    if git(["show","-s","--format=%s","HEAD"],repo).strip()!=subject:o.add("GIT_PERSISTENCE_SUBJECT")
    if set(filter(None,git(["show","--format=","--name-only","HEAD"],repo).splitlines()))!=set(exact):o.add("GIT_PERSISTENCE_EXACT_SEVEN")
    upstream=f"origin/{branch}"
    try:upstream_tip=git(["rev-parse",upstream],repo).strip()
    except Exception:upstream_tip=None
    if head!=upstream_tip or head!=live("refs/heads/"+branch,repo):o.add("GIT_REMOTE_ACTIVE")
    try:local_protected=git(["rev-parse",f"refs/heads/{protected_branch}"],repo).strip()
    except Exception:local_protected=None
    if local_protected!=protected:o.add("GIT_LOCAL_PROTECTED")
    if live("refs/heads/"+protected_branch,repo)!=protected:o.add("GIT_REMOTE_PROTECTED")
    if live("refs/heads/main",repo)!=main:o.add("GIT_REMOTE_MAIN")
    return o

def persistence():
    d=persistence_diagnostics(REPO,BRANCH,PARENT,SUBJECT,EXACT_SEVEN,PROTECTED_BRANCH,PROTECTED,MAIN)
    if d:raise ValidationError("PERSISTENCE:"+",".join(sorted(d)))
    print("PASS_P062_STEP56_PERSISTENCE")

def docs_diagnostics(root:Path)->set[str]:
    o=set();result=(root/RESULT).read_text(encoding="utf-8")
    if any(sha((root/path).read_bytes().replace(b"\r\n",b"\n"))!=expected for path,expected in DOC_LF_SHA.items()):o.add("DOC_CONTENT_DIGEST")
    gates=re.findall(r"^Gate: `([^`]+)`\s*$",result,re.M);terminals=re.findall(r"^Terminal: `([^`]+)`\s*$",result,re.M);commits=re.findall(r"^Containing commit: `([^`]+)`\s*$",result,re.M)
    bad_word=r"(?:FAIL|CONDITIONAL|BLOCKED)"
    gate_label=r"(?:(?:Current|Overall)[ _-]+)?(?:gate|status)"
    terminal_label=r"(?:(?:Current|Overall)[ _-]+)?terminal"
    gate_bad=re.search(rf"^{gate_label}\s*:.*\b{bad_word}\b",result,re.I|re.M) or re.search(rf"^##+\s*{gate_label}\s*$\r?\n\s*`?{bad_word}\b",result,re.I|re.M)
    terminal_bad=re.search(rf"^{terminal_label}\s*:.*\b{bad_word}\b",result,re.I|re.M) or re.search(rf"^##+\s*{terminal_label}\s*$\r?\n\s*`?{bad_word}\b",result,re.I|re.M)
    if gates!=["PASS_WITH_CONCERNS"] or commits!=["PENDING_AT_PRECOMMIT_BY_DESIGN"] or gate_bad:o.add("DOC_RESULT_GATE_UNIQUENESS")
    if terminals!=["PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS"] or terminal_bad:o.add("DOC_RESULT_TERMINAL_UNIQUENESS")
    result_tokens=(MATRIX_SHA,"A01/A02/A03/A04/A05","OPEN/OPEN/OPEN","adopted `12/12`","non-adopted `36/36`","forbidden rendered `21`","P1_LAYOUT","named controls: `74/74`","attack fixtures: `112/112`",STRUCTURAL_SCHEMA_SHA,BUILDER_FULL_AST_SHA,"PASS_P062_STEP56_PERSISTENCE")
    if any(token not in result for token in result_tokens):o.add("DOC_RESULT_GATE_UNIQUENESS")
    specs=((PARENT_LEDGER,"| 062 | 52–57 |","DOC_PARENT_LEDGER_STEP56_ROW"),(ACTIVE_LEDGER,"| Step 56 |","DOC_ACTIVE_LEDGER_STEP56_ROW"),(HANDOVER,"| Phase 062 Step 56 |","DOC_HANDOVER_STEP56_ROW"))
    required=(PARENT,"PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS","named controls `74/74`","attack fixtures `112/112`","P1_LAYOUT","PASS_P062_STEP56_PERSISTENCE")
    for path,prefix,name in specs:
        text=(root/path).read_text(encoding="utf-8");rows=[line for line in text.splitlines() if line.startswith(prefix)]
        contradictions=[line for line in text.splitlines() if re.search(r"(?:Phase 062.*Step 56|Step 56).*\b(?:FAIL|CONDITIONAL|BLOCKED)\b",line,re.I) or re.search(r"Step 57\.1\s+(?:is\s+)?(?:ALLOWED|COMPLETE|COMPLETED)\b",line,re.I)]
        if "PASS_P062_STEP55_PERSISTENCE" not in text or len(rows)!=1 or any(token not in rows[0] for token in required) or contradictions:o.add(name)
    return o

def docs():
    d=docs_diagnostics(REPO)
    if d:raise ValidationError("DOCS:"+",".join(sorted(d)))

def docs_negative():
    cases=(("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\nGate: `FAIL`\n"),("DOC_RESULT_TERMINAL_UNIQUENESS",RESULT,"\nTerminal: `FAIL`\n"),("DOC_PARENT_LEDGER_STEP56_ROW",PARENT_LEDGER,"\n| 062 | 52–57 | contradictory Step 56 |\n"),("DOC_ACTIVE_LEDGER_STEP56_ROW",ACTIVE_LEDGER,"\n| Step 56 | contradictory |\n"),("DOC_HANDOVER_STEP56_ROW",HANDOVER,"\n| Phase 062 Step 56 | contradictory |\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\nOverall gate: FAIL\n"),("DOC_PARENT_LEDGER_STEP56_ROW",PARENT_LEDGER,"\nPhase 062 Step 56 status: FAIL\n"),("DOC_ACTIVE_LEDGER_STEP56_ROW",ACTIVE_LEDGER,"\nStep 56 status: FAIL\n"),("DOC_HANDOVER_STEP56_ROW",HANDOVER,"\nPhase 062 Step 56 gate: FAIL\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\nCurrent status: FAIL\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\n## Status\nFAIL\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\nCurrent gate: CONDITIONAL\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\nOverall status: BLOCKED\n"),("DOC_RESULT_TERMINAL_UNIQUENESS",RESULT,"\nCurrent terminal: BLOCKED\n"),("DOC_RESULT_TERMINAL_UNIQUENESS",RESULT,"\nOverall terminal: CONDITIONAL\n"),("DOC_RESULT_GATE_UNIQUENESS",RESULT,"\n## Current gate\nBLOCKED\n"),("DOC_RESULT_TERMINAL_UNIQUENESS",RESULT,"\n## Overall terminal\nFAIL\n"),(None,RESULT,"\nopaque append without state words\n"))
    coupled_signatures=0
    for name,path,suffix in cases:
        with tempfile.TemporaryDirectory(prefix="p062-step56-doc-") as td:
            root=Path(td).resolve()
            if root==REPO.resolve() or REPO.resolve() in root.parents:raise ValidationError("DOC_TEMP_BOUNDARY")
            for source in (RESULT,PARENT_LEDGER,ACTIVE_LEDGER,HANDOVER):
                target=root/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(REPO/source,target)
            with (root/path).open("a",encoding="utf-8",newline="\n") as f:f.write(suffix)
            observed=docs_diagnostics(root)
            expected={"DOC_CONTENT_DIGEST"}|({name} if name else set());coupled_signatures+=len(expected)>1
            if observed!=expected:raise ValidationError(f"DOC_SIGNATURE:{name}:{sorted(observed)}")
    print(f"PASS_P062_STEP56_DOC_CONTROLS named=6 attack_fixtures=18 exact_signatures=18 coupled_signatures={coupled_signatures}")

def fixture_write(repo:Path,path:str,text:str)->None:
    target=repo/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding="utf-8",newline="\n")

def fixture_init(repo:Path)->str:
    repo.mkdir(parents=True);git(["init","-b","main"],repo);git(["config","user.name","Phase062 Fixture"],repo);git(["config","user.email","phase062@example.invalid"],repo)
    fixture_write(repo,"seed.txt","seed\n");git(["add","seed.txt"],repo);git(["commit","-m","seed"],repo);base=git(["rev-parse","HEAD"],repo).strip();git(["branch","protected",base],repo);git(["switch","-c","active"],repo);return base

def git_precommit_fixture(name:str)->set[str]:
    with tempfile.TemporaryDirectory(prefix="p062-step56-git-pre-") as td:
        root=Path(td).resolve();repo=root/"repo"
        if root==REPO.resolve() or REPO.resolve() in root.parents:raise ValidationError("GIT_TEMP_BOUNDARY")
        base=fixture_init(repo);exact=tuple(f"Codex/exact-{i}.txt" for i in range(1,8));branch="active";protected=base
        if name=="GIT_BRANCH":git(["switch","-c","wrong"],repo)
        elif name=="GIT_HEAD":fixture_write(repo,"advance.txt","advance\n");git(["add","advance.txt"],repo);git(["commit","-m","advance"],repo)
        elif name=="GIT_LOCAL_PROTECTED":
            git(["switch","-c","drift"],repo);git(["commit","--allow-empty","-m","drift"],repo);drift=git(["rev-parse","HEAD"],repo).strip();git(["switch","active"],repo);git(["branch","-f","protected",drift],repo)
        paths=exact[:-1] if name=="GIT_WORKTREE_EXACT_SEVEN" else exact
        for path in paths:fixture_write(repo,path,path+"\n")
        staged=name in {"GIT_STAGED_MISMATCH","GIT_WORKTREE_INDEX_DIVERGENCE"}
        if name=="GIT_EXTRA_DIRTY":fixture_write(repo,"extra.txt","extra\n")
        if name=="GIT_STAGED_MISMATCH":fixture_write(repo,"extra.txt","extra\n");git(["add","--",*exact,"extra.txt"],repo)
        elif name=="GIT_WORKTREE_INDEX_DIVERGENCE":git(["add","--",*exact],repo);fixture_write(repo,exact[0],"changed after stage\n")
        observed=precommit_diagnostics(repo,staged,branch,base,"protected",protected,exact,False)
        if observed!={name}:raise ValidationError(f"GIT_SIGNATURE:{name}:{sorted(observed)}")
        return observed

def git_persistence_fixture(name:str)->set[str]:
    with tempfile.TemporaryDirectory(prefix="p062-step56-git-post-") as td:
        root=Path(td).resolve();repo=root/"repo";origin=root/"origin.git"
        if root==REPO.resolve() or REPO.resolve() in root.parents:raise ValidationError("GIT_TEMP_BOUNDARY")
        base=fixture_init(repo);exact=tuple(f"Codex/exact-{i}.txt" for i in range(1,8));subject="fixture subject"
        if name=="GIT_PERSISTENCE_PARENT":fixture_write(repo,"middle.txt","middle\n");git(["add","middle.txt"],repo);git(["commit","-m","middle"],repo)
        paths=exact[:-1] if name=="GIT_PERSISTENCE_EXACT_SEVEN" else exact
        for path in paths:fixture_write(repo,path,path+"\n")
        git(["add","--",*paths],repo);git(["commit","-m","wrong subject" if name=="GIT_PERSISTENCE_SUBJECT" else subject],repo);head=git(["rev-parse","HEAD"],repo).strip()
        git(["init","--bare",str(origin)],root);git(["remote","add","origin",str(origin)],repo)
        git(["push","origin","active:refs/heads/active","protected:refs/heads/protected","main:refs/heads/main"],repo);git(["branch","--set-upstream-to=origin/active","active"],repo)
        if name=="GIT_REMOTE_ACTIVE":git(["--git-dir",str(origin),"update-ref","refs/heads/active",base],root)
        elif name=="GIT_REMOTE_PROTECTED":git(["--git-dir",str(origin),"update-ref","refs/heads/protected",head],root)
        elif name=="GIT_REMOTE_MAIN":git(["--git-dir",str(origin),"update-ref","refs/heads/main",head],root)
        observed=persistence_diagnostics(repo,"active",base,subject,exact,"protected",base,base)
        if observed!={name}:raise ValidationError(f"GIT_SIGNATURE:{name}:{sorted(observed)}")
        return observed

def git_negative():
    pre=("GIT_BRANCH","GIT_HEAD","GIT_WORKTREE_EXACT_SEVEN","GIT_EXTRA_DIRTY","GIT_STAGED_MISMATCH","GIT_WORKTREE_INDEX_DIVERGENCE","GIT_LOCAL_PROTECTED")
    post=("GIT_PERSISTENCE_PARENT","GIT_PERSISTENCE_SUBJECT","GIT_PERSISTENCE_EXACT_SEVEN","GIT_REMOTE_ACTIVE","GIT_REMOTE_PROTECTED","GIT_REMOTE_MAIN")
    seen=set()
    for name in pre:seen.update(git_precommit_fixture(name))
    for name in post:seen.update(git_persistence_fixture(name))
    if seen!=set(GIT_CONTROLS):raise ValidationError(f"GIT_MANIFEST_COVERAGE:{sorted(seen)}")
    print("PASS_P062_STEP56_GIT_CONTROLS 13/13 exact_signatures=13 disposable_local_and_bare_origin=PASS cleanup=PASS")
def main():
    p=argparse.ArgumentParser();p.add_argument("--content-only",action="store_true");p.add_argument("--run-negative-probes",action="store_true");p.add_argument("--determinism-check",action="store_true");p.add_argument("--run-clean-build",action="store_true");p.add_argument("--verify-staged",action="store_true");p.add_argument("--verify-persistence",action="store_true");a=p.parse_args();m=validate();print(f"PASS schema content=48/48 decisions=12/36 figures=31/31 builds=5/5 pages=214 code=21 A01-A05=5/5 structural_paths={STRUCTURAL_SCHEMA_PATHS} structural_sha256={STRUCTURAL_SCHEMA_SHA} ast_sha256={BUILDER_FULL_AST_SHA}")
    if a.content_only and (a.verify_staged or a.verify_persistence):raise ValidationError("CLI_MODE_CONFLICT")
    if a.verify_staged and a.verify_persistence:raise ValidationError("CLI_MODE_CONFLICT")
    if a.run_negative_probes:
        negative(m);source_negative();docs_negative();git_negative();print("PASS_P062_STEP56_ALL_CONTROLS named=74 attack_fixtures=112 matrix=54/80 source=1/1 docs=6/18 git=13/13")
    if a.determinism_check:determinism()
    should_build=a.run_clean_build or (not a.content_only and not a.verify_persistence)
    if should_build:clean_build("EXPLICIT" if a.run_clean_build else "AUTO_PRECOMMIT")
    if a.content_only:print("PASS_P062_STEP56_CONTENT");return 0
    docs();persistence() if a.verify_persistence else precommit(a.verify_staged);print("PASS_P062_STEP56_PHYSICS_CLOSURE_WITH_CONCERNS");return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except ValidationError as e:print("FAIL_P062_STEP56:"+str(e));raise SystemExit(1)
