import os
import pathspec


def load_gitignore(directory):
    """加载目录下的.gitignore文件,返回pathspec对象"""
    gitignore_path = os.path.join(directory, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            patterns = f.read().splitlines()
    patterns.append('.git/')  # 默认忽略.git目录
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)


def count_py_files(directory):
    """递归统计给定目录下所有代码文件的数量(忽略.gitignore中的内容)"""
    code_cout = {".py": 0, ".ipynb": 0, ".sql": 0,
                 ".java": 0, ".scala": 0, ".cpp": 0,
                 ".h": 0, ".rs": 0, "CMakeLists.txt": 0}
    spec = load_gitignore(directory)
    for root, dirs, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        if rel_root == '.':
            rel_root = ''
        dirs[:] = [d for d in dirs if not spec.match_file(
            os.path.join(rel_root, d, '').replace('\\', '/') if rel_root else d + '/'
        )]
        for file in files:
            rel_file = os.path.join(rel_root, file).replace('\\', '/') if rel_root else file
            if spec.match_file(rel_file):  # 跳过gitignore中指定的文件
                continue

            for k in code_cout.keys():
                if file.endswith(k):
                    code_cout[k] += 1
    return {key: value for key, value in code_cout.items() if value != 0}


# 加油学习!
print("MLBase:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\MLBase'))
print("LLM:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\LLM'))
print("PyDevelopment:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\PyDevelopment'))
print("Algorithms:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\Algorithms'))
print("RustStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\RustStudy'))
print("CPPStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\CPPStudy'))
print("OtherStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\OtherStudy'))
print("JavaScalaStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy'))
print("SQLStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\SQLStudy'))
print("Script:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\Script'))
