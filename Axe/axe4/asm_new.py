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
# asm_code = """
# ; 分号开始到行尾表示注释
# ; 相应的汇编代码如下
# ; 数字 表示数字
# ; @数字 表示内存地址
# ; 我们假设第一行代码是从地址 0 开始
# ;
# set a1 1 ; 这里是内存地址 0 第一条指令
# set a2 2
# save a1 @100
# save a2 @101
# load @100 a1
# load @101 a2
# add a1 a2 a3
# save a3 @102
# compare a1 a2
# jump_if_great @label1 ; 这里 @label1 表示的是下面 @label1 的内存地址
# add a3 a2 a1
# ; 下面 @label1 是一个地址标记，需要汇编器自己算出来具体的数字
# @label1
# add a3 a1 a2
# """
# 根据上面的资料，实现下面的函数

# class Asm():
#
def symble_table():
    regs = {
                'pa': '00000000',
                'f1': '01010000',  # pa内存位置专用寄存器
                'a1': '00010000',
                'a2': '00100000',
                'a3': '00110000',
                'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
            }
    ops = {
        'halt': '11111111',
        'jump_from_register': '00010000',
        'save_from_register': '00000111',
        'load_from_register': '00001101',
        'jump_if_less': '00000101',
        'jump': '00000110',
        'compare': '00000100',
        'save': '00000011',
        'load': '00000001',
        'add': '00000010',
        'set': '00000000',
        'set2': '00001000',
        'load2': '00001001',
        'add2': '00001010',
        'save2': '00001011',
        'subtract2': '00001100',
        'load_from_register2': '00001110',
        'save_from_register2': '00001111',
    }
    op_lens = {
        # 这里就是对多少asm_code里面操作进行读取
        # memory自己加入相应内容
        # 但是label是一开始asm_code里面加入的
        'halt': 0,
        'save_from_register2': 2,  # 是用小端来存么
        'save_from_register': 2,
        'load_from_register2': 2,  # 这个寄存器应该几位不知
        'load_from_register': 2,
        'jump_from_register': 1,  # 存疑后面是几位
        'jump_if_great': 1,
        'jump_if_less': 1,
        'jump': 1,
        'compare': 2,
        'save': 2,  # 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
        'load': 2,  # 改成16位2字节内存
        'add': 3,
        'set': 2,
        'set2': 2,
        'load2': 2,
        'add2': 3,  # 和substract2一样存疑 事实上得一个个改回来
        'save2': 2,
        'subtract2': 3,
        '.memory': 1,
        '.return': 1,
        '.call': 1,  # 根据下面修改 因为提前调用了clearnote
    }
    return regs, ops, op_lens

def memory_address(code_1):
    a = code_1[1:]
    print('a now', a)
    try:
        m = int(a)
        return m
    except ValueError as e:
        return a
def clear_notes(asm):
    lines = asm.split('\n')
    new_lines = ''''''
    for line in lines:
        if ';' in line:
            num = line.index(';')
            line = line[:num]
        new_lines += line + '\n'
        # print('new_lines now', new_lines)
    final_asm = new_lines
    return final_asm

def machine_code_asm(asm):
    """
    asm 是汇编语言字符串
    返回 list, list 中每个元素是一个 1 字节的数字
    """
    memory = []
    regs, ops, op_lens = symble_table()
    # print('regs', regs)
    op_len = 0
    label_dict = {}
    asm = clear_notes(asm)
    lines = asm.split('\n')# 注意按行分割不然后面只拿到第一行
    # print('lines now', lines)
    for line in lines:

        if line.strip() == '':
            # 空行就跳过
            continue

        print('line now', line)
        code = line.split()

        if code[0][:1] == ';':
            continue
            # 其实这里是鸡肋因为不会有读取这里的分支

        if code[0][:1] == '@':
            # 对上来就是单行的@label直接放到字典里面给出坐标记录
            label_dict[code[0][1:]] = op_len
            # print('memory now', memory)
            print('label_dict now', label_dict)
            continue

        op = code[0]
        op_num = int(ops[op], 2)
        op_len += op_lens[op] + 1
        if op == 'set':
            reg = code[1]
            r = int(regs[reg], 2)
            value = int(code[2])
            memory.append(op_num)
            memory.append(r)
            memory.append(value)
        elif op == 'load':
            address = int(code[1][1:])
            reg = code[2]
            r = int(regs[reg], 2)
            memory.append(op_num)
            memory.append(address)
            memory.append(r)
        elif op == 'add':
            reg1 = code[1]
            r1 = int(regs[reg1], 2)
            reg2 = code[2]
            r2 = int(regs[reg2], 2)
            reg3 = code[3]
            r3 = int(regs[reg3], 2)
            memory.append(op_num)
            memory.append(r1)
            memory.append(r2)
            memory.append(r3)
        elif op == 'save':
            reg = code[1]
            r = int(regs[reg], 2)
            address = int(code[2][1:])
            memory.append(op_num)
            memory.append(r)
            memory.append(address)
        elif op == 'compare':
            reg1 = code[1]
            r1 = int(regs[reg1], 2)
            reg2 = code[2]
            r2 = int(regs[reg2], 2)
            memory.append(op_num)
            memory.append(r1)
            memory.append(r2)
        elif op == 'jump_if_less':
            # 更改下面的内容是为了将label暂时存到memory中
            # 第二遍遍历再放进去
            address = memory_address(code[1])
            # address = int(code[1][1:])
            memory.append(op_num)
            memory.append(address)
        elif op == 'jump':
            address = memory_address(code[1])
            # address = int(code[1][1:])
            memory.append(op_num)
            memory.append(address)
        elif op == 'halt':
            print('final now')
            memory.append(255)


    for i, e in enumerate(memory):
        if e in label_dict:
            # 对已经在字典里面存好的label进行精准替换
            memory[i] = label_dict[e]

    return memory


#
# if __name__ == '__main__':
#     machine_code_asm()