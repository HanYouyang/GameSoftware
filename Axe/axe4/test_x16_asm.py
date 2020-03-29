# from x16_asm_new import Asmblerx16
# from x16_vm_new import Axecpux16

# def get_memory_u16(value1, value2):
#     low = value1
#     high = value2
#     value = (high << 8) + low
#     return value
# def set_memory_u16(number: int):
#     low = number & 0xFF
#     high = (number >> 8) & 0xFF
#     return low, high

# def test_jump_jump_if_less_x16_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     jump @1024
#     .memory 1024
#     ; 初始化 f1 寄存器，这是需要我们手动做的
#     set2 f1 3 ; 设置 f1 寄存器为 3，我们用这个寄存器里的内存地址来保存函数返回后应该跳转的地址
#     ; 我们要在接下来的的内存存放函数定义，所以直接跳转到 @function_end 避免执行函数
#     jump @function_end
#         @function_multiply
#         set2 a3 2 ; 因为下面用 a2 < a3 做判断，所以 a3 从 2 开始
#         ; 我们需要在循环中把 a3 + 1，并且把 a1 累加
#         ; 由于我们只有 3 个通用寄存器可用，我们需要用 3 个内存来暂存 a1 a2 a3 的值
#         ; 因为我们现在是自主决定使用所有内存，所以我们可以手动指定使用的内存区域
#         ; 我们把 65534 65532 65530 这三个地址拿来存储 a1 a2 a3 的值
#         ; 我们先保存 a1
#         save2 a1 @65534
#             @while_start ; 循环开始
#                 compare a2 a3 ;
#                 jump_if_less @while_end ; 一旦 a2 小于 a2，就结束循环
#                 ; 把 a2 保存到 65532, 然后利用 a2 把 a3+1
#                 save2 a2 @65532
#                 set2 a2 1
#                 add2 a3 a2 a3
#                 ; 把循环开始之前暂存的 a1 放到 a2 中然后累加到 a1
#                 load2 @65534 a2
#                 add2 a1 a2 a1
#                 ; 恢复 a2 的值并跳转到循环开始
#                 load2 @65532 a2
#                 jump @while_start
#             @while_end
#         ; 函数结束了，这时候 a1 存的就是 a1*a2 的值
#         ; f1 寄存器里面存储的是函数调用前的地址，我们让 f1-2，然后把它取出来, 然后返回
#         set2 a3 2
#         subtract2 f1 a3 f1
#         load_from_register2 f1 a2
#         jump_from_register a2
#         ; 所有函数定义结束的标记（但我们这个例子中，只有一个函数定义）
#         @function_end

#     ; 我们来调用前面的 multiply 函数
#     set2 a1 300 ; a1 是 300
#     set2 a2 10 ; a2 是 10

#     ; 保存 pa 到 f1 所表示的内存中
#     ; 请特别注意下面的写法
#     ; save_from_register2 长度是 3 字节
#     ; jump 长度是 3 字节
#     ; set2 add2 各自占用 4 字节
#     ; 所以我们用它们两句之前的 add2 来修正函数返回时候的正确地址(也就是 14)
#     ; cpu 读了 add2 这句后就会把 pa + 4（add2 占用 4 字节）
#     ; 然后才会执行 add2，所以执行 add2 这句的时候只需要把 pa + 6 就能指向 jump @function_multiply 的下一句
#     set2 a3 14
#     add2 pa a3 a3
#     save_from_register2 a3 f1 ; 3 字节
#     ; 保存后，要把 f1 的值 +2
#     set2 a3 2 ; 4 字节
#     add2 f1 a3 f1 ; 4 字节
#     jump @function_multiply ; 3 字节
#     halt
#     '''
# #     expected = [ 0,
# # 6, 0, 4, 
# # 8, 80, 3, 0, 
# # 6, 54, 
# # 8, 48, 2, 0, 11, 16, 254, 255, 4, 32, 48, 5, 40, 11, 32, 252, 255, 8, 32, 1, 0, 10, 48, 32, 48, 9, 254, 255, 32, 10, 16, 32, 16, 9, 252, 255, 32, 6, 13, 8, 48, 2, 0, 12, 80, 48, 80, 14, 80, 32, 16, 32, 8, 16, 44, 1, 8, 32, 10, 0, 8, 48, 14, 0, 10, 0, 48, 48, 15, 48, 80, 8, 48, 2, 0, 10, 80, 48, 80, 6, 7, 255
# #     ]
#     expected_xijt = [6, 0, 4] + [0] * 1021 +  [
#         8, 80, 3, 0,
#         6, 61, 4,
#         8, 48, 2, 0,
#         11, 16, 254, 255,
#         4, 32, 48,
#         5, 48, 4,
#         11, 32, 252, 255,
#         8, 32, 1, 0,
#         10, 48, 32, 48,
#         9, 254, 255, 32,
#         10, 16, 32, 16,
#         9, 252, 255, 32,
#         6, 15, 4,
#         8, 48, 2, 0,
#         12, 80, 48, 80,
#         14, 80, 32,
#         16, 32,
#         8, 16, 44, 1,
#         8, 32, 10, 0,
#         8, 48, 14, 0,
#         10, 0, 48, 48,
#         15, 48, 80,
#         8, 48, 2, 0,
#         10, 80, 48, 80,
#         6, 7, 4,
#         255,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 65556
#     cpu = Axecpux16(memory)
#     # print('cpu.regs', cpu.regs)
#     # cpu.run()
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     # expected_regs = {
#     #     'a1': 266,
#     #     # 'a2': 2,
#     #     # 'a3': '00110000',
#     #     # 'pa': '00000000',
#     #     # 'f1': '01010000',  # pa内存位置专用寄存器
#     #     # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     # }
#     for i,e in enumerate(expected_xijt):
#         if output[i] != expected_xijt[i]:
#             print('i now', i, output[i], expected_xijt[i])
#     assert expected_xijt == output, output
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs


