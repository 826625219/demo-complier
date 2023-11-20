# 定义栈
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class Node:
    """
    Node类用于表示语法树的一个节点，包括节点的类型nodeKind、子节点列表child、兄弟节点Sibling、
    父节点father、行号Lineno、节点类型kind、标识符个数idnum、
    标识符名称name和属性attr等。其中属性attr是一个包含三个字典的列表，用于存储节点的属性信息。
    另外，还有一个judge属性用于标记当前节点是否为一个声明节点。
    """

    def __init__(self, nodeKind, line_no=-1, judge=False):
        self.nodeKind = nodeKind
        self.child = []
        self.Sibling = None
        self.father = None
        self.line_no = line_no
        self.kind = {'dec': ' ', 'stmt': ' ', 'exp': ' '}
        self.idnum = 0  # 一个节点中的标识符的个数
        self.name = []
        ArrayAttr = {'low': 0, 'up': 0, 'childType': ' '}
        procAttr = {'paramt': ' '}
        ExpAttr = {'op': ' ', 'val': 0, 'varkind': ' ', 'type': ' '}
        attr = []
        attr.append(ArrayAttr)
        attr.append(procAttr)
        attr.append(ExpAttr)
        self.attr = attr
        self.judge = judge


class Tree(object):
    """
    Tree类用于表示整个语法树，包含根节点root、节点栈stack、行号栈NumStack和符号栈SignStack等。
    其中，节点栈用于保存当前正在访问的节点，行号栈用于保存当前节点所在行号，符号栈用于保存当前节点的符号类型。
    另外，还有一些用于标记语法分析的变量，如getExpResult、getExpResult2和expflag等。
    """

    def __init__(self):
        root = Node('ProK', line_no=0, judge=True)
        self.root = root
        self.stack = Stack()
        self.NumStack = Stack()
        self.SignStack = Stack()
        # 语法规则使用时用到
        self.getExpResult = True
        self.getExpResult2 = True
        self.expflag = 0
        # 默认每一个ProK都有这三个子结构
        self.root.child.append(Node('PheadK'))
        self.root.child.append(Node('TypeK'))
        self.root.child.append(Node('StmLK'))
        self.stack.push(self.root.child[2])
        self.stack.push(self.root.child[1])
        self.stack.push(self.root.child[0])

    def write_to_file(self, TreePath, priJudge=False):
        """
        生成语法树
        根节点默认有三个child :PheadK，TypeK，StmLK
        line_no=-1，表示先占位，如果发现里面没内容会删去，不会写入语法树文件中
        先根 然后处理儿子 最后兄弟节点
        根据节点当前属性 填充前面空格
        """
        stack1 = Stack()  # 初始化栈，用于遍历语法树
        stack1.push(self.root)  # 将根节点压入栈中
        stackLine = Stack()  # 初始化栈，用于记录节点所在行数
        stackLine.push(0)  # 将根节点所在行数压入栈中

        with open(TreePath, "w") as file:  # 打开指定路径的文件，并以写入模式打开
            while not stack1.isEmpty():  # 如果栈不为空，循环遍历
                node = stack1.pop()  # 将栈顶节点弹出
                # print(node.line_no)
                Line = stackLine.pop()  # 将节点所在行数弹出
                stm = ''  # 初始化节点信息字符串
                if Line > 0:  # 如果节点不是根节点，则需要添加缩进
                    for i in range(Line):
                        stm += '   '
                if node.nodeKind != 'ProcK':  # 根据节点类型添加节点信息到节点信息字符串中
                    stm += node.nodeKind
                else:
                    stm += 'ProcDecK'
                stm = stm + ' ' + str(node.line_no)
                if node.nodeKind == 'DecK':
                    if node.attr[1]['paramt'] != ' ':
                        stm = stm + ' ' + node.attr[1]['paramt']
                    stm = stm + ' ' + node.kind['dec']
                    if node.kind['dec'] == 'ArrayK':
                        stm = stm + ' ' + str(node.attr[0]['low']) + ' ' + str(node.attr[0]['up']) + ' ' + node.attr[0][
                            'childType']
                elif node.nodeKind == 'StmtK':
                    stm = stm + ' ' + node.kind['stmt']
                elif node.nodeKind == 'ExpK':
                    stm = stm + ' ' + node.kind['exp']
                    if node.attr[2]['varkind'] != ' ':
                        stm = stm + ' ' + node.attr[2]['varkind']
                for i in range(node.idnum):
                    stm = stm + ' ' + str(node.name[i])
                b = ['TypeK', 'VarK', 'ProcK']
                if node.judge or ((not node.judge) and (node.nodeKind in b)):  # 根据节点类型和judge属性决定是否写入节点信息到文件中
                    if priJudge and node.line_no != -1:
                        print(stm)  # 如果priJudge为True，则在控制台打印节点信息
                    stm += '\n'
                    if node.line_no == -1:
                        a = 10
                    else:
                        file.write(stm)  # 将节点信息写入文件中
                if node.Sibling != None:  # 如果节点有兄弟节点，则将其压入栈中
                    if not (node.nodeKind == 'ProcDecK' and node.Sibling.nodeKind == 'ProcDecK' and (
                            not node.Sibling.judge)):
                        stack1.push(node.Sibling)
                        stackLine.push(Line)
                num = len(node.child)  # 获取节点的子节点数量
                if num > 0:  # 如果有子节点，则将子节点压入栈中，并记录其所在行数
                    for i in range(num):
                        stack1.push(node.child[num - 1 - i])
                        stackLine.push(Line + 1)
