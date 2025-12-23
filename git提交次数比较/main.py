import subprocess
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 自定义颜色列表
custom_colors = [
    '#d62728',  # tab:red
    '#ff7f0e',  # tab:orange
    '#e377c2',  # tab:pink
    '#9467bd',  # tab:purple
    '#bcbd22',  # tab:olive
    '#2ca02c',  # tab:green
    '#17becf',  # tab:cyan
    '#1f77b4',  # tab:blue
    '#8c564b',  # tab:brown
    '#7f7f7f',  # tab:gray
    '#aec7e8',  # light blue
    '#ffbb78',  # light orange
    '#98df8a',  # light green
    '#ff9896',  # light red
    '#c5b0d5',  # light purple
    '#c49c94',  # light brown
    '#f7b6d2',  # light pink
    '#dbdb8d',  # light olive
    '#9edae5',  # light cyan
    '#ad494a',  # dark red
    '#8c6d31',  # dark yellow
]

projects = {"MLBase": r'C:\Users\duanm\Music\GitHubProjects\MLBase',
            "LLM": r'C:\Users\duanm\Music\GitHubProjects\LLM',
            "PyDevelopment": r'C:\Users\duanm\Music\GitHubProjects\PyDevelopment',
            "Algorithms": r'C:\Users\duanm\Music\GitHubProjects\Algorithms',
            "RustStudy": r'C:\Users\duanm\Music\GitHubProjects\RustStudy',
            "CPPStudy": r'C:\Users\duanm\Music\GitHubProjects\CPPStudy',
            "OtherStudy": r'C:\Users\duanm\Music\GitHubProjects\OtherStudy',
            "JavaScalaStudy": r'C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy',
            "SQLStudy": r'C:\Users\duanm\Music\GitHubProjects\SQLStudy',
            "Script": r'C:\Users\duanm\Music\GitHubProjects\Script'}


def get_total_commits(repo_path):
    """获取git仓库的总提交次数"""
    result = subprocess.run(
        ['git', 'rev-list', '--all', '--count'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    commit_count = int(result.stdout.strip())
    return commit_count


def plot_pie_chart(commit_counts):
    """绘制饼图"""
    labels, sizes = list(commit_counts.keys()), list(commit_counts.values())
    total = sum(sizes)
    plt.figure(figsize=(12, 6))

    # 项目数量超出颜色列表长度时循环使用
    colors = [custom_colors[i % len(custom_colors)] for i in range(len(labels))]

    threshold = 0.02  # 占比过小的项目在饼图上不显示标签(防止重叠)
    pie_labels = [label if size/total > threshold else '' for label, size in zip(labels, sizes)]

    def make_autopct(pct):
        return ('%1.1f%%' % pct) if pct/100 > threshold else ''

    wedges, texts, autotexts = plt.pie(sizes,
                                       labels=pie_labels,
                                       autopct=make_autopct,
                                       startangle=90,
                                       colors=colors,
                                       pctdistance=0.85,
                                       wedgeprops=dict(width=0.4, edgecolor='w'))

    plt.setp(autotexts, size=12, weight="bold")
    plt.setp(texts, size=12)
    plt.text(0, 0, f'Total Commits\n{total}', ha='center', va='center', fontsize=14, fontweight='bold')
    plt.title('各项目Git提交次数统计', fontsize=16)
    legend_labels = [f'{l}: {s} ({s/total:.1%})' for l, s in zip(labels, sizes)]
    plt.legend(wedges, legend_labels,
               title="项目详情",
               loc="center left",
               bbox_to_anchor=(1.09, 0, 0.5, 1))
    plt.tight_layout()


def plot_bar_chart(commit_counts):
    """绘制柱状图"""
    labels, sizes = list(commit_counts.keys()), list(commit_counts.values())
    plt.figure(figsize=(10, 6))

    colors = [custom_colors[i % len(custom_colors)] for i in range(len(labels))]

    bars = plt.bar(labels, sizes, color=colors)

    plt.title('各项目Git提交次数统计', fontsize=16)
    plt.xlabel('项目名', fontsize=14, fontweight='bold')
    plt.ylabel('提交次数', fontsize=12)
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    plt.tight_layout()


if __name__ == "__main__":
    print("正在统计各项目的Git提交次数...\n")
    commit_counts = {}
    for project_name, project_path in projects.items():
        commits = get_total_commits(project_path)
        commit_counts[project_name] = commits

    # 按提交次数从高到低排序
    sorted_commits = dict(sorted(commit_counts.items(), key=lambda x: x[1], reverse=True))
    for project_name, commits in sorted_commits.items():
        print(f"{project_name:20s}: {commits:5d} 次提交")

    total_commits = sum(commit_counts.values())
    print(f"\n{'='*40}")
    print(f"{'total':20s}: {total_commits:5d} 次提交")
    print(f"{'='*40}\n")

    plot_pie_chart(sorted_commits)
    plot_bar_chart(sorted_commits)
    plt.show()
