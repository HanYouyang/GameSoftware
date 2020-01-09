from . import x16asm

def get_memory_u16(value1, value2):
    low = value1
    high = value2
    value = (high << 8) + low
    return value
def set_memory_u16(number: int):
    low = number & 0xFF
    high = (number >> 8) & 0xFF
    return low, high

def test11_subtract2_load_from_register2():
    asm_code = """00000000 00010000 00000001
    00000000 00010000 00000001
    00000010 00010000 00100000 00110000
    00000011 00010000 01010000 00010000
    00000001 01010000 00010000 00010000
    00000100 00010000 00100000
    00000101 01010000 00010000
    00000110 01010000 00010000
    00001000 00100000 01010000 00010000
    00001010 00010000 00010000 00100000 00100000 00110000 00110000
    00001001 01010000 00010000 00100000 00100000
    00001011 00100000 00100000 01010000 00010000
    00001100 00010000 00010000 00100000 00100000 00010000 00010000
    00001110 00010000 00010000 00100000 00100000
    00001101 00010000 00100000
    00010000 00010000
    11111111
    """
    # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
    expected = [
        'set', 'a1', 1,
        'set', 'a1', 1,
        'add', 'a1', 'a2', 'a3',
        'save', 'a1', '@4176',
        'load', '@4176', 'a1',
        'compare', 'a1', 'a2',
        'jump_if_less', '@4176',
        'jump', '@4176',
        'set2', 'a2', 4176,
        'add2', 'a11', 'a22', 'a33',
        'load2', '@4176', 'a22',
        'save2', 'a22', '@4176',
        'subtract2', 'a11', 'a22', 'a11',
        'load_from_register2', 'a11', 'a22',
        'load_from_register', 'a1', 'a2',
        'jump_from_register', 'a1',
        'halt',
    ]
    finalCode = x16asm.machine_code(asm_code)
    assert finalCode == expected, finalCode
def test10_subtract2_load_from_register2():
    asm_code = """00000000 00010000 00000001
    00000000 00010000 00000001
    00000010 00010000 00100000 00110000
    00000011 00010000 01010000 00010000
    00000001 01010000 00010000 00010000
    00000100 00010000 00100000
    00000101 01010000 00010000
    00000110 01010000 00010000
    00001000 00100000 01010000 00010000
    00001010 00010000 00010000 00100000 00100000 00110000 00110000
    00001001 01010000 00010000 00100000 00100000
    00001011 00100000 00100000 01010000 00010000
    00001100 00010000 00010000 00100000 00100000 00010000 00010000
    00001110 00010000 00010000 00100000 00100000
    00001101 00010000 00100000
    11111111
    """
    # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
    expected = [
        'set', 'a1', 1,
        'set', 'a1', 1,
        'add', 'a1', 'a2', 'a3',
        'save', 'a1', '@4176',
        'load', '@4176', 'a1',
        'compare', 'a1', 'a2',
        'jump_if_less', '@4176',
        'jump', '@4176',
        'set2', 'a2', 4176,
        'add2', 'a11', 'a22', 'a33',
        'load2', '@4176', 'a22',
        'save2', 'a22', '@4176',
        'subtract2', 'a11', 'a22', 'a11',
        'load_from_register2', 'a11', 'a22',
        'load_from_register', 'a1', 'a2',
        'halt',
    ]
    finalCode = x16asm.machine_code(asm_code)
    assert finalCode == expected, finalCode
