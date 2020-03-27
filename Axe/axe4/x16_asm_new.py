# 根据本作业的描述，实现下面两个函数
# x16asm.machine_code(asm_code: str)
# x16vm.run(memory: List[int])
#
# jump @1024
# ;
# ; 从第四个字节开始，剩下的 1021 个字节都是我们的
# ;
# ;
# ;
# ;
# ; 下面是内存 1024 开始的内容
# ; 初始化 f1 寄存器，这是需要我们手动做的
# set2 f1 3 ; 设置 f1 寄存器为 3，我们用这个寄存器里的内存地址来保存函数返回后应该跳转的地址
# ;
# ; 我们要在接下来的的内存存放函数定义，所以直接跳转到 @function_end 避免执行函数
# jump @function_end
# ;
# ; 定义一个函数 function_multiply，接受两个参数，返回两个数的乘积
# ; 参数通过 a1 a2 得到，返回值通过 a1 传给调用方
# @function_multiply
# set2 a3 2 ; 因为下面用 a2 < a3 做判断，所以 a3 从 2 开始
# ; 我们需要在循环中把 a3 + 1，并且把 a1 累加
# ; 由于我们只有 3 个通用寄存器可用，我们需要用 3 个内存来暂存 a1 a2 a3 的值
# ; 因为我们现在是自主决定使用所有内存，所以我们可以手动指定使用的内存区域
# ; 我们把 65534 65532 65530 这三个地址拿来存储 a1 a2 a3 的值
# ; 我们先保存 a1
# save2 a1 @65534
# @while_start ; 循环开始
# compare a2 a3 ;
# jump_if_less @while_end ; 一旦 a2 小于 a2，就结束循环
# ;
# ; 把 a2 保存到 65532, 然后利用 a2 把 a3+1
# save2 a2 @65532
# set2 a2 1
# add2 a3 a2 a3
# ;
# ; 把循环开始之前暂存的 a1 放到 a2 中然后累加到 a1
# load2 @65534 a2
# add2 a1 a2 a1
# ;
# ; 恢复 a2 的值并跳转到循环开始
# load2 @65532 a2
# jump @while_start
# @while_end
# ; 函数结束了，这时候 a1 存的就是 a1*a2 的值
# ; f1 寄存器里面存储的是函数调用前的地址，我们让 f1-2，然后把它取出来, 然后返回
# set2 a3 2
# subtract2 f1 a3 f1
# load_from_register2 f1 a2
# jump_from_register a2
# ;
# ;
# ; 所有函数定义结束的标记（但我们这个例子中，只有一个函数定义）
# @function_end
# ;
# ;
# ; 我们来调用前面的 multiply 函数
# set2 a1 300 ; a1 是 300
# set2 a2 10 ; a2 是 10
# ; 保存 pa 到 f1 所表示的内存中
# ; 请特别注意下面的写法
# ; save_from_register2 长度是 3 字节
# ; jump 长度是 3 字节
# ; set2 add2 各自占用 4 字节
# ; 所以我们用它们两句之前的 add2 来修正函数返回时候的正确地址(也就是 14)
# ; cpu 读了 add2 这句后就会把 pa + 4（add2 占用 4 字节）
# ; 然后才会执行 add2，所以执行 add2 这句的时候只需要把 pa + 6 就能指向 jump @function_multiply 的下一句
# set2 a3 14
# add2 pa a3 a3
# save_from_register2 a3 f1 ; 3 字节
# ; 保存后，要把 f1 的值 +2
# set2 a3 2 ; 4 字节
# add2 f1 a3 f1 ; 4 字节
# ; 跳转到函数
# jump @function_multiply ; 3 字节
# ; 函数返回了，这里的 a1 就是我们想要的返回值
# halt

