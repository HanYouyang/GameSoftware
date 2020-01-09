def regsMapper():
    regs = {
    'pa': '00000000',
    'f1': '01010000',  # pa内存位置专用寄存器
    'a1': '16',
    'a2': '00100000',
    'a3': '00110000',
    'c1': '01000000', 
    }
    return regs
def machine_code(asm):
    memory = []
    code = asm.split()
    if code[0] == 'set':
        reg = code[1]
        regs = regsMapper()
        r = int(regs[reg])
        value = int(code[2])
        memory.append(0)
        memory.append(r)
        memory.append(value)
    return memory

