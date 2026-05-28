# Phase 018 — Final Chapter 1 TeX Result

## Summary

The first-principles Chapter 1 manuscript was created as a new file:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex`

It starts with a review-paper-like convention section and does not repair or reuse the invalidated manuscript.

Gate result: `PASS_FINAL_TEX_CREATED`

## Metadata

| Item | Value |
|---|---|
| File | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex` |
| Lines | 386 |
| SHA256 | `C1DF430F20F27B2A5F438D9331AEECFDD71DB320938D59F2DED82C2E4ADE9988` |

## Static Verification

| Check | Result |
|---|---|
| Brace balance | PASS, `OK` |
| Labels | PASS, 21 labels / 21 unique |
| Duplicate labels | PASS, none |
| Missing `eqref` targets | PASS, none |
| Document begin/end count | PASS, 1 / 1 |
| Forbidden hygiene/search markers | PASS, no matches |

## Content Verification

| Requirement | Result |
|---|---|
| Starts with convention section | PASS |
| Uses new variables and derivation | PASS |
| No old TeX equation line references | PASS |
| No invalidated manuscript references | PASS |
| No fitting code or solver | PASS |
| Peak area not central | PASS |
| Chapter 2-5 only roadmap | PASS |

## Gate

Gate: `PASS_FINAL_TEX_CREATED`

Status: PASS

Reason:

- new final TeX file exists;
- convention section appears before the main derivation;
- static checks pass;
- the manuscript is based on the Phase 016 first-principles derivation and Phase 017 equation-origin audit.

## Confirmed Non-Changes

- Invalidated manuscript was not edited during this phase.
- Original source files were not modified.
- Claude folder was not modified by this Codex phase.
