# import asm
from asm import machine_code

# def test():
#     pass
#     assert False, 'Hello'

def test1():
    asm = 'set a1 1'
    expected = [0, 16, 1]
    output = machine_code(asm)
    assert output == expected, output

