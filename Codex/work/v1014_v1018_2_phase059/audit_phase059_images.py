#!/usr/bin/env python3
"""Audit all ten unique standalone image blobs in Phase 059."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
QUEUE = ROOT / "Codex/results/PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
OUTPUT = ROOT / "Codex/results/PHASE_059_IMAGE_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_STANDALONE_IMAGE_REVIEW.md"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"

GENERATOR_MAP = {
    "Claude/docs/v1.0.14/figs/P4_lco_heat_validation.png":
        "Claude/docs/v1.0.14/demo_lco_heat.py",
    "Claude/docs/v1.0.14/figs/graph_suite_v1014.png":
        "Claude/docs/v1.0.14/graph_suite_v1014.py",
    "Claude/docs/v1.0.14/sample_test_v1014.png":
        "Claude/docs/v1.0.14/sample_test_v1014.py",
    "Claude/docs/v1.0.15/figs/P4_lco_heat_validation.png":
        "Claude/docs/v1.0.15/demo_lco_heat.py",
    "Claude/docs/v1.0.15/figs/graph_suite_v1015.png":
        "Claude/docs/v1.0.15/graph_suite_v1015.py",
    "Claude/docs/v1.0.15/sample_test_v1015.png":
        "Claude/docs/v1.0.15/sample_test_v1015.py",
    "Claude/docs/v1.0.16/figs/anode_fit_v1_0_14_dqdv.png":
        "Claude/docs/v1.0.16/plot_dqdv.py",
    "Claude/docs/v1.0.16/figs/graph_suite_v1016.png":
        "Claude/docs/v1.0.16/graph_suite_v1016.py",
    "Claude/docs/v1.0.16/sample_test_v1016.png":
        "Claude/docs/v1.0.16/sample_test_v1016.py",
    "Claude/docs/v1.0.18.2/sample_test_v1018_2.png":
        "Claude/docs/v1.0.18.2/sample_test_v1018_2.py",
}

VISUAL = {
    "Claude/docs/v1.0.14/figs/P4_lco_heat_validation.png": {
        "family": "P4_LCO_HEAT",
        "panel_count": 3,
        "axes_and_units": (
            "V axis labelled [V] without Li/Li+ reference; dQ/dV has no unit; "
            "q_rev is [W]."
        ),
        "conditions": (
            "Graphite 298.15 K at 0.02/0.2/1.0 labelled C; LCO 298.15 K at "
            "0.02/0.05/0.2 labelled C; heat uses I=1 A at 298.15 K."
        ),
        "sign": (
            "s=+1 is labelled graphite discharge and LCO charge/delithiation; "
            "heat title states I>0 cell discharge and graphite lithiation."
        ),
        "morphology": (
            "Graphite rate traces mainly shift; LCO rate traces nearly overlap; "
            "no low-temperature series."
        ),
        "visual_defects": ["RIGHT_CLIPPED_PANEL_C_TITLE"],
        "scientific_scope": (
            "Synthetic graphite/LCO model output only; no observations, residuals, "
            "uncertainty, Si, blend, dopant, or >4.15 V validation."
        ),
    },
    "Claude/docs/v1.0.15/figs/P4_lco_heat_validation.png": {
        "family": "P4_LCO_HEAT",
        "panel_count": 3,
        "axes_and_units": (
            "V axis labelled [V] without Li/Li+ reference; dQ/dV has no unit; "
            "q_rev is [W]."
        ),
        "conditions": (
            "Graphite 298.15 K at 0.02/0.2/1.0 labelled C; LCO 298.15 K at "
            "0.02/0.05/0.2 labelled C; heat uses I=1 A at 298.15 K."
        ),
        "sign": (
            "s=+1 is labelled graphite discharge and LCO charge/delithiation; "
            "heat title states I>0 cell discharge and graphite lithiation."
        ),
        "morphology": (
            "Graphite rate traces mainly shift; LCO rate traces nearly overlap; "
            "no low-temperature series."
        ),
        "visual_defects": ["RIGHT_CLIPPED_PANEL_C_TITLE"],
        "scientific_scope": (
            "Synthetic graphite/LCO model output only; no observations, residuals, "
            "uncertainty, Si, blend, dopant, or >4.15 V validation."
        ),
    },
    "Claude/docs/v1.0.14/figs/graph_suite_v1014.png": {
        "family": "GRAPH_SUITE",
        "panel_count": 9,
        "axes_and_units": (
            "Voltage and heat panels carry V/W/mV/K labels, but dQ/dV, "
            "Delta-S parity axes, and charge bars omit units."
        ),
        "conditions": (
            "Graphite/LCO at 298.15 K and I_abs=0.05; graphite temperature "
            "series -15/+25/+45 C at nominal 0.2 for Q_cell=1."
        ),
        "sign": (
            "Labels state delithiation s=+1 and q_rev=-I*T*dU/dT; heat fill "
            "distinguishes endothermic/exothermic sign."
        ),
        "morphology": (
            "The low-temperature equilibrium/rate panel is taller and narrower, "
            "not a demonstration of low-T finite-current suppression/broadening."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic identity/shape suite; it explicitly labels frozen-linear "
            "LCO U(T) and no T^2 curvature. No experimental overlay."
        ),
    },
    "Claude/docs/v1.0.15/figs/graph_suite_v1015.png": {
        "family": "GRAPH_SUITE",
        "panel_count": 9,
        "axes_and_units": (
            "Voltage and heat panels carry V/W/mV/K labels, but dQ/dV, "
            "Delta-S parity axes, and charge bars omit units."
        ),
        "conditions": (
            "Graphite/LCO at 298.15 K and I_abs=0.05; graphite temperature "
            "series -15/+25/+45 C at nominal 0.2 for Q_cell=1."
        ),
        "sign": (
            "Labels state delithiation s=+1 and q_rev=-I*T*dU/dT; heat fill "
            "distinguishes endothermic/exothermic sign."
        ),
        "morphology": (
            "The low-temperature equilibrium/rate panel is taller and narrower, "
            "not a demonstration of low-T finite-current suppression/broadening."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic identity/shape suite; it explicitly labels frozen-linear "
            "LCO U(T) and no T^2 curvature. No experimental overlay."
        ),
    },
    "Claude/docs/v1.0.16/figs/graph_suite_v1016.png": {
        "family": "GRAPH_SUITE",
        "panel_count": 9,
        "axes_and_units": (
            "Voltage and heat panels carry V/W/mV/K labels, but dQ/dV, "
            "Delta-S parity axes, and charge bars omit units."
        ),
        "conditions": (
            "Graphite/LCO at 298.15 K and I_abs=0.05; graphite temperature "
            "series -15/+25/+45 C at nominal 0.2 for Q_cell=1."
        ),
        "sign": (
            "Labels state delithiation s=+1 and q_rev=-I*T*dU/dT; heat fill "
            "distinguishes endothermic/exothermic sign."
        ),
        "morphology": (
            "The low-temperature equilibrium/rate panel is taller and narrower, "
            "not a demonstration of low-T finite-current suppression/broadening."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic identity/shape suite; it explicitly labels frozen-linear "
            "LCO U(T) and no T^2 curvature. No experimental overlay."
        ),
    },
    "Claude/docs/v1.0.16/figs/anode_fit_v1_0_14_dqdv.png": {
        "family": "DQDV_BELL_SHAPES",
        "panel_count": 4,
        "axes_and_units": (
            "Voltage is [V vs Li/Li+]; dQ/dV unit is absent. FWHM is mV and "
            "integrated area is shown numerically."
        ),
        "conditions": (
            "Graphite at 298.15 K; observed branch comparison uses I_abs=0.1 "
            "and Q_cell=1; equilibrium temperature series is 5/25/55 C."
        ),
        "sign": "Discharge s=+1 and charge s=-1 are plotted explicitly.",
        "morphology": (
            "Shows bell shape, finite-window area, charge/discharge shift, and "
            "RT/F equilibrium broadening with rising temperature; lower T is "
            "taller/narrower."
        ),
        "visual_defects": ["FILENAME_VERSION_1_0_14_BUT_TITLE_AND_CODE_1_0_16"],
        "scientific_scope": (
            "Synthetic graphite-only shape check; filename is stale and the "
            "figure does not test finite-current low-T suppression/broadening."
        ),
    },
    "Claude/docs/v1.0.14/sample_test_v1014.png": {
        "family": "SAMPLE_TEST",
        "panel_count": 4,
        "axes_and_units": (
            "Voltage reference, Q_cell/V, W, J/(mol K), and composition units "
            "are shown; graphite |I|=0.05 lacks A/C unit in the title."
        ),
        "conditions": (
            "Graphite 298 K, I_abs=0.05, Q_cell=1; LCO 298 K at 0.02/0.05/0.2 C; "
            "heat at I=+1 A."
        ),
        "sign": (
            "Graphite discharge and cell-discharge heat convention are explicit; "
            "LCO facade traces are labelled discharge."
        ),
        "morphology": (
            "Free n=0.12 resolves four graphite peaks while default n=1 merges "
            "them; LCO rate traces almost overlap."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic illustrative output. Peak resolution after free-width "
            "adjustment is not phase identification or experimental validation."
        ),
    },
    "Claude/docs/v1.0.15/sample_test_v1015.png": {
        "family": "SAMPLE_TEST",
        "panel_count": 4,
        "axes_and_units": (
            "Voltage reference, Q_cell/V, W, J/(mol K), and composition units "
            "are shown; graphite |I|=0.05 lacks A/C unit in the title."
        ),
        "conditions": (
            "Graphite 298 K, I_abs=0.05, Q_cell=1; LCO 298 K at 0.02/0.05/0.2 C; "
            "heat at I=+1 A."
        ),
        "sign": (
            "Graphite discharge and cell-discharge heat convention are explicit; "
            "LCO facade traces are labelled discharge."
        ),
        "morphology": (
            "Free n=0.12 resolves four graphite peaks while default n=1 merges "
            "them; LCO rate traces almost overlap."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic illustrative output. Peak resolution after free-width "
            "adjustment is not phase identification or experimental validation."
        ),
    },
    "Claude/docs/v1.0.16/sample_test_v1016.png": {
        "family": "SAMPLE_TEST",
        "panel_count": 4,
        "axes_and_units": (
            "Voltage reference, Q_cell/V, W, J/(mol K), and composition units "
            "are shown; graphite |I|=0.05 lacks A/C unit in the title."
        ),
        "conditions": (
            "Graphite 298 K, I_abs=0.05, Q_cell=1; LCO 298 K at 0.02/0.05/0.2 C; "
            "heat at I=+1 A."
        ),
        "sign": (
            "Graphite discharge and cell-discharge heat convention are explicit; "
            "LCO facade traces are labelled discharge."
        ),
        "morphology": (
            "Free n=0.12 resolves four graphite peaks while default n=1 merges "
            "them; LCO rate traces almost overlap."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic illustrative output. Peak resolution after free-width "
            "adjustment is not phase identification or experimental validation."
        ),
    },
    "Claude/docs/v1.0.18.2/sample_test_v1018_2.png": {
        "family": "SAMPLE_TEST",
        "panel_count": 4,
        "axes_and_units": (
            "Voltage reference, Q_cell/V, W, J/(mol K), and composition units "
            "are shown; graphite |I|=0.05 lacks A/C unit in the title."
        ),
        "conditions": (
            "Graphite 298 K, I_abs=0.05, Q_cell=1; LCO 298 K at 0.02/0.05/0.2 C; "
            "heat at I=+1 A."
        ),
        "sign": (
            "Graphite discharge and cell-discharge heat convention are explicit; "
            "LCO facade traces are labelled discharge."
        ),
        "morphology": (
            "Free n=0.12 resolves four graphite peaks while default n=1 merges "
            "them; LCO rate traces almost overlap."
        ),
        "visual_defects": [],
        "scientific_scope": (
            "Synthetic illustrative output. The added Einstein feature is not "
            "activated or displayed, and there is no experimental overlay."
        ),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def raster_metrics(path: Path) -> dict:
    with Image.open(path) as source:
        source.verify()
    with Image.open(path) as source:
        mode = source.mode
        width, height = source.size
        info = {
            str(key): value
            for key, value in source.info.items()
            if isinstance(value, (str, int, float, bool, list, tuple))
        }
        gray = np.asarray(source.convert("L"), dtype=np.uint8)
    content = gray < 245
    rows, columns = np.nonzero(content)
    bbox = [
        int(columns.min()),
        int(rows.min()),
        int(columns.max()),
        int(rows.max()),
    ]
    return {
        "decode_ok": True,
        "format": "PNG",
        "mode": mode,
        "width_px": width,
        "height_px": height,
        "pil_info": info,
        "content_bbox_lt245": bbox,
        "nonwhite_fraction_lt245": float(np.mean(content)),
        "edge_nonwhite_count_lt245": {
            "left": int(np.count_nonzero(content[:, 0])),
            "right": int(np.count_nonzero(content[:, -1])),
            "top": int(np.count_nonzero(content[0, :])),
            "bottom": int(np.count_nonzero(content[-1, :])),
        },
    }


def build_report(payload: dict) -> str:
    lines = [
        "# Phase 059 standalone image review",
        "",
        "정본일: 2026-07-28",
        "",
        f"판정: `{payload['status']}`",
        "",
        "## 범위와 경계",
        "",
        (
            "Phase 059의 24 image path occurrence를 content-addressed로 묶은 "
            "10 unique PNG를 원해상도로 전부 검독했다. 이미지 hash, dimensions, "
            "pixel edge, 생성 script, 축·단위·legend·온도/전류·부호·peak morphology를 "
            "기록했다."
        ),
        "",
        (
            "10개는 모두 코드가 생성한 synthetic model output이다. 관측 데이터, "
            "오차막대, residual, 불확도, 데이터 출처가 없으므로 그림의 유한성·개형·"
            "내부 항등성 이상을 과학적 또는 실험적 validation으로 승격하지 않는다."
        ),
        "",
        "## 핵심 판정",
        "",
        (
            "- 10/10 PNG가 정상 decode되고 전 panel의 curve, axes, legend가 "
            "보인다. P4 두 unique blob은 panel (c) title이 우측 canvas에서 "
            "잘리며, 이는 6개 version occurrence에 전파된다."
        ),
        "",
        (
            "- `anode_fit_v1_0_14_dqdv.png`는 보이는 title과 generator가 "
            "v1.0.16인데 파일명은 v1.0.14다. v1.0.16 이후 네 경로에 같은 "
            "blob이 복사돼 artifact naming provenance가 틀린다."
        ),
        "",
        (
            "- P4, graph suite, bell-shape figure의 dQ/dV에는 단위가 없고, "
            "graph suite의 Delta-S parity/charge 축도 단위가 없다. sample "
            "figures는 Q_cell/V를 쓰지만 `|I|=0.05`의 A/C 단위가 없다."
        ),
        "",
        (
            "- 저온 series는 equilibrium RT/F 효과로 저온일수록 더 높고 좁게 "
            "그려진다. rate series와 temperature series를 결합한 그림은 없으므로 "
            "사용자가 관찰한 저온·유한전류 peak suppression/broadening을 입증하지 않는다."
        ),
        "",
        (
            "- Si, graphite+Si, doped high-voltage LCO, 4.15 V 초과 구간, "
            "실험 overlay가 전부 없다. LCO rate traces는 거의 겹쳐 보이며 "
            "고전압 내구성 또는 도핑 효과의 증거가 아니다."
        ),
        "",
        "## 이미지별 기록",
        "",
        "| representative | occurrences | px | family | panels | visual defect |",
        "|---|---:|---:|---|---:|---|",
    ]
    for record in payload["images"]:
        metrics = record["raster_metrics"]
        defects = ", ".join(record["visual_review"]["visual_defects"]) or "none"
        lines.append(
            f"| `{record['representative_path']}` | "
            f"{record['occurrence_count']} | "
            f"{metrics['width_px']}×{metrics['height_px']} | "
            f"{record['visual_review']['family']} | "
            f"{record['visual_review']['panel_count']} | {defects} |"
        )
    lines.extend(
        [
            "",
            "## 과학 주장 판정",
            "",
            "| ID | 판정 | 내용 |",
            "|---|---|---|",
            (
                "| IMG-059-01 | PASS_ARTIFACT_DECODE | 10/10 unique PNG decode, "
                "hash, dimensions, source mapping과 원해상도 육안 검독 완료 |"
            ),
            (
                "| IMG-059-02 | VISUAL_DEFECT | P4 panel-(c) title 우측 잘림: "
                "2 unique blobs, 6 occurrences |"
            ),
            (
                "| IMG-059-03 | PROVENANCE_DEFECT | v1.0.16 title/code image가 "
                "`v1_0_14` filename으로 저장되고 4개 release에 복사됨 |"
            ),
            (
                "| IMG-059-04 | METADATA_DEBT | 6/10 images의 dQ/dV 단위 부재; "
                "graph suite의 parity/charge 단위와 sample의 `|I|` 단위도 불완전 |"
            ),
            (
                "| IMG-059-05 | SCOPE_ABSENT | low-T × finite-current joint figure, "
                "Si/blend, doped high-voltage LCO, >4.15 V, experimental overlay 없음 |"
            ),
            (
                "| IMG-059-06 | INTERNAL_ONLY | 자유 폭으로 네 peak를 분리하고 "
                "항등/면적/열 부호를 보이는 synthetic output은 실험 상 식별이나 "
                "재료 validation이 아님 |"
            ),
            "",
            "## 다음 단계",
            "",
            (
                "Step 35.3에서 image/PDF/golden blob을 generator·TeX·Git commit과 "
                "연결하고 copy-forward, stale artifact, non-bit-exact rerender를 "
                "현재 과학 증거에서 분리한다."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    figure_records = [
        record for record in queue["records"] if record["role"] == "figure"
    ]
    images = []
    for queue_record in figure_records:
        representative = queue_record["representative_path"]
        image_path = ROOT / representative
        generator_path = ROOT / GENERATOR_MAP[representative]
        occurrences = []
        for relative in queue_record["occurrence_paths"]:
            occurrence_path = ROOT / relative
            occurrences.append(
                {
                    "path": relative,
                    "sha256": sha256(occurrence_path),
                    "git_blob_sha": git_blob_sha(occurrence_path),
                    "matches_representative": (
                        git_blob_sha(occurrence_path) == queue_record["blob_sha"]
                    ),
                }
            )
        source = generator_path.read_text(encoding="utf-8")
        images.append(
            {
                "blob_sha": queue_record["blob_sha"],
                "representative_path": representative,
                "sha256": sha256(image_path),
                "git_blob_sha": git_blob_sha(image_path),
                "queue_blob_matches": (
                    git_blob_sha(image_path) == queue_record["blob_sha"]
                ),
                "occurrence_count": len(occurrences),
                "occurrences": occurrences,
                "raster_metrics": raster_metrics(image_path),
                "generator": {
                    "path": str(generator_path.relative_to(ROOT)),
                    "sha256": sha256(generator_path),
                    "git_blob_sha": git_blob_sha(generator_path),
                    "line_count": len(source.splitlines()),
                    "mentions_output_basename": image_path.name in source,
                },
                "visual_review": {
                    **VISUAL[representative],
                    "inspection_status": "ORIGINAL_RESOLUTION_VISUALLY_INSPECTED",
                },
                "evidence_class": "SYNTHETIC_MODEL_OUTPUT",
                "contains_experimental_observations": False,
            }
        )

    findings = [
        {
            "id": "IMG-059-01",
            "status": "PASS_ARTIFACT_DECODE",
            "claim": "All 10 unique PNGs decode and were inspected at original resolution.",
        },
        {
            "id": "IMG-059-02",
            "status": "VISUAL_DEFECT",
            "claim": (
                "Both unique P4 images clip the panel-(c) title at the right canvas "
                "edge; the defect occurs at six version paths."
            ),
        },
        {
            "id": "IMG-059-03",
            "status": "PROVENANCE_DEFECT",
            "claim": (
                "The v1.0.16 bell-shape image has a v1.0.14 filename and is copied "
                "unchanged through v1.0.18.2."
            ),
        },
        {
            "id": "IMG-059-04",
            "status": "METADATA_DEBT",
            "claim": (
                "Six images omit dQ/dV units, while graph-suite parity/charge units "
                "and sample-test current units are also incomplete."
            ),
        },
        {
            "id": "IMG-059-05",
            "status": "SCOPE_ABSENT",
            "claim": (
                "No image contains a joint low-temperature/finite-current sweep, "
                "Si or graphite-Si, doped high-voltage LCO, >4.15 V coverage, or "
                "experimental observations."
            ),
        },
        {
            "id": "IMG-059-06",
            "status": "INTERNAL_ONLY",
            "claim": (
                "Peak splitting under a free width and internal identity/shape plots "
                "do not establish phase identity or experimental validity."
            ),
        },
    ]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": BASELINE,
        "source_queue": str(QUEUE.relative_to(ROOT)),
        "source_queue_sha256": sha256(QUEUE),
        "unique_image_count": len(images),
        "image_path_occurrence_count": sum(
            image["occurrence_count"] for image in images
        ),
        "visually_inspected_unique_image_count": len(images),
        "image_family_counts": {
            family: sum(
                image["visual_review"]["family"] == family for image in images
            )
            for family in sorted(
                {image["visual_review"]["family"] for image in images}
            )
        },
        "images": images,
        "findings": findings,
        "summary": {
            "decode_failure_count": sum(
                not image["raster_metrics"]["decode_ok"] for image in images
            ),
            "queue_blob_mismatch_count": sum(
                not image["queue_blob_matches"] for image in images
            ),
            "occurrence_blob_mismatch_count": sum(
                not occurrence["matches_representative"]
                for image in images
                for occurrence in image["occurrences"]
            ),
            "generator_missing_count": sum(
                not (ROOT / image["generator"]["path"]).exists() for image in images
            ),
            "generator_output_name_missing_count": sum(
                not image["generator"]["mentions_output_basename"] for image in images
            ),
            "unique_visual_defect_image_count": sum(
                bool(image["visual_review"]["visual_defects"]) for image in images
            ),
            "right_edge_content_image_count": sum(
                image["raster_metrics"]["edge_nonwhite_count_lt245"]["right"] > 0
                for image in images
            ),
            "experimental_observation_image_count": sum(
                image["contains_experimental_observations"] for image in images
            ),
        },
        "claim_boundary": (
            "Image decoding and synthetic-model shape checks do not validate physical "
            "mechanisms, material identity, parameters, literature, or experiments."
        ),
        "status": "CONDITIONAL_P059_SYNTHETIC_IMAGE_EVIDENCE",
        "next_action": (
            "Connect image/PDF/golden blobs to generators and Git commits and test "
            "isolated rerender reproducibility in Step 35.3."
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    print(f"wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
