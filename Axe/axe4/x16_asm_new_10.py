class Asmblerx16(object):
    def __init__(self):
        self.vars = {
            'has_func':0,
        }
        # 下面的逻辑要跟return一起，用了多少个add位数就要返回多少位数
        # 也要注意函数的调用得在声明之前
        self.funcs = {
            '@draw_point': '''
                @draw_point
                    .expand_f1 2
                    ;原先下边两个分别是4和2
                    ;只是因为不可能使用a3寄存器
                    ;再就是因为你里面除了已有的新建变量，还要调用函数
                    ;为了调用函数所以必须使用一定隔离的手段
                    ;尽管值的位置并没有改变
            
                    ;此处暂定空间是100*100
                    .get_local 6 a1;目的是获得a1得到值
                    set2 a2 100;此处在不改动mutliply时候先把a2设置为10
                    .super_call @multiply a1 a2
                    
                    ;此时获得的a1是需要的值
                    ;还需要a2值进行加和
                    .get_local 4 a2
                    .super_call @add a1 a2
                    
                    ;此时a1的值是计算总的值
                    ;还需要给出具体的偏移量
                    .super_call @add a1 3
                    
                    ;此时是从jump后面的第三位开始计算总的偏移值
                    .get_local 2 a2
                    ;此时需要给出颜色，先默认是111是红色
                    save_from_register2 a2 a1;此时需要给出颜色，先默认是111是红色
                    .return 8
                ''',
            '@add': '''
                @add
                    .expand_f1 2
                    .get_local 2 a2
                    .get_local 4 a1
                    add2 a1 a2 a1
                    .return 6
                ''',
            '@multiply': '''
                @multiply
                    .expand_f1 2
                    .expand_f1 4
                    .get_local 8 a1
                    ;获得可变a1也是最终返回值
                    .save_local 4 a1
                    set2 a2 2
                    .save_local 2 a2
            
                    @while_start 
                        ;拿到a2（代表n）和a1（代表2）比较大小
                        .get_local 6 a2
                        .get_local 2 a1
                        compare a2 a1 
                        jump_if_less @while_end
                        
                        ;对a1进行加和，此处是a1代表的2增大为后续的3、4、5、6
                        set2 a2 1
                        add2 a1 a2 a1
                        ;把a3存在f1栈顶
                        .save_local 2 a1
            
                        ;获得原始a1的值，只是这里写作a2
                        .get_local 8 a2
                        ;获得可变的加和a1的值
                        .get_local 4 a1
                        add2 a1 a2 a1
            
                        ;及时保存可变a1的值到-4位置
                        .save_local 4 a1
            
                        jump @while_start
                    @while_end
                    .get_local 4 a1        
                    .return 10 ;此处因为已经有4而局部又加了6

                ''',
            '@factorial': '''
                @factorial
                    .expand_f1 2
                    .expand_f1 4
                    set2 a2 1       ;此处存储乘积值到这里，但是开始的乘积值就是输入的1
                    .save_local 4 a2 
            
                    .get_local 8 a1                    
                    set2 a2 1       
                    subtract2 a1 a2 a1
                    ;此处获得的是当前栈空间的a1 - 1 
                    .save_local 2 a1 
                 
                    ;此处获得此时的a1 与 a2终止点比较
                    ;此处获得的是当前栈空间的原始终止点a2
                    .get_local 6 a2
                    ;此处获得的是当前栈空间的当前栈空间的a1 - 1 
                    .get_local 2 a1
                    compare a1 a2
                    jump_if_less @if
            
                    @else
                    ;此时需要拿到 a1 - 1和a2继续传到里面去 
                    ;拿到a1-1即n-1
                    .get_local 2 a1
                    ;此时a2没变化
                    .get_local 6 a2
                    .super_call @factorial a1 a2
            
                    ;此时已经拿到a1
                    ;拿到当前栈a1原始值即n存到a2里面
                    .get_local 8 a2
                    .super_call @multiply a1 a2 
            
                    ;此时存储累乘到原始位置
                    .save_local 4 a1
                    .return 10
            
                    @if
                    ;存储此时a1中的1到a3位置
                    set2 a1 1
                    .save_local 2 a1
                    .return 10
                        ''',
        }
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
            'shift_right': '00010001',
            'and': '00010011',
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
                # '.super_call': 2, # 似乎不用加上
                # '.var': 2,
                'shift_right': 1,
                'and': 3,
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

    def add_fake(self, asm):
        asm_split = asm.splitlines()
        new_asm = []
        for e in asm_split:
            if e.strip() == '' or not len(e):
                continue

            ele = e.strip().split()
            print('ele now', ele)
            if ele[0] == '.call':  # 两个参数版本 目前就a1 a2两个寄存器没法调用三个参数
                function_name = ele[1]  # 模板字符串里面注释去掉 存在有影响
                call_replace_str = '''
                    set2 a3 14
                    add2 pa a3 a3
                    save_from_register2 a3 f1

                    set2 a3 2
                    add2 f1 a3 f1

                    jump {target_fun_name}
                '''
                # 第二段是为了存储返回地址
                final_str = call_replace_str.format(target_fun_name=function_name)
                new_asm.append(final_str)
                continue
            elif ele[0] == '.return':
                retur_nums = int(ele[1])
                # 此处的a3负责目前写函数的时候开辟多少空间存值
                # 如果开辟一个变量空间var a1 = 1 那么需要1,0 存储这个1也就是说
                # 此处要开通两个位置的值

                # 注意作业8需要注释2、3行，但是作业10不能注释掉
                # 另外思路就是就是作业8后面return 8
                # return_replace_str = '''
                #     set2 a3 {retur_space}
                #     set2 a2 2
                #     add2 a2 a3 a3
                #     subtract2 f1 a3 f1
                #     load_from_register2 f1 a2
                #     jump_from_register a2
                # '''
                return_space_self_str = '''
                    set2 a3 {retur_space}               
                    subtract2 f1 a3 f1
                    load_from_register2 f1 a2
                    jump_from_register a2
                '''
                # final_str = return_replace_str.format(retur_space=retur_nums)
                final_str = return_space_self_str.format(retur_space=retur_nums)
                new_asm.append(final_str)
                continue
            elif ele[0] == '.super_call':  # 两个参数版本 目前就a1 a2两个寄存器没法调用三个参数
                function_name = ele[1]  # 模板字符串里面注释去掉 存在有影响
                # 现在测算后面有多少个数值
                arg_ary = ele[2:]
                len_arg = len(arg_ary)
                # print('arg_ary now', arg_ary)
                # print('len_arg now', len_arg)
                target_offset = 0
                offset_str = '''
                    set2 a3 {offset}
                    add2 f1 a3 a3
                '''
                updat_str = '''
                '''
                add_more_space = '''
                    set2 a2 2
                    add2 a3 a2 a3
                '''
                add_more_regs_space = '''
                    set2 {x1} 2
                    add2 a3 {x1} a3
                '''
                for i in range(len_arg):
                    # print('arg_ary[i] now', arg_ary[i])
                    target_offset += 1
                    real_offset = 2 * target_offset
                    updat_str = updat_str + offset_str.format(offset=real_offset)
                    if arg_ary[i][0] == '@':
                        loc_str_format = '''
                            load2 {x1} a2
                            save_from_register2 a2 a3
                        '''
                        updat_str = updat_str + loc_str_format.format(x1=arg_ary[i])
                        updat_str = updat_str + add_more_space
                    elif arg_ary[i].isdigit():
                        digit_str_format = '''
                            set2 a2 {reg_value}
                            save_from_register2 a2 a3
                        '''
                        updat_str = updat_str + digit_str_format.format(reg_value=int(arg_ary[i]))
                        updat_str = updat_str + add_more_space
                    elif arg_ary[i] in self.vars:
                        var_str = '''
                            set2 a2 {var_value}
                            save_from_register2 a2 a3
                        '''
                        updat_str = updat_str + var_str.format(var_value=int(self.vars[arg_ary[i]]))
                        updat_str = updat_str + add_more_space
                    else:
                        reg_str_format = '''
                            save_from_register2 {x1} a3
                        '''
                        updat_str = updat_str + reg_str_format.format(x1=arg_ary[i])
                        updat_str = updat_str + add_more_regs_space.format(x1=arg_ary[i])
                call_replace_str = '''
                    ;此处是在存储f1的返回位置
                    set2 a3 14
                    add2 pa a3 a3
                    save_from_register2 a3 f1
                    
                    ;此处是在存储f1之前的参数的位置
                    ;f1之前的位置是参数，f1之后理论上可以加上局部变量参数
                    ;布局应该和所谓的函数调用相关联
                    ;最终布局就是 参数 f1返回位置 局部变量
                    set2 a3 {offset}
                    add2 f1 a3 f1
                    
                    jump {target_fun_name}
                '''
                replace_str = call_replace_str.format(offset=real_offset, target_fun_name=function_name)

                final_str = updat_str + replace_str
                # print('final_str now', final_str)
                new_asm.append(final_str)
                continue
            elif ele[0] == '.func':
                self.vars['has_func'] = 1
                add_str = self.funcs[ele[1]]
                # print('add_str', add_str)
                new_asm.append(add_str)
                continue
            elif ele[0] == '.var':
                if ele[1] not in self.vars:
                    self.vars[ele[1]] = int(ele[2]) # 此处要存上地址位置
                    # print('self.vars', self.vars)
                continue
            elif ele[0] == '.update':
                if ele[1] in self.vars:
                    self.vars[ele[1]] = int(ele[2]) # 此处要存上地址位置
                    # print('self.vars', self.vars)
                continue
            elif ele[0] == '.get':
                if ele[1] in self.vars:
                    get_str = '''
                        set2 {var_to_reg} {var_value}
                    '''
                    get_updat_str = get_str.format(var_value=self.vars[ele[1]], var_to_reg=ele[2])
                    # print('get_updat_str', get_updat_str)
                new_asm.append(get_updat_str)
                continue
            # elif ele[0] == '.array':
            #     # 增加可以但是不知道如何去访问
            #     e = ele[1]
            #     nums_array = ele[2 : ]
            #     self.vars[e] = nums_array
            #     get_updat_str = '''
            #         '''
            #     len_nums = len(nums_array)
            #     for i in range(len_nums):
            #         save_array_str = '''
            #             set2 a3 2
            #             add2 f1 a3 f1
            #             set2 a3 {value}
            #             save_from_register2 a3 f1
            #         '''
            #         get_updat_str += save_array_str.format(value=nums_array[i])
            #     append_updat_str = '''
            #             set2 a3 2
            #             add2 f1 a3 f1
            #         '''
            #     get_updat_str += append_updat_str
            #     new_asm.append(get_updat_str)
            #     continue
            elif ele[0] == '.expand_f1':
                get_str = '''
                    set2 a3 {var_value}
                    add2 f1 a3 f1
                '''
                get_updat_str = get_str.format(var_value=ele[1])
                new_asm.append(get_updat_str)
                continue
            elif ele[0] == '.save_local':
                get_str = '''
                    set2 a3 {var_value}
                    subtract2 f1 a3 a3
                    save_from_register2 {target_reg} a3 
                '''
                get_updat_str = get_str.format(var_value=ele[1], target_reg=ele[2])
                # print('get_updat_str', get_updat_str)
                new_asm.append(get_updat_str)
                continue
            elif ele[0] == '.get_local':
                get_str = '''
                    set2 a3 {var_value}
                    subtract2 f1 a3 a3
                    load_from_register2 a3 {target_reg}  
                '''
                get_updat_str = get_str.format(var_value=ele[1], target_reg=ele[2])
                # print('get_updat_str', get_updat_str)
                new_asm.append(get_updat_str)
                continue
            new_asm.append(e)
        final_str_muti_lines = '\n'.join(new_asm)
        # print('final_str_muti_lines now', final_str_muti_lines)
        return final_str_muti_lines

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
        asm = self.add_fake(asm)
        if self.vars['has_func'] == 1:
            asm = self.clear_notes(asm)
            asm = self.add_fake(asm)
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
            elif op == 'shift_right':  # 假设 a1 中存储的是 20，程序会跳转到 20
                reg1 = code[1]
                r1 = int(regs[reg1], 2)
                memory.append(op_value)
                memory.append(r1)
            elif op == 'and':
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