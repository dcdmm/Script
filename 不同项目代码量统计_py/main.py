import os
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Final, TypeAlias
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from matplotlib.patches import Patch
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
    ".html",
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
    ".html": "#E34F26",
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
DISPLAY_DPI: Final = 160
EXPORT_DPI: Final = 300


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


def _draw_project_share_donut(
        ax,
        project_counts: Mapping[str, Mapping[str, int]],
) -> None:
    """绘制各项目源码文件数量占比的空心饼图。"""
    project_totals = {
        project: sum(counts.values())
        for project, counts in project_counts.items()
    }
    projects = sorted(
        project_totals,
        key=lambda project: (-project_totals[project], project.casefold()),
    )
    total_source_files = sum(project_totals.values())

    color_map = plt.get_cmap("tab20")
    project_colors = {
        project: color_map(index % color_map.N)
        for index, project in enumerate(sorted(projects, key=str.casefold))
    }

    ax.set_facecolor(SURFACE_COLOR)
    ax.set_title(
        "各项目源码文件占比",
        loc="left",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=28,
    )
    ax.text(
        0,
        1.015,
        "项目源码文件数 ÷ 全部项目源码文件数",
        transform=ax.transAxes,
        color=MUTED_COLOR,
        fontsize=9,
    )

    if total_source_files:
        visible_projects = [
            project for project in projects if project_totals[project] > 0
        ]
        wedges, _, percentage_labels = ax.pie(
            [project_totals[project] for project in visible_projects],
            colors=[project_colors[project] for project in visible_projects],
            startangle=90,
            counterclock=False,
            radius=0.82,
            center=(0, 0.18),
            wedgeprops={
                "width": 0.32,
                "edgecolor": SURFACE_COLOR,
                "linewidth": 2,
            },
            autopct=lambda percentage: (
                f"{percentage:.1f}%" if percentage >= 4 else ""
            ),
            pctdistance=0.79,
            textprops={
                "color": TEXT_COLOR,
                "fontsize": 9,
                "fontweight": "bold",
            },
        )
        for wedge, percentage_label in zip(
                wedges,
                percentage_labels,
                strict=True,
        ):
            percentage_label.set_color(
                _get_contrasting_text_color(to_hex(wedge.get_facecolor()))
            )
    else:
        ax.pie(
            [1],
            colors=[ROW_BAND_COLOR],
            startangle=90,
            radius=0.82,
            center=(0, 0.18),
            wedgeprops={
                "width": 0.32,
                "edgecolor": SURFACE_COLOR,
                "linewidth": 2,
            },
        )

    ax.text(
        0,
        0.23,
        f"{total_source_files:,}",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color=TEXT_COLOR,
    )
    ax.text(
        0,
        0.08,
        "源码文件",
        ha="center",
        va="center",
        fontsize=9,
        color=MUTED_COLOR,
    )

    legend_handles = []
    for project in projects:
        count = project_totals[project]
        percentage = count / total_source_files if total_source_files else 0
        legend_handles.append(
            Patch(
                facecolor=project_colors[project],
                edgecolor="none",
                label=f"{project}  {count:,} · {percentage:.1%}",
            )
        )

    if legend_handles:
        legend = ax.legend(
            handles=legend_handles,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=2,
            frameon=False,
            labelcolor=TEXT_COLOR,
            fontsize=8.5,
            columnspacing=1.2,
            handlelength=1.2,
            handletextpad=0.6,
            labelspacing=0.85,
        )
        legend.set_zorder(5)

    ax.set_aspect("equal")
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def show_source_file_chart(
        project_counts: Mapping[str, Mapping[str, int]],
) -> None:
    """用堆叠柱状图和空心饼图展示各项目的源码文件数量"""
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = DISPLAY_DPI
    plt.rcParams["savefig.dpi"] = EXPORT_DPI

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

    fig = plt.figure(
        figsize=(18, 8.8),
        dpi=DISPLAY_DPI,
        facecolor=BACKGROUND_COLOR,
    )
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=(2.4, 1),
        wspace=0.14,
    )
    ax = fig.add_subplot(grid[0, 0])
    share_ax = fig.add_subplot(grid[0, 1])
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

    if visible_types:
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

    _draw_project_share_donut(share_ax, project_counts)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.84, bottom=0.23)

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
