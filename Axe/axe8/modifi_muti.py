asm_code = """
    jump @1024 ;注释真的很多
    .memory 1024
    set2 f1 3 设置内存起始点为3开始
    jump @function_end ; 注释非常多

            @function_multiply
                set2 a3 2 设定初始a3计数因为是less判断所以要用2
                save2 a1 @65534   存储a1的值
                @while_start 和下面三句设置循环初始条件
                    compare a2 a3
                    jump_if_less @while_end
                    save2 a2 @65532 存储a2的值
                    set2 a2 1 设置步进长度a2
                    add2 a3 a2 a3 计数器当前值
                    load2 @65534 a2   此时a2又变成被加数把a1之前保存的放到a2里面
                    add2 a1 a2 a1 把a1中加入a2
                    load2 @65532 a2  读取a2原始的计数值10
                    jump @while_start
                @while_end
                set2 a3 2 此处设置也是为了a3为2给下面减去内存2
                subtract2 f1 a3 f1    
                load_from_register2 f1 a2
                jump_from_register a2
            @function_end

        set2 a1 300
        set2 a2 10
        set2 a3 14 设置14是到最后的步数
        add2 pa a3 a3 把pa指向最后的步数存到f1
        save_from_register2 a3 f1 把数据从那时候开始开发地址
        set2 a3 2 往下两步手动开辟栈空间来调用函数
        add2 f1 a3 f1 从下面再开辟地址
        jump @function_multiply
    
    halt




jump @1024 
.memory 1024
set2 f1 3 
jump @function_end ; 注释非常多

    @factorial
        ; 函数开始 设置f1 + 3
        set2 a3 3
        add2 f1 a3 f1

        set2 a1 {a1} ;a1是递减的
        load2 a2 @65532 ;a2是累乘的 放在65532位置
        ;a3是可变存储递减的1和比较的2

        ; 比较a1当前值
        set2 a3 2
        compare a1 a3
        jump_if_less @function_end
        
        ; 此时a1比较结束开始递减
        set2 a3 1
        substract a1 a3 a1
        save2 a1 @65534 ;存储a1到地址
        save2 a2 @65532 ;存储a2到地址

        .call @factorial {a1}
        .call @multiply {a2, a1} ;这里重新把里面加上参数
        ; 此时mutiply存储a2应该在某位置

        .return 3 ;这里应存储.return多少？？？
    @function_end

    set a1 1
    load2 a2 @65532
    .call @multiply {a2, a1} 

halt

.call @factorial 未知什么时候用
