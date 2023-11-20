import tkinter as tk
import os
from src.main import main

# 创建主窗口
root = tk.Tk()
root.title("编译原理课程设计")
root.geometry("800x800")

chooseMapping = {
    "正确源程序01": "right_01",
    "正确源程序02": "right_02",
    "词法错误": "error_01",
    "语法错误": "error_02",
    "语义错误": "error_03",
}
# 创建一个下拉框和选项
var = tk.StringVar(root)
var.set("源代码类型")
dropdown = tk.OptionMenu(root, var, "正确源程序01", "正确源程序02", "词法错误",
                         "语法错误", "语义错误")
dropdown.grid(row=0, column=0, sticky="EW")
selected_value = ""


def callback(*args):
    global selected_value
    selected_value = var.get()
    print(chooseMapping[selected_value])
    if not main(chooseMapping[selected_value]):
        show_error_msg()
    else:
        show_program()


var.trace("w", callback)


# 定义按钮点击事件
def show_token():
    # pass
    text.delete("1.0", tk.END)
    with open("../intermediate/token.txt", "r") as f:
        content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


def show_syntax_tree():
    text.delete("1.0", tk.END)
    with open("../intermediate/syntax_tree.txt", "r") as f:
        content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


def show_symbol_table():
    text.delete("1.0", tk.END)
    with open("../intermediate/symbol_table.txt", "r") as f:
        content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


def show_error_msg():
    text.delete("1.0", tk.END)
    with open("../intermediate/error.txt", "r") as f:
        content = f.read()
        text.delete("1.0", tk.END)
        text.tag_config("red", foreground="red")
        text.insert(tk.END, content, "red")


def show_program():
    global selected_value

    with open(f"../source/{chooseMapping[selected_value]}.txt", "r",encoding="utf-8") as f:
        content = f.read()
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


program_button = tk.Button(root, text="源代码", command=show_program)
program_button.grid(row=1, column=0, padx=10, pady=10)
# 创建按钮
token_button = tk.Button(root, text="Token", command=show_token)
token_button.grid(row=1, column=1, padx=10, pady=10)

syntax_tree_button = tk.Button(root, text="语法树", command=show_syntax_tree)
syntax_tree_button.grid(row=1, column=2, padx=10, pady=10)

symbol_table_button = tk.Button(root, text="符号表", command=show_symbol_table)
symbol_table_button.grid(row=1, column=3, padx=10, pady=10)

symbol_table_button = tk.Button(root, text="错误信息", command=show_error_msg)
symbol_table_button.grid(row=1, column=4, padx=10, pady=10)

# 创建文本框所在的Frame
text_frame = tk.Frame(root)
text_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

# 创建Label来显示行数
line_label = tk.Text(text_frame, width=3, padx=2, takefocus=0, highlightthickness=0, borderwidth=0, background='#f0f0f0', state='disabled')
line_label.pack(side='left', fill='y')



# 创建文本框
text = tk.Text(root, height=50, width=100)
text.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

scrollbar = tk.Scrollbar(root, orient="vertical", command=text.yview)
scrollbar.grid(row=2, column=5, sticky="NS")

# 将Scrollbar与Text控件进行绑定
text.config(yscrollcommand=scrollbar.set)
# 运行主循环
root.mainloop()
