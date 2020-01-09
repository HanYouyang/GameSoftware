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
def test_mutiply():
    memory = [
        'jump', '@1024',
        'set2', 'f1', 3,
        'jump', '@function_end',

        '@function_multiply',
        'set2', 'a3', 2,
        'save2', 'a1', '@65534',
        '@while_start',
        'compare', 'a2', 'a3',
        'jump_if_less', '@while_end',
        'save2', 'a2', '@65532',
        'set2', 'a2', 1,
        'add2', 'a3', 'a2', 'a3',
        'load2', '@65534', 'a2',
        'add2', 'a1', 'a2', 'a1',
        'load2', '@65532', 'a2',# '@65532',
        'jump', '@while_start',
        '@while_end',
        'set2', 'a3', 2,
        'subtract2', 'f1', 'a3', 'f1',
        'load_from_register2', 'f1', 'a2',
        'jump_from_register', 'a2',
        '@function_end',

        'set2', 'a1', 300,
        'set2', 'a2', 10,
        'set2', 'a3', 14,
        'add2', 'pa', 'a3', 'a3',
        'save_from_register2', 'a3', 'f1',
        'set2', 'a3', 2,
        'add2', 'f1', 'a3', 'f1',
        'jump', '@function_multiply',
        'halt',
    ]
    memory = memory[: 2] + [0] * 1022 + memory[2 :] + [0] * 65566
    print('len of memory', len(memory))
    regNum, labelDict, finalMem = x16vm.run(memory)
    print('labelDict[@function_multiply]', labelDict['@function_multiply'])

    labelDictExpected = {
        '@function_multiply': 1029, # 不行得继续加上所有功能
        '@while_start': 15,
    }
    # print('labelDict[@function_multiply]', labelDict['@function_multiply'])

    assert labelDict['@function_multiply'] == labelDictExpected['@function_multiply'], labelDict
    # assert labelDict['@while_start'] == labelDictExpected['@while_start'], labelDict
# def test_1024():
    # memory = [
    #     'jump', '@1024',
    #     'halt',
    # ]
    # memory = memory[: 2] + [0] * 1022 + memory[2 :] + [0] * 4177
    # print('memory[1024]', memory[1024])
    # print('memory[1025]', memory[1025])
    # print('memory[1026]', memory[1026])

    # regNum, mem = x16vm.run(memory, 0)
    # # expectedA1 = 0
    # print('regNum[a1]', regNum['a1'])
    # print('regNum', regNum)

    # # assert finalCode['a2'] == expectedA2, finalCode
    # memExpected = [0] * 4177 # 单点测算mem值
    # low, high = set_memory_u16(4176)
    # memExpected[50] = low
    # memExpected[51] = high
    # assert mem[50] == memExpected[50], mem[50]
    # assert mem[51] == memExpected[51], mem

# def test_1024():
#     memory = [
#         'jump', '@1024',
#         'set', 'a1', 50,
#         'set', 'a2', 2,
#         'add', 'a1', 'a2', 'a3', # 此时a3为52
#         # 'compare', 'a1', 'a2',
#         # 'jump_if_less', '@4176',
#         # 'jump', '@4176',
#         'set2', 'a11', 4176,
#         'add2', 'a11', 'a22', 'a22',# 此时a22是4176
#         'load2', 'a33', '@4175',
#         'save2', '@4175', 'a11', 
#         'subtract2', 'a11', 'a22', 'a11',# 此时a11是-4176
#         'load_from_register2', 'a22', 'a11', # 此时a22是4176使得内存4176位的0给a11
#         'save_from_register2', 'a22', 'a1', # 此时a22是4176使得内存50和51位的拆开
#         # 'jump_from_register', 'a1', 
#         'halt',
#     ]
#     memory = memory[: 2] + [0] * 1022 + memory[2 :] + [0] * 4177
#     print('memory[1024]', memory[1024])
#     print('memory[1025]', memory[1025])

#     # print('memory[1026]', memory[1026])

#     regNum, mem = x16vm.run(memory)
#     # expectedA1 = 0
#     # print('regNum[a1]', regNum['a1'])
#     print('regNum', regNum)
#     print('regNum[a33]', regNum['a33'])
#     print('regNum[a11]', regNum['a11'])
#     print('regNum[a22]', regNum['a22'])
#     print('memory[4175]', memory[4175])

#     # assert finalCode['a2'] == expectedA2, finalCode

