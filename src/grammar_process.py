from src.ll1_handle import Node


def Priosity(op):
    if op == 'END':
        pri = 0
    elif op == '<' or op == '=':
        pri = 1
    elif op == '+' or op == '-':
        pri = 2
    elif op == '*' or op == '/':
        pri = 3
    else:
        pri = -1
    return pri


def judgeType(op):
    a = ['+', '-', '*', '/', '=', '<']
    if op in a:
        b = 'OpK'
    elif op.isdigit() or ('\'' in op and len(op) == 3):
        b = 'ConstK'
    else:
        b = 'IdK'
    return b


def copyNode(x, y):
    x.nodeKind = y.nodeKind
    x.child = y.child
    x.Sibling = y.Sibling
    x.line_no = y.line_no
    x.kind = y.kind
    x.idnum = y.idnum  # 一个节点中的标识符的个数
    x.name = y.name
    x.attr = y.attr
    x.judge = y.judge


def process1(Tree, toke, pre_node):
    # Program ::= ProgramHead DeclarePart ProgramBody .
    return pre_node


def process2(Tree, toke, pre_node):
    # ProgramHead ::= PROGRAM ProgramName
    PheadK = Tree.stack.pop()
    PheadK.line_no = toke[0]
    PheadK.judge = True
    return PheadK


def process3(Tree, toke, pre_node):
    # ProgramName ::= ID
    pre_node.name.append(str(toke[2]))
    pre_node.idnum += 1
    return pre_node


def process4(Tree, toke, pre_node):
    return pre_node


def process5(Tree, toke, pre_node):
    return pre_node


def process6(Tree, toke, pre_node):
    return pre_node


def process7(Tree, toke, pre_node):
    TypeK = Tree.stack.pop()
    TypeK.line_no = toke[0]
    TypeK.judge = True
    TypeK.child.append(Node('DecK'))
    TypeK.Sibling = Node('VarK')
    Tree.stack.push(TypeK.Sibling)
    Tree.stack.push(TypeK.child[0])
    return TypeK


