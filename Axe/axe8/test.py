from . import x16asm
from . import x16vm

def get_memory_u16(value1, value2):
    low = value1
    high = value2
    value = (high << 8) + low
    return value
def set_memory_u16(number: int):
    low = number & 0xFF
    high = (number >> 8) & 0xFF
    return low, high








# def test_call_return():
#     asm = """
#     ;注释多行都有
#     jump @1024 ;注释真的很多
#     .memory 1024
#     set2 f1 3 ;设置内存起始点为3开始
#     jump @function_end ; 注释非常多
#         @function_multiply
#             ; 函数开始 设置f1 + 3
#             set2 a3 3
#             add2 f1 a3 f1
#             set2 a3 2 ;设定初始a3计数因为是less判断所以要用2
#             save2 a1 @65534   ;存储a1的值
#             @while_start ;和下面三句设置循环初始条件
#                 compare a2 a3
#                 jump_if_less @while_end
#                 save2 a2 @65532 ;存储a2的值
#                 set2 a2 1 ;设置步进长度a2
#                 add2 a3 a2 a3 ;计数器当前值
#                 load2 @65534 a2   ;此时a2又变成被加数把a1之前保存的放到a2里面
#                 add2 a1 a2 a1 ;把a1中加入a2
#                 load2 @65532 a2  ;读取a2原始的计数值10
#                 jump @while_start
#             @while_end
#         .return 3
#         @function_end

#         set2 a1 300
#         set2 a2 10
#         .call @function_multiply
#     halt

#     """
#     expected = [
#         3000,
#         1131,
#         2,
#         1131,
#     ]
#     memory = x16asm.machine_code(asm)
#     memory += [0] * 65555
#     reg_num, final_mem = x16vm.run(memory)    
#     output = [
#         reg_num["a1"],
#         reg_num["pa"],
#         reg_num["a3"],
#         reg_num["a2"],
#     ]
#     assert expected == output, final_mem 


# def test_load_from_register2():
#     asm = """
#         set2 a1 288
#         set2 a2 777
#         save_from_register2 a1 a2
#         halt
#     """
#     expected = [
#         288,
#         32,
#         1,
#         # 288,
#     ]
#     memory = x16asm.machine_code(asm)
#     memory += [0] * 1024
#     reg_num, final_mem = x16vm.run(memory)    
#     output = [
#         reg_num['a1'],
#         memory[777],
#         memory[778],
#         # reg_num['a2'],
#     ]
#     print("reg_num now", reg_num)
#     assert expected == output, output

# def test_load_from_register2():
#     asm = """
#         set2 a1 288
#         save2 a1 @777
#         set2 a1 777
#         load_from_register2 a1 a2
#         halt
#     """
#     expected = [
#         777,
#         32,
#         1,
#         288,
#     ]
#     memory = x16asm.machine_code(asm)
#     memory += [0] * 1024
#     reg_num, final_mem = x16vm.run(memory)    
#     output = [
#         reg_num['a1'],
#         memory[777],
#         memory[778],
#         reg_num['a2']
#     ]
#     print("reg_num now", reg_num)
#     assert expected == output, output


