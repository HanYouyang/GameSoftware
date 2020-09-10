from x16_asm_new_10 import Asmblerx16
from x16_vm_new_10 import Axecpux16, Screen16
# from x16_screen_new_10 import Screen16

def get_memory_u16(value1, value2):
    low = value1
    high = value2
    value = (high << 8) + low
    return value
def set_memory_u16(number: int):
    low = number & 0xFF
    high = (number >> 8) & 0xFF
    return low, high

def test_screen_pygame():
    asm ='''
    jump @20003
    .memory 20003;确保空间打开这么多长度
    ;从3到1026的内存全部都是屏幕大小的
    set2 f1 10003;栈内存开始点，但是配合第一行得1024+3
    ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

    jump @main
    .func @add
    .func @multiply
    .func @factorial
    .func @draw_point
    
    @main
    .super_call @draw_point 50 50 233

    halt
    '''
    asmbeler = Asmblerx16()
    output = asmbeler.machine_code_asm(asm)
    # print('len of out put now', len(output))
    # len_append = 65535 - len(output)
    len_append = 30003 - len(output)
    memory = output + [0] * len_append
    cpu = Axecpux16(memory)
    vm_regs, vm_memory = cpu.run()
    # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
    # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    # test_num = get_memory_u16(9, 4)
    # print("print test_num 149,5", test_num)
    # screen_ori = Screen16(memory, runable = True)
    # screen_ori.run_test()

    # screen_aft = Screen16(vm_memory, runable = True)
    # screen_aft = Screen16(memory, runable = True)

    # screen_aft.run_test()
    # screen_aft.run()

    expected_regs = {
        'a1': 674,
        # 'a2': 20,
        # 'a3': 20,
        # 'pa': '00000000',
        # 'f1': '01010000',  # pa内存位置专用寄存器
        # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
    }
    # assert expected_xijt == output, output
    # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    assert vm_memory[5053] == 233, vm_memory[308]




# def test_array():
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     ;从3到1026的内存全部都是屏幕大小的
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
#     .func @add
#     .func @multiply
#     .func @draw_point


#     @main
#     ;.array a 2 3 4 5 6
#     ;.var num1 a[2]
#     ;.super_call @draw_point a[2] a[3]
#     .super_call @draw_point 3 5 233

#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     # print('len of out put now', len(output))
#     memory = output + [0] * 2048
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
#     test_num = get_memory_u16(9, 4)
#     print("print test_num 149,5", test_num)
#     # screen_ori = Screen16(memory, runable = True)
#     # screen_aft = Screen16(vm_memory, runable = True)
#     # screen_ori.run_test()
#     # screen_aft.run_test()
#     expected_regs = {
#         'a1': 674,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     assert vm_memory[308] == 233, vm_memory[308]





# def test_draw_point():
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     ;从3到1026的内存全部都是屏幕大小的
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
#     .func @add
#     .func @multiply
#     .func @draw_point


#     @main
#     .super_call @draw_point 3 5 233

#     halt
#     '''
    # asmbeler = Asmblerx16()
    # output = asmbeler.machine_code_asm(asm)
    # # print('len of out put now', len(output))
    # memory = output + [0] * 2048
    # cpu = Axecpux16(memory)
    # vm_regs, vm_memory = cpu.run()
    # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
    # # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
    # test_num = get_memory_u16(9, 4)
    # print("print test_num 149,5", test_num)
    # # screen_ori = Screen16(memory, runable = True)
    # # screen_aft = Screen16(vm_memory, runable = True)
    # # screen_ori.run_test()
    # # screen_aft.run_test()
    # expected_regs = {
    #     'a1': 674,
    #     # 'a2': 20,
    #     # 'a3': 20,
    #     # 'pa': '00000000',
    #     # 'f1': '01010000',  # pa内存位置专用寄存器
    #     # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
    # }
    # # assert expected_xijt == output, output
    # # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    # assert vm_memory[38] == 233, vm_memory[38]

# def test_rewrite_factorial():
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     ;从3到1026的内存全部都是屏幕大小的
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
#     .func @multiply
#     .func @factorial

#     @main
#     ;函数计算的时候是左闭右开
#     .super_call @factorial 5 2
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     # print('len of out put now', len(output))
#     memory = output + [0] * 2048
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
#     # screen_ori = Screen16(memory, runable = True)
#     # screen_aft = Screen16(vm_memory, runable = True)
#     # screen_ori.run_test()
#     # screen_aft.run_test()

    
#     expected_regs = {
#         'a1': 674,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    


# def test_rewrite_muti():
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     ;从3到1026的内存全部都是屏幕大小的
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
       
