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



## 版本1固定分配内存位置
jump @1024 
.memory 1024
set2 f1 3 
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

        .return {0} ;这里应存储.return多少？？？
    @function_end

    set a1 1
    load2 a2 @65532
    .call @multiply {a2, a1} 

halt

.call @factorial 未知什么时候用



版本2 手动用f1存储内存位置

jump @1024 
.memory 1024
set2 f1 3 
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

        .return {0} ;这里应存储.return多少？？？
    @function_end

    set a1 1
    load2 a2 @65532
    .call @multiply {a2, a1} 

halt

原理是现在需要让内存中的函数不要使用旧的方式固定内存位置
而是使用自动开辟的新内存空间
方法：
1.不要动用 f1, 用寄存器来做加减这个事情, 推荐这种方式
set2 a3 4
sub2 f1 a3 a3 ; 这里我忘了 sub 的全称了, 以后可以变成伪指令 .sub 这样就好记了
load_from_register2 a3 a1 ; 这里假设将内存中的值给 a1
; 这种方式没有改变 f1 的值

2.每次用完 f1 就恢复 f1 的值
set2 a3 4
; 注意这里的区别, 取内存的值是通过 f1 的
sub2 f1 a3 f1 ; 这里我忘了 sub 的全称了, 以后可以变成伪指令 .sub 这样就好记了
load_from_register2 f1 a1 ; 这里假设将内存中的值给 a1

; 恢复 f1 的值, 前面 -4 这里就要 +4
; 用一个用不到的 寄存器做加减
set2 a3 4
add2 f1 a3 f1

总结：
这样前两者的函数都得改造 重新计算f1的情况

先按照方法2改写mutiply：
jump @1024 
.memory 1024
set2 f1 3 
        @multiply
            ;最下面开始的时候是给了寄存器数值
            ;现在是直接给函数参数
                        
            set2 a1 {a1}
            set2 a2 {a2}

            set2 a3 2;设置两次变量相加都需要的内存长度
            add2 f1 a3 f1
            save_from_register2 a1 f1 ;设置f1位置的值为a1
            add2 f1 a3 f1
            save_from_register2 a2 f1 ;设置f1位置的值为a2
            ;save_from_register2代替save就是用来获得局部变量的？
            
            set2 a3 2 ;获得a3的比较值
            ;save2 a1 @65534   ;存储a1的值
            ;原来上一语句是存储a1的现在不用

            @while_multiply_start 和下面三句设置循环初始条件
                compare a2 a3
                jump_if_less @while_multiply_end

                ;save2 a2 @65532 ;存储a2的值
                ;上面这句此时没必要 
                set2 a1 2
                substract f1 a1 f1        ;此时获得之前的a2值
                save_from_register2 f1 a2 ;因为a2在f1 - 2 里面

                set2 a2 1     ;设置步进长度a2
                add2 a3 a2 a3 ;计数器当前值
                
                ;load2 @65534 a2   ;此时a2又变成被加数把a1之前保存的放到a2里面
                ;单个语句被翻译成下面的语句 此时获得a2累加值就是当下的a1
                set2 a1 2
                substract f1 a1 f1        ;此时获得之前的a1值
                load_from_register2 f1 a2 ;此时的a2是之前的a1

                add2 a1 a2 a1 ;把原始a1的值加入a2
                
                set2 a1 2
                add2 f1 a1 f1 ;此时获得之前的a2值
                ;load2 @65532 a2          ;读取a2原始的计数值10
                load_from_register2 f1 a2 ;读取a2原始的计数值10

                set2 a1 2   
                add2 f1 a1 f1 ;回到开始的指针位置

                jump @while_multiply_start
            @while_multiply_end
            
            ;set2 a3 {4} 此处设置也是为了a3为2给下面减去内存2
            ;subtract2 f1 a3 f1    
            ;load_from_register2 f1 a2
            ;jump_from_register a2
            .return {4} ;以上内容是.return的翻译

        @multiply_end


        ;set2 a1 {a1} ;最下面开始的时候是给了寄存器数值
        ;set2 a2 {a2} ;现在要用参数内部值所以这两行也没了
        ;set2 a3 14 设置14是到最后的步数
        ;add2 pa a3 a3 把pa指向最后的步数存到f1
        ;save_from_register2 a3 f1 把数据从那时候开始开发地址
        ;set2 a3 2 往下两步手动开辟栈空间来调用函数
        ;add2 f1 a3 f1 从下面再开辟地址
        ;jump @multiply
        .call @multiply {a1, a2}

