"""varios.py - tres comprobaciones sueltas: (1) 50 anillos ($2F con D07B=49) acaban el nivel, (2) pergamino $3F con 2 jugadores (busca en la tabla de claves de 2P, $B564),
(3) esperar tecla de disparo con joystick Kempston ($AD9E).
Uso: python3 -I varios.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def go(pokes, frames, keys=lambda f: set(), kemp=None, watch=()):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
    if kemp is not None: tr.kemp = kemp
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; vis = set()
    while frame < frames:
        pc = reg[24]; vis.add(pc); ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame)
            else: nxt += fd
    return mem, vis
m, v = go({0xDE5A+17: 0x2F, 0xD07B: 49, 0xD3A7: 24, 0xD3A8: 16, 0xD39A: 5}, 60)
print('1) 49 anillos + anillo: nivel 5 ->', m[0xD39A], '| $B405:', 0xB405 in v)
m, v = go({0xDE5A+17: 0x3F, 0xD3A7: 24, 0xD3A8: 16, 0xD39A: 12, 0xD91D: 2}, 120, keys=lambda f: {'SPACE'} if 40 <= f < 50 else set())
print('2) pergamino con 2 jugadores en el nivel 12: pasa por $B564:', 0xB564 in v, '| clave mostrada ($B572):', 0xB572 in v)
# (3) recuperar el orbe lanzado: segunda pulsación larga con el orbe en vuelo ($B011-$B026)
def bit6(m): return (m[0xD3BC] >> 6 & 1, m[0xD3BB])
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
mem[0xD3BC] = 0x18; mem[0xD3C0] = 0xC0
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; out = []; vis = set()
keys = lambda f: {'SPACE'} if (6 <= f < 80 or 140 <= f < 200) else set()
while frame < 220:
    pc = reg[24]; vis.add(pc); ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd; tr.pressed = keys(frame)
                if frame % 20 == 0: out.append((frame, bit6(mem)))
        else: nxt += fd
print('3) orbe lanzado (bit6 de +15, contador +14) por frame:', out, '| recuperacion $B01E:', 0xB01E in vis)
# (4) poder del jugador 2 que caduca ($AFCA-$AFE2)
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
mem[0xD91D] = 2; mem[0xD3D9] = 0x18; mem[0xD3DD] = 3; vis = set()
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
while frame < 100:
    pc = reg[24]; vis.add(pc); ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd
        else: nxt += fd
print('4) poder del jugador 2 (+15 del J2 = $D3D9): $18 ->', hex(mem[0xD3D9]), '| pasa por $AFE2:', 0xAFE2 in vis)
