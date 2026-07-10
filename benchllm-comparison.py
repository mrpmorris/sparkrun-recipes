#!/usr/bin/env python3
# pip install pandas matplotlib pillow requests

import argparse
import json
import os
import re
import statistics
import textwrap
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")  # headless: no display on the DGX

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
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
    scores = {metric: 0.0 for metric in INTEL_METRICS}

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


def build_intelligence_figure(
    intel_df: pd.DataFrame,
    cmap: LinearSegmentedColormap,
) -> plt.Figure:
    df = intel_df.copy()
    df["Mean"] = df[INTEL_METRICS].mean(axis=1)
    df = df.sort_values("Mean", ascending=False)

    table_rows = []
    for test in INTEL_METRICS:
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

    plot_cols = INTEL_METRICS + ["Mean"]
    plot_df = df[plot_cols]

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
    image = ax.imshow(values, aspect="auto", vmin=0, vmax=1, cmap=cmap)

    ax.set_xticks(range(len(plot_cols)))
    ax.set_xticklabels(plot_cols, rotation=35, ha="right", fontsize=11)
    ax.set_yticks(range(len(plot_df.index)))
    ax.set_yticklabels(plot_df.index, fontsize=10)

    ax.set_title("Sparkrun intelligence scores, failures as zero", fontsize=18, pad=16)
    ax.set_xlabel("lm-eval metric", fontsize=12)
    ax.set_ylabel("Benchmark", fontsize=12)

    ax.set_xticks([x - 0.5 for x in range(1, len(plot_cols))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(plot_df.index))], minor=True)
    ax.grid(which="minor", color="black", linewidth=0.45)
    ax.tick_params(which="minor", bottom=False, left=False)

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            ax.text(
                j,
                i,
                f"{values[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color="black",
                bbox={
                    "boxstyle": "square,pad=0.18",
                    "facecolor": "white",
                    "edgecolor": "none",
                    "alpha": 0.92,
                },
            )

    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Score", fontsize=12)
    cbar.ax.tick_params(labelsize=10)
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
    cbar.set_ticklabels(["0 red", "0.25", "0.50", "0.75", "1 green"])

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

    ax_note = fig.add_subplot(grid[1, 1])
    ax_note.axis("off")
    ax_note.text(
        0,
        1,
        "Ranking rule:\n"
        "- Failures counted as 0\n"
        "- Top 5 chosen by score for each test\n"
        "- Ties broken by Mean, then current order",
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
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(18, 10))

    if speed_df.empty:
        ax.text(0.5, 0.5, "No numeric speed rows found", ha="center", va="center")
        ax.set_title(title)
        return fig

    pivot = (
        speed_df.pivot_table(
            index="prompt_tokens",
            columns="benchmark",
            values=value_col,
            aggfunc="first",
        )
        .sort_index()
    )

    x_values = list(pivot.index)
    max_x = max(x_values)

    # Draw each series, remembering its colour and last data point so the
    # right-hand label can match and connect to it.
    label_points = []
    for benchmark in pivot.columns:
        series = pivot[benchmark].dropna()
        if series.empty:
            continue

        line = ax.plot(series.index, series.values, marker="o", linewidth=2)[0]

        last_x = series.index[-1]
        last_y = float(series.iloc[-1])
        label_points.append((benchmark, last_x, last_y, line.get_color()))

    ax.set_xscale("log", base=2)
    if log_y:
        ax.set_yscale("log")

    ax.set_xticks(x_values)
    ax.set_xticklabels([f"{int(x):,}" for x in x_values], rotation=30, ha="right")
    ax.set_xlabel("Prompt tokens")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True, which="both", axis="both")
    ax.set_xlim(min(x_values) * 0.85, max_x * 1.05)

    # Reserve room on the right for the label column (the longest recipe names
    # run ~50 characters). Fix the axes box first so the transforms below are
    # final before we measure where each line ends.
    margin_top, margin_bottom = 0.94, 0.09
    fig.subplots_adjust(left=0.05, right=0.74, top=margin_top, bottom=margin_bottom)

    # List the model names in a column to the right of the plot: ordered by
    # final value (highest at the top), stacked at normal line spacing, and
    # each joined to its series' last data point by a thin colour-matched
    # leader line.
    if label_points:
        label_points.sort(key=lambda item: item[2], reverse=True)
        n = len(label_points)

        # Axes-fraction height of each series' last data point (handles the
        # log/linear y-axis transparently via the finalised transforms).
        fig.canvas.draw()
        inv_axes = ax.transAxes.inverted()
        target_fracs = [
            float(inv_axes.transform(ax.transData.transform((px, py)))[1])
            for _bm, px, py, _color in label_points
        ]

        # One text line high (points -> axes fraction), shrinking only if the
        # whole stack would not otherwise fit in the plot height.
        axis_height_in = fig.get_figheight() * (margin_top - margin_bottom)
        spacing = (9 * 1.35 / 72.0) / axis_height_in
        lo, hi = 0.01, 0.99
        if n > 1 and spacing * (n - 1) > (hi - lo):
            spacing = (hi - lo) / (n - 1)

        # Slide the compact block to the offset that minimises total leader
        # length: label i wants block_top = target_i + i*spacing, and the
        # median of those values minimises the sum of absolute errors.
        block_top = statistics.median(
            [t + i * spacing for i, t in enumerate(target_fracs)]
        )
        block_top = min(block_top, hi)
        block_top = max(block_top, lo + spacing * (n - 1))

        for i, (benchmark, point_x, point_y, color) in enumerate(label_points):
            ax.annotate(
                benchmark,
                xy=(point_x, point_y),
                xycoords="data",
                xytext=(1.015, block_top - i * spacing),
                textcoords="axes fraction",
                va="center",
                ha="left",
                fontsize=9,
                color=color,
                arrowprops={
                    "arrowstyle": "-",
                    "lw": 0.7,
                    "color": color,
                    "alpha": 0.6,
                    "shrinkA": 0,
                    "shrinkB": 2,
                },
                annotation_clip=False,
            )

    return fig


