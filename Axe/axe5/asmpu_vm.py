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
        self.machineList = self.decodeByOri()
        self.actionList = self.transAction()
        self.memAction = self.actionList[1: 156]
        self.memDone = self.actionList[156: 256]
        # print('memAction now', memAction)
        # print('memDone before', memDone)
        self.doList = self.doListGenr()
    def decodeByOri(self):
        machineMemory = []
        for i in self.memory:
            i = bin(i)
            newI = str(i).replace('0b', '').zfill(8)
            machineMemory.append(newI)
        return machineMemory
    def transAction(self):
        realList = []
        for i in range(len(self.machineList)):
            ele = self.machineList[i]
            if self.readLen > 0:
                self.readLen -= 1
                readEle = self.registerLoc[ele]
                realList.append(readEle)
            else:
                if ele in self.instruAction:
                    eleAction = self.instruAction[ele]
                    realList.append(eleAction)
                    self.readLen = self.instruLen[eleAction] - 1
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
            # return
            print('final now')
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
    def breakOut(self):
        # print('1', 1)
        return
        # continue
    def forBody(self, idx, ele):
        # self.actionList = self.transAction()
        if self.actionList[idx] == 'halt':
            print('do list over')
        elif self.readLen > 0:
            self.readLen -= 1
            # continue
        else:
            print('ele now', ele)
            do = self.doList[ele]
            ele1 = self.actionList[idx + 1]
            ele2 = self.actionList[idx + 2]
            ele3 = self.actionList[idx + 3]
            self.readLen = self.instruLen[ele]
            print('self.readLen now', self.readLen)
            print('do now', do)

            if self.readLen == 0:
                do()
            elif self.readLen == 1:
                do(ele1)
            elif self.readLen == 2:
                do(ele1, ele2)
            elif self.readLen == 3:
                do(ele1, ele2, ele3)
    def run(self, idx):
        # self.readLen = 0
        # for idx, ele in enumerate(self.actionList):
        if not self.actionList[idx]:
            return
        ele = self.actionList[idx]
        self.forBody(idx, ele)
        return self.varAll

# memory = memory + [0] * (256 - len(memory))

import pygame
import math
def main():
    vm = RunVM()
    idx = 0
    colotDict = {
        '00': 0,
        '01': 85,
        '10': 170,
        '11': 255,
    }

    width, height = 500, 500
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    fps = 30
    red = (255, 0, 0)

    while running:
        varAll = vm.run(idx)
        idx += 1
        x = (int(varAll['a2']) - 156) % 10 * 5
        y = math.floor((varAll['a2'] - 156) / 10) * 5

        colorA1 = bin(varAll['a1']).replace('0b', '')
        rD = colorA1[0 : 2]
        r = colotDict[rD]
        gD = colorA1[2 : 4]
        g = colotDict[gD]
        bD = colorA1[4 : 6]
        b = colotDict[bD]
        colorNow = (r, g, b)
        pygame.draw.rect(screen, colorNow, (10 * x, 10 * y, 50, 50))

        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