jump @function_factorial_end ; 注释非常多

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

        .return {0} ;这里应存储.return多少？？？
    @function_factorial_end

    set a1 1
    load2 a2 @65532
    .call @multiply {a2, a1} 

halt



再按照方法2简化之前的思路

jump @1024 
.memory 1024
set2 f1 3 
jump @function_factorial_end ; 注释非常多
        @multiply
            set2 a3 2                   ;设置步长为2

            save_from_register2 a1 f1   ;设置f1位置的值为累加值final_a 此时f1指向的是原始f1+0
            add2 f1 a3 f1               ;计算此时f1值
            save_from_register2 a1 f1   ;设置f1位置的值为a1 此时f1指向的是f1+2
            add2 f1 a3 f1               ;步进f1值
            save_from_register2 a2 f1   ;设置f1位置的值为a2 此时f1指向的是f1+4
            add2 f1 a3 f1               ;步进f1值
            save_from_register2 a3 f1   ;设置f1位置的值为c即2 此时f1指向的是f1+6
            add2 f1 a3 f1               ;步进f1值
            save_from_register2 a3 f1   ;设置f1位置的值为final_c即2 此时f1指向的是f1+8

            set2 a1 8                   ;不动a2和a3
            subtract2 f1 a1 f1          ;复位f1

            @while_multiply_start
                    compare a2 a3             ;比较a2（此时为原始比较值a2）和a3（此时为计数器c）
                    jump_if_less @while_multiply_end 


                    set2 a2 1                 ;设置计数器累加步长为1
                    add2 a3 a2 a3             ;计数器a3 + 1
                    set2 a2 8                 ;获得步进字节长度为2
                    add2 f1 a2 f1             ;f1 + 6位置此时用f1指向计数器c = 2
                    save_from_register2 a3 f1 ;存储计数器值到f1 + 8
                                              ;c += 1 完成

                    ;最末位代表地址指向的内存位置值 是累加的
                    ;原始f1和原始f1 + 8应该是不变的
                    set2 a3 6                 
                    subtract2 f1 a3 f1        ;倒退f1 + 4长度4字节指向f1 + 2即原始参数a1
                    load_from_register2 f1 a2 ;拿到原始参数a1值即300
                    set2 a3 2                 ;获得步进字节数为6
                    subtract2 f1 a3 f1        ;倒退f1 + 2长度2字节指向f1即累加值
                    load_from_register2 f1 a1 ;拿到累加值存到a2
                    add2 a1 a2 a1             ;把原始参数a1累加到a2
                    save_from_register2 a1 f1 ;存储a2参数到此时指向的f1即累加位置
                                              ;final_a += a完成
                                              ;此时已经自动指回f1开始位置 还需要.return么？
                    
                    set2 a1 4
                    add2 f1 a1 f1
                    load_from_register2 f1 a2 ;拿回a2 此时f1指向f1 + 4
                    add2 f1 a1 f1
                    load_from_register2 f1 a3 ;拿回计数器 此时f1指向f1 + 8

                    set2 a1 8
                    subtract2 f1 a1 f1 ;回复第一圈开始位置为f1
                        
                    jump @while_multiply_start
            @while_multiply_end
            
            load_from_register2 f1 a1 

            .return 0

        @multiply_end    


    @factorial
        ; 函数开始 设置f1 + 3
        set2 a3 2
        add2 f1 a3 f1
        save_from_register2 a1 f1   ;设置f1位置的值为a1 此时f1指向的是原始f1+0
        add2 f1 a3 f1
        save_from_register2 a1 f1   ;设置f1位置的值为a1 此时f1指向的是原始f1+2
        add2 f1 a3 f1
        save_from_register2 a2 f1   ;设置f1位置的值为a2 此时f1指向的是原始f1+4
        add2 f1 a3 f1
        save_from_register2 a2 f1   ;设置f1位置的值为a2 此时f1指向的是原始f1+6

        set2 a3 6                   
        subtract2 f1 a1 f1          ;复位f1

        set2 a3 2 
        
        compare a1 a3
        jump_if_less @function_factorial_end

            set2 a3 1
            subtract2 a1 a3 a1
            save_from_register2 a1 f1   ;存储计数器


            .call @factorial a1 a1
            .call @multiply a1 a2       ;这里重新把里面加上参数

            set2 a3 6
            add2 f1 a3 f1
            load_from_register2 a1 f1   ;存到累加器里面

            jump @while_multiply_start
        @while_multiply_end

        set2 a1 1                    ;a1负责
        .call @multiply a1 a2

        .return 0
    @function_factorial_end

    set2 a1 5
    .call @factorial a1 a1 ;后一个a1实则是a2

halt

