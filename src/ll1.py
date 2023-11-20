from grammar_error import handle_error
from grammar_process import predict1
from src.ll1_handle import Stack, Tree
from predict import getPredict


class LL1:
    """
token_stack: 存储分析器要分析的token的栈。
sign_stack: 存储分析器分析到的符号的栈。
grammar: 存储分析器使用的文法。
predict, left, only_right: 存储分析器使用的预测分析表和相关信息。
TreePath: 存储分析生成的语法树路径。
left_row_mapping, table: 存储分析器使用的分析表。
sign_replace: 用于存储需要向符号栈中压入的符号，以便在分析程序错误时进行回溯。 因为被替换了 所以需要记录 signReplace
sign_replace_len: 用于存储需要从符号栈中弹出的符号的数量，以便在分析程序错误时进行回溯。
token_replace: 用于存储需要向记号栈中压入的记号，以便在分析程序错误时进行回溯。
    """

    def __init__(self, grammarPath, tokenPath, TreePath):
        self.token_stack = Stack()
        self.sign_stack = Stack()
        self.grammar = []
        self.predict, self.left, self.only_right = getPredict()
        self.TreePath = TreePath
        with open(grammarPath) as file:
            lines = file.readlines()
            for line in lines:
                line = str(line).replace("\n", "")
                pos = line.split(" ", 20)
                x = {'left': pos[0], 'right': pos[2:]}
                self.grammar.append(x)
        with open(tokenPath) as file:
            lines = file.readlines()
            nums = len(lines)
            for i in range(nums):
                # 因为是栈所以从最后一行开始push
                line = lines[nums - i - 1]
                line = str(line).replace("\n", "")
                pos = line.split(" ", 20)
                self.token_stack.push(pos)
        self.sign_stack.push('Program')
        # 建立分析表
        self.left_row_mapping, self.table = self.create_analysis_table(self.predict, self.grammar, self.only_right)
        print("分析表:")
        for sign in self.left:  # 如果是非终极符，则用语法进行替换
            row = self.left_row_mapping[sign]
            # 产生式编号
            print(f"sign:{sign}",end="")
            print(self.table[row])
        self.handle_error = handle_error(self.left, self.left_row_mapping, self.table, self.grammar)
        self.errImag = []
        self.runJudge = False
        self.sign_replace = Stack()
        self.sign_replace_len = Stack()
        self.token_replace = Stack()

    # 分析表建立函数
    def create_analysis_table(self, predict, grammar, only_right):
        """
        根据给定的文法预测分析表，生成语法分析表的行和列。
        :param predict: 预测表，即可以根据当前的文法符号和下一个token推出下一步的推导。
        :param grammar: 文法规则。
        :param only_right: 只出现在右边的文法符号集合。
        :return: 语法分析表的行和列。

        """
        pre = ''  # 记录上一个处理过的左部符号
        num = 0  # 行号
        left_row_mapping = {}  # 存储每个非终结符对应的行号
        table = []  # 存储语法分析表每一行的内容
        for i in range(len(grammar)):
            if grammar[i]['left'] != pre:  # 新的非终结符
                left_row_mapping[grammar[i]['left']] = num  # 设置行号
                num += 1
                x = {}
                for j in only_right:  # 初始化列
                    x[j] = -1  # 表示该位置无法匹配
                for g in predict[i + 1]:  # 处理左端无相同的文法,i+1是因为pridict从1开始记录的
                    x[g] = i  # 根据预测表填写该行
                table.append(x)
                pre = grammar[i]['left']
            else:  # 已经处理过该左部符号，填写列即可,不需要填写mapping
                row = left_row_mapping[grammar[i]['left']]
                for g in predict[i + 1]:
                    table[row][g] = i
        return left_row_mapping, table

    # LL1核心程序
    def run(self):
        """
        将当前分析的符号和当前要分析的token进行匹配，如果当前符号是非终结符，则使用语法进行替换；
        如果当前符号是终结符，则将符号栈和token栈弹出匹配。如果无法匹配，则会调用handle_error方法分析错误，
        生成相应的错误信息，并退出分析程序。当分析完全部的token后，该
        方法会输出语法树的生成结果以及可能的语法错误信息。
        """
        syntax_tree = Tree()
        pre_node = syntax_tree.root
        while not self.sign_stack.isEmpty() and self.token_stack.peek()[2] != 'EOF':
            # 分析栈
            sign = self.sign_stack.peek()
            # 输入流
            toke = self.token_stack.peek()
            """这样的设计是为了将 token 的种类（type）映射为更易读的文本形式。在这段代码中，如果 toke[1] 的值为 'ID'、'INTC' 或 'CHARC'，那么将 token 的值赋为 
            'ID'、'INTC' 或 'CHARC'，分别代表标识符、整型常量和字符常量。如果不是这三种情况，那么将 token 的值设置为 toke[2]，即该 token 
            对应的字符串。这样做的目的是为了后面代码的可读性和易维护性，而不是用数字代表不同类型的 token。"""
            if toke[1] == 'ID':
                token = 'ID'
            elif toke[1] == 'INTC':
                token = 'INTC'
            elif toke[1] == 'CHARC':
                token = 'CHARC'
            else:
                token = toke[2]
            if sign in self.left:  # 如果是非终极符，则用语法进行替换
                row = self.left_row_mapping[sign]
                # 产生式编号
                judge = self.table[row][token]
                if judge != -1:
                    # 因为被替换了 所以需要记录 signReplace
                    self.sign_replace.push(self.sign_stack.pop())
                    self.token_replace.push(['', 'back', ''])
                    rig = self.grammar[judge]['right']
                    length = len(rig)
                    # 记录被替换的多长
                    self.sign_replace_len.push(length)
                    for i in range(length):
                        if rig[length - 1 - i] != 'NULL':
                            # 替换
                            self.sign_stack.push(rig[length - 1 - i])
                    pre_node = predict1(judge + 1, syntax_tree, toke, pre_node)
                else:  # 无法匹配 记录后退出循环
                    err_imag = self.handle_error.run(self.sign_stack, self.token_stack, self.sign_replace, self.sign_replace_len,
                                                    self.token_replace)
                    err = {'line': 0, 'message': ' '}
                    err['line'] = int(toke[0])
                    line_add1 = ['常量', ';']
                    """
                    如果错误消息中包含某些关键词，比如“常量”和“;”，那么需要通过加1来调整错误所在的行号。
                    这是因为这些关键词通常出现在语句的末尾，而错误可能实际上是在下一行。
                    因此，如果错误消息包含这些关键词，实现会假设错误实际上是在下一行，通过加1来调整行号。
                    """
                    judge_add1 = True
                    for i in range(len(line_add1)):
                        if line_add1[i] in err_imag:
                            judge_add1 = False
                            break
                    if judge_add1:
                        err['line'] += 1
                    err['message'] = err_imag
                    self.errImag.append(err)
                    break
            else:  # 是终极符
                if sign == token:  # 相等则进行匹配
                    self.sign_replace.push(self.sign_stack.pop())
                    self.sign_replace_len.push(0)
                    self.token_replace.push(self.token_stack.pop())
                else:  # 不相等出错 也跳出循环处理
                    err_imag = self.handle_error.run(self.sign_stack, self.token_stack, self.sign_replace, self.sign_replace_len,
                                                    self.token_replace)
                    err = {'line': 0, 'message': ' '}
                    err['line'] = int(toke[0])
                    line_add1 = ['常量', ';']
                    judge_add1 = True
                    for i in range(len(line_add1)):
                        if line_add1[i] in err_imag:
                            judge_add1 = False
                            break
                    if judge_add1:
                        err['line'] += 1
                    err['message'] = err_imag
                    self.errImag.append(err)
                    break
        # 循环结束 还没有把输入流处理完毕
        if self.token_stack.peek()[2] != 'EOF':
            if len(self.errImag) == 0:
                err = {'line': 0, 'message': ' '}
                err['line'] = int(self.token_stack.peek()[0])
                err['message'] = '符号栈仍有残余'
                self.errImag.append(err)
        else:
            self.runJudge = True
        syntax_tree.write_to_file(self.TreePath)
        self.syntax_tree = syntax_tree

    def show_error(self, show=False):
        if show:
            if self.runJudge:
                print('语法树生成成功，可以继续运行')
            else:
                err_msg = "有语法错误，语法树生成失败，不可继续运行\n"
                print('有语法错误，语法树生成失败，不可继续运行')
            for i in range(len(self.errImag)):
                err_msg = err_msg+f"line:{self.errImag[i]['line']} {self.errImag[i]['message']}\n"
                with open("../intermediate/error.txt", "w") as file:
                    file.write(err_msg)
        if len(self.errImag) > 0:
            return -1, self.errImag
        return 0, self.errImag
