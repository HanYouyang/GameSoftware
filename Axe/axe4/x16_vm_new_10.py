import pygame
import random
import threading

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
            17: 'shift_right',
            19: 'and',
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


    def run(self):
        while True:
            pa = self.regs['pa']
            # print('pa now ', pa)
            # print('self.regs now', self.regs)
            op_num = self.memory[pa]
            print('op_num now ', op_num)

            op = self.op_name[op_num]
            print('op now', op)

            if op == 'halt':
                break
            elif op == 'set': # 往下顺延此处获得数字
                self.regs['pa'] += self.op_lens[op] + 1
                reg = self.memory[pa + 1] # 这里的paj就是上面没有变化的pa
                reg_name = self.regs_name[reg]
                value = self.memory[pa + 2]
                self.regs[reg_name] = value
            elif op == 'set2': # 往下顺延此处获得数字
                self.regs['pa'] += self.op_lens[op] + 1
                reg = self.memory[pa + 1] # 这里的paj就是上面没有变化的pa
                reg_name = self.regs_name[reg]
                v1 = self.memory[pa + 2]
                v2 = self.memory[pa + 3]
                value = self.combine_memory_u16(v1, v2)
                self.regs[reg_name] = value
            elif op == 'load': # 往下顺延此处获得数字
                self.regs['pa'] += self.op_lens[op] + 1
                loc_num = self.memory[pa + 1]
                value = self.memory[loc_num]
                reg = self.memory[pa + 2] # 获得a1名字
                reg_name = self.regs_name[reg]
                self.regs[reg_name] = value
            elif op == 'load2': # 往下顺延此处获得数字
                self.regs['pa'] += self.op_lens[op] + 1
                loc1 = self.memory[pa + 1]
                loc2 = self.memory[pa + 2]
                loc_num = self.combine_memory_u16(loc1, loc2)
                v1 = self.memory[loc_num]
                v2 = self.memory[loc_num + 1]
                value = self.combine_memory_u16(v1, v2)
                reg = self.memory[pa + 3] # 获得a1名字
                reg_name = self.regs_name[reg]
                self.regs[reg_name] = value
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
                self.regs['pa'] += self.op_lens[op] + 1
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
            elif op == 'save':  # 往下顺延此处获得数字
                self.regs['pa'] += self.op_lens[op] + 1
                reg = self.memory[pa + 1]  # 获得a1名字
                reg_name = self.regs_name[reg]
                value = self.regs[reg_name]
                loc_num = self.memory[pa + 2]
                self.memory[loc_num] = value
            elif op == 'save2':
                self.regs['pa'] += self.op_lens[op] + 1
                reg = self.memory[pa + 1]
                reg_name = self.regs_name[reg]
                value = self.regs[reg_name]
                v1, v2 = self.split_memory_u16(value)
                loc1 = self.memory[pa + 2]
                loc2 = self.memory[pa + 3]
                loc_num = self.combine_memory_u16(loc1, loc2)
                self.memory[loc_num] = v1
                self.memory[loc_num + 1] = v2
            elif op == 'compare':
                self.regs['pa'] += self.op_lens[op] + 1
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
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_1_value = self.regs[reg_1_name]
                self.regs[reg_2_name] = self.memory[reg_1_value]
            elif op == 'load_from_register2':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_1_value = self.regs[reg_1_name]
                # print('reg_1_value now', reg_1_value)
                # reg_2_value = self.regs[reg_2_name]
                v1 = self.memory[reg_1_value]
                v2 = self.memory[reg_1_value + 1]
                value = self.combine_memory_u16(v1, v2)
                # print('v1 v2 and vaue now', v1, v2, value)
                self.regs[reg_2_name] = value
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
            elif op == 'shift_right':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_1_name = self.regs_name[reg_1]
                reg_1_value = self.regs[reg_1_name]
                trans_to_bin = bin(reg_1_value).replace('0b', '').zfill(8)
                # print('trans_to_bin now', trans_to_bin)
                right_trans_to_bin_old = trans_to_bin[:7].zfill(8)
                # print('right_trans_to_bin_old', right_trans_to_bin_old)
                right_trans_to_bin = '0b' + right_trans_to_bin_old
                # print('right_trans_to_bin', right_trans_to_bin)
                retur_to_int = int(right_trans_to_bin, 2)
                # print('retur_to_int now', retur_to_int)
                self.regs[reg_1_name] = retur_to_int
                # self.regs['pa'] = reg_1_value
            elif op == 'and':
                self.regs['pa'] += self.op_lens[op] + 1
                reg_1 = self.memory[pa + 1]
                reg_2 = self.memory[pa + 2]
                reg_3 = self.memory[pa + 3]
                reg_1_name = self.regs_name[reg_1]
                reg_2_name = self.regs_name[reg_2]
                reg_3_name = self.regs_name[reg_3]
                reg_1_value = self.regs[reg_1_name]
                reg_2_value = self.regs[reg_2_name]
                if reg_1_value == 0 or reg_2_value == 0:
                    self.regs[reg_3_name] = 0
                else:
                    self.regs[reg_3_name] = reg_2_value

        return self.regs, self.memory

