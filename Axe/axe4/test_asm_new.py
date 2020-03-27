# from . import Asm
# from . import machine_code_asm
# 不能有__init__
# from asm_new import machine_code_asm
# from vm_new import Axecpu
# def get_memory_u16(value1, value2):
#     low = value1
#     high = value2
#     value = (high << 8) + low
#     return value
# def set_memory_u16(number: int):
#     low = number & 0xFF
#     high = (number >> 8) & 0xFF
#     return low, high

# def test_load_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 111 ; 行内注释
#     save a1 @100 
#     set a2 3
#     add a1 a2 a1
#     load_from_register a1 a2
#     ;save_from_register a2 a1
#     set a1 21
#     jump_from_register a1
#     halt
#     '''
#     expected = [
#     0, 16, 111,
#     3, 16, 100,
#     0, 32, 3,
#     2, 16, 32, 16,
#     13, 16, 32,  
#     # 7, 32, 16,
#     0, 16, 21,
#     16, 16,
#     255, 
#     ]
#     output = machine_code_asm(asm)
#     memory = output + [0] * 120
#     cpu = Axecpu(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     # 此处应该a2是0
#     expected_regs = {
#         'a1': 21,
#         'a2': 0,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     assert expected == output, output
#     assert expected_regs['a2'] == vm_regs['a2'], vm_regs

# def test_save_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 111 ; 行内注释
#     save a1 @100 
#     set a2 3
#     add a1 a2 a1
#     ;load_from_register a1 a2
#     save_from_register a2 a1
#     set a1 21
#     jump_from_register a1
#     halt
#     '''
#     expected = [
#     0, 16, 111,
#     3, 16, 100,
#     0, 32, 3,
#     2, 16, 32, 16,
#     # 13, 16, 32, 
#     7, 32, 16,
#     0, 16, 21,
#     16, 16,
#     255, 
#     ]
#     output = machine_code_asm(asm)
#     memory = output + [0] * 120
#     cpu = Axecpu(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     expected_memory = 3
#     assert expected == output, output
#     assert expected_memory == vm_memory[114], vm_memory

# def test_save_load_reg():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 111 ; 行内注释
#     save a1 @100 
#     set a2 2
#     add a1 a2 a1
#     ;load_from_register a1 a2
#     ;save_from_register a2 a1
#     set a2 21
#     jump_from_register a2
#     halt
#     '''
#     expected = [
#     0, 16, 111,
#     3, 16, 100,
#     0, 32, 2,
#     2, 16, 32, 16,
#     13, 16, 32, 
#     # 7, 32, 16,
#     255, 
#     ]
#     output = machine_code_asm(asm)
#     memory = output + [0] * 120
#     # print('memory now', memory) # 翻译出来的没有运行过，所以内部没有内容可以看到
#     cpu = Axecpu(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#             'a1': 111,
#             # 'a2': 2,
#             # 'a3': '00110000',
#             # 'pa': '00000000',
#             # 'f1': '01010000',  # pa内存位置专用寄存器
#             'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#         }
#     assert expected == output, output
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     # assert expected_regs['c1'] == vm_regs['c1'], vm_regs


# def test_8bit_add_load():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     ; 单行注释
#     @label1
#     set a1 1111 ; 行内注释
#     save a1 @100 
#     set a2 2
#     @label2
#     add a1 a2 a1
#     load @100 a1
#     compare a1 a2
#     jump_if_less @label3
#     jump @label2 ; 不能和上边lab2放一起不然会位置相同
#     @label3
#     halt
#     '''
#     expected = [
#     0, 16, 1111,
#     3, 16, 100,
#     0, 32, 2,
#     2, 16, 32, 16,
#     1, 100, 16,
#     4, 16, 32,
#     5, 23, 
#     6, 9,
#     255,
#     ]
#     output = machine_code_asm(asm)
#     memory = output + [0] * 101
#     # print('memory now', memory) # 翻译出来的没有运行过，所以内部没有内容可以看到
#     cpu = Axecpu(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#             'a1': 1111,
#             # 'a2': 2,
#             # 'a3': '00110000',
#             # 'pa': '00000000',
#             # 'f1': '01010000',  # pa内存位置专用寄存器
#             'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#         }
#     assert expected == output, output
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     assert expected_regs['c1'] == vm_regs['c1'], vm_regs

  


# def test_vm():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     ; 单行注释
#     @label1
#     set a1 1 ; 行内注释
#     '''
#     expected = [
#     0, 16, 1,
#     ]
#     output = machine_code_asm(asm)
#     memory = output
#     cpu = Axecpu(memory)
#     vm_regs, vm_memory = cpu.run()
#     expected_regs = {
#             'a1': 1,
#             # 'a2': '00100000',
#             # 'a3': '00110000',
#             # 'pa': '00000000',
#             # 'f1': '01010000',  # pa内存位置专用寄存器
#             # 'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#         }
#     assert expected == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs

  
# def test9_comment():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     ; 单行注释
#     @label1
#     set a1 1 ; 行内注释
#     set a2 2
#     load @100 a1
#     save a2 @101
#     add a1 a2 a1
#     compare a1 a2
#     jump_if_great @label1
#     @end
#     jump @end
#     '''
#     expected = [
    
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     2, 16, 32, 16,
#     4, 16, 32,
#     5, 0,
#     6, 21,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  
# def test8_end():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     @label1
#     set a1 1
#     set a2 2
#     load @100 a1
#     save a2 @101
#     add a1 a2 a1
#     compare a1 a2
#     jump_if_great @label1
#     @end
#     jump @end
#     '''
#     expected = [
    
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     2, 16, 32, 16,
#     4, 16, 32,
#     5, 0,
#     6, 21,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  

# def test7_label():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     @label1
#     set a1 1
#     set a2 2
#     load @100 a1
#     save a2 @101
#     add a1 a2 a1
#     compare a1 a2
#     jump_if_great @label1
#     jump @2
#     '''
#     expected = [
    
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     2, 16, 32, 16,
#     4, 16, 32,
#     5, 0,
#     6, 2,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  


# def test6_compare():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 1
#     set a2 2
#     load @100 a1
#     save a2 @101
#     add a1 a2 a1
#     compare a1 a2
#     jump_if_great @1
#     jump @2
#     '''
#     expected = [
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     2, 16, 32, 16,
#     4, 16, 32,
#     5, 1,
#     6, 2,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  

# def test5():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 1
#     set a2 2
#     load @100 a1
#     save a2 @101
#     add a1 a2 a1
#     '''
#     expected = [
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     2, 16, 32, 16,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  

# def test4():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 1
#     set a2 2
#     load @100 a1
#     save a2 @101
#     '''
#     expected = [
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16,
#     3, 32, 101,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  
# def test3():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 1
#     set a2 2
#     load @100 a1
#     '''
#     expected = [
#     0, 16, 1,
#     0, 32, 2,
#     1, 100, 16
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  

# def test2():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     set a1 1
#     set a2 2
#     '''
#     expected = [
#     0, 16, 1,
#     0, 32, 2,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  
# def test1():
#     asm ='''
#     set a1 1
#     '''
#     expected = [
#     0, 16, 1,
#     ]
#     output = machine_code_asm(asm)
#     assert expected == output, output
  