# def test_set2():
#     asm = """
#         jump @1024
#         .memory 1024
#         ;
#         ; 从第四个字节开始，剩下的 1021 个字节都是我们的
#         ;
#         ;
#         ;
#         ;
#         ; 下面是内存 1024 开始的内容
#         ; 初始化 f1 寄存器，这是需要我们手动做的
#         set2 f1 3 ; 设置 f1 寄存器为 3，我们用这个寄存器里的内存地址来保存函数返回后应该跳转的地址
#         ;
#         ; 我们要在接下来的的内存存放函数定义，所以直接跳转到 @function_end 避免执行函数
#         jump @function_end
#         ;
#         ; 定义一个函数 function_multiply，接受两个参数，返回两个数的乘积
#         ; 参数通过 a1 a2 得到，返回值通过 a1 传给调用方
#         @function_multiply
#         set2 a3 2 ; 因为下面用 a2 < a3 做判断，所以 a3 从 2 开始
#         ; 我们需要在循环中把 a3 + 1，并且把 a1 累加
#         ; 由于我们只有 3 个通用寄存器可用，我们需要用 3 个内存来暂存 a1 a2 a3 的值
#         ; 因为我们现在是自主决定使用所有内存，所以我们可以手动指定使用的内存区域
#         ; 我们把 65534 65532 65530 这三个地址拿来存储 a1 a2 a3 的值
#         ; 我们先保存 a1
#         save2 a1 @65534
#         @while_start ; 循环开始
#         compare a2 a3 ;
#         jump_if_less @while_end ; 一旦 a2 小于 a3，就结束循环
#         ;
#         ; 把 a2 保存到 65532, 然后利用 a2 把 a3+1
#         save2 a2 @65532
#         set2 a2 1
#         add2 a3 a2 a3
#         ;
#         ; 把循环开始之前暂存的 a1 放到 a2 中然后累加到 a1
#         load2 @65534 a2
#         add2 a1 a2 a1
#         ;
#         ; 恢复 a2 的值并跳转到循环开始
#         load2 @65532 a2
#         jump @while_start
#         @while_end
#         ; 函数结束了，这时候 a1 存的就是 a1*a2 的值
#         ; f1 寄存器里面存储的是函数调用前的地址，我们让 f1-2，然后把它取出来, 然后返回
#         set2 a3 2
#         subtract2 f1 a3 f1
#         load_from_register2 f1 a2
#         jump_from_register a2
#         ;
#         ;
#         ; 所有函数定义结束的标记（但我们这个例子中，只有一个函数定义）
#         @function_end
#         ;
#         ;
#         ; 我们来调用前面的 multiply 函数
#         set2 a1 300 ; a1 是 300
#         set2 a2 10 ; a2 是 10
#         ; 保存 pa 到 f1 所表示的内存中
#         ; 请特别注意下面的写法
#         ; save_from_register2 长度是 3 字节
#         ; jump 长度是 3 字节
#         ; set2 add2 各自占用 4 字节
#         ; 所以我们用它们两句之前的 add2 来修正函数返回时候的正确地址(也就是 14)
#         ; cpu 读了 add2 这句后就会把 pa + 4（add2 占用 4 字节）
#         ; 然后才会执行 add2，所以执行 add2 这句的时候只需要把 pa + 6 就能指向 jump @function_multiply 的下一句
#         set2 a3 14
#         add2 pa a3 a3
#         save_from_register2 a3 f1 ; 3 字节
#         ; 保存后，要把 f1 的值 +2
#         set2 a3 2 ; 4 字节
#         add2 f1 a3 f1 ; 4 字节
#         ; 跳转到函数
#         jump @function_multiply ; 3 字节
#         ; 函数返回了x 里的 a1 就是我们想要的返回值
#         halt
#     """
#     memory = x16asm.machine_code(asm)
#     memory += [0] * 65535
#     reg_num, final_mem = x16vm.run(memory)    
#     output = [
#         reg_num["a1"],
#         reg_num["pa"],
#         reg_num["a3"],
#         reg_num["a2"],
#         final_mem[65532],
#         final_mem[65533],
#         final_mem[65534],
#         final_mem[65535],
#     ]
#     # print("final_mem[777] now", final_mem[777])
#     # print("final_mem[778] now", final_mem[778])

#     expected = [
#         3000, # 300 * 10 = 3000
#         1115,
#         2,
#         1115,
#         10,
#         0,
#         44,
#         1
#     ]
#     assert expected == output, output
    # assert expected == output, 


