class X16vm():
    def __init__(self, memory):
        self.registers = {
            'pa': '00000000',
            'f1': '01010000',  # pa内存位置专用寄存器
            'a1': '00010000',
            'a2': '00100000',
            'a3': '00110000',
            'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
            'a11':'0001000000010000',
            'a22':'0010000000100000',
            'a33':'0011000000110000',
        }
        self.regNum = {
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'pa': 0,
            'f1': 0,
            'c1': 0,
            'a11': 0,
            'a22': 0,
            'a33': 0,
        }
        self.action = {
            'halt':               '11111111',
            'jump_from_register': '00010000',
            'save_from_register': '00000111',
            'load_from_register': '00001101',
            'jump_if_great':      '00000101',
            'jump':               '00000110',
            'compare':            '00000100',
            'save':               '00000011',
            'load':               '00000001',
            'add':                '00000010',
            'set':                '00000000',
            'set2':               '00001000',
            'load2':              '00001001',
            'add2':               '00001010',
            'save2':              '00001011',
            'subtract2':          '00001100',
            'load_from_register2':'00001110',
            'save_from_register2':'00001111',
        }
        self.actLen = {
            'halt':               0,
            'save_from_register': 2,
            'load_from_register': 2,
            'jump_from_register': 1,# 存疑后面是几位
            'jump_if_great':      1,
            'jump_if_less':       1,# 此时是操作长度和读取长度不同
            'jump':               1,
            'compare':            2,
            'save':               2,# 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
            'load':               2,# 改成16位2字节内存?? 还是改成2位
            'add':                3,
            'set':                2,
            'set2':               2,
            'load2':              2,
            'add2':               3,  # 和substract2一样存疑
            'save2':              2,
            'subtract2':          3,# 开始居然是6也能运行？？？
            'load_from_register2':2,  # 这个寄存器应该几位不知
            'save_from_register2':2,  # 是用小端来存么
        }
        self.labelDict = self.allLabel(memory)
    def get_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value
    def set_memory_u16(self, number: int):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high
    def giveNum(self, e):
        biStr = self.action[e]
        val = int(biStr, 2)
        return val
    def allLabel(self, memory):
        labelDict = {}
        for i, e in enumerate(memory):
            e = str(e)
            if (not e.isdigit()) and e[0] == '@' and (not e[1:].isdigit()) and memory[i - 1] != 'jump' and memory[i - 1] != 'jump_if_less':
                labelDict[e] = i
                # labelDict[e] = i + 1024
        return labelDict
    def run(self, memory, start):
        memAct = memory[start :]

        readLen = 0
        act = memAct[0]
        diff = 0
        for i, e in enumerate(memAct):
            pa = self.regNum['pa']
            if diff > 0:
                diff -= 1
                readLen == 0
                continue
            if readLen > 0:
                readLen -= 1
                continue

            if readLen == 0:
                if memAct[pa]:
                    act = memAct[pa]
                    if act in self.labelDict:
                        continue
                    if act in self.actLen:
                        readLen = self.actLen[act]
                else:
                    break

            # if readLen == 0:
            #     if memAct[i]:
            #         act = memAct[i]
            #         if act in self.labelDict:
            #             continue
            #         if act in self.actLen:
            #             readLen = self.actLen[act]
            #     else:
            #         break
            # if act == 'set':
                # self.regNum['pa'] += self.actLen['set']
                # act = memAct[i]
                # reg = memAct[i + 1]
                # self.regNum[reg] = memAct[i + 2]
            if act == 'set2':
                # act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg = memAct[i + 1]
                self.regNum[reg] = memAct[i + 2]
            elif act == 'halt':
                self.regNum['pa'] += self.actLen[act] + 1
                return
            elif e in self.labelDict: # 其实这个不再act里面也是直接跳出
                print('e now', e)
                return
            # elif act == 'add':
            #     act = memAct[i]
            #     self.regNum['pa'] += self.actLen[act] + 1
            #     reg1 = memAct[i + 1]
            #     reg2 = memAct[i + 2]
            #     reg3 = memAct[i + 3]
            #     self.regNum[reg3] = self.regNum[reg2] + self.regNum[reg1]
            elif act == 'add2':
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg1 = memAct[i + 1]
                reg2 = memAct[i + 2]
                reg3 = memAct[i + 3]
                self.regNum[reg3] = self.regNum[reg2] + self.regNum[reg1]
            elif act == 'subtract2':
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg1 = memAct[i + 1]
                reg2 = memAct[i + 2]
                reg3 = memAct[i + 3]
                self.regNum[reg3] = self.regNum[reg2] - self.regNum[reg1]
            # elif act == 'save': # 对最终读取和写入内存的操作都设置为memory开始
            #     act = memAct[i]
            #     memLoc = int(memAct[i + 1][1 :])
            #     reg = memAct[i + 2]
            #     memory[memLoc] = self.regNum[reg]
            elif act == 'save2':
                # save2 a2 @65532（类似 save_from_register2
                # 把 a2 寄存器的值
                # 存放到 65532 这个内存地址
                # 先取到 a3 的值，拆成高低位
                # 根据机器码拆成的两位数字，还原出 65532
                # memory[65532] = 低位
                # memory[65533] = 高位
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg = memAct[i + 1]
                val = self.regNum[reg]
                low, high = self.set_memory_u16(val)
                memLoc1 = int(memAct[i + 2][1 :])
                memLoc2 = int(memAct[i + 2][1 :]) + 1
                memory[memLoc1] = low
                memory[memLoc2] = high
            # elif act == 'load': # load @100 a1
            #     act = memAct[i]
            #     reg = memAct[i + 1]
            #     memLoc = int(memAct[i + 2][1:])
            #     self.regNum[reg] = memory[memLoc]
            elif act == 'load2':
                # load2 @65534 a2（类似 load_from_register2把 65534 这个内存地址的值取出来，
                # 存到 a2 寄存器 根据机器码拆成的两位数字，还原出 65534 内存地址
                # 低位值在65534，高位值在65535
                # 根据高低位值，还原出本来的值并存到 a2
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                memLoc1 = int(memAct[i + 1][1:])
                memLoc2 = int(memAct[i + 1][1:]) + 1
                val = self.get_memory_u16(memory[memLoc1], memory[memLoc2])
                reg = memAct[i + 2]
                self.regNum[reg] = val
            # elif act == 'load_from_register': # 下面的例子中，假设 a1 是 100，则会把内存地址 100 中的值读取到 a2 寄存器中
            #     act = memAct[i]
            #     reg1 = memAct[i + 1]
            #     memLoc = self.regNum[reg1]
            #     reg2 = memAct[i + 2]
            #     self.regNum[reg2] = memory[memLoc]
            elif act == 'load_from_register2':
                # load_from_register2 a1 a2
                # 把 a1 存放的内存地址的值，
                # 存到 a2 寄存器里 先取到 a1 的值，比如值是 777,
                # 内存地址 777 这个位置存放的值，低位值在777，高位值在778
                # （因为往内存地址里写入值的时候是这样写入的，所以相应的，取也是这么取，然后再还原）
                # 所以 a2 的 value 是 memory[777] + memory[778]
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg1 = memAct[i + 1]
                memLoc = self.regNum[reg1]
                reg2 = memAct[i + 2]
                self.regNum[reg2] = memory[memLoc]
            elif act == 'save_from_register2':
                # save_from_register2 a3 f1
                # 将 a3 寄存器里的值存到 f1 存放的内存地址里 先取到 a3 的值，
                # 拆成 高低位 取到 f1 的值，如果值是 100 那么
                # memory[100] = 低位
                # memory[101] = 高位
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg1 = memAct[i + 1]
                val = self.regNum[reg1]
                low, high = self.set_memory_u16(val)
                reg2 = memAct[i + 2]
                memLoc1 = self.regNum[reg2]
                memLoc2 = self.regNum[reg2] + 1
                memory[memLoc1] = low
                memory[memLoc2] = high
            elif act == 'compare': # ; 0 表示小于，1 表示相等，2 表示大于
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg1 = memAct[i + 1]
                reg2 = memAct[i + 2]
                self.regNum['c1'] = 1
                if self.regNum[reg1] > self.regNum[reg2]:
                    self.regNum['c1'] = 2
                elif self.regNum[reg1] < self.regNum[reg2]:
                    self.regNum['c1'] = 0
            elif act == 'jump_if_less': # 此处理解的是执行位置的内存也就是列表改变
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                if self.regNum['c1'] == 0:
                    return
                jumpTo = memAct[pa + 1]
                if memAct[pa + 1][1:].isdigit():
                    self.regNum['pa'] = int(memAct[i + 1][1:])
                elif self.labelDict[jumpTo]:
                    self.regNum['pa'] = int(self.labelDict[jumpTo])
                memLoc = self.regNum['pa']
                self.run(memory, memLoc)
            elif act == 'jump': # 此处理解的是执行位置的内存也就是列表改变
                # act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                jumpTo = memAct[pa + 1]# 从i + 1往后改出来的
                if memAct[pa + 1][1 :].isdigit():
                    self.regNum['pa'] = int(memAct[i + 1][1 :])
                elif self.labelDict[jumpTo]:
                    self.regNum['pa'] = int(self.labelDict[jumpTo])
                memLoc = self.regNum['pa']
                self.run(memory, memLoc)
            elif act == 'jump_from_register': # 假设 a1 中存储的是 20，程序会跳转到 20
                act = memAct[i]
                self.regNum['pa'] += self.actLen[act] + 1
                reg = memAct[i + 1]
                memLoc = self.regNum[reg]
                self.run(memory, memLoc)
        finalMem = memory
        return self.regNum, self.labelDict, finalMem

def run(memory):
    x16vm = X16vm(memory)
    regNum, labelDict, finalMem= x16vm.run(memory, 0)
    return regNum, labelDict, finalMem

if __name__ == '__main__':
    main()



