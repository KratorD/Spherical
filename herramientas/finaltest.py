"""finaltest.py - mundo 8, nivel 80: deja el jefe con 1 de vida, lanza el orbe contra él y comprueba que se ejecuta $AD45 (pantalla final)."""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
sched = lambda f: {'1'} if 5 <= f < 12 else ({'r'} if 150 <= f < 156 else set())
tr.pressed = sched(0); hit = None
while frame < 900 and hit is None:
    pc = reg[24]
    if pc == 0xAD45: hit = frame; break
    ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd; tr.pressed = sched(frame)
                if frame % 100 == 0: print(frame, mem[0xD39A], mem[0xDC3A], flush=True)
                if frame == 140: mem[0xD39A] = 80; mem[0xD98B] = 8; mem[0xD91D] = 1
                if frame == 200: mem[0xDC3A] = 1; mem[0xD3A7] = 0x24; mem[0xD3A8] = 0x28; mem[0xD3BC] = 0x08; mem[0xD3C0] = 0xC0
        else: nxt += fd
print('AD45 alcanzado en el frame', hit, '| nivel', mem[0xD39A], 'vida jefe', mem[0xDC3A])
