"""tecleotest.py - llama directamente a $AE6B (entrada de texto) y teclea S K Y, DELETE ('0'), F, ENTER; el resultado debe ser SKF.
Uso: python3 -I tecleotest.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
keytrace.KEYS.update({'k': (0xBF, 2), 'y': (0xDF, 4), 's': (0xFD, 1), 'f': (0xFD, 3), '0': (0xEF, 0), 'ENTER': (0xBF, 0)})
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
reg[24] = 0xAE6B; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF   # dirección de retorno ficticia
reg[26] = 1
keys = ['s', 'k', 'y', '0', 'f', 'ENTER']
sched = {(10+12*i, 16+12*i): k for i, k in enumerate(keys)}
cur = lambda f: {v for (a, b), v in sched.items() if a <= f < b}
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; ret = False
ops_n = 0
while frame < 120 and not ret and ops_n < 6000000:
    ops_n += 1
    if reg[24] == 0xFFF0: ret = True; break
    ops[mem[reg[24]]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, reg[24]):
                frame += 1; nxt += fd; tr.pressed = cur(frame)
                if frame % 10 == 0: print(frame, sorted(tr.pressed), hex(reg[24]), bytes(mem[0xDC44:0xDC48]))
        else: nxt += fd
print('ops', ops_n, 'IFF', reg[26], 'PC', hex(reg[24]))
print('terminó (RET con ENTER):', ret, '| frame', frame, '| búfer DC44 =', bytes(mem[0xDC44:0xDC44+13]))
