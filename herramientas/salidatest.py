"""salidatest.py - la esfera llega a la casilla de salida $44 ($B7AF/$B7BB): el nivel pasa al siguiente. Se coloca la salida delante de la esfera.
Uso: python3 -I salidatest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
print('esfera (x,y,dir):', mem[0xD3F0], mem[0xD3F1], mem[0xD3F7], '| nivel', mem[0xD39A])
x, y, dr = mem[0xD3F0], mem[0xD3F1], mem[0xD3F7]
row = (y >> 4) * 14
col = (x >> 3)
for c in range(14):                       # suelo bajo la esfera y salida a 3 casillas en su direccion
    if mem[0xDE5A+row+14+c] == 0: mem[0xDE5A+row+14+c] = 0x2D+0x1A     # suelo ($47)
    if c != col: mem[0xDE5A+row+c] = mem[0xDE5A+row+c] if mem[0xDE5A+row+c] >= 0x2D else 0
dest = col + (3 if dr in (1,) else -3)
mem[0xDE5A+row+max(0, min(13, dest))] = 0x44
vis = set(); fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; n0 = mem[0xD39A]
while frame < 200 and mem[0xD39A] == n0:
    pc = reg[24]; vis.add(pc); ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd
        else: nxt += fd
print('nivel tras', frame, 'frames:', mem[0xD39A], '| pasa por $B7BB:', 0xB7BB in vis)