def process8(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process9(Tree, toke, pre_node):
    Tree.stack.pop()
    return pre_node


def process10(Tree, toke, pre_node):
    return pre_node


def process11(Tree, toke, pre_node):
    pre_node.name.append(str(toke[2]))
    pre_node.idnum += 1
    return pre_node


def process12(Tree, toke, pre_node):
    return pre_node


def process13(Tree, toke, pre_node):
    return pre_node


def process14(Tree, toke, pre_node):
    pre_node.kind['dec'] = 'IdK'
    pre_node.name.append(str(toke[2]))
    pre_node.idnum += 1
    return pre_node


def process15(Tree, toke, pre_node):
    if pre_node.kind['dec'] == 'ArrayK':
        pre_node.attr[0]['childType'] = 'IntegerK'
    else:
        pre_node.kind['dec'] = 'IntegerK'
    return pre_node


def process16(Tree, toke, pre_node):
    if pre_node.kind['dec'] == 'ArrayK':
        pre_node.attr[0]['childType'] = 'CharK'
    else:
        pre_node.kind['dec'] = 'CharK'
    return pre_node


def process17(Tree, toke, pre_node):
    return pre_node


def process18(Tree, toke, pre_node):
    return pre_node


def process19(Tree, toke, pre_node):
    pre_node.kind['dec'] = 'ArrayK'
    return pre_node


def process20(Tree, toke, pre_node):
    pre_node.attr[0]['low'] = toke[2]
    return pre_node


def process21(Tree, toke, pre_node):
    pre_node.attr[0]['up'] = toke[2]
    return pre_node


def process22(Tree, toke, pre_node):
    pre_node.kind['dec'] = 'RecordK'
    pre_node.line_no = toke[0]
    pre_node.child.append(Node('DecK'))
    Tree.stack.push(pre_node)
    Tree.stack.push(pre_node.child[0])
    return pre_node


def process23(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process24(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process25(Tree, toke, pre_node):
    Tree.stack.pop()
    pre_node = Tree.stack.pop()
    # pre_node.line_no = toke[0]
    pre_node.judge = True
    return pre_node


def process26(Tree, toke, pre_node):
    return pre_node


def process27(Tree, toke, pre_node):
    pre_node.name.append(toke[2])
    pre_node.idnum += 1
    return pre_node


def process28(Tree, toke, pre_node):
    return pre_node


def process29(Tree, toke, pre_node):
    return pre_node


def process30(Tree, toke, pre_node):
    return pre_node


def process31(Tree, toke, pre_node):
    return pre_node


def process32(Tree, toke, pre_node):
    VarK = Tree.stack.pop()
    if VarK.nodeKind == 'TypeK':
        VarK.Sibling = Node('VarK')
        VarK = VarK.Sibling
    VarK.judge = True
    VarK.line_no = toke[0]
    VarK.child.append(Node('DecK'))
    VarK.Sibling = Node('ProcK')
    VarK.Sibling.judge = True
    VarK.Sibling.child.append(Node('ProcDecK'))
    VarK.Sibling.child[0].father = VarK.Sibling
    Tree.stack.push(VarK.Sibling.child[0])
    Tree.stack.push(VarK.child[0])
    return VarK


def process33(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process34(Tree, toke, pre_node):
    Tree.stack.pop()
    return pre_node


def process35(Tree, toke, pre_node):
    return pre_node


def process36(Tree, toke, pre_node):
    pre_node.name.append(toke[2])
    pre_node.idnum += 1
    return pre_node


def process37(Tree, toke, pre_node):
    return pre_node


def process38(Tree, toke, pre_node):
    return pre_node


def process39(Tree, toke, pre_node):
    return pre_node


def process40(Tree, toke, pre_node):
    return pre_node


def process41(Tree, toke, pre_node):
    ProcDecK = Tree.stack.pop()
    if ProcDecK == 'VarK':
        ProcDecK.Sibling = Node('ProcDecK')
        ProcDecK = ProcDecK.Sibling
    elif ProcDecK == 'TypeK':
        ProcDecK.Sibling = Node('VarK')
        ProcDecK = ProcDecK.Sibling
        ProcDecK.Sibling = Node('ProcK')
        ProcDecK.Sibling.judge = True
        ProcDecK.Sibling.child.append(Node('ProcDecK'))
        ProcDecK.Sibling.child[0].father = ProcDecK.Sibling
        ProcDecK = ProcDecK.Sibling.child[0]
    ProcDecK.judge = True
    ProcDecK.line_no = toke[0]
    if ProcDecK.father != None:
        ProcDecK.father.line_no = toke[0]
    ProcDecK.child.append(Node('DecK'))
    ProcDecK.child.append(Node('TypeK'))
    ProcDecK.child.append(Node('StmLK'))
    ProcDecK.Sibling = Node('ProcDecK')
    Tree.stack.push(ProcDecK.Sibling)
    Tree.stack.push(ProcDecK.child[2])
    Tree.stack.push(ProcDecK.child[1])
    Tree.stack.push(ProcDecK.child[0])
    return ProcDecK


def process42(Tree, toke, pre_node):
    return pre_node


def process43(Tree, toke, pre_node):
    return pre_node


def process44(Tree, toke, pre_node):
    pre_node.name.append(toke[2])
    pre_node.idnum += 1
    return pre_node


def process45(Tree, toke, pre_node):
    Tree.stack.pop()
    return pre_node


def process46(Tree, toke, pre_node):
    return pre_node


def process47(Tree, toke, pre_node):
    return pre_node


def process48(Tree, toke, pre_node):  # ???/??/?????????/
    Tree.stack.pop()
    return pre_node


def process49(Tree, toke, pre_node):
    return pre_node


def process50(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.attr[1]['paramt'] = 'valparamType'
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process51(Tree, toke, pre_node):
    DecK = Tree.stack.pop()
    DecK.line_no = toke[0]
    DecK.judge = True
    DecK.attr[1]['paramt'] = 'varparamtype'
    DecK.Sibling = Node('DecK')
    Tree.stack.push(DecK.Sibling)
    return DecK


def process52(Tree, toke, pre_node):
    pre_node.name.append(toke[2])
    pre_node.idnum += 1
    return pre_node


def process53(Tree, toke, pre_node):
    return pre_node


def process54(Tree, toke, pre_node):
    return pre_node


def process55(Tree, toke, pre_node):
    return pre_node


def process56(Tree, toke, pre_node):
    return pre_node


def process57(Tree, toke, pre_node):
    Tree.stack.pop()
    StmLK = Tree.stack.pop()
    StmLK.line_no = toke[0]
    StmLK.judge = True
    StmLK.child.append(Node('StmtK'))
    Tree.stack.push(StmLK.child[0])
    return StmLK


def process58(Tree, toke, pre_node):
    return pre_node


def process59(Tree, toke, pre_node):
    Tree.stack.pop()
    return pre_node


def process60(Tree, toke, pre_node):
    return pre_node


def process61(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'IfK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process62(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'WhileK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process63(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'ReadK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process64(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'WriteK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process65(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.kind['stmt'] = 'ReturnK'
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process66(Tree, toke, pre_node):
    StmtK = Tree.stack.pop()
    StmtK.line_no = toke[0]
    StmtK.judge = True
    StmtK.child.append(Node('ExpK'))
    StmtK.child[0].name.append(toke[2])
    StmtK.child[0].line_no = toke[0]
    StmtK.child[0].idnum += 1
    StmtK.child[0].judge = True
    StmtK.child[0].kind['exp'] = judgeType(toke[2])
    StmtK.Sibling = Node('StmtK')
    Tree.stack.push(StmtK.Sibling)
    return StmtK


def process67(Tree, toke, pre_node):
    pre_node.kind['stmt'] = 'AssignK'
    return pre_node


def process68(Tree, toke, pre_node):
    pre_node.kind['stmt'] = 'CallK'
    pre_node.name.append(pre_node.child[0].name[0])
    pre_node.idnum += 1
    pre_node.child[0].attr[2]['varkind'] = 'IdV'
    pre_node.child[0].judge = False
    return pre_node


def process69(Tree, toke, pre_node):
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[1])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return pre_node.child[0]


def process70(Tree, toke, pre_node):
    pre_node.child.append(Node('ExpK'))
    pre_node.child.append(Node('StmtK'))
    pre_node.child.append(Node('StmtK'))
    Tree.stack.push(pre_node.child[2])
    Tree.stack.push(pre_node.child[1])
    Tree.stack.push(pre_node.child[0])
    return pre_node


def process71(Tree, toke, pre_node):
    pre_node.child.append(Node('ExpK'))
    pre_node.child.append(Node('StmtK'))
    Tree.stack.push(pre_node.child[1])
    Tree.stack.push(pre_node.child[0])
    return pre_node


def process72(Tree, toke, pre_node):
    return pre_node


def process73(Tree, toke, pre_node):
    pre_node.name.append(toke[2])
    pre_node.idnum += 1
    return pre_node


def process74(Tree, toke, pre_node):
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return pre_node


def process75(Tree, toke, pre_node):
    return pre_node


def process76(Tree, toke, pre_node):
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[1])
    return pre_node


def process77(Tree, toke, pre_node):
    Tree.stack.pop()
    return pre_node


def process78(Tree, toke, pre_node):
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    return pre_node


def process79(Tree, toke, pre_node):
    return pre_node


def process80(Tree, toke, pre_node):
    pre_node.Sibling = Node('ExpK')
    Tree.stack.push(pre_node.Sibling)
    return pre_node


def process81(Tree, toke, pre_node):
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult = False
    return pre_node


def process82(Tree, toke, pre_node):  # ???//????/
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.line_no = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    Tree.getExpResult = True
    return currentP


def process83(Tree, toke, pre_node):
    return pre_node


def process84(Tree, toke, pre_node):
    # 看看是第一条还是第二条产生式
    if toke[2] == ')' and Tree.expflag != 0:
        while Tree.SignStack.peek().name[0] != '(':
            t = Tree.SignStack.pop()
            Rnum = Tree.NumStack.pop()
            Lnum = Tree.NumStack.pop()
            t.judge = True
            Lnum.judge = True
            Rnum.judge = True
            t.child.append(Lnum)
            t.child.append(Rnum)
            Tree.NumStack.push(t)
        Tree.SignStack.pop()
        Tree.expflag -= 1
    else:
        if Tree.getExpResult or Tree.getExpResult2:
            while Tree.SignStack.peek().name[0] != 'END':
                t = Tree.SignStack.pop()
                Rnum = Tree.NumStack.pop()
                Lnum = Tree.NumStack.pop()
                t.judge = True
                Lnum.judge = True
                Rnum.judge = True
                t.child.append(Lnum)
                t.child.append(Rnum)
                Tree.NumStack.push(t)
            Tree.SignStack.pop()
            currentP = Tree.stack.pop()
            t1 = Tree.NumStack.pop()
            copyNode(currentP, t1)
            Tree.getExpResult2 = False
            pre_node = currentP
    return pre_node


def process85(Tree, toke, pre_node):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.line_no = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    return currentP


def process86(Tree, toke, pre_node):
    return pre_node


def process87(Tree, toke, pre_node):
    return pre_node


def process88(Tree, toke, pre_node):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.line_no = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    while Priosity(Tree.SignStack.peek().name[0]) >= Priosity(currentP.name[0]):
        t = Tree.SignStack.pop()
        Rnum = Tree.NumStack.pop()
        Lnum = Tree.NumStack.pop()
        t.judge = True
        Lnum.judge = True
        Rnum.judge = True
        t.child.append(Lnum)
        t.child.append(Rnum)
        Tree.NumStack.push(t)
    Tree.SignStack.push(currentP)
    return currentP


def process89(Tree, toke, pre_node):
    currentP = Node('ExpK')
    currentP.name.append('(')
    currentP.line_no = toke[0]
    Tree.SignStack.push(currentP)
    Tree.expflag += 1
    return currentP


def process90(Tree, toke, pre_node):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.line_no = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    Tree.NumStack.push(currentP)
    return currentP


def process91(Tree, toke, pre_node):
    currentP = Node('ExpK')
    currentP.name.append(toke[2])
    currentP.line_no = toke[0]
    currentP.idnum += 1
    currentP.judge = True
    currentP.kind['exp'] = judgeType(toke[2])
    Tree.NumStack.push(currentP)
    return currentP


def process92(Tree, toke, pre_node):
    return pre_node


def process93(Tree, toke, pre_node):  # ??????????
    t = Node('ExpK')
    t.name.append(toke[2])
    t.line_no = toke[0]
    t.idnum += 1
    t.judge = True
    Tree.NumStack.push(t)
    return t


def process94(Tree, toke, pre_node):
    pre_node.kind['exp'] = 'IdK'
    pre_node.attr[2]['varkind'] = 'IdV'
    return pre_node


def process95(Tree, toke, pre_node):
    pre_node.kind['exp'] = 'IdK'
    pre_node.attr[2]['varkind'] = 'ArrayMembV'
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult2 = True
    return pre_node


def process96(Tree, toke, pre_node):
    pre_node.kind['exp'] = 'IdK'
    pre_node.attr[2]['varkind'] = 'FieldMembV'
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[0])
    return pre_node


def process97(Tree, toke, pre_node):
    ExpK = Tree.stack.pop()
    ExpK.line_no = toke[0]
    ExpK.judge = True
    ExpK.name.append(toke[2])
    ExpK.idnum += 1
    ExpK.kind['exp'] = 'IdK'
    return ExpK


def process98(Tree, toke, pre_node):
    pre_node.attr[2]['varkind'] = 'IdV'
    return pre_node


def process99(Tree, toke, pre_node):
    pre_node.attr[2]['varkind'] = 'ArrayMembV'
    pre_node.child.append(Node('ExpK'))
    Tree.stack.push(pre_node.child[0])
    t = Node('ExpK')
    t.name.append('END')
    Tree.SignStack.push(t)
    Tree.getExpResult2 = True
    return pre_node


def process100(Tree, toke, pre_node):
    return pre_node


def process101(Tree, toke, pre_node):
    return pre_node


def process102(Tree, toke, pre_node):
    return pre_node


def process103(Tree, toke, pre_node):
    return pre_node


def process104(Tree, toke, pre_node):
    return pre_node


def process105(Tree, toke, pre_node):
    return pre_node


def predict1(num, tree, toke, pre_node):
    if num == 1:
        t = process1(tree, toke, pre_node)
    elif num == 2:
        t = process2(tree, toke, pre_node)
    elif num == 3:
        t = process3(tree, toke, pre_node)
    elif num == 4:
        t = process4(tree, toke, pre_node)
    elif num == 5:
        t = process5(tree, toke, pre_node)
    elif num == 6:
        t = process6(tree, toke, pre_node)
    elif num == 7:
        t = process7(tree, toke, pre_node)
    elif num == 8:
        t = process8(tree, toke, pre_node)
    elif num == 9:
        t = process9(tree, toke, pre_node)
    elif num == 10:
        t = process10(tree, toke, pre_node)
    elif num == 11:
        t = process11(tree, toke, pre_node)
    elif num == 12:
        t = process12(tree, toke, pre_node)
    elif num == 13:
        t = process13(tree, toke, pre_node)
    elif num == 14:
        t = process14(tree, toke, pre_node)
    elif num == 15:
        t = process15(tree, toke, pre_node)
    elif num == 16:
        t = process16(tree, toke, pre_node)
    elif num == 17:
        t = process17(tree, toke, pre_node)
    elif num == 18:
        t = process18(tree, toke, pre_node)
    elif num == 19:
        t = process19(tree, toke, pre_node)
    elif num == 20:
        t = process20(tree, toke, pre_node)
    elif num == 21:
        t = process21(tree, toke, pre_node)
    elif num == 22:
        t = process22(tree, toke, pre_node)
    elif num == 23:
        t = process23(tree, toke, pre_node)
    elif num == 24:
        t = process24(tree, toke, pre_node)
    elif num == 25:
        t = process25(tree, toke, pre_node)
    elif num == 26:
        t = process26(tree, toke, pre_node)
    elif num == 27:
        t = process27(tree, toke, pre_node)
    elif num == 28:
        t = process28(tree, toke, pre_node)
    elif num == 29:
        t = process29(tree, toke, pre_node)
    elif num == 30:
        t = process30(tree, toke, pre_node)
    elif num == 31:
        t = process31(tree, toke, pre_node)
    elif num == 32:
        t = process32(tree, toke, pre_node)
    elif num == 33:
        t = process33(tree, toke, pre_node)
    elif num == 34:
        t = process34(tree, toke, pre_node)
    elif num == 35:
        t = process35(tree, toke, pre_node)
    elif num == 36:
        t = process36(tree, toke, pre_node)
    elif num == 37:
        t = process37(tree, toke, pre_node)
    elif num == 38:
        t = process38(tree, toke, pre_node)
    elif num == 39:
        t = process39(tree, toke, pre_node)
    elif num == 40:
        t = process40(tree, toke, pre_node)
    elif num == 41:
        t = process41(tree, toke, pre_node)
    elif num == 42:
        t = process42(tree, toke, pre_node)
    elif num == 43:
        t = process43(tree, toke, pre_node)
    elif num == 44:
        t = process44(tree, toke, pre_node)
    elif num == 45:
        t = process45(tree, toke, pre_node)
    elif num == 46:
        t = process46(tree, toke, pre_node)
    elif num == 47:
        t = process47(tree, toke, pre_node)
    elif num == 48:
        t = process48(tree, toke, pre_node)
    elif num == 49:
        t = process49(tree, toke, pre_node)
    elif num == 50:
        t = process50(tree, toke, pre_node)
    elif num == 51:
        t = process51(tree, toke, pre_node)
    elif num == 52:
        t = process52(tree, toke, pre_node)
    elif num == 53:
        t = process53(tree, toke, pre_node)
    elif num == 54:
        t = process54(tree, toke, pre_node)
    elif num == 55:
        t = process55(tree, toke, pre_node)
    elif num == 56:
        t = process56(tree, toke, pre_node)
    elif num == 57:
        t = process57(tree, toke, pre_node)
    elif num == 58:
        t = process58(tree, toke, pre_node)
    elif num == 59:
        t = process59(tree, toke, pre_node)
    elif num == 60:
        t = process60(tree, toke, pre_node)
    elif num == 61:
        t = process61(tree, toke, pre_node)
    elif num == 62:
        t = process62(tree, toke, pre_node)
    elif num == 63:
        t = process63(tree, toke, pre_node)
    elif num == 64:
        t = process64(tree, toke, pre_node)
    elif num == 65:
        t = process65(tree, toke, pre_node)
    elif num == 66:
        t = process66(tree, toke, pre_node)
    elif num == 67:
        t = process67(tree, toke, pre_node)
    elif num == 68:
        t = process68(tree, toke, pre_node)
    elif num == 69:
        t = process69(tree, toke, pre_node)
    elif num == 70:
        t = process70(tree, toke, pre_node)
    elif num == 71:
        t = process71(tree, toke, pre_node)
    elif num == 72:
        t = process72(tree, toke, pre_node)
    elif num == 73:
        t = process73(tree, toke, pre_node)
    elif num == 74:
        t = process74(tree, toke, pre_node)
    elif num == 75:
        t = process75(tree, toke, pre_node)
    elif num == 76:
        t = process76(tree, toke, pre_node)
    elif num == 77:
        t = process77(tree, toke, pre_node)
    elif num == 78:
        t = process78(tree, toke, pre_node)
    elif num == 79:
        t = process79(tree, toke, pre_node)
    elif num == 80:
        t = process80(tree, toke, pre_node)
    elif num == 81:
        t = process81(tree, toke, pre_node)
    elif num == 82:
        t = process82(tree, toke, pre_node)
    elif num == 83:
        t = process83(tree, toke, pre_node)
    elif num == 84:
        t = process84(tree, toke, pre_node)
    elif num == 85:
        t = process85(tree, toke, pre_node)
    elif num == 86:
        t = process86(tree, toke, pre_node)
    elif num == 87:
        t = process87(tree, toke, pre_node)
    elif num == 88:
        t = process88(tree, toke, pre_node)
    elif num == 89:
        t = process89(tree, toke, pre_node)
    elif num == 90:
        t = process90(tree, toke, pre_node)
    elif num == 91:
        t = process91(tree, toke, pre_node)
    elif num == 92:
        t = process92(tree, toke, pre_node)
    elif num == 93:
        t = process93(tree, toke, pre_node)
    elif num == 94:
        t = process94(tree, toke, pre_node)
    elif num == 95:
        t = process95(tree, toke, pre_node)
    elif num == 96:
        t = process96(tree, toke, pre_node)
    elif num == 97:
        t = process97(tree, toke, pre_node)
    elif num == 98:
        t = process98(tree, toke, pre_node)
    elif num == 99:
        t = process99(tree, toke, pre_node)
    elif num == 100:
        t = process100(tree, toke, pre_node)
    elif num == 101:
        t = process101(tree, toke, pre_node)
    elif num == 102:
        t = process102(tree, toke, pre_node)
    elif num == 103:
        t = process103(tree, toke, pre_node)
    elif num == 104:
        t = process104(tree, toke, pre_node)
    elif num == 105:
        t = process105(tree, toke, pre_node)
    return t

# syntax_tree = Tree()
# process2(syntax_tree, 1)
# print(syntax_tree.root.child[1].judge)
