# Phase 062 Step 54 - v1.0.21 LCO/Si literature, unit, and scope audit

## Outcome

Status: **PASS_WITH_CONCERNS**
Gate: `PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS`

Step 54 closes the audit inventory and routing scope; it does **not** accept the frozen LCO/Si science as canonical. The frozen release remains untouched. External scientific truth validated: **false**. External material and experimental truth validated: **false**.

## Full-read and inventory coverage

- Direct READ_FULL attestations: **21** files, each pinned by commit, Git blob, byte SHA-256, and 1-EOF line coverage.
- Frozen material bibliography: **28/28** rows (**14 LCO + 14 Si**).
- DOI/resolver metadata: **27** matched records and **1 conflicting identifier**.
- Relevant cite-key occurrences in the release: **72** (**54 LCO + 18 Si**).
- Lexical cited/numeric source-line inventory: **504** rows. This inventory is not proposition proof; load-bearing use requires a curated scope row.
- Atomic source-claim manifest and scope matrix: **482 / 482** rows, exact 1:1 claim-to-scope bijection. Adopted release text contributes **439** claim atoms; bibliography **28** and reference-ledger self-report **15** remain separate authority classes.
- All **1363** physical lines across the eight LCO sections, AppA and AppD were classified exactly once. Pure formatting, environment boundaries, comments and blanks are excluded; scientific TikZ node/draw/axis commands are retained as load-bearing claims.
- Adopted-text claim atoms by path: sec11 **66**, sec12 **32**, sec13 **45**, sec14 **29**, sec15 **109**, sec16 **17**, sec17 **38**, sec18 **38**, AppA **28**, AppD **37**.
- Explicit frozen-release GNF records: **17**; lexical cite/numeric inventory remains navigation only.
- V1021 reference-ledger self-report inventory: **4** exact statements, independently classified from adopted release text.
- Q6/Q7 strict snapshot traversal: Q6 **1172** nodes, Q7 **1193** nodes.

## Decisive LCO findings

1. The publisher abstract for Swiderska distinguishes **+0.83 mV/K** as an inferred absolute LCO single-electrode coefficient from the isothermal **Li|LCO cell coefficient -0.25 mV/K**. The frozen text calls +0.83 a vs-Li half-cell quantity and derives about +80 J/(mol K); that basis/sign transfer is rejected. The corresponding narrow isothermal cell conversion is `F*(-0.25e-3) = -24.12125 J/(mol K)`, subject to Phase 74 reaction-direction adjudication.
2. Q6's slot arithmetic is internally reproducible: `Delta S_e=-45.678261885 J/(mol K)`, `Delta S_eff=-39.678261885 J/(mol K)`, and `-0.411237621 mV/K`. The **1.1 k_B/atom model gate integral/complete-metal electronic entropy** is a different quantity from the **0.18 k_B/atom O3 total partial-molar quantity**; their unit, basis, meaning, and evidence gaps are separate rows.
3. The `x_bar=0.50` row is not gate-off. `x_bar` is the global delithiation fraction, while the electronic term is evaluated at the T1 transition's fixed `x_center=0.85`. Independent same-formula recomputation gives gate ON/OFF at x_bar=0.50: `U=3.924249955/4.042610795 V`, slope `-0.312434776/-0.034630812 mV/K`.
4. The reported -91 mV ON/OFF shift holds the electronic-absorbed T1 enthalpy fixed. Reanchoring the gate-off T1 to 3.930 V at Tref changes the x_bar=0.85 voltage by only `-0.000122016 mV`; the same-dH shift is not an isolated physical gate effect.
5. Tier-C one-point arithmetic is separated from missing multi-temperature reconstruction, irreversible heat, doped/high-voltage LCO, oxygen redox/loss, structural-transition validation, and experiment. Production output is not scientific authority.

## Decisive Si findings

1. The frozen Limthongkul DOI `10.1016/S1359-6454(02)00515-4` does not identify the cited paper. The matching record is **10.1016/S1359-6454(02)00514-1**, Acta Materialia 51(4), 1103-1113. The frozen row is preserved as evidence and routed to Phase 71 for correction.
2. Q6 to Q7 Ch1 labels are **247 -> 254**, or **+7**. The change log and execution ledger say +6 and 1:1 PASS; that structural claim is conflicting.
3. General charge accounting survives, but exact logistic-weighted inversion and uniqueness are conditional on noninteracting site classes. Verbrugge 2016 equations 2-7 explicitly state this assumption; the bridgehead's electrode-neutral promotion is rejected.
4. The approximately 55 mV value at `Omega=4RT` is not a global regular-solution upper bound over Omega. It is only the fixed-Omega branch bound (and gamma<=1 branch scaling).
5. The blanket “mechanical contribution is dominant” wording is stronger than the narrow sources, and Eyring-tail universality has no Si-specific source or derivation.
6. No Si-specific governing equation in v1.0.21: **No Si-specific governing equation** was added (`equation-block delta = 0`). Free energy, stress chemical potential, plasticity/damage, interface/SEI, hysteresis, SiOx, Si-C, and blend allocation remain missing and routed.

## Findings and authority ceiling

- P0/P1/P2: **0/8/8**.
- `PASS_WITH_CONCERNS` means the inventory, internal arithmetic checks, contradictions, and owner routing are complete enough for downstream repair. It is not a scientific/material PASS.
- Required actual-mutation negative controls: **28/28 contract cases**, including a missing source claim and a duplicate/multi-mapped source claim. The precommit validator must execute every case and report singleton rejection; no stored `ENFORCED` string is accepted as evidence.
- Validator-only staged/index and CRLF identity boundary controls: **2/2**. They do not mutate the real Git index or repository files.
- Primary owners are Phase 71/74/75/76/78/79/80/82 as recorded in the matrix. Phase 82 owns final equation and validity-domain freezing.

## Validation and recovery record

- Builder SHA-256: `57162f0431b593be004b0dcf50caf1eafa2d65d6b5d42d9355e4d1ebc9007427`
- Artifact semantic SHA-256: `6002a757e953a0aa4bf7124acb10ba1f97bbcb1d00773b0c9ae1643551b629ec`
- Expected parent: `9dee2f4d6bdde48f248227cdede08d0d307cc8bc`
- Q6/Q7 commits: `bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17` / `9ea5cb23754061261923bab013e279d7f6938723`
- External observation date: `2026-08-27`
- Result-first sentinel: `P062_STEP54_RESULT_FIRST_PRECOMMIT`
- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN` (persistence is not claimed)

This result was generated before the machine matrix under the result-first precommit contract. Both execution ledgers and the active handover complete the Step 54 recovery set. Commit/push and persistence verification are separate gate actions; Step 55 remains blocked until `PASS_P062_STEP54_PERSISTENCE`.
