import os
from subprocess import Popen, PIPE, STDOUT

"""
这段代码的主要作用是调用一个名为 recursion.cpp 的 C++ 程序，并通过标准输入（stdin）向该程序传递名为 token_path 的文件路径。
这个 C++ 程序会对该文件中的词法单元序列进行递归下降语法分析，并输出相应的语法分析树。

首先，该函数使用 g++ 编译 recursion.cpp，并将其生成的可执行文件命名为 work。
然后，通过 Popen 函数调用该可执行文件，并使用 stdout 捕获该程序的标准输出。
接下来，该函数遍历 stdout 中的每一行，并将其打印到控制台上。
最后，该函数等待程序执行结束，并返回相应的退出码，若返回值为0则表示程序执行成功，否则执行失败。
"""


def recurse(token_path):
    # print(os.getcwd())

    err = os.system("g++ -std=c++11 ./recursion.cpp -o recurse")
    if err != 0:
        print("c++ 环境加载失败")
        return -1
    process = Popen('recurse', stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            print(line.decode('gbk', 'ignore').strip())
    exitcode = process.wait()
    if exitcode != 0:
        return -1
    return 0


if __name__ == '__main__':
    print(recurse("../intermediate/token.txt"))
