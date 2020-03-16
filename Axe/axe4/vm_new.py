# 作业讨论频道：
# #vm
#
# 补充资料：
# 补充 2 个新的指令
# 11111111 ; halt，停机指令，这个指令会让 CPU 停止执行
# ; 把这个指令放在程序的最后，CPU 就可以停止了
# 00000111 ; save_from_register
# ; save_from_register 的用法和说明参见下面的例子
#
# 需要安装 pygame 来设置像素点
# 下方有一个小的示例程序来演示如何设置像素点
# （注意，py3.7 的 pygame 有 bug，怎么解决请 chat 中提问）
#
# 1，实现下面的函数，注意参数是 python3 type hinting 修饰的
def run(memory: List[int]):
    '''
    memory 是一个长度为 256 的数字数组，也就是作业 4 生成的机器码
    这是一个虚拟机程序

    run 函数将 memory 数组视为内存，并且以地址 0 为起点执行这个内存
    你需要用变量来模拟寄存器，模拟程序的执行

    下方会给出一个用于测试的 memory 例子并更新在 #general
    你现在可以用自己生成的内容来测试

    注意，memory 目前只能支持 256 字节，因为 pa 寄存器只有 8 位
    '''
    regs_num = {
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'pa': 0,
            'f1': 0,  # pa内存位置专用寄存器
            'c1': 0,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }
    regs = {
        0: 'pa',
        80: 'f1',
        16: 'a1',
        32: 'a2',
        48: 'a3',
        64: 'c1'
    }
    op_name = {
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
    # memory = [0] * 256


    while op_name[i] != 'halt':
        i += op_lens[i] + 1
        if op_name[i] == 'set':






    final_regs = regs_num
    final_memory = memory
    return final_regs, final_memory
#
# 2，实现下面的功能
# 让上面的虚拟机程序支持显示屏，显示屏的像素是 10x10
# 因此内存的最后 100 个字节用于表示屏幕上的内容，每个字节表示一个像素，从左到右从上到下
# 也就是说内存 156 表示屏幕左上角第一个像素的颜色，具体表示方法见下方机器码例子
# 程序通过设置这 100 个字节的内存来控制屏幕的显示
#
# 给虚拟显示屏加一个放大功能，比如可以用 50x50 像素来模拟显示 10x10 像素
# 这样每个像素在屏幕上就是 5x5 那么大，这样方便查看、调试
#
# 下面是一段示例机器码
# 注意 你可以不用理会这段机器码，用你自己的代码来测试
#
# memory = [
# 0b00000000, # set
# 0b00100000, # a2
# 0b10011100, # 156, 左上角第一个像素
# 0b00000000, # set
# 0b00110000, # a3
# 0b00010110, # 22, 用于斜方向设置像素，每两排设置一个
# 0b00000000, # set
# 0b00010000, # a1
# 0b11000011, # 红色，我们用一字节表示 RGBA 颜色，所以这里红色就是 11000011
# 0b00000111, # save_from_register
# # 这个指令需要使用两个寄存器
# # 把 a1 的值（这里是 0b11000011）写入 a2 表示的内存中
# # 这里 a2 中是 156，这个指令会把内存地址 156 中的值设置为 0b11000011
# 0b00010000, # a1
# 0b00100000, # a2
# # 设置新像素点
# 0b00000010, # add
# 0b00100000, # a2
# 0b00110000, # a3
# 0b00100000, # a2
# 0b00000111, # save_from_register
# 0b00010000, # a1
# 0b00100000, # a2
# # 设置新像素点
# 0b00000010, # add
# 0b00100000, # a2
# 0b00110000, # a3
# 0b00100000, # a2
# 0b00000111, # save_from_register
# 0b00010000, # a1
# 0b00100000, # a2
# # 设置新像素点
# 0b00000010, # add
# 0b00100000, # a2
# 0b00110000, # a3
# 0b00100000, # a2
# 0b00000111, # save_from_register
# 0b00010000, # a1
# 0b00100000, # a2
# # 设置新像素点
# 0b00000010, # add
# 0b00100000, # a2
# 0b00110000, # a3
# 0b00100000, # a2
# 0b00000111, # save_from_register
# 0b00010000, # a1
# 0b00100000, # a2
# # 结果是在显示屏上显示一条斜线，一共 5 个红色的像素点
# 0b11111111, # 停机
# ]
#
# 扩充内存长度为 256，对后面的元素填 0
# memory = memory + [0] * (256 - len(memory))
#
# 这段代码每秒会在屏幕上随机画 30 个随机颜色的点
# 根据这个代码，实现上面作业的虚拟显示屏
# import pygame
# import random
#
# def main():
# width, height = 100, 100
# screen = pygame.display.set_mode((width, height))
# clock = pygame.time.Clock()
# running = True
# fps = 30
#
# while running:
#     x = random.randint(0, width - 1)
#     y = random.randint(0, height - 1)
#     position = (x, y)
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     color = (r, g, b)
#     screen.set_at(position, color)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     pygame.display.flip()
#     clock.tick(fps)
# if __name__ == '__main__':
# main()
