import os
import subprocess

import matplotlib.pyplot as plt

SOURCE_SUFFIXES = (
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

PROJECTS = {
    "LLM": r"C:\Users\duanm\Music\GitHubProjects\LLM",
    "MLBase": r"C:\Users\duanm\Music\GitHubProjects\MLBase",
    "PyDevelopment": r"C:\Users\duanm\Music\GitHubProjects\PyDevelopment",
    "RustStudy": r"C:\Users\duanm\Music\GitHubProjects\RustStudy",
    "FrontendStudy": r"C:\Users\duanm\Music\GitHubProjects\FrontendStudy",
    "CPPStudy": r"C:\Users\duanm\Music\GitHubProjects\CPPStudy",
    "OtherStudy": r"C:\Users\duanm\Music\GitHubProjects\OtherStudy",
    "JavaScalaStudy": r"C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy",
    "SQLStudy": r"C:\Users\duanm\Music\GitHubProjects\SQLStudy",
}


def count_git_source_files(directory):
    """统计已经纳入Git版本控制的源码文件数量"""
    try:
        repository = os.path.abspath(directory)
        result = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repository}",
                "-C",
                repository,
                "ls-files",
                "-z",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("未找到 git 命令，请先安装 Git 并加入 PATH") from exc
    except subprocess.CalledProcessError as exc:
        error = exc.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"无法读取 Git 仓库 {directory}: {error}") from exc

    counts = {suffix: 0 for suffix in SOURCE_SUFFIXES}
    counts["CMakeLists.txt"] = 0

    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue

        filename = os.path.basename(os.fsdecode(raw_path))
        if filename == "CMakeLists.txt":
            counts["CMakeLists.txt"] += 1
            continue

        suffix = os.path.splitext(filename)[1].lower()
        if suffix in counts:
            counts[suffix] += 1

    return {file_type: count for file_type, count in counts.items() if count}


def show_source_file_chart(project_counts):
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
    max_total = max(totals, default=1)

    color_map = plt.colormaps["tab20"]
    fig, ax = plt.subplots(figsize=(15, 8))
    left = [0] * len(sorted_projects)

    for index, source_type in enumerate(visible_types):
        values = [
            project_counts[project].get(source_type, 0)
            for project in sorted_projects
        ]
        bars = ax.barh(
            sorted_projects,
            values,
            left=left,
            height=0.62,
            label=source_type,
            color=color_map(index / max(1, len(visible_types) - 1)),
        )

        for bar, count in zip(bars, values):
            if count >= max_total * 0.025:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    str(count),
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=9,
                    fontweight="bold",
                )

        left = [current + value for current, value in zip(left, values)]

    for project, total in zip(sorted_projects, totals):
        ax.text(
            total + max_total * 0.01,
            project,
            f"合计 {total}",
            va="center",
            fontsize=10,
        )

    ax.set_xlim(0, max_total * 1.12)
    ax.set_xlabel("源码文件数")
    ax.set_ylabel("项目")
    ax.set_title("各项目 Git 源码文件数量对比", fontsize=18, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(
        title="源码类型",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=min(7, len(visible_types)),
        frameon=False,
    )
    fig.tight_layout()
    plt.show()


def main():
    project_counts = {}
    for project, directory in PROJECTS.items():
        counts = count_git_source_files(directory)
        project_counts[project] = counts
        print(f"{project}: {counts}")

    show_source_file_chart(project_counts)


if __name__ == "__main__":
    main()
