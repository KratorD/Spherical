"""orbe45.py - ¿de dónde sale el fotograma $45 del registro del orbe (D3E3) en el nivel 80? Sondea D3E3 cada trama.
Uso: python3 -I orbe45.py tape/mundo8.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; tr.pressed = {'1'}; n = 0; prev = None
seq = [{'o'}, {'p'}, {'q'}, {'a'}, {'SPACE'}, {'p', 'q'}, {'o', 'q'}, set()]
while frame < 1500 and n < 80000000:
    pc = reg[24]; ops[mem[pc]](); n += 1
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, pc)
        frame += 1; nxt += fd
        tr.pressed = {'1'} if frame < 12 else ({'r'} if 150 <= frame < 156 else seq[(frame//14) % len(seq)])
        if frame > 20: mem[0xD079] = 255
        if frame == 140: mem[0xD39A] = 80; mem[0xD98B] = 8; mem[0xD91D] = 1
        v = (mem[0xD3E3], mem[0xD3BC] & 0x18, mem[0xD39A])
        if v != prev: print(frame, 'D3E3=%02X D3BC&18=%02X nivel=%d' % v, 'DC3A=%d' % mem[0xDC3A]); prev = v
