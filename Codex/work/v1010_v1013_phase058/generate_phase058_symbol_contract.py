#!/usr/bin/env python3
"""Generate a source-linked core symbol contract/collision audit for Phase 058."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Codex" / "results" / "PHASE_058_THEORY_SYMBOL_CONTRACT_AUDIT.json"
PATHS = [
    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex",
    "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
]


CONTRACTS = [
    {
        "id": "SYM-001",
        "symbol": "V_app",
        "pattern": r"V_\\app|V_\{\\mathrm\{app\}\}",
        "intended_quantity": "externally applied/measured terminal voltage",
        "unit": "V",
        "status": "PRESERVE_WITH_OBSERVATION_CONTRACT",
        "collision": "Must not be identified with internal electrode potential or equilibrium OCP.",
    },
    {
        "id": "SYM-002",
        "symbol": "V_n",
        "pattern": r"V_\\?n",
        "intended_quantity": "internally corrected voltage after the model's polarization subtraction",
        "unit": "V",
        "status": "CORRECT_MODEL_SCOPE",
        "collision": "A single lumped Rn correction is not a complete porous-electrode potential decomposition.",
    },
    {
        "id": "SYM-003",
        "symbol": "U_j",
        "pattern": r"U_j|U_1|U_\\oc|U_\\eq",
        "intended_quantity": "equilibrium reaction/transition potential or OCP",
        "unit": "V",
        "status": "CORRECT_AND_SPLIT",
        "collision": "Used as standard center, composition-dependent OCP, branch center, and a V-dependent fixed-point quantity.",
    },
    {
        "id": "SYM-004",
        "symbol": "U_j^(d)",
        "pattern": r"U_j\^\{\\,d|U_j\^\{\(d\)|U_j\^\{d",
        "intended_quantity": "phenomenological direction/branch-shifted transition center",
        "unit": "V",
        "status": "EMPIRICAL_ONLY",
        "collision": "Must not be described as direction-dependent thermodynamic equilibrium without metastable-state specification.",
    },
    {
        "id": "SYM-005",
        "symbol": "q",
        "pattern": r"\\bq\\b|\\dd q|q=",
        "intended_quantity": "normalized accumulated charge/protocol coordinate",
        "unit": "dimensionless when Q/Q_cell",
        "status": "PRESERVE_WITH_EXPLICIT_ORIENTATION",
        "collision": "Orientation and relation to material stoichiometry are not globally fixed in early sources.",
    },
    {
        "id": "SYM-006",
        "symbol": "Q_cell",
        "pattern": r"Q_\\cell|Q_\\{\\mathrm\\{cell\\}\\}",
        "intended_quantity": "cell/reference capacity used for normalization",
        "unit": "v1.0.10–12 state C; v1.0.13 allows C or Ah",
        "status": "BLOCKER_UNIT_CONTRACT",
        "collision": "The same variable is multiplied by c_rate[h^-1] to obtain current and divides I in a time derivative; C versus Ah changes the result by 3600.",
    },
    {
        "id": "SYM-007",
        "symbol": "Q_j",
        "pattern": r"Q_j|Q_\\{j",
        "intended_quantity": "charge/capacity assigned to transition j",
        "unit": "same charge unit as dQ/dV integral",
        "status": "PRESERVE_WITH_CAPACITY_BASIS",
        "collision": "For blends and electrodes, mass/cell/component capacity bases must be distinguished.",
    },
    {
        "id": "SYM-008",
        "symbol": "|I| / I_abs",
        "pattern": r"\|I\||I_\\mathrm\{abs\}|I_\{\\mathrm\{abs\}\}",
        "intended_quantity": "absolute applied current magnitude",
        "unit": "A",
        "status": "BLOCKED_BY_Q_CELL_UNITS",
        "collision": "Correct when independently supplied in A; ambiguous when derived from c_rate times Q_cell.",
    },
    {
        "id": "SYM-009",
        "symbol": "c_rate",
        "pattern": r"c\\_rate|c_rate",
        "intended_quantity": "C-rate",
        "unit": "h^-1",
        "status": "CORRECT_INPUT_CONVERSION",
        "collision": "Requires an Ah capacity basis or explicit conversion from coulombs.",
    },
    {
        "id": "SYM-010",
        "symbol": "theta",
        "pattern": r"\\theta",
        "intended_quantity": "Li-site occupancy/lithiation fraction",
        "unit": "dimensionless",
        "status": "PRESERVE_V1013_DEFINITION",
        "collision": "Earlier derivations intermittently identify its complement with the same logistic without a stable reaction orientation.",
    },
    {
        "id": "SYM-011",
        "symbol": "xi_j",
        "pattern": r"\\xi",
        "intended_quantity": "v1.0.13: delithiation progress, xi=1-theta",
        "unit": "dimensionless",
        "status": "CORRECT_AND_ELECTRODE_MAP",
        "collision": "v1.0.10–12 use direction-dependent progress; peak magnitude hides complement/sign errors.",
    },
    {
        "id": "SYM-012",
        "symbol": "sigma_d",
        "pattern": r"\\sigma_d|\\sigma_\\{d\\}",
        "intended_quantity": "protocol/delithiation direction sign",
        "unit": "dimensionless ±1",
        "status": "REMOVE_FROM_EQUILIBRIUM_STATE",
        "collision": "Acts in equilibrium logistic, hysteresis, polarization, and causal direction; a path sign cannot define equilibrium occupancy.",
    },
    {
        "id": "SYM-013",
        "symbol": "s",
        "pattern": r"\\bs\\b|s\\{=\\}|s=",
        "intended_quantity": "fixed derivation/reaction-orientation sign in v1.0.13 Ch2",
        "unit": "dimensionless",
        "status": "PRESERVE_IF_REACTION_DEFINED",
        "collision": "Introduced to repair sigma_d contamination but coexists with facade direction conventions.",
    },
    {
        "id": "SYM-014",
        "symbol": "w_j",
        "pattern": r"w_j|w_\\{j\\}|\\bw\\b",
        "intended_quantity": "voltage-domain transition width",
        "unit": "V",
        "status": "SPLIT_IDEAL_AND_EMPIRICAL_WIDTHS",
        "collision": "Ideal single-site thermal width and empirical two-phase/ensemble width share one symbol and often one forced T law.",
    },
    {
        "id": "SYM-015",
        "symbol": "n_j",
        "pattern": r"n_j|n_\\{j\\}",
        "intended_quantity": "dimensionless width multiplier/effective degeneracy parameter",
        "unit": "dimensionless",
        "status": "UNVERIFIED_PARAMETER_MEANING",
        "collision": "Multiplicity, stoichiometric electron number, and empirical width multiplier are not derived as one quantity.",
    },
    {
        "id": "SYM-016",
        "symbol": "Omega_j",
        "pattern": r"\\Omega",
        "intended_quantity": "regular-solution interaction energy",
        "unit": "J mol^-1",
        "status": "CORRECT_FREE_ENERGY_ROLE; REJECT_ROLE_OVERLOAD",
        "collision": "Also drives hysteresis gap, activation-barrier reduction and dopant smear without one consistent free-energy/kinetic derivation.",
    },
    {
        "id": "SYM-017",
        "symbol": "gamma_j",
        "pattern": r"\\gamma",
        "intended_quantity": "phenomenological fraction of a computed gap",
        "unit": "dimensionless",
        "status": "EMPIRICAL_ONLY",
        "collision": "Not derived from the regular-solution spinodal calculation.",
    },
    {
        "id": "SYM-018",
        "symbol": "h_eta,j",
        "pattern": r"h_\\eta|h_\\{\\eta",
        "intended_quantity": "partial-cycle/path branch scaling",
        "unit": "dimensionless",
        "status": "EMPIRICAL_ONLY",
        "collision": "History dependence is reduced to one static scalar rather than an internal-state evolution.",
    },
    {
        "id": "SYM-019",
        "symbol": "Delta H_rxn",
        "pattern": r"\\Delta H_\\rxn|\\Delta H_\\{\\mathrm\\{rxn\\}",
        "intended_quantity": "molar reaction enthalpy under an insertion reaction convention",
        "unit": "J mol^-1",
        "status": "PRESERVE_WITH_REFERENCE_REACTION",
        "collision": "Differential reaction enthalpy is compared in places with cumulative formation enthalpy.",
    },
    {
        "id": "SYM-020",
        "symbol": "Delta S_rxn",
        "pattern": r"\\Delta S_\\rxn|\\Delta S_\\{\\mathrm\\{rxn\\}",
        "intended_quantity": "molar reaction entropy under the same reference reaction",
        "unit": "J mol^-1 K^-1",
        "status": "SPLIT_STANDARD_CENTER_FROM_COMPOSITION_FUNCTION",
        "collision": "Used as a center constant, full partial-molar function, and a container for config/vib/electronic terms.",
    },
    {
        "id": "SYM-021",
        "symbol": "Delta H_a / Delta S_a",
        "pattern": r"\\Delta [HS]_a|\\Delta [HS]_\\{a",
        "intended_quantity": "activation enthalpy/entropy for a specified elementary or effective kinetic process",
        "unit": "J mol^-1 / J mol^-1 K^-1",
        "status": "UNVERIFIED_EFFECTIVE_KINETICS",
        "collision": "No unique elementary process or microstructural length/active-site normalization closes the Eyring rate.",
    },
    {
        "id": "SYM-022",
        "symbol": "chi_d",
        "pattern": r"\\chi_d|\\chi_\\{d\\}",
        "intended_quantity": "direction-dependent transfer coefficient split",
        "unit": "dimensionless",
        "status": "CORRECT_OR_REPLACE_WITH_KINETIC_MODEL",
        "collision": "Direction split is imposed algebraically and reused in an effective barrier reduction.",
    },
    {
        "id": "SYM-023",
        "symbol": "A / affinity",
        "pattern": r"\\mathcal A|A_\\cap|A_\\{\\mathrm\\{cap\\}",
        "intended_quantity": "reaction affinity/driving free energy",
        "unit": "J mol^-1",
        "status": "REJECT_CONSTANT_CAP_AS_PHYSICAL_AFFINITY",
        "collision": "Local voltage/state dependence is replaced by min(z_cut nRT, A_cap RT), then frozen per transition.",
    },
    {
        "id": "SYM-024",
        "symbol": "k_j",
        "pattern": r"k_j|k_\\{j\\}",
        "intended_quantity": "relaxation/rate coefficient",
        "unit": "s^-1 only if prefactor and time basis are explicit",
        "status": "UNVERIFIED_SCALE",
        "collision": "Eyring molecular attempt frequency is inserted into an electrode-scale progress equation without a demonstrated coarse-graining bridge.",
    },
    {
        "id": "SYM-025",
        "symbol": "L_q",
        "pattern": r"L_q|L_\\{q",
        "intended_quantity": "lag length in normalized charge coordinate",
        "unit": "dimensionless q",
        "status": "PRESERVE_KINEMATIC_IDENTITY_ONLY",
        "collision": "Its physical value inherits the Q_cell unit ambiguity and unverified k_j scale.",
    },
    {
        "id": "SYM-026",
        "symbol": "L_V",
        "pattern": r"L_V|L_\\{V",
        "intended_quantity": "lag length mapped to voltage coordinate",
        "unit": "V",
        "status": "EMPIRICAL_NUMERICAL_KERNEL",
        "collision": "Mapping through a local dV/dq and switching by grid steps creates grid-dependent behavior.",
    },
    {
        "id": "SYM-027",
        "symbol": "R_n",
        "pattern": r"R_n|R_\\{n\\}",
        "intended_quantity": "lumped polarization resistance",
        "unit": "ohm",
        "status": "EMPIRICAL_OBSERVATION_LAYER",
        "collision": "Ohmic, charge-transfer, and transport overpotentials are not separable in one constant.",
    },
    {
        "id": "SYM-028",
        "symbol": "C_bg",
        "pattern": r"C_\\bg|C_\\{\\mathrm\\{bg\\}",
        "intended_quantity": "background differential capacity",
        "unit": "charge per volt",
        "status": "EMPIRICAL_OBSERVATION_LAYER",
        "collision": "Must not absorb unresolved active-material transitions without an identifiability test.",
    },
    {
        "id": "SYM-029",
        "symbol": "x",
        "pattern": r"\\bx\\b|x_\\mathrm|x_\\{",
        "intended_quantity": "material Li stoichiometry in Lix host",
        "unit": "dimensionless",
        "status": "SEVERE_SYMBOL_COLLISION",
        "collision": "The same glyph/name is also used for transfer coefficient input/chi and generic SOC; separate x_host, alpha_ct, and q.",
    },
    {
        "id": "SYM-030",
        "symbol": "g",
        "pattern": r"g\(|g_j|g_\\{j",
        "intended_quantity": "requires distinct names",
        "unit": "J mol^-1, V^-1, or states energy^-1 atom^-1",
        "status": "SEVERE_SYMBOL_COLLISION",
        "collision": "Denotes free energy, dQ/dV overlap weight, and electronic DOS g(E_F).",
    },
    {
        "id": "SYM-031",
        "symbol": "g(E_F,x)",
        "pattern": r"g\(E_F|g_\\{\\max",
        "intended_quantity": "electronic density of states at the Fermi level versus composition",
        "unit": "states eV^-1 atom^-1 or explicitly normalized alternative",
        "status": "THEORY_HYPOTHESIS_UNVERIFIED",
        "collision": "A composition logistic gate is inferred from functional resemblance to Fermi occupancy, not from electronic-structure data.",
    },
    {
        "id": "SYM-032",
        "symbol": "Delta S_e",
        "pattern": r"\\Delta S_\\{e|\\Delta S_e",
        "intended_quantity": "partial-molar electronic entropy contribution",
        "unit": "J mol^-1 K^-1",
        "status": "BLOCKED_NORMALIZATION_AND_PHASE_RULE",
        "collision": "DOS normalization, composition derivative, two-phase lever rule, and relation to measured total partial entropy are unresolved.",
    },
]


def occurrences(pattern: str) -> tuple[int, list[dict]]:
    regex = re.compile(pattern)
    count = 0
    evidence: list[dict] = []
    for relative in PATHS:
        lines = (ROOT / relative).read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            if regex.search(line):
                count += 1
                if len(evidence) < 12:
                    evidence.append(
                        {
                            "path": relative,
                            "line": number,
                            "excerpt": re.sub(r"\s+", " ", line.strip())[:300],
                        }
                    )
    return count, evidence


def main() -> None:
    records = []
    for item in CONTRACTS:
        count, evidence = occurrences(item["pattern"])
        record = {key: value for key, value in item.items() if key != "pattern"}
        record["occurrence_count"] = count
        record["representative_evidence"] = evidence
        records.append(record)

    collision_counts: dict[str, int] = {}
    for record in records:
        status = record["status"]
        collision_counts[status] = collision_counts.get(status, 0) + 1

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "scope": "Core symbol, quantity, unit, sign, and role audit for six Phase 058 theory sources",
        "status": "CORE_CONTRACT_COMPLETE; EXHAUSTIVE_EQUATION_ADJUDICATION_PENDING",
        "record_count": len(records),
        "status_counts": dict(sorted(collision_counts.items())),
        "rules": [
            "One symbol must denote one physical quantity within a derivation.",
            "Reaction direction, electrode identity, and protocol label must be distinct.",
            "Units are part of the public model contract, not prose annotations.",
            "Empirical observation kernels cannot be promoted to equilibrium thermodynamics.",
        ],
        "records": records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
