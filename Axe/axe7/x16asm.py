class X16asm():
    def __init__(self):
        self.registersBefore = {
             '00000000':'pa',
             '01010000':'f1',  # pa内存位置专用寄存器
             '00010000':'a1',
             '00100000':'a2',
             '00110000':'a3',
             '01000000':'c1',
             '0001000000010000':'a11',# 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
             '0010000000100000':'a22',
             '0011000000110000':'a33',
        }
        self.actionBefore = {
            '11111111':'halt',
             '00010000':'jump_from_register',
             '00000111':'save_from_register',
             '00001101':'load_from_register',
                  # '00000101':'jump_if_great',
                  '00000101': 'jump_if_less',
                           '00000110':'jump',
                        '00000100':'compare',
                           '00000011':'save',
                           '00000001':'load',
                            '00000010':'add',
                            '00000000':'set',
                           '00001000':'set2',
                          '00001001':'load2',
                           '00001010':'add2',
                          '00001011':'save2',
                      '00001100':'subtract2',
            '00001110':'load_from_register2',
            '00001111':'save_from_register2',
        }
        self.actLen = {
            'halt':               0,
            'save_from_register': 2,
            'load_from_register': 2,
            'jump_from_register': 1,# 存疑后面是几位
            'jump_if_great':      2,
            'jump_if_less':       2,
            'jump':               2,
            'compare':            2,
            'save':               3,# 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
            'load':               3,# 改成16位2字节内存
            'add':                3,
            'set':                2,
            'set2':               3,
            'load2':              4,
            'add2':               6,  # 和substract2一样存疑
            'save2':              4,
            'subtract2':          6,
            'load_from_register2':4,  # 这个寄存器应该几位不知
            'save_from_register2':3,  # 是用小端来存么
        }
    # 由于我们前面 1024 字节都需要留空，所以我们要增加一个汇编语法来方便生成机器码
    # 具体见下方的简单例子
    # 它实现了 jump 1024 占用前三字节，空 1021 字节
    #
    # jump @1024
    # ; 下面的 .memory 是一个 x16 汇编标记
    # ; 它表明下面的代码要放到内存 1024 的地方开始
    # ; 汇编器会用 0 填充之间的空余内存
    # .memory 1024
    # ; 代码
    def get_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value
    def set_memory_u16(self, number: int):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high
    def string_int_with_8(string):
        mod = 0b11111111
        return int(string) & mod
    def string_int_with_16(string):
        mod1 = 0b0000000011111111
        i = int(string)
        low = i & mod1
        high = i >> 8
        return low, high
    def splitStr(self, asm_code):
        asmSplit = asm_code.splitlines()
        asmSplitFinal = []
        for ele in asmSplit:
            asmSplitFinal += ele.split()
        return asmSplitFinal

    def machine_code(self, asm_code: str):
        # low, high = self.set_memory_u16(1024)
        # startCode = ['00000110', low, high]
        # firstPart = startCode + ['00000000'] * (1024 - len(startCode))

        finalCode = []
        readLen = 0
        asm_code = self.splitStr(asm_code)
        act = self.actionBefore[asm_code[0]]
        for i, e in enumerate(asm_code):
            if readLen > 0:
                readLen -= 1
                continue

            if readLen == 0:
                act = self.actionBefore[e]
                readLen = self.actLen[act]

            if act == 'set':
                act = self.actionBefore[e]
                reg = self.registersBefore[asm_code[i + 1]]
                val = int(asm_code[i + 2], 2)
                finalCode.append(act)
                finalCode.append(reg)
                finalCode.append(val)
            elif act == 'halt':
                finalCode.append(act)
                break
            elif act == 'add':
                act = self.actionBefore[e]
                reg1 = self.registersBefore[asm_code[i + 1]]
                reg2 = self.registersBefore[asm_code[i + 2]]
                reg3 = self.registersBefore[asm_code[i + 3]]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
                finalCode.append(reg3)
            elif act == 'save':
                act = self.actionBefore[e]
                reg = self.registersBefore[asm_code[i + 1]]
                v1 = int(asm_code[i + 2], 2)
                v2 = int(asm_code[i + 3], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                finalCode.append(act)
                finalCode.append(reg)
                finalCode.append(valStr)
            elif act == 'load':
                act = self.actionBefore[e]
                v1 = int(asm_code[i + 1], 2)
                v2 = int(asm_code[i + 2], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                reg = self.registersBefore[asm_code[i + 3]]
                finalCode.append(act)
                finalCode.append(valStr)
                finalCode.append(reg)
            elif act == 'compare':# 这里体现只读不操作
                act = self.actionBefore[e]
                reg1 = self.registersBefore[asm_code[i + 1]]
                reg2 = self.registersBefore[asm_code[i + 2]]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
            elif act == 'load':
                act = self.actionBefore[e]
                v1 = int(asm_code[i + 1], 2)
                v2 = int(asm_code[i + 2], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                reg = self.registersBefore[asm_code[i + 3]]
                finalCode.append(act)
                finalCode.append(valStr)
                finalCode.append(reg)
            elif act == 'jump_if_less':
                act = self.actionBefore[e]
                v1 = int(asm_code[i + 1], 2)
                v2 = int(asm_code[i + 2], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                finalCode.append(act)
                finalCode.append(valStr)
            elif act == 'jump':
                act = self.actionBefore[e]
                v1 = int(asm_code[i + 1], 2)
                v2 = int(asm_code[i + 2], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                finalCode.append(act)
                finalCode.append(valStr)
            elif act == 'set2':
                act = self.actionBefore[e]
                reg = self.registersBefore[asm_code[i + 1]]
                v1 = int(asm_code[i + 2], 2)
                v2 = int(asm_code[i + 3], 2)
                value = self.get_memory_u16(v1, v2)
                # valStr = str(value)
                finalCode.append(act)
                finalCode.append(reg)
                finalCode.append(value)
            elif act == 'add2':
                act = self.actionBefore[e]
                regstr1 = asm_code[i + 1] + asm_code[i + 2]
                reg1 = self.registersBefore[regstr1]
                regstr2 = asm_code[i + 3] + asm_code[i + 4]
                reg2 = self.registersBefore[regstr2]
                regstr3 = asm_code[i + 5] + asm_code[i + 6]
                reg3 = self.registersBefore[regstr3]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
                finalCode.append(reg3)
            elif act == 'load2':
                act = self.actionBefore[e]
                v1 = int(asm_code[i + 1], 2)
                v2 = int(asm_code[i + 2], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                regstr = asm_code[i + 3] + asm_code[i + 4]
                reg = self.registersBefore[regstr]
                finalCode.append(act)
                finalCode.append(valStr)
                finalCode.append(reg)
            elif act == 'save2':
                act = self.actionBefore[e]
                regstr = asm_code[i + 1] + asm_code[i + 2]
                reg = self.registersBefore[regstr]
                v1 = int(asm_code[i + 3], 2)
                v2 = int(asm_code[i + 4], 2)
                value = self.get_memory_u16(v1, v2)
                valStr = '@' + str(value)
                finalCode.append(act)
                finalCode.append(reg)
                finalCode.append(valStr)
            elif act == 'subtract2':
                act = self.actionBefore[e]
                regstr1 = asm_code[i + 1] + asm_code[i + 2]
                reg1 = self.registersBefore[regstr1]
                regstr2 = asm_code[i + 3] + asm_code[i + 4]
                reg2 = self.registersBefore[regstr2]
                regstr3 = asm_code[i + 5] + asm_code[i + 6]
                reg3 = self.registersBefore[regstr3]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
                finalCode.append(reg3)
            elif act == 'load_from_register2':
                act = self.actionBefore[e]
                regstr1 = asm_code[i + 1] + asm_code[i + 2]
                reg1 = self.registersBefore[regstr1]
                regstr2 = asm_code[i + 3] + asm_code[i + 4]
                reg2 = self.registersBefore[regstr2]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
            elif act == 'load_from_register':
                act = self.actionBefore[e]
                regstr1 = asm_code[i + 1]
                reg1 = self.registersBefore[regstr1]
                regstr2 = asm_code[i + 2]
                reg2 = self.registersBefore[regstr2]
                finalCode.append(act)
                finalCode.append(reg1)
                finalCode.append(reg2)
            elif act == 'jump_from_register':
                act = self.actionBefore[e]
                regstr = asm_code[i + 1]
                reg = self.registersBefore[regstr]
                finalCode.append(act)
                finalCode.append(reg)

        return finalCode

def machine_code(asm_code):
    x16asm = X16asm()
    finalCode = x16asm.machine_code(asm_code)
    return finalCode
if __name__ == '__main__':
    machine_code()



