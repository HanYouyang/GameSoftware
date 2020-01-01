提问表格要按照下面的格式来填写
1, 标题
格式为「课程名称|课次|题目|有问题的步骤」
比如「axe3|课2|axe5|第2作业」

2, 你的目的
「怎么用run函数调用pygame的画图功能，从而在一个循环中完成刷新」

3, 你的想法和思路
1.x和y都是用`dict['a2']`计算出来
2.每读到一个前面156个的list当中的函数操作，具体表现为读到字典中对应的匿名函数比如`do['set'](ele1, ele2)`等操作后，更新一次画图的pygame.draw.screen中的x和y

4, 描述你的问题
1.在遍历前156个元素的list时候，已经是在循环中，这样的情况下如何做到步进中跟main()中不断循环的while running:联系起来？
2.难道自己重构个类出来写update比较好？但是update也得有步进调用pygame.draw.screen，这个思路也可以给个方式验证
3.输出没有，不知道如何下手

5, 你的实现代码

```buildoutcfg
'''
memory 是一个长度为 256 的数字数组，也就是作业 4 生成的机器码
这是一个虚拟机程序
run 函数将 memory 数组视为内存，并且以地址 0 为起点执行这个内存
你需要用变量来模拟寄存器，模拟程序的执行
下方会给出一个用于测试的 memory 例子并更新在 #general
你现在可以用自己生成的内容来测试
注意，memory 目前只能支持 256 字节，因为 pa 寄存器只有 8 位
'''
from typing import List

class RunVM():
    def __init__(self):
        self.memory = [
0b00000000, # set
0b00100000, # a2
0b10011100, # 156, 左上角第一个像素
0b00000000, # set
0b00110000, # a3
0b00010110, # 22, 用于斜方向设置像素，每两排设置一个
0b00000000, # set
0b00010000, # a1
0b11000011, # 红色，我们用一字节表示 RGBA 颜色，所以这里红色就是 11000011
0b00000111, # save_from_register
# 这个指令需要使用两个寄存器
# 把 a1 的值（这里是 0b11000011）写入 a2 表示的内存中
# 这里 a2 中是 156，这个指令会把内存地址 156 中的值设置为 0b11000011
0b00010000, # a1
0b00100000, # a2
# 设置新像素点
0b00000010, # add
0b00100000, # a2
0b00110000, # a3
0b00100000, # a2
0b00000111, # save_from_register
0b00010000, # a1
0b00100000, # a2
# 设置新像素点
0b00000010, # add
0b00100000, # a2
0b00110000, # a3
0b00100000, # a2
0b00000111, # save_from_register
0b00010000, # a1
0b00100000, # a2
# 设置新像素点
0b00000010, # add
0b00100000, # a2
0b00110000, # a3
0b00100000, # a2
0b00000111, # save_from_register
0b00010000, # a1
0b00100000, # a2
# 设置新像素点
0b00000010, # add
0b00100000, # a2
0b00110000, # a3
0b00100000, # a2
0b00000111, # save_from_register
0b00010000, # a1
0b00100000, # a2
# 结果是在显示屏上显示一条斜线，一共 5 个红色的像素点
0b11111111, # 停机
]
        self.instruAction = {
    '11111111': 'halt',
    '00000111': 'save_from_register',
    '00000110': 'jump',
    '00000101': 'jump_if_great',
    '00000100': 'compare',
    '00000011': 'save',
    '00000001': 'load',
    '00000010': 'add',
    '00000000': 'set',
}
        self.instruLen = {
    'halt': 0,
    'save_from_register': 2,
    'jump': 1,
    'jump_if_great': 1,
    'compare': 2,  # 要改2？
    'save': 2,  # 要改2？
    'load': 2,  # 要改2？
    'add': 3,  # 要改2？
    'set': 2,  # 要改2？
}
        self.registerLoc = {
    '00000000': 'pa',
    '01010000': 'f1',  # pa内存位置专用寄存器
    '00010000': 'a1',
    '00100000': 'a2',
    '00110000': 'a3',
    '01000000': 'c1',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
}
        self.varAll = {
        'a1':0,
        'a2':0,
        'a3':0,
        'pa':0,
        'f1':0,
        'c1':0,
    }
        self.readLen = 0
    def decodeByOri(self):
        machineMemory = []
        for i in self.memory:
            i = bin(i)
            newI = str(i).replace('0b', '').zfill(8)
            machineMemory.append(newI)
        return machineMemory
    def transAction(self):
        realList = []
        readLen = 0
        for i in range(len(self.machineList)):
            ele = self.machineList[i]
            if readLen > 0:
                readLen -= 1
                readEle = self.registerLoc[ele]
                realList.append(readEle)
            else:
                if ele in self.instruAction:
                    eleAction = self.instruAction[ele]
                    realList.append(eleAction)
                    readLen = self.instruLen[eleAction] - 1
                else:
                    ele = int(ele, 2)
                    realList.append(ele)
        # print('realList', realList)
        # print('len(realList)', len(realList))
        realList = realList + [0] * (256 - len(realList))
        return realList
        # print('realList after', realList)
    def doListGenr(self):
        # 寄存器用字典保存值
        def doSet(a1, a2):
            self.varAll[a1] = a2  # set 指令，用于给寄存器存一个数字
            return self.varAll[a1]
        def doAdd(a1, a2, a3):
            self.varAll[a1] = self.varAll[a1] + self.varAll[a2]  # add 指令, 操作寄存器两个数字相加
            return self.varAll[a1]
        def doSaveFrom(a1, a2):
            self.memDone[a2] = self.varAll[a1]
            return self.memDone[a2]
            # save_from_register这个指令需要使用两个寄存器,把 a1 的值（这里是 0b11000011）写入 a2 表示的内存中
            # 这里 a2 中是 156，这个指令会把内存地址 156 中的值设置为 0b11000011
        def doLoad(a1, a2):
            self.memDone[a2] = self.memAction[a1]  # load 指令，用于把内存中的一个数字读到寄存器中
            # 暂时不知道memory里面是什么？应该是一个
            return a2
        def doCompare(a1, a2):
            self.varAll['c1'] = 0  # ; 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
            if a1 > a2:
                self.varAll['c1'] = 2
            elif a1 == a2:
                self.varAll['c1'] = 1
        def doSave(a1, a2):
            self.memDone[a2] = self.varAll[a1]  # save 指令，用手把寄存器的一个数字存到内存地址中
            return self.memDone[a2]
        def doJumpIf(a1):
            return self.memDone[a1]
        def doJump(a1):
            return self.memDone[a1]
        def doHalt():
            return
        doList = {
            'set': doSet,
            'add': doAdd,
            'compare': doCompare,
            'halt': doHalt,
            'save_from_register': doSaveFrom,
            'jump': doJump,
            'jump_if_great': doJumpIf,
            'save': doSave,
            'load': doLoad,
        }
        return doList
    def setup(self):
        self.machineMemory = self.decodeByOri()
        self.actionList = self.transAction()
        self.memAction = self.actionList[1: 156]
        self.memDone = self.actionList[156: 256]
        # print('memAction now', memAction)
        # print('memDone before', memDone)
        self.doList = self.doListGenr()
    def breakOut(self):
        return
    def forBody(self, ele, idx):
        if self.readLen > 0:
            self.readLen -= 1
            # continue
        else:
            if ele == 'halt':
                self.breakOut()
            do = self.doList[ele]
            ele1 = self.actionList[idx + 1]
            ele2 = self.actionList[idx + 2]
            ele3 = self.actionList[idx + 3]
            self.readLen = self.instruLen[ele]
            if self.readLen == 1:
                do(ele1)
            elif self.readLen == 2:
                do(ele1, ele2)
            elif self.readLen == 3:
                do(ele1, ele2, ele3)
    def run(self):
        self.readLen = 0
        for idx, ele in enumerate(self.actionList):
            self.forBody(idx, ele)

            x = (self.varAll['a2'] - 156) % 10
            y = math.floor((self.varAll['a2'] - 156) / 10)
            pygame.draw.rect(self.screen, (255, 0, 0), (10 * x, 10 * y, 50, 50))

# memory = memory + [0] * (256 - len(memory))

import pygame
import random
import math
def main():
    vm = RunVM()

    width, height = 500, 500
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    fps = 30
    red = (255, 0, 0)

    while running:

        x = (varAll['a2'] - 156) % 10
        y = math.floor((varAll['a2'] - 156) / 10)
        pygame.draw.rect(screen, red, (10 * x, 10 * y, 50, 50))

        # varAll = run(memory)
        #
        # x = (varAll['a2'] - 156) % 10
        # y = math.floor((varAll['a2'] - 156) / 10)
        # print('x and y', x, y)
        # x = random.randint(0, width - 1) * 10
        # y = random.randint(0, height - 1) * 10
        # position = (x, y)
        # color = varAll['a1']
        # r = random.randint(0, 255)
        # g = random.randint(0, 255)
        # b = random.randint(0, 255)
        # color = (r, g, b)
        # screen.set_at(position, color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)
if __name__ == '__main__':
    main()




```
