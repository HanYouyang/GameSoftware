# 作业讨论频道：
# #vm

# 我们对内存的使用做如下约定
# 把前 1024 字节留空，用于函数调用时暂存信息
# 所以头 3 个字节(jump 1 字节，后面的地址 2 字节)的指令固定如下，这样 cpu 加载后会从内存 1024 开始执行代码
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
#
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
class Axecpux16(object):
    def __init__(self, memory):
        self.memory = memory
        self.regs = {
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'pa': 0,
            'f1': 0,  # pa内存位置专用寄存器
            'c1': 0,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }
        self.regs_name = {
            0: 'pa',
            80: 'f1',
            16: 'a1',
            32: 'a2',
            48: 'a3',
            64: 'c1',
        }
        self.op_name = {
            0: 'set',
            1: 'load',
            2: 'add',
            3: 'save',
            4: 'compare',
            5: 'jump_if_less',
            6: 'jump',
            7: 'save_from_register',
            8: 'set2',
            9: 'load2',
            10: 'add2',
            11: 'save2',
            12: 'subtract2',
            13: 'load_from_register',
            14: 'load_from_register2',
            15: 'save_from_register2',
            16: 'jump_from_register',
            255: 'halt',
        }
        self.op_lens = {
            # 这里就是对多少asm_code里面操作进行读取
            # memory自己加入相应内容
            # 但是label是一开始asm_code里面加入的
            'halt': 0,
            'save_from_register2':  2,
            'save_from_register':   2,
            'load_from_register2':  2,
            'load_from_register':   2,
            'jump_from_register':   1,
            # 'jump_if_great': 1,
            'jump_if_less': 2,
            'jump': 2,
            'compare': 2,
            'save': 2,  # 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
            'load': 2,  # 改成16位2字节内存
            'add': 3,
            'set': 2,
            'set2': 3,# 带寄存器的不用变动长度，但是带数字的必须变化
            'load2': 3,
            'add2': 3,  # 和substract2一样存疑 事实上得一个个改回来
            'save2': 3,# 带地址的因为被拆成数字也得+1
            'subtract2': 3,
            # '.memory': 1,
            # '.return': 1,
            # '.call': 1,  # 根据下面修改 因为提前调用了clearnote
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


    def run(self):
        while True:
            pa = self.regs['pa']
            print('pa now ', pa)
            print('self.regs now', self.regs)
            op_num = self.memory[pa]
            # print('op_num now ', op_num)

            op = self.op_name[op_num]
            print('op now', op)

            if op == 'halt':
                break
            elif op == 'set': # 往下顺延此处获得数字
                reg = self.memory[pa + 1] # 这里的paj就是上面没有变化的pa
                reg_name = self.regs_name[reg]
                value = self.memory[pa + 2]
                self.regs[reg_name] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'set2': # 往下顺延此处获得数字
                reg = self.memory[pa + 1] # 这里的paj就是上面没有变化的pa
                reg_name = self.regs_name[reg]
                v1 = self.memory[pa + 2]
                v2 = self.memory[pa + 3]
                value = self.combine_memory_u16(v1, v2)
                self.regs[reg_name] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'load': # 往下顺延此处获得数字
                loc_num = self.memory[pa + 1]
                value = self.memory[loc_num]
                reg = self.memory[pa + 2] # 获得a1名字
                reg_name = self.regs_name[reg]
                self.regs[reg_name] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'load2': # 往下顺延此处获得数字
                loc1 = self.memory[pa + 1]
                loc2 = self.memory[pa + 2]
                loc_num = self.combine_memory_u16(loc1, loc2)
                v1 = self.memory[loc_num]
                v2 = self.memory[loc_num + 1]
                value = self.combine_memory_u16(v1, v2)
                reg = self.memory[pa + 3] # 获得a1名字
                reg_name = self.regs_name[reg]
                self.regs[reg_name] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'add':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_3 = self.memory[pa + 3]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_3_name = self.regs_name[reg_3]
                reg_1_value = self.regs[reg_1_name]
                reg_2_value = self.regs[reg_2_name]
                reg_3_value = reg_1_value + reg_2_value
                self.regs[reg_3_name] = reg_3_value
            elif op == 'add2':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_3 = self.memory[pa + 3]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_3_name = self.regs_name[reg_3]
                reg_1_value = self.regs[reg_1_name]
                reg_2_value = self.regs[reg_2_name]
                reg_3_value = reg_1_value + reg_2_value
                self.regs[reg_3_name] = reg_3_value
            elif op == 'subtract2':
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_3 = self.memory[pa + 3]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_3_name = self.regs_name[reg_3]
                reg_1_value = self.regs[reg_1_name]
                reg_2_value = self.regs[reg_2_name]
                reg_3_value = reg_1_value - reg_2_value
                self.regs[reg_3_name] = reg_3_value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'save':  # 往下顺延此处获得数字
                reg = self.memory[pa + 1]  # 获得a1名字
                reg_name = self.regs_name[reg]
                value = self.regs[reg_name]
                loc_num = self.memory[pa + 2]
                self.memory[loc_num] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'save2':
                reg = self.memory[pa + 1]
                reg_name = self.regs_name[reg]
                value = self.regs[reg_name]
                v1, v2 = self.split_memory_u16(value)
                loc1 = self.memory[pa + 2]
                loc2 = self.memory[pa + 3]
                loc_num = self.combine_memory_u16(loc1, loc2)
                self.memory[loc_num] = v1
                self.memory[loc_num + 1] = v2
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'compare':
                reg_1 = self.memory[pa + 1]
                reg_1_name = self.regs_name[reg_1]
                reg_1_value = self.regs[reg_1_name]
                reg_2 = self.memory[pa + 2]
                reg_2_name = self.regs_name[reg_2]
                reg_2_value = self.regs[reg_2_name]
                #  0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
                if  reg_1_value < reg_2_value:
                    self.regs['c1'] = 0
                elif reg_1_value > reg_2_value:
                    self.regs['c1'] = 2
                else:
                    self.regs['c1'] = 1
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'jump':
                v1 = self.memory[pa + 1]
                v2 = self.memory[pa + 2]
                loc_num = self.combine_memory_u16(v1, v2)
                self.regs['pa'] = loc_num
            elif op == 'jump_if_less':
                v1 = self.memory[pa + 1]
                v2 = self.memory[pa + 2]
                loc_num = self.combine_memory_u16(v1, v2)
                if self.regs['c1'] == 0:
                    self.regs['pa'] = loc_num
                else:
                    self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'load_from_register':
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_1_value = self.regs[reg_1_name]
                self.regs[reg_2_name] = self.memory[reg_1_value]
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'load_from_register2':
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_1_value = self.regs[reg_1_name]
                print('reg_1_value now', reg_1_value)
                # reg_2_value = self.regs[reg_2_name]
                v1 = self.memory[reg_1_value]
                v2 = self.memory[reg_1_value + 1]
                value = self.combine_memory_u16(v1, v2)
                print('v1 v2 and vaue now', v1, v2, value)
                self.regs[reg_2_name] = value
                self.regs['pa'] += self.op_lens[op] + 1
            elif op == 'save_from_register':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_2_value = self.regs[reg_2_name]
                self.memory[reg_2_value] = self.regs[reg_1_name]
            elif op == 'save_from_register2':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_1_value = self.regs[reg_1_name]
                reg_2_value = self.regs[reg_2_name]
                v1, v2 = self.split_memory_u16(reg_1_value)
                self.memory[reg_2_value] = v1
                self.memory[reg_2_value + 1] = v2
            elif op == 'jump_from_register':
                reg_1 = self.memory[pa + 1]
                reg_1_name = self.regs_name[reg_1]
                reg_1_value = self.regs[reg_1_name]
                self.regs['pa'] = reg_1_value

        return self.regs, self.memory


# 1 问题在于compare_if_less不能跳转
# 改变当前的jump方式
# 2 问题在于1083步跳出来直到1111并不能解决问题
# 如果寄存器里面有pa，那么计算pa的时候，尤其在保存函数返回位置的时候
# 必须先加入pa和op_lens的运算，否则内容上计算会出现偏差
# 但是如果寄存器的值需要计算的比如jump_from_regs时候必须得使用自己的内容