# def test9_load2_save2():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     00000011 00010000 01010000 00010000
#     00000001 01010000 00010000 00010000
#     00000100 00010000 00100000
#     00000101 01010000 00010000
#     00000110 01010000 00010000
#     00001000 00100000 01010000 00010000
#     00001010 00010000 00010000 00100000 00100000 00110000 00110000
#     00001001 01010000 00010000 00100000 00100000
#     00001011 00100000 00100000 01010000 00010000
#     11111111
#     """
#     # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',
#         'save', 'a1', '@4176',
#         'load', '@4176', 'a1',
#         'compare', 'a1', 'a2',
#         'jump_if_less', '@4176',
#         'jump', '@4176',
#         'set2', 'a2', 4176,
#         'add2', 'a11', 'a22', 'a33',
#         'load2', '@4176', 'a22',
#         'save2', 'a22', '@4176',
#         'halt',
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode
# def test8_add2():
    asm_code = """00000000 00010000 00000001
    00000000 00010000 00000001
    00000010 00010000 00100000 00110000
    00000011 00010000 01010000 00010000
    00000001 01010000 00010000 00010000
    00000100 00010000 00100000
    00000101 01010000 00010000
    00000110 01010000 00010000
    00001000 00100000 01010000 00010000
    00001010 00010000 00010000 00100000 00100000 00110000 00110000
    11111111
    """
    # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
    expected = [
        'set', 'a1', 1,
        'set', 'a1', 1,
        'add', 'a1', 'a2', 'a3',
        'save', 'a1', '@4176',
        'load', '@4176', 'a1',
        'compare', 'a1', 'a2',
        'jump_if_less', '@4176',
        'jump', '@4176',
        'set2', 'a2', 4176,
        'add2', 'a11', 'a22', 'a33',
        'halt',
    ]
    finalCode = x16asm.machine_code(asm_code)
    assert finalCode == expected, finalCode
# def test7_jump_set2():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     00000011 00010000 01010000 00010000
#     00000001 01010000 00010000 00010000
#     00000100 00010000 00100000
#     00000101 01010000 00010000
#     00000110 01010000 00010000
#     00001000 00100000 01010000 00010000
#     11111111
#     """
#     # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',
#         'save', 'a1', '@4176',
#         'load', '@4176', 'a1',
#         'compare', 'a1', 'a2',
#         'jump_if_less', '@4176',
#         'jump', '@4176',
#         'set2', 'a2', 4176,
#         'halt',
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode
# def test6_jump_if_less():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     00000011 00010000 01010000 00010000
#     00000001 01010000 00010000 00010000
#     00000100 00010000 00100000
#     00000101 01010000 00010000
#     11111111
#     """
#     # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',
#         'save', 'a1', '@4176',
#         'load', '@4176', 'a1',
#         'compare', 'a1', 'a2',
#         'jump_if_less', '@4176',
#         'halt',
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode
# def test5_compare():
    asm_code = """00000000 00010000 00000001
    00000000 00010000 00000001
    00000010 00010000 00100000 00110000
    00000011 00010000 01010000 00010000
    00000001 01010000 00010000 00010000
    00000100 00010000 00100000
    11111111
    """
    # number = get_memory_u16(int('01010000', 2), int('00010000', 2))
    expected = [
        'set', 'a1', 1,
        'set', 'a1', 1,
        'add', 'a1', 'a2', 'a3',
        'save', 'a1', '@4176',
        'load', '@4176', 'a1',
        'compare', 'a1', 'a2',
        'halt',
    ]
    finalCode = x16asm.machine_code(asm_code)
    assert finalCode == expected, finalCode
# def test4_load_new():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     00000011 00010000 01010000 00010000
#     00000001 01010000 00010000 00010000
#     11111111
#     """
#     number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',
#         'save', 'a1', '@4176',
#         'load', '@4176', 'a1',
#         'halt',
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode

# def test3_save_new():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     00000011 00010000 01010000 00010000
#     """
#     number = get_memory_u16(int('01010000', 2), int('00010000', 2))
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',
#         'save', 'a1', '@4176',
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode
#     # assert false, finalCode

# def test2_add():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     00000010 00010000 00100000 00110000
#     """
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#         'add', 'a1', 'a2', 'a3',

#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     assert finalCode == expected, finalCode


# def test1_space():
#     asm_code = """00000000 00010000 00000001
#     00000000 00010000 00000001
#     """
#     expected = [
#         'set', 'a1', 1,
#         'set', 'a1', 1,
#     ]
#     finalCode = x16asm.machine_code(asm_code)
#     # print('finalCode', finalCode)
#     assert finalCode == expected, finalCode

# def test():
    asm_code = """00000000 00010000 00000001"""
    expected = ['set', 'a1', 1]
    finalCode = x16asm.machine_code(asm_code)
    assert finalCode == expected, finalCode
