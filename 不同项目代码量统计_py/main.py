import os
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Final, TypeAlias
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

SourceCounts: TypeAlias = dict[str, int]
ProjectCounts: TypeAlias = dict[str, SourceCounts]

SOURCE_SUFFIXES: Final[tuple[str, ...]] = (
    ".py",
    ".ipynb",
    ".sql",
    ".java",
    ".scala",
    ".cpp",
    ".h",
    ".rs",
    ".ts",
    ".tsx",
    ".css",
    ".js",
    ".jsx",
)

PROJECTS: Final[dict[str, Path]] = {
    "LLM": Path(r"C:\Users\duanm\Music\GitHubProjects\LLM"),
    "MLBase": Path(r"C:\Users\duanm\Music\GitHubProjects\MLBase"),
    "PyDevelopment": Path(
        r"C:\Users\duanm\Music\GitHubProjects\PyDevelopment"
    ),
    "RustStudy": Path(r"C:\Users\duanm\Music\GitHubProjects\RustStudy"),
    "FrontendStudy": Path(
        r"C:\Users\duanm\Music\GitHubProjects\FrontendStudy"
    ),
    "CPPStudy": Path(r"C:\Users\duanm\Music\GitHubProjects\CPPStudy"),
    "OtherStudy": Path(r"C:\Users\duanm\Music\GitHubProjects\OtherStudy"),
    "JavaScalaStudy": Path(
        r"C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy"
    ),
    "SQLStudy": Path(r"C:\Users\duanm\Music\GitHubProjects\SQLStudy"),
}

SOURCE_COLORS: Final[dict[str, str]] = {
    ".py": "#3776AB",
    ".ipynb": "#F37626",
    ".sql": "#336791",
    ".java": "#E76F00",
    ".scala": "#DC322F",
    ".cpp": "#00599C",
    ".h": "#659AD2",
    ".rs": "#A6531B",
    ".ts": "#3178C6",
    ".tsx": "#087EA4",
    ".css": "#663399",
    ".js": "#E7C500",
    ".jsx": "#149ECA",
    "CMakeLists.txt": "#064F8C",
}

TEXT_COLOR: Final = "#172033"
MUTED_COLOR: Final = "#64748B"
GRID_COLOR: Final = "#D7DEE8"
BACKGROUND_COLOR: Final = "#F5F7FB"
ROW_BAND_COLOR: Final = "#EAF0F7"
SURFACE_COLOR: Final = "#FFFFFF"
BORDER_COLOR: Final = "#DCE3ED"


def count_git_source_files(directory: str | os.PathLike[str]) -> SourceCounts:
    """统计已经纳入 Git 版本控制的源码文件数量"""
    try:
        repository = Path(directory).resolve()
        result: subprocess.CompletedProcess[bytes] = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repository}",
                "-C",
                str(repository),
                "ls-files",
                "-z",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("未找到 git 命令，请先安装 Git 并加入 PATH") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr
        error = (
            stderr.decode(errors="replace").strip()
            if isinstance(stderr, bytes)
            else str(stderr or "").strip()
        )
        raise RuntimeError(f"无法读取 Git 仓库 {directory}: {error}") from exc

    counts = {suffix: 0 for suffix in SOURCE_SUFFIXES}
    counts["CMakeLists.txt"] = 0

    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue

        filename = Path(os.fsdecode(raw_path)).name
        if filename == "CMakeLists.txt":
            counts["CMakeLists.txt"] += 1
            continue

        suffix = os.path.splitext(filename)[1].lower()
        if suffix in counts:
            counts[suffix] += 1

    return {file_type: count for file_type, count in counts.items() if count}


def _get_contrasting_text_color(background_color: str) -> str:
    """根据背景色亮度选择易读的标签文字颜色"""
    hex_color = background_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 255
    return TEXT_COLOR if luminance > 0.62 else "#FFFFFF"