# def test_jump_jump_if_less_x16_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     jump @267
#     .memory 266
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     4, 16, 32,
#     5, 12, 0,    
#     255,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     expected_number = 255
#     for i, e in enumerate(output):
#         if e == 6:
#             print('i now', i)
#     assert expected_number == output[266], output



# def test_jump_jump_if_less_x16_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     .memory 266
#     jump @266

#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     4, 16, 32,
#     5, 12, 0,    
#     255,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     expected_number = 6
#     for i, e in enumerate(output):
#         if e == 6:
#             print('i now', i)
#     assert expected_number == output[266], output



# def test_jump_jump_if_less_x16_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set2 a1 266
#     set2 a2 277
#     compare a1 a2
#     jump_if_less @12
#     @label1
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     4, 16, 32,
#     5, 12, 0,    
#     255,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     memory = output + [0] * 1099
#     cpu = Axecpux16(memory)
#     # vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     # expected_memory = 3
#     expected_regs = {
#         'a1': 266,
#         # 'a2': 2,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     assert expected == output, output
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs



# def test_save_reg2_load_reg2_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''ß
#     @label2333
#     set2 a1 266
#     set2 a2 277
#     save_from_register2 a2 a1
#     load_from_register2 a1 a2
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     15, 32, 16,
#     14, 16, 32,
#     255, 
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     memory = output + [0] * 277
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_memory = 3
#     expected_regs = {
#         'a1': 266,
#         # 'a2': 2,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     assert expected == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs

# def test_add2_sub2_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     @label2333
#     set2 a1 266
#     set2 a2 277
#     add2 a1 a2 a1
#     subtract2 a1 a2 a1
#     ;load_from_register2 a1 a2
#     ;save_from_register2 a2 a1
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     # 14, 16, 32,
#     # 15, 32, 16,
#     255, 0,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     memory = output + [0] * 277
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_memory = 3
#     expected_regs = {
#         'a1': 266,
#         # 'a2': 2,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     assert expected == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs


# def test_save2_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     @label2333
#     set2 a1 266
#     set2 a2 277
#     save2 a2 @266
#     load2 @266 a2
#     ;load_from_register2 a1 a2
#     ;save_from_register2 a2 a1
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     # 11, 32, 10, 1,
#     # 10, 16, 32, 16,
#     9, 10, 1, 32,
#     # 14, 16, 32,
#     # 15, 32, 16,
#     255, 0,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     memory = output + [0] * 277
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_memory = 3
#     expected_regs = {
#         'a1': 266,
#         # 'a2': 2,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     assert expected == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs

# def test_set2_load2_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set2 a1 266
#     set2 a2 277
#     save2 a2 @266
#     load2 @266 a2
#     add2 a1 a2 a1
#     halt
#     '''
#     expected = [
#     8, 16, 10, 1,
#     8, 32, 21, 1,
#     9, 10, 1, 32,
#     10, 16, 32, 16,
#     255, 0,
#     ]
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     memory = output + [0] * 300
#     assert expected == output, output
