"""bosstest.py - arranca el juego desde un snapshot de mundo (tape/mundoN.sna), empieza 1 jugador, salta al nivel de jefe (10*N) y observa vida del jefe y segmentos.
Uso: python3 -I bosstest.py tape/mundoN.sna N"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap, w = sys.argv[1], int(sys.argv[2])
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
def sched(f):
    if 5 <= f < 12: return {'1'}
    if 150 <= f < 156: return {'r'}
    return set()
tr.pressed = sched(0)
log = []
while frame < 700:
    pc = reg[24]; ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd; tr.pressed = sched(frame)
                if frame == 140: mem[0xD39A] = 10*w; mem[0xD98B] = w
                if frame == 200: mem[0xD3A7] = 0x34; mem[0xD3A8] = 0x40; mem[0xD3BC] = 0x08; mem[0xD3C0] = 0xC0
                if frame % 50 == 0:
                    n = mem[0xD52C]
                    log.append((frame, 'nivel', mem[0xD39A], 'mundo', mem[0xD98B], 'hpjefe', mem[0xDC3A], 'enem', n, [(mem[0xD3F8+22*k], mem[0xD3F9+22*k], mem[0xD3FA+22*k], mem[0xD3F8+22*k+8]) for k in range(min(n, 4))]))
            else: nxt += fd
for l in log: print(l)