def show_source_file_chart(
        project_counts: Mapping[str, Mapping[str, int]],
) -> None:
    """用一张堆叠柱状图比较各项目的源码文件数量。"""
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    all_types = [*SOURCE_SUFFIXES, "CMakeLists.txt"]
    visible_types = [
        source_type
        for source_type in all_types
        if any(counts.get(source_type, 0) for counts in project_counts.values())
    ]
    sorted_projects = sorted(
        project_counts,
        key=lambda project: sum(project_counts[project].values()),
    )
    totals = [sum(project_counts[project].values()) for project in sorted_projects]
    max_total = max(max(totals, default=0), 1)
    type_counts = [
        sum(
            project_counts[project].get(source_type, 0) > 0
            for source_type in visible_types
        )
        for project in sorted_projects
    ]

    fig, ax = plt.subplots(figsize=(15, 8.2), facecolor=BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)
    y_positions = list(range(len(sorted_projects)))
    left = [0 for _ in sorted_projects]

    for row_index, y_position in enumerate(y_positions):
        if row_index % 2 == 0:
            ax.axhspan(
                y_position - 0.43,
                y_position + 0.43,
                color=ROW_BAND_COLOR,
                zorder=0,
            )

    for source_type in visible_types:
        values = [
            project_counts[project].get(source_type, 0)
            for project in sorted_projects
        ]
        bars = ax.barh(
            y_positions,
            values,
            left=left,
            height=0.62,
            label=source_type,
            color=SOURCE_COLORS[source_type],
            edgecolor=BACKGROUND_COLOR,
            linewidth=1,
            zorder=3,
        )

        label_color = _get_contrasting_text_color(SOURCE_COLORS[source_type])
        for bar, count, type_count in zip(
                bars,
                values,
                type_counts,
                strict=True,
        ):
            if type_count > 1 and count >= max_total * 0.018:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{count:,}",
                    ha="center",
                    va="center",
                    color=label_color,
                    fontsize=9,
                    fontweight="bold",
                    zorder=4,
                )

        left = [
            current + value
            for current, value in zip(left, values, strict=True)
        ]

    for y_position, total in zip(y_positions, totals, strict=True):
        ax.text(
            total + max_total * 0.01,
            y_position,
            f"{total:,}",
            va="center",
            fontsize=10,
            color=TEXT_COLOR,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": SURFACE_COLOR,
                "edgecolor": BORDER_COLOR,
                "linewidth": 0.8,
            },
            zorder=5,
        )

    ax.set_xlim(0, max_total * 1.12)
    ax.set_yticks(y_positions, labels=sorted_projects)
    ax.set_xlabel("Git 跟踪的源码文件数", color=MUTED_COLOR, labelpad=12)
    ax.set_ylabel("")
    ax.set_title(
        "各项目源码文件数量对比",
        loc="left",
        fontsize=20,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=34,
    )
    ax.text(
        0,
        1.025,
        f"共 {len(sorted_projects)} 个项目 · {sum(totals):,} 个源码文件 · 按总量升序排列",
        transform=ax.transAxes,
        color=MUTED_COLOR,
        fontsize=10,
    )
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)
    for spine_name in ("top", "right", "left", "bottom"):
        ax.spines[spine_name].set_visible(False)
    ax.tick_params(axis="x", colors=MUTED_COLOR, length=0, pad=8)
    ax.tick_params(axis="y", colors=TEXT_COLOR, length=0, pad=10, labelsize=10)
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    totals_descending = sorted(totals, reverse=True)
    second_largest = totals_descending[1] if len(totals_descending) > 1 else 0
    has_right_side_space = second_largest < max_total * 0.55

    if has_right_side_space:
        legend = ax.legend(
            title="源码类型",
            loc="center left",
            bbox_to_anchor=(0.48, 0.39),
            ncol=2,
            frameon=True,
            labelcolor=TEXT_COLOR,
            fontsize=9,
            title_fontsize=10,
            columnspacing=1.6,
            handlelength=1.4,
            handletextpad=0.7,
            labelspacing=0.9,
            borderpad=1,
        )
        legend.get_frame().set_facecolor(SURFACE_COLOR)
        legend.get_frame().set_edgecolor(BORDER_COLOR)
        legend.get_frame().set_linewidth(0.8)
        legend.get_title().set_color(TEXT_COLOR)
        fig.subplots_adjust(left=0.15, right=0.97, top=0.84, bottom=0.12)
    else:
        legend = ax.legend(
            title="源码类型",
            loc="upper center",
            bbox_to_anchor=(0.5, -0.14),
            ncol=min(7, len(visible_types)),
            frameon=False,
            labelcolor=TEXT_COLOR,
            columnspacing=1.4,
            handlelength=1.2,
        )
        legend.get_title().set_color(TEXT_COLOR)
        fig.subplots_adjust(left=0.15, right=0.97, top=0.84, bottom=0.23)

    plt.show()


def main() -> None:
    project_counts: ProjectCounts = {}
    for project, directory in PROJECTS.items():
        counts = count_git_source_files(directory)
        project_counts[project] = counts
        print(f"{project}: {counts}")

    show_source_file_chart(project_counts)


if __name__ == "__main__":
    main()