#     @multiply
#         .expand_f1 6
#         .get_local 8 a1
#         ;获得可变a1也是最终返回值
#         .save_local 4 a1
#         set2 a2 2
#         .save_local 2 a2

#         @while_start 
#             ;拿到a2（代表n）和a1（代表2）比较大小
#             .get_local 6 a2
#             .get_local 2 a1
#             compare a2 a1 
#             jump_if_less @while_end
            
#             ;对a1进行加和，此处是a1代表的2增大为后续的3、4、5、6
#             set2 a2 1
#             add2 a1 a2 a1
#             ;把a3存在f1栈顶
#             .save_local 2 a1

#             ;获得原始a1的值，只是这里写作a2
#             .get_local 8 a2
#             ;获得可变的加和a1的值
#             .get_local 4 a1
#             add2 a1 a2 a1

#             ;及时保存可变a1的值到-4位置
#             .save_local 4 a1

#             jump @while_start
#         @while_end
#         .get_local 4 a1        
#         .return 10 ;此处因为已经有4而局部又加了6

#     @main
#     .super_call @multiply 10 5
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     # print('len of out put now', len(output))
#     memory = output + [0] * 2048
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
#     # screen_ori = Screen16(memory, runable = True)
#     # screen_aft = Screen16(vm_memory, runable = True)
#     # screen_ori.run_test()
#     # screen_aft.run_test()

    
#     expected_regs = {
#         'a1': 674,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    




# def test_10_3_var_update_get():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
    
#     @function_draw_point

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1;注意此处返回的时候是在用a1存值而非其他
        
#         .return 2
        
#     @main

#     .var num1 4
#     .update num1 8
#     .var num2 666
#     .get num2 a1

#     .super_call @function_draw_point a1 num2
#     ;.super_call @function_draw_point num1 num2
#     ;.super_call @function_draw_point 4 4

#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     # print('len of out put now', len(output))
#     memory = output + [0] * 2048
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
#     # screen_ori = Screen16(memory, runable = True)
#     # screen_aft = Screen16(vm_memory, runable = True)
#     # screen_ori.run_test()
#     # screen_aft.run_test()

    
#     expected_regs = {
#         'a1': 1332,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
  
# def test_10_3():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @2048
#     .memory 2048;确保空间打开这么多长度
#     set2 f1 1027;栈内存开始点，但是配合第一行得1024+3
#     ;此时应该尽可能减少但是明白栈内存空间开辟到了哪里

#     jump @main
    
#     @function_draw_point

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1;注意此处返回的时候是在用a1存值而非其他
        
#         .return 2
        
#     @main

#     .super_call @function_draw_point 4 4
    
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     # print('len of out put now', len(output))
#     memory = output + [0] * 2048
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    
#     # screen_ori = Screen16(memory, runable = True)
#     screen_aft = Screen16(vm_memory, runable = True)
#     # screen_ori.run_test()
#     screen_aft.run_test()

    
#     expected_regs = {
#         'a1': 8,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    



# def test_change_call_all_locs():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3

#     jump @main
    
#     @function_draw_point

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1
#         ;注意此处返回的时候是在用a1存值而非其他
#         ;save_from_register2 a1 a3 ;存入此时的a1累加值
        
#         .return 2
        
#     @main

#     .super_call @function_draw_point 4 4
    
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 8,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs


# def test_change_call_all_locs():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3

#     jump @main
    
#     @function_add
        
#         ;有几个add2 最后返回几
#         ;下面的内容写到外面去了
#         ;save_from_register2 a1 f1 ;存储a1原始值 此处-6位默认
#         ;set2 a3 2
#         ;add2 f1 a3 f1
#         ;save_from_register2 a2 f1 ;存储a1累加值 此处-4位默认

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1
#         ;注意此处返回的时候是在用a1存值而非其他
#         ;save_from_register2 a1 a3 ;存入此时的a1累加值
        
#         .return 2
        
#     @main

#     set2 a1 10
#     set2 a2 20
#     save2 a1 @5
#     save2 a2 @7
#     ;.call @function_add
#     ;先用add函数尝试传入参数
#     ;后面再用mutilply尝试调用复杂进入逻辑
#     ;.call_multi_arg_locs @function_add @5 @7
#     ;此处注销下面两个任意个都可以
#     ;.call_multi_arg_all @function_add a1 @7
#     ;.call_multi_arg_all @function_add @5 a2
#     ;.call_multi_arg_all @function_add a1 a2
#     .call_multi_arg_all @function_add 10 20

#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 30,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a3'] == vm_regs['a3'], vm_regs

# def test_change_call_all_regs():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3

#     jump @main
    
#     @function_add
        
