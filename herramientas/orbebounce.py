"""orbebounce.py - orbe lanzado: trayectoria completa (x, y, direccion +$1A) con rebotes en paredes/suelo/techo, y colision con un enemigo caminante tipo 0.
Uso: python3 -I orbebounce.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def go(pokes, sched, frames, probe, every):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; tr.pressed = set(sched(0)); out = []
    while frame < frames:
        pc = reg[24]; ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    frame += 1; tr.pressed = set(sched(frame)); nxt += fd
                    if frame % every == 0: out.append((frame, probe(mem)))
            else: nxt += fd
    return out
print('1) trayectoria del orbe lanzado (frame, (x, y, +1A, bit6 de +15))')
for r in go({0xD3BC: 0x18, 0xD3C0: 0xC0}, lambda f: {'SPACE'} if 6 <= f < 130 else set(), 220, lambda m: (m[0xD3E1], m[0xD3E2], m[0xD3C1], m[0xD3BC] >> 6 & 1), 10): print(r)
print('2) orbe orbitando contra un caminante tipo 0 colocado a 16 px del jugador: (x enemigo, D3E1)')
base = {0xD3BC: 0x08, 0xD3C0: 0xC0, 0xD52C: 1, 0xD3F8: 40, 0xD3F9: 16, 0xD3FA: 0x24, 0xD3FF: 0xFF, 0xD400: 0}
for r in go(base, lambda f: set(), 60, lambda m: (m[0xD3F8], m[0xD3E1], m[0xD3E2]), 5): print(r)
