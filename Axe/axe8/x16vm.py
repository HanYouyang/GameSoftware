class X16vm():
    def __init__(self):
        self.regs = {
            0: 'pa',
            80: 'f1',
            16: 'a1',
            32: 'a2',
            48: 'a3',
            64: 'c1'
        }
        self.reg_num = {
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'pa': 0,
            'f1': 0,
            'c1': 0,
        }
        self.action = {
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
        # 此处16位的vm就意味着所有内存和寄存器数字操作都是用16位去读
        self.act_len = {
            'halt':               0,
            'save_from_register': 2,
            'load_from_register': 2,
            'jump_from_register': 1,# 存疑后面是几位
            'jump_if_great':      2,
            'jump_if_less':       2,# 此时是操作长度和读取长度不同
            'jump':               2,
            'compare':            2,
            'save':               3,# 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
            'load':               3,# 改成16位2字节内存?? 还是改成2位
            'add':                3,
            'set':                3,
            'set2':               3,
            'add2':               3,  # 和substract2一样存疑
            'subtract2':          3,  # 开始居然是6也能运行？？？
            'save2':              3,
            'load2':              3,
            'load_from_register2':2,  # 这个寄存器应该几位不知
            'save_from_register2':2,  # 是用小端来存么
        }

    def get_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value

    def set_memory_u16(self, number: int):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high

    def run(self, memory, start):
        mem_act = memory[start :] # 因为包含跳转 需要用数字来给出内存读取位置

        read_len = 0 # 每个操作读长 预先设置为0
        self.reg_num['pa'] = start
        for i, e in enumerate(mem_act):

            if read_len > 0:
                read_len -= 1
                continue

            if read_len == 0: # 此时没有读长按照原操作进行
                print('self.reg_num now', self.reg_num)
                if mem_act[i]:
                    v = mem_act[i]
                    act = self.action[v]
                    read_len = self.act_len[act]
                    self.reg_num['pa'] = start + i + read_len + 1# read_len + 1  start + i +
                    print('act now', act)
                    print('pa now', self.reg_num['pa'])

                else:
                    print('mem_act[i] now', mem_act[i])

            if act == 'set':
                reg_val = mem_act[i + 1]
                reg = self.regs[reg_val]
                v1 = mem_act[i + 2]
                # v2 = mem_act[i + 3]
                v2 = 0
                value = self.get_memory_u16(v1, v2)
                self.reg_num[reg] = value
            elif act == 'set2':
                reg_val = mem_act[i + 1]
                reg = self.regs[reg_val]
                v1 = mem_act[i + 2]
                v2 = mem_act[i + 3]
                value = self.get_memory_u16(v1, v2)
                self.reg_num[reg] = value
            elif act == 'add':
                reg_val_1 = mem_act[i + 1]
                reg_val_2 = mem_act[i + 2]
                reg_val_3 = mem_act[i + 3]
                reg1 = self.regs[reg_val_1]
                reg2 = self.regs[reg_val_2]
                reg3 = self.regs[reg_val_3]
                low1, high1 = self.set_memory_u16(self.reg_num[reg1])
                low2, high2 = self.set_memory_u16(self.reg_num[reg2])
                value = low1 + low2
                low3, high3 = self.get_memory_u16(value)
                self.reg_num[reg3] = low3
            elif act == 'add2':
                reg_val_1 = mem_act[i + 1]
                reg_val_2 = mem_act[i + 2]
                reg_val_3 = mem_act[i + 3]
                reg1 = self.regs[reg_val_1]
                reg2 = self.regs[reg_val_2]
                reg3 = self.regs[reg_val_3]
                self.reg_num[reg3] = self.reg_num[reg1] + self.reg_num[reg2]
            elif act == 'subtract2':
                reg_val_1 = mem_act[i + 1]
                reg_val_2 = mem_act[i + 2]
                reg_val_3 = mem_act[i + 3]
                reg1 = self.regs[reg_val_1]
                reg2 = self.regs[reg_val_2]
                reg3 = self.regs[reg_val_3]
                self.reg_num[reg3] = self.reg_num[reg1] - self.reg_num[reg2]
            elif act == 'save':
                # save a2 @100（类似 save_from_register
                # 把 a2 寄存器的值
                # 存放到 100 这个内存地址
                # 先取到 a2 的值，拆成高低位
                # 根据机器码拆成的两位数字，还原出 65532
                # memory[65532] = 低位
                # memory[65533] = 高位
                reg_val = mem_act[i + 1]
                reg = self.regs[reg_val]
                reg_value = self.reg_num[reg]
                low, high = self.set_memory_u16(reg_value)
                v1 = mem_act[i + 2]
                v2 = mem_act[i + 3]
                value = self.get_memory_u16(v1, 0)
                mem_loc_1 = value
                mem_loc_2 = value + 1
                memory[mem_loc_1] = low
                memory[mem_loc_2] = high #应该上面是v2有关是0
            elif act == 'save2':
                # save2 a2 @65532（类似 save_from_register2
                # 把 a2 寄存器的值
                # 存放到 65532 这个内存地址
                # 先取到 a3 的值，拆成高低位
                # 根据机器码拆成的两位数字，还原出 65532
                # memory[65532] = 低位
                # memory[65533] = 高位
                reg_val = mem_act[i + 1]
                reg = self.regs[reg_val]
                reg_value = self.reg_num[reg]
                low, high = self.set_memory_u16(reg_value)
                v1 = mem_act[i + 2]
                v2 = mem_act[i + 3]
                value = self.get_memory_u16(v1, v2)
                mem_loc_1 = value
                mem_loc_2 = value + 1
                memory[mem_loc_1] = low
                memory[mem_loc_2] = high
            elif act == 'load':
                # load @100 a2（类似 load_from_register2把 65534 这个内存地址的值取出来，
                # 存到 a2 寄存器 根据机器码拆成的两位数字，还原出 65534 内存地址
                # 低位值在65534，高位值在65535
                # 根据高低位值，还原出本来的值并存到 a2
                v1 = mem_act[i + 1]
                v2 = mem_act[i + 2]
                value_1 = self.get_memory_u16(v1, 0)
                mem_loc_1 = value_1
                mem_loc_2 = value_1 + 1
                low = memory[mem_loc_1]
                high = memory[mem_loc_2]
                value_2 = self.get_memory_u16(low, high)
                reg_val = mem_act[i + 3]
                reg = self.regs[reg_val]
                self.reg_num[reg] = value_2
            elif act == 'load2':
                # load2 @65534 a2（类似 load_from_register2把 65534 这个内存地址的值取出来，
                # 存到 a2 寄存器 根据机器码拆成的两位数字，还原出 65534 内存地址
                # 低位值在65534，高位值在65535
                # 根据高低位值，还原出本来的值并存到 a2
                v1 = mem_act[i + 1]
                v2 = mem_act[i + 2]
                value_1 = self.get_memory_u16(v1, v2)
                mem_loc_1 = value_1
                mem_loc_2 = value_1 + 1
                low = memory[mem_loc_1]
                high = memory[mem_loc_2]
                value_2 = self.get_memory_u16(low, high)

                reg_val = mem_act[i + 3]
                reg = self.regs[reg_val]
                self.reg_num[reg] = value_2
            elif act == 'load_from_register':
                # ; 下面的例子中，假设 a1 是 100，则会把内存地址 100 中的值读取到 a2 寄存器中
                # ; 注意，这个指令读取 2 字节
                # load_from_register a1 a2
                # 把 a1 存放的内存地址的值，存到 a2 寄存器里
                #  先取到 a1 的值，比如值是 100,
                # 内存地址 100 这个位置存放的值，低位值在100，高位值在101
                # （因为往内存地址里写入值的时候是这样写入的，所以相应的，取也是这么取，然后再还原）
                # 所以 a2 的 value 是 memory[100] + memory[101]
                reg_val_1 = mem_act[i + 1]
                reg1 = self.regs[reg_val_1]
                value_1 = self.reg_num[reg1] # 先取到 a1 的值
                mem_loc_1 = value_1
                mem_loc_2 = value_1 + 1
                low = memory[mem_loc_1]
                high = memory[mem_loc_2] # 是0？？？
                value_2 = self.get_memory_u16(low, high)
                reg_val_2 = mem_act[i + 2]
                reg2 = self.regs[reg_val_2]
                self.reg_num[reg2] = value_2
            elif act == 'load_from_register2':
                # ; 下面的例子中，假设 a1 是 100，则会把内存地址 100 中的值读取到 a2 寄存器中
                # ; 注意，这个指令读取 2 字节

                # load_from_register2 a1 a2
                # 把 a1 存放的内存地址的值，存到 a2 寄存器里
                #  先取到 a1 的值，比如值是 777,
                # 内存地址 777 这个位置存放的值，低位值在777，高位值在778
                # （因为往内存地址里写入值的时候是这样写入的，所以相应的，取也是这么取，然后再还原）
                # 所以 a2 的 value 是 memory[777] + memory[778]
                reg_val_1 = mem_act[i + 1]
                reg1 = self.regs[reg_val_1]
                value_1 = self.reg_num[reg1] # 先取到 a1 的值
                print('value_1 now', value_1)
                mem_loc_1 = value_1
                mem_loc_2 = value_1 + 1
                print('mem_loc_1 and mem_loc_2 now', mem_loc_1, mem_loc_2)
                low = memory[mem_loc_1]
                high = memory[mem_loc_2]
                value_2 = self.get_memory_u16(low, high)
                reg_val_2 = mem_act[i + 2]
                reg2 = self.regs[reg_val_2]
                self.reg_num[reg2] = value_2
            elif act == 'save_from_register2':
                # save_from_register2 a3 f1
                # 将 a3 寄存器里的值存到 f1 存放的内存地址里 先取到 a3 的值，
                # 拆成 高低位 取到 f1 的值，如果值是 100 那么
                # memory[100] = 低位
                # memory[101] = 高位
                reg_num_1 = mem_act[i + 1]
                reg1 = self.regs[reg_num_1]
                reg_val_1 = self.reg_num[reg1] # 先取到 a3 的值
                low, high = self.set_memory_u16(reg_val_1) # 拆成 高低位

                reg_num_2 = mem_act[i + 2]
                reg2 = self.regs[reg_num_2]
                reg_val_2 = self.reg_num[reg2] # 取到 f1 的值
                mem_loc_1 = reg_val_2
                mem_loc_2 = reg_val_2 + 1
                memory[mem_loc_1] = low
                memory[mem_loc_2] = high
            elif act == 'compare': # ; 0 表示小于，1 表示相等，2 表示大于
                reg_val_1 = mem_act[i + 1]
                reg_val_2 = mem_act[i + 2]
                reg1 = self.regs[reg_val_1]
                reg2 = self.regs[reg_val_2]
                value_1 = self.reg_num[reg1]
                value_2 = self.reg_num[reg2]
                self.reg_num['c1'] = 1
                if value_1 > value_2:
                    self.reg_num['c1'] = 2
                elif value_1 < value_2:
                    self.reg_num['c1'] = 0
            elif act == 'jump_if_less': # 此处理解的是执行位置的内存也就是列表改变
                v1 = mem_act[i + 1]
                v2 = mem_act[i + 2]
                val = self.get_memory_u16(v1, v2)
                jump_to_num = val
                if  self.reg_num['c1'] == 0:
                    return self.run(memory, jump_to_num)

            elif act == 'jump': # 此处理解的是执行位置的内存也就是列表改变
                v1 = mem_act[i + 1]
                v2 = mem_act[i + 2]
                val = self.get_memory_u16(v1, v2)
                jump_to_num = val
                self.run(memory, jump_to_num)
                break

            elif act == 'jump_from_register': # 假设 a1 中存储的是 20，程序会跳转到 20
                reg_val = mem_act[i + 1]
                reg = self.regs[reg_val]
                jump_to_num = self.reg_num[reg]
                self.run(memory, jump_to_num)
                break

            elif act == 'halt':
                self.reg_num['pa'] -= 1 # 目前存疑只是为了计算暂时留下来
                break

        final_mem = memory
        return self.reg_num, final_mem

def run(memory):
    x16vm = X16vm()
    reg_num, final_mem= x16vm.run(memory, 0)
    return reg_num, final_mem

if __name__ == '__main__':
    main()