#         ;有几个add2 最后返回几
#         ;下面的内容写到外面去了
#         ;save_from_register2 a1 f1 ;存储a1原始值 此处-6位默认
#         ;set2 a3 2
#         ;add2 f1 a3 f1
#         ;save_from_register2 a2 f1 ;存储a1累加值 此处-4位默认

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1
#         ;注意此处返回的时候是在用a1存值而非其他
#         ;save_from_register2 a1 a3 ;存入此时的a1累加值
        
#         .return 2
        
#     @main

#     set2 a1 10
#     set2 a2 20
#     ;.call @function_add
#     ;先用add函数尝试传入参数
#     ;后面再用mutilply尝试调用复杂进入逻辑
#     .call_multi_arg_regs @function_add a1 a2
#     ;先看后面有几个参数
#     ;再继续入栈看加入几个内容出来
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 30,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a3'] == vm_regs['a3'], vm_regs




# def test_change_call_all_nums():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3

#     jump @main
    
#     @function_add
        
#         ;有几个add2 最后返回几
#         ;下面的内容写到外面去了
#         ;save_from_register2 a1 f1 ;存储a1原始值 此处-6位默认
#         ;set2 a3 2
#         ;add2 f1 a3 f1
#         ;save_from_register2 a2 f1 ;存储a1累加值 此处-4位默认

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1

#         add2 a1 a2 a1
#         ;注意此处返回的时候是在用a1存值而非其他
#         ;save_from_register2 a1 a3 ;存入此时的a1累加值
        
#         .return 2
        
#     @main

#     ;set2 a1 10
#     ;set2 a2 20
#     ;.call @function_add
#     ;先用add函数尝试传入参数
#     ;后面再用mutilply尝试调用复杂进入逻辑
#     .call_multi_arg @function_add 10 20
#     ;先看后面有几个参数
#     ;再继续入栈看加入几个内容出来
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 30,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a3'] == vm_regs['a3'], vm_regs




# def test_change_call_add():
#     # 先写出来原版的function_add
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3

#     jump @function_end
    
#     @function_add
        
#         ;有几个add2 最后返回几
#         save_from_register2 a1 f1 ;存储a1原始值 此处-6位默认
#         set2 a3 2
#         add2 f1 a3 f1
#         save_from_register2 a2 f1 ;存储a1累加值 此处-4位默认

#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2

#         set2 a3 2
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1


#         add2 a1 a2 a1
#         ;注意此处返回的时候是在用a1存值而非其他

#         .return 2
        
#     @function_end

#     set2 a1 10
#     set2 a2 20
#     .call @function_add
#     ;先用add函数尝试传入参数
#     ;后面再用mutilply尝试调用复杂进入逻辑
#     ;.call_multi_arg @function_add 10 20
#     ;先看后面有几个参数
#     ;再继续入栈看加入几个内容出来
#     halt
#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 30,
#         # 'a2': 20,
#         # 'a3': 20,
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
#     # assert expected_regs['a2'] == vm_regs['a2'], vm_regs
#     # assert expected_regs['a3'] == vm_regs['a3'], vm_regs



# def test_draw_point_16():
#     # 此处注意split直接获得的是第一行要用for循环
    # asm ='''
    # set2 a1 20
    # shift_right a1
    # set2 a2 20
    # and a1 a2 a3
    # halt
    # '''
    # asmbeler = Asmblerx16()
    # output = asmbeler.machine_code_asm(asm)
    # print('len of out put now', len(output))
    # memory = output + [0] * 2000
    # cpu = Axecpux16(memory)
    # vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
    # expected_regs = {
    #     'a1': 10,
    #     # 'a2': 2,
    #     'a3': 20,
    #     # 'pa': '00000000',
    #     # 'f1': '01010000',  # pa内存位置专用寄存器
    #     # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
    # }
#     # assert expected_xijt == output, output
    # assert expected_regs['a1'] == vm_regs['a1'], vm_regs
    # assert expected_regs['a3'] == vm_regs['a3'], vm_regs



# def test_draw_point_16():
#     # 此处注意split直接获得的是第一行要用for循环
#     asm ='''
#     jump @1024
#     .memory 1024
#     set2 f1 3 ; 设置 f1 寄存器为 3，我们用这个寄存器里的内存地址来保存函数返回后应该跳转的地址

#     jump @function_end
#         @function_multiply
#             set2 a3 2 ; 因为下面用 a2 < a3 做判断，所以 a3 从 2 开始
#             ;有几个add2 最后返回几
#             save_from_register2 a1 f1 ;存储a1原始值 此处-6位默认
#             add2 f1 a3 f1
#             set2 a1 0                 ;此处位置要求使用的是0为起点不然会多 bug+1
#             save_from_register2 a1 f1 ;存储a1累加值 此处-4位默认
#             add2 f1 a3 f1
#             save_from_register2 a2 f1 ;存储a2原始值 此处-2位默认
#             add2 f1 a3 f1
#             set2 a3 1
#             save_from_register2 a3 f1 ;存储i累加值开始应该为1不然计数会多一次bug+1 此处0位默认

