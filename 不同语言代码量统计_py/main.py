import os


def count_py_files(directory):
    """递归统计给定目录下所有代码文件的数量"""
    code_cout = {".py": 0, ".ipynb": 0, ".sql": 0,
                 ".java": 0, ".scala": 0, ".cpp": 0,
                 ".h": 0, ".rs": 0, "CMakeLists.txt": 0}
    for root, dirs, files in os.walk(directory):
        for file in files:
            for k in code_cout.keys():
                if file.endswith(k):
                    code_cout[k] += 1

    return {key: value for key, value in code_cout.items() if value != 0}


print("MLNote:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\MLBase'))
print("CPPStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\CPPStudy'))
print("SQLStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\SQLStudy'))
print("JavaScalaStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\JavaScalaStudy'))
print("RustStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\RustStudy'))
print("OtherStudy:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\OtherStudy'))
print("PyDevelopment:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\PyDevelopment'))
print("Algorithms:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\Algorithms'))
print("Script:", count_py_files(r'C:\Users\duanm\Music\GitHubProjects\Script'))