class Asmblerx16(object):
    def __init__(self):
        self.regs = {
                'pa': '00000000',
                'f1': '01010000',  # pa内存位置专用寄存器
                'a1': '00010000',
                'a2': '00100000',
                'a3': '00110000',
                'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }
        self.ops = {
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
            '.memory': '00000000', # 此处填充不看内容是多少，后面也不append这里的操作所以是多少无所谓

        }
        self.op_lens = {

                'halt': 0,
                'save_from_register2': 2,  # 是用小端来存么
                'save_from_register': 2,
                'load_from_register2': 2,  # 这个寄存器应该几位不知
                'load_from_register': 2,
                'jump_from_register': 1,  # 存疑后面是几位
                'jump_if_great': 2,
                'jump_if_less': 2,
                'jump': 2,
                'compare': 2,
                'save': 2,  # 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
                'load': 2,  # 改成16位2字节内存
                'add': 3,
                'set': 2,
                'set2': 3,
                'load2': 3,
                'add2': 3,  # 和substract2一样存疑 事实上得一个个改回来
                'save2': 3,
                'subtract2': 3,
                '.memory': 0,
                '.return': 1,
                '.call': 1,  # 根据下面修改 因为提前调用了clearnote
            }

    def combine_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value

    def split_memory_u16(self, number):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high
    #
    def memory_address(self, code_1):
            a = code_1[1:]
            print('a now', a)
            try:
                m = int(a)
                return m
            except ValueError as e:
                return a

    def clear_notes(self, asm):
            lines = asm.split('\n')
            new_lines = ''''''
            for line in lines:
                if ';' in line:
                    num = line.index(';')
                    line = line[:num]
                new_lines += line + '\n'
            final_asm = new_lines
            return final_asm

    def machine_code_asm(self, asm):
        """
        asm 是汇编语言字符串
        返回 list, list 中每个元素是一个 1 字节的数字
        """
        memory = []
        regs = self.regs
        ops = self.ops
        op_lens = self.op_lens
        op_len = 0 # 计算距离开始位置的偏移量，用以下面计算label
        label_dict = {}
        asm = self.clear_notes(asm)
        lines = asm.split('\n')# 注意按行分割不然后面只拿到第一行
        for line in lines:

            if line.strip() == '':
                # 空行就跳过
                continue

            # print('line now', line)
            code = line.split()

            if code[0][:1] == ';':
                continue

            if code[0][:1] == '@':
                # 对上来就是单行的@label直接放到字典里面给出坐标记录
                label_dict[code[0][1:]] = op_len
                # print('memory now', memory)
                print('label_dict now', label_dict)
                continue

            op = code[0]
            op_value = int(ops[op], 2)
            op_len += op_lens[op] + 1
            if op == 'set':
                reg = code[1]
                r = int(regs[reg], 2)
                value = int(code[2])
                memory.append(op_value)
                memory.append(r)
                memory.append(value)
            elif op == 'set2':
                reg = code[1]
                r = int(regs[reg], 2)
                value = int(code[2])
                v1, v2 = self.split_memory_u16(value)
                memory.append(op_value)
                memory.append(r)
                memory.append(v1)
                memory.append(v2)
            elif op == 'load':
                address = int(code[1][1:])
                reg = code[2]
                r = int(regs[reg], 2)
                memory.append(op_value)
                memory.append(address)
                memory.append(r)
            elif op == 'load2':
                address_value = int(code[1][1:])
                v1, v2 = self.split_memory_u16(address_value)
                reg = code[2]
                r = int(regs[reg], 2)
                memory.append(op_value)
                memory.append(v1)
                memory.append(v2)
                memory.append(r)
            elif op == 'add':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                reg3 = code[3]
                r3 = int(regs[reg3], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
                memory.append(r3)
            elif op == 'add2':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                reg3 = code[3]
                r3 = int(regs[reg3], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
                memory.append(r3)
            elif op == 'subtract2':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                reg3 = code[3]
                r3 = int(regs[reg3], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
                memory.append(r3)
            elif op == 'save':
                reg = code[1]
                r = int(regs[reg], 2)
                address = int(code[2][1:])
                memory.append(op_value)
                memory.append(r)
                memory.append(address)
            elif op == 'save2':
                reg = code[1]
                r = int(regs[reg], 2)
                address = int(code[2][1:])
                v1, v2 = self.split_memory_u16(address)
                memory.append(op_value)
                memory.append(r)
                memory.append(v1)
                memory.append(v2)
            elif op == 'compare':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
            elif op == 'jump_if_less':
                # 更改下面的内容是为了将label暂时存到memory中
                # 第二遍遍历再放进去
                # address = self.memory_address(code[1]
                address = code[1][1:]
                if address.isdigit():
                    value = int(address)
                    v1, v2 = self.split_memory_u16(value)
                    memory.append(op_value)
                    memory.append(v1)
                    memory.append(v2)
                else:
                    memory.append(op_value)
                    memory.append(address)
                    memory.append(0)
            elif op == 'jump':
                # address = self.memory_address(code[1]
                address = code[1][1:]
                if address.isdigit():
                    value = int(address)
                    v1, v2 = self.split_memory_u16(value)
                    memory.append(op_value)
                    memory.append(v1)
                    memory.append(v2)
                else:
                    memory.append(op_value)
                    memory.append(address)
                    memory.append(0)
            elif op == 'halt':
                print('final now')
                memory.append(255)
            elif op == 'load_from_register':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
            elif op == 'load_from_register2':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
            elif op == 'save_from_register':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
            elif op == 'save_from_register2':
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                reg2 = code[2]
                r2 = int(regs[reg2], 2)
                memory.append(op_value)
                memory.append(r1)
                memory.append(r2)
            elif op == 'jump_from_register':  # 假设 a1 中存储的是 20，程序会跳转到 20
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                memory.append(op_value)
                memory.append(r1)
            elif op == '.memory':  # 假设 a1 中存储的是 20，程序会跳转到 20
                # jump @1024
                # ; 下面的 .memory 是一个 x16 汇编标记
                # ; 它表明下面的代码要放到内存 1024 的地方开始
                # ; 汇编器会用 0 填充之间的空余内存
                # .memory 1024
                # ; 代码
                value = int(code[1])
                len_before = len(memory)
                len_append = value - len_before
                memory = memory + [0] * len_append
                op_len += len_append - 1

        for i, e in enumerate(memory):
            if e in label_dict:
                # 字典这里其实不应该使用两位的值？？？？
                # print('e now', e)
                # 对已经在字典里面存好的label进行精准替换
                # memory[i] = label_dict[e]
                # 后面改动的时候，其实应该把大于256的内容分隔开补充进去
                value = int(label_dict[e])
                v1, v2 = self.split_memory_u16(value)
                memory[i] = v1
                memory[i + 1] = v2

        return memory

# 1 注意此处计算的结果与后面的vm是不同的
# 后面有几位"append"上去，就相应放上多少
# 只是此处需要-1因为开始有个+1
# 2 jump计算的时候既然提升了位数，那么就要提前补上0
# 这样自己第二遍可以继续放内容进去
# 3 .memory后面数字也可以加到计算内容中去
# 这样的label计算就可以使用自己的内容