#                 @while_start ; 循环开始

#                     ;拿到a2原始值
#                     set2 a3 2
#                     subtract2 f1 a3 a3
#                     load_from_register2 a3 a2

#                     ;拿到a3比较值
#                     load_from_register2 f1 a3

#                     compare a2 a3
#                     jump_if_less @while_end ; 一旦 a2 小于 a2，就结束循环

#                     ;累加a3获得与a2的临时比较值
#                     set2 a2 1
#                     add2 a3 a2 a3
#                     save_from_register2 a3 f1 ;存入此时a3代表的位置

#                     ;对a1进行累加
#                     set2 a3 6
#                     subtract2 f1 a3 a3
#                     load_from_register2 a3 a2 ;拿到a1原始值存入a2
#                     set2 a3 4
#                     subtract2 f1 a3 a3
#                     load_from_register2 a3 a1 ;拿到a1累加值存入a1
#                     add2 a1 a2 a1
#                     save_from_register2 a1 a3 ;存入此时的a1累加值


#                     jump @while_start
#                 @while_end

#             set2 a3 4 ;观察风行的内容理解自己需要加上一个读取数字
#             subtract2 f1 a3 a3
#             load_from_register2 a3 a1

#             .return 6 ;里面之前有一个+2的过程这里去掉了


#     @function_factorial
#         save_from_register2 a3 f1 ;此处存储乘积值到这里，但是开始的乘积值就是输入的1
#                                   ;存储a1原始值 此处-6位默认
#         set2 a3 2 ; 因为下面用 a2 < a3 做判断，所以 a3 从 2 开始
#         ;有几个add2 最后返回几
#         add2 f1 a3 f1
#         save_from_register2 a1 f1 ;存储a1原始值 此处-4位默认
#         add2 f1 a3 f1
#         save_from_register2 a2 f1 ;存储a2原始值 此处-2位默认
#         add2 f1 a3 f1
#         set2 a3 1
#         subtract2 a1 a3 a1
#         save_from_register2 a1 f1 ;存储a1-1即此时的n-1 此处0位默认

#         ;此处获得此时的a1 与 a2终止点比较
#         set2 a3 4
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1 ;拿到a1原始值
#         compare a1 a2
#         jump_if_less @if
#         @else
#         set2 a3 0
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a1 ;拿到a1-1即n-1
#         ;此时a2没变化
#         set2 a3 6
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a3 ;拿到此时的a3
#         .call @function_factorial

#         ;此时已经拿到a1
#         ;也已经拿到 a2 是当下上面那个值？还是继续创造
#         set2 a3 4
#         subtract2 f1 a3 a3
#         load_from_register2 a3 a2 ;拿到此时的a1原始值即n存到a2里面
#         .call @function_multiply
#         set2 a3 6
#         subtract2 f1 a3 a3
#         save_from_register2 a1 a3 ;存储此时a1中的乘积值到最开始的位置即默认a3位置
#         .return 6

#         @if
#         set2 a1 1
#         set2 a3 6
#         subtract2 f1 a3 a3
#         save_from_register2 a1 a3 ;存储此时a1中的1到a3位置
#         .return 6

#     @function_end
#     set2 a1 5   ; a1 是 5
#     set2 a2 1   ; a2 是 阶乘的终止点
#     set2 a3 1
#     .call @function_factorial
#     halt

#     '''
#     asmbeler = Asmblerx16()
#     output = asmbeler.machine_code_asm(asm)
#     print('len of out put now', len(output))
#     memory = output + [0] * 2000
#     cpu = Axecpux16(memory)
#     vm_regs, vm_memory = cpu.run()
#     # print('vm_memory now', vm_memory) # 此处是运行结束后的内容可以看到变化
#     # print('vm_regs now', vm_regs) # 此处是运行结束后的内容可以看到变化
#     expected_regs = {
#         'a1': 120,
#         # 'a2': 2,
#         # 'a3': '00110000',
#         # 'pa': '00000000',
#         # 'f1': '01010000',  # pa内存位置专用寄存器
#         # 'c1': 2,  # 0 表示小于，1 表示相等，2 表示大于（对的，和上课讲的不一样）
#     }
#     # assert expected_xijt == output, output
#     assert expected_regs['a1'] == vm_regs['a1'], vm_regs
