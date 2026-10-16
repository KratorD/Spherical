"""recogetest.py - pone cada casilla de recogida ($2D-$3E, $41-$43) bajo el jugador 1 y registra el efecto (puntos, energia, bits +$15, temporizadores, D920, D98C, D07B, nivel).
Tambien: llaves $3B-$3D con puertas $55-$57 en el mapa, 2 pociones $33 seguidas (orbe -> poder doble) y la caducidad de los poderes.
Uso: python3 -I recogetest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def go(pokes, frames=40, keys=lambda f: set(), tiles_at=()):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    mem[0xD3A7] = 24; mem[0xD3A8] = 16
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
    est = lambda: dict(pts=mem[0xD3BD] | mem[0xD3BE] << 8, en=mem[0xD3EF], f15=mem[0xD3BC], t18=mem[0xD3BF], t19=mem[0xD3C0], D920=mem[0xD920], D98C=mem[0xD98C], D07B=mem[0xD07B], niv=mem[0xD39A], cel=mem[0xDE5A+17])
    antes = est(); hist = []
    while frame < frames:
        pc = reg[24]; ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame); hist.append(est())
            else: nxt += fd
    return antes, hist, mem
def dif(a, h):
    z = h[-1]; return {k: (a[k], z[k]) for k in a if a[k] != z[k]}
NOM = {0x2D: 'gema +30', 0x2E: 'gema +1', 0x2F: 'anillo +10 (cuenta)', 0x30: 'anillo +10', 0x31: 'energia 100', 0x32: 'bit0 de +15', 0x33: 'poder magico', 0x34: 'reloj arena', 0x35: 'matraz verde', 0x36: 'pocion',
       0x37: 'frasco azul', 0x38: 'escudo', 0x39: '+40', 0x3A: 'fin de nivel', 0x3E: 'bloquea bloques', 0x41: 'peligro', 0x42: 'peligro', 0x43: 'peligro'}
for c in sorted(NOM):
    base = {0xDE5A+17: c, 0xD3EF: 50, 0xD39A: 5, 0xD920: 1 if c == 0x34 else 0}
    a, h, m = go(base, 40)
    print('%02X %-22s' % (c, NOM[c]), dif(a, h))
print('--- pociones $33 consecutivas (1a: orbe, 2a: poder doble)')
a, h, m = go({0xDE5A+17: 0x33}, 20); print('1a', dif(a, h))
a2, h2, m2 = go({0xDE5A+17: 0x33, 0xD3BC: 0x08, 0xD3C0: 0xC0}, 20); print('2a', dif(a2, h2))
print('--- llave + puerta: la puerta $55/$56/$57 desaparece')
for key, door in ((0x3B, 0x55), (0x3C, 0x56), (0x3D, 0x57)):
    sim_pk = {0xDE5A+17: key, 0xDE5A+60: door}
    a, h, m = go(sim_pk, 120)
    print('llave %02X puerta %02X -> celda puerta antes/despues:' % (key, door), door, m[0xDE5A+60])
print('--- caducidad del escudo (+18) y del poder magico (+19)')
a, h, m = go({0xD3BC: 0x0A, 0xD3BF: 3, 0xD3C0: 3}, 80); print(a, '->', h[-1])
