import os

from src.words import delimiters, reservedWords

tokenList = []
has_error = 0
err_msg = ""


class Token:
    # 行数
    # 类型
    # 单词
    def __init__(self, line, lex, sem):
        self.line = line
        self.lex = lex
        self.sem = sem


def add(word, num, err=False):
    global has_error, err_msg
    if err:
        has_error = 1
        tokenList.append(Token(num, "ERROR", word))
        # 只打印第一个出错的 num代表源代码第几行
        err_msg = err_msg + f"line:{num + 1} invalid: {word}\n"

    elif str.isdigit(word):
        tokenList.append(Token(num, "INTC", int(word, 10)))
    elif word in delimiters:
        tokenList.append((Token(num, delimiters[word], word)))
    elif word in reservedWords:
        tokenList.append((Token(num, reservedWords[word], word)))
    elif word[0] == '\'' and word[-1] == '\'':
        tokenList.append((Token(num, "CHARC", word)))
    else:
        tokenList.append((Token(num, "ID", word)))


# 这个函数的作用是将传入的文本内容分析成 token 列表并返回，
# 其中每个 token 表示代码中的一个单词、符号或标识符等。
# 函数通过对每个字符进行遍历，并根据不同的情况将字符转换为 token 并添加到 tokenList 列表中。
# 具体来说，函数首先将传入的文本内容 lines 划分成一行一行的字符串，然后对每一行字符串进行分析。
# 在分析每行字符串时，函数会遍历字符串中的每个字符，并根据字符的不同，判断其所属的 token 类型，然后将其添加到 tokenList 列表中。
# 函数支持的 token 类型包括数字、字母、注释、运算符、分隔符等。
# 最后，函数将一个特殊的 token 添加到 tokenList 列表中，表示文本内容的结束，并将列表返回

def analysis_lines(lines):
    """
    这个函数的作用是将传入的文本内容分析成 token 列表并返回，其中每个 token 表示代码中的一个单词、符号或标识符等。函数通过对每个字符进行遍历，并根据不同的情况将字符转换为 token 并添加到 tokenList
    列表中。具体来说，函数首先将传入的文本内容 lines 划分成一行一行的字符串，然后对每一行字符串进行分析。在分析每行字符串时，函数会遍历字符串中的每个字符，并根据字符的不同，判断其所属的 token 类型，然后将其添加到
    tokenList 列表中。函数支持的 token 类型包括数字、字母、注释、运算符、分隔符等。最后，函数将一个特殊的 token 添加到 tokenList 列表中，表示文本内容的结束，并将列表返回。 #

    comment_flag是一个布尔变量，用于跟踪当前是否正在处理代码中的注释部分。在此函数中，当解析到一个左大括号 # {时，comment_flag会被设置为 # True，表示代码进入了一个注释块。当解析到一个右大括号}
    时，comment_flag会被设置为 # False，表示注释块结束。在注释块内，代码会被忽略，直到解析到右大括号。
    """
    comment_flag = False
    for num in range(0, len(lines)):
        # 将列表lines中下标为num的元素去掉换行符后再加上一个空格，存储到变量line中。
        line = lines[num].replace("\n", "", -1) + " "
        i = 0
        while i < len(line):
            c = line[i]
            if comment_flag:
                if c == '}':
                    comment_flag = False
            elif str.isdigit(c):
                word = c
                while str.isdigit(line[i + 1]):
                    word = word + line[i + 1]
                    i = i + 1
                add(word, num)
            elif str.isalpha(c):
                word = c
                while str.isdigit(line[i + 1]) or str.isalpha(line[i + 1]):
                    word = word + line[i + 1]
                    i = i + 1
                add(word, num)
            elif c == '.':
                if line[i + 1] == ".":
                    i = i + 1
                    add("..", num)
                else:
                    add(".", num)
                    # 如果当前不在注释块中，且当前字符是单引号 需要转义
            elif c == '\'':
                word = c
                i = i + 1
                while i < len(line):
                    # 遍历单引号内的字符，如果是单引号，则表示字符串结束，将字符串加入到词法分析器的 tokenList 中
                    word = word + line[i]
                    if line[i] == '\'':
                        add(word, num)
                        break
                        # 如果当前字符不是数字或字母，将word存储到tokens中并结束循环。
                    elif (str.isdigit(line[i]) or str.isalpha(line[i])) == False:
                        add(word, num, True)
                        break
                    i = i + 1
            elif c == '{':
                comment_flag = True
            elif c == ':':
                if line[i + 1] == "=":
                    add(":=", num)
                else:
                    # 出错了
                    add(line[i] + line[i + 1], num, True)
                i = i + 1
            elif c in delimiters:
                add(c, num)
                # 这段代码是在处理代码中的空格和制表符
            elif c == " " or c == "	":
                _ = c
            else:
                add(line[i], num, True)
            i = i + 1
    tokenList.append(Token(len(lines), "EOF", "EOF"))


def lex_analysis(pro_path, token_path):
    global tokenList,has_error,err_msg
    tokenList = []
    has_error = 0
    err_msg = ""
    if not os.path.exists(pro_path):
        print(f"Open pro_path:{pro_path} failed")
        return True
    with open(pro_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        analysis_lines(lines)

    # 写结果,如果有误那么就不写了
    if has_error == 0:
        print("token 生成成功,具体请查看文件")
        with open(token_path, "w") as file:
            file.seek(0)
            file.truncate()

        with open(token_path, "w") as file:
            print("open token_path w+")
            # file.seek(0)
            # file.truncate()
            for x in tokenList:
                if x.sem in delimiters:
                    file.write(f"{x.line} Other {x.sem}\n")
                elif x.sem in reservedWords:
                    file.write(f"{x.line} Reserved_word {x.lex}\n")
                else:
                    file.write(f"{x.line} {x.lex} {x.sem}\n")
        return False
    else:
        with open("../intermediate/error.txt", "w") as file:
            file.write(err_msg)
        print("token 生成失败")
        return True
