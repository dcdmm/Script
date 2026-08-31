import os
import subprocess


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
    ".jsx"
)


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


# 加油学习!
print("LLM:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\LLM'))
print("MLBase:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\MLBase'))
print("PyDevelopment:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\PyDevelopment'))
print("RustStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\RustStudy'))
print("FrontendStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\FrontendStudy'))
print("CPPStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\CPPStudy'))
print("OtherStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\OtherStudy'))
print("JavaScalaStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy'))
print("SQLStudy:", count_git_source_files(r'C:\Users\duanm\Music\GitHubProjects\SQLStudy'))