#     print('mem[50]', mem[50])
#     print('mem[51]', mem[51])
#     for i, e in enumerate(mem):
#         if mem[i] == 80:
#             print('mem[i]', i, mem[i])
#             print('mem[i + 1]', i + 1, mem[i + 1])
#     memExpected = [0] * 4177 # 单点测算mem值
#     low, high = set_memory_u16(4176)
#     memExpected[50] = low
#     memExpected[51] = high
#     print('memExpected[50]', memExpected[50])
#     print('memExpected[51]', memExpected[51])
#     assert mem[50] == memExpected[50], mem[50]
#     assert mem[51] == memExpected[51], mem

# def test_translate_int():
#     memory = [
#         'set', 'a1', 50,
#         'set', 'a2', 2,
#         'add', 'a1', 'a2', 'a3', # 此时a3为52
#         'compare', 'a1', 'a2',
#         'jump_if_less', '@4176',
#         'jump', '@4176',
#         'set2', 'a11', 4176,
#         'add2', 'a11', 'a22', 'a22',
#         'load2', 'a33', '@4175',
#         'save2', '@4175', 'a11',
#         'subtract2', 'a11', 'a22', 'a11',
#         'load_from_register2', 'a22', 'a11', # 此时a22是4176使得内存4176位的0给a11
#         'save_from_register2', 'a22', 'a1', # 此时a22是4176使得内存50和51位的拆开
#         'jump_from_register', 'a1', 
#         'halt',
#     ]
#     memory = memory + [0] * 4177
#     # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     # 测寄存器直接看寄存器值
#     # regNum = x16vm.run(memory)
#     regNum, mem = x16vm.run(memory)
#     # expectedA1 = 0
#     # assert finalCode['a1'] == expectedA1, finalCode
#     # expectedA2 = 0
#     # assert finalCode['a2'] == expectedA2, finalCode
#     memExpected = [0] * 200 # 单点测算mem值
#     low, high = set_memory_u16(4176)
#     memExpected[50] = low
#     memExpected[51] = high
#     assert mem[50] == memExpected[50], mem
#     assert mem[51] == memExpected[51], mem

#     # memExpected[100] = 50
#     # assert mem[100] == memExpected[100], mem
#     # memExpected[101] = 0
#     # assert mem[101] == memExpected[101], mem
#     # assert finalCode['c1'] == 2, finalCode
#     # assert finalCode['pa'] == 4176, finalCode
#     # assert finalCode['a11'] == 0, finalCode
#     # assert finalCode['a22'] == 4176, finalCode
#     # memExpected[4175] = 4176
#     # assert mem[4175] == memExpected[4175], mem







# def test_translate_int():
#     memory = [
#         'set', 'a1', 50,
#         'set', 'a2', 2,
#         'add', 'a1', 'a2', 'a3', # 此时a3为52
#         'save', '@100', 'a1', # 此时a1为50 第100位是50
#         'load', 'a2', '@101', # 此时a2为0
#         'compare', 'a1', 'a2',
#         'jump_if_less', '@4176',
#         'jump', '@4176',
#         'set2', 'a11', 4176,
#         'add2', 'a11', 'a22', 'a22',
#         'load2', 'a33', '@4175',
#         'save2', '@4175', 'a11',
#         'subtract2', 'a11', 'a22', 'a11',
#         'load_from_register', 'a3', 'a1', # 此时a3的52使得内存52位的0给a1
#         'load_from_register', 'a22', 'a11', # 此时a22是4176使得内存4176位的0给a11
#         'halt',
#     ]
#     memory = memory + [0] * 4177
#     # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     # 测寄存器直接看寄存器值
#     # regNum = x16vm.run(memory)
#     # print('regNum', regNum)
#     finalCode, mem = x16vm.run(memory)
#     expectedA1 = 0
#     assert finalCode['a1'] == expectedA1, finalCode
#     expectedA2 = 0
#     assert finalCode['a2'] == expectedA2, finalCode
#     memExpected = [0] * 4177 # 单点测算mem值
#     memExpected[100] = 50
#     assert mem[100] == memExpected[100], mem
#     memExpected[101] = 0
#     assert mem[101] == memExpected[101], mem
#     assert finalCode['c1'] == 2, finalCode
#     assert finalCode['pa'] == 4176, finalCode
#     assert finalCode['a11'] == 0, finalCode
#     assert finalCode['a22'] == 4176, finalCode
#     memExpected[4175] = 4176
#     assert mem[4175] == memExpected[4175], mem
#     # memExpected[52] = 50
#     # assert mem[52] == memExpected[52], mem





