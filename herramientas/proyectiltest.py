"""proyectiltest.py - lanzador tipo 5 junto al borde derecho: su proyectil sale de pantalla (x >= $6A, rama $BA88-$BA8C) y +$07 vuelve a 0.
Uso: python3 -I proyectiltest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
for i in range(140): mem[0xDE5A+i] = 0 if i < 126 else mem[0xDE5A+i]
mem[0xD52C] = 1; b = 0xD3F8
mem[b] = 0x58; mem[b+1] = 0x40; mem[b+2] = 0x24; mem[b+7] = 0; mem[b+8] = 5; mem[b+9] = 0x0A
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; vis = set(); xs = []
while frame < 160:
    pc = reg[24]; vis.add(pc); ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd
                if frame % 8 == 0: xs.append(mem[b+7])
        else: nxt += fd
print('+$07 (casillas recorridas) cada 8 frames:', xs, '| sale de pantalla $BA88:', 0xBA88 in vis)
