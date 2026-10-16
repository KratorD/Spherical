"""orbtest.py - comprueba en el simulador: (1) lanzamiento del orbe, (2) reloj de arena, (3) casilla $3E (bloqueo de bloques).
Uso: python3 -I orbtest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def go(pokes, sched, frames, probe, every=8):
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
print('1) orbe: poder doble (+15 bit4), mantener SPACE')
for f, r in go({0xD3BC: 0x18, 0xD3C0: 0xC0}, lambda f: {'SPACE'} if f >= 6 else set(), 80, lambda m: (m[0xD3BB], hex(m[0xD3BC]), (m[0xD3E1], m[0xD3E2])), 8): print(f, r)
print('2) reloj de arena: D920=$05, esfera (x,y,frame,D920)')
for f, r in go({0xD920: 5}, lambda f: set(), 240, lambda m: (m[0xD3F0], m[0xD3F1], m[0xD3F2], m[0xD920]), 20): print(f, r)
print('3) casilla $3E: contar bloques rojos tras pulsar y soltar SPACE con +15 bit7 = 0 / 1')
cnt = lambda m: sum(1 for i in range(140) if m[0xDE5A+i] in (0x45, 0x46, 0x47, 0x48))
for bit in (0, 0x80):
    r = go({0xD3BC: bit}, lambda f: {'SPACE'} if 6 <= f < 14 else set(), 60, cnt, 60)
    print('+15 =', hex(bit), 'bloques', r)
print('4) matraz verde $35 (+15 bit2): enemigo tipo 0 inmovil / con bit2 = 0 se mueve')
sys.argv = ['x']
def rec0(m):
    return (m[0xD3F8], m[0xD3F9])
base = {0xD52C: 1, 0xD3F8: 0x30, 0xD3F9: 0x90, 0xD3FA: 0x24, 0xD3FF: 1, 0xD400: 0}
for bit in (0, 4):
    p = dict(base); p[0xD3BC] = bit
    print('+15 =', bit, go(p, lambda f: set(), 60, rec0, 20))
print('5) frasco azul $37 (+15 bit5): bloques rojos en el mapa tras 300 frames')
print(go({0xD3BC: 0x20}, lambda f: set(), 300, cnt, 100), go({0xD3BC: 0}, lambda f: set(), 300, cnt, 100))
print('6) flecha de diamante $58/$5A/$59 delante del jugador y acción de bloque: D91F (velocidad vertical de la esfera)')
for tile in (0x58, 0x59, 0x5A):
    pk = {0xDE5A+16: tile, 0xDE5A+18: tile, 0xDE5A+17: tile}
    print(hex(tile), go(pk, lambda f: {'SPACE'} if 6 <= f < 14 else set(), 40, lambda m: m[0xD91F], 20))
print('7) casilla $2E delante del jugador + acción de bloque: D39B y mapa cargado')
pk = {0xDE5A+16: 0x2E, 0xDE5A+17: 0x2E, 0xDE5A+18: 0x2E}
for f, r in go(pk, lambda f: {'SPACE'} if 6 <= f < 14 else set(), 400, lambda m: (hex(m[0xD39B]), m[0xD39A], bytes(m[0xDE5A:0xDE5A+14]).hex()), 50): print(f, r)