def build_dataframes(reports: list[tuple[str, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    intel_rows = []
    speed_rows = []

    for filename, text in reports:
        benchmark = label_from_filename(filename)

        scores = parse_intelligence_scores(text)
        scores["benchmark"] = benchmark
        intel_rows.append(scores)

        for row in parse_speed_rows(text):
            row["benchmark"] = benchmark
            speed_rows.append(row)

    intel_df = pd.DataFrame(intel_rows).set_index("benchmark")
    intel_df = intel_df.reindex(columns=INTEL_METRICS).fillna(0.0)

    speed_df = pd.DataFrame(speed_rows)
    if not speed_df.empty:
        speed_df = speed_df[
            ["benchmark", "prompt_tokens", "ttft_s", "tpot_ms", "generation_tps"]
        ]

    return intel_df, speed_df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="mrpmorris/sparkrun-recipes")
    parser.add_argument("--ref", default="master")
    parser.add_argument("--path", default="benchmarks")
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--gradient", type=Path)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/_Comparison.pdf"))
    args = parser.parse_args()

    if args.input_dir:
        reports = load_local_markdown(args.input_dir)
    else:
        reports = fetch_github_markdown(args.repo, args.ref, args.path)

    if not reports:
        raise RuntimeError("No markdown benchmark reports found")

    intel_df, speed_df = build_dataframes(reports)
    cmap = make_score_cmap(args.gradient)

    with PdfPages(args.output) as pdf:
        fig = build_intelligence_figure(intel_df, cmap)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "ttft_s",
            "Sparkrun benchmark time to first token by prompt size",
            "TTFT seconds, log scale",
            log_y=True,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "tpot_ms",
            "Sparkrun benchmark TPOT by prompt size",
            "TPOT ms",
            log_y=False,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = build_line_figure(
            speed_df,
            "generation_tps",
            "Sparkrun benchmark TPS by prompt size",
            "TPS, generation tokens/s",
            log_y=False,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    print(args.output)


if __name__ == "__main__":
    main()
