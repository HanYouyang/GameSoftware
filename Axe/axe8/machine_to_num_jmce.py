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
    asm_machine_code = """00000000 00010000 00000001
    00000000 00010000 00000001
    00000010 00010000 00100000 00110000
    00000011 00010000 01010000 00010000
    00000001 01010000 00010000 00010000
    00000100 00010000 00100000
    00000101 01010000 00010000
    00000110 01010000 00010000
    00001000 00100000 01010000 00010000
    00001010 00010000 00100000 00110000
    00001001 01010000 00010000 00100000
    00001011 00100000 01010000 00010000
    00001100 00010000 00100000 00010000
    00001110 00010000 00100000
    00001101 00010000 00100000
    00010000 00010000
    00001111 00010000 00100000
    00000111 00010000 00100000
    11111111
    """
    asm_machine_code_expected = [
        'set', 'a1', 1,
        'set', 'a1', 1,
        'add', 'a1', 'a2', 'a3',
        'save', 'a1', '@4176',
        'load', '@4176', 'a1',
        'compare', 'a1', 'a2',
        'jump_if_less', '@4176',
        'jump', '@4176',
        'set2', 'a2', 4176,
        'add2', 'a1', 'a2', 'a3',
        'load2', '@4176', 'a2',
        'save2', 'a2', '@4176',
        'subtract2', 'a1', 'a2', 'a1',
        'load_from_register2', 'a1', 'a2',
        'load_from_register', 'a1', 'a2',
        'jump_from_register', 'a1',
        'save_from_register2', 'a1', 'a2',
        'save_from_register', 'a1', 'a2',
        'halt',
    ]
    memory_expected = [
        0, 16, 1,        # 'set', 'a1', 1,
        0, 16, 1,        # 'set', 'a1', 1,
        2, 16, 32, 48,   # 'add', 'a1', 'a2', 'a3',
        3, 16, 4176,    # 'save', 'a1', '@4176',
        1, 4176, 16,    # 'load', '@4176', 'a1',
        4, 16, 32,  # 'compare', 'a1', 'a2',
        5, 4176,    # 'jump_if_less', '@4176',
        6, 4176,    # 'jump', '@4176',
        8, 32, 4176,    # 'set2', 'a2', 4176,
        10, 16, 32, 48, # 'add2', 'a1', 'a2', 'a3',
        9, 4176, 32,    # 'load2', '@4176', 'a2',
        11, 32, 4176,   # 'save2', 'a2', '@4176',
        12, 16, 32, 16, # 'subtract2', 'a1', 'a2', 'a1',
        14, 16, 32,     # 'load_from_register2', 'a1', 'a2',
        13, 16, 32,     # 'load_from_register', 'a1', 'a2',
        16, 16,         # 'jump_from_register', 'a1',
        15, 16, 32,     # 'save_from_register', 'a1', 'a2',
        7, 16, 32,     # 'save_from_register', 'a1', 'a2',
        255,            # 'halt',
    ]
    asm, memory = x16asm.machine_code(asm_machine_code)
    assert asm == asm_machine_code_expected, asm
    # print('asm', asm)
    assert memory == memory_expected, memory