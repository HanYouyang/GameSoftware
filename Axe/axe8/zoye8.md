作业 8

作业截止时间
周日

讨论频道：
#a16

交作业方式：
本次作业 8 需要在项目中新建一个 axe8 目录，上交如下文件
axe8/x16asm.py
axe8/x16vm.py
axe8/factorial.a16

请注意
不要上传除了 .py 文件外的其他文件到仓库，使用 sourcetree 来确保这一点
使用 flake8 --max-line-length=120 命令来检查代码格式
确保你的模块顶层只有函数定义或者类定义，不能有任何暴露在外的其他变量
确保你的代码可以正确实现功能

根据本作业的描述，实现下面的内容
x16asm.machine_code(asm_code: str)
x16vm.run(memory: List[int])
axe8/factorial.a16
见下方描述

说明如下：

1，
在作业 7 中，我们实现了一个 x16 的函数 multiply
在 multiply 中我们使用了 3 个内存地址来暂存局部变量

问题在于我们硬编码了函数中使用的局部变量的内存地址
我们不可能知道那块地址是否被别的函数使用了
所以实际上那样的写法是不对的
我们需要有一个方法可以在函数调用期间有一块独立的内存，在函数返回后回收这块内存

之前的方案如下
1）每次函数调用，把返回的地址写入 f1 寄存器代表的内存中，并把 f1 + 2
2）每次函数返回，从 f1 - 2 处拿到返回地址

我们做一个小修改使得它能够支持函数内的局部内存，这样就可以实现嵌套函数调用和递归函数
1）假设函数内部要使用 3 字节内存作为局部变量，则在函数开始后由程序员手动让 f1 + 3
2）函数内部可以使用 3 字节的内存，也可以调用别的函数
3）函数返回时，让 f1 正确复位
4）注意，这个修改是写函数的程序员实现的

2，
我们这样手动计算函数偏移地址再调用的方法太过麻烦了
就像我们会给汇编器添加一个 .memory 而不是手动填充中间的空白内存一样
我们也应该给函数的调用和返回增加新的汇编语法

我们通常把这种非 cpu 指令的汇编语法称为 伪指令（看起来像是指令实际上是汇编器的辅助语法）
现在，给汇编器添加如下 2 个伪指令来使用函数

.call @multiply ; 调用函数 @multiply
.return 3 ; 函数返回，3 是函数内使用的局部内存的字节数，没有这个数字汇编器就没办法修正返回地址

3，
axe8/factorial.a16
这是一个 x16 汇编程序，它实现了一个递归函数 @factorial
@factorial 接受一个参数并返回它的阶乘，确保使用递归而不是循环来实现它
注意，我的自动测试程序会加上我的调用代码并检查结果（我会修改前三个字节来跳转到我的测试代码）
注意，你需要使用 .call .return 这两个伪指令来实现、测试函数


;先写出阶乘递归
def factorial(n):
    if  2 > n:
        return 1
    else:
        n_minus_1 = n - 1
        t = factorial(n_minus_1)
        t = multiply(t, n_minus_1)
        return t