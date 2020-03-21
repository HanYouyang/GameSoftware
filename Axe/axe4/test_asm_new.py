# from . import Asm
# from . import machine_code_asm
# 不能有__init__
from asm_new import machine_code_asm
from vm_new import Axecpu

def test_vm():
    # 此处注意split直接获得的是第一行要用for循环
    asm ='''
    ; 单行注释
    @label1
    set a1 1 ; 行内注释
    '''
    expected = [
    0, 16, 1,
    ]
    output = machine_code_asm(asm)
    memory = output
    cpu = Axecpu(memory)
    vm_regs, vm_memory = cpu.run()
    expected_regs = {
            'a1': 1,
            # 'a2': '00100000',
            # 'a3': '00110000',
            # 'pa': '00000000',
            # 'f1': '01010000',  # pa内存位置专用寄存器
            # 'c1': '01000000',  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
        }
    assert expected == output, output
    assert expected_regs['a1'] == vm_regs['a1'], vm_regs

  
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
  