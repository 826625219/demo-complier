import copy
import json
import re
import sys  # 导入sys模块

sys.setrecursionlimit(3000)
error_flag = False


class Node:
    def __init__(self, line, val, deep):
        self.child = []
        self.val = val
        self.deep = deep
        self.line = str(line + 1)
        self.converse(val)

    def __str__(self):
        return str(self.__dict__)

    def print(self):
        print(str(json.dumps(self.__dict__)))

    def converse(self, val):
        """
        接收一个字符串参数val，将其拆分为单词并根据这些单词的值更新类实例的属性。
        该方法首先将输入字符串拆分为单词列表，并将第一个单词分配给nodeKind属性，将第二个单词加1后转换为字符串并分配给rawline属性。
        然后，它通过处理余下的单词来更新kind、id_num、name和attr等属性。这些属性的含义和用途在代码注释中有详细的说明。
        总体来说，这个方法是用来解析输入的字符串，并根据输入中包含的信息更新类实例的属性，以便在编译器的后续处理中使用这些属性。
        
        self.node_kind: 该属性表示节点的类型，用于标识节点的种类，比如“声明节点”、“语句节点”、“表达式节点”等。在编译器的后续处理中，根据节点的类型可以确定其具体的语义和处理方式
        self.raw_line: 该属性表示节点在源代码中的行号。在解析源代码时，可以通过该属性将抽象语法树中的节点与源代码中的相应行号对应起来，从而更方便地进行调试和错误定位。
        self.kind: 该属性表示节点的具体类型，与self.nodeKind不同，该属性更具体、更具有区分度，比如“变量声明”、“函数声明”、“赋值语句”等。在编译器的后续处理中，根据节点的具体类型可以更精确地确定其语义和处理方式。
        self.id_num: 该属性表示节点中标识符的个数，用于表示节点中有多少个标识符需要处理。标识符通常指变量、函数、常量等在源代码中具有名称和含义的实体。
        self.name: 该属性是一个列表，用于存储节点中的标识符名称。在编译器的后续处理中，可以通过遍历这个列表来获取节点中所有的标识符。
        self.attr: 该属性是一个字典，用于存储节点的其它属性，比如节点的数据类型、运算符类型、参数类型等
        """
        vals = val.split(" ")
        self.node_kind = vals[0]
        self.raw_line = str(int(vals[1]) + 1)
        # vals[1]是:=
        vals = vals[2:]

        self.kind = ""
        self.id_num = 0  # 一个节点中的标识符的个数
        self.name = []
        self.attr = {}

        # ProK, PheadK, TypeK, VarK, ProDecK, StmLK, DecK, Stmtk, ExpK
        if self.node_kind == 'DecK':  # 如果节点类型是声明节点
            if vals[0] == 'valparamType' or vals[0] == "varparamType":  # 如果节点是参数声明节点
                self.attr['paramt'] = vals[0]  # 将参数类型记录到属性中
                vals = vals[1:]  # 跳过参数类型
            self.kind = vals[0]  # 记录声明节点的具体类型
            vals = vals[1:]  # 跳过节点类型
            if self.kind == "IdK":  # 如果是变量或常量声明节点
                self.real_kind = vals[0]  # 记录变量/常量的具体类型
                vals = vals[1:]  # 跳过变量/常量类型
            # 如果是数组声明节点，记录数组的下界、上界和子类型
            if self.kind == 'ArrayK':
                self.attr['low'] = vals[0]
                self.attr['up'] = vals[1]
                self.attr['childType'] = vals[2]
                vals = vals[3:]  # 跳过下界、上界和子类型

        # 如果节点类型是语句节点
        elif self.node_kind == 'StmtK':
            # 记录语句节点的具体类型（赋值语句、条件语句、循环语句等）
            if vals[0] != "" or vals[0] != " ":
                self.kind = vals[0]
            vals = vals[1:]  # 跳过语句类型

        # 如果节点类型是表达式节点
        elif self.node_kind == 'ExpK':
            # 记录表达式节点的具体类型（运算符、常量、变量等）
            self.kind = vals[0]
            vals = vals[1:]  # 跳过表达式类型
            # 如果节点是变量节点，记录变量的具体类型（变量、数组、结构体成员等）
            if vals[0] in ("IdV", "ArrayMembV", "FieldMembV"):
                self.attr['varkind'] = vals[0]
                vals = vals[1:]  # 跳过变量类型
            # 如果节点是运算符节点，记录运算符的具体类型
            if self.kind == 'OpK':
                self.attr['op'] = vals[0]
            # 如果节点是常量节点，记录常量的值
            if self.kind == 'ConstK':
                self.attr['val'] = vals[0]

        # 处理余下的单词，将标识符名称加入name列表
        for x in vals:
            if x != "":
                self.id_num += 1  # 计算节点中标识符的个数
                self.name.append(x)  # 记录标识符名称

        # self.type_name = type_name


err_msg_file = ""


def error(*param):
    global error_flag, err_msg_file
    error_flag = True
    s = ""
    for x in param:
        if type(x) == "str":
            s += x
        else:
            s = s + str(x) + " "
    # print(f"\033[31m{s}\033[0m")
    print("line:" + s)
    err_msg_file = err_msg_file + "line:" + s + '\n'


def dfs(node):
    for x in node.child:
        print(node.val, "->", x.val)
    for x in node.child:
        dfs(x)


def generate_node(tree_path):
    """
    根据语法分析树的文本表示，构造出对应的语法分析树。它读取文本文件中的每一行，每一行代表树中的一个节点，
    并且节点的深度和在树中的位置可以根据行前面的空格数量计算得到。函数会遍历所有的节点，并将它们添加到它们在树中的深度所对应的节点列表中。
    如果某个节点是另一个节点的子节点，则会将它添加到父节点的child列表中。最后，函数返回树的根节点，即深度为0的节点。
    """
    # 初始化一个字典，键为树的深度，值为该深度的节点
    level_list = {}
    with open(tree_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            # 将每一行的末尾的换行符去掉
            line = lines[i].replace("\n", "")
            bn = 0
            j = 0
            # 计算该节点的深度,因为有前置空格
            for j in range(len(line)):
                if line[j] != " ":
                    break
                else:
                    bn += 1
            # 从没空格那取
            text = line[j:]
            # 三空格一个层次
            level = int(bn / 3)
            # 创建一个新节点，并将其添加到对应深度的节点列表中 每一层都只有一个节点
            node = Node(i, text, level)
            if level not in level_list:
                level_list[str(level)] = node
                if level > 0:
                    # 将该节点添加为其父节点的子节点
                    father_node = level_list[str(level - 1)]
                    father_node.child.append(node)
    # 返回深度为0的节点，即根节点
    # print(level_list)
    return level_list.get("0")


class DefaultKind:
    def __init__(self, kind):
        self.kind = kind


class Kind:
    def __init__(self, node, body=None):
        self.kind = node.kind
        self.size = 0
        if node.kind == 'ArrayK':
            indexTy = {"low": node.attr["low"], "up": node.attr["up"]}
            elemTy = Kind(DefaultKind(node.attr["childType"])).__dict__
            self.arrayAttr = {"indexTy": indexTy, "elemTy": elemTy}
            self.size = elemTy["size"] * (int(node.attr["up"]) - int(node.attr["low"]))
            self.arrayKind = elemTy["kind"]
        if node.kind == 'RecordK':
            for x in body:
                self.size += x.size
        if node.kind == 'IntegerK':
            self.size = 2
        if node.kind == 'CharK':
            self.size = 1

    def __str__(self):
        return str(self.__dict__)


class SymbolTable:
    def __init__(self, node, name, level, off, body=None, params=None, is_type=False,delete_flag=True):
        self.kind = node.kind  # 记录符号表条目的类型
        self.name = name  # 记录符号表条目的名称
        self.level = level  # 记录符号表条目的层级
        self.off = off  # 记录符号表条目的偏移量
        self.body = None  # 记录符号表条目的子项
        self.delete_flag = False
        self.params = None  # 记录符号表条目的参数（如果有的话）
        # 标识符是否是类型 用于表示符号表条目是否是一个类型。在编译器中，有些符号表条目是代表数据类型的，比如int、float、struct等，而有些符号表条目则是代表变量或函数等。
        self.is_type = is_type
        # 如果符号表条目有参数，记录参数列表
        if params is not None:
            self.params = params

        # 如果符号表条目有子项，处理子项
        if body is not None:
            tmp = []
            lp = 0
            # 处理子项中的每一个成员
            for x in body:
                lp += 1
                # 处理成员中的每一个名称
                for na in x.name:
                    error_flag = False
                    # 判断成员名称是否重复
                    for i in tmp:
                        if na == i.name:
                            error_flag = True
                    # 如果名称重复，报错并跳过
                    if error_flag:
                        error(str(int(node.raw_line) + lp), f"record {name} 成员 {na} 重复定义")
                        continue
                    # 记录成员类型、名称等信息
                    y = Kind(x)
                    y.name = na
                    tmp.append(y)

            # 记录符号表条目的子项列表
            self.body = tmp

        # 记录符号表条目的类型信息
        self.typePtr = Kind(node, self.body)

    # 定义符号表条目的字符串表示
    def __str__(self):
        s = ""
        if self.body is not None:
            for x in self.body:
                s += str(x.__dict__)
        return f"kind:{self.kind}, name:{self.name}, level:{self.level}, off:{self.off}, typePtr:{self.typePtr.__dict__}, body:{s}, params:{self.params}, is_type:{self.is_type}"


def CallSymbolTable(node, name, level, off, body=None, params=None, is_type=False):
    if node.kind == 'IdK':
        v = find(node.real_kind, type=True)
        if v is None:
            error(node.raw_line, f"未知类型: {node.real_kind}")
            return None
        tab = copy.deepcopy(v)
        tab.is_type = False
        tab.name = name
        return tab
    return SymbolTable(node, name, level, off, body=body, params=params, is_type=is_type)


all_scope = [[]]
scope = [[]]
scope_line = 0
off = 0


def find(name, exist=None, type=False):
    # print("----")
    # for i in range(scope_line, -1, -1):
    #     for x in reversed(scope[i]):
    #         print(x)
    # print("find name:", name)
    if exist is not None:
        low = scope_line - 1
    else:
        low = -1
    for i in range(scope_line, low, -1):
        for x in reversed(scope[i]):
            if name == x.name and x.is_type == type:
                return x
    return None


def ck(kind, vkind):
    if kind == "IdV" and vkind in ("IntegerK", "CharK"):
        return True
    if kind == "ArrayMembV" and vkind == "ArrayK":
        return True
    if kind == "FieldMembV" and vkind == "RecordK":
        return True
    return False


def getFieldKind(field):
    if field.kind in ("IntegerK", "CharK"):
        return field.kind
    if field.kind == "ArrayK":
        return field.arrayKind
    return None


def createName(node):
    if "varkind" in node.attr and node.attr["varkind"] == "FieldMembV":
        return node.name[0] + '.' + node.child[0].name[0]
    else:
        return node.name[0]


def get_kind(node):
    """
    获取节点的类型(kind)。
    如果节点是常量节点(ConstK)，则根据节点值来判断其类型，如果节点值是数字，则为"IntegerK"，如果节点值是字符，则为"CharK"。
    如果节点是标识符节点(IdK)，则获取其kind属性值，根据该值和符号表中该标识符对应的值的kind进行匹配，如果不匹配则返回错误。
    如果kind为"IdV"，则返回该标识符对应值的类型(kind)；如果kind为"ArrayMembV"，则检查其子节点是否只有一个，且该节点的类型为"IntegerK"，并且根据下标获取数组对应的元素类型(kind)；如果kind为"FieldMembV"，则找到对应的字段记录，如果找不到则返回错误，否则检查字段类型是否匹配，并处理字段子节点的符号表。
    如果节点是操作符节点(OpK)，则调用operator函数处理该节点，返回其类型(kind)。
    """
    if node.kind == "ConstK":
        if str.isdigit(node.name[0]):
            return "IntegerK"
        if re.match(r"\'[a-zA-Z]\'", node.name[0]):
            return "CharK"

    if node.kind == "IdK":
        kind = node.attr["varkind"]
        v = find(node.name[0])
        if v is None:
            error(node.raw_line, "变量查找失败:", node.name[0])
            return None
        if ck(kind, v.kind) is False:
            error(node.raw_line, "变量类型错误:", node.name[0], kind, v.kind)
            return None
        if kind == "IdV":
            return v.kind
        if kind == "ArrayMembV":
            if len(node.child) == 1:
                x = node.child[0]
                id = x.name[0]
                l = int(v.typePtr.arrayAttr["indexTy"]["low"])
                r = int(v.typePtr.arrayAttr["indexTy"]["up"])
                if str.isdigit(id) is False:
                    if get_kind(x) != "IntegerK":
                        error(node.raw_line, f"数组下标不合法: {createName(x)}, kind: {get_kind(x)}")
                elif int(id) < l or int(id) >= r:
                    error(node.raw_line, "数组越界:", f"index:{id}, l:{l}, r:{r}")
            else:
                error(node.raw_line, "array cant operate directed:", node.name[0])
            return v.typePtr.arrayKind
        if kind == "FieldMembV":
            nd = None
            for x in v.body:
                if x.name == node.child[0].name[0]:
                    nd = x
            if nd is None:
                error(node.raw_line, f"record {node.name[0]} 不存在成员 {node.child[0].name[0]}")
                return None
            if ck(node.child[0].attr["varkind"], nd.kind) is False:
                error(node.raw_line, f"record {node.name[0]} member {node.child[0].name[0]} kind err: {nd.kind}, ",
                      node.child[0].attr["varkind"])
                return None
            for x in node.child:
                for y in x.child:
                    analysis_and_generate_table(y)
            return getFieldKind(nd)
    if node.kind == 'OpK':
        return operator(node, node.name[0])


def operator(node, op):
    """
    它首先遍历node节点的所有子节点，将它们的类型存储在kindList列表中。
    然后它根据操作符类型和kindList列表中的元素类型检查它们是否合法，
    如果合法，则返回第一个元素。如果不合法，则返回None。
    """
    kind_list = []
    for x in node.child:
        kind_list.append(analysis_and_generate_table(x))
    if len(kind_list) == 0:
        error(node.raw_line, "operate not have child")
        return None
    for i in range(len(kind_list)):
        if kind_list[i] is None:
            return None
        elif kind_list[i] not in ("IntegerK", "CharK"):
            error(node.raw_line, op, "运算类型不合法:", kind_list[i])
        elif kind_list[i] != kind_list[0]:
            error(node.raw_line, op, "运算失败:",
                  [(node.child[x].name[0], kind_list[x]) for x in range(len(kind_list))])
            return None
        elif op in ("+", "-", "*", "/") and kind_list[i] == "CharK":
            error(node.raw_line, op, "不可以对字符类型进行加减乘除操作",
                  [(node.child[x].name[0], kind_list[x]) for x in range(len(kind_list))])
            return None

    return kind_list[0]


def analysis_and_generate_table(node):
    """
    语义分析阶段的符号表生成和类型检查功能。主要实现过程如下：
    通过递归遍历语法树来检查各种声明类型的语法树节点，并生成相应的符号表。
    对于每个声明的变量，记录其名称、作用域、类型和偏移等信息，检查其是否重复定义或调用等错误情况，并给出相应的错误提示。
    对于各种语法结构（如赋值语句、函数调用、循环语句等），对其内部的变量、函数等进行类型检查，确保其语法合法性。
    将符号表的内容输出到文件中，用于后续生成汇编代码时进行参考。
    """
    # 传入根节点
    global scope_line, scope, off
    # ProK, PheadK, TypeK, VarK, ProDecK, StmLK, DecK, Stmtk, ExpK
    # 处理 DecK 节点
    if node.node_kind == "DecK":
        # 遍历节点的每个变量名
        for x in node.name:
            # 如果该变量名已经存在于符号表中，报错并跳过
            if find(x, exist=True) is not None:
                error(node.raw_line, "重复变量:", x)
                continue

            # 如果节点的 kind 为 RecordK，则将该节点的每个子节点加入body
            body = None
            if node.kind == "RecordK":
                body = []
                for y in node.child:
                    body.append(y)

            # 创建符号表，并将其添加到符号表列表中
            tab = CallSymbolTable(node, x, level=scope_line, off=off, body=body)
            if tab is None:
                continue

            # 设置变量的偏移量，若是该层的第一个变量则偏移量为0，否则为前一个变量的大小+偏移量
            if len(scope[scope_line]) == 0:
                tab.off = 0
            else:
                tmp = scope[scope_line][-1]
                tab.off = tmp.typePtr.size + tmp.off

            # 将符号表添加到当前层的符号表列表和所有符号表列表中
            scope[scope_line].append(tab)
            all_scope[scope_line].append(tab)

            # 如果该节点的 kind 不为 RecordK，则继续处理节点的子节点
            if node.kind == "RecordK":
                return
            for x in node.child:
                analysis_and_generate_table(x)

    # 处理函数声明
    elif node.node_kind == "ProcDecK" and node.id_num > 0:
        # kind则是CallSymbolTable类的属性 表示符号表中存储的元素的类型，比如"int"、"char"、"ProcDecK"、"VarK"等等
        node.kind = "ProcDecK"
        # 如果函数已存在，报错
        if find(node.name[0], exist=True) is not None:
            error(node.raw_line, "重复变量:", node.name[0])
            return
        # 遍历语法分析树中当前过程的所有子节点，对于每个类型为DecK的子节点，进一步遍历其name属性，将非空的名称添加到params列表中，并同时记录该参数的类型(
        #     kind)。
        params = []
        for x in node.child:
            if x.node_kind == "DecK":
                for y in x.name:
                    if y != " " and y != "":
                        params.append({"kind": x.kind, "name": y})
        # 生成符号表
        tab = CallSymbolTable(node, node.name[0], level=scope_line, off=off, params=params)
        if tab is None:
            return
        # 确定函数在作用域中的偏移量
        if len(scope[scope_line]) == 0:
            tab.off = 0
        else:
            tmp = scope[scope_line][-1]
            tab.off = tmp.typePtr.size + tmp.off
        # 添加到当前作用域中
        scope[scope_line].append(tab)
        all_scope[scope_line].append(tab)
        # 处理函数体
        # 首先增加作用域层数（sl加1），并向scope和all_scope列表中添加一个空列表，表示开启新的作用域，因为函数体中的变量和参数只在函数内部有效。
        # 然后遍历函数体中的每个子节点x，并递归调用generate_table函数，以便处理它们，生成符号表等信息。
        # 最后，恢复作用域层数，将scope中的最后一个列表删除，表示离开当前作用域。
        scope_line += 1
        scope.append([])
        all_scope.append([])
        for x in node.child:
            analysis_and_generate_table(x)
        scope_line -= 1
        scope = scope[:-1]
        # print("删除法")
        # print(all_scope[len(all_scope)-1])
        for t in all_scope[len(all_scope)-1]:
            t.delete_flag = True

    elif node.node_kind == "StmtK":
        # 处理语句节点（StmtK），它有不同的种类，包括：IfK、WhileK、AssignK、ReadK、WriteK、CallK和ReturnK。
        # 检查调用的函数是否存在，并且参数类型是否正确。
        if node.kind == "CallK":
            pro = find(node.name[0])
            if pro is None:
                error(node.raw_line, "procDeck 查找失败:", node.name[0])
                return
            elif pro.kind != "ProcDecK":
                error(node.raw_line, "procDeck 类型错误:", node.name[0], pro.kind)
                return
            # 参数校验
            params = []
            for x in node.child:
                if x.kind == "OpK":
                    kind = operator(x, x.name[0])
                    if kind is None:
                        return
                else:
                    kind = get_kind(x)
                    if kind is None:
                        error(x.raw_line, "无此变量类型:", x.name[0])
                        return
                params.append(kind)
            proParams = [x["kind"] for x in pro.params]
            # print(params, pro.params)
            if len(params) != len(proParams):
                error(node.raw_line, "调用失败:", params, proParams)
                return
            for i in range(len(params)):
                if params[i] != proParams[i]:
                    error(node.raw_line, "调用失败:", params, proParams)
                    return
            return
        # 对其子节点进行语义分析
        if node.kind == "IfK":
            for x in node.child:
                analysis_and_generate_table(x)
        # AssignK，需要检查赋值左侧是否是合法的标识符，并且对其右侧进行语义分析
        if node.kind == "AssignK":
            if node.child[0].kind != "IdK":
                error(node.raw_line, "赋值左侧非法", node.name[0])
            return operator(node, "=")
        # 需要检查变量是否存在。
        if node.kind == "ReadK":
            if find(node.name[0]) is None:
                error(node.raw_line, "变量不存在:", node.name[0])
            return
        # 对子节点进行语义分析，并返回操作类型
        if node.kind == "WriteK":
            return operator(node, "write")
        # 需要检查变量是否存在
        if node.kind == "ReturnK":
            return
        # 需要对其子节点进行语义分析
        if node.kind == "WhileK":
            for x in node.child:
                analysis_and_generate_table(x)
            return
        # ConstK 表示常量、IdK表示标识符和OpK
        # 表示操作符
    elif node.node_kind == "ExpK":
        # OpK ConstK IdK
        if node.kind == "OpK":
            return operator(node, node.name[0])

        if node.kind in ("IdK", "ConstK"):
            return get_kind(node)
    elif node.node_kind == "TypeK":
        for x in node.child:
            # 递归地分析它的子节点
            if x.kind == "RecordK":
                analysis_and_generate_table(x)
                continue
            if find(x.name[0], exist=True) is not None:
                error(node.raw_line, "类型重复定义:", x.name[0])
                continue
            tab = CallSymbolTable(x, x.name[0], level=scope_line, off=off, is_type=True)
            if tab is None:
                continue

            if len(scope[scope_line]) == 0:
                tab.off = 0
            else:
                tmp = scope[scope_line][-1]
                tab.off = tmp.typePtr.size + tmp.off

            scope[scope_line].append(tab)
            all_scope[scope_line].append(tab)
    else:
        for x in node.child:
            analysis_and_generate_table(x)
    return


def table_print(table):
    for i in range(len(table)):
        for x in table[i]:
            print(f"", str(x))


root = None


def init():
    global root, all_scope, scope_line, off, error_flag, scope
    root = None
    all_scope = [[]]
    scope = [[]]
    scope_line = 0
    off = 0
    error_flag = False


def semantic_analysis(tree_path):
    global root  # 声明使用全局变量root
    init()  # 初始化全局变量
    root = generate_node(tree_path)  # 通过解析语法分析树文件，生成语法树节点
    analysis_and_generate_table(root)  # 语义分析和生成符号表
    with open('../intermediate/symbol_table.txt', "w") as f:  # 打开语义分析表文件
        for i in range(len(all_scope)):  # 遍历符号表中所有作用域
            for x in all_scope[i]:  # 遍历当前作用域下所有符号表项
                dic = x.__dict__  # 将符号表项的属性字典赋值给变量dic
                f.write(f"scope:{i}\n")  # 将当前行数写入文件
                for key in x.__dict__:  # 遍历符号表项的属性字典
                    if dic[key] is not None:  # 如果属性值不为空
                        if type(dic[key]) == list:  # 如果属性值是列表
                            f.write(f"{key}:\n")  # 写入属性名称
                            for xx in dic[key]:  # 遍历列表中的元素
                                f.write("   " + str(xx) + "\n")  # 写入列表元素
                        else:
                            f.write(f"{key}:{dic[key]}\n")  # 写入属性名和属性值
                f.write("\n")  # 写入空行
    print("符号表:")
    table_print(all_scope)  # 打印符号表
    if error_flag:  # 如果flag标志位为真
        with open("../intermediate/error.txt", "w") as file:
            file.write(err_msg_file)
        return True  # 表示语义分析出错
    return False  # 表示语义分析成功完成


if __name__ == '__main__':
    init()
    semantic_analysis("../intermediate/syntax_tree.txt")
