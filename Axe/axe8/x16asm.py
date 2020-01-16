class X16asm():
    def __init__(self):
        self.act_len = {
            # 这里就是对多少asm_code里面操作进行读取
            # memory自己加入相应内容
            # 但是label是一开始asm_code里面加入的
            'halt':               0,
            'save_from_register2':2,  # 是用小端来存么
            'save_from_register': 2,
            'load_from_register2':2,  # 这个寄存器应该几位不知
            'load_from_register': 2,
            'jump_from_register': 1,# 存疑后面是几位
            'jump_if_great':      1,
            'jump_if_less':       1,
            'jump':               1,
            'compare':            2,
            'save':               2,# 用手把寄存器的一个数字存到内存地址中，注意这里的内存地址是一个 16 位的数字
            'load':               2,# 改成16位2字节内存
            'add':                3,
            'set':                2,
            'set2':               2,
            'load2':              2,
            'add2':               3,  # 和substract2一样存疑 事实上得一个个改回来
            'save2':              2,
            'subtract2':          3,
            '.memory':            1,
            '.return':            1,
            '.call':              1,
        }
        self.regs = {
            'pa': '00000000',
            'f1': '01010000',  # pa内存位置专用寄存器
            'a1': '00010000',
            'a2': '00100000',
            'a3': '00110000',
            'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }
        self.acts = {
            'halt':               '11111111',
            'jump_from_register': '00010000',
            'save_from_register': '00000111',
            'load_from_register': '00001101',
            'jump_if_less':       '00000101',
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

    def get_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value

    def set_memory_u16(self, number: int):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high

    # 先用带有伪指令的给出数组如何运转
    def clear_note(self, asm_code):
        asm_split = self.split_str_list(asm_code)

        # 分开list后再重新拼成字符串
        # 目的是后面用模板字符串补进来的时候计算方便不出错
        # 原则是先替换字符串这样获得所有的内容后再计算label的偏差值不会出错
        final_asm = []
        read_len = 0
        for i, e in enumerate(asm_split):
            if read_len > 0:
                read_len -= 1
                continue

            if e in self.act_len:
                lis_now = []
                len_now = self.act_len[e]
                read_len = len_now
                for j in range(0, len_now + 1):
                    lis_now.append(asm_split[i + j])
                st_now = ' '.join(lis_now)
                final_asm.append(st_now)
            elif e[0] == '@':# 除了在字典里面的还有部分是@function_end和@while_end等标记
                final_asm.append(e)
        # 重新拼成字符串
        final_asm = '\n'.join(final_asm)
        print('final_asm', final_asm)
        return final_asm

    def fake_act_pre(self, asm_code):
        asm_split_cut = asm_code.splitlines()

        new_asm_code = []
        for e in asm_split_cut:
            if e == '':
                continue
            e_sp = e.strip()
            # print('e now', e)
            new_e = e_sp.split()
            # print('new_e now', new_e)
            if new_e[0] == '.call':
                rep_func_name = new_e[1] # 模板字符串里面注释去掉 存在有影响
                target_str = '''
                    set2 a3 14
                    add2 pa a3 a3
                    save_from_register2 a3 f1
                    set2 a3 2
                    add2 f1 a3 f1
                    jump {fun_name}
                '''
                final_str = target_str.format(fun_name = rep_func_name)
                new_asm_code.append(final_str)
                continue
            elif new_e[0] == '.return':
                rep_func_num = int(new_e[1])
                target_str = '''
                    set2 a3 {fun_num}
                    subtract2 f1 a3 f1
                    set2 a3 2
                    subtract2 f1 a3 f1
                    load_from_register2 f1 a2
                    jump_from_register a2
                '''
                final_str = target_str.format(fun_num = rep_func_num)
                new_asm_code.append(final_str)
                continue

            new_asm_code.append(e)
        final_str_muti_lines = '\n'.join(new_asm_code)
        # print('final_str_muti_lines now', final_str_muti_lines)

        return final_str_muti_lines
    def split_str_list(self, asm_code):
        asm_split_cut = asm_code.splitlines()
        asm_split = []
        for e in asm_split_cut:
            idx = e.find(';')
            if idx >= 0:
                e_clear = e[: idx]
                asm_split += e_clear.split() # 尝试不分开组合起来分行 最终再调用一次分成数组的内容
            else:
                asm_split += e.split()
        return asm_split

    # 计算所有label给出一个直接跳过循环的机会
    def label_dict_gen(self, asm_code):
        label_dict = {}
        for i, e in enumerate(asm_code):# 现在的位置再后面可以修正
            right_loc = asm_code[i - 1] != 'jump' and asm_code[i - 1] != 'jump_if_less'
            not_num = not e[1 :].isdigit()
            if e[0] == '@' and not_num and right_loc: # and not_num and right_loc不写
                label_dict[e] = 1 # 只是用来记录出现和查询 用来跟jump后面的值关联
        return label_dict

    def machine_code(self, asm_code: str):
        asm_code = self.clear_note(asm_code)
        asm_code = self.fake_act_pre(asm_code)
        asm_code = self.split_str_list(asm_code)
        print('final list of asm_code', asm_code)
        # 先去掉注释 再填充内容
        label_dict = self.label_dict_gen(asm_code)

        memory = []# 要将机器操作转变为数字给vm读取
        read_len = 0 # 操作读长初始为0
        act = asm_code[0] # 初始操作
        for i, e in enumerate(asm_code):
            if read_len > 0:
                read_len -= 1
                continue

            if read_len == 0:
                if e in label_dict: # 因为两个jump的read_len已经避免遇到此时
                    label_dict[e] = len(memory) # 对当前的内存位置进行记录 但是内存直接删除掉
                    # 此处的标记位置举例就是function调用跳到此处调用 但是标记被删除
                    continue
                act = e
                print('act now', act)
                if act == 0:
                    continue
                read_len = self.act_len[act]

            # if act == 'set':
            #     act = e
            #     reg = asm_code[i + 1]
            #     val = int(asm_code[i + 2], 2)
            #     act_val = int(self.acts[act], 2)
            #     reg_val = int(self.regs[reg], 2)
            #     memory.append(act_val)
            #     memory.append(reg_val)
            #     memory.append(val)
            # elif act == 'add':
            #     act = e
            #     reg1 = asm_code[i + 1]
            #     reg2 = asm_code[i + 2]
            #     reg3 = asm_code[i + 3]
            #     act_val = int(self.acts[act], 2)
            #     reg1_val = int(self.regs[reg1], 2)
            #     reg2_val = int(self.regs[reg2], 2)
            #     reg3_val = int(self.regs[reg3], 2)
            #     memory.append(act_val)
            #     memory.append(reg1_val)
            #     memory.append(reg2_val)
            #     memory.append(reg3_val)
            # elif act == 'save':
            #     act = e
            #     reg = asm_code[i + 1]
            #     value = int(asm_code[i + 2][1 :])
            #     act_val = int(self.acts[act], 2)
            #     reg_val = int(self.regs[reg], 2)
            #     memory.append(act_val)
            #     memory.append(reg_val)
            #     memory.append(value)
            # elif act == 'load':
            #     act = e
            #     value = int(asm_code[i + 1][1:])
            #     reg = asm_code[i + 2]
            #     act_val = int(self.acts[act], 2)
            #     reg_val = int(self.regs[reg], 2)
            #     memory.append(act_val)
            #     memory.append(value)
            #     memory.append(reg_val)
            if act == 'compare':# 这里体现只读不操作
                act = e
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
            elif act == 'jump_if_less':# 现在确保在read_len里面的内容不至于坏掉
                act = e
                label = asm_code[i + 1]
                act_val = int(self.acts[act], 2)
                memory.append(act_val)
                if label in label_dict: # 没有明确的值的时候就是给上+1和+2的标签
                    l1 = label + '+1'
                    l2 = label + '+2'
                    memory.append(l1)
                    memory.append(l2)
                else:
                    value = int(asm_code[i + 1][1:])
                    low, high = self.set_memory_u16(value)
                    memory.append(low)
                    memory.append(high)
            elif act == 'jump':
                act = e
                label = asm_code[i + 1]
                act_val = int(self.acts[act], 2)
                memory.append(act_val)  # 得上来就append不然长度不是紧接着
                if label in label_dict:
                    l1 = label + '+1'
                    l2 = label + '+2'
                    memory.append(l1)
                    memory.append(l2)
                else:
                    value = int(asm_code[i + 1][1:])
                    low, high = self.set_memory_u16(value)
                    memory.append(low)
                    memory.append(high)
            elif act == 'set2':
                act = e
                reg = asm_code[i + 1]
                value = int(asm_code[i + 2])
                low, high = self.set_memory_u16(value)
                act_val = int(self.acts[act], 2)
                reg_val = int(self.regs[reg], 2)
                memory.append(act_val)
                memory.append(reg_val)
                memory.append(low)
                memory.append(high)
            elif act == 'add2':
                act = e # 注意这里面的e需要自己小心控制len
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                reg3 = asm_code[i + 3]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                reg3_val = int(self.regs[reg3], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
                memory.append(reg3_val)
            elif act == 'subtract2':
                act = e # 注意这里面的e需要自己小心控制len
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                reg3 = asm_code[i + 3]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                reg3_val = int(self.regs[reg3], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
                memory.append(reg3_val)
            elif act == 'load2': # 涉及到地址的与增加位数有关 只是设计到寄存器在此处无关
                act = e
                act_val = int(self.acts[act], 2)
                memory.append(act_val)  # 得上来就append不然长度不是紧接着
                value = int(asm_code[i + 1][1:])
                low, high = self.set_memory_u16(value)
                memory.append(low)
                memory.append(high)
                reg = asm_code[i + 2]
                reg_val = int(self.regs[reg], 2)
                memory.append(reg_val)
            elif act == 'save2': # 涉及到地址的与增加位数有关 只是设计到寄存器在此处无关
                act = e
                reg = asm_code[i + 1]
                value = int(asm_code[i + 2][1 :])
                low, high = self.set_memory_u16(value)
                act_val = int(self.acts[act], 2)
                reg_val = int(self.regs[reg], 2)
                memory.append(act_val)
                memory.append(reg_val)
                memory.append(low)
                memory.append(high)
            elif act == 'save_from_register2':
                act = e
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
            elif act == 'save_from_register':
                act = e
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
            elif act == 'load_from_register2':
                act = e
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
            elif act == 'load_from_register':
                act = e
                reg1 = asm_code[i + 1]
                reg2 = asm_code[i + 2]
                act_val = int(self.acts[act], 2)
                reg1_val = int(self.regs[reg1], 2)
                reg2_val = int(self.regs[reg2], 2)
                memory.append(act_val)
                memory.append(reg1_val)
                memory.append(reg2_val)
            elif act == 'jump_from_register':
                act = e
                reg = asm_code[i + 1]
                act_val = int(self.acts[act], 2)
                reg_val = int(self.regs[reg], 2)
                memory.append(act_val)
                memory.append(reg_val)
            elif act == 'halt':
                act = e
                act_val = int(self.acts[act], 2)
                memory.append(act_val)
                break
            elif act == '.memory':
                mem_add = int(asm_code[i + 1])
                mem_add_len = mem_add - i - 1
                memory = memory + [0] * mem_add_len

        return memory, label_dict

    def second_code(self, memory):
        memory, label_dict = self.machine_code(memory)
        new_label_dict = {}

        for key in label_dict:# 先建立字典 注意字典不能在循环中修改
            value = label_dict[key]
            low, high = self.set_memory_u16(value)
            l1 = key + '+1'
            l2 = key + '+2'
            new_label_dict[l1] = low
            new_label_dict[l2] = high

        for i, e in enumerate(memory):
            if e in new_label_dict:
                memory[i] = new_label_dict[e]
        print('new_label_dict final', new_label_dict)

        second_memory = memory
        return second_memory

def machine_code(asm_code):
    x16asm = X16asm()
    memory = x16asm.second_code(asm_code)
    return memory
if __name__ == '__main__':
    machine_code()



