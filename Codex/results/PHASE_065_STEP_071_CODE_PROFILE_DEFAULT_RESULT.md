# Phase 065 Step 71 Code, Profile and Default Static Audit Result

Date: 2026-08-30
Status: `PASS_PENDING_PERSISTENCE`
Phase plan: `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
Expected parent: `d6f680b26fb59c24098f44ed633873a2c6419a4e`
Expected subject: `audit(phase065): trace v1024 code profile defaults`

## 1. Selected Gate

Current Step 71 gate: `PASS_P065_STEP71_STATIC_WITH_CONCERNS`; commit/push persistence is pending.

This Gate means that the frozen v1.0.23, v1.0.24, and v1.0.24.1
Python source/test endpoints were completely read and parsed without importing
the checkout; code/profile/default routes, change/non-change boundaries, and
unresolved runtime routes are source-anchored. It does **not** mean that runtime
behavior, scientific validity, material identity, experimental fit, external
primary-literature authority, canonical-model selection, defect repair, or
publication readiness has been established. Those authority flags remain
false.

Step 72 remains locked until the exact-eight Step 71 commit has been pushed,
fetched, and both supported Python runtimes emit
`PASS_P065_STEP71_PERSISTENCE`.

## 2. Recovery and Input Authority

- Active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- Frozen Claude baseline:
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- Step 70 persisted parent:
  `d6f680b26fb59c24098f44ed633873a2c6419a4e`.
- Step 70 was independently re-read at that parent:
  result `1–1720`, topology JSON `45,772` traversed nodes, attestation JSON
  `571` traversed nodes, all stored semantic/cross-bindings equal, all 15
  mandatory evidence groups bound, all 98 routed process commits completely
  classified, no unread interval, and no unresolved output truncation.
- Step 70 exact-eight persistence was re-confirmed on Python 3.12 and 3.14.
- Protected branch pin:
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- Main pin:
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- `Claude/**` was treated as read-only. Every Step 71 source byte was read by
  `git cat-file blob` at the frozen baseline; no frozen module was imported or
  executed.

Guide, brief, result, review, and ledger prose was not accepted as callable
default authority. A default is recorded only where it is bound to a callable
signature and exact frozen source range.

## 3. Complete Python Endpoint Read

The independent read covered every required blob from line 1 through EOF.
All files ended in LF; no unread or truncated interval remains.

| Version | Occurrences | Lines | Static parse | Notes |
|---|---:|---:|---:|---|
| v1.0.23 | 6 | 2,733 | 6/6 | production, gates, self-consistency, P1 observation, curve QA, structure tool |
| v1.0.24 | 7 | 2,881 | 7/7 | production, three gates, structure tool, final sample, reflect curves |
| v1.0.24.1 | 7 | 2,881 | 7/7 | byte-identical counterparts of all seven v1.0.24 endpoints |
| Total | 20 | 8,495 | 20/20 | 12 unique Git blobs; the structure tool is also shared across v1.0.23/v1.0.24 |

The parser is `ast.parse(..., feature_version=(3, 12))`. The generated endpoint
rows bind path, release label, Git blob, raw and LF-normalized SHA-256, byte and
line counts, AST SHA-256, function/class/import node counts, and explicit
`STATIC_PARSE_PASS_NO_IMPORT` status.

Principal production identities are:

- v1.0.23 main blob `554425dd566c20314357eddfcf4261517df907ee`,
  1,585 lines, raw SHA-256
  `0298bb5fdf47ed5faf2f8301b6d84dc88fd580a69c8e616daa3942d35ceae7cf`;
- v1.0.24 main blob `daad1d0a8bcdacda5283b0692382262a7d85d5af`,
  1,734 lines, raw SHA-256
  `f230f59bb10bcc49cdce9047c196530f857d2eda4d3b1be819ceb36ee6aaf680`;
- all seven v1.0.24.1 counterparts have the same blob as their v1.0.24
  counterpart. This is mirror identity, not independent corroboration.

## 4. v1.0.23 to v1.0.24 Static Delta

The callable census contains 52 paired symbols:

- 46 are full-AST identical;
- one has documentation/annotation change while executable statements remain
  identical (`func_dH_a_eff`);
- two retain signatures but change executable statements:
  `GraphiteAnodeDischargeDQDV.equilibrium` and
  `LCOCathodeDQDV._effective_dS_rxn`;
- three are added: `_regsol_binodal_xa`, `_regsol_dqdv`, and
  `LCOCathodeDQDV.__init__`;
- no callable is removed and no common callable signature changes.

In particular, `func_L_q`, `GraphiteAnodeDischargeDQDV.curve`, `dqdv`,
`solve_U_oc`, the blend implementation, and the fallback helpers retain their
v1.0.23 executable AST. The new seconds/hour prose therefore does not itself
constitute executable repair.

## 5. Constructor, Default, Registry and Restoration Matrix

The matrix records 40 argument rows across six callable entry surfaces and 11
named profile/registry surfaces.

### 5.1 Graphite

`GraphiteAnodeDischargeDQDV.__init__`, v1.0.24 lines 368–401, requires
`transitions`. Its declared defaults are `x=0.5`, `Rn=0.0`, `Cbg=0.0`,
`chi=None`, `chi_split=func_chi_d`, `use_dH_eff=True`, `z_cut=4.357`,
`A_cap_RT=4.0`, `seed_T=298.15`, `seed_I=0.1`, `seed_Q_cell=1.0`, and
`lag_ratio_correction=False`. The transition list is stored by reference.
`chi=None` falls back to `x`, while explicit zero is retained.
Both option gates are stored through `bool(...)`: absent `use_dH_eff=True`
turns its route on, while `False`, numeric zero, and `None` turn it off;
absent `lag_ratio_correction=False`, `False`, numeric zero, and `None` are off,
while any truthy value is on.

The `curve` route at lines 733–763 distinguishes `I_abs=None`, which derives
`abs(c_rate*Q_cell)`, from explicit `I_abs=0`, which overrides a nonzero
`c_rate`. Numeric direction zero is mapped to the positive direction.

### 5.2 LCO

v1.0.23 has no LCO constructor and applies the electronic entropy seam
unconditionally. v1.0.24 adds
`LCOCathodeDQDV.__init__(*args, include_electronic_entropy=False, **kwargs)` at
lines 1061–1084. Absent, `False`, numeric zero, and `None` all collapse to off;
a truthy value turns the route on. The calculation uses the stored
`x_center`, not a live composition variable. No named LCO registry entry
contains `Omega`, `kernel`, or an independently wired per-peak interaction
route.

### 5.3 Blend

`BlendedAnodeDQDV.__init__`, lines 1356–1433, declares
`f_Si`, `si_case='sic'`, `graphite_transitions=None`,
`si_transitions=None`, `Cbg=0.0`, and `si_stress_offset=None`.

- graphite `None` selects `GRAPHITE_STAGING_LIT`; an explicit empty list does
  not select the default and reaches the positive-total-Q guard;
- Si `None` selects and validates `SI_CASE_SETS[si_case]`; an explicit Si list
  bypasses named-case membership. In both cases `si_case` is stored and still
  selects `SI_CASE_GAPS.get(si_case, [])`;
- `si_stress_offset=None` skips the offset route. Explicit zero is distinct: it
  passes finite validation and the transition loop but applies a zero offset;
- `from_wt` uses `SI_SPECIFIC_CAPACITY.get(si_case)` only when `q_Si=None`,
  while explicit `q_Si` bypasses that lookup;
- `q_gr` is bound to `GRAPHITE_SPECIFIC_CAPACITY`;
- no Graphite/LCO named-profile factory, model save/load schema,
  `state_dict`, `to_dict`, `from_dict`, legacy restore key, or current saved
  state key exists in the inspected source/test universe.

Five release-side Python endpoints define `importlib.util` module loaders. The
static census requires an ordered, same-binding chain within one lexical module,
function, class, or lambda scope: exact
`importlib.util.spec_from_file_location`, exact
`importlib.util.module_from_spec(spec)`, and then
`spec.loader.exec_module(module)`. Before completion, any non-required load of a
live spec or module invalidates the chain. This includes aliases of the spec,
module, or loader; passing them to unknown calls; attribute/subscript/object
mutation through direct, `object.__setattr__`, `__dict__`, `operator.setitem`,
`vars`, or `getattr` routes; and any potential binding nested in an intervening
`if`, loop, `with`, `try`/`except`/`finally`, or `match` statement. Harmless
independent statements do not invalidate a candidate. In the ordered prefix
through the exact exec, any semantic reference or exposure involving
`eval`, `exec`, `compile`, `__import__`, `importlib.import_module`, `globals`,
`locals`, `vars`, `builtins`, `__builtins__`, `sys._getframe`, `f_locals`,
`f_globals`, `__globals__`, `__getattribute__`, `inspect.currentframe`, or
`sys.modules` invalidates every live candidate.
This includes `sys`/`inspect`/`builtins` imports and bare `importlib` imports,
relevant `ImportFrom` facts, unpacked calls, aliases, containers, annotations,
and computed attribute/subscript/getattr forms without relying on one module
spelling. An `importlib` Name load is admissible only in the current direct,
single-Name-target assignment when the exact two-argument
`importlib.util.spec_from_file_location` assignment creates a live spec or the
exact one-argument `importlib.util.module_from_spec(spec)` assignment advances
that same live chain. An exact-shaped call transported through a consumer,
container, attribute target, or multiple assignment is not exempt; every other
pre-exec `importlib` Name load is danger. The sole `sys`-import exception is the exact frozen,
stable-AST-hash-pinned `import numpy as np, importlib.util, sys` statement used
by two result scripts; that import fact does not authorize any semantic `sys`
load before completion, so assignment, container, argument, return, or
computed-`getattr` use of `sys` invalidates the candidate. Wildcard
`ImportFrom` from `sys`, `importlib`, `inspect`, or `builtins` is likewise
dangerous;
exact unaliased `import importlib.util` and the exact three required loader calls
also remain admissible.
For the non-frozen four-statement grammar, the spec and module assignment
targets must be distinct identifiers, neither target may reuse a reserved
loader/execution/frame/import root, `module_from_spec` must consume the immediately preceding
live spec role, and `exec_module` must use that spec as receiver and that module
as its sole argument. The shared exact-spelling boundary covers
`eval`, `exec`, `compile`, `__import__`, `import_module`, `_getframe`,
`currentframe`, `f_locals`, `f_globals`, `__globals__`, `__getattribute__`,
`getattr`, `attrgetter`, `methodcaller`, `subprocess`, `os`, `importlib`, `sys`,
`inspect`, `builtins`, `__builtins__`, `operator`, `_operator`, `globals`,
`locals`, and `vars` for both roles. Python identifier matching remains
case-sensitive and adjacent longer dunder spellings are not conflated with the
listed exact names.
A danger marker after a completed exact exec does not retroactively erase that
completed chain, but it prevents a later candidate from being certified. The
census does not attempt branch-sensitive proof: any pre-exec uncertain use
fails closed. Same-spelled names in another scope cannot complete it. The
recognized chains
occur in the main gate, self-consistency gate, reflect gate, final-sample script,
and reflect-curves script. This conservative
straight-line census does not model arbitrary branch/exception control flow.
It is static evidence that those five fresh module-load paths
exist; whether they succeed and which defaults they observe remain reserved for
the isolated runtime gate. Consequently, the four route outcomes are fixed as:

| Route | Static result |
|---|---|
| fresh module load | `STATIC_TEST_LOADERS_PRESENT_RUNTIME_PENDING` |
| explicit profile injection | `STATIC_ENTRYPOINT_PRESENT_RUNTIME_PENDING` |
| legacy saved-state restoration | `ABSENT_IN_FROZEN_SOURCE` |
| current saved-state restoration | `ABSENT_IN_FROZEN_SOURCE` |

## 6. Feature Routing Findings

### 6.1 Regular-solution split

The helpers `_regsol_binodal_xa` and `_regsol_dqdv` occupy lines 119–145.
The sole production activation is the exact
`tr.get('kernel') == 'regsol'` branch in graphite `equilibrium`, lines
597–602. Named graphite, LCO, and Si profiles contain no `kernel` key.
`dqdv` lines 679–726, `entropy_coefficient` lines 813–834, and
`solve_U_oc` lines 884–910 remain logistic and ignore the kernel selector.

Therefore:

- the regular-solution route is explicit opt-in and equilibrium-only;
- it is reachable by a custom transition dictionary, including through blend
  hosts, but not by a frozen named Si profile;
- `GRAPHITE_STAGING_XRD_v1024` having `Omega` fields does not make it a
  regular-solution profile;
- absent, `None`, false, `logistic`, or an unknown kernel spelling silently
  selects logistic behavior;
- absent `delta` falls back to the computed width, while zero or negative
  `delta` is silently clamped to `1e-9` inside `_regsol_dqdv`.

### 6.2 Graphite feature ladders

- `GRAPHITE_STAGING_LIT` is the four-transition default.
- `GRAPHITE_STAGING_XRD_v1024`, lines 1157–1183, is a manual five-feature
  opt-in with no kernel keys. Its frozen reflect check covers only limited
  shape/separation conditions, not cross-method kernel consistency.
- `GRAPHITE_STAGING_MSMR6_LIT`, lines 1187–1205, is a declared six-gallery
  logistic option. No activation reference occurs in the seven frozen v1.0.24
  Python endpoints. This is deliberately narrower than “no release reference”:
  six documentation references do exist in `CODE_GUIDE_v24.md` (lines 284,
  334), `CODE_GUIDE_v24.html` (lines 183, 210), `HANDOVER_v24.md` (line 73),
  and `INDEX_v24.md` (line 17). No dedicated Python gate was found.

### 6.3 Blend current and capacity

The blend calculates `self.Q_gr`, `self.Q_Si`, and `self.Q` at lines
1401–1419. At lines 1480–1501 it nevertheless sends the same full
`I_abs`/`c_rate` and external `Q_cell` to both hosts. No current partition law
or validation binding external `Q_cell` to `self.Q` was found, and
`nonadditive_correction` is explicitly unimplemented.

## 7. Defect and Non-change Boundaries

All runtime conclusions below are `WITHHELD_TO_STEP_73`. The table records
descriptive dispositions, while the validator separately enforces only the
listed static predicates; it does not convert those predicates into runtime
evidence.

| Boundary | Static determination | Required continuation |
|---|---|---|
| seconds/hour | comment-only change; executable `func_L_q` inherited and its AST contains no division by numeric 3600 | Step 72 unit/migration contract; Step 73 equivalence probes |
| current partition | inherited unchanged from v1.0.23; no partition law | Step 72 capacity/current contract; Step 73 conservation probes |
| capacity basis | `self.Q` is assigned in blend initialization, while blend `dqdv` and `curve` contain no load of `self.Q`; external `Q_cell` remains unbound | Step 72 basis selection; Step 73 endpoint and mixture tests |
| root validation | a parent-map proof admits exactly one `max_iter` Load in the direct `_` loop bound `range(int(max_iter))` and exactly one `tol` Load as the right comparator of the direct `if hi - lo < tol: break` convergence test; any other semantic Load of either parameter anywhere in the complete root-function subtree, including assignment, container, destructuring, default, helper, call, or lambda capture, is treated as potential explicit validation and blocks the absence claim; any semantic `getattr`/`vars`/`globals`/`locals`/`eval`/`exec`/`compile` reference or `__globals__`/`__builtins__`/`__getattribute__`/frame/module/import marker anywhere in that subtree likewise conservatively counts as potential explicit validation of both parameters without call-graph or constructed-name decoding; the exact `out[k] = 0.5 * (lo + hi)` assignment is structurally after the inner iteration loop in the outer-loop body | Step 72 exception/convergence contract; Step 73 adversarial tests |
| fallback routes | exact kernel equality selects regsol, missing delta uses width, nonpositive delta clamps to `1e-9`, and missing `n` yields width factor `1.0` while `_dwdT` yields zero | Step 72 explicit schema; Step 73 route matrix |

One additional P1 static inconsistency is fixed for routing: when a transition
has neither `n` nor `w`, `_n_factor` returns `1.0`, creating a thermal width,
but `_dwdT` returns `0.0` when `n` is absent. Explicit `n_T1=None` is also
treated as absent by `_n_factor` but passed to the finite-number validator by
`_dwdT`.

## 8. Findings and Authority Ceiling

The independent technical census selected P0/P1/P2 = `0/6/4`. The integrated
machine matrix records P0/P1/P2 = `0/7/6` because it additionally gives a
separate P1 identity to the absent persistence/migration contract and retains
two P2 provenance routes inherited from Step 70. This is a wider routing
denominator, not a severity contradiction.

The six core P1 findings are:

1. regular-solution equilibrium versus logistic dQ/dV/entropy/root split;
2. missing blend current-partition and capacity-closure contract;
3. incomplete root input/convergence validation and silent exhaustion;
4. seconds/hour change confined to comments;
5. width fallback versus thermal-derivative inconsistency; and
6. LCO electronic-entropy/live-composition and per-peak-interaction contract
   gap.

The four core P2 findings are kernel/delta validation, named profile/factory
coverage, saved-state migration absence, and mutable/silent fallback
visibility. No source-backed basis exists here to choose a canonical profile
or current-sharing law. That choice is intentionally not fabricated.

Step 70 routes F08, F09, F19, F22, F24, F25, and F33–F40 remain preserved in
the machine findings. A web-accessible author-upload candidate for Ref. 7 DOI
`10.1063/1.4802584` was located during recovery, but it is not part of this
frozen static-code Gate and is not promoted here. Step 72 must acquire, hash,
read, and bind the document before changing the Phase 064 literature status.

## 9. Validation Design and Current Evidence

The builder writes canonical strict JSON and exposes `build_artifacts()`.
The validator independently replays every endpoint from Git, rejects duplicate
keys/non-finite constants/noncanonical bytes, traverses the complete JSON,
checks semantic hashes and cross-bindings, runs 488 named semantic probes,
runs six strict-JSON negative cases, and rebuilds twice for
determinism. Source policy pins the complete import statement signature of each
audited builder/validator, rejects added network or child-process module roots,
and permits path-sensitive receivers only through the read-only method surface
actually used by the audited sources or the five exact collector mutations.

The initial validator-first run correctly failed with
`E_BUILDER_MISSING`. A first cross-runtime attempt then rejected all endpoint
hashes because Python 3.14 omits empty AST fields from its default dump. The
builder and independent validator were corrected to serialize every AST field
through a version-independent canonical tree while retaining the pinned Python
3.12 grammar. The rejected evidence was not accepted or staged.

After the full repair, both Python 3.12 and 3.14 emitted:

`PASS_P065_STEP71_CONTENT {"attestation_nodes": 46, "determinism": "2/2", "matrix_nodes": 2482, "mode": "content", "semantic_cases": 488, "source_policy_cases": 361, "strict_json_cases": 6}`

The first independent staged reviews then found blocking P1 defects in the
candidate evidence. The current/capacity boundaries incorrectly said that the
blend route was added in v1.0.24 even though it is AST-identical to v1.0.23;
the saved-state finding also overclaimed that no model factory existed despite
`BlendedAnodeDQDV.from_wt`. Both statements were corrected before commit. The
validator now independently reconstructs the recorded fields of all 40 selected
initialization rows, source-derives the default routes of all 11 profile
surfaces, replays all 52 lineage rows, and compares all 13 feature-route records
and all five defect-boundary records with its independent replay. The
load-bearing initialization, feature, and defect claims listed above also have
explicit AST/source predicates. It
also inventories model persistence callables, restoration keys, and factory
entry points: no saved-state contract exists, while
`BlendedAnodeDQDV.from_wt` remains explicitly present. The review additionally
corrected the three variadic forwarding descriptions so LCO `**kwargs`, blend
`**host_kwargs`, and `from_wt` `**kwargs` no longer share one overbroad label.
It further bound the `chi=None`, numeric-direction-zero, and blend `I_abs=None`
fallbacks to their actual source routes, corrected the regular-solution entry
from an indexing overstatement to `tr.get('kernel')`, and separated the five
static fresh-load endpoints from the absent saved-state restoration routes.

The same review found that the first validator did not implement the detailed
plan's full source-policy and Git boundary contract. The corrected validator
requires the exact builder/validator definition set and pins the complete
top-level `run_process`, `run_git`, and validator `load_builder` AST shapes. It
rejects protected-name Store/Del targets through assignment, annotation,
destructuring, walrus, loop/comprehension targets, parameters, imports, classes,
exception targets, all match capture forms, and every sensitive definition not
represented by the exact direct `Module.body` definition node; this includes
module-level `if`, `try`, `with`, `match`, and loop-nested definitions. It also
rejects mutation targets rooted in protected callables, execution modules,
`builtins`/`__builtins__`, `sys.modules`, `__globals__`, `f_globals`, or
`f_locals`, including nested tuple/list,
attribute, subscript, `__code__`, `__defaults__`, `__dict__`, `setattr`,
`delattr`, and mutator-call routes. It recursively rejects sensitive
references captured through positional/keyword arguments, function or lambda
defaults, decorators, and containers. A generic descendant traversal covers
binary, Boolean, unary, conditional, formatted-string, comparison, slice,
subscript, and comprehension wrappers rather than relying on an expression-type
allowlist. It rejects escape through function or property returns, `yield`,
`yield from`, lambda bodies, and returned callable/container surfaces. Exact
current execution calls are exempted only when separately whole-AST and
call-contract pinned in place. It also rejects `__import__`, dynamic
attributes, `sys.modules`, `vars` variants, non-direct `getattr` transport,
`operator`/`_operator` imports/roots, dotted-module imports, and receiver-independent
`attrgetter`/`methodcaller` retrieval, aliased
`spec_from_file_location`, aliased or indirect `loader.exec_module` access, and
non-`util` importlib submodule/from-import roots.
Because no valid builder or validator route needs a dynamic namespace mapping,
the policy fails closed on every semantic reference to `globals`, `locals`,
`vars`, `builtins`, `__builtins__`, `__globals__`, `f_globals`, `f_locals`,
`_getframe`, `currentframe`, or `__getattribute__`, regardless of direct arguments, unpacked
arguments, alias, container, return, annotation, or direct-call position.
Imports of `builtins` and computed attribute/subscript routes are rejected by
the same broad rule; this is a full semantic-root ban rather than an arity or
string-key census. Function parameter and return annotations, `AnnAssign`
annotations, class bases/keywords, Python 3.12 type-parameter bounds, supported
type-parameter defaults, and `TypeAlias` values/type parameters all receive the
same generic captured-reference inspection. Every other semantic sensitive
load is rejected in every AST expression context; the only exemptions are the
target-expression nodes of exact separately pinned current calls and the
whole-function-pinned loader contract. Source is parsed with type comments
enabled, and every function, assignment, loop, or `with` type comment is
rejected because neither valid file requires one. Plain and tagged
`# type: ignore` entries are likewise rejected through the parsed module's
`type_ignores`; `eval`, `exec`, and `compile` are protected semantic loads in
addition to being forbidden direct calls.
Every Git read remains pinned to a required exact top-level caller and complete
call AST; omission of a required caller fails closed. Filesystem policy rejects
`Path.touch`, path `move`/`move_into`/replace, stream/file `write`, `writelines`, and
`truncate`, while built-in `open` and `Path.open` accept only an omitted mode or
one of the literal read-only modes `r`, `rb`, `rt`, `br`, or `tr`; a nonliteral,
starred, or keyword-unpacked mode route fails closed. It permits only five exact filesystem mutations in the
unique atomic collector. The collector's ordered seven-statement prefix accepts
only `Codex/results`, verifies that the human result is already staged and
byte-identical to the worktree, and only then replaces the two JSON files;
dead-string lookalikes cannot satisfy this check. The final source policy also
permits the frozen builder import/exec chain only in the exact whole-AST-pinned
validator `load_builder` function. One recursive syntactic path-value predicate
covers the case-folded naming conventions `path`, `filepath`, `*_path`, and
`*_file`; directly proven aliases; `pathlib.Path`, `PurePath`, platform-specific
path constructors and their exact imported-name forms; and path-bearing
Attribute, Subscript, `/`, Boolean/conditional, container, unpacking, walrus,
slice, and comprehension expressions. Receiver, alias-RHS fixpoint, and complete
expression escape scanning all query that same predicate rather than parallel
name-only sets. This is an exact syntactic boundary and does not claim arbitrary
Call return-type inference. These values may appear only within individually
pinned current statements or separately pinned collector, loader, and process calls. The existing builder/validator
path-use statements are individually pinned by stable
AST identity and exact occurrence count. A direct-name assignment target becomes
file-wide path-sensitive as soon as any one of its syntactic RHS expressions is
path-sensitive; this taint is a monotone union and is not cleared by a later,
earlier, conditional, loop, exception, or other-scope scalar rebind. A nominally
read-only `open`,
`Path.open`, `read`, `relative_to`, or other allowed outer call does not exempt
path-sensitive values transported in arguments or nested expressions;
destructuring, container/subscript, walrus, loop/comprehension,
default/decorator, lambda/closure, return, and call-argument transport fail
closed without an unbounded alias graph. Three hundred sixty-one
AST-only negative/positive probes
inspect but never execute injected payloads. The direct callable expression is
subject to the same generic descendant scan as every captured value; only an
exact separately pinned current call node is exempt. Four hundred eighty-eight
named semantic probes cover
parent/baseline/branch/protected/main/allowlist, every newly independent
initialization/profile/route/defect claim class, authority, semantic bindings,
result binding, seventy-two explicit root-guard mutations injected into both frozen
trees, two hundred forty-seven lexical loader negative mutations plus ten positive
exact-chain/post-exec controls, and one hundred six structured authoritative
controls. Those controls replace an authoritative row in place, validate every
individually present named counter even beside a correct slash triplet, and
reject missing, empty, nonnumeric, signed, decimal, multiple-numeric,
comma/slash-ambiguous, or alphanumeric-prefixed/suffixed values as
well as combined-triplet sign/dot/alphanumeric boundary violations and
conflicting or malformed `v`, `v.`, `version`, or `attempt` markers. Dotted
release labels remain excluded while attempt decimal continuation is rejected.
For non-frozen sources, loader certification is restricted to module top level
and uses a closed canonical grammar: the first four module statements must be
exactly one non-aliased `import importlib.util`, exactly one single-name spec
assignment with two literal-string arguments, exactly one single-name module
assignment tied to that live spec, and exactly one live `exec_module` expression.
Duplicates, decoy/alternate chains, or any additional statement before that exec
fail closed; statements after the completed exec are non-retroactive. No function, class,
comprehension, lambda, or other nested lexical scope in a non-frozen tree can
contribute a certified loader exec.

Current final-policy counters: v35; semantic/source-policy/loader-negative/loader-positive/strict-JSON `488/361/247/10/6`.

The current result marker and every authoritative Step 71 control row are
machine-checked against the same v35 version and counters; explicitly rejected
or superseded correction-history prose remains historical rather than current.
Content,
staged, and persistence gates pin the active branch
and upstream plus local/tracking/live equality for active, protected, and main
as applicable. The v2 and v3 candidates, their artifacts, and their PASS
terminals were rejected and superseded after independent review found blocking
P1 defects. The later v4 candidate and its PASS terminals were likewise rejected
after live-binding/capture, root-certification, and loader-dataflow review. The
v5 candidate was then rejected after returned-callable, `ast.Match`, nested
control-flow rebind, and stale-authoritative-row review. The v6 candidate was
rejected after expression-wrapper escape, live loader-object mutation, and
structured authoritative-row review. The v7 candidate was rejected after
direct callable-expression, loader alias/mutator, and individually named
authoritative-counter review. The v8 candidate was rejected after dynamic
namespace source-policy, loader-census, root-guard, and punctuation-general
authoritative-row review. The v9 candidate was rejected after semantic builtin
namespace references with unpacked arguments or aliases, builtins-rooted
`getattr` routes, and trailing-period/underscore authoritative tokens escaped
the then-current checks. The v10 candidate was rejected after annotation/type
contexts, direct `builtins`/`__builtins__` roots, scope-wide loader namespace
markers, separated root namespace/key evidence, and punctuation-prefixed
attempt markers escaped the then-current checks. The v11 candidate was rejected
after match-star/mapping-rest bindings, live sensitive-object mutation targets,
builtins import exposure in loader/root scopes, and malformed named counters
escaped the then-current checks. The v12 candidate was rejected after semantic
sensitive loads in additional expression contexts, type comments, prefix-order
loader danger, separated root-danger/key evidence, and ambiguous authoritative
counter segments escaped the then-current checks. The v13 candidate was rejected
after `eval`/`exec`/`compile` semantic loads and module type-ignore records,
aliased/computed loader danger, embedded watched root-key strings, and combined
triplet/attempt boundaries escaped the then-current checks. The v14 candidate was
rejected after mixed-import `sys` use, dynamic-danger control predicates, and
spaced-sign/punctuation-continuation authoritative tokens escaped the
then-current checks. The v15 candidate was rejected after non-call semantic
`importlib` transport in a mixed-import loader prefix, whole-function dynamic
root danger, and Unicode-minus/separator-digit authoritative-token variants
escaped the then-current checks. The v16 candidate was rejected after exact-shaped
loader calls outside a chain-advancing assignment, computed dynamic root markers,
and fullwidth/plus-minus/arbitrary-punctuation numeric continuations escaped the
then-current checks. The v17 candidate was rejected after module-control-nested
protected definitions, `__globals__`/frame namespace routes, ordinary watched
root-parameter aliases, and non-collector filesystem write/open modes escaped
the then-current checks. The v18 candidate was rejected after filesystem
callables could escape as aliases, containers, returns, or callbacks, starred
and keyword-unpacked `open` calls escaped mode validation, and nonliteral
`getattr` attribute names escaped both source policy and pre-exec loader danger.
The v19 candidate was rejected after semantic `getattr` aliases and
`operator.attrgetter`/`operator.methodcaller` routes escaped source policy and
loader danger, while the present-tense final-policy paragraph retained stale
v18 counts. The v20 candidate was rejected after `_operator` imports, aliases,
and roots plus receiver-independent `attrgetter`/`methodcaller` Attributes
escaped source policy and both loader mirrors. The v21 candidate was rejected
after dotted `operator`/`_operator` imports and importlib submodule/from-import
roots escaped both loader mirrors. The v22 candidate was rejected after trusted
`importlib` spelling could be rebound or shadowed before an exact-shaped chain.
The v23 candidate was rejected after nested function/class scopes inherited
trusted `importlib` from any earlier exact import without replaying intervening
direct, dynamic-namespace, closure, or called-mutator provenance changes. The
v24 candidate was rejected after helper aliases, defaults, decorators,
container-indirect calls, star imports, and class execution contexts could alter
the inherited loader namespace without revoking certification. The v25 candidate
was rejected after property/subscript access, formatted values, comprehension
iteration, overloaded operations, definition-time decorator/default evaluation,
and suspension expressions remained outside its enumerated precompletion danger
classes. The v26 candidate was rejected because a non-frozen function or class
could locally re-import `importlib.util` and satisfy the four-statement body
grammar despite definition-time, enclosing-scope, class-base/metaclass, or module
namespace effects. The v27 candidate was rejected because its per-statement
loader grammar admitted duplicate or decoy chain statements, its filesystem
surface omitted additional `pathlib` mutators, and its import/root policy omitted
several network and child-process families. The v28 candidate was rejected because
path objects could still be transported through destructuring, containers,
subscripts, walrus expressions, iteration, defaults, closures, or other value
contexts and regain an unknown method receiver. The v29 candidate was rejected
because the broad nominally read-only call exemption still admitted path values
transported through nested walrus, lambda/default, generator, and method-argument
expressions. The v30 candidate was rejected because receiver sensitivity recognized
case-folded `path` and `*_path`/`*_file` conventions while its value-use escape
set contained only hard-coded and directly propagated names; convention-named
values could therefore be transported through destructuring, containers, walrus,
iteration, or defaults. The v31 candidate was rejected because the unified Name
set still did not treat a direct `pathlib.Path(...)` or related exact constructor
Call as a path-value expression; constructor results could be transported through
the same non-Name contexts. The v32 candidate was rejected because its file-wide
alias aggregation required every RHS for one spelling to be path-sensitive, so a
scalar rebind in the same or another scope could erase taint while a relocated
pinned path assignment preserved its occurrence count. The v33 candidate was
rejected because its exact-four loader grammar allowed one identifier to occupy
both live roles or a live role to clobber a reserved root, and because Python
3.14 `Path.move_into` remained outside the explicit filesystem-mutator surface.
The v34 candidate was rejected because its reserved-role set still omitted
execution, frame, import-helper, attribute-retrieval, subprocess, and OS root
spellings documented by the policy. Only final v35 evidence may support the
Step 71 commit.

The v5 repair was test-first. With the new probes present but their corresponding
implementation absent, Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-math-isfinite`; after that predicate was repaired,
the direct loader probe failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-cross-function-same-spelling`; and the
source-policy probe failed at
`E_SOURCE_POLICY_NEGATIVE: post-definition-rebind-run-git`. A later nested
loader-root probe independently failed at
`E_SOURCE_POLICY_NEGATIVE: exec-module-nested-getattr-loader-root`. Injected
source was parsed and inspected only and was never executed. Each RED preceded
the corresponding minimum policy/dataflow implementation, after which both
supported runtimes passed content and staged replay with the then-current v5
counters.

The v6 repair was also test-first. After all new official probes were added and
before their implementations changed, Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-match-subject`. Direct named runs independently
failed at `E_SOURCE_POLICY_NEGATIVE: return-run-git-callable`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-if-spec-rebind`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-1`. These payloads and stale rows were held
in memory and inspected only; none was executed or written into frozen source.

The v7 repair was test-first as well. With all new official probes present and
their corresponding implementation absent, Python 3.12 content validation
failed at `E_LOADER_DATAFLOW_NEGATIVE: loader-spec-loader-assign`. Direct named
runs independently failed at
`E_SOURCE_POLICY_NEGATIVE: return-binop-tuple-union-run-git` and
`E_CONTROL_DOCUMENT_NEGATIVE: case-3`; the pre-v7 control parser also returned
no error for the parent authoritative row despite its missing strict-JSON
counter. Final full-range review then exposed that appended stale rows could
pass a negative probe solely through the authoritative-row count. Replacing the
row in place produced a further Python 3.12 RED,
`E_CONTROL_DOCUMENT_NEGATIVE: case-8: []`, for a mixed current/prior-version
marker. The final parser recognizes one- or two-digit attempt versions while
excluding `v1024` release labels and requires the only recognized attempt
version to be v7. All injected source remained AST-only and was never executed.

The v8 repair was test-first. With only the official probes added, Python 3.12
content validation failed at `E_LOADER_DATAFLOW_NEGATIVE: loader-alias-spec`;
direct runs independently failed at
`E_SOURCE_POLICY_NEGATIVE: direct-call-binop-tuple-run-git` and
`E_CONTROL_DOCUMENT_NEGATIVE: case-9`. The latter demonstrated that a correct
slash triplet could mask one stale named counter. The final implementation uses
generic callable-expression traversal, conservative pre-exec live-name use
invalidation, per-token named-counter validation, and attempt-marker parsing
that recognizes `v8`, `v.8`, `version 8`, and `attempt 8` while ignoring release
labels such as `v1024`. Injected payloads were parsed only and never executed.

The v9 repair was test-first. With only the official probes added, Python 3.12
content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-locals-subscript`. Direct named runs independently
failed at
`E_SOURCE_POLICY_NEGATIVE: dynamic-namespace-globals-subscript-direct-call`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-globals-spec-mutation`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-14`. The v9 implementation bans dynamic
namespace calls in validator/builder policy, invalidates any pre-completion
loader candidate encountering those calls, treats a watched string key tied to
such a namespace lookup as explicit root-parameter validation use, and parses
arbitrary non-digit counter/version punctuation while ignoring release token
`v1024`. Injected payloads were parsed only and never executed.

The v10 repair was test-first. With only the new official probes present,
Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-globals-unpacked-positional`. Focused official
corpora independently failed at
`E_SOURCE_POLICY_NEGATIVE: dynamic-namespace-globals-unpacked-positional`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-globals-unpacked-spec-mutation`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-23`. The implementation now identifies
semantic namespace references independently of syntactic call arity, propagates
conservative aliases for root validation, treats builtins-rooted namespace
access as load-bearing, accepts normal trailing punctuation after an attempt
number while excluding dotted release labels and `v1024`, and recognizes named
counter labels across underscore and arbitrary punctuation forms. Injected
payloads were parsed only and never executed.

The v11 repair was test-first. With only the new official probes present,
Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-namespace-helper-body-separated-key`. Focused
official corpora independently failed at
`E_SOURCE_POLICY_NEGATIVE: annotation-posonly-protected`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-namespace-helper-before-candidate`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-27`. The implementation now applies generic
sensitive-reference inspection to every requested annotation/type context,
bans the complete dynamic/builtins semantic-root family, prechecks the entire
loader lexical scope, links any subtree namespace marker to watched string keys
in root validation controls, and recognizes attempt markers preceded by dot,
underscore, or other non-alphanumeric punctuation. Injected payloads were
parsed only and never executed.

The v12 repair was test-first. With only the new official probes present,
Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-import-builtins-alias-separated-key`. Focused
official corpora independently failed at
`E_SOURCE_POLICY_NEGATIVE: match-star-protected-binding`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-import-builtins-alias-scopewide`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-31`. The implementation now covers all
match capture nodes, live sensitive-identity Store/Del and mutator targets,
scope-wide builtins import and `__import__` markers in both loader and root
mirrors, and malformed individually named authoritative counters. Injected
payloads were parsed only and never executed.

The v13 repair was test-first. With only the new official probes present,
Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-eval-danger-separated-key`. Focused official
corpora independently failed at
`E_SOURCE_POLICY_NEGATIVE: sensitive-load-for-iterator`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-eval-before-spec`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-38`. The implementation now rejects
sensitive semantic loads across all non-exempt expression contexts and all
type-comment surfaces, applies ordered prefix-sensitive loader danger tracking,
links the expanded danger family to watched root-validation keys, and parses
each authoritative named-counter segment as exactly one unsigned integer token.
Injected payloads were parsed or inspected as text only and were never executed.

The v14 repair was test-first. With only the new official probes present,
Python 3.12 content validation failed at
`E_ROOT_GUARD_NEGATIVE: tol-eval-attribute-content-key`. Focused official
corpora independently failed at
`E_SOURCE_POLICY_NEGATIVE: sensitive-load-alias-eval`,
`E_LOADER_DATAFLOW_NEGATIVE: loader-import-sys-alias-before-spec`, and
`E_CONTROL_DOCUMENT_NEGATIVE: case-45`; the mixed valid/decimal attempt
variant separately failed at `case-52`. Final exact-five reconciliation added
the unaliased-import case and reproduced
`E_LOADER_DATAFLOW_NEGATIVE: loader-import-sys-before-spec`. The implementation now protects
`eval`/`exec`/`compile` loads and rejects module type-ignore records, applies
alias- and computed-form loader danger while preserving exact `importlib.util`
chains, folds static string additions for root watched-token evidence, and
enforces combined-triplet and attempt token boundaries. Injected payloads were
parsed or inspected as text only and were never executed.

The v15 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_ROOT_GUARD_NEGATIVE: tol-eval-format-control-predicate: builder=False, independent=[]`.
The final implementation marks both `tol` and `max_iter` potentially validated
when dynamic execution or introspection occurs inside a control predicate,
pins the exact frozen mixed import by stable AST hash while forbidding every
pre-exec semantic `sys` use and wildcard sensitive-module import, and rejects
spaced signs plus punctuation-digit continuations around authoritative triplet
and attempt tokens. Injected loader/root payloads remained AST-only and
authoritative rows remained in-memory text fixtures; none was executed.

The v16 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_ROOT_GUARD_NEGATIVE: dynamic-eval-nested-helper-outside-control: builder=False, independent=[]`.
The v16 loader census constructed per-statement allowed semantic-Load node sets:
`importlib` is allowed only inside the exact two-argument
`importlib.util.spec_from_file_location` or exact one-argument
`importlib.util.module_from_spec` call target, while every other pre-exec
`importlib` or `sys` Load invalidates the candidate. No frozen loader contains a
pre-exec `sys.modules[...] = module` registration, so no `sys` semantic-Load
exception is present. The root predicate now treats any dynamic
execution/introspection marker anywhere in the complete root-function subtree,
including nested helper definitions, as potential explicit validation of both
`tol` and `max_iter`. Authoritative attempt/triplet parsing rejects ASCII or
Unicode-minus signs before a token and every optional-space separator-digit
continuation from `/,:;._+-` or Unicode minus after it. Injected loader/root
payloads remained AST-only and authoritative rows remained in-memory text
fixtures; none was executed.

The v17 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_ROOT_GUARD_NEGATIVE: dynamic-getattr-nested-helper-outside-control: builder=False, independent=[]`.
The final loader proof creates an `importlib` Load exemption only while the
current statement is the direct single-Name-target exact spec assignment that
starts a live candidate or the exact module assignment that advances that
candidate. Exact-shaped calls in consumers, containers, attribute targets, and
multiple assignments are danger before completion; post-exec uses do not erase
an already certified chain. The root predicate treats dynamic callable names
and dunder/frame/module/import attributes as danger anywhere in the complete
function subtree without attempting to fold the selected attribute string.
Authoritative-number parsing recognizes plus/minus sign characters through
Unicode normalization/name data and scans beyond arbitrary punctuation for any
additional digit before alphabetic text or a row boundary. Injected loader/root
payloads remained AST-only and authoritative rows remained in-memory text
fixtures; none was executed.

The v18 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_ROOT_GUARD_NEGATIVE: ordinary-tol-assignment-alias: builder=False, independent=[]`.
Focused AST-only checks showed empty error lists for a module-level `if`-nested
`run_git` definition, `helper.__globals__['run_git'](...)`, and `path.touch()`;
the loader corpus separately failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-dunder-globals-importlib-before-spec`, with
both builder and independent mirrors incorrectly certifying line 5. The final
policy identifies protected definitions by direct `Module.body` node identity,
closes namespace/frame reference and mutation routes, admits only the two exact
operational root-parameter Load shapes, and enforces read-only literal/default
open modes plus non-collector write-method rejection. Injected source and frozen
root/loader mutations were parsed as AST only and were never executed.

The v19 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-dynamic-getattr-general-receiver-before-spec`,
with builder and independent mirrors both incorrectly certifying line 6.
Focused AST-only checks also returned empty error lists for built-in `open`
aliasing, `path.open` aliasing, starred direct `open`, and a variable-name
`getattr(path, attribute_name)`. The final source policy classifies built-in
`open` and filesystem callable attributes as sensitive semantic Loads, allowing
them only at independently validated exact collector calls, exact safe
non-filesystem replacement calls, or direct read-only `open`/`Path.open` calls.
Starred positional and keyword-unpacked open calls fail closed. Every direct
`getattr` call requires an exact constant-string attribute name, while both
loader mirrors treat any pre-exec nonconstant-name `getattr` as danger; a
post-exec occurrence does not invalidate an already completed exact chain.
Injected source remained AST-only and was never executed.

The v20 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-getattr-alias-before-spec`, with builder and
independent mirrors both incorrectly certifying line 5. Focused AST-only checks
returned empty error lists for `ga = getattr`, `consume(getattr)`, `import
operator`, and `operator.attrgetter('write')(stream)`; the control mutation
probe independently failed because no current final-policy marker existed. The
v20 policy allows the semantic `getattr` Name only as the direct function of
an exact literal-attribute call that still passes the existing sensitive
receiver/attribute checks. All other `getattr` transport and every `operator`,
`attrgetter`, or `methodcaller` import/reference fail closed. Both loader mirrors
treat those roots as pre-exec danger, while completed-chain post-exec controls
remain accepted. Injected source was parsed as AST only and never executed.

The v21 repair was test-first. With only the new official probes present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-underscore-operator-import-before-spec`,
with builder and independent mirrors both incorrectly certifying line 5.
Focused AST-only checks then established the intended corpus boundary: 282
source-policy probes and 130 loader probes. The implementation treats
`operator` and `_operator` identically for imports, from-imports, aliases, and
semantic roots, and treats `attrgetter` and `methodcaller` Attributes as danger
regardless of receiver. Completed-chain post-exec controls and all five frozen
exact loader chains remain accepted. Injected source was parsed as AST only and
never executed.

The v22 repair was test-first. With only the new AST-only fixtures present and
before the import predicates changed, Python 3.12 content validation failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-dotted-operator-attrgetter-import-before-spec`,
with builder and independent mirrors both incorrectly certifying line 5. The
implementation now classifies sensitive imports by module root, preserving only
the exact non-aliased `importlib.util` route and the pinned frozen mixed-import
shape required by the five real chains. Dotted `operator`/`_operator`, other
importlib submodules, and importlib from-import roots fail closed before chain
completion; seven post-completion/exact positives remain accepted. The final
loader corpus is 131 negative plus seven positive cases. Synthetic sources were
parsed as AST/text only and never executed.

The v23 repair was test-first. Python 3.12 first failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-importlib-assignment-rebind`, with both
mirrors incorrectly certifying line 5. The symmetric repair tracks trusted
`importlib` provenance from the exact permitted import and rejects assignment,
walrus, alias/from/relative import, parameter, loop, and destructuring bindings
before completion. The final loader corpus is 139 negative plus seven positive
cases; synthetic sources were parsed only and never executed.

The v24 repair was test-first. With the twelve new AST/text-only fixtures
present and before the provenance implementation changed, Python 3.12 content
validation failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-nested-after-module-assignment-rebind`,
with builder and independent mirrors both incorrectly certifying line 6. The
symmetric repair replaces the earlier-line shortcut with ordered parent-scope
statement replay. Direct assignment/import/loop/with/except targets, dynamic
namespace mutation, `global`/`nonlocal` mutation, calls to statically identified
sibling mutators, ancestor closure shadowing, and later parent-scope provenance
revocation now prevent nested function/class inheritance. Scope placement or
execution timing that cannot be proved is rejected conservatively. The final
loader corpus is 151 negative plus seven positive cases; all five frozen exact
chains and the completed-chain post-exec controls remain accepted. Synthetic
sources were parsed as AST/text only and never executed.

The v25 repair was test-first. Before implementation, Python 3.12 content
validation failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-called-mutator-helper-alias`, with both
mirrors incorrectly certifying line 10. A direct AST census located exactly five
frozen loader chains: four module-scope chains and one `load` function in
`test_gates_v1024.py`. The latter's executed ancestor prefix contains six exact
call-bearing statement shapes, while the two result scripts share the exact
`matplotlib.use('Agg')` prefix shape. Rather than claim general Python effect or
call-graph analysis, v25 pins the five complete frozen tree identities and uses
a minimal grammar for every non-frozen candidate: only the live exact
spec→module→exec calls may execute before completion; other calls, star imports,
class execution, and uncertain control constructs fail closed. Non-module
candidate scopes are not certified unless they belong to one of the five exact
frozen trees. Completed-chain post-exec controls remain non-retroactive. The
final loader corpus is 164 negative plus seven positive cases. All synthetic
sources were parsed as AST/text only and never executed.

The v26 repair was test-first. With the nine new AST/text-only fixtures present
and before the loader predicates changed, Python 3.12 content validation failed
at `E_LOADER_DATAFLOW_NEGATIVE: loader-property-read-before-chain`, with both
mirrors incorrectly certifying line 5. The repair removes effect-category
enumeration from the non-frozen fallback. Its precompletion body grammar is now
closed to exactly four statement shapes: the exact non-aliased
`import importlib.util`, the exact single-name spec assignment with two literal
string arguments, the exact single-name module assignment from the live spec,
and the exact live `spec.loader.exec_module(module)` expression. All other
statements and expressions fail closed, covering property and subscript reads,
formatted values, comprehension iteration, overloaded binary operations, bare
decorators, evaluated defaults, `yield`, and `await` without an open-ended effect
census. The five frozen source trees remain identified by path/census input and
full stable AST hash and then must still yield their expected loader lines. The
seven positives now contain only the canonical chain before completion; their
independent statements and deliberately dangerous controls occur after the
recorded exec and remain non-retroactive. The final loader corpus is 173 negative
plus seven positive cases. Synthetic sources were parsed as AST/text only and
never executed.

The v27 repair was test-first. With the nine new AST/text-only fixtures present
and before the scope restriction changed, Python 3.12 content validation failed
at `E_LOADER_DATAFLOW_NEGATIVE: loader-nested-function-canonical-chain`, with
both mirrors incorrectly certifying line 5. Non-frozen certification is now
restricted to the module body; every function, async function, class, lambda,
comprehension, and other nested lexical scope is excluded before loader state is
created, so a local exact re-import cannot restore trust. The sole real nested
`load` function remains eligible only when its complete frozen source tree has
one of the five pinned stable AST identities, after which the normal exact
path/line census still applies. The new corpus covers plain nested function and
class-method chains, default and decorator effects, enclosing unknown calls,
class base/metaclass calls, and module `sys.modules['importlib.util']` mutation.
All seven positives remain module-level canonical chains with any extra controls
after the recorded exec. The final loader corpus is 182 negative plus seven
positive cases. Synthetic sources were parsed as AST/text only and never
executed.

The v28 repair was test-first. With the new AST/text-only fixtures present and
before the corresponding predicates changed, Python 3.12 content validation
failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-duplicate-canonical-import-before-spec`,
with builder and independent mirrors both incorrectly certifying line 5. The
non-frozen proof now accepts only the exact ordered four-statement module prefix;
duplicate imports, extra specs/modules, and alternate precompletion chains fail.
The source-policy corpus pins each audited file's complete import signature,
rejects the requested network/child-process module families and direct roots,
and restricts path-sensitive receivers and proven aliases to the audited
read-only `pathlib` surface plus the five exact collector mutations. The final
corpora contain 304 source-policy probes and 187 loader-negative plus seven
loader-positive probes. Synthetic sources were parsed as AST/text only and never
executed.

The v29 repair was test-first. With the fifteen new AST/text-only fixtures present
and before the corresponding policy changed, Python 3.12 content validation
failed at
`E_SOURCE_POLICY_NEGATIVE: filesystem-path-destructuring-alias: []`. The final
policy rejects any non-exempt semantic Load of a path-object root or proven direct
alias. Direct enumerated read-only receivers and separately pinned collector,
loader, or process calls remain accepted; every pre-existing audited path-use
statement is additionally fixed by stable-AST identity and exact occurrence
count, so duplicating a pinned transport statement fails the context contract.
The same transport rule applies to the audited lowercase `path` variable, whose
legitimate statement shapes are pinned rather than broadly exempted. The corpus
covers tuple/list/dict transport, subscripts, walrus, loop and
comprehension capture, function defaults, decorator arguments, lambda/closure
return, ordinary return, call arguments, and attribute chains. The final
source-policy corpus contains 319 cases. Synthetic sources were parsed as AST/text
only and never executed.

The v30 repair was test-first. With the eight new AST/text-only fixtures present
and before the broad read-only descendant exemption was removed, Python 3.12
content validation failed at
`E_SOURCE_POLICY_NEGATIVE: filesystem-read-call-walrus-result-transport: []`.
The final policy grants no general path-sensitive descendant exemption to an
unpinned nominally read-only call. Every legitimate current statement containing
a path-sensitive value is accepted only by stable AST identity and exact
occurrence count, with the five collector mutations and already pinned
loader/process calls remaining separate exact exceptions. The new cases cover
uppercase and lowercase walrus transport, lambda/default capture, generator
transport, nested containers, and `relative_to` method arguments. The final
source-policy corpus contains 327 cases. Synthetic sources were parsed as
AST/text only and never executed.

The v31 repair was test-first. With ten new AST/text-only fixtures present and
before the divergent receiver/escape name sets were unified, Python 3.12 content
validation failed at
`E_SOURCE_POLICY_NEGATIVE: filesystem-uppercase-path-destructuring: []`. The
repair now case-folds and pre-registers `path`, `filepath`, `*_path`, and `*_file`
Names from the complete AST in the same canonical set used by receiver checks,
direct-alias fixpoint propagation, pinned-load admission, and the final value-use
Visitor. The fixtures cover `PATH`, `RESULT_PATH`, `source_file`, `output_path`,
`Path`, `filepath`, `file_path`, and mixed-case forms across destructuring,
containers, walrus, loops, and defaults. The newly recognized legitimate frozen
builder `RESULT_PATH` statements are admitted only by stable AST identity and
exact occurrence count. The final source-policy corpus contains 337 cases.
Synthetic sources were parsed as AST/text only and never executed.

The v32 repair was test-first. With sixteen new AST/text-only fixtures present
and before recursive path-value expression scanning was implemented, Python 3.12
content validation failed at
`E_SOURCE_POLICY_NEGATIVE: filesystem-pathlib-path-container: []`. The shared
predicate now recognizes exact `pathlib.Path`, `PurePath`, `PurePosixPath`,
`PureWindowsPath`, `PosixPath`, and `WindowsPath` constructors, exact imported
constructor names, directly proven constructor aliases, and the specified derived
expression wrappers. The same predicate supplies receiver classification,
alias-RHS fixpoint propagation, and whole-tree expression escape rejection.
Direct literal `pathlib.Path(...).open()` in an admitted read-only mode retains a
narrow syntactic positive; no general read-only descendant or arbitrary-call
return exemption was introduced. The final source-policy corpus contains 353
cases. Synthetic sources were parsed as AST/text only and never executed.

The v33 repair was test-first. With seven new AST/text-only full-source mutation
fixtures present and before alias taint became monotone, Python 3.12 content
validation failed at
`E_SOURCE_POLICY_NEGATIVE: filesystem-sticky-alias-sensitive-before-scalar-rebind: []`.
The fixtures preserve the exact stable-AST occurrence count of the pinned
`original = CANONICAL_LEDGER` statement while placing scalar and sensitive
rebindings before, after, inside `if`, loop, and `try` bodies, or in another
function. The repair changes the direct-name alias fixpoint from an all-RHS
requirement to a monotone any-RHS union: once an identifier has one syntactically
path-sensitive RHS anywhere in the audited file, unrelated scalar rebindings do
not erase that policy taint. Legitimate same-name reuse remains admitted only by
the existing exact stable-AST/count pins. The final source-policy corpus contains
360 cases. Synthetic sources were parsed as AST/text only and never executed.

The v34 repair was test-first. With the new AST/text-only fixtures present and
before the role and filesystem predicates changed, Python 3.12 content validation
failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-role-collision-same-target`, with builder and
independent mirrors both incorrectly certifying line 4. A focused source-policy
call separately returned `[]` for `args.output_dir.move_into('x')`. The repair
requires distinct non-reserved spec/module target identities and preserves the
exact live-role consumption contract through `module_from_spec` and
`exec_module`. It also classifies `move_into` as a filesystem callable and direct
mutator alongside the existing `move`, `copy`, and `copy_into` controls. The
final loader corpus contains 195 negative and eight positive cases; the final
source-policy corpus contains 361 cases. Synthetic sources were parsed or
inspected as AST/text only and never executed.

The v35 repair was test-first. With the parameterized reserved-role fixtures
present and before the shared comprehensive sets were installed, Python 3.12
content validation failed at
`E_LOADER_DATAFLOW_NEGATIVE: loader-reserved-role-eval-spec-target`, with builder
and independent mirrors both incorrectly certifying line 4. The final corpus
tests all 26 exact sensitive execution/frame/import/root spellings in both spec
and module roles, plus case-sensitive and adjacent-dunder positive controls. It
contains 247 loader-negative and ten loader-positive cases. Synthetic sources
were parsed as AST/text only and never executed.

Stable precommit identities are:

- builder SHA-256:
  `a1089b973644fef9064a113a40ec3af6da4ed32ba5794b4f574d359bc201856d`;
- validator SHA-256:
  `a5986401463b2c7fbe0bbe4ed794ac77880fc1d7a018bca5502954ee190d531a`;
- matrix LF-byte SHA-256:
  `571a4b781d292201f07868045d98cbe5f4c2a71a9ca568f66d8bcb6b509d86d9`;
- matrix semantic SHA-256:
  `ebb2e69becaeb70682f876751592e0c14ad9a412ac39c136a3dc113fe9c60dd6`.

The attestation byte identity is intentionally not embedded here because it
binds this result's LF-byte hash. It is collected after this final human result
under the JSON-last rule and independently checked by the validator.

## 10. Exact Commit Contract

The Step 71 commit may contain exactly these eight paths:

1. `Codex/work/v1024_phase065/build_phase065_step71.py`
2. `Codex/work/v1024_phase065/validate_phase065_step71.py`
3. `Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json`
4. `Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json`
5. `Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected subject: `audit(phase065): trace v1024 code profile defaults`.

No `Claude/**` path may change. Protected/main pins must remain fixed. A
precommit PASS does not release Step 72; only dual-runtime live-remote
persistence does.
