from ll1 import LL1
from lexical_analyzer import lex_analysis
from recursion import recurse
from semantic_analysis import semantic_analysis

token_path = "../intermediate/token.txt"
tree_path = "../intermediate/syntax_tree.txt"
gram_path = "../source/grammar.txt"
symbol_path = "../intermediate/symbol_table.txt"


def main(file_name="source_program"):
    print("run main")
    using_ll1 = True
    pro_path = f"../source/{file_name}.txt"
    print("in main" + pro_path)
    is_wrong = lex_analysis(pro_path, token_path)
    if is_wrong:
        print("词法分析错误")
        return False
        # exit()
    message = ""
    if using_ll1:
        # is_wrong = ll1(token_path, tree_path)
        ll1 = LL1(gram_path, token_path, tree_path)
        ll1.run()
        is_wrong, message = ll1.show_error(show=True)
    else:
        is_wrong = recurse(token_path)
    if is_wrong:
        print("语法分析失败")
        return False
    print("语法分析成功")
    is_wrong = semantic_analysis(tree_path)
    if is_wrong:
        print("语义分析失败")
        return False
    else:
        print("语义分析成功")
        with open("../intermediate/error.txt", "w") as file:
            file.seek(0)
            file.truncate()
    return True


if __name__ == '__main__':
    main()
