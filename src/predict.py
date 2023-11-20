import copy

"""
原文法规则下，对于字符来说没有相应的指代符，即非终极符 Exp 无法推出 CHARC
文法加了一条 Factor::=CHARC 的文法。
"""
# sign_arr 是某一行语法的所有符号 包括 :=
sign_arr_arr = []
left = set()
right = set()
first = {"": set()}
follow = {"": set()}
predict = {0: set()}


def first_handle(sign_arr, only_right):
    """
    遍历当前产生式右部 遇到终极符/遇到已经处理的符号/还没到终极符并且有空（把NULL减去再union）
    """
    i = 0
    flag = 0
    for i in range(2, len(sign_arr)):  # 遍历右边的串
        if sign_arr[i] in only_right:  # 遇到终极符了
            first[sign_arr[0]].add(sign_arr[i])
            flag = 1
            break
        elif "NULL" not in first[sign_arr[i]]:  # 遇到已经处理的符号
            first[sign_arr[0]] = first[sign_arr[0]].union(first[sign_arr[i]])
            flag = 1
            break
        else:  # 还没到终极符并且有空
            first[sign_arr[0]] = first[sign_arr[0]].union(first[sign_arr[i]]) - {"NULL"}
    if flag == 0 and ("NULL" in first[sign_arr[len(sign_arr) - 1]]):
        first[sign_arr[0]].add("NULL")


def handle_sign_arr_i_follow(sign_arr, i, only_right):
    """
    找到下标为sign_arr[i]的所有follow集合,和课堂上学的一样的
    """
    # j是他右边第一个符号下标
    j = i + 1
    # 找到第一个终极符或非终极符不能推出NULL的关键字sign_arr[j]
    while j < len(sign_arr) and (sign_arr[j] not in only_right) and ("NULL" in first[sign_arr[j]]):
        # 将first[sign_arr[j]]中除了"NULL"以外的终极符加入到follow[sign_arr[i]]中
        follow[sign_arr[i]] = follow[sign_arr[i]].union(first[sign_arr[j]]) - {"NULL"}
        j = j + 1
        # 如果j超了len(sign_arr),union左边的入follow（说明当前找的符号右边是空）
    if j == len(sign_arr):
        follow[sign_arr[i]] = follow[sign_arr[i]].union(follow[sign_arr[0]])

        # 如果j是非终极符，将其加入到follow[sign_arr[i]]中
    elif sign_arr[j] in only_right:
        follow[sign_arr[i]].add(sign_arr[j])
    else:
        # NULL" not in first[sign_arr[j]],说明这个sign_arr[i]右边的符号firts集合不包括Null
        follow[sign_arr[i]] = follow[sign_arr[i]].union(first[sign_arr[j]])


def handle_sign_arr_i_predict(sign_arr, i, only_right):  # i是行号，x是行
    j = 2
    while j < len(sign_arr) and (sign_arr[j] not in only_right) and ("NULL" in first[sign_arr[j]]):
        # 如果退出循环可能能的情况：j超了/是只出现在右边的word/非终但是没有Null
        predict[i] = predict[i].union(first[sign_arr[j]]) - {"NULL"}
        j = j + 1
    if j == len(sign_arr):  # 超过了说明需要union左边的
        predict[i] = predict[i].union(follow[sign_arr[0]])
    elif sign_arr[j] in only_right and sign_arr[j] != "NULL":  # 非空的终极符
        predict[i].add(sign_arr[j])
    elif sign_arr[j] in only_right and sign_arr[j] == "NULL":  # 是空的终极符
        predict[i] = predict[i].union(follow[sign_arr[0]])
    else:
        # 全部没有Null ("NULL" not in first[sign_arr[j]])
        predict[i] = predict[i].union(first[sign_arr[j]])


def getPredict():
    with open("../source/grammar.txt") as file:
        lines = file.readlines()
        for line in lines:  # 得到left和right
            line = str(line).replace("\n", "")
            pos = line.split(" ", 20)
            # 1是::=
            sign_arr_arr.append(pos)
            left.add(pos[0])  # left
            for sign in pos[2:]:  # right
                right.add(sign)
        only_right = right - left  # 只出现的右边的终极符
        # 构建first
        # 1.构建key 把左边的符号加进去
        # 2.处理当前的sign[i]
        # 3.处理直到first集合不发生变化
        for sign_arr in sign_arr_arr:
            if sign_arr[0] not in first.keys():  # 把左边的key(产生式左部)
                first.update({sign_arr[0]: set()})
                follow.update({sign_arr[0]: set()})
            if sign_arr[2] in only_right:  # 右边第一个是终极符
                first[sign_arr[0]].add(sign_arr[2])
        t = copy.copy(first)
        while True:  # 循环处理，直到first不再变化
            for y in sign_arr_arr:
                if y[2] not in only_right:  # 如果该产生式右部第一个符号是非终结符，对其进行first处理
                    first_handle(y, only_right)
            if t == first:
                break
            t = copy.copy(first)

        # 将#添加到开始符号的follow集合中
        follow.update({sign_arr_arr[0][0]: {"#"}})
        t = copy.copy(follow)
        while True:  # 循环处理，直到follow不再变化
            for sign_arr in sign_arr_arr:
                for i in range(2, len(sign_arr)):  # 遍历右部,左部在处理first的时候已经做了
                    if sign_arr[i] not in follow.keys() and sign_arr[i] not in only_right:  # 还没有关键词并且需要创建关键词
                        follow.update({sign_arr[i]: set()})
                    if sign_arr[i] not in only_right:  # 只对非终极符进行函数调用
                        handle_sign_arr_i_follow(sign_arr, i, only_right)
            if t == follow:
                break
            t = copy.copy(follow)

        # 最后处理predict集
        i = 1
        t = copy.copy(predict)
        while True:
            for sign_arr in sign_arr_arr:
                if i not in follow.keys():
                    predict.update({i: set()})
                handle_sign_arr_i_predict(sign_arr, i, only_right)
                i = i + 1
            if t == predict:
                break
            t = copy.copy(predict)
            i = 1
        # print(first)
        # print(follow)
        # for key in predict:
        #     print(key, predict[key])

        return predict, left, only_right


if __name__ == '__main__':
    getPredict()
