import copy


# left_row_mapping, table
class handle_error:
    def __init__(self, left, left_row_mapping, table, grammar):
        self.left = left
        self.left_row_mapping = left_row_mapping
        self.table = table
        self.grammar = grammar
        self.reservedWords = [
            "PROGRAM",
            "TYPE",
            "VAR",
            "PROCEDURE",
            "IF",
            "THEN",
            "ELSE",
            "FI",
            "WHILE",
            "DO",
            "ENDWH",
            "BEGIN",
            "END",
            "READ",
            "WRITE",
            "ARRAY",
            "OF",
            "RECORD",
            "RETURN",
            "INTEGER",
            "CHAR",
        ]  # 保留字
        self.delimiters = [
            ".",
            ":=",
            "=",
            "<",
            "+",
            "-",
            "*",
            "/",
            ",",
            "[",
            "]",
            "..",
            ";",
            "(",
            ")",
        ]  # 运算符、限界符

    # 判断修改是否正确：
    def judge_error_type2(self, SignStack, TokenStack):
        num = 10
        """
        把新的两个栈进行匹配 探测我们做的修改是否正确
        """
        while (not SignStack.isEmpty()) and num > 0:
            sign = SignStack.peek()
            toke = TokenStack.peek()
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
                judge = self.table[row][token]
                if judge != -1:
                    SignStack.pop()
                    rig = self.grammar[judge]['right']
                    length = len(rig)
                    for i in range(length):
                        if rig[length - 1 - i] != 'NULL':
                            SignStack.push(rig[length - 1 - i])
                else:
                    return False
            else:
                if sign == token:  # 相等则进行匹配
                    SignStack.pop()
                    TokenStack.pop()
                else:  # 不相等出错
                    return False
            num -= 1
        return True

    # 判断修改是否正确：
    def judge_error_type(self, sign, token):
        if sign in self.left:
            row = self.left_row_mapping[sign]
            judge = self.table[row][token]
            if judge != -1:
                return True
            else:
                return False
        else:
            if sign == token:  # 相等则进行匹配
                return True
            else:  # 不相等出错
                return False

    def run(self, SignStack, TokenStack, sign_replace, sign_replace_len, token_replace):
        ErrImag = ' '
        self.sign_replace = sign_replace
        self.sign_replace_len = sign_replace_len
        self.token_replace = token_replace
        for i in range(4):
            ErrImag = self.find_error_type(i + 1, SignStack, TokenStack)
            if ErrImag:
                break
        if not ErrImag:
            ErrImag = '语句存在未知语法错误'

        return ErrImag

    def find_error_type(self, num, SignStack, TokenStack):
        self.sign = SignStack.peek()
        toke = TokenStack.peek()
        if toke[1] == 'ID':
            self.token = 'ID'
        elif toke[1] == 'INTC':
            self.token = 'INTC'
        elif toke[1] == 'CHARC':
            self.token = 'CHARC'
        else:
            self.token = toke[2]
        if num == 1:
            ErrImag = self.handle_error1(SignStack, TokenStack)
        elif num == 2:
            ErrImag = self.handle_error2(SignStack, TokenStack)
        elif num == 3:
            ErrImag = self.handle_error3(SignStack, TokenStack)
        elif num == 4:
            ErrImag = self.handle_error4(SignStack, TokenStack)
        return ErrImag

    def handle_error1(self, SignStack, TokenStack):
        # 缺少保留字
        for i in range(len(self.reservedWords)):
            ReWord = self.reservedWords[i]
            S1 = copy.deepcopy(SignStack)
            T1 = copy.deepcopy(TokenStack)
            T1.push(['0', 'Reserved_word', ReWord])
            # 把这个加进去是否ok
            if self.judge_error_type2(S1, T1):
                message = '缺少保留字' + ReWord
                return message
        return "缺少保留字"

    def handle_error2(self, SignStack, TokenStack):
        if self.judge_error_type(self.sign, 'INTC'):
            return '缺少常量'

    def handle_error3(self, SignStack, TokenStack):
        # 缺少符号
        for i in range(len(self.delimiters)):
            Deli = self.delimiters[i]
            S1 = copy.deepcopy(SignStack)
            T1 = copy.deepcopy(TokenStack)
            T1.push(['0', 'Other', Deli])
            if self.judge_error_type2(S1, T1):
                message = '缺少符号' + Deli
                return message
            return ''

    def handle_error4(self, SignStack, TokenStack):
        # 回溯查错 10层
        # 备份当前状态
        sign_replace = copy.deepcopy(self.sign_replace)
        sign_replace_len = copy.deepcopy(self.sign_replace_len)
        token_replace = copy.deepcopy(self.token_replace)
        SB = copy.deepcopy(SignStack)
        TB = copy.deepcopy(TokenStack)
        if sign_replace.size() < 10:
            x = sign_replace.size()
        else:
            x = 10
        while x > 0:
            # 回溯时将SB和TB栈中的内容还原到之前的状态，以便后续的错误分析。
            for j in range(sign_replace_len.pop()):
                SB.pop()
            SB.push(sign_replace.pop())
            t = token_replace.pop()
            if t[1] != 'back':
                TB.push(t)
                # 在保留字中查找是否有缺失
            for i in range(len(self.reservedWords)):
                ReWord = self.reservedWords[i]
                S1 = copy.deepcopy(SB)
                T1 = copy.deepcopy(TB)
                T1.push(['0', 'Reserved_word', ReWord])
                if self.judge_error_type2(S1, T1):
                    message = '缺少保留字' + ReWord
                    return message
            x -= 1
        return ''
