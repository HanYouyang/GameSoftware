import pygame
import random
from x16_vm_new_10 import Axecpux16

class Screen16(object):
    def __init__(self, memory, runable):
        self.memory = memory
        self.runable = runable
        self.width = 300
        self.height = 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = 30

    def combine_memory_u16(self, value1, value2):
        low = value1
        high = value2
        value = (high << 8) + low
        return value

    def split_memory_u16(self, number):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return low, high

    def run_vm(self):
        vm = Axecpux16(self.memory)
        vm.run()

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



# 1 问题在于compare_if_less不能跳转
# 改变当前的jump方式
# 2 问题在于1083步跳出来直到1111并不能解决问题
# 如果寄存器里面有pa，那么计算pa的时候，尤其在保存函数返回位置的时候
# 必须先加入pa和op_lens的运算，否则内容上计算会出现偏差
# 但是如果寄存器的值需要计算的比如jump_from_regs时候必须得使用自己的内容


