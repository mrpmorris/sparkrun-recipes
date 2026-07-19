#!/usr/bin/env python3
# pip install pandas matplotlib pillow requests

import argparse
import colorsys
import json
import math
import os
import re
import textwrap
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")  # headless: no display on the DGX

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import MultipleLocator
from PIL import Image


INTEL_METRICS = [
    "MMLU",
    "GSM8K strict",
    "GSM8K flex",
    "ARC acc",
    "ARC norm",
    "HellaSwag acc",
    "HellaSwag norm",
    "HumanEval",
    "MBPP",
]

# BFCL v4 OVERALL (weighted aggregate) from the tool-calling section. Kept out
# of INTEL_METRICS so it does not shift the lm-eval Mean used for row ordering.
TOOL_METRIC = "BFCL overall"

# lm-eval task name -> the heat-map columns it feeds, for mapping the report's
# "Failed benchmarks" codes onto cells.
TASK_METRICS = {
    "mmlu": ["MMLU"],
    "gsm8k": ["GSM8K strict", "GSM8K flex"],
    "arc_challenge": ["ARC acc", "ARC norm"],
    "hellaswag": ["HellaSwag acc", "HellaSwag norm"],
    "humaneval": ["HumanEval"],
    "mbpp": ["MBPP"],
}

PURPOSES = {
    "MMLU": "general knowledge",
    "GSM8K strict": "math reasoning",
    "GSM8K flex": "math reasoning",
    "ARC acc": "science reasoning",
    "ARC norm": "science reasoning",
    "HellaSwag acc": "commonsense",
    "HellaSwag norm": "commonsense",
    "HumanEval": "coding",
    "MBPP": "coding",
    TOOL_METRIC: "tool calling",
}


def http_get_text(url: str) -> str:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "sparkrun-report-generator",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    with urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8")


def fetch_github_markdown(repo: str, ref: str, path: str) -> list[tuple[str, str]]:
    api_url = (
        f"https://api.github.com/repos/{repo}/contents/"
        f"{quote(path.strip('/'))}?ref={quote(ref)}"
    )

    items = json.loads(http_get_text(api_url))
    reports = []

    for item in items:
        if item.get("type") != "file":
            continue

        name = item.get("name", "")
        if not name.lower().endswith(".md"):
            continue

        download_url = item.get("download_url")
        if not download_url:
            continue

        reports.append((name, http_get_text(download_url)))

    return reports


def load_local_markdown(input_dir: Path) -> list[tuple[str, str]]:
    reports = []
    for file_path in sorted(input_dir.glob("*.md")):
        reports.append((file_path.name, file_path.read_text(encoding="utf-8")))
    return reports


def format_prompt_size(tokens: float) -> str:
    if tokens < 1024:
        return f"{int(tokens)}B"
    return f"{math.ceil(tokens / 1024)}K"


def label_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    return stem.replace("__", "-").replace("_", "-")


def split_md_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_float(value: str) -> float | None:
    value = value.strip().replace(",", "")
    if not value or value.upper() == "FAILED":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def parse_int(value: str) -> int | None:
    value = value.strip().replace(",", "")
    if not value or value.upper() == "FAILED":
        return None

    try:
        return int(float(value))
    except ValueError:
        return None


def metric_name(task: str, metric: str) -> str | None:
    task = task.strip().lower()
    metric = metric.strip().lower()

    if task == "mmlu" and metric == "acc,none":
        return "MMLU"

    if task == "gsm8k" and metric == "exact_match,strict-match":
        return "GSM8K strict"

    if task == "gsm8k" and metric == "exact_match,flexible-extract":
        return "GSM8K flex"

    if task == "arc_challenge" and metric == "acc,none":
        return "ARC acc"

    if task == "arc_challenge" and metric == "acc_norm,none":
        return "ARC norm"

    if task == "hellaswag" and metric == "acc,none":
        return "HellaSwag acc"

    if task == "hellaswag" and metric == "acc_norm,none":
        return "HellaSwag norm"

    if task == "humaneval" and metric == "pass@1,create_test":
        return "HumanEval"

    if task == "mbpp" and metric == "pass_at_1,none":
        return "MBPP"

    return None


def parse_intelligence_scores(text: str) -> dict[str, float]:
    # Only metrics actually present in the report; missing ones stay NaN in the
    # dataframe so they can be shown as failures rather than fake 0.00 scores.
    scores: dict[str, float] = {}

    in_intel = False
    for line in text.splitlines():
        if line.startswith("## Intelligence"):
            in_intel = True
            continue

        if in_intel and line.startswith("## Tool calling"):
            break

        if not in_intel:
            continue

        if not line.strip().startswith("|"):
            continue

        cols = split_md_row(line)
        if len(cols) < 5:
            continue

        task = cols[0]
        metric = cols[2]
        value = parse_float(cols[3])
        key = metric_name(task, metric)

        if key is not None and value is not None:
            scores[key] = value

    return scores


def parse_tool_call_overall(text: str) -> float | None:
    in_section = False

    for line in text.splitlines():
        if line.startswith("## Tool calling"):
            in_section = True
            continue

        if in_section and line.startswith("## "):
            break

        if not in_section:
            continue

        if not line.strip().startswith("|"):
            continue

        cols = split_md_row(line)
        if len(cols) < 2:
            continue

        if cols[0].upper() == "OVERALL":
            return parse_float(cols[1])

    return None


def report_failed(text: str) -> bool:
    return any(line.startswith("## Status: FAILED") for line in text.splitlines())


def parse_failed_tasks(text: str) -> dict[str, str]:
    """Task -> failure code (OOM/CRASH/HANG/...) from the Failed benchmarks table."""
    failures: dict[str, str] = {}
    in_section = False

    for line in text.splitlines():
        if line.startswith("### Failed benchmarks"):
            in_section = True
            continue

        if in_section and (line.startswith("## ") or line.startswith("### ")):
            break

        if not in_section:
            continue

        if not line.strip().startswith("|"):
            continue

        cols = split_md_row(line)
        if len(cols) < 4:
            continue

        task = cols[0].lower()
        code = cols[1].upper()
        if task in TASK_METRICS and code and code not in ("CODE", "---"):
            failures[task] = code

    return failures


def parse_speed_rows(text: str) -> list[dict[str, float]]:
    rows = []
    in_speed = False

    for line in text.splitlines():
        if line.startswith("## Speed vs prompt size"):
            in_speed = True
            continue

        if in_speed and line.startswith("## "):
            break

        if not in_speed:
            continue

        if not line.strip().startswith("|"):
            continue

        cols = split_md_row(line)
        if len(cols) < 7:
            continue

        prompt_tokens = parse_int(cols[0])
        ttft_s = parse_float(cols[2])
        tpot_ms = parse_float(cols[3])
        generation_tps = parse_float(cols[5])

        if prompt_tokens is None:
            continue

        if ttft_s is None or tpot_ms is None or generation_tps is None:
            continue

        rows.append(
            {
                "prompt_tokens": prompt_tokens,
                "ttft_s": ttft_s,
                "tpot_ms": tpot_ms,
                "generation_tps": generation_tps,
            }
        )

    return rows


def parse_concurrency_rows(text: str) -> list[dict[str, float]]:
    rows = []
    in_section = False

    for line in text.splitlines():
        if line.startswith("## Throughput vs concurrency"):
            in_section = True
            continue

        if in_section and line.startswith("## "):
            break

        if not in_section:
            continue

        if not line.strip().startswith("|"):
            continue

        cols = split_md_row(line)
        if len(cols) < 8:
            continue

        concurrency = parse_int(cols[0])
        aggregate_tps = parse_float(cols[6])

        if concurrency is None or aggregate_tps is None:
            continue

        rows.append(
            {
                "concurrency": concurrency,
                "aggregate_tps": aggregate_tps,
            }
        )

    return rows


def make_score_cmap(gradient_path: Path | None) -> LinearSegmentedColormap:
    if gradient_path is None:
        return LinearSegmentedColormap.from_list(
            "red_yellow_green",
            ["#f05a28", "#f59a2f", "#f5e94e", "#8cc63f"],
            N=256,
        )

    img = Image.open(gradient_path).convert("RGB")
    arr = np.asarray(img)
    row = arr[arr.shape[0] // 2, :, :] / 255.0

    left = row[0]
    right = row[-1]

    left_redness = left[0] - left[1]
    right_redness = right[0] - right[1]

    if right_redness > left_redness:
        xs = np.linspace(row.shape[0] - 1, 0, 256).astype(int)
    else:
        xs = np.linspace(0, row.shape[0] - 1, 256).astype(int)

    colors = [tuple(row[x]) for x in xs]
    return LinearSegmentedColormap.from_list("user_red0_green1", colors, N=256)


def wrap_text(value: str, width: int) -> str:
    if not value:
        return ""

    return "\n".join(
        textwrap.wrap(str(value), width=width, break_long_words=False)
    )


def _color_distance(rgb_a: tuple[float, float, float],
                    rgb_b: tuple[float, float, float]) -> float:
    """Approximate perceptual distance between two RGB colours ("redmean")."""
    r1, g1, b1 = (channel * 255.0 for channel in rgb_a)
    r2, g2, b2 = (channel * 255.0 for channel in rgb_b)
    r_mean = (r1 + r2) / 2.0
    dr, dg, db = r1 - r2, g1 - g2, b1 - b2
    return math.sqrt(
        (2 + r_mean / 256.0) * dr * dr
        + 4 * dg * dg
        + (2 + (255.0 - r_mean) / 256.0) * db * db
    )


def pick_distinct_color(existing: list[str]) -> str:
    """Colour maximally distant from every colour already assigned. Candidates
    are the default matplotlib cycle (so early picks stay familiar) plus a grid
    of hues at several saturation/brightness levels, all dark enough to read
    against the white page."""
    existing_rgb = [mcolors.to_rgb(c) for c in existing]

    candidates = [
        mcolors.to_rgb(c)
        for c in plt.rcParams["axes.prop_cycle"].by_key()["color"]
    ]
    for value, saturation in ((0.85, 0.9), (0.55, 0.9), (0.85, 0.5), (0.4, 0.7)):
        for step in range(36):
            candidates.append(colorsys.hsv_to_rgb(step / 36.0, saturation, value))

    best = max(
        candidates,
        key=lambda c: min(
            (_color_distance(c, e) for e in existing_rgb), default=float("inf")
        ),
    )
    return mcolors.to_hex(best)


def build_color_map(benchmarks: list[str], colors_path: Path) -> dict[str, str]:
    """Persistent benchmark -> colour map shared by every figure and every run
    (upsert: known models keep the colour stored in colors_path; new models get
    a colour as visually distinct as possible from those already assigned)."""
    color_map: dict[str, str] = {}
    if colors_path.exists():
        color_map = json.loads(colors_path.read_text(encoding="utf-8"))

    added = False
    for bm in sorted(benchmarks):
        if bm not in color_map:
            color_map[bm] = pick_distinct_color(list(color_map.values()))
            added = True

    if added:
        colors_path.write_text(
            json.dumps(color_map, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    return color_map


FAIL_CELL_COLOR = "#c8c8c8"


def build_intelligence_figure(
    intel_df: pd.DataFrame,
    codes_df: pd.DataFrame,
    cmap: LinearSegmentedColormap,
    color_map: dict[str, str],
) -> plt.Figure:
    # Failures still count as 0 for the Mean and the rankings; NaN survives
    # only into the heat-map cells, where it is drawn grey with its code.
    df = intel_df.fillna(0.0)
    df["Mean"] = df[INTEL_METRICS].mean(axis=1)
    df = df.sort_values("Mean", ascending=False)

    table_rows = []
    for test in INTEL_METRICS + [TOOL_METRIC]:
        ranked = df.sort_values([test, "Mean"], ascending=False)
        top5 = ranked.head(5).index.tolist()
        while len(top5) < 5:
            top5.append("")

        table_rows.append(
            [
                test,
                PURPOSES.get(test, ""),
                top5[0],
                top5[1],
                top5[2],
                top5[3],
                top5[4],
            ]
        )

    rank_table = pd.DataFrame(
        table_rows,
        columns=["Test name", "Purpose", "1st", "2nd", "3rd", "4th", "5th"],
    )

    wrapped_table = rank_table.copy()
    wrapped_table["Test name"] = wrapped_table["Test name"].apply(
        lambda x: wrap_text(x, 12)
    )
    wrapped_table["Purpose"] = wrapped_table["Purpose"].apply(
        lambda x: wrap_text(x, 13)
    )
    for col in ["1st", "2nd", "3rd", "4th", "5th"]:
        wrapped_table[col] = wrapped_table[col].apply(lambda x: wrap_text(x, 21))

    plot_cols = INTEL_METRICS + [TOOL_METRIC, "Mean"]
    # NaN scores (test failed / never ran) drawn as grey cells; the Mean column
    # is always numeric.
    plot_df = intel_df.reindex(index=df.index)
    plot_df["Mean"] = df["Mean"]
    plot_df = plot_df[plot_cols]
    cell_codes = codes_df.reindex(index=df.index)

    fig = plt.figure(figsize=(22, 18))
    grid = fig.add_gridspec(
        nrows=2,
        ncols=2,
        height_ratios=[3.2, 1.7],
        width_ratios=[2.8, 1.2],
        hspace=0.22,
        wspace=0.08,
    )

    ax = fig.add_subplot(grid[0, :])
    values = plot_df.values
    heat_cmap = cmap.copy()
    heat_cmap.set_bad(FAIL_CELL_COLOR)
    image = ax.imshow(
        np.ma.masked_invalid(values), aspect="auto", vmin=0, vmax=1, cmap=heat_cmap
    )

    ax.set_xticks(range(len(plot_cols)))
    ax.set_xticklabels(plot_cols, rotation=35, ha="right", fontsize=11)
    ax.set_yticks(range(len(plot_df.index)))
    ax.set_yticklabels(plot_df.index, fontsize=10)
    # Colour each model name to match its line on the speed graphs (models with
    # no speed data have no line, so they stay black).
    for label, name in zip(ax.get_yticklabels(), plot_df.index):
        label.set_color(color_map.get(name, "black"))

    ax.set_title(
        "Sparkrun intelligence scores (grey = test failed or could not run)",
        fontsize=18,
        pad=16,
    )
    ax.set_xlabel("Metric (lm-eval, plus BFCL v4 tool calling)", fontsize=12)
    ax.set_ylabel("Benchmark", fontsize=12)

    ax.set_xticks([x - 0.5 for x in range(1, len(plot_cols))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(plot_df.index))], minor=True)
    ax.grid(which="minor", color="black", linewidth=0.45)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Score", fontsize=12)
    cbar.ax.tick_params(labelsize=10)
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
    cbar.set_ticklabels(["0 red", "0.25", "0.50", "0.75", "1 green"])

    # Fill each cell with its score, sized so text + a 0.25em border fills the
    # cell height (uniform scaling keeps the aspect ratio). The border is the
    # bbox padding, drawn in the cell's own heat-map colour. Measure the final
    # cell height (after the colorbar has shrunk the axes) to pick the size.
    fig.canvas.draw()
    cell_px = abs(
        ax.transData.transform((0, 1))[1] - ax.transData.transform((0, 0))[1]
    )
    cell_pts = cell_px * 72.0 / fig.dpi
    # box height ~= text(1em) + 2 * 0.25em pad = 1.5em; fill ~95% of the cell.
    cell_fontsize = max(6.0, cell_pts * 0.95 / 1.5)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = values[i, j]
            if np.isnan(value):
                # Test never produced a score: show why instead of a fake 0.00
                # (UNSUP = server can't do echo+logprobs, FAILED = server never
                # started, else the report's OOM/CRASH/HANG/ERROR code).
                code = cell_codes.iloc[i][plot_cols[j]] or "n/a"
                label = "UNSUP" if code == "UNSUPPORTED" else code
                text_color = "#555555"
                face = FAIL_CELL_COLOR
                fontsize = cell_fontsize * min(1.0, 4.5 / len(label))
            else:
                label = f"{value:.2f}"
                text_color = "black"
                face = cmap(value)
                fontsize = cell_fontsize
            ax.text(
                j,
                i,
                label,
                ha="center",
                va="center",
                fontsize=fontsize,
                color=text_color,
                bbox={
                    "boxstyle": "square,pad=0.25",
                    "facecolor": face,
                    "edgecolor": "none",
                },
            )

    ax_table = fig.add_subplot(grid[1, 0])
    ax_table.axis("off")
    ax_table.set_title("Top 5 models per test", loc="left", fontsize=14, pad=8)

    table = ax_table.table(
        cellText=wrapped_table.values,
        colLabels=wrapped_table.columns,
        cellLoc="left",
        colLoc="left",
        loc="upper left",
        colWidths=[0.12, 0.12, 0.15, 0.15, 0.15, 0.15, 0.16],
        bbox=[0.0, 0.0, 1.0, 1.0],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.1)
    table.scale(1, 1.45)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(0.6)
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#f2f2f2")
        else:
            cell.set_facecolor("white")
            # Columns 2..6 hold model names; colour them to match the graphs.
            if col >= 2:
                name = table_rows[row - 1][col]
                cell.set_text_props(color=color_map.get(name, "black"))

    ax_note = fig.add_subplot(grid[1, 1])
    ax_note.axis("off")
    ax_note.text(
        0,
        1,
        "Ranking rule:\n"
        "- Failures counted as 0 (shown grey with a code)\n"
        "- FAILED: server never started; UNSUP: server\n"
        "  lacks echo+logprobs for multiple-choice tasks;\n"
        "  OOM/CRASH/HANG/ERROR: from the report\n"
        "- Top 5 chosen by score for each test\n"
        "- Ties broken by Mean, then current order\n"
        "- Mean covers lm-eval metrics only (excludes BFCL)",
        va="top",
        ha="left",
        fontsize=11,
    )

    return fig


def build_line_figure(
    speed_df: pd.DataFrame,
    value_col: str,
    title: str,
    y_label: str,
    log_y: bool,
    color_map: dict[str, str],
    y_tick_step: float | None = None,
    x_col: str = "prompt_tokens",
    x_label: str = "Prompt tokens",
    x_tick_formatter=format_prompt_size,
    x_tick_rotation: float = 90,
) -> plt.Figure:
    # Portrait page (the intelligence page keeps its own landscape size).
    fig, ax = plt.subplots(figsize=(12, 16))

    if speed_df.empty:
        ax.text(0.5, 0.5, "No numeric speed rows found", ha="center", va="center")
        ax.set_title(title)
        return fig

    pivot = (
        speed_df.pivot_table(
            index=x_col,
            columns="benchmark",
            values=value_col,
            aggfunc="first",
        )
        .sort_index()
    )

    x_values = list(pivot.index)
    max_x = max(x_values)

    # Draw each series, remembering its colour and first data point so the
    # left-hand label can match and connect to it.
    label_points = []
    for benchmark in pivot.columns:
        series = pivot[benchmark].dropna()
        if series.empty:
            continue

        color = color_map.get(benchmark)
        ax.plot(series.index, series.values, marker="o", linewidth=2, color=color)

        first_x = series.index[0]
        first_y = float(series.iloc[0])
        label_points.append((benchmark, first_x, first_y, color))

    ax.set_xscale("log", base=2)
    if log_y:
        ax.set_yscale("log")

    ax.set_xticks(x_values)
    ax.set_xticklabels(
        [x_tick_formatter(x) for x in x_values],
        rotation=x_tick_rotation,
        ha="center",
    )
    ax.set_xlabel(x_label)
    # The y-axis moves to the right so the left side is clear for the model
    # name column.
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    if y_tick_step and not log_y:
        # A fixed tick step over a huge data range (e.g. bogus tok/s values
        # when a diffusion model reports near-zero TPOT) makes matplotlib
        # grind on ~1M ticks at 100% CPU and tens of GB of RAM. Only use the
        # fixed step when it yields a sane number of ticks.
        lo, hi = ax.get_ylim()
        if (hi - lo) / y_tick_step <= 400:
            ax.yaxis.set_major_locator(MultipleLocator(y_tick_step))
    ax.grid(True, which="both", axis="both")
    ax.set_xlim(min(x_values) * 0.85, max_x * 1.05)

    # Reserve room on the left for the label column (the longest recipe names
    # run ~50 characters, ~3.7in at 9pt on the narrower portrait page). Fix the
    # axes box first so the transforms below are final before we measure where
    # each line starts.
    margin_top, margin_bottom = 0.96, 0.06
    fig.subplots_adjust(left=0.34, right=0.92, top=margin_top, bottom=margin_bottom)

    # List the model names in a column to the left of the plot. Each name sits
    # at the same height as its series' first data point; only where names would
    # collide are they merged into a stack centred on the group's mean height.
    # A thin colour-matched leader line joins each name to its first data point.
    if label_points:
        n = len(label_points)

        # Axes-fraction height of each series' first data point (handles the
        # log/linear y-axis transparently via the finalised transforms).
        fig.canvas.draw()
        inv_axes = ax.transAxes.inverted()
        items = [
            (bm, px, py, color,
             float(inv_axes.transform(ax.transData.transform((px, py)))[1]))
            for bm, px, py, color in label_points
        ]
        # Work bottom-to-top so stacking preserves the lines' vertical order.
        items.sort(key=lambda it: it[4])

        # Minimum gap between two names = one text line (points -> axes
        # fraction), shrinking only if every name landed in one stack that
        # could not otherwise fit the plot height.
        axis_height_in = fig.get_figheight() * (margin_top - margin_bottom)
        spacing = (9 * 1.35 / 72.0) / axis_height_in
        lo, hi = 0.01, 0.99
        if n > 1 and spacing * (n - 1) > (hi - lo):
            spacing = (hi - lo) / (n - 1)

        # Greedily merge overlapping names into groups. Each group is stored as
        # [sum_of_ideal_heights, count]; two adjacent groups overlap when their
        # centres are closer than half their combined heights, and a merged
        # group re-centres on the mean ideal height of all its members.
        groups: list[list[float]] = []
        for _bm, _px, _py, _color, frac in items:
            groups.append([frac, 1])
            while len(groups) >= 2:
                lower_c = groups[-2][0] / groups[-2][1]
                upper_c = groups[-1][0] / groups[-1][1]
                min_sep = (groups[-2][1] + groups[-1][1]) / 2 * spacing
                if upper_c - lower_c < min_sep:
                    s = groups[-2][0] + groups[-1][0]
                    k = groups[-2][1] + groups[-1][1]
                    groups[-2:] = [[s, k]]
                else:
                    break

        # Expand groups back into a label position per item (bottom-to-top).
        positions: list[float] = []
        for s, k in groups:
            center = s / k
            start = center - (k - 1) / 2 * spacing
            positions.extend(start + j * spacing for j in range(int(k)))

        # Keep the whole column inside the plot height.
        if positions[0] < lo:
            positions = [p + (lo - positions[0]) for p in positions]
        if positions[-1] > hi:
            positions = [p - (positions[-1] - hi) for p in positions]

        label_x = -0.015
        for (benchmark, point_x, point_y, color, _frac), label_y in zip(
            items, positions
        ):
            # Leader ends exactly at the label's right-centre anchor (no bbox
            # shrink), so it always meets the very right of the name.
            leader = ConnectionPatch(
                xyA=(point_x, point_y),
                coordsA=ax.transData,
                xyB=(label_x, label_y),
                coordsB=ax.transAxes,
                color=color,
                lw=0.7,
                alpha=0.6,
                zorder=2.5,
            )
            leader.set_clip_on(False)
            ax.add_artist(leader)
            ax.text(
                label_x,
                label_y,
                benchmark,
                transform=ax.transAxes,
                va="center",
                ha="right",
                fontsize=9,
                color=color,
                clip_on=False,
            )

    return fig


def build_dataframes(
    reports: list[tuple[str, str]],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    intel_rows = []
    code_rows = []
    speed_rows = []
    concurrency_rows = []

    for filename, text in reports:
        benchmark = label_from_filename(filename)

        scores = parse_intelligence_scores(text)
        tool_overall = parse_tool_call_overall(text)
        if tool_overall is not None:
            scores[TOOL_METRIC] = tool_overall
        scores["benchmark"] = benchmark
        intel_rows.append(scores)

        # Failure code per metric with no score: whole-report failures (server
        # never started) mark every cell, otherwise use the per-task codes from
        # the report's Failed benchmarks table.
        if report_failed(text):
            codes = {m: "FAILED" for m in INTEL_METRICS + [TOOL_METRIC]}
        else:
            codes = {}
            for task, code in parse_failed_tasks(text).items():
                for m in TASK_METRICS[task]:
                    codes[m] = code
        codes["benchmark"] = benchmark
        code_rows.append(codes)

        for row in parse_speed_rows(text):
            row["benchmark"] = benchmark
            speed_rows.append(row)

        for row in parse_concurrency_rows(text):
            row["benchmark"] = benchmark
            concurrency_rows.append(row)

    intel_df = pd.DataFrame(intel_rows).set_index("benchmark")
    intel_df = intel_df.reindex(columns=INTEL_METRICS + [TOOL_METRIC])

    codes_df = pd.DataFrame(code_rows).set_index("benchmark")
    codes_df = codes_df.reindex(columns=INTEL_METRICS + [TOOL_METRIC]).fillna("")

    speed_df = pd.DataFrame(speed_rows)
    if not speed_df.empty:
        speed_df = speed_df[
            ["benchmark", "prompt_tokens", "ttft_s", "tpot_ms", "generation_tps"]
        ]

    concurrency_df = pd.DataFrame(concurrency_rows)
    if not concurrency_df.empty:
        concurrency_df = concurrency_df[["benchmark", "concurrency", "aggregate_tps"]]

    return intel_df, codes_df, speed_df, concurrency_df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="mrpmorris/sparkrun-recipes")
    parser.add_argument("--ref", default="master")
    parser.add_argument("--path", default="benchmarks")
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--gradient", type=Path)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/_Comparison.pdf"))
    parser.add_argument(
        "--colors",
        type=Path,
        help="model -> colour upsert file (default: _colors.json next to the output)",
    )
    args = parser.parse_args()

    if args.input_dir:
        reports = load_local_markdown(args.input_dir)
    else:
        reports = fetch_github_markdown(args.repo, args.ref, args.path)

    if not reports:
        raise RuntimeError("No markdown benchmark reports found")

    intel_df, codes_df, speed_df, concurrency_df = build_dataframes(reports)
    cmap = make_score_cmap(args.gradient)

    names = set()
    if not speed_df.empty:
        names.update(speed_df["benchmark"].unique())
    if not concurrency_df.empty:
        names.update(concurrency_df["benchmark"].unique())
    colors_path = args.colors or args.output.parent / "_colors.json"
    color_map = build_color_map(sorted(names), colors_path)

    with PdfPages(args.output) as pdf:
        fig = build_intelligence_figure(intel_df, codes_df, cmap, color_map)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "generation_tps",
            "Sparkrun benchmark TPS by prompt size",
            "TPS, generation tokens/s",
            log_y=False,
            color_map=color_map,
            y_tick_step=5,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            concurrency_df,
            "aggregate_tps",
            "Sparkrun benchmark aggregate TPS by concurrency (1024-token prompts)",
            "Aggregate generation tokens/s",
            log_y=False,
            color_map=color_map,
            x_col="concurrency",
            x_label="Concurrent requests",
            x_tick_formatter=lambda x: f"{int(x):,}",
            x_tick_rotation=0,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "ttft_s",
            "Sparkrun benchmark time to first token by prompt size",
            "TTFT seconds",
            log_y=False,
            color_map=color_map,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "tpot_ms",
            "Sparkrun benchmark TPOT by prompt size",
            "TPOT ms",
            log_y=False,
            color_map=color_map,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    print(args.output)


if __name__ == "__main__":
    main()
