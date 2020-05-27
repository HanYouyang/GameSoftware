周五晚 22:00



交作业方式：
本次作业需要在项目中新建一个 axe10 目录，上交如下文件
axe10/x16asm.py
axe10/x16vm.py
axe10/drawpoint.a16



根据本作业的描述，实现下面的内容

1,
为汇编器和虚拟机新增 2 条指令
这两条新增的指令应该十分钟内写出来测试好
00010001    ; shift_right
            ; 下面的例子中，假设 a1 中存储的是 20(0b00010100)
            ; 执行 shift_right 后会把 a1 设置为 10(0b00001010)
            ; 相当于 a1 >>= 1
            ; shift_right a1
"其实可以使用的是直接除以2？？？"
00010011    ; and
            ; 下面的例子中，相当于 a3 = a1 & a2
            ; and a1 a2 a3
"此处直接使用的是python的and逻辑？？？"
https://axe3.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E5.B7.B2.E8.A7.A3.E5.86.B3.5D.E9.A2.98.E7.9B.AE1.E7.9A.84.20and.20.E4.B8.8D.E6.98.8E.E7.99.BD
这次作业没有用上and的功能，所以可以暂时先这么认为


2,
增加函数多参数功能
目前的函数通过 a1 a2 两个寄存器传递参数，是不够用的
假设我们要传递 4 个参数给函数，目前的方案做不到，所以需要进行修改
我们可以将需要传递的参数全部存放在当前函数的局部变量中
这样用 f1 减去相应的字节数，就能访问到 4 个参数了

因为函数的定义和调用都是程序员完成的，所以这只是一个约定
这个东西无法理解的话，一定要在 chat 问清楚
https://axe3.kybmig.cc/#narrow/stream/36-axe10/topic/.E9.87.8D.E6.96.B0.E8.AF.BB.E9.A2.98.E5.8F.91.E7.8E.B0.E5.88.86.E6.AD.A7
这条说明我们约定的到底是什么意思，我们需要的约定是什么情况下的
https://axe3.kybmig.cc/#narrow/stream/36-axe10/topic/.E5.8F.98.E9.87.8F.E9.80.9A.E8.BF.87.E5.B1.80.E9.83.A8.E5.8F.98.E9.87.8F.E5.AD.98.E5.82.A8.EF.BC.8C.E5.87.BD.E6.95.B0.20.E5.A6.82.E4.BD.95.E5.A4.9A.E6.AC.A1.E8.B0.83.E7.94.A8.EF.BC.9F
这里有两个方法的简易理解版本
https://axe3.kybmig.cc/#narrow/stream/36-axe10/topic/.E3.80.90.E5.B7.B2.E8.A7.A3.E5.86.B3.E3.80.91.E5.AF.B9.E9.A2.98.E7.9B.AE2.E7.9A.84.E7.90.86.E8.A7.A3
说的约定是到底参数的入栈顺序是什么样的？
根据下面题目要写成.call @func x1 x2这样方便函数调用

完整.call实现
https://axe3.zulip.kybmig.cc/#narrow/stream/34-a16/topic/.E6.88.91.E8.AE.A4.E4.B8.BA.E7.9A.84.E5.AE.8C.E6.95.B4.20.2Ecall.E5.AE.9E.E7.8E.B0

伪指令实现
https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E5.88.86.E4.BA.AB.5D.20.E4.BC.AA.E6.8C.87.E4.BB.A4.E5.AE.9E.E7.8E.B0


3,
实现汇编程序 axe10/drawpoint.a16
本文件包含如下函数

@function_draw_point
它有 2 个参数分别是 x y
它会在屏幕指定的 x y 处画一个点（颜色你自己定，无所谓）

https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.E4.BD.9C.E4.B8.9A10.2E3.20.E7.9A.84.E7.96.91.E9.97.AE
一共两个部分
第一部分就是写一个可以给指定位置内存赋值的函数，通过这个函数可以赋值颜色
第二部分就是把这个指定位置转化成x，y，取出指定位置的颜色。在pygame的相应位置把点画出来

https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E5.88.86.E4.BA.AB.5D.E5.A6.82.E4.BD.95.E4.B8.80.E6.AD.A5.E6.AD.A5.E5.AE.9E.E7.8E.B0.E4.BC.AA.E6.8C.87.E4.BB.A4
一步步实现伪指令

https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E5.88.86.E4.BA.AB.5D.20Mac.20.E5.A4.9A.E8.BF.9B.E7.A8.8B.E6.89.A7.E8.A1.8C.E6.B1.87.E7.BC.96.20.E6.9B.B4.E6.96.B0.E5.B1.8F.E5.B9.95
多进程执行汇编
https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E5.88.86.E4.BA.AB.5DScreen.E7.B1.BB.2C.20pygame.E7.94.BB.E5.9B.BE
screen类的Pygame画图实现
https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.5B.E8.AE.B0.E5.BD.95.5D.20pygame.20.E5.92.8C.20vm.20.E4.BA.92.E7.9B.B8.E9.85.8D.E5.90.88.E6.9D.A5.E5.87.BA.E6.9C.A8.E6.96.A7.E7.9A.84.E7.AC.AC.E4.B8.80.E6.AD.A5
pygame与vm结合

https://axe3.zulip.kybmig.cc/#narrow/stream/36-axe10/topic/.E5.85.B3.E4.BA.8E.E9.A2.98.E7.9B.AE.E6.84.8F.E6.80.9D/near/8890
draw是VM自动完成的，他会在刷新周期内检查显存有没有被更新，汇编要做的只是更新显存的内容




https://axe3.zulip.kybmig.cc/#narrow/stream/34-a16/topic/.5B.E5.B7.B2.E8.A7.A3.E5.86.B3.5D.E5.85.A8.E5.B1.80.E5.8F.98.E9.87.8F.E8.AE.BE.E8.AE.A1
全局变量和局部变量待区分

https://axe3.zulip.kybmig.cc/#narrow/stream/34-a16/topic/.5B.E8.A7.A3.E5.86.B3.5D.E4.B8.8D.E7.9F.A5.E9.81.93.E5.A6.82.E4.BD.95.E6.8A.8Apygame.E7.9A.84.E7.82.B9.E5.87.BB.E4.BA.8B.E4.BB.B6.E5.92.8C.E6.B1.87.E7.BC.96.E4.BB.A3.E7.A0.81.E7.BB.93.E5.90.88.E8.B5.B7.E6.9D.A5
cpu每执行多少次，就调用一次screen

https://axe3.zulip.kybmig.cc/#narrow/stream/34-a16/topic/.5B.E6.8F.90.E9.97.AE.5D.E7.94.BB.E5.9B.BE.E5.A4.AA.E6.85.A2.E5.A6.82.E4.BD.95.E8.A7.A3.E5.86.B3
画图的具体位置如何，要自己写一个screen出来










