# 1 问题在于compare_if_less不能跳转
# 改变当前的jump方式
# 2 问题在于1083步跳出来直到1111并不能解决问题
# 如果寄存器里面有pa，那么计算pa的时候，尤其在保存函数返回位置的时候
# 必须先加入pa和op_lens的运算，否则内容上计算会出现偏差
# 但是如果寄存器的值需要计算的比如jump_from_regs时候必须得使用自己的内容


class Screen16(object):
    def __init__(self, memory, runable):
        self.memory = memory
        self.display_memory = self.memory[3 : 10003]
        self.runable = runable
        self.size = 100
        self.width = 300
        self.height = 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = 30

    def run_vm(self):
        vm = Axecpux16(self.memory)
        vm.run()

    def draw_point(self, display_memory):
        dm = display_memory
        len_now = 100
        for i in range(len(dm)):
            e = dm[i]
            if e == 0:
                continue
            else:
                x = i // len_now
                y = i % len_now
                position = (x, y)
                # color = self.number_to_color(e)
                color_red = (255, 0, 0)
                # print('e now', e)
                # num = hex(e)
                # color = self.Hex_to_RGB(num)
                self.screen.set_at(position, color_red)

    def run(self):
       # 这里开启了第二个线程，跑的是虚拟机
        t = threading.Thread(target=self.run_vm, args=())
        t.start()
        while self.runable:
            self.draw_point(self.display_memory)
            # self.draw_block(self.display_memory, self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runable = False

            pygame.display.flip()
            self.clock.tick(self.fps)

    def number_to_color(self, n, bits=16):
        """
        映射并不完美, 现在不想这个问题了, 比较麻烦, 暂时不想做这个

        bits = 8 * n
        rgb 比例分配(8 * n 个字节)
        r : g : b
        3 : 3 : 2
        """
        # 按比例分配 r g b
        ratio = bits // 8
        red_ratio = 3 * ratio
        green_ratio = 3 * ratio
        blue_ratio = 2 * ratio

        bits = str(bits)
        formatted = '{0:' + bits + 'b}'
        s = formatted.format(n).replace(' ', '0')
        length = len(s)

        # 这里可能有问题, 暂时不想做这个事情
        nr = int(s[:red_ratio], 2)
        ng = int(s[red_ratio:length - blue_ratio], 2)
        nb = int(s[length - blue_ratio:], 2)

        # 计算出 r g b 映射后的值
        r = int(nr / (2 ** red_ratio) * 255)
        g = int(ng / (2 ** green_ratio) * 255)
        b = int(nb / (2 ** blue_ratio) * 255)

        color = (r, g, b)
        return color

    def run_my(self):# 出现闪退是不能有return不然直接出去了
        while self.runable:
            # x = 3 + 100 * 3
            # y = random.randint(0, self.height - 1)
            position = (50, 50)
            # r = random.randint(0, 255)
            # g = random.randint(0, 255)
            # b = random.randint(0, 255)
            # color = self.number_to_color(233)
            # 下面是红色
            color_red = (255, 0, 0)
            # 下面是黄色
            # color_yellow = (255, 255, 0)
            self.screen.set_at(position, color_red)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runable = False

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run_test(self):# 出现闪退是不能有return不然直接出去了
        while self.runable:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            position = (x, y)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = (r, g, b)
            self.screen.set_at(position, color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runable = False

            pygame.display.flip()
            self.clock.tick(self.fps)


def main():



    return

if __name__ == '__main__':
    main()