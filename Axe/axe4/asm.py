# 根据上课所讲的 CPU、指令、机器语言、汇编的原理，实现一个汇编器程序
# 汇编器是用于把汇编语言翻译为机器语言的程序
#
# 汇编语言资料如下：
# 我们假设 AxePU 有如下寄存器
# 00000000 ; pa（program address） 寄存器
# 00010000 ; a1
# 00100000 ; a2
# 00110000 ; a3
# 01000000 ; c1，保存比较结果的寄存器
# ; 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
# 01010000 ; f1 寄存器，保存存放 pa 的内存的地址
#
# 我们需要的指令如下
# 00000000 ; set 指令，用于给寄存器存一个数字
# 00000001 ; load 指令，用于把内存中的一个数字读到寄存器中
# 00000010 ; add 指令
# 00000011 ; save 指令，用手把寄存器的一个数字存到内存地址中
# save_from_register
# 这个指令需要使用两个寄存器
# 把 a1 的值（这里是 0b11000011）写入 a2 表示的内存中
# 这里 a2 中是 156，这个指令会把内存地址 156 中的值设置为 0b11000011
# 00000100 ; compare 指令，用于比较 a1 a2 的大小并且保存结果到 c1
# 00000101 ; jump_if_great 指令
# 00000110 ; jump
#

# 根据上面的资料，实现下面的函数
class ASMdecode():
    def __init__(self):
        self.asm = """
                ; 分号开始到行尾表示注释
                ; 相应的汇编代码如下
                ; 数字 表示数字
                ; @数字 表示内存地址
                ; 我们假设第一行代码是从地址 0 开始
                ;
                set a1 1 ; 这里是内存地址 0 第一条指令
                set a2 2
                save a1 @100
                save a2 @101
                load @100 a1
                load @101 a2
                add a1 a2 a3
                save a3 @102
                compare a1 a2
                jump_if_great @label1 ; 这里 @label1 表示的是下面 @label1 的内存地址
                add a3 a2 a1
                ; 下面 @label1 是一个地址标记，需要汇编器自己算出来具体的数字
                @label1
                add a3 a1 a2
                """
        self.asm2 = """
            set a1 1
            set a2 2
            add a1 a2 a3
            save a3 @102
            @label2
            compare a1 a2
            jump_if_great @label1
            add a3 a2 a1
            jump @label2
            @label1
            add a3 a1 a2
            """
    def clearAsm(self):
        asmCut = self.asm.splitlines()
        asmNew = []
        for ele in asmCut:
            findReplace = ele.find(';')
            if findReplace > 0:
                ele = ele[: findReplace]
            if ele == []:
                continue
            finalEle = ele.split()
            for _ in finalEle:
                asmNew.append(_)
        return asmNew
    def findLabelIndex(self):
        asmLabelIndex = self.clearAsm()
        labelDict = {}
        countIndex = -1
        for i in asmLabelIndex:
            countIndex += 1
            isSingleLabel = asmLabelIndex[countIndex - 1] != 'jump' and asmLabelIndex[countIndex - 1] != 'jump_if_great'
            if i[: 6] == '@label' and isSingleLabel:
                labelDict[i] = countIndex
        print('labelDict final', labelDict)
        return labelDict
    def machine_code(self):
        asmNew = self.clearAsm()
        #print('asmNew', asmNew)
        labelDict = self.findLabelIndex()
        instructAction = {
            'jump': '00000110',
            'jump_if_great': '00000101',
            'compare': '00000100',
            'save': '00000011',
            'load': '00000001',
            'add': '00000010',
            'set': '00000000',
        }
        registerLocation = {
            'pa': '00000000',
            'f1': '01010000',  # pa内存位置专用寄存器
            'a1': '00010000',
            'a2': '00100000',
            'a3': '00110000',
            'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }

        finaList = []
        for i in asmNew:
            if i in instructAction:
                insAct = int(instructAction[i], 2)
                finaList.append(insAct)
            elif i in registerLocation:
                regLoc =  int(registerLocation[i], 2)
                finaList.append(regLoc)
            elif i[: 6] == '@label':
                labelIndex = labelDict[i]
                finaList.append(labelIndex)
            elif i[0] == '@':
                numLater = int(i[1:])
                finaList.append(numLater)
            else:
                finaList.append(int(i))
        return finaList

if __name__ == '__main__':
    finalList = ASMdecode()
    final = finalList.machine_code()
    print('final', final)
