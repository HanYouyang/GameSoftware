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
    labelDictExpected = {
        '@function_multiply': 1029, # 不行得继续加上所有功能
        '@while_start': 15,
    }
    print('labelDict', labelDict)
    assert labelDict['@function_multiply'] == labelDictExpected['@function_multiply'], labelDict