# def test_vm_all():
#     memory = [6, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 80, 3, 0, 6, 61, 4, 8, 48, 2, 0, 11, 16, 254, 255, 4, 32, 48, 5, 48, 4, 11, 32, 252, 255, 8, 32, 1, 0, 10, 48, 32, 48, 9, 254, 255, 32, 10, 16, 32, 16, 9, 252, 255, 32, 6, 15, 4, 8, 48, 2, 0, 12, 80, 48, 80, 14, 80, 32, 16, 32, 8, 16, 44, 1, 8, 32, 10, 0, 8, 48, 14, 0, 10, 0, 48, 48, 15, 48, 80, 8, 48, 2, 0, 10, 80, 48, 80, 6, 7, 4, 255]
#     # memory = x16asm.machine_code(asm_code)
#     memory += [0] * 65535
#     final_memory = x16vm.run(memory)
#     # 这时候要看的是a1 a2等寄存器的值
#     print('lenth of memory', len(memory))
#     print('lenth of final_memory', len(final_memory))
#     assert final_memory == memory, final_memory
#     # assert memory == memory_expected, memory
#     # assert memory == memory_expected, memory


# def test_asm_all():
#     asm_code = """
#     ;注释多行都有
#     jump @1024 ;注释真的很多
#     .memory 1024
#     set2 f1 3 设置内存起始点为3开始
#     jump @function_end ; 注释非常多
        #     @function_multiply
        #     set2 a3 2 设定初始a3计数因为是less判断所以要用2
        #     save2 a1 @65534   存储a1的值
        #     @while_start 和下面三句设置循环初始条件
            #     compare a2 a3
            #     jump_if_less @while_end
            #     save2 a2 @65532 存储a2的值
            #     set2 a2 1 设置步进长度a2
            #     add2 a3 a2 a3 计数器当前值
            #     load2 @65534 a2   此时a2又变成被加数把a1之前保存的放到a2里面
            #     add2 a1 a2 a1 把a1中加入a2
            #     load2 @65532 a2  读取a2原始的计数值10
            #     jump @while_start
        #     @while_end
        #     set2 a3 2 此处设置也是为了a3为2给下面减去内存2
        #     subtract2 f1 a3 f1    
        #     load_from_register2 f1 a2
        #     jump_from_register a2
    #     @function_end
    #     set2 a1 300
    #     set2 a2 10
    #     set2 a3 14 设置14是到最后的步数
    #     add2 pa a3 a3 把pa指向最后的步数存到f1
    #     save_from_register2 a3 f1 把数据从那时候开始开发地址
    #     set2 a3 2 往下两步手动开辟栈空间来调用函数
    #     add2 f1 a3 f1 从下面再开辟地址
#     jump @function_multiply
#     halt
#     """
#     memory_expected = [6, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 80, 3, 0, 6, 61, 4, 8, 48, 2, 0, 11, 16, 254, 255, 4, 32, 48, 5, 48, 4, 11, 32, 252, 255, 8, 32, 1, 0, 10, 48, 32, 48, 9, 254, 255, 32, 10, 16, 32, 16, 9, 252, 255, 32, 6, 15, 4, 8, 48, 2, 0, 12, 80, 48, 80, 14, 80, 32, 16, 32, 8, 16, 44, 1, 8, 32, 10, 0, 8, 48, 14, 0, 10, 0, 48, 48, 15, 48, 80, 8, 48, 2, 0, 10, 80, 48, 80, 6, 7, 4, 255]
#     # memory_expected = memory_expected[: 2] + [0] * 1022 + memory_expected[2 :]
#     memory = x16asm.machine_code(asm_code)
#     print('lenth of memory', len(memory))
#     print('lenth of memory_expected', len(memory_expected))
#     # print('memory', memory)
#     # funct_muti = get_memory_u16(7, 4)
#     # print('funct_muti', funct_muti)
#     # funct_end = get_memory_u16(61, 4)
#     # print('funct_end', funct_end)
#     # while_start = get_memory_u16(15, 4)
#     # print('while_start', while_start)
#     # while_end = get_memory_u16(48, 4)
#     # print('while_end', while_end)
#     # for i in range(len(memory)):
#         # if i > 1024:
#             # print('i', i, memory[i])
#         # if memory[i] != memory_expected[i]:
#             # print('diff i now', i, memory[i], memory_expected[i])
#     assert memory == memory_expected, memory
#     # assert new_action == memory_expected, new_action
#     # assert new_reg == memory_expected, new